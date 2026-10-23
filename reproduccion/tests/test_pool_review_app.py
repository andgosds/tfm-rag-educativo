from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "pool_review_app.py"
SPEC = importlib.util.spec_from_file_location("pool_review_app", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
build_review_state = MODULE.build_review_state
load_jsonl = MODULE.load_jsonl
render_app_html = MODULE.render_app_html
save_human_decision = MODULE.save_human_decision


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def test_build_review_state_adds_gold_context_and_auxiliary_rationales(tmp_path: Path) -> None:
    priority_path = tmp_path / "priority.jsonl"
    golden_path = tmp_path / "golden.jsonl"
    judge1_path = tmp_path / "judge1.json"
    judge2_path = tmp_path / "judge2.json"
    judge3_path = tmp_path / "judge3.json"
    chunks_path = tmp_path / "chunks.jsonl"
    write_jsonl(
        priority_path,
        [
            {
                "pool_id": "q1-pool-001",
                "qid": "q1",
                "question": "Question?",
                "chunk_id": "chunk-1",
                "retrieval_text": "Source: Book\nChapter 1\nSection 1.1\n\nEvidence",
                "judge1_grade": 2,
                "judge2_grade": 1,
                "human_grade": None,
                "human_canonical": None,
                "human_note": "",
            }
        ],
    )
    write_jsonl(
        golden_path,
        [
            {
                "qid": "q1",
                "question_type": "explanatory",
                "answerability": "answerable",
                "gold_answer": "Reference answer",
            }
        ],
    )
    judge1_path.write_text(
        json.dumps(
            [
                {
                    "pool_id": "q1-pool-001",
                    "relevance_grade": 2,
                    "canonical_candidate": "yes",
                    "confidence": 0.9,
                    "rationale": "Direct evidence.",
                }
            ]
        ),
        encoding="utf-8",
    )
    judge2_path.write_text(
        json.dumps(
            [
                {
                    "pool_id": "q1-pool-001",
                    "relevance_grade": 1,
                    "canonical_candidate": "no",
                    "confidence": 0.7,
                    "rationale": "Incomplete evidence.",
                }
            ]
        ),
        encoding="utf-8",
    )

    judge3_path.write_text(
        json.dumps(
            [
                {
                    "pool_id": "q1-pool-001",
                    "reviewer_id": "pool-judge-3-kimi-k3-max",
                    "relevance_grade": 0,
                    "canonical_candidate": "no",
                    "confidence": 0.8,
                    "rationale": "No direct evidence.",
                }
            ]
        ),
        encoding="utf-8",
    )
    write_jsonl(chunks_path, [{"chunk_id": "chunk-1", "formula_risk": True}])
    state = build_review_state(
        priority_path,
        golden_path,
        judge1_path,
        judge2_path,
        chunks_path,
        judge3_path,
    )

    candidate = state["candidates"][0]
    assert candidate["gold_answer"] == "Reference answer"
    assert candidate["question_type"] == "explanatory"
    assert candidate["answerability"] == "answerable"
    assert candidate["formula_risk"] is True
    assert candidate["auxiliary_reviews"][0]["rationale"] == "Direct evidence."
    assert candidate["auxiliary_reviews"][1]["rationale"] == "Incomplete evidence."
    assert candidate["auxiliary_reviews"][2]["rationale"] == "No direct evidence."
    assert len(candidate["auxiliary_reviews"]) == 3
    assert "source_system" not in candidate
    assert "bm25_rank" not in candidate
    assert state["summary"] == {"total": 1, "reviewed": 0, "pending": 1}


def test_save_human_decision_updates_only_target_and_records_traceability(tmp_path: Path) -> None:
    path = tmp_path / "priority.jsonl"
    write_jsonl(
        path,
        [
            {"pool_id": "p1", "human_grade": None, "human_canonical": None, "human_note": ""},
            {"pool_id": "p2", "human_grade": None, "human_canonical": None, "human_note": ""},
        ],
    )

    save_human_decision(
        path,
        pool_id="p2",
        grade=2,
        canonical=True,
        note="Direct and sufficient.",
        reviewer_id="andres",
        reviewed_at="2026-08-24T12:00:00+02:00",
    )

    rows = load_jsonl(path)
    assert rows[0]["human_grade"] is None
    assert rows[1]["human_grade"] == 2
    assert rows[1]["human_canonical"] is True
    assert rows[1]["human_note"] == "Direct and sufficient."
    assert rows[1]["human_reviewer_id"] == "andres"
    assert rows[1]["human_reviewed_at"] == "2026-08-24T12:00:00+02:00"
    assert rows[1]["human_status"] == "adjudicated"
    assert not list(tmp_path.glob("*.tmp"))


def test_save_human_decision_rejects_invalid_grade_and_invalid_canonical_pair(tmp_path: Path) -> None:
    path = tmp_path / "priority.jsonl"
    write_jsonl(
        path,
        [{"pool_id": "p1", "human_grade": None, "human_canonical": None, "human_note": ""}],
    )

    with pytest.raises(ValueError, match="grade"):
        save_human_decision(path, "p1", 3, False, "", "andres")
    with pytest.raises(ValueError, match="canonical"):
        save_human_decision(path, "p1", 1, True, "", "andres")


def test_save_human_decision_can_clear_a_previous_decision(tmp_path: Path) -> None:
    path = tmp_path / "priority.jsonl"
    write_jsonl(
        path,
        [
            {
                "pool_id": "p1",
                "human_grade": 2,
                "human_canonical": True,
                "human_note": "old",
                "human_reviewer_id": "andres",
                "human_reviewed_at": "old-date",
                "human_status": "adjudicated",
            }
        ],
    )

    save_human_decision(path, "p1", None, None, "", "andres")

    row = load_jsonl(path)[0]
    assert row["human_grade"] is None
    assert row["human_canonical"] is None
    assert row["human_status"] == "pending"
    assert "human_reviewed_at" not in row


def test_render_app_html_contains_fast_blind_review_controls() -> None:
    html = render_app_html()

    assert "Revisión ciega del pool" in html
    assert 'id="grade-0"' in html
    assert 'id="grade-1"' in html
    assert 'id="grade-2"' in html
    assert 'id="canonical"' in html
    assert 'id="note"' in html
    assert 'id="save-next"' in html
    assert 'id="auxiliary-reviews"' in html
    assert 'id="empty-state"' in html
    assert 'id="formula-risk"' in html
    assert 'id="decision-guide"' in html
    assert 'id="shortcut-guide"' in html
    assert "No aporta evidencia útil" in html
    assert "Relacionado, pero insuficiente" in html
    assert "Evidencia directa y suficiente" in html
    assert "Pregunta multichunk" in html
    assert "pregunta marcada como no respondible" in html
    assert "Canónica" in html
    assert "innerHTML = '<div" not in html
    assert "<details" in html
    assert "event.key === '0'" in html
    assert "event.key === '1'" in html
    assert "event.key === '2'" in html
    assert "ArrowLeft" in html
    assert "ArrowRight" in html
    assert "source_system" not in html
    assert "bm25_rank" not in html
    assert "dense_rank" not in html
