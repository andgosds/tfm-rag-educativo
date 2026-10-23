from __future__ import annotations

import asyncio
import importlib.util
import math
import sys
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/evaluate_rag.py"


def load_module():
    spec = importlib.util.spec_from_file_location("evaluate_rag", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_resolve_external_judge_connection_requires_named_environment_key(monkeypatch):
    evaluator = load_module()
    monkeypatch.setenv("TEST_OPENCODE_GO_KEY", "synthetic-secret")

    connection = evaluator.resolve_judge_connection(
        provider="opencode-go",
        base_url="https://opencode.ai/zen/go/v1",
        api_key_env="TEST_OPENCODE_GO_KEY",
    )

    assert connection == {
        "provider": "opencode-go",
        "base_url": "https://opencode.ai/zen/go/v1",
        "api_key": "synthetic-secret",
        "external": True,
    }


def test_resolve_external_judge_connection_rejects_missing_key(monkeypatch):
    evaluator = load_module()
    monkeypatch.delenv("MISSING_JUDGE_KEY", raising=False)

    try:
        evaluator.resolve_judge_connection(
            provider="opencode-go",
            base_url="https://opencode.ai/zen/go/v1",
            api_key_env="MISSING_JUDGE_KEY",
        )
    except ValueError as exc:
        assert "MISSING_JUDGE_KEY" in str(exc)
    else:
        raise AssertionError("missing external judge key was accepted")


def test_openai_behavior_judge_scores_expected_abstention_without_penalizing_non_answer():
    evaluator = load_module()
    captured = {}

    class FakeCompletions:
        async def create(self, **kwargs):
            captured.update(kwargs)
            message = SimpleNamespace(
                content='{"score": 2, "rationale": "Correct abstention because evidence is insufficient."}'
            )
            usage = SimpleNamespace(prompt_tokens=100, completion_tokens=20)
            return SimpleNamespace(
                choices=[SimpleNamespace(message=message)], usage=usage
            )

    client = SimpleNamespace(
        chat=SimpleNamespace(completions=FakeCompletions())
    )
    record = {
        "question": "What value was observed?",
        "expected_behavior": "abstain",
        "reference": None,
        "retrieved_contexts": ["The requested value is not reported."],
        "response": "I cannot answer from the supplied contexts.",
    }

    score, rationale, usage = asyncio.run(
        evaluator.judge_behavior_openai(
            record,
            client=client,
            model="glm-5.3-flash",
            seed=20260902,
            max_tokens=4096,
            reasoning_effort="low",
        )
    )

    assert score == 2
    assert "Correct abstention" in rationale
    assert usage == {
        "behavior_judge_prompt_tokens": 100,
        "behavior_judge_completion_tokens": 20,
        "behavior_judge_attempts": 1,
        "behavior_judge_attempt_errors": [],
    }
    assert captured["model"] == "glm-5.3-flash"
    assert captured["temperature"] == 0
    assert captured["seed"] == 20260902
    assert captured["max_tokens"] == 4096
    assert captured["reasoning_effort"] == "low"
    user_prompt = captured["messages"][1]["content"]
    assert "For 'abstain'" in user_prompt
    assert "Expected behavior: abstain" in user_prompt
    assert 'Use exactly the keys "score" and "rationale"' in user_prompt
    assert 'do not use "answer" or "scores"' in user_prompt


def test_openai_behavior_judge_retries_invalid_structured_output():
    evaluator = load_module()
    responses = iter(
        [
            SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content='{"score": 2}'))],
                usage=SimpleNamespace(prompt_tokens=100, completion_tokens=10),
            ),
            SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(
                            content='{"score": 2, "rationale": "Correct answer."}'
                        )
                    )
                ],
                usage=SimpleNamespace(prompt_tokens=100, completion_tokens=20),
            ),
        ]
    )

    class FakeCompletions:
        async def create(self, **kwargs):
            return next(responses)

    client = SimpleNamespace(chat=SimpleNamespace(completions=FakeCompletions()))
    record = {
        "question": "What is the answer?",
        "expected_behavior": "answer",
        "reference": "A",
        "retrieved_contexts": ["A"],
        "response": "A",
    }

    score, rationale, usage = asyncio.run(
        evaluator.judge_behavior_openai(
            record,
            client=client,
            model="glm-5.3-flash",
            max_tokens=4096,
            max_attempts=3,
        )
    )

    assert score == 2
    assert rationale == "Correct answer."
    assert usage["behavior_judge_attempts"] == 2
    assert usage["behavior_judge_attempt_errors"] == ["invalid behavior judge result"]


def test_build_ragas_llm_sets_configured_token_budget():
    evaluator = load_module()
    captured = {}

    def fake_factory(model, **kwargs):
        captured["model"] = model
        captured.update(kwargs)
        return "llm"

    result = evaluator.build_ragas_llm(
        fake_factory,
        model="glm-5.3-flash",
        client="client",
        max_tokens=4096,
        reasoning_effort="low",
    )

    assert result == "llm"
    assert captured == {
        "model": "glm-5.3-flash",
        "client": "client",
        "temperature": 0,
        "seed": 20260902,
        "max_tokens": 4096,
        "reasoning_effort": "low",
    }


def test_evaluate_record_uses_external_openai_behavior_client():
    evaluator = load_module()
    captured = {}

    class FakeMetric:
        async def ascore(self, **kwargs):
            return SimpleNamespace(value=1.0)

    class FakeCompletions:
        async def create(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(
                            content='{"score": 2, "rationale": "Correct abstention."}'
                        )
                    )
                ],
                usage=SimpleNamespace(prompt_tokens=10, completion_tokens=5),
            )

    client = SimpleNamespace(
        chat=SimpleNamespace(completions=FakeCompletions())
    )
    record = {
        "question": "What value was observed?",
        "expected_behavior": "abstain",
        "reported_behavior": "abstain",
        "reference": None,
        "retrieved_contexts": ["No value is reported."],
        "retrieved_chunk_ids": ["c1"],
        "citations": [],
        "response": "I cannot answer from the supplied contexts.",
    }

    result = asyncio.run(
        evaluator.evaluate_record(
            record,
            FakeMetric(),
            FakeMetric(),
            "glm-5.3-flash",
            behavior_client=client,
            judge_provider="opencode-go",
            judge_max_tokens=4096,
            judge_reasoning_effort="low",
        )
    )

    assert result["behavior_judge_score"] == 2
    assert result["judge_provider"] == "opencode-go"
    assert result["judge_model"] == "glm-5.3-flash"
    assert captured["max_tokens"] == 4096
    assert captured["reasoning_effort"] == "low"
    assert result["judge_reasoning_effort"] == "low"
    assert result["evaluation_prompt_version"] == "rag_behavior_rubric_v2"


def test_evaluate_record_marks_local_behavior_rubric_as_v1(monkeypatch):
    evaluator = load_module()

    class FakeMetric:
        async def ascore(self, **kwargs):
            return SimpleNamespace(value=1.0)

    monkeypatch.setattr(
        evaluator,
        "judge_behavior",
        lambda record, model: (2, "Correct answer.", {}),
    )
    record = {
        "question": "Question?",
        "expected_behavior": "answer",
        "reported_behavior": "answer",
        "reference": "Reference.",
        "retrieved_contexts": ["Context."],
        "retrieved_chunk_ids": ["c1"],
        "citations": ["c1"],
        "response": "Answer.",
    }

    result = asyncio.run(
        evaluator.evaluate_record(
            record,
            FakeMetric(),
            FakeMetric(),
            "gemma3:4b",
            judge_provider="ollama",
        )
    )

    assert result["evaluation_prompt_version"] == "rag_behavior_rubric_v1"


def test_parse_args_accepts_explicit_judge_token_budget(monkeypatch, tmp_path):
    evaluator = load_module()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "evaluate_rag.py",
            "--input",
            str(tmp_path / "input.jsonl"),
            "--output",
            str(tmp_path / "output.jsonl"),
            "--summary",
            str(tmp_path / "summary.json"),
            "--risk-queue",
            str(tmp_path / "risk.jsonl"),
            "--judge-max-tokens",
            "4096",
            "--judge-reasoning-effort",
            "low",
            "--judge-session-id",
            "751f27d8-b165-5b56-bf41-7553b32e7cf4",
        ],
    )

    args = evaluator.parse_args()
    assert args.judge_max_tokens == 4096
    assert args.judge_reasoning_effort == "low"
    assert args.judge_session_id == "751f27d8-b165-5b56-bf41-7553b32e7cf4"


def test_openai_client_kwargs_adds_opencode_session_header():
    evaluator = load_module()
    connection = {
        "base_url": "https://opencode.ai/zen/go/v1",
        "api_key": "secret",
        "external": True,
    }

    result = evaluator.openai_client_kwargs(
        connection,
        judge_session_id="751f27d8-b165-5b56-bf41-7553b32e7cf4",
    )

    assert result["default_headers"] == {
        "x-opencode-session": "751f27d8-b165-5b56-bf41-7553b32e7cf4"
    }


def test_openai_client_kwargs_rejects_opencode_without_session_id():
    evaluator = load_module()
    connection = {
        "base_url": "https://opencode.ai/zen/go/v1",
        "api_key": "secret",
        "external": True,
    }

    try:
        evaluator.openai_client_kwargs(connection, judge_session_id=None)
    except ValueError as exc:
        assert "x-opencode-session" in str(exc)
    else:
        raise AssertionError("OpenCode Go accepted a missing session id")


def test_evaluation_quality_gate_rejects_completely_failed_run():
    evaluator = load_module()
    summary = {
        "row_count": 22,
        "evaluation_error_count": 22,
        "conditions": {
            "dense": {
                "faithfulness_n": 0,
                "factual_correctness_n": 0,
                "behavior_judge_score_n": 0,
            }
        },
    }

    try:
        evaluator.ensure_usable_evaluation(summary)
    except RuntimeError as exc:
        assert "completely failed" in str(exc)
    else:
        raise AssertionError("A completely failed evaluation was accepted")


def test_evaluation_quality_gate_allows_partial_metric_errors():
    evaluator = load_module()
    summary = {
        "row_count": 22,
        "evaluation_error_count": 4,
        "conditions": {
            "bm25": {
                "faithfulness_n": 18,
                "factual_correctness_n": 15,
                "behavior_judge_score_n": 22,
            }
        },
    }

    evaluator.ensure_usable_evaluation(summary)


def test_factual_correctness_applies_to_answer_and_grounded_correction_only():
    evaluator = load_module()

    assert evaluator.metric_applicability({"expected_behavior": "answer", "reference": "A"}) == {
        "faithfulness": True,
        "factual_correctness": True,
    }
    assert evaluator.metric_applicability(
        {"expected_behavior": "grounded_correction", "reference": "Correction"}
    )["factual_correctness"] is True
    assert evaluator.metric_applicability(
        {"expected_behavior": "abstain", "reference": None}
    )["factual_correctness"] is False


def test_score_deterministic_dimensions_checks_behavior_and_citations():
    evaluator = load_module()
    record = {
        "expected_behavior": "answer",
        "reported_behavior": "answer",
        "retrieved_chunk_ids": ["c1", "c2"],
        "citations": ["c1"],
    }

    scores = evaluator.score_deterministic_dimensions(record)

    assert scores == {
        "reported_behavior_match": 1.0,
        "citation_validity": 1.0,
        "citation_presence": 1.0,
    }


def test_score_deterministic_dimensions_requires_no_citations_for_abstention():
    evaluator = load_module()
    record = {
        "expected_behavior": "abstain",
        "reported_behavior": "abstain",
        "retrieved_chunk_ids": ["c1"],
        "citations": [],
    }

    scores = evaluator.score_deterministic_dimensions(record)

    assert scores["citation_presence"] == 1.0
    assert scores["reported_behavior_match"] == 1.0


def test_aggregate_scores_ignores_missing_metric_values():
    evaluator = load_module()
    rows = [
        {"retrieval_condition": "rrf", "faithfulness": 1.0, "factual_correctness": 0.5},
        {"retrieval_condition": "rrf", "faithfulness": 0.0, "factual_correctness": None},
    ]

    summary = evaluator.aggregate_scores(rows)

    assert summary["rrf"]["row_count"] == 2
    assert summary["rrf"]["faithfulness_n"] == 2
    assert summary["rrf"]["faithfulness_mean"] == 0.5
    assert summary["rrf"]["factual_correctness_n"] == 1
    assert summary["rrf"]["factual_correctness_mean"] == 0.5


def test_risk_queue_prioritizes_low_scores_and_metric_disagreement():
    evaluator = load_module()
    rows = [
        {
            "qid": "q1",
            "retrieval_condition": "rrf",
            "faithfulness": 0.95,
            "factual_correctness": 0.95,
            "behavior_judge_score": 2,
            "reported_behavior_match": 1.0,
        },
        {
            "qid": "q2",
            "retrieval_condition": "rerank",
            "faithfulness": 0.9,
            "factual_correctness": 0.2,
            "behavior_judge_score": 1,
            "reported_behavior_match": 1.0,
        },
    ]

    risks = evaluator.build_risk_queue(rows, low_threshold=0.5, disagreement_threshold=0.5)

    assert [row["qid"] for row in risks] == ["q2"]
    assert "low_factual_correctness" in risks[0]["risk_reasons"]
    assert "metric_disagreement" in risks[0]["risk_reasons"]
    assert "behavior_judge_below_full" in risks[0]["risk_reasons"]
