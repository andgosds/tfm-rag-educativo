from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/compare_pooled_retrieval.py"


def load_module():
    spec = importlib.util.spec_from_file_location("compare_pooled_retrieval", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def test_comparison_reports_metric_deltas_and_full_evidence_coverage(tmp_path):
    compare = load_module()
    paths = {}
    for method, baseline, pooled in (
        ("bm25", 0.2, 0.5),
        ("dense", 0.4, 0.5),
    ):
        paths[f"{method}_baseline"] = tmp_path / f"{method}_baseline.csv"
        paths[f"{method}_pooled"] = tmp_path / f"{method}_pooled.csv"
        write_csv(
            paths[f"{method}_baseline"],
            [{"run_id": f"{method}_old", "metric": "recall", "k": 5, "value": baseline, "query_count": 1}],
        )
        write_csv(
            paths[f"{method}_pooled"],
            [{"run_id": f"{method}_new", "metric": "recall", "k": 5, "value": pooled, "query_count": 1}],
        )
        paths[f"{method}_per_query"] = tmp_path / f"{method}_per_query.csv"
    write_csv(
        paths["bm25_per_query"],
        [{"qid": "q-1", "answerability": "answerable", "relevant_count": 2, "recall_at_5": 1.0}],
    )
    write_csv(
        paths["dense_per_query"],
        [{"qid": "q-1", "answerability": "answerable", "relevant_count": 2, "recall_at_5": 0.5}],
    )
    output = tmp_path / "comparison.json"

    result = compare.build_comparison(
        bm25_baseline_metrics=paths["bm25_baseline"],
        dense_baseline_metrics=paths["dense_baseline"],
        bm25_pooled_metrics=paths["bm25_pooled"],
        dense_pooled_metrics=paths["dense_pooled"],
        bm25_pooled_per_query=paths["bm25_per_query"],
        dense_pooled_per_query=paths["dense_per_query"],
        output_path=output,
    )

    metric = result["metrics"][0]
    assert metric == {
        "metric": "recall",
        "k": 5,
        "bm25_baseline": 0.2,
        "bm25_pooled": 0.5,
        "bm25_delta": 0.3,
        "dense_baseline": 0.4,
        "dense_pooled": 0.5,
        "dense_delta": 0.1,
        "pooled_difference_dense_minus_bm25": 0.0,
        "pooled_winner": "tie",
    }
    assert result["full_evidence_coverage"] == [
        {
            "method": "bm25",
            "k": 5,
            "fully_covered_query_count": 1,
            "metric_query_count": 1,
            "rate": 1.0,
        },
        {
            "method": "dense",
            "k": 5,
            "fully_covered_query_count": 0,
            "metric_query_count": 1,
            "rate": 0.0,
        },
    ]
    assert json.loads(output.read_text(encoding="utf-8")) == result
