from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_hybrid_rrf.py"


def load_module():
    spec = importlib.util.spec_from_file_location("run_hybrid_rrf", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_rrf_sums_reciprocal_rank_contributions_across_rankings():
    hybrid = load_module()

    ranking = hybrid.reciprocal_rank_fusion(
        [["chunk-a", "chunk-b"], ["chunk-b", "chunk-c"]],
        k0=60,
        top_k=3,
    )

    assert [chunk_id for chunk_id, _ in ranking] == [
        "chunk-b",
        "chunk-a",
        "chunk-c",
    ]
    scores = dict(ranking)
    assert scores["chunk-b"] == 1 / 62 + 1 / 61
    assert scores["chunk-a"] == 1 / 61
    assert scores["chunk-c"] == 1 / 62


def test_rrf_counts_each_chunk_once_per_source_ranking():
    hybrid = load_module()

    ranking = hybrid.reciprocal_rank_fusion(
        [["chunk-a", "chunk-a"], ["chunk-b"]],
        k0=60,
        top_k=2,
    )

    assert ranking == [
        ("chunk-a", 1 / 61),
        ("chunk-b", 1 / 61),
    ]


def test_rrf_limits_each_source_ranking_to_declared_fusion_depth():
    hybrid = load_module()

    ranking = hybrid.reciprocal_rank_fusion(
        [
            ["chunk-a", "chunk-b", "chunk-shared-below-depth"],
            ["chunk-c", "chunk-d", "chunk-shared-below-depth"],
        ],
        k0=60,
        top_k=2,
    )

    assert ranking == [
        ("chunk-a", 1 / 61),
        ("chunk-c", 1 / 61),
    ]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8"
    )


def test_run_experiment_rejects_traversal_run_id_before_creating_outputs(tmp_path):
    hybrid = load_module()
    output_root = tmp_path / "outputs"

    with pytest.raises(ValueError, match="run_id must contain only"):
        hybrid.run_experiment(
            run_id="../escape",
            bm25_run_path=tmp_path / "missing-bm25.jsonl",
            dense_run_path=tmp_path / "missing-dense.jsonl",
            golden_path=tmp_path / "missing-golden.jsonl",
            qrels_path=tmp_path / "missing-qrels.tsv",
            output_root=output_root,
        )

    assert not output_root.exists()


def test_run_experiment_writes_evaluated_hybrid_artifacts(tmp_path):
    hybrid = load_module()
    golden_path = tmp_path / "golden.jsonl"
    qrels_path = tmp_path / "qrels.tsv"
    bm25_path = tmp_path / "bm25.jsonl"
    dense_path = tmp_path / "dense.jsonl"
    output_root = tmp_path / "outputs"
    write_jsonl(
        golden_path,
        [
            {
                "qid": "q-1",
                "question": "Question one?",
                "question_type": "factual",
                "answerability": "answerable",
            },
            {
                "qid": "q-2",
                "question": "Question two?",
                "question_type": "unanswerable",
                "answerability": "unanswerable",
            },
        ],
    )
    qrels_path.write_text(
        "q-1\t0\tchunk-a\t2\n"
        "q-1\t0\tchunk-b\t1\n",
        encoding="utf-8",
    )

    def rows(run_id: str, rankings: dict[str, list[str]], latency: float):
        questions = {"q-1": "Question one?", "q-2": "Question two?"}
        answerability = {"q-1": "answerable", "q-2": "unanswerable"}
        return [
            {
                "run_id": run_id,
                "qid": qid,
                "question": questions[qid],
                "answerability": answerability[qid],
                "chunk_id": chunk_id,
                "rank": rank,
                "score": 1.0 / rank,
                "query_latency_ms": latency,
            }
            for qid, chunks in rankings.items()
            for rank, chunk_id in enumerate(chunks, start=1)
        ]

    write_jsonl(
        bm25_path,
        rows("bm25_source", {"q-1": ["chunk-b", "chunk-a"], "q-2": ["chunk-c"]}, 2.0),
    )
    write_jsonl(
        dense_path,
        rows("dense_source", {"q-1": ["chunk-a", "chunk-c"], "q-2": ["chunk-d"]}, 5.0),
    )

    summary = hybrid.run_experiment(
        run_id="hybrid_test",
        bm25_run_path=bm25_path,
        dense_run_path=dense_path,
        golden_path=golden_path,
        qrels_path=qrels_path,
        output_root=output_root,
        k0=60,
        top_k=2,
        cutoffs=(1, 2),
    )

    run_rows = [
        json.loads(line)
        for line in (output_root / "runs/hybrid_test.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert len(run_rows) == 4
    assert run_rows[0]["chunk_id"] == "chunk-a"
    assert run_rows[0]["bm25_rank"] == 2
    assert run_rows[0]["dense_rank"] == 1
    assert run_rows[0]["relevant_grade"] == 2
    assert run_rows[0]["query_latency_serial_estimate_ms"] >= 7.0
    assert run_rows[0]["query_latency_parallel_estimate_ms"] >= 5.0

    metrics = (output_root / "metrics/hybrid_test_metrics.csv").read_text(
        encoding="utf-8"
    )
    assert "precision,1,1.0,1" in metrics
    assert "recall,1,1.0,1" in metrics
    assert (output_root / "metrics/hybrid_test_per_query.csv").exists()
    assert (output_root / "metrics/hybrid_test_audit.json").exists()
    assert summary["method"] == "hybrid_rrf"
    assert summary["source_run_ids"] == ["bm25_source", "dense_source"]
    assert summary["k0"] == 60
    assert summary["fusion_depth"] == 2
    assert summary["metric_query_count"] == 1
    assert summary["qrels_sha256"]


def test_build_incremental_pool_keeps_only_pairs_absent_from_prior_pool(tmp_path):
    hybrid = load_module()
    run_path = tmp_path / "hybrid.jsonl"
    qrels_path = tmp_path / "qrels.tsv"
    prior_pool_path = tmp_path / "prior_pool.jsonl"
    pool_path = tmp_path / "pool.jsonl"
    report_path = tmp_path / "report.json"
    write_jsonl(
        run_path,
        [
            {
                "run_id": "hybrid",
                "qid": "q-1",
                "question": "Question?",
                "answerability": "answerable",
                "chunk_id": "judged",
                "rank": 1,
                "score": 0.03,
                "bm25_rank": 1,
                "dense_rank": 2,
            },
            {
                "run_id": "hybrid",
                "qid": "q-1",
                "question": "Question?",
                "answerability": "answerable",
                "chunk_id": "new",
                "rank": 2,
                "score": 0.02,
                "bm25_rank": None,
                "dense_rank": 1,
            },
        ],
    )
    qrels_path.write_text("q-1\t0\tjudged\t2\n", encoding="utf-8")
    write_jsonl(
        prior_pool_path,
        [{"qid": "q-1", "chunk_id": "judged"}],
    )

    report = hybrid.build_incremental_pool(
        run_path=run_path,
        qrels_path=qrels_path,
        prior_pool_path=prior_pool_path,
        pool_path=pool_path,
        report_path=report_path,
    )

    rows = [json.loads(line) for line in pool_path.read_text().splitlines()]
    assert [row["chunk_id"] for row in rows] == ["new"]
    assert report["candidate_count"] == 2
    assert report["existing_prior_pool_count"] == 1
    assert report["new_candidate_count"] == 1
    assert report["new_candidate_qid_count"] == 1
    assert json.loads(report_path.read_text()) == report
