from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build_rag_judge_risk_queue.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_rag_judge_risk_queue", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def case(condition: str, qid: str, *, expected: str = "answer", behavior: int = 2) -> dict:
    return {
        "retrieval_condition": condition,
        "qid": qid,
        "question": "Question?",
        "answerability": "answerable" if expected == "answer" else "unanswerable",
        "expected_behavior": expected,
        "reference": "Reference" if expected != "abstain" else None,
        "response": "Response",
        "reported_behavior": expected,
        "reported_behavior_match": 1.0,
        "citations": ["c1"] if expected != "abstain" else [],
        "retrieved_chunk_ids": ["c1"],
        "retrieved_contexts": ["Context"],
        "faithfulness": 1.0,
        "factual_correctness": 1.0 if expected != "abstain" else None,
        "behavior_judge_score": behavior,
        "behavior_judge_rationale": "Rationale",
        "evaluation_errors": [],
        "evaluation_prompt_version": "v2",
    }


def test_build_queue_supports_four_conditions_and_preserves_previous_adjudication():
    builder = load_module()
    gemma = [
        case("bm25", "q1", behavior=1),
        case("dense", "q1"),
        case("rrf", "q2", expected="abstain"),
        case("rrf_rerank", "q2", expected="abstain"),
    ]
    glm = [
        case("bm25", "q1", behavior=2),
        case("dense", "q1"),
        case("rrf", "q2", expected="abstain"),
        case("rrf_rerank", "q2", expected="abstain"),
    ]
    previous = [
        {
            **case("rrf", "q2", expected="abstain"),
            "human_adjudication": {
                "status": "adjudicated",
                "faithfulness_assessment": "not_applicable",
                "factual_correctness_assessment": "not_applicable",
                "behavior_score": 2,
                "notes": "Reviewed",
                "reviewer_id": "andres",
                "reviewed_at": "2026-09-03T12:00:00+02:00",
            },
        }
    ]

    queue, summary = builder.build_queue(gemma, glm, previous_rows=previous)

    assert {(row["retrieval_condition"], row["qid"]) for row in queue} == {
        ("bm25", "q1"),
        ("rrf", "q2"),
        ("rrf_rerank", "q2"),
    }
    preserved = next(row for row in queue if row["retrieval_condition"] == "rrf")
    assert preserved["human_adjudication"]["status"] == "adjudicated"
    assert summary["source_case_count"] == 4
    assert summary["queued_case_count"] == 3
    assert summary["preserved_adjudication_count"] == 1
    assert summary["by_condition"] == {"bm25": 1, "rrf": 1, "rrf_rerank": 1}


def test_build_queue_does_not_preserve_adjudication_for_changed_response():
    builder = load_module()
    gemma = [case("rrf", "q1", behavior=1)]
    glm = [case("rrf", "q1", behavior=2)]
    previous = [
        {
            **case("rrf", "q1", behavior=1),
            "response": "A different historical response",
            "human_adjudication": {
                "status": "adjudicated",
                "faithfulness_assessment": "supported",
                "factual_correctness_assessment": "correct",
                "behavior_score": 2,
                "notes": "Historical unit",
            },
        }
    ]

    queue, summary = builder.build_queue(gemma, glm, previous_rows=previous)

    assert queue[0]["human_adjudication"]["status"] == "pending"
    assert summary["preserved_adjudication_count"] == 0


def test_build_queue_rejects_different_judge_case_sets():
    builder = load_module()

    try:
        builder.build_queue([case("bm25", "q1")], [case("dense", "q1")])
    except ValueError as exc:
        assert "case sets differ" in str(exc)
    else:
        raise AssertionError("different judge case sets were accepted")