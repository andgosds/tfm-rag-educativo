from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_pooled_qrels.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_pooled_qrels", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row) + "\n" for row in rows),
        encoding="utf-8",
    )


def test_build_preserves_originals_and_adds_adjudicated_positive_grades(tmp_path):
    builder = load_module()
    original = tmp_path / "original.tsv"
    original.write_text("q-001\t0\tchunk-a\t2\n", encoding="utf-8")
    golden = tmp_path / "golden.jsonl"
    write_jsonl(
        golden,
        [
            {
                "qid": "q-001",
                "answerability": "answerable",
                "evidence": [
                    {
                        "chunk_id": "chunk-a",
                        "relevance_grade": 2,
                        "is_canonical": True,
                    }
                ],
            },
            {"qid": "q-002", "answerability": "answerable"},
            {"qid": "q-003", "answerability": "unanswerable"},
        ],
    )
    pool = tmp_path / "pool.jsonl"
    write_jsonl(
        pool,
        [
            {
                "pool_id": "p-1",
                "qid": "q-001",
                "chunk_id": "chunk-b",
                "human_grade": 1,
                "human_canonical": False,
                "human_reviewer_id": "andres-delegated-assistant",
                "adjudication_mode": "assistant_on_behalf_of_andres",
            },
            {
                "pool_id": "p-2",
                "qid": "q-002",
                "chunk_id": "chunk-c",
                "human_grade": 0,
                "human_canonical": False,
                "human_reviewer_id": "andres",
            },
            {
                "pool_id": "p-3",
                "qid": "q-003",
                "chunk_id": "chunk-d",
                "human_grade": 2,
                "human_canonical": True,
                "human_reviewer_id": "andres",
                "adjudication_mode": "user_advised_after_assistant_review",
            },
        ],
    )
    output = tmp_path / "pooled.tsv"
    provenance = tmp_path / "provenance.jsonl"
    report = tmp_path / "report.json"

    result = builder.build_pooled_qrels(
        original_qrels_path=original,
        adjudication_path=pool,
        golden_path=golden,
        output_qrels_path=output,
        provenance_path=provenance,
        report_path=report,
    )

    assert output.read_text(encoding="utf-8") == (
        "q-001\t0\tchunk-a\t2\n"
        "q-001\t0\tchunk-b\t1\n"
        "q-003\t0\tchunk-d\t2\n"
    )
    provenance_rows = [
        json.loads(line) for line in provenance.read_text(encoding="utf-8").splitlines()
    ]
    assert provenance_rows[0]["source"] == "original_qrel"
    assert provenance_rows[0]["canonical"] is True
    assert provenance_rows[1]["adjudication_mode"] == "assistant_on_behalf_of_andres"
    assert provenance_rows[2]["canonical"] is True
    assert result["original_qrel_count"] == 1
    assert result["added_qrel_count"] == 2
    assert result["audited_grade_0_count"] == 1
    assert result["final_qrel_count"] == 3
    assert result["answerability_conflicts"] == [
        {"qid": "q-003", "chunk_id": "chunk-d", "grade": 2}
    ]
    assert json.loads(report.read_text(encoding="utf-8"))["output_sha256"]


def test_build_rejects_pending_adjudications(tmp_path):
    builder = load_module()
    original = tmp_path / "original.tsv"
    original.write_text("", encoding="utf-8")
    golden = tmp_path / "golden.jsonl"
    write_jsonl(golden, [{"qid": "q-001", "answerability": "answerable"}])
    pool = tmp_path / "pool.jsonl"
    write_jsonl(
        pool,
        [
            {
                "pool_id": "p-1",
                "qid": "q-001",
                "chunk_id": "chunk-a",
                "human_grade": None,
            }
        ],
    )

    with pytest.raises(ValueError, match="pending adjudication"):
        builder.build_pooled_qrels(
            original_qrels_path=original,
            adjudication_path=pool,
            golden_path=golden,
            output_qrels_path=tmp_path / "pooled.tsv",
            provenance_path=tmp_path / "provenance.jsonl",
            report_path=tmp_path / "report.json",
        )


def test_build_reports_unresolved_original_qrel_answerability_conflict(tmp_path):
    builder = load_module()
    original = tmp_path / "original.tsv"
    original.write_text(
        "q-unanswerable\t0\tchunk-original\t2\n", encoding="utf-8"
    )
    golden = tmp_path / "golden.jsonl"
    write_jsonl(
        golden,
        [{"qid": "q-unanswerable", "answerability": "unanswerable"}],
    )
    pool = tmp_path / "pool.jsonl"
    pool.write_text("", encoding="utf-8")
    report = tmp_path / "report.json"

    result = builder.build_pooled_qrels(
        original_qrels_path=original,
        adjudication_path=pool,
        golden_path=golden,
        output_qrels_path=tmp_path / "pooled.tsv",
        provenance_path=tmp_path / "provenance.jsonl",
        report_path=report,
    )

    expected_conflict = {
        "qid": "q-unanswerable",
        "chunk_id": "chunk-original",
        "grade": 2,
    }
    assert result["answerability_conflicts"] == [expected_conflict]
    assert json.loads(report.read_text(encoding="utf-8"))[
        "answerability_conflicts"
    ] == [expected_conflict]


def test_build_marks_adjudicated_false_premise_evidence_as_contradiction(tmp_path):
    builder = load_module()
    original = tmp_path / "original.tsv"
    original.write_text("", encoding="utf-8")
    golden = tmp_path / "golden.jsonl"
    write_jsonl(
        golden,
        [
            {
                "qid": "q-false-premise",
                "answerability": "unanswerable",
                "unanswerable_category": "false_premise",
            }
        ],
    )
    pool = tmp_path / "pool.jsonl"
    write_jsonl(
        pool,
        [
            {
                "pool_id": "p-contradiction",
                "qid": "q-false-premise",
                "chunk_id": "chunk-refutation",
                "human_grade": 2,
                "human_canonical": True,
                "human_reviewer_id": "andres",
            }
        ],
    )
    resolutions = tmp_path / "answerability.json"
    resolutions.write_text(
        json.dumps(
            {
                "resolutions": [
                    {
                        "resolution_id": "answerability-q-false-premise-v1",
                        "qid": "q-false-premise",
                        "decision": "keep_unanswerable_with_contradiction_evidence",
                        "expected_response_behavior": "grounded_correction",
                        "evidence_role": "contradiction",
                        "evidence_chunk_ids": ["chunk-refutation"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    provenance = tmp_path / "provenance.jsonl"

    result = builder.build_pooled_qrels(
        original_qrels_path=original,
        adjudication_path=pool,
        golden_path=golden,
        answerability_resolution_path=resolutions,
        output_qrels_path=tmp_path / "pooled.tsv",
        provenance_path=provenance,
        report_path=tmp_path / "report.json",
    )

    provenance_row = json.loads(provenance.read_text(encoding="utf-8"))
    assert provenance_row["evidence_role"] == "contradiction"
    assert provenance_row["answerability_resolution_id"] == (
        "answerability-q-false-premise-v1"
    )
    assert result["answerability_conflicts"] == []
    assert result["resolved_answerability_conflicts"] == [
        {
            "qid": "q-false-premise",
            "chunk_id": "chunk-refutation",
            "grade": 2,
            "evidence_role": "contradiction",
            "resolution_id": "answerability-q-false-premise-v1",
        }
    ]
