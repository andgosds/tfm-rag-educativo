from __future__ import annotations

import importlib.util
import json
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "consolidate_rag_behavior.py"
SPEC = importlib.util.spec_from_file_location("consolidate_rag_behavior", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

consolidate_behavior = MODULE.consolidate_behavior
generate_consolidated_report = MODULE.generate_consolidated_report


def test_consolidate_behavior_preserves_automatic_and_applies_human_override() -> None:
    full = [
        {"qid": "q1", "retrieval_condition": "rrf", "behavior_judge_score": 1},
        {"qid": "q1", "retrieval_condition": "rrf_rerank", "behavior_judge_score": 2},
        {"qid": "q2", "retrieval_condition": "rrf", "behavior_judge_score": 2},
        {"qid": "q2", "retrieval_condition": "rrf_rerank", "behavior_judge_score": 2},
    ]
    audit = [
        {
            "qid": "q1",
            "retrieval_condition": "rrf",
            "human_adjudication": {"status": "adjudicated", "behavior_score": 2},
        },
        {
            "qid": "q1",
            "retrieval_condition": "rrf_rerank",
            "human_adjudication": {"status": "adjudicated", "behavior_score": 0},
        },
    ]

    result = consolidate_behavior(full, audit, primary_judge="glm53flash_low")

    cases = {(c["retrieval_condition"], c["qid"]): c for c in result["per_case"]}
    assert cases[("rrf", "q1")] == {
        "retrieval_condition": "rrf",
        "qid": "q1",
        "automatic_behavior_score": 1.0,
        "final_behavior_score": 2.0,
        "final_behavior_source": "human_adjudication",
    }
    assert cases[("rrf", "q2")]["final_behavior_source"] == "glm53flash_low"
    assert result["source_counts"] == {"human_adjudication": 2, "glm53flash_low": 2}
    assert result["by_retrieval_condition"]["rrf"]["final_mean"] == 2.0
    assert result["paired"] == {
        "common_qid_count": 2,
        "rerank_wins": 0,
        "ties": 1,
        "rrf_wins": 1,
        "mean_delta_rerank_minus_rrf": -1.0,
    }


def test_generate_consolidated_report_writes_json(tmp_path: Path) -> None:
    full_path = tmp_path / "full.jsonl"
    audit_path = tmp_path / "audit.jsonl"
    output_path = tmp_path / "result.json"
    full_path.write_text(
        json.dumps(
            {"qid": "q1", "retrieval_condition": "rrf", "behavior_judge_score": 1}
        )
        + "\n",
        encoding="utf-8",
    )
    audit_path.write_text(
        json.dumps(
            {
                "qid": "q1",
                "retrieval_condition": "rrf",
                "human_adjudication": {
                    "status": "adjudicated",
                    "behavior_score": 2,
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )

    result = generate_consolidated_report(
        [full_path], audit_path, output_path, primary_judge="glm53flash_low"
    )

    assert result["case_count"] == 1
    assert json.loads(output_path.read_text(encoding="utf-8")) == result


def test_consolidate_behavior_reports_all_pairs_for_four_conditions() -> None:
    full = [
        {"qid": "q1", "retrieval_condition": condition, "behavior_judge_score": score}
        for condition, score in (
            ("bm25", 1),
            ("dense", 2),
            ("rrf", 2),
            ("rrf_rerank", 1),
        )
    ]

    result = consolidate_behavior(full, [], primary_judge="glm53flash_low")

    assert set(result["all_pairwise"]) == {
        "bm25__vs__dense",
        "bm25__vs__rrf",
        "bm25__vs__rrf_rerank",
        "dense__vs__rrf",
        "dense__vs__rrf_rerank",
        "rrf__vs__rrf_rerank",
    }
    assert result["all_pairwise"]["bm25__vs__dense"] == {
        "baseline": "bm25",
        "contender": "dense",
        "common_qid_count": 1,
        "contender_wins": 1,
        "ties": 0,
        "baseline_wins": 0,
        "mean_delta_contender_minus_baseline": 1.0,
    }
