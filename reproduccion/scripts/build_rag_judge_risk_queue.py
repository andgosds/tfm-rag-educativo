from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, cast


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Carga los registros JSONL de evaluación o revisión previa."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    """Indexa por estrategia y pregunta, rechazando unidades duplicadas."""
    indexed = {(row["retrieval_condition"], row["qid"]): row for row in rows}
    if len(indexed) != len(rows):
        raise ValueError("duplicate retrieval condition and qid")
    return indexed


def _is_number(value: object) -> bool:
    """Reconoce valores numéricos sin aceptar booleanos como puntuaciones."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _judge_view(row: dict[str, Any]) -> dict[str, Any]:
    """Extrae las puntuaciones, razones y errores del juez que acompañan la revisión."""
    return {
        "faithfulness": row.get("faithfulness"),
        "factual_correctness": row.get("factual_correctness"),
        "behavior_judge_score": row.get("behavior_judge_score"),
        "behavior_judge_rationale": row.get("behavior_judge_rationale"),
        "evaluation_errors": row.get("evaluation_errors", []),
        "evaluation_prompt_version": row.get("evaluation_prompt_version"),
    }


def _same_review_unit(current: dict[str, Any], previous: dict[str, Any]) -> bool:
    """Comprueba si pregunta, respuesta, referencia y contexto coinciden con la revisión previa."""
    fields = (
        "question",
        "expected_behavior",
        "reference",
        "response",
        "retrieved_chunk_ids",
        "retrieved_contexts",
    )
    return all(current.get(field) == previous.get(field) for field in fields)


def build_queue(
    gemma_rows: list[dict[str, Any]],
    glm_rows: list[dict[str, Any]],
    *,
    previous_rows: list[dict[str, Any]] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Selecciona casos de riesgo entre dos jueces y conserva las adjudicaciones aún válidas."""
    gemma = _index(gemma_rows)
    glm = _index(glm_rows)
    if set(gemma) != set(glm):
        raise ValueError("judge case sets differ")
    previous = _index(previous_rows or [])

    queue = []
    preserved = 0
    for key in sorted(gemma):
        left = gemma[key]
        right = glm[key]
        reasons: list[str] = []
        if left.get("expected_behavior") != "answer":
            reasons.append(f"sensitive_behavior:{left.get('expected_behavior')}")
        if left.get("evaluation_errors"):
            reasons.append("gemma_evaluation_error")
        if right.get("evaluation_errors"):
            reasons.append("glm_evaluation_error")
        if left.get("behavior_judge_score") != right.get("behavior_judge_score"):
            reasons.append("behavior_score_disagreement")
        if left.get("reported_behavior_match") != 1 or right.get("reported_behavior_match") != 1:
            reasons.append("reported_behavior_mismatch")
        for metric in ("faithfulness", "factual_correctness"):
            left_value = left.get(metric)
            right_value = right.get(metric)
            if _is_number(left_value) and float(cast(float, left_value)) < 0.5:
                reasons.append(f"gemma_{metric}_below_0.5")
            if _is_number(right_value) and float(cast(float, right_value)) < 0.5:
                reasons.append(f"glm_{metric}_below_0.5")
            if (
                _is_number(left_value)
                and _is_number(right_value)
                and abs(
                    float(cast(float, right_value))
                    - float(cast(float, left_value))
                )
                >= 0.5
            ):
                reasons.append(f"{metric}_interjudge_delta_at_least_0.5")
        if not reasons:
            continue

        human = {
            "status": "pending",
            "faithfulness_assessment": None,
            "factual_correctness_assessment": None,
            "behavior_score": None,
            "notes": None,
        }
        previous_row = previous.get(key, {})
        previous_human = previous_row.get("human_adjudication")
        if (
            previous_human
            and previous_human.get("status") == "adjudicated"
            and _same_review_unit(left, previous_row)
        ):
            human = previous_human
            preserved += 1
        queue.append(
            {
                "retrieval_condition": key[0],
                "qid": key[1],
                "priority_reasons": reasons,
                "question": left["question"],
                "answerability": left.get("answerability"),
                "expected_behavior": left.get("expected_behavior"),
                "reference": left.get("reference"),
                "response": left.get("response"),
                "reported_behavior": left.get("reported_behavior"),
                "reported_behavior_match": left.get("reported_behavior_match"),
                "citations": left.get("citations"),
                "retrieved_chunk_ids": left.get("retrieved_chunk_ids"),
                "retrieved_contexts": left.get("retrieved_contexts"),
                "gemma3_4b": _judge_view(left),
                "glm53flash_low": _judge_view(right),
                "human_adjudication": human,
            }
        )

    summary = {
        "source_case_count": len(gemma),
        "queued_case_count": len(queue),
        "queued_unique_qids": len({row["qid"] for row in queue}),
        "preserved_adjudication_count": preserved,
        "pending_adjudication_count": len(queue) - preserved,
        "by_condition": dict(
            sorted(Counter(row["retrieval_condition"] for row in queue).items())
        ),
        "by_expected_behavior": dict(
            sorted(Counter(row["expected_behavior"] for row in queue).items())
        ),
        "reason_counts": dict(
            sorted(
                Counter(
                    reason
                    for row in queue
                    for reason in row["priority_reasons"]
                ).items()
            )
        ),
        "rules": {
            "include_non_answer_behavior": True,
            "include_any_evaluation_error": True,
            "include_behavior_score_disagreement": True,
            "include_reported_behavior_mismatch": True,
            "low_metric_threshold": 0.5,
            "interjudge_absolute_delta_threshold": 0.5,
        },
    }
    return queue, summary


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    """Guarda la cola de revisión como registros JSONL con texto Unicode."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    """Lee las fuentes de ambos jueces y las rutas de la cola y su resumen."""
    parser = argparse.ArgumentParser(
        description="Build a reproducible human risk queue from two aligned RAG judges"
    )
    parser.add_argument("--gemma", type=Path, action="append", required=True)
    parser.add_argument("--glm", type=Path, action="append", required=True)
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    """Construye la cola humana de riesgo y exporta sus recuentos de selección."""
    args = parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="build_rag_judge_risk_queue")
    gemma_rows = [row for path in args.gemma for row in read_jsonl(path)]
    glm_rows = [row for path in args.glm for row in read_jsonl(path)]
    previous_rows = read_jsonl(args.previous) if args.previous else None
    queue, summary = build_queue(
        gemma_rows, glm_rows, previous_rows=previous_rows
    )
    write_jsonl(args.output, queue)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()