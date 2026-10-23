from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_reranker.py"


def load_module():
    spec = importlib.util.spec_from_file_location("run_reranker", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_rerank_candidates_orders_scores_and_breaks_ties_by_chunk_id():
    reranker = load_module()
    candidates = [
        {"chunk_id": "chunk-c", "retrieval_text": "third"},
        {"chunk_id": "chunk-b", "retrieval_text": "second"},
        {"chunk_id": "chunk-a", "retrieval_text": "first"},
    ]

    ranking = reranker.rerank_candidates(
        "question",
        candidates,
        score_pairs=lambda pairs: [0.1, 0.5, 0.5],
    )

    assert ranking == [
        ("chunk-a", 0.5),
        ("chunk-b", 0.5),
        ("chunk-c", 0.1),
    ]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8"
    )


def test_run_experiment_rejects_absolute_run_id_before_creating_outputs(tmp_path):
    reranker = load_module()
    output_root = tmp_path / "outputs"

    with pytest.raises(ValueError, match="run_id must contain only"):
        reranker.run_experiment(
            run_id="/tmp/escape",
            hybrid_run_path=tmp_path / "missing-hybrid.jsonl",
            chunks_path=tmp_path / "missing-chunks.jsonl",
            golden_path=tmp_path / "missing-golden.jsonl",
            qrels_path=tmp_path / "missing-qrels.tsv",
            output_root=output_root,
            score_pairs=lambda pairs: [],
            count_pair_tokens=lambda pairs: [],
            model_id="model/test",
            model_revision="abc123",
            max_seq_length=512,
            batch_size=2,
            device="cpu",
            model_load_latency_ms=0.0,
        )

    assert not output_root.exists()


def test_run_experiment_writes_reranked_artifacts(tmp_path):
    reranker = load_module()
    chunks_path = tmp_path / "chunks.jsonl"
    golden_path = tmp_path / "golden.jsonl"
    qrels_path = tmp_path / "qrels.tsv"
    hybrid_path = tmp_path / "hybrid.jsonl"
    output_root = tmp_path / "outputs"
    write_jsonl(
        chunks_path,
        [
            {"chunk_id": "chunk-a", "retrieval_text": "relevant"},
            {"chunk_id": "chunk-b", "retrieval_text": "context"},
            {"chunk_id": "chunk-c", "retrieval_text": "other"},
            {"chunk_id": "chunk-d", "retrieval_text": "none"},
        ],
    )
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
        "q-1\t0\tchunk-a\t2\nq-1\t0\tchunk-b\t1\n", encoding="utf-8"
    )
    hybrid_rows = []
    for qid, question, answerability, chunk_ids in (
        ("q-1", "Question one?", "answerable", ["chunk-b", "chunk-a"]),
        ("q-2", "Question two?", "unanswerable", ["chunk-c", "chunk-d"]),
    ):
        for rank, chunk_id in enumerate(chunk_ids, start=1):
            hybrid_rows.append(
                {
                    "run_id": "hybrid_source",
                    "qid": qid,
                    "question": question,
                    "answerability": answerability,
                    "chunk_id": chunk_id,
                    "rank": rank,
                    "score": 1 / rank,
                    "bm25_rank": rank,
                    "dense_rank": rank,
                    "query_latency_serial_estimate_ms": 7.0,
                    "query_latency_parallel_estimate_ms": 5.0,
                }
            )
    write_jsonl(hybrid_path, hybrid_rows)

    def score_pairs(pairs):
        scores = {"relevant": 3.0, "context": 1.0, "other": 2.0, "none": 0.0}
        return [scores[pair[1]] for pair in pairs]

    summary = reranker.run_experiment(
        run_id="reranker_test",
        hybrid_run_path=hybrid_path,
        chunks_path=chunks_path,
        golden_path=golden_path,
        qrels_path=qrels_path,
        output_root=output_root,
        score_pairs=score_pairs,
        count_pair_tokens=lambda pairs: [10 for _ in pairs],
        model_id="model/test",
        model_revision="abc123",
        max_seq_length=512,
        batch_size=2,
        device="cpu",
        model_load_latency_ms=10.0,
        cutoffs=(1, 2),
    )

    rows = [
        json.loads(line)
        for line in (output_root / "runs/reranker_test.jsonl")
        .read_text()
        .splitlines()
    ]
    assert len(rows) == 4
    assert rows[0]["chunk_id"] == "chunk-a"
    assert rows[0]["source_rank"] == 2
    assert rows[0]["rerank_score"] == 3.0
    assert rows[0]["relevant_grade"] == 2
    assert rows[0]["query_latency_serial_estimate_ms"] >= 7.0
    assert rows[0]["query_latency_parallel_estimate_ms"] >= 5.0
    assert {row["chunk_id"] for row in rows[:2]} == {"chunk-a", "chunk-b"}

    metrics = (output_root / "metrics/reranker_test_metrics.csv").read_text()
    assert "precision,1,1.0,1" in metrics
    assert "recall,1,1.0,1" in metrics
    assert (output_root / "metrics/reranker_test_per_query.csv").exists()
    assert (output_root / "metrics/reranker_test_audit.json").exists()
    assert summary["method"] == "hybrid_cross_encoder_reranking"
    assert summary["source_run_id"] == "hybrid_source"
    assert summary["model_id"] == "model/test"
    assert summary["model_revision"] == "abc123"
    assert summary["candidate_depth"] == 2
    assert summary["truncated_pair_count"] == 0
    assert summary["metric_query_count"] == 1
    assert summary["qrels_sha256"]
