from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/compare_rag_judges.py"


def load_module():
    spec = importlib.util.spec_from_file_location("compare_rag_judges", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_read_many_jsonl_combines_condition_files(tmp_path):
    comparison = load_module()
    rrf = tmp_path / "rrf.jsonl"
    rerank = tmp_path / "rerank.jsonl"
    rrf.write_text(
        '{"qid":"q1","retrieval_condition":"rrf"}\n', encoding="utf-8"
    )
    rerank.write_text(
        '{"qid":"q1","retrieval_condition":"rrf_rerank"}\n', encoding="utf-8"
    )

    rows = comparison.read_many_jsonl([rrf, rerank])

    assert [row["retrieval_condition"] for row in rows] == [
        "rrf",
        "rrf_rerank",
    ]


def test_execution_summary_reports_observed_behavior_tokens_and_latency():
    comparison = load_module()
    rows = [
        {
            "evaluation_latency_ms": 1000.0,
            "behavior_judge_prompt_tokens": 100,
            "behavior_judge_completion_tokens": 20,
            "behavior_judge_attempts": 1,
        },
        {
            "evaluation_latency_ms": 3000.0,
            "behavior_judge_prompt_tokens": 250,
            "behavior_judge_completion_tokens": 50,
            "behavior_judge_attempts": 2,
        },
    ]

    result = comparison.execution_summary(rows)

    assert result == {
        "row_count": 2,
        "evaluation_latency_ms_total": 4000.0,
        "evaluation_latency_ms_mean": 2000.0,
        "behavior_prompt_tokens_observed": 350,
        "behavior_completion_tokens_observed": 70,
        "behavior_total_tokens_observed": 420,
        "behavior_attempts_total": 3,
        "behavior_retried_case_count": 1,
        "ragas_token_usage_available": False,
    }


def test_compare_judges_aligns_cases_and_reports_missing_values():
    comparison = load_module()
    gemma = [
        {
            "qid": "q1",
            "retrieval_condition": "rrf",
            "faithfulness": 0.5,
            "factual_correctness": 0.8,
        },
        {
            "qid": "q2",
            "retrieval_condition": "rrf",
            "faithfulness": None,
            "factual_correctness": 1.0,
        },
    ]
    glm = [
        {
            "qid": "q1",
            "retrieval_condition": "rrf",
            "faithfulness": 1.0,
            "factual_correctness": 0.7,
        },
        {
            "qid": "q2",
            "retrieval_condition": "rrf",
            "faithfulness": 0.75,
            "factual_correctness": 1.0,
        },
    ]

    result = comparison.compare_judges(
        gemma,
        glm,
        baseline_name="gemma3:4b",
        alternative_name="glm-5.3-flash",
    )

    faithfulness = result["metrics"]["faithfulness"]
    assert result["aligned_case_count"] == 2
    assert faithfulness["baseline_n"] == 1
    assert faithfulness["alternative_n"] == 2
    assert faithfulness["common_n"] == 1
    assert faithfulness["alternative_wins"] == 1
    assert faithfulness["ties"] == 0
    assert faithfulness["baseline_wins"] == 0
    assert faithfulness["mean_delta_alternative_minus_baseline"] == 0.5


def test_compare_judges_rejects_mismatched_case_sets():
    comparison = load_module()
    baseline = [{"qid": "q1", "retrieval_condition": "rrf", "faithfulness": 1.0}]
    alternative = [
        {"qid": "q2", "retrieval_condition": "rrf", "faithfulness": 1.0}
    ]

    try:
        comparison.compare_judges(
            baseline,
            alternative,
            baseline_name="gemma3:4b",
            alternative_name="glm-5.3-flash",
        )
    except ValueError as exc:
        assert "case sets differ" in str(exc)
    else:
        raise AssertionError("mismatched judge case sets were accepted")
