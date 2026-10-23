from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "analyze_rag_human_adjudication.py"
SPEC = importlib.util.spec_from_file_location("analyze_rag_human_adjudication", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

analyze_human_alignment = MODULE.analyze_human_alignment
analyze_judges = MODULE.analyze_judges
generate_report = MODULE.generate_report


def row(qid: str, expected: str, human: int, automatic: int) -> dict:
    return {
        "qid": qid,
        "retrieval_condition": "rrf",
        "expected_behavior": expected,
        "gemma3_4b": {
            "faithfulness": 1.0,
            "factual_correctness": 1.0,
            "behavior_judge_score": automatic,
            "evaluation_errors": [],
        },
        "human_adjudication": {
            "status": "adjudicated",
            "faithfulness_assessment": "supported",
            "factual_correctness_assessment": "correct",
            "behavior_score": human,
        },
    }


def test_behavior_alignment_reports_exact_agreement_and_strata() -> None:
    rows = [
        row("q1", "answer", 2, 2),
        row("q2", "abstain", 2, 0),
        row("q3", "grounded_correction", 1, 2),
    ]

    result = analyze_human_alignment(rows, "gemma3_4b", "Gemma 3 4B")

    behavior = result["behavior"]
    assert behavior["human_applicable_n"] == 3
    assert behavior["judge_available_on_applicable_n"] == 3
    assert behavior["exact_agreement_n"] == 1
    assert behavior["exact_agreement_rate"] == 1 / 3
    assert behavior["mae_on_applicable"] == 1.0
    assert behavior["by_expected_behavior"]["answer"]["exact_agreement_rate"] == 1.0
    assert behavior["by_expected_behavior"]["abstain"]["exact_agreement_rate"] == 0.0
    assert [(case["qid"], case["human"], case["judge"]) for case in behavior["disagreements"]] == [
        ("q2", 2.0, 0.0),
        ("q3", 1.0, 2.0),
    ]


@pytest.mark.parametrize(
    ("metric", "human_field", "positive", "negative"),
    [
        ("faithfulness", "faithfulness_assessment", "supported", "unsupported"),
        (
            "factual_correctness",
            "factual_correctness_assessment",
            "correct",
            "incorrect",
        ),
    ],
)
def test_metric_alignment_separates_applicability_and_numeric_error(
    metric: str, human_field: str, positive: str, negative: str
) -> None:
    rows = [row("q1", "answer", 2, 2) for _ in range(4)]
    for index, item in enumerate(rows, 1):
        item["qid"] = f"q{index}"
    rows[0]["human_adjudication"][human_field] = positive
    rows[0]["gemma3_4b"][metric] = 1.0
    rows[1]["human_adjudication"][human_field] = "not_applicable"
    rows[1]["gemma3_4b"][metric] = 0.0
    rows[2]["human_adjudication"][human_field] = negative
    rows[2]["gemma3_4b"][metric] = 0.25
    rows[3]["human_adjudication"][human_field] = positive
    rows[3]["gemma3_4b"][metric] = None

    result = analyze_human_alignment(rows, "gemma3_4b", "Gemma 3 4B")[metric]

    assert result["human_applicable_n"] == 3
    assert result["judge_available_on_applicable_n"] == 2
    assert result["missing_on_applicable_n"] == 1
    assert result["human_not_applicable_n"] == 1
    assert result["judge_scored_not_applicable_n"] == 1
    assert result["mae_on_applicable"] == 0.125


def test_analyze_judges_reports_audit_scope_and_judge_errors() -> None:
    rows = [row("q1", "answer", 2, 2), row("q2", "abstain", 2, 0)]
    for item in rows:
        item["glm53flash_low"] = {
            "faithfulness": 1.0,
            "factual_correctness": 1.0,
            "behavior_judge_score": 2,
            "evaluation_errors": [],
        }
    rows[1]["gemma3_4b"]["evaluation_errors"] = ["failed faithfulness"]

    result = analyze_judges(
        rows,
        {"gemma3_4b": "Gemma 3 4B", "glm53flash_low": "GLM 5.3 Flash (low)"},
    )

    assert result["audit_scope"] == {
        "risk_queue_case_count": 2,
        "unique_qid_count": 2,
        "all_cases_adjudicated": True,
        "selection": "risk_directed_nonrandom_subset",
    }
    assert result["judges"]["gemma3_4b"]["evaluation_error_case_count"] == 1
    assert result["judges"]["glm53flash_low"]["evaluation_error_case_count"] == 0


def test_generate_report_writes_reproducible_json(tmp_path: Path) -> None:
    item = row("q1", "answer", 2, 2)
    item["glm53flash_low"] = dict(item["gemma3_4b"])
    input_path = tmp_path / "queue.jsonl"
    output_path = tmp_path / "report.json"
    input_path.write_text(json.dumps(item) + "\n", encoding="utf-8")

    result = generate_report(input_path, output_path)

    assert result["audit_scope"]["risk_queue_case_count"] == 1
    assert json.loads(output_path.read_text(encoding="utf-8")) == result
    assert output_path.read_bytes().endswith(b"\n")
