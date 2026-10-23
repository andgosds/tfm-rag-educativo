from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_three_judge_priority.py"
SPEC = importlib.util.spec_from_file_location("build_three_judge_priority", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
select_priority_candidates = MODULE.select_priority_candidates


def review(pool_id: str, grade: int, conflict: bool = False) -> dict:
    return {
        "pool_id": pool_id,
        "qid": "q1",
        "chunk_id": f"chunk-{pool_id}",
        "relevance_grade": grade,
        "canonical_candidate": "yes" if grade == 2 else "no",
        "answerability_conflict": conflict,
    }


def test_select_priority_candidates_applies_risk_rules_and_preserves_human_work() -> None:
    ids = ["any2", "all-different", "conflict", "consensus0-a", "consensus0-b", "consensus1-a", "consensus1-b", "reviewed", "exclude"]
    pool = [
        {
            "pool_id": pool_id,
            "qid": "q1",
            "chunk_id": f"chunk-{pool_id}",
            "question": "Question?",
            "retrieval_text": "Evidence",
            "human_grade": None,
            "human_canonical": None,
            "human_note": "",
        }
        for pool_id in ids
    ]
    grades = {
        "any2": (2, 1, 1),
        "all-different": (0, 1, 2),
        "conflict": (0, 0, 0),
        "consensus0-a": (0, 0, 0),
        "consensus0-b": (0, 0, 0),
        "consensus1-a": (1, 1, 1),
        "consensus1-b": (1, 1, 1),
        "reviewed": (0, 0, 0),
        "exclude": (0, 1, 1),
    }
    judges = []
    for judge_index in range(3):
        judges.append(
            [
                review(
                    pool_id,
                    grades[pool_id][judge_index],
                    conflict=pool_id == "conflict" and judge_index == 0,
                )
                for pool_id in ids
            ]
        )
    existing_human = {
        "reviewed": {
            **next(row for row in pool if row["pool_id"] == "reviewed"),
            "human_grade": 1,
            "human_canonical": False,
            "human_note": "Preserved",
            "human_reviewer_id": "andres",
            "human_status": "adjudicated",
            "human_reviewed_at": "2026-08-24T12:00:00+02:00",
        }
    }

    selected = select_priority_candidates(
        pool,
        judges,
        existing_human,
        audit_per_stratum=1,
        seed="test-seed",
    )

    by_id = {row["pool_id"]: row for row in selected}
    assert {"any2", "all-different", "conflict", "reviewed"} <= set(by_id)
    assert sum("audit_unanimous_grade_0" in row["selection_reasons"] for row in selected) == 1
    assert sum("audit_unanimous_grade_1" in row["selection_reasons"] for row in selected) == 1
    assert by_id["reviewed"]["human_grade"] == 1
    assert by_id["reviewed"]["human_note"] == "Preserved"
    assert "existing_human_decision" in by_id["reviewed"]["selection_reasons"]
    assert by_id["any2"]["judge3_grade"] == 1
    assert by_id["all-different"]["selection_reasons"] == [
        "any_judge_grade_2",
        "all_judges_disagree",
    ]
    assert len({row["pool_id"] for row in selected}) == len(selected)
    assert all("source_system" not in row for row in selected)
    assert "exclude" not in by_id
