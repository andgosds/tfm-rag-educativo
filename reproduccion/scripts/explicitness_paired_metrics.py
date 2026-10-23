"""Métricas emparejadas de recuperación de la campaña de explicitud (v2).

Evalúa las cuatro runs de `outputs/explicitness_v2/runs/` (BM25, dense E5,
RRF híbrido, RRF+reranking) contra `qrels_explicitness_v2.tsv` con las
definiciones fijadas para el TFM: Recall y MRR usan solo grado 2 como
relevante; nDCG conserva toda la escala 0/1/2 con descuento estándar.

La comparación es emparejada: cada formulación (qid de variante) tiene su
qrels propio derivado de la misma base de evidencias, y las diferencias
explícita–implícita se calculan por pregunta base (misma técnica, par
emparejado). Salidas en outputs/local_runs/explicitness_paired_metrics/.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

RUN_FILES = {
    "bm25": "explicitness_v2_bm25.jsonl",
    "dense": "explicitness_v2_dense.jsonl",
    "rrf": "explicitness_v2_rrf.jsonl",
    "rerank": "explicitness_v2_rerank.jsonl",
}
K_LIST = (5, 10)
BASE_QIDS = (1, 2, 3, 6, 12, 14, 16)


def _sha256(path: Path) -> str:
    """Calcula la huella SHA-256 de un archivo de entrada o salida."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _atomic_write(path: Path, text: str) -> None:
    """Sustituye el archivo de destino mediante una escritura temporal."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def _dcg(grades: list[int]) -> float:
    """Calcula la ganancia acumulada con descuento logarítmico por posición."""
    return sum((2 ** grade - 1) / math.log2(rank + 1) for rank, grade in enumerate(grades, start=1))


def load_qrels(path: Path) -> dict[str, dict[str, int]]:
    """Carga los grados del TSV de qrels por formulación y fragmento."""
    qrels: dict[str, dict[str, int]] = defaultdict(dict)
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        qid, _, chunk_id, grade = line.split("\t")
        qrels[qid][chunk_id] = int(grade)
    return dict(qrels)


def load_rankings(runs_dir: Path) -> dict[str, dict[str, list[str]]]:
    """{method: {qid: [chunk_id ordenado por rank]}}."""
    rankings: dict[str, dict[str, list[str]]] = {}
    for method, filename in RUN_FILES.items():
        path = runs_dir / filename
        by_qid: dict[str, list[tuple[int, str]]] = defaultdict(list)
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            by_qid[row["qid"]].append((int(row["rank"]), row["chunk_id"]))
        rankings[method] = {
            qid: [chunk_id for _, chunk_id in sorted(entries)] for qid, entries in by_qid.items()
        }
    return rankings


def evaluate_ranking(ranking: list[str], qrels: dict[str, int], *, k: int) -> dict[str, float | None]:
    """Mismas definiciones que run_bm25.evaluate_ranking: Recall/MRR en grado 2, nDCG 0/1/2."""
    strict_relevant = {c for c, g in qrels.items() if g == 2}
    if not strict_relevant:
        return {"recall": None, "mrr": None, "ndcg": None}
    retrieved = ranking[:k]
    hits = [c for c in retrieved if c in strict_relevant]
    first = next((r for r, c in enumerate(retrieved, 1) if c in strict_relevant), None)
    grades = [qrels.get(c, 0) for c in retrieved]
    ideal_dcg = _dcg(sorted(qrels.values(), reverse=True)[:k])
    return {
        "recall": len(hits) / len(strict_relevant),
        "mrr": 0.0 if first is None else 1.0 / first,
        "ndcg": 0.0 if ideal_dcg == 0 else _dcg(grades) / ideal_dcg,
    }


def compute_metrics(
    rankings: dict[str, dict[str, list[str]]], qrels: dict[str, dict[str, int]]
) -> dict[str, dict[str, dict[str, dict[str, float | None]]]]:
    """{method: {qid: {f'{metric}@{k}': value}}}."""
    out: dict[str, dict[str, dict[str, dict[str, float | None]]]] = {}
    for method, by_qid in rankings.items():
        per_qid: dict[str, dict[str, dict[str, float | None]]] = {}
        for qid, ranking in by_qid.items():
            if qid not in qrels:
                raise ValueError(f"qid in run without qrels: {method}/{qid}")
            per_qid[qid] = {
                f"{metric}@{k}": value
                for k in K_LIST
                for metric, value in evaluate_ranking(ranking, qrels[qid], k=k).items()
            }
        out[method] = per_qid
    return out


def paired_differences(
    metrics: dict[str, dict[str, dict[str, dict[str, float | None]]]],
) -> dict[str, Any]:
    """Diferencias implícita − explícita por pregunta base y agregados."""
    rows: list[dict[str, Any]] = []
    sums: dict[tuple[str, str], dict[str, list[float]]] = defaultdict(lambda: {"explicit": [], "implicit": []})
    for method, by_qid in metrics.items():
        for n in BASE_QIDS:
            explicit = by_qid.get(f"q-v1-{n:03d}__explicit")
            implicit = by_qid.get(f"q-v1-{n:03d}__implicit")
            if explicit is None or implicit is None:
                continue
            for mkey in explicit:
                explicit_value = explicit[mkey]
                implicit_value = implicit.get(mkey)
                if explicit_value is None or implicit_value is None:
                    continue
                rows.append({
                    "method": method,
                    "base_qid": f"q-v1-{n:03d}",
                    "metric": mkey,
                    "explicit": round(explicit_value, 4),
                    "implicit": round(implicit_value, 4),
                    "diff_implicit_minus_explicit": round(implicit_value - explicit_value, 4),
                })
                sums[(method, mkey)]["explicit"].append(explicit_value)
                sums[(method, mkey)]["implicit"].append(implicit_value)
    mean_rows: list[dict[str, Any]] = []
    for (method, mkey), sides in sums.items():
        pairs = zip(sides["explicit"], sides["implicit"])
        mean_rows.append({
            "method": method,
            "metric": mkey,
            "mean_explicit": round(mean(sides["explicit"]), 4),
            "mean_implicit": round(mean(sides["implicit"]), 4),
            "mean_diff_implicit_minus_explicit": round(mean(i - e for e, i in pairs), 4),
        })
    return {"per_question": rows, "means": mean_rows}


def run_paired_metrics(
    *,
    runs_dir: Path,
    qrels_path: Path,
    output_csv_path: Path,
    output_json_path: Path,
    report_path: Path,
) -> dict[str, Any]:
    """Calcula las diferencias pareadas y guarda tablas e informe de procedencia."""
    qrels = load_qrels(qrels_path)
    rankings = load_rankings(runs_dir)
    metrics = compute_metrics(rankings, qrels)
    import csv

    world = paired_differences(metrics)
    per_question = world["per_question"]
    fieldnames = list(per_question[0].keys())
    output_csv_path.parent.mkdir(parents=True, exist_ok=True)
    with output_csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(per_question)
    report = {
        "protocol_id": "explicitness_paired_retrieval_metrics_v2",
        "metric_definitions": {
            "recall": "grade 2 only (binary relevant)",
            "mrr": "grade 2 only (binary relevant)",
            "ndcg": "graded 0/1/2, standard discount",
            "k_values": list(K_LIST),
        },
        "qrels_path": str(qrels_path),
        "qrels_sha256": _sha256(qrels_path),
        "runs_directory": str(runs_dir),
        "runs_sha256": {name: _sha256(runs_dir / fname) for name, fname in RUN_FILES.items()},
        "paired_differences_note": "implicit minus explicit, per base question; means over 7 base questions",
        "output_csv_path": str(output_csv_path),
        "output_json_path": str(output_json_path),
        "output_csv_sha256": _sha256(output_csv_path),
    }
    _atomic_write(output_json_path, json.dumps({"report": report, "metrics_by_qid": metrics, "means": world["means"]}, ensure_ascii=False, indent=2) + "\n")
    _atomic_write(report_path, json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return report


def build_parser(root: Path) -> argparse.ArgumentParser:
    """Define las rutas de entrada y salida del análisis pareado v2."""
    parser = argparse.ArgumentParser(description="Paired retrieval metrics for explicitness v2")
    parser.add_argument("--runs-dir", type=Path, default=root / "outputs/explicitness_v2/runs")
    parser.add_argument("--qrels", type=Path, default=root / "outputs/local_runs/explicitness_qrels_v2/qrels_explicitness_v2.tsv")
    parser.add_argument("--output", type=Path, default=root / "outputs/local_runs/explicitness_paired_metrics/paired_diff_by_question.csv")
    parser.add_argument("--output-json", type=Path, default=root / "outputs/local_runs/explicitness_paired_metrics/paired_metrics_full.json")
    parser.add_argument("--report", type=Path, default=root / "outputs/local_runs/explicitness_paired_metrics/paired_metrics_report.json")
    return parser


def main() -> int:
    """Ejecuta las métricas pareadas v2 con protección de los archivos de salida."""
    root = Path(__file__).resolve().parents[1]
    args = build_parser(root).parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="explicitness_paired_metrics")
    report = run_paired_metrics(
        runs_dir=args.runs_dir,
        qrels_path=args.qrels,
        output_csv_path=args.output,
        output_json_path=args.output_json,
        report_path=args.report,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
