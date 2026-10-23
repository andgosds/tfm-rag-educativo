"""Calcula las métricas de recuperación de v3 contra los qrels definitivos.

Definiciones exactas del pre-registro §5, sin alterar:

- **Recall@k** — proporción de la evidencia de grado 2 conocida que aparece en el top-k.
  Solo el grado 2 cuenta como relevante: recuperar contexto de grado 1 no es acceso suficiente.
- **Precision@k** — proporción de los resultados del top-k que son de grado 2.
- **MRR@k** — posición del primer fragmento de grado 2.
- **nDCG@k** — calidad del orden con la escala graduada 0/1/2, ganancia 2^rel − 1 y descuento
  logarítmico. Es la única que conserva la gradación entera.

Se calculan a k=5 y k=10. La unidad de análisis es la **pregunta base**; las dos formulaciones
de una misma pareja se promedian entre sí antes de agregarse, conforme al §4, para no contar
una misma necesidad informativa dos veces.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

from output_safety import guard_cli_outputs

METRICS = ("recall", "precision", "mrr", "ndcg")


def sha256(path: Path) -> str:
    """Calcula la huella SHA-256 del archivo para registrar su procedencia."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: list[dict]) -> None:
    """Crea un CSV nuevo con las columnas de la primera fila."""
    if not rows:
        raise ValueError(f"no rows for {path.name}")
    with path.open("x", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def aggregate(rows: list[dict], bases: set[str]) -> list[dict]:
    """Promedia las métricas de las preguntas base seleccionadas por método y corte."""
    groups = defaultdict(list)
    for row in rows:
        if row["base_qid"] in bases:
            groups[(row["method"], int(row["k"]))].append(row)
    return [dict(method=method, k=k, n_base=len(group),
                 **{metric: sum(float(r[metric]) for r in group) / len(group)
                    for metric in METRICS})
            for (method, k), group in sorted(groups.items())]


def load_jsonl(path: Path) -> list[dict]:
    """Carga los registros JSONL sin incluir líneas vacías."""
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def metrics_for(ranked: list[int], k: int, n_relevant: int,
                *, qrel_grades: list[int]) -> dict[str, float]:
    """IDCG uses all base-question qrels, independent of retrieved candidates."""
    top = ranked[:k]
    hits2 = sum(1 for g in top if g == 2)
    first = next((i + 1 for i, g in enumerate(top) if g == 2), None)
    dcg = sum((2 ** g - 1) / math.log2(i + 2) for i, g in enumerate(top))
    ideal = sorted(qrel_grades, reverse=True)[:k]
    idcg = sum((2 ** g - 1) / math.log2(i + 2) for i, g in enumerate(ideal))
    return {
        "recall": (hits2 / n_relevant) if n_relevant else 0.0,
        "precision": hits2 / k if top else 0.0,
        "mrr": (1.0 / first) if first else 0.0,
        "ndcg": (dcg / idcg) if idcg > 0 else 0.0,
    }


def main() -> int:
    """Calcula métricas pareadas y exporta la corrección y sus cohortes de sensibilidad."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--qrels", type=Path, required=True)
    ap.add_argument("--methods", default="bm25,dense,rrf,rerank")
    ap.add_argument("--output-dir", type=Path, required=True,
                    help="Fresh directory under outputs/local_runs; existing directories are refused.")
    args = ap.parse_args()
    guard_cli_outputs(SimpleNamespace(output_root=args.output_dir), script="evaluate_retrieval_v3")
    qrel_rows = load_jsonl(args.qrels)
    qrels = {(r["base_qid"], r["chunk_id"]): r["grade"] for r in qrel_rows}
    if len(qrels) != len(qrel_rows) or any(g not in (0, 1, 2) for g in qrels.values()):
        raise ValueError("qrels must have unique base/chunk keys and grades 0/1/2")
    ks = (5, 10)
    methods = args.methods.split(",")
    if not methods or len(set(methods)) != len(methods) or set(methods) - {"bm25", "dense", "rrf", "rerank"}:
        raise ValueError("methods must be unique supported method names")
    inputs = {"qrels": dict(filename=args.qrels.name, sha256=sha256(args.qrels))}
    expected_cells = None
    n_run_rows = {}
    per_query: list[dict] = []
    for method in methods:
        path = args.run_dir / "runs" / f"explicitness_v3_{method}.jsonl"
        inputs[method] = dict(filename=path.name, sha256=sha256(path))
        rows = load_jsonl(path)
        n_run_rows[method] = len(rows)
        by_qid: dict[str, list[dict]] = defaultdict(list)
        for r in rows:
            by_qid[r["qid"]].append(r)
        for qid, rr in by_qid.items():
            rr.sort(key=lambda r: r["rank"])
            base = rr[0]["base_qid"]
            expl = rr[0]["explicitness"]
            if expl not in ("explicit", "implicit") or any(r["base_qid"] != base or r["explicitness"] != expl for r in rr):
                raise ValueError(f"inconsistent formulation metadata: {qid}")
            if len({r["rank"] for r in rr}) != len(rr) or len({r["chunk_id"] for r in rr}) != len(rr):
                raise ValueError(f"duplicate rank/chunk: {qid}")
            if not any(b == base for b, _ in qrels):
                raise ValueError(f"missing qrels for {base}")
            grades = [qrels.get((base, c["chunk_id"]), 0) for c in rr]
            # evidencia de grado 2 CONOCIDA para esta pregunta base (unión de las dos formulaciones)
            n_rel = sum(1 for (b, _), g in qrels.items() if b == base and g == 2)
            for k in ks:
                m = metrics_for(grades, k, n_rel,
                                qrel_grades=[g for (b, _), g in qrels.items() if b == base])
                per_query.append(dict(method=method, qid=qid, base_qid=base, explicitness=expl,
                                      k=k, n_relevant=n_rel, **m))
        cells = {(r["base_qid"], r["explicitness"]) for r in per_query if r["method"] == method}
        if len(cells) * 2 != sum(r["method"] == method for r in per_query):
            raise ValueError("duplicate formulation cell")
        if cells != {(base, side) for base, _ in cells for side in ("explicit", "implicit")}:
            raise ValueError("incomplete formulation pair")
        if expected_cells is not None and cells != expected_cells:
            raise ValueError("methods have different paired question coverage")
        expected_cells = cells

    # agregación: primero se promedian las dos formulaciones de cada pareja (§4),
    # después se promedian las parejas
    by_base: dict[tuple, list[dict]] = defaultdict(list)
    for r in per_query:
        by_base[(r["method"], r["base_qid"], r["k"])].append(r)
    rows_out = []
    for (method, base, k), rr in sorted(by_base.items()):
        row = dict(method=method, base_qid=base, k=k, n_formulaciones=len(rr),
                   n_relevant=rr[0]["n_relevant"])
        for m in METRICS:
            row[m] = sum(x[m] for x in rr) / len(rr)
        rows_out.append(row)

    bases = {r["base_qid"] for r in rows_out}
    eligible = {r["base_qid"] for r in rows_out if r["n_relevant"] > 0}
    cohorts = {name: dict(n_base=len(subset), base_qids=sorted(subset),
                         aggregates=aggregate(rows_out, subset))
               for name, subset in (("all_pairs", bases), ("grade2_eligible", eligible))}
    before = []
    historical = args.run_dir / "retrieval_metrics_v3/per_base.csv"
    if historical.exists():
        inputs["historical_per_base"] = dict(filename=historical.name, sha256=sha256(historical))
        with historical.open(encoding="utf-8", newline="") as fh:
            legacy_rows = list(csv.DictReader(fh))
        if {(r["method"], r["base_qid"], int(r["k"])) for r in legacy_rows} != set(by_base):
            raise ValueError("historical baseline coverage does not match corrected coverage")
        old = {(r["method"], r["k"]): r for r in aggregate(legacy_rows, bases)}
        for row in cohorts["all_pairs"]["aggregates"]:
            for metric in METRICS:
                previous = old[(row["method"], row["k"])][metric]
                before.append(dict(method=row["method"], k=row["k"], metric=metric,
                                   before=previous, after=row[metric], delta=row[metric] - previous,
                                   n_base=len(bases)))
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=False)
    write_csv(out / "per_query.csv", per_query)
    write_csv(out / "per_base.csv", rows_out)
    summary_rows = [dict(cohort=name, **row) for name, cohort in cohorts.items() for row in cohort["aggregates"]]
    write_csv(out / "aggregate_metrics.csv", summary_rows)
    if before:
        write_csv(out / "before_after.csv", before)
    report = dict(schema_version=1, correction="R01: global qrel IDCG independent of retrieved candidates",
                  unit="base question; mean of two formulations, then macro mean over base questions",
                  definitions=dict(recall="grade-2 hits / all known grade-2 qrels for base",
                                   precision="grade-2 hits / k, even if fewer than k retrieved",
                                   mrr="reciprocal rank of first grade-2 hit in top-k",
                                   ndcg="gain 2^grade-1; log2(rank+1); IDCG over ALL base qrels at k",
                                   no_grade2="legacy all-pairs Recall/MRR zero retained; separate grade2-eligible sensitivity",
                                   no_positive_gain="nDCG zero when global IDCG zero"),
                  qrel_scope="base-question union shared across formulations and methods; not variant-specific",
                  unjudged_policy="unjudged run chunks scored as 0 by frozen convention; does not assert true irrelevance",
                  cohorts=cohorts, no_grade2_base_qids=sorted(bases - eligible),
                  counts=dict(qrels=len(qrels), run_rows=n_run_rows, per_query=len(per_query), per_base=len(rows_out)),
                  before_after=before, before_source="frozen historical per_base.csv" if before else "unavailable",
                  inputs=inputs, outputs={p.name: sha256(p) for p in sorted(out.iterdir())},
                  interpretation="Descriptive correction and sensitivity, not hypothesis confirmation.")
    (out / "retrieval_correction_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"consultas: {len({r['qid'] for r in per_query})} | parejas: {len({r['base_qid'] for r in rows_out})}")
    print()
    print(f"{'método':8s} " + " ".join(f"{m}@{k}" for k in ks for m in ("R", "P", "MRR", "nDCG")))
    for method in args.methods.split(","):
        cells = []
        for k in ks:
            sub = [r for r in rows_out if r["method"] == method and r["k"] == k]
            for m in ("recall", "precision", "mrr", "ndcg"):
                cells.append(f"{sum(r[m] for r in sub)/len(sub):.3f}")
        print(f"{method:8s} " + " ".join(cells))
    print(f"\nsalidas: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
