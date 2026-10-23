from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_golden_set.py"


def load_validator():
    if not MODULE_PATH.exists():
        pytest.fail("El validador del golden set todavía no está implementado")
    spec = importlib.util.spec_from_file_location("validate_golden_set", MODULE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_answerable_record() -> dict:
    return {
        "schema_version": "golden_set_v1",
        "corpus_version": "corpus_v1",
        "chunking_method": "section_paragraphs_300w_overlap60_v1",
        "qid": "q-v1-001",
        "question": "What is the mean of the standard normal distribution?",
        "question_language": "en",
        "question_type": "factual",
        "answerability": "answerable",
        "unanswerable_category": None,
        "gold_answer": "The mean of the standard normal distribution is zero.",
        "answer_language": "en",
        "evidence_sufficient": True,
        "evidence": [
            {
                "chunk_id": "chunk-001",
                "relevance_grade": 2,
                "is_canonical": True,
                "quote": "The mean for the standard normal distribution is zero.",
                "supports": "Directly states the requested value.",
                "source_verified": False,
                "verification_note": "",
            }
        ],
        "notes": "",
        "question_origin": "human",
        "annotator_id": "annotator-01",
        "reviews": [],
        "human_adjudication": None,
        "annotation_status": "draft",
    }


def test_validate_answerable_record_accepts_canonical_direct_evidence():
    validator = load_validator()
    chunks = {
        "chunk-001": {
            "chunk_id": "chunk-001",
            "text": "The mean for the standard normal distribution is zero.",
            "formula_risk": False,
        }
    }

    errors = validator.validate_record(valid_answerable_record(), chunks)

    assert errors == []


def test_unanswerable_question_preserves_semantic_type():
    validator = load_validator()
    record = valid_answerable_record()
    record.update(
        question_type="factual",
        answerability="unanswerable",
        unanswerable_category="missing_evidence",
        gold_answer=None,
        answer_language=None,
        evidence_sufficient=False,
        evidence=[],
        notes="The corpus does not state this value.",
    )

    errors = validator.validate_record(record, {})

    assert errors == []


def test_formula_risk_evidence_requires_documented_source_verification():
    validator = load_validator()
    record = valid_answerable_record()
    chunks = {
        "chunk-001": {
            "chunk_id": "chunk-001",
            "text": "The mean for the standard normal distribution is zero.",
            "formula_risk": True,
        }
    }

    errors = validator.validate_record(record, chunks)
    assert any("source verification" in error for error in errors)

    record["evidence"][0]["source_verified"] = True
    record["evidence"][0]["verification_note"] = "Checked against PDF page 336."
    assert validator.validate_record(record, chunks) == []


def test_comparative_question_can_require_multiple_canonical_chunks():
    validator = load_validator()
    record = valid_answerable_record()
    record["question_type"] = "comparative"
    record["evidence"].append(
        {
            "chunk_id": "chunk-002",
            "relevance_grade": 2,
            "is_canonical": True,
            "quote": "The second method has lower variance.",
            "supports": "Provides the second side of the comparison.",
            "source_verified": False,
            "verification_note": "",
        }
    )
    chunks = {
        "chunk-001": {
            "chunk_id": "chunk-001",
            "text": "The mean for the standard normal distribution is zero.",
            "formula_risk": False,
        },
        "chunk-002": {
            "chunk_id": "chunk-002",
            "text": "The second method has lower variance.",
            "formula_risk": False,
        },
    }

    assert validator.validate_record(record, chunks) == []


def test_duplicate_evidence_chunk_is_rejected():
    validator = load_validator()
    record = valid_answerable_record()
    record["evidence"].append(record["evidence"][0].copy())
    chunks = {
        "chunk-001": {
            "chunk_id": "chunk-001",
            "text": "The mean for the standard normal distribution is zero.",
            "formula_risk": False,
        }
    }

    errors = validator.validate_record(record, chunks)

    assert any("duplicate evidence chunk_id" in error for error in errors)


def test_reviewed_record_requires_llm_reviews_and_human_adjudication():
    validator = load_validator()
    record = valid_answerable_record()
    record["annotation_status"] = "reviewed"
    chunks = {
        "chunk-001": {
            "chunk_id": "chunk-001",
            "text": "The mean for the standard normal distribution is zero.",
            "formula_risk": False,
        }
    }

    errors = validator.validate_record(record, chunks)

    assert any("LLM review" in error for error in errors)
    assert any("human_adjudication" in error for error in errors)


def test_adjudicated_record_accepts_multiple_llm_reviews_and_human_decision():
    validator = load_validator()
    record = valid_answerable_record()
    record["annotation_status"] = "adjudicated"
    record["reviews"] = [
        {
            "reviewer_type": "llm",
            "reviewer_id": "model-a",
            "model_version": "model-a-2026-08",
            "prompt_version": "gold-review-v1",
            "answerability_decision": "answerable",
            "evidence_sufficient_decision": True,
            "reference_answer_decision": "accept",
            "rationale": "The cited chunk directly supports the answer.",
            "confidence": 0.9,
            "execution_date": "2026-08-13",
        },
        {
            "reviewer_type": "llm",
            "reviewer_id": "model-b",
            "model_version": "model-b-2026-08",
            "prompt_version": "gold-review-v1",
            "answerability_decision": "answerable",
            "evidence_sufficient_decision": True,
            "reference_answer_decision": "accept",
            "rationale": "The answer is fully grounded in the quote.",
            "confidence": 0.85,
            "execution_date": "2026-08-13",
        },
    ]
    record["human_adjudication"] = {
        "reviewer_id": "andres",
        "final_answerability": "answerable",
        "final_evidence_sufficient": True,
        "decision": "accept",
        "rationale": "Human review confirms the annotation.",
    }
    chunks = {
        "chunk-001": {
            "chunk_id": "chunk-001",
            "text": "The mean for the standard normal distribution is zero.",
            "formula_risk": False,
        }
    }

    assert validator.validate_record(record, chunks) == []


def test_llm_review_requires_execution_date():
    validator = load_validator()
    record = valid_answerable_record()
    record["reviews"] = [
        {
            "reviewer_type": "llm",
            "reviewer_id": "judge-1",
            "model_version": "gpt-5.6-sol; reasoning_effort=high",
            "prompt_version": "golden-set-review-v1",
            "answerability_decision": "answerable",
            "evidence_sufficient_decision": True,
            "reference_answer_decision": "accept",
            "rationale": "The cited evidence supports the proposed answer.",
            "confidence": 0.9,
        }
    ]
    chunks = {
        "chunk-001": {
            "chunk_id": "chunk-001",
            "text": "The mean for the standard normal distribution is zero.",
            "formula_risk": False,
        }
    }

    errors = validator.validate_record(record, chunks)

    assert any("execution_date" in error for error in errors)


def test_unanswerable_record_requires_a_valid_category():
    validator = load_validator()
    record = valid_answerable_record()
    record.update(
        answerability="unanswerable",
        unanswerable_category=None,
        gold_answer=None,
        answer_language=None,
        evidence_sufficient=False,
        evidence=[],
        notes="The requested result is not present in the corpus.",
    )

    errors = validator.validate_record(record, {})

    assert any("unanswerable_category" in error for error in errors)


def test_qid_must_follow_stable_v1_pattern():
    validator = load_validator()
    record = valid_answerable_record()
    record["qid"] = "question-one"
    chunks = {
        "chunk-001": {
            "chunk_id": "chunk-001",
            "text": "The mean for the standard normal distribution is zero.",
            "formula_risk": False,
        }
    }

    errors = validator.validate_record(record, chunks)

    assert any("qid must match" in error for error in errors)


def test_validate_file_uses_real_chunk_collection_and_rejects_duplicate_qid(tmp_path):
    validator = load_validator()
    chunks_path = ROOT / "data" / "processed" / "chunks_v1.jsonl"
    first_chunk = json.loads(chunks_path.read_text(encoding="utf-8").splitlines()[0])
    record = valid_answerable_record()
    record["evidence"][0].update(
        chunk_id=first_chunk["chunk_id"],
        quote=first_chunk["text"].splitlines()[0],
    )
    golden_path = tmp_path / "golden.jsonl"
    golden_path.write_text(json.dumps(record) + "\n", encoding="utf-8")

    assert validator.validate_file(golden_path, chunks_path) == []

    golden_path.write_text(
        json.dumps(record) + "\n" + json.dumps(record) + "\n",
        encoding="utf-8",
    )
    errors = validator.validate_file(golden_path, chunks_path)
    assert any("duplicate qid" in error for error in errors)
