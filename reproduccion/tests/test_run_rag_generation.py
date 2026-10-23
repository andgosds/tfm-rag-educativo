from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_rag_generation.py"


def load_module():
    spec = importlib.util.spec_from_file_location("run_rag_generation", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def test_build_prompt_requires_grounded_answer_correction_or_abstention():
    rag = load_module()
    messages = rag.build_messages(
        question="Why does X increase?",
        contexts=[{"chunk_id": "chunk-1", "text": "X decreases."}],
    )

    joined = "\n".join(message["content"] for message in messages)
    assert "use only the supplied contexts" in joined.lower()
    assert "correct the premise" in joined.lower()
    assert "cannot answer from the supplied contexts" in joined
    assert "chunk-1" in joined


def test_validate_generation_result_rejects_unknown_citations():
    rag = load_module()

    with pytest.raises(ValueError, match="citation outside retrieved contexts"):
        rag.validate_generation_result(
            {"answer": "A", "behavior": "answer", "citations": ["chunk-2"]},
            retrieved_chunk_ids=["chunk-1"],
        )


def test_parse_text_contract_extracts_behavior_answer_and_citations():
    rag = load_module()
    parsed = rag.parse_text_contract(
        "BEHAVIOR: grounded_correction\n"
        "ANSWER: The premise is false.\n"
        "CITATIONS: chunk-1, chunk-2"
    )

    assert parsed == {
        "answer": "The premise is false.",
        "behavior": "grounded_correction",
        "citations": ["chunk-1", "chunk-2"],
    }


def test_parse_text_contract_accepts_inline_citations_field():
    rag = load_module()
    parsed = rag.parse_text_contract(
        "BEHAVIOR: grounded_correction\n"
        "ANSWER: The premise is false. CITATIONS: chunk-1"
    )

    assert parsed["answer"] == "The premise is false."
    assert parsed["citations"] == ["chunk-1"]


def test_parse_text_contract_accepts_none_for_abstention():
    rag = load_module()
    parsed = rag.parse_text_contract(
        "BEHAVIOR: abstain\n"
        "ANSWER: I cannot answer from the supplied contexts.\n"
        "CITATIONS: NONE"
    )

    assert parsed["citations"] == []
    assert parsed["behavior"] == "abstain"


def test_generate_validated_retries_unknown_citation_with_allowed_ids():
    rag = load_module()
    calls = []
    outputs = iter(
        [
            (
                {"answer": "First", "behavior": "answer", "citations": ["chunk-x"]},
                {"raw_generation_text": "invalid"},
            ),
            (
                {"answer": "Second", "behavior": "answer", "citations": ["chunk-1"]},
                {"raw_generation_text": "valid"},
            ),
        ]
    )

    def generator(messages):
        calls.append(messages)
        return next(outputs)

    result, usage = rag.generate_validated(
        [{"role": "user", "content": "Question"}],
        generator,
        retrieved_chunk_ids=["chunk-1"],
        max_attempts=2,
    )

    assert result["answer"] == "Second"
    assert usage["generation_attempts"] == 2
    assert "chunk-1" in calls[1][-1]["content"]
    assert "chunk-x" not in result["citations"]


def test_terminal_failure_preserves_all_raw_attempts_and_usage():
    rag = load_module()
    calls = []
    def generator(messages):
        calls.append(messages)
        return ({"answer": "A", "behavior": "answer", "citations": ["invented"]},
                {"raw_generation_text": "CITATIONS: invented", "prompt_tokens": 10,
                 "completion_tokens": 2, "generation_latency_ms": 5})
    with pytest.raises(ValueError) as caught:
        rag.generate_validated([], generator, retrieved_chunk_ids=["real"], max_attempts=3)
    assert len(calls) == 3
    assert caught.value.usage["generation_attempts"] == 3
    assert caught.value.usage["prompt_tokens"] == 30
    assert caught.value.usage["generation_latency_ms"] == 15
    assert caught.value.usage["raw_generation_attempts"] == ["CITATIONS: invented"] * 3


def test_build_reference_uses_corrective_answer_for_false_premise():
    rag = load_module()
    golden = {"qid": "q-1", "answerability": "unanswerable", "gold_answer": None}
    resolutions = {
        "q-1": {
            "expected_response_behavior": "grounded_correction",
            "corrective_reference_answer": "X decreases.",
        }
    }

    reference, expected_behavior = rag.build_reference(golden, resolutions)

    assert reference == "X decreases."
    assert expected_behavior == "grounded_correction"


def test_run_experiment_writes_one_top5_record_per_question(tmp_path):
    rag = load_module()
    chunks_path = tmp_path / "chunks.jsonl"
    golden_path = tmp_path / "golden.jsonl"
    run_path = tmp_path / "run.jsonl"
    resolutions_path = tmp_path / "resolutions.json"
    output_path = tmp_path / "outputs" / "rag.jsonl"

    write_jsonl(
        chunks_path,
        [
            {"chunk_id": f"chunk-{i}", "text": f"context {i}"}
            for i in range(1, 7)
        ],
    )
    write_jsonl(
        golden_path,
        [
            {
                "qid": "q-1",
                "question": "Question?",
                "answerability": "answerable",
                "unanswerable_category": None,
                "gold_answer": "Reference.",
            }
        ],
    )
    write_jsonl(
        run_path,
        [
            {"qid": "q-1", "question": "Question?", "chunk_id": f"chunk-{i}", "rank": i}
            for i in range(1, 7)
        ],
    )
    resolutions_path.write_text(json.dumps({"resolutions": []}), encoding="utf-8")

    rag.run_experiment(
        experiment_id="rag_test",
        retrieval_condition="rrf",
        retrieval_run_path=run_path,
        chunks_path=chunks_path,
        golden_path=golden_path,
        resolutions_path=resolutions_path,
        output_path=output_path,
        top_k=5,
        generator=lambda messages: (
            {"answer": "Answer.", "behavior": "answer", "citations": ["chunk-1"]},
            {"generation_latency_ms": 12.0, "prompt_tokens": 10, "completion_tokens": 3},
        ),
        generator_model="model:1",
        prompt_version="rag_answer_prompt_v1",
    )

    rows = [json.loads(line) for line in output_path.read_text().splitlines()]
    assert len(rows) == 1
    assert rows[0]["retrieved_chunk_ids"] == [f"chunk-{i}" for i in range(1, 6)]
    assert len(rows[0]["retrieved_contexts"]) == 5
    assert rows[0]["reference"] == "Reference."
    assert rows[0]["expected_behavior"] == "answer"
    assert rows[0]["response"] == "Answer."
    assert rows[0]["citations"] == ["chunk-1"]


def test_ollama_parse_failure_retains_raw_usage(monkeypatch):
    rag = load_module()
    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def read(self):
            return json.dumps({"message": {"content": "malformed"}, "eval_count": 7}).encode()
    monkeypatch.setattr(rag.urllib.request, "urlopen", lambda *a, **k: Response())
    with pytest.raises(ValueError) as caught:
        rag.generate_validated([], rag.ollama_generator("m"), retrieved_chunk_ids=["c"], max_attempts=3)
    assert caught.value.usage["raw_generation_attempts"] == ["malformed"] * 3
    assert caught.value.usage["completion_tokens"] == 21


def test_terminal_failures_are_separate_continue_and_skip_on_resume(tmp_path):
    rag = load_module()
    write_jsonl(tmp_path / "chunks", [{"chunk_id": "c", "text": "context"}])
    write_jsonl(tmp_path / "golden", [{"qid": q, "question": q, "answerability": "answerable", "gold_answer": "ref"} for q in ("bad", "good")])
    write_jsonl(tmp_path / "run", [{"qid": q, "chunk_id": "c", "rank": 1} for q in ("bad", "good")])
    (tmp_path / "res").write_text('{"resolutions": []}')
    calls = []
    def generator(messages):
        calls.append(messages)
        bad = "Question:\nbad" in messages[1]["content"]
        return ({"answer": "a", "behavior": "answer", "citations": ["wrong" if bad else "c"]}, {"raw_generation_text": "raw", "prompt_tokens": 1})
    kwargs = dict(experiment_id="exp", retrieval_condition="rrf", retrieval_run_path=tmp_path / "run", chunks_path=tmp_path / "chunks", golden_path=tmp_path / "golden", resolutions_path=tmp_path / "res", output_path=tmp_path / "out.jsonl", top_k=1, generator=generator, generator_model="m", prompt_version="p")
    metadata = rag.run_experiment(**kwargs)
    assert [r["qid"] for r in rag.read_jsonl(tmp_path / "out.jsonl")] == ["good"]
    failures = rag.read_jsonl(tmp_path / "out_failures.jsonl")
    assert failures[0]["qid"] == "bad"
    assert failures[0]["status"] == "failed"
    assert failures[0]["generation_attempts"] == 3
    assert metadata["accepted_count"] == metadata["failed_count"] == 1
    rag.run_experiment(**kwargs)
    assert len(calls) == 4
    assert len(rag.read_jsonl(tmp_path / "out_failures.jsonl")) == 1
    # Resume must reject cross-condition contamination before any model call.
    rows = rag.read_jsonl(tmp_path / "out.jsonl")
    rows[0]["retrieval_condition"] = "dense"
    write_jsonl(tmp_path / "out.jsonl", rows)
    with pytest.raises(ValueError, match="condition"):
        rag.run_experiment(**kwargs)
    assert len(calls) == 4


def test_run_experiment_rejects_traversal_before_output_creation(tmp_path):
    rag = load_module()
    output_path = tmp_path / "outputs" / "rag.jsonl"

    with pytest.raises(ValueError, match="experiment_id must contain only"):
        rag.run_experiment(
            experiment_id="../escape",
            retrieval_condition="rrf",
            retrieval_run_path=tmp_path / "missing-run.jsonl",
            chunks_path=tmp_path / "missing-chunks.jsonl",
            golden_path=tmp_path / "missing-golden.jsonl",
            resolutions_path=tmp_path / "missing-resolutions.json",
            output_path=output_path,
            top_k=5,
            generator=lambda messages: ({}, {}),
            generator_model="model:1",
            prompt_version="v1",
        )

    assert not output_path.parent.exists()
