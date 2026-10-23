from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "golden_set_v1"
CORPUS_VERSION = "corpus_v1"
CHUNKING_METHOD = "section_paragraphs_300w_overlap60_v1"
QUESTION_LANGUAGES = {"en"}
QUESTION_TYPES = {"factual", "explanatory", "comparative", "procedural"}
ANSWERABILITY = {"answerable", "unanswerable"}
UNANSWERABLE_CATEGORIES = {
    "out_of_scope",
    "nonexistent_entity_or_concept",
    "false_premise",
    "missing_evidence",
    "insufficient_evidence",
}
QUESTION_ORIGINS = {"human", "llm_assisted"}
ANNOTATION_STATUS = {"draft", "reviewed", "adjudicated"}
RELEVANCE_GRADES = {0, 1, 2}
REFERENCE_ANSWER_DECISIONS = {"accept", "revise", "not_applicable"}
ADJUDICATION_DECISIONS = {"accept", "revise", "exclude"}


def validate_record(record: dict[str, Any], chunks: dict[str, dict[str, Any]]) -> list[str]:
    """Comprueba el esquema, la revisión y la coherencia de la evidencia de una pregunta."""
    errors: list[str] = []
    required = {
        "schema_version",
        "corpus_version",
        "chunking_method",
        "qid",
        "question",
        "question_language",
        "question_type",
        "answerability",
        "unanswerable_category",
        "gold_answer",
        "answer_language",
        "evidence_sufficient",
        "evidence",
        "notes",
        "question_origin",
        "annotator_id",
        "reviews",
        "human_adjudication",
        "annotation_status",
    }
    missing = sorted(required - record.keys())
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")
        return errors

    if record["schema_version"] != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if record["corpus_version"] != CORPUS_VERSION:
        errors.append(f"corpus_version must be {CORPUS_VERSION}")
    if record["chunking_method"] != CHUNKING_METHOD:
        errors.append(f"chunking_method must be {CHUNKING_METHOD}")
    if not isinstance(record["qid"], str) or not record["qid"].strip():
        errors.append("qid must be a non-empty string")
    elif re.fullmatch(r"q-v1-[0-9]{3}", record["qid"]) is None:
        errors.append("qid must match q-v1-NNN")
    if not isinstance(record["question"], str) or not record["question"].strip():
        errors.append("question must be a non-empty string")
    if record["question_language"] not in QUESTION_LANGUAGES:
        errors.append("question_language must be en for golden_set_v1")
    if record["answerability"] == "answerable" and record["answer_language"] not in QUESTION_LANGUAGES:
        errors.append("answerable questions require answer_language=en")
    if record["question_type"] not in QUESTION_TYPES:
        errors.append("invalid question_type")
    if record["answerability"] not in ANSWERABILITY:
        errors.append("invalid answerability")
    if record["question_origin"] not in QUESTION_ORIGINS:
        errors.append("question_origin must be human or llm_assisted")
    if not isinstance(record["annotator_id"], str) or not record["annotator_id"].strip():
        errors.append("annotator_id must be a non-empty string")
    if record["annotation_status"] not in ANNOTATION_STATUS:
        errors.append("invalid annotation_status")
    if not isinstance(record["reviews"], list):
        errors.append("reviews must be a list")
        reviews: list[Any] = []
    else:
        reviews = record["reviews"]
    for index, review in enumerate(reviews):
        prefix = f"reviews[{index}]"
        if not isinstance(review, dict):
            errors.append(f"{prefix} must be an object")
            continue
        required_review_fields = {
            "reviewer_type",
            "reviewer_id",
            "model_version",
            "prompt_version",
            "answerability_decision",
            "evidence_sufficient_decision",
            "reference_answer_decision",
            "rationale",
            "confidence",
            "execution_date",
        }
        missing_review = sorted(required_review_fields - review.keys())
        if missing_review:
            errors.append(f"{prefix} missing fields: {', '.join(missing_review)}")
            continue
        if review["reviewer_type"] != "llm":
            errors.append(f"{prefix}.reviewer_type must be llm")
        for field in ("reviewer_id", "model_version", "prompt_version", "rationale"):
            if not isinstance(review[field], str) or not review[field].strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")
        if review["answerability_decision"] not in ANSWERABILITY:
            errors.append(f"{prefix}.answerability_decision is invalid")
        if not isinstance(review["evidence_sufficient_decision"], bool):
            errors.append(f"{prefix}.evidence_sufficient_decision must be boolean")
        if review["reference_answer_decision"] not in REFERENCE_ANSWER_DECISIONS:
            errors.append(f"{prefix}.reference_answer_decision is invalid")
        confidence = review["confidence"]
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1:
            errors.append(f"{prefix}.confidence must be between 0 and 1")
        execution_date = review["execution_date"]
        if not isinstance(execution_date, str):
            errors.append(f"{prefix}.execution_date must be an ISO date")
        else:
            try:
                date.fromisoformat(execution_date)
            except ValueError:
                errors.append(f"{prefix}.execution_date must be an ISO date")

    human_adjudication = record["human_adjudication"]
    if human_adjudication is not None:
        if not isinstance(human_adjudication, dict):
            errors.append("human_adjudication must be an object or null")
        else:
            required_human_fields = {
                "reviewer_id",
                "final_answerability",
                "final_evidence_sufficient",
                "decision",
                "rationale",
            }
            missing_human = sorted(required_human_fields - human_adjudication.keys())
            if missing_human:
                errors.append(f"human_adjudication missing fields: {', '.join(missing_human)}")
            else:
                if not isinstance(human_adjudication["reviewer_id"], str) or not human_adjudication["reviewer_id"].strip():
                    errors.append("human_adjudication.reviewer_id must be a non-empty string")
                if human_adjudication["final_answerability"] not in ANSWERABILITY:
                    errors.append("human_adjudication.final_answerability is invalid")
                if not isinstance(human_adjudication["final_evidence_sufficient"], bool):
                    errors.append("human_adjudication.final_evidence_sufficient must be boolean")
                if human_adjudication["decision"] not in ADJUDICATION_DECISIONS:
                    errors.append("human_adjudication.decision is invalid")
                if not isinstance(human_adjudication["rationale"], str) or not human_adjudication["rationale"].strip():
                    errors.append("human_adjudication.rationale must be a non-empty string")

    if record["annotation_status"] in {"reviewed", "adjudicated"}:
        minimum_reviews = 2 if record["annotation_status"] == "adjudicated" else 1
        if len(reviews) < minimum_reviews:
            errors.append(
                f"{record['annotation_status']} records require at least {minimum_reviews} LLM review(s)"
            )
        if human_adjudication is None:
            errors.append("reviewed or adjudicated records require human_adjudication")
    if not isinstance(record["evidence_sufficient"], bool):
        errors.append("evidence_sufficient must be boolean")
    if not isinstance(record["evidence"], list):
        errors.append("evidence must be a list")
        return errors

    canonical_count = 0
    direct_count = 0
    seen_evidence_ids: set[str] = set()
    for index, evidence in enumerate(record["evidence"]):
        prefix = f"evidence[{index}]"
        if not isinstance(evidence, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in (
            "chunk_id",
            "relevance_grade",
            "is_canonical",
            "quote",
            "supports",
            "source_verified",
            "verification_note",
        ):
            if field not in evidence:
                errors.append(f"{prefix}.{field} is required")
        if "chunk_id" not in evidence:
            continue
        chunk_id = evidence["chunk_id"]
        if chunk_id in seen_evidence_ids:
            errors.append(f"{prefix}: duplicate evidence chunk_id: {chunk_id}")
        seen_evidence_ids.add(chunk_id)
        chunk = chunks.get(chunk_id)
        if chunk is None:
            errors.append(f"{prefix}.chunk_id does not exist: {chunk_id}")
            continue
        grade = evidence.get("relevance_grade")
        if grade not in RELEVANCE_GRADES:
            errors.append(f"{prefix}.relevance_grade must be 0, 1 or 2")
        if grade == 0:
            errors.append(f"{prefix}: grade 0 evidence must not be stored in the gold record")
        if grade == 2:
            direct_count += 1
        if evidence.get("is_canonical") is True:
            canonical_count += 1
            if grade != 2:
                errors.append(f"{prefix}: canonical evidence must have relevance_grade 2")
        quote = evidence.get("quote")
        if not isinstance(quote, str) or not quote.strip():
            errors.append(f"{prefix}.quote must be a non-empty string")
        elif quote not in chunk.get("text", ""):
            errors.append(f"{prefix}.quote is not an exact substring of the chunk text")
        if chunk.get("formula_risk") is True:
            # La extracción puede perder símbolos; estas evidencias exigen contraste con la fuente.
            source_verified = evidence.get("source_verified") is True
            verification_note = evidence.get("verification_note")
            if not source_verified or not isinstance(verification_note, str) or not verification_note.strip():
                errors.append(
                    f"{prefix}: formula-risk chunk requires documented source verification before annotation"
                )

    if record["answerability"] == "answerable":
        if record["unanswerable_category"] is not None:
            errors.append("answerable questions require unanswerable_category=null")
        if not isinstance(record["gold_answer"], str) or not record["gold_answer"].strip():
            errors.append("answerable questions require a non-empty gold_answer")
        if record["evidence_sufficient"] is not True:
            errors.append("answerable questions require evidence_sufficient=true")
        if direct_count == 0:
            errors.append("answerable questions require at least one relevance_grade 2 evidence")
        if canonical_count == 0:
            errors.append("answerable questions require at least one canonical evidence")
    elif record["answerability"] == "unanswerable":
        if record["unanswerable_category"] not in UNANSWERABLE_CATEGORIES:
            errors.append("unanswerable questions require a valid unanswerable_category")
        if record["gold_answer"] not in (None, ""):
            errors.append("unanswerable questions must not include a gold_answer")
        if record["answer_language"] is not None:
            errors.append("unanswerable questions require answer_language=null")
        if record["evidence_sufficient"] is not False:
            errors.append("unanswerable questions require evidence_sufficient=false")
        if direct_count > 0 or canonical_count > 0:
            errors.append("unanswerable questions must not include direct or canonical evidence")
        if not isinstance(record["notes"], str) or not record["notes"].strip():
            errors.append("unanswerable questions require notes explaining the corpus boundary")

    return errors


def load_chunks(path: Path) -> dict[str, dict[str, Any]]:
    """Carga el corpus por identificador y rechaza fragmentos sin clave o duplicados."""
    chunks: dict[str, dict[str, Any]] = {}
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            chunk = json.loads(line)
            chunk_id = chunk.get("chunk_id")
            if not chunk_id:
                raise ValueError(f"chunk without chunk_id at line {line_number}")
            if chunk_id in chunks:
                raise ValueError(f"duplicate chunk_id: {chunk_id}")
            chunks[chunk_id] = chunk
    return chunks


def validate_file(golden_path: Path, chunks_path: Path) -> list[str]:
    """Valida cada pregunta del JSONL y detecta identificadores repetidos o un conjunto vacío."""
    chunks = load_chunks(chunks_path)
    errors: list[str] = []
    seen_qids: set[str] = set()
    with golden_path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_number}: invalid JSON: {exc.msg}")
                continue
            qid = record.get("qid")
            if qid in seen_qids:
                errors.append(f"line {line_number}: duplicate qid: {qid}")
            if isinstance(qid, str):
                seen_qids.add(qid)
            errors.extend(
                f"line {line_number} ({qid or 'unknown qid'}): {error}"
                for error in validate_record(record, chunks)
            )
    if not seen_qids:
        errors.append("golden set contains no records")
    return errors


def parse_args() -> argparse.Namespace:
    """Recoge las rutas del golden set y de los fragmentos congelados."""
    parser = argparse.ArgumentParser(description="Validate a golden-set JSONL file against the frozen chunk collection.")
    parser.add_argument("golden_path", type=Path)
    parser.add_argument("--chunks", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    """Valida el golden set e informa de los errores con un código de salida no nulo."""
    args = parse_args()
    errors = validate_file(args.golden_path, args.chunks)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"PASS: {args.golden_path} is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
