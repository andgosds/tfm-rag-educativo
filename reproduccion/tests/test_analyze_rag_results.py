from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/analyze_rag_results.py"


def load_module():
    spec = importlib.util.spec_from_file_location("analyze_rag_results", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_paired_comparison_counts_wins_ties_losses_and_mean_delta():
    analysis = load_module()
    rows = [
        {"qid": "q1", "retrieval_condition": "rrf", "faithfulness": 0.4},
        {"qid": "q1", "retrieval_condition": "rrf_rerank", "faithfulness": 0.8},
        {"qid": "q2", "retrieval_condition": "rrf", "faithfulness": 1.0},
        {"qid": "q2", "retrieval_condition": "rrf_rerank", "faithfulness": 1.0},
        {"qid": "q3", "retrieval_condition": "rrf", "faithfulness": 0.9},
        {"qid": "q3", "retrieval_condition": "rrf_rerank", "faithfulness": 0.3},
    ]

    result = analysis.paired_comparison(rows, "faithfulness")

    assert result["n"] == 3
    assert result["rerank_wins"] == 1
    assert result["ties"] == 1
    assert result["rrf_wins"] == 1
    assert abs(result["mean_delta_rerank_minus_rrf"] + 0.0666666667) < 1e-9


def test_summarize_by_behavior_keeps_missing_values_out_of_denominator():
    analysis = load_module()
    rows = [
        {
            "retrieval_condition": "rrf",
            "expected_behavior": "answer",
            "factual_correctness": 1.0,
        },
        {
            "retrieval_condition": "rrf",
            "expected_behavior": "answer",
            "factual_correctness": None,
        },
        {
            "retrieval_condition": "rrf",
            "expected_behavior": "abstain",
            "factual_correctness": None,
        },
    ]

    summary = analysis.summarize_by_behavior(rows, ["factual_correctness"])

    assert summary["rrf"]["answer"]["row_count"] == 2
    assert summary["rrf"]["answer"]["factual_correctness_n"] == 1
    assert summary["rrf"]["answer"]["factual_correctness_mean"] == 1.0
    assert summary["rrf"]["abstain"]["factual_correctness_n"] == 0


def test_applicable_content_keeps_unsupported_abstention_and_raw_scores():
    import copy

    analysis = load_module()
    rows = [
        {"qid": "q1", "retrieval_condition": "dense", "expected_behavior": "abstain", "faithfulness": 0.3},
        {"qid": "q2", "retrieval_condition": "dense", "expected_behavior": "answer", "reported_behavior": "abstain", "faithfulness": 0.0, "factual_correctness": 0.0},
        {"qid": "q3", "retrieval_condition": "dense", "expected_behavior": "grounded_correction", "faithfulness": 1.0, "factual_correctness": 1.0},
    ]
    original = copy.deepcopy(rows)
    assert hasattr(analysis, "analyze_applicable_content"), "applicability analysis is missing"
    result = analysis.analyze_applicable_content(rows)
    assert result["row_count"] == 2
    assert result["excluded_expected_abstention_count"] == 1
    assert result["overall"]["dense"]["faithfulness_mean"] == 0.5
    assert rows == original


def test_analyze_reports_every_pairwise_comparison_for_four_conditions():
    analysis = load_module()
    rows = []
    values = {"bm25": 0.4, "dense": 0.5, "rrf": 0.7, "rrf_rerank": 0.8}
    for condition, value in values.items():
        rows.append(
            {
                "qid": "q1",
                "retrieval_condition": condition,
                "expected_behavior": "answer",
                "faithfulness": value,
                "factual_correctness": value,
                "reported_behavior_match": 1.0,
                "citation_validity": 1.0,
                "citation_presence": 1.0,
                "behavior_judge_score": 2.0,
            }
        )

    result = analysis.analyze(rows)

    assert set(result["all_pairwise"]) == {
        "bm25__vs__dense",
        "bm25__vs__rrf",
        "bm25__vs__rrf_rerank",
        "dense__vs__rrf",
        "dense__vs__rrf_rerank",
        "rrf__vs__rrf_rerank",
    }
    comparison = result["all_pairwise"]["bm25__vs__rrf"]["faithfulness"]
    assert comparison["baseline"] == "bm25"
    assert comparison["contender"] == "rrf"
    assert comparison["contender_wins"] == 1
    assert abs(comparison["mean_delta_contender_minus_baseline"] - 0.3) < 1e-12
    assert comparison["per_query"] == [
        {
            "qid": "q1",
            "baseline_condition": "bm25",
            "contender_condition": "rrf",
            "baseline_score": 0.4,
            "contender_score": 0.7,
            "delta_contender_minus_baseline": 0.7 - 0.4,
        }
    ]
