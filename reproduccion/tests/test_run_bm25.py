from __future__ import annotations

import importlib.util
import csv
import json
import math
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_bm25.py"


def load_bm25():
    spec = importlib.util.spec_from_file_location("run_bm25", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_bm25_ranks_matching_document_with_expected_score():
    bm25 = load_bm25()
    index = bm25.BM25Index(
        {
            "chunk-b": "banana carrot",
            "chunk-a": "Apple, apple! banana.",
        },
        k1=1.5,
        b=0.75,
    )

    ranking = index.rank("APPLE", top_k=2)

    expected_idf = math.log(1 + (2 - 1 + 0.5) / (1 + 0.5))
    expected_tf = (2 * (1.5 + 1)) / (2 + 1.5 * (1 - 0.75 + 0.75 * 3 / 2.5))
    assert ranking[0][0] == "chunk-a"
    assert ranking[0][1] == pytest.approx(expected_idf * expected_tf)
    assert ranking[1] == ("chunk-b", 0.0)


def test_evaluate_ranking_uses_grade2_for_binary_metrics_and_grades_for_ndcg():
    bm25 = load_bm25()
    ranking = ["chunk-grade1", "chunk-x", "chunk-grade2"]
    qrels = {"chunk-grade2": 2, "chunk-grade1": 1}

    metrics = bm25.evaluate_ranking(ranking, qrels, k=2)

    expected_dcg = 1.0
    expected_idcg = 3 + 1 / math.log2(3)
    assert metrics == {
        "precision": pytest.approx(0.0),
        "recall": pytest.approx(0.0),
        "mrr": pytest.approx(0.0),
        "ndcg": pytest.approx(expected_dcg / expected_idcg),
    }
    assert bm25.evaluate_ranking(ranking, {}, k=2) == {
        "precision": None,
        "recall": None,
        "mrr": None,
        "ndcg": None,
    }


def test_run_experiment_writes_rankings_qrels_and_answerable_metrics(tmp_path):
    bm25 = load_bm25()
    chunks_path = tmp_path / "chunks.jsonl"
    chunks_path.write_text(
        "\n".join(
            json.dumps(record)
            for record in [
                {"chunk_id": "chunk-1", "retrieval_text": "Apples are fruit."},
                {"chunk_id": "chunk-2", "retrieval_text": "Carrots are vegetables."},
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    golden_path = tmp_path / "golden.jsonl"
    golden_path.write_text(
        "\n".join(
            json.dumps(record)
            for record in [
                {
                    "qid": "q-v1-001",
                    "question": "Which document mentions apples?",
                    "answerability": "answerable",
                    "annotation_status": "adjudicated",
                    "evidence": [
                        {"chunk_id": "chunk-1", "relevance_grade": 2}
                    ],
                },
                {
                    "qid": "q-v1-002",
                    "question": "What value is reported for pears?",
                    "answerability": "unanswerable",
                    "annotation_status": "adjudicated",
                    "evidence": [],
                },
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    output_root = tmp_path / "outputs"
    qrels_path = tmp_path / "qrels.tsv"

    summary = bm25.run_experiment(
        run_id="bm25_test",
        chunks_path=chunks_path,
        golden_path=golden_path,
        output_root=output_root,
        qrels_path=qrels_path,
        k1=1.5,
        b=0.75,
        top_k=2,
        cutoffs=(1, 2),
    )

    run_rows = [
        json.loads(line)
        for line in (output_root / "runs" / "bm25_test.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    aggregate_rows = list(
        csv.DictReader(
            (output_root / "metrics" / "bm25_test_metrics.csv").open(
                encoding="utf-8", newline=""
            )
        )
    )
    per_query_rows = list(
        csv.DictReader(
            (output_root / "metrics" / "bm25_test_per_query.csv").open(
                encoding="utf-8", newline=""
            )
        )
    )

    assert len(run_rows) == 4
    assert run_rows[0]["run_id"] == "bm25_test"
    assert run_rows[0]["qid"] == "q-v1-001"
    assert run_rows[0]["chunk_id"] == "chunk-1"
    assert run_rows[0]["relevant_grade"] == 2
    assert qrels_path.read_text(encoding="utf-8") == "q-v1-001\t0\tchunk-1\t2\n"
    recall_at_1 = next(
        row for row in aggregate_rows if row["metric"] == "recall" and row["k"] == "1"
    )
    assert float(recall_at_1["value"]) == pytest.approx(1.0)
    assert recall_at_1["query_count"] == "1"
    assert per_query_rows[1]["answerability"] == "unanswerable"
    assert per_query_rows[1]["recall_at_1"] == ""
    assert summary["query_count"] == 2
    assert summary["metric_query_count"] == 1
    assert summary["run_id"] == "bm25_test"
    assert summary["binary_relevance_grade"] == 2
    assert summary["ndcg_relevance_grades"] == [0, 1, 2]


def test_cli_defaults_to_current_22q_run():
    bm25 = load_bm25()
    root = Path("/project")

    args = bm25.build_parser(root).parse_args([])

    assert args.run_id == "bm25_v1_22q"
    assert args.qrels == root / "data/golden/qrels_bm25_v1_22q.tsv"
    assert args.qrels_input is None


def test_run_experiment_uses_external_qrels_without_scoring_unanswerable_queries(tmp_path):
    bm25 = load_bm25()
    chunks_path = tmp_path / "chunks.jsonl"
    chunks_path.write_text(
        "".join(
            json.dumps(row) + "\n"
            for row in [
                {"chunk_id": "chunk-a", "retrieval_text": "alpha evidence"},
                {"chunk_id": "chunk-b", "retrieval_text": "beta correction"},
            ]
        ),
        encoding="utf-8",
    )
    golden_path = tmp_path / "golden.jsonl"
    golden_path.write_text(
        "".join(
            json.dumps(row) + "\n"
            for row in [
                {
                    "qid": "q-001",
                    "question": "alpha",
                    "answerability": "answerable",
                    "annotation_status": "adjudicated",
                    "evidence": [],
                },
                {
                    "qid": "q-002",
                    "question": "beta",
                    "answerability": "unanswerable",
                    "annotation_status": "adjudicated",
                    "evidence": [],
                },
            ]
        ),
        encoding="utf-8",
    )
    external_qrels = tmp_path / "pooled.tsv"
    external_text = "q-001\t0\tchunk-a\t2\nq-002\t0\tchunk-b\t2\n"
    external_qrels.write_text(external_text, encoding="utf-8")
    generated_qrels = tmp_path / "must-not-be-written.tsv"

    summary = bm25.run_experiment(
        run_id="bm25_external",
        chunks_path=chunks_path,
        golden_path=golden_path,
        output_root=tmp_path / "outputs",
        qrels_path=generated_qrels,
        qrels_input_path=external_qrels,
        k1=1.5,
        b=0.75,
        top_k=2,
        cutoffs=(1, 2),
    )

    run_rows = [
        json.loads(line)
        for line in (tmp_path / "outputs/runs/bm25_external.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    metric_rows = list(
        csv.DictReader(
            (tmp_path / "outputs/metrics/bm25_external_metrics.csv").open(
                encoding="utf-8", newline=""
            )
        )
    )
    assert not generated_qrels.exists()
    assert external_qrels.read_text(encoding="utf-8") == external_text
    assert next(row for row in run_rows if row["qid"] == "q-002" and row["rank"] == 1)[
        "relevant_grade"
    ] == 2
    assert summary["metric_query_count"] == 1
    assert summary["unanswerable_query_count"] == 1
    assert summary["qrels_source"] == "external_tsv"
    assert summary["qrels_source_path"] == str(external_qrels)
    assert {row["query_scope"] for row in metric_rows} == {
        "answerable_with_grade2_qrels"
    }
    assert b"\r\n" not in (
        tmp_path / "outputs/metrics/bm25_external_metrics.csv"
    ).read_bytes()
