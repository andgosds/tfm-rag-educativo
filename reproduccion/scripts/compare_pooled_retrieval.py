from __future__ import annotations

import argparse
import csv
import json
import os
import tempfile
from pathlib import Path
from typing import Any


def _read_metrics(path: Path) -> dict[tuple[str, int], float]:
    """Indexa las métricas agregadas del CSV por nombre y profundidad de recuperación."""
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return {(row["metric"], int(row["k"])): float(row["value"]) for row in rows}


def _read_per_query(path: Path) -> list[dict[str, str]]:
    """Lee las métricas por pregunta conservando los campos del CSV como texto."""
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _atomic_write(path: Path, content: str) -> None:
    """Escribe el informe mediante un temporal sincronizado y reemplazo atómico."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def _rounded(value: float) -> float:
    """Redondea las diferencias de métricas a doce decimales."""
    return round(value, 12)


def build_comparison(
    *,
    bm25_baseline_metrics: Path,
    dense_baseline_metrics: Path,
    bm25_pooled_metrics: Path,
    dense_pooled_metrics: Path,
    bm25_pooled_per_query: Path,
    dense_pooled_per_query: Path,
    output_path: Path,
) -> dict[str, Any]:
    """Compara BM25 y recuperación densa antes y después de ampliar los qrels."""
    metric_sets = {
        "bm25_baseline": _read_metrics(bm25_baseline_metrics),
        "dense_baseline": _read_metrics(dense_baseline_metrics),
        "bm25_pooled": _read_metrics(bm25_pooled_metrics),
        "dense_pooled": _read_metrics(dense_pooled_metrics),
    }
    keys = set(metric_sets["bm25_baseline"])
    if any(set(values) != keys for values in metric_sets.values()):
        raise ValueError("metric files do not contain the same metric/cutoff keys")

    metric_rows: list[dict[str, Any]] = []
    for metric, cutoff in sorted(keys, key=lambda item: (item[1], item[0])):
        bm25_baseline = metric_sets["bm25_baseline"][(metric, cutoff)]
        dense_baseline = metric_sets["dense_baseline"][(metric, cutoff)]
        bm25_pooled = metric_sets["bm25_pooled"][(metric, cutoff)]
        dense_pooled = metric_sets["dense_pooled"][(metric, cutoff)]
        difference = _rounded(dense_pooled - bm25_pooled)
        winner = "tie" if difference == 0 else ("dense" if difference > 0 else "bm25")
        metric_rows.append(
            {
                "metric": metric,
                "k": cutoff,
                "bm25_baseline": bm25_baseline,
                "bm25_pooled": bm25_pooled,
                "bm25_delta": _rounded(bm25_pooled - bm25_baseline),
                "dense_baseline": dense_baseline,
                "dense_pooled": dense_pooled,
                "dense_delta": _rounded(dense_pooled - dense_baseline),
                "pooled_difference_dense_minus_bm25": difference,
                "pooled_winner": winner,
            }
        )

    coverage_rows: list[dict[str, Any]] = []
    for method, path in (
        ("bm25", bm25_pooled_per_query),
        ("dense", dense_pooled_per_query),
    ):
        rows = _read_per_query(path)
        metric_rows_for_coverage = [
            row
            for row in rows
            if row["answerability"] == "answerable" and int(row["relevant_count"]) > 0
        ]
        recall_cutoffs = sorted(
            int(field.removeprefix("recall_at_"))
            for field in rows[0]
            if field.startswith("recall_at_")
        )
        for cutoff in recall_cutoffs:
            fully_covered = sum(
                float(row[f"recall_at_{cutoff}"]) == 1.0
                for row in metric_rows_for_coverage
            )
            query_count = len(metric_rows_for_coverage)
            coverage_rows.append(
                {
                    "method": method,
                    "k": cutoff,
                    "fully_covered_query_count": fully_covered,
                    "metric_query_count": query_count,
                    "rate": fully_covered / query_count if query_count else 0.0,
                }
            )

    result = {
        "comparison_id": "bm25_dense_before_after_pooled_qrels_v1_22q",
        "metrics": metric_rows,
        "full_evidence_coverage": coverage_rows,
        "inputs": {
            "bm25_baseline_metrics": str(bm25_baseline_metrics),
            "dense_baseline_metrics": str(dense_baseline_metrics),
            "bm25_pooled_metrics": str(bm25_pooled_metrics),
            "dense_pooled_metrics": str(dense_pooled_metrics),
            "bm25_pooled_per_query": str(bm25_pooled_per_query),
            "dense_pooled_per_query": str(dense_pooled_per_query),
        },
    }
    _atomic_write(output_path, json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    return result


def build_parser(root: Path) -> argparse.ArgumentParser:
    """Define los CSV de métricas y la salida del contraste de qrels ampliados."""
    metrics = root / "outputs/metrics"
    parser = argparse.ArgumentParser(description="Compare BM25 and dense before and after pooled qrels")
    parser.add_argument("--bm25-baseline", type=Path, default=metrics / "bm25_v1_22q_metrics.csv")
    parser.add_argument("--dense-baseline", type=Path, default=metrics / "dense_e5_base_v2_22q_metrics.csv")
    parser.add_argument("--bm25-pooled", type=Path, default=metrics / "bm25_pooled_v1_22q_metrics.csv")
    parser.add_argument("--dense-pooled", type=Path, default=metrics / "dense_e5_base_v2_pooled_v1_22q_metrics.csv")
    parser.add_argument("--bm25-per-query", type=Path, default=metrics / "bm25_pooled_v1_22q_per_query.csv")
    parser.add_argument("--dense-per-query", type=Path, default=metrics / "dense_e5_base_v2_pooled_v1_22q_per_query.csv")
    parser.add_argument("--output", type=Path, default=metrics / "retrieval_comparison_bm25_dense_pooled_22q.json")
    return parser


def main() -> int:
    """Exporta la comparación de métricas y cobertura completa de evidencia."""
    root = Path(__file__).resolve().parents[1]
    args = build_parser(root).parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="compare_pooled_retrieval")
    result = build_comparison(
        bm25_baseline_metrics=args.bm25_baseline,
        dense_baseline_metrics=args.dense_baseline,
        bm25_pooled_metrics=args.bm25_pooled,
        dense_pooled_metrics=args.dense_pooled,
        bm25_pooled_per_query=args.bm25_per_query,
        dense_pooled_per_query=args.dense_per_query,
        output_path=args.output,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
