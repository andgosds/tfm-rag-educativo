from __future__ import annotations

import importlib.util
import json
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "rag_review_app.py"
SPEC = importlib.util.spec_from_file_location("rag_review_app", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

build_review_state = MODULE.build_review_state
load_jsonl = MODULE.load_jsonl
save_human_adjudications = MODULE.save_human_adjudications
render_app_html = MODULE.render_app_html
restore_human_adjudications = MODULE.restore_human_adjudications
make_handler = MODULE.make_handler


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def test_build_review_state_groups_conditions_by_qid_and_counts_progress(tmp_path: Path) -> None:
    path = tmp_path / "risk.jsonl"
    base = {
        "question": "Question?",
        "expected_behavior": "answer",
        "reference": "Reference",
        "human_adjudication": {
            "status": "pending",
            "faithfulness_assessment": None,
            "factual_correctness_assessment": None,
            "behavior_score": None,
            "notes": None,
        },
    }
    reviewed = {
        **base,
        "human_adjudication": {
            "status": "adjudicated",
            "faithfulness_assessment": "supported",
            "factual_correctness_assessment": "correct",
            "behavior_score": 2,
            "notes": "",
        },
    }
    write_jsonl(
        path,
        [
            {**base, "qid": "q2", "retrieval_condition": "rrf", "response": "B"},
            {**reviewed, "qid": "q1", "retrieval_condition": "rrf_rerank", "response": "A2"},
            {**reviewed, "qid": "q1", "retrieval_condition": "rrf", "response": "A1"},
        ],
    )

    state = build_review_state(path)

    assert [item["qid"] for item in state["questions"]] == ["q1", "q2"]
    assert [row["retrieval_condition"] for row in state["questions"][0]["conditions"]] == [
        "rrf",
        "rrf_rerank",
    ]
    assert state["summary"] == {
        "total_pairs": 3,
        "reviewed_pairs": 2,
        "pending_pairs": 1,
        "total_questions": 2,
        "reviewed_questions": 1,
        "pending_questions": 1,
    }


def test_build_review_state_orders_all_four_retrieval_conditions(tmp_path: Path) -> None:
    path = tmp_path / "risk.jsonl"
    rows = [
        {
            "qid": "q1",
            "question": "Question?",
            "retrieval_condition": condition,
            "expected_behavior": "answer",
            "reference": "Reference",
            "response": condition,
            "human_adjudication": {"status": "pending"},
        }
        for condition in ["rrf_rerank", "rrf", "dense", "bm25"]
    ]
    write_jsonl(path, rows)

    state = build_review_state(path)

    assert [
        row["retrieval_condition"]
        for row in state["questions"][0]["conditions"]
    ] == ["bm25", "dense", "rrf", "rrf_rerank"]


def test_build_review_state_normalizes_real_judge_fields(tmp_path: Path) -> None:
    path = tmp_path / "risk.jsonl"
    write_jsonl(
        path,
        [
            {
                "qid": "q1",
                "question": "Question?",
                "retrieval_condition": "rrf",
                "gemma3_4b": {
                    "faithfulness": 1.0,
                    "factual_correctness": 1.0,
                    "behavior_judge_score": 2,
                    "behavior_judge_rationale": "Gemma rationale",
                    "evaluation_errors": [],
                },
                "glm53flash_low": {
                    "faithfulness": 0.5,
                    "factual_correctness": 0.0,
                    "behavior_judge_score": 1,
                    "behavior_judge_rationale": "GLM rationale",
                    "evaluation_errors": ["metric warning"],
                },
                "human_adjudication": {"status": "pending"},
            }
        ],
    )

    condition = build_review_state(path)["questions"][0]["conditions"][0]

    assert condition["judges"] == {
        "Gemma 3 4B": {
            "faithfulness": 1.0,
            "factual_correctness": 1.0,
            "behavior_score": 2,
            "behavior_rationale": "Gemma rationale",
            "evaluation_errors": [],
        },
        "GLM 5.3 Flash (low)": {
            "faithfulness": 0.5,
            "factual_correctness": 0.0,
            "behavior_score": 1,
            "behavior_rationale": "GLM rationale",
            "evaluation_errors": ["metric warning"],
        },
    }


def test_save_human_adjudications_updates_qid_atomically_and_preserves_scores(tmp_path: Path) -> None:
    path = tmp_path / "risk.jsonl"
    pending = {
        "status": "pending",
        "faithfulness_assessment": None,
        "factual_correctness_assessment": None,
        "behavior_score": None,
        "notes": None,
    }
    write_jsonl(
        path,
        [
            {"qid": "q1", "retrieval_condition": "rrf", "faithfulness": 0.2, "response": "A", "human_adjudication": pending},
            {"qid": "q1", "retrieval_condition": "rrf_rerank", "faithfulness": 0.8, "response": "B", "human_adjudication": pending},
            {"qid": "q2", "retrieval_condition": "rrf", "faithfulness": 1.0, "response": "C", "human_adjudication": pending},
        ],
    )
    decisions = {
        "rrf": {
            "faithfulness_assessment": "partially_supported",
            "factual_correctness_assessment": "correct",
            "behavior_score": 1,
            "notes": "Minor unsupported claim.",
        },
        "rrf_rerank": {
            "faithfulness_assessment": "supported",
            "factual_correctness_assessment": "correct",
            "behavior_score": 2,
            "notes": "",
        },
    }

    saved = save_human_adjudications(
        path,
        qid="q1",
        decisions=decisions,
        reviewer_id="andres",
        reviewed_at="2026-09-03T12:00:00+02:00",
    )

    rows = load_jsonl(path)
    assert len(saved) == 2
    assert rows[0]["faithfulness"] == 0.2
    assert rows[0]["response"] == "A"
    assert rows[0]["human_adjudication"] == {
        "status": "adjudicated",
        "faithfulness_assessment": "partially_supported",
        "factual_correctness_assessment": "correct",
        "behavior_score": 1,
        "notes": "Minor unsupported claim.",
        "reviewer_id": "andres",
        "reviewed_at": "2026-09-03T12:00:00+02:00",
    }
    assert rows[1]["human_adjudication"]["behavior_score"] == 2
    assert rows[2]["human_adjudication"]["status"] == "pending"
    assert not list(tmp_path.glob("*.tmp"))


def test_save_human_adjudications_preserves_metadata_for_unchanged_decision(tmp_path: Path) -> None:
    path = tmp_path / "risk.jsonl"
    previous = {
        "status": "adjudicated",
        "faithfulness_assessment": "supported",
        "factual_correctness_assessment": "correct",
        "behavior_score": 2,
        "notes": "",
        "reviewer_id": "andres",
        "reviewed_at": "2026-09-04T12:00:00+02:00",
    }
    write_jsonl(
        path,
        [
            {"qid": "q1", "retrieval_condition": "bm25", "human_adjudication": {"status": "pending"}},
            {"qid": "q1", "retrieval_condition": "rrf", "human_adjudication": previous},
        ],
    )

    save_human_adjudications(
        path,
        qid="q1",
        decisions={
            "bm25": {
                "faithfulness_assessment": "supported",
                "factual_correctness_assessment": "correct",
                "behavior_score": 2,
                "notes": "new",
            },
            "rrf": {
                "faithfulness_assessment": "supported",
                "factual_correctness_assessment": "correct",
                "behavior_score": 2,
                "notes": "",
            },
        },
        reviewer_id="human_primary",
        reviewed_at="2026-09-07T12:00:00+02:00",
    )

    rows = load_jsonl(path)
    assert rows[0]["human_adjudication"]["reviewer_id"] == "human_primary"
    assert rows[1]["human_adjudication"] == previous


def test_save_human_adjudications_rejects_invalid_or_incomplete_batch_without_writing(tmp_path: Path) -> None:
    path = tmp_path / "risk.jsonl"
    write_jsonl(
        path,
        [
            {"qid": "q1", "retrieval_condition": "rrf", "human_adjudication": {"status": "pending"}},
            {"qid": "q1", "retrieval_condition": "rrf_rerank", "human_adjudication": {"status": "pending"}},
        ],
    )
    original = path.read_bytes()

    import pytest

    with pytest.raises(ValueError, match="exactly match"):
        save_human_adjudications(
            path,
            qid="q1",
            decisions={
                "rrf": {
                    "faithfulness_assessment": "supported",
                    "factual_correctness_assessment": "correct",
                    "behavior_score": 2,
                    "notes": "",
                }
            },
            reviewer_id="andres",
        )
    assert path.read_bytes() == original

    with pytest.raises(ValueError, match="faithfulness"):
        save_human_adjudications(
            path,
            qid="q1",
            decisions={
                condition: {
                    "faithfulness_assessment": "maybe",
                    "factual_correctness_assessment": "correct",
                    "behavior_score": 2,
                    "notes": "",
                }
                for condition in ("rrf", "rrf_rerank")
            },
            reviewer_id="andres",
        )
    assert path.read_bytes() == original


def test_render_app_html_contains_grouped_adjudication_controls_and_shortcuts() -> None:
    html = render_app_html()

    assert "Auditoría humana de respuestas RAG" in html
    assert 'id="qid-filter"' in html
    assert 'id="status-filter"' in html
    assert 'id="condition-grid"' in html
    assert 'data-field="faithfulness_assessment"' in html
    assert 'data-field="factual_correctness_assessment"' in html
    assert 'data-behavior="0"' in html
    assert 'data-behavior="1"' in html
    assert 'data-behavior="2"' in html
    assert 'id="save-next"' in html
    assert 'id="undo"' in html
    assert 'id="export"' in html
    assert "Gemma 3 4B" in html
    assert "GLM 5.3 Flash" in html
    assert "not_applicable" in html
    assert "ArrowLeft" in html
    assert "ArrowRight" in html
    compact = html.replace(" ", "")
    assert "event.key==='0'" in compact
    assert "event.key==='1'" in compact
    assert "event.key==='2'" in compact
    assert "innerHTML" not in html


def test_render_app_html_labels_all_four_retrieval_conditions() -> None:
    html = render_app_html()

    for label in ("BM25", "Dense", "RRF", "RRF + reranking"):
        assert f"'{label}'" in html
    assert "condition.retrieval_condition==='rrf'?'RRF':'RRF + reranking'" not in html


def test_render_app_html_autosaves_complete_decisions_without_advancing() -> None:
    html = render_app_html()

    assert "function scheduleAutosave" in html
    assert "saveCurrent(false)" in html
    assert "Autosave" in html


def test_restore_human_adjudications_restores_pending_batch_atomically(tmp_path: Path) -> None:
    path = tmp_path / "risk.jsonl"
    adjudicated = {
        "status": "adjudicated",
        "faithfulness_assessment": "supported",
        "factual_correctness_assessment": "correct",
        "behavior_score": 2,
        "notes": "done",
        "reviewer_id": "andres",
        "reviewed_at": "2026-09-03T12:00:00+02:00",
    }
    write_jsonl(
        path,
        [
            {"qid": "q1", "retrieval_condition": "rrf", "human_adjudication": adjudicated},
            {"qid": "q1", "retrieval_condition": "rrf_rerank", "human_adjudication": adjudicated},
        ],
    )
    pending = {
        condition: {
            "status": "pending",
            "faithfulness_assessment": None,
            "factual_correctness_assessment": None,
            "behavior_score": None,
            "notes": None,
        }
        for condition in ("rrf", "rrf_rerank")
    }

    restore_human_adjudications(path, qid="q1", decisions=pending)

    rows = load_jsonl(path)
    assert all(row["human_adjudication"] == pending[row["retrieval_condition"]] for row in rows)
    assert not list(tmp_path.glob("*.tmp"))


def test_http_handler_serves_state_saves_batch_and_exports_jsonl(tmp_path: Path) -> None:
    import threading
    import urllib.request
    from http.server import ThreadingHTTPServer

    path = tmp_path / "risk.jsonl"
    pending = {
        "status": "pending",
        "faithfulness_assessment": None,
        "factual_correctness_assessment": None,
        "behavior_score": None,
        "notes": None,
    }
    write_jsonl(
        path,
        [
            {
                "qid": "q1",
                "retrieval_condition": "rrf",
                "question": "Question?",
                "answerability": "answerable",
                "expected_behavior": "answer",
                "reference": "Reference",
                "response": "Response",
                "human_adjudication": pending,
            }
        ],
    )
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(path, "andres"))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        with urllib.request.urlopen(f"{base}/api/state") as response:
            state = json.loads(response.read())
        assert state["summary"]["pending_pairs"] == 1

        payload = json.dumps(
            {
                "qid": "q1",
                "decisions": {
                    "rrf": {
                        "faithfulness_assessment": "supported",
                        "factual_correctness_assessment": "correct",
                        "behavior_score": 2,
                        "notes": "Reviewed.",
                    }
                },
            }
        ).encode()
        request = urllib.request.Request(
            f"{base}/api/adjudications",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request) as response:
            saved = json.loads(response.read())
        assert saved["saved_count"] == 1
        assert load_jsonl(path)[0]["human_adjudication"]["status"] == "adjudicated"

        with urllib.request.urlopen(f"{base}/api/export") as response:
            assert response.read() == path.read_bytes()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
