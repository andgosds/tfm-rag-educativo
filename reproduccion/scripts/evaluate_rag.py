from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import statistics
import time
import urllib.request
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse


METRIC_NAMES = (
    "faithfulness",
    "factual_correctness",
    "reported_behavior_match",
    "citation_validity",
    "citation_presence",
    "behavior_judge_score",
)
JUDGE_SEED = 20260902
BEHAVIOR_JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "score": {"type": "integer", "enum": [0, 1, 2]},
        "rationale": {"type": "string"},
    },
    "required": ["score", "rationale"],
}


def resolve_judge_connection(
    *,
    provider: str,
    base_url: str | None = None,
    api_key_env: str | None = None,
) -> dict:
    """Resuelve la conexión y las credenciales del proveedor del juez."""
    if provider == "ollama":
        return {
            "provider": "ollama",
            "base_url": base_url or "http://127.0.0.1:11434/v1",
            "api_key": "ollama",
            "external": False,
        }
    if not base_url:
        raise ValueError("external judge requires --judge-base-url")
    if not api_key_env:
        raise ValueError("external judge requires --judge-api-key-env")
    api_key = os.getenv(api_key_env)
    if not api_key:
        raise ValueError(f"judge credential environment variable is unavailable: {api_key_env}")
    return {
        "provider": provider,
        "base_url": base_url,
        "api_key": api_key,
        "external": True,
    }


def openai_client_kwargs(
    connection: dict, *, judge_session_id: str | None = None
) -> dict:
    """Prepara el cliente y la cabecera de sesión exigida por OpenCode."""
    kwargs = {
        "base_url": connection["base_url"],
        "api_key": connection["api_key"],
    }
    if urlparse(str(connection["base_url"])).hostname == "opencode.ai":
        if not judge_session_id or not judge_session_id.strip():
            raise ValueError(
                "OpenCode Go requires --judge-session-id for x-opencode-session"
            )
        kwargs["default_headers"] = {
            "x-opencode-session": judge_session_id.strip()
        }
    return kwargs


def ensure_usable_evaluation(summary: dict) -> None:
    """Rechaza una evaluación sin puntuaciones cuando han fallado todas las filas."""
    if not summary.get("row_count"):
        return
    conditions = summary.get("conditions", {}).values()
    score_count = sum(
        condition.get("faithfulness_n", 0)
        + condition.get("factual_correctness_n", 0)
        + condition.get("behavior_judge_score_n", 0)
        for condition in conditions
    )
    if (
        summary.get("evaluation_error_count") == summary["row_count"]
        and score_count == 0
    ):
        raise RuntimeError(
            "evaluation completely failed: all rows contain errors and no judge scores are available"
        )


def read_jsonl(path: Path) -> list[dict]:
    """Carga los registros JSONL omitiendo las líneas vacías."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def metric_applicability(record: dict) -> dict[str, bool]:
    """Determina qué métricas proceden según la referencia y la conducta esperada."""
    return {
        "faithfulness": True,
        "factual_correctness": record.get("reference") is not None
        and record["expected_behavior"] in {"answer", "grounded_correction"},
    }


def score_deterministic_dimensions(record: dict) -> dict[str, float]:
    """Puntúa la conducta declarada y la validez y presencia de citas."""
    citations = record["citations"]
    retrieved = set(record["retrieved_chunk_ids"])
    expected = record["expected_behavior"]
    if citations:
        citation_validity = sum(citation in retrieved for citation in citations) / len(citations)
    else:
        citation_validity = 1.0 if expected == "abstain" else 0.0
    citation_presence = float(not citations) if expected == "abstain" else float(bool(citations))
    return {
        "reported_behavior_match": float(record["reported_behavior"] == expected),
        "citation_validity": citation_validity,
        "citation_presence": citation_presence,
    }


def aggregate_scores(rows: list[dict]) -> dict[str, dict]:
    """Resume puntuaciones disponibles y latencias por condición de recuperación."""
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["retrieval_condition"]].append(row)
    summary: dict[str, dict] = {}
    for condition, condition_rows in sorted(grouped.items()):
        stats: dict[str, float | int | None] = {"row_count": len(condition_rows)}
        for metric in METRIC_NAMES:
            values = [
                float(row[metric])
                for row in condition_rows
                if row.get(metric) is not None
                and not (isinstance(row.get(metric), float) and math.isnan(row[metric]))
            ]
            stats[f"{metric}_n"] = len(values)
            stats[f"{metric}_mean"] = statistics.fmean(values) if values else None
        latency = [
            float(row["evaluation_latency_ms"])
            for row in condition_rows
            if row.get("evaluation_latency_ms") is not None
        ]
        stats["evaluation_latency_ms_total"] = sum(latency) if latency else None
        stats["evaluation_latency_ms_mean"] = (
            statistics.fmean(latency) if latency else None
        )
        summary[condition] = stats
    return summary


def build_risk_queue(
    rows: list[dict], *, low_threshold: float = 0.5, disagreement_threshold: float = 0.5
) -> list[dict]:
    """Selecciona respuestas de riesgo por puntuaciones bajas o discrepancias."""
    risks = []
    for row in rows:
        reasons: list[str] = []
        for metric in ("faithfulness", "factual_correctness"):
            value = row.get(metric)
            if value is not None and value < low_threshold:
                reasons.append(f"low_{metric}")
        faithfulness = row.get("faithfulness")
        correctness = row.get("factual_correctness")
        if (
            faithfulness is not None
            and correctness is not None
            and abs(faithfulness - correctness) >= disagreement_threshold
        ):
            reasons.append("metric_disagreement")
        if row.get("behavior_judge_score") is not None and row["behavior_judge_score"] < 2:
            reasons.append("behavior_judge_below_full")
        if row.get("reported_behavior_match") == 0:
            reasons.append("reported_behavior_mismatch")
        if reasons:
            risks.append(
                {
                    "qid": row["qid"],
                    "retrieval_condition": row["retrieval_condition"],
                    "expected_behavior": row.get("expected_behavior"),
                    "response": row.get("response"),
                    "faithfulness": faithfulness,
                    "factual_correctness": correctness,
                    "behavior_judge_score": row.get("behavior_judge_score"),
                    "behavior_judge_rationale": row.get("behavior_judge_rationale"),
                    "risk_reasons": reasons,
                }
            )
    return sorted(risks, key=lambda row: (row["qid"], row["retrieval_condition"]))


def build_behavior_prompt(record: dict) -> str:
    """Compone la rúbrica de conducta con la pregunta, los contextos y la respuesta."""
    rubric = (
        "Score the response against the expected behavior. Do not infer the retrieval condition. "
        "Score 2 when the behavior is fully correct, 1 when partially correct, and 0 when incorrect. "
        "For 'answer', require a substantively correct answer consistent with the reference and contexts. "
        "For 'grounded_correction', require explicit rejection of the false premise plus the correct corpus-grounded correction; plain abstention is not sufficient. "
        "For 'abstain', require a clear statement that the supplied contexts are insufficient and no unsupported answer or speculation. "
        "An appropriate abstention is a complete response and must not be penalized for omitting an answer that the evidence cannot support."
    )
    context_text = "\n\n".join(record["retrieved_contexts"])
    return (
        f"{rubric}\n\nQuestion: {record['question']}\n"
        f"Expected behavior: {record['expected_behavior']}\n"
        f"Reference: {record.get('reference')}\n"
        f"Supplied contexts:\n{context_text}\n\nResponse:\n{record['response']}\n\n"
        'Return exactly one JSON object such as {"score": 2, "rationale": "..."}. '
        'The score must be the integer 0, 1, or 2 and rationale must be a non-empty string. '
        'Use exactly the keys "score" and "rationale"; do not use "answer" or "scores".'
    )


async def judge_behavior_openai(
    record: dict,
    *,
    client,
    model: str,
    seed: int = JUDGE_SEED,
    max_tokens: int = 250,
    max_attempts: int = 3,
    reasoning_effort: str | None = None,
) -> tuple[int, str, dict]:
    """Solicita un juicio de conducta remoto y reintenta las salidas JSON inválidas."""
    attempt_errors: list[str] = []
    prompt_tokens = 0
    completion_tokens = 0
    completion_kwargs = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a strict blinded evaluator for an educational RAG experiment. Return valid JSON only.",
            },
            {"role": "user", "content": build_behavior_prompt(record)},
        ],
        "temperature": 0,
        "seed": seed,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
    }
    if reasoning_effort is not None:
        completion_kwargs["reasoning_effort"] = reasoning_effort
    for attempt in range(1, max_attempts + 1):
        response = await client.chat.completions.create(**completion_kwargs)
        usage = response.usage
        if usage:
            prompt_tokens += usage.prompt_tokens or 0
            completion_tokens += usage.completion_tokens or 0
        try:
            content = response.choices[0].message.content
            if not content:
                raise ValueError("empty behavior judge result")
            result = json.loads(content)
            if result.get("score") not in {0, 1, 2} or not str(
                result.get("rationale", "")
            ).strip():
                raise ValueError("invalid behavior judge result")
        except (json.JSONDecodeError, ValueError) as exc:
            attempt_errors.append(str(exc))
            if attempt == max_attempts:
                raise ValueError(
                    f"behavior judge failed after {max_attempts} attempts: {attempt_errors}"
                ) from exc
            continue
        return (
            int(result["score"]),
            str(result["rationale"]).strip(),
            {
                "behavior_judge_prompt_tokens": prompt_tokens,
                "behavior_judge_completion_tokens": completion_tokens,
                "behavior_judge_attempts": attempt,
                "behavior_judge_attempt_errors": attempt_errors,
            },
        )
    raise RuntimeError("unreachable behavior judge state")


def judge_behavior(
    record: dict,
    *,
    model: str,
    endpoint: str = "http://127.0.0.1:11434/api/chat",
    seed: int = 20260902,
) -> tuple[int, str, dict]:
    """Obtiene de Ollama un juicio de conducta con su latencia y consumo."""
    rubric = (
        "Score the response against the expected behavior. Do not infer the retrieval condition. "
        "Score 2 when the behavior is fully correct, 1 when partially correct, and 0 when incorrect. "
        "For 'answer', require a substantively correct answer consistent with the reference and contexts. "
        "For 'grounded_correction', require explicit rejection of the false premise plus the correct corpus-grounded correction; plain abstention is not sufficient. "
        "For 'abstain', require a clear statement that the supplied contexts are insufficient and no unsupported answer or speculation."
    )
    context_text = "\n\n".join(record["retrieved_contexts"])
    prompt = (
        f"{rubric}\n\nQuestion: {record['question']}\n"
        f"Expected behavior: {record['expected_behavior']}\n"
        f"Reference: {record.get('reference')}\n"
        f"Supplied contexts:\n{context_text}\n\nResponse:\n{record['response']}"
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a strict blinded evaluator for an educational RAG experiment."},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "format": BEHAVIOR_JUDGE_SCHEMA,
        "options": {"temperature": 0, "seed": seed, "num_predict": 250},
        "keep_alive": "30m",
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=300) as response:
        body = json.loads(response.read().decode("utf-8"))
    elapsed_ms = (time.perf_counter() - started) * 1000
    result = json.loads(body["message"]["content"])
    if result["score"] not in {0, 1, 2} or not result["rationale"].strip():
        raise ValueError("invalid behavior judge result")
    usage = {
        "behavior_judge_latency_ms": elapsed_ms,
        "behavior_judge_prompt_tokens": body.get("prompt_eval_count"),
        "behavior_judge_completion_tokens": body.get("eval_count"),
    }
    return result["score"], result["rationale"].strip(), usage


async def evaluate_record(
    record: dict,
    faithfulness_metric,
    factual_metric,
    judge_model: str,
    *,
    behavior_client=None,
    judge_provider: str = "ollama",
    judge_max_tokens: int = 250,
    judge_reasoning_effort: str | None = None,
) -> dict:
    """Evalúa una respuesta con RAGAS y la rúbrica, conservando los errores parciales."""
    started = time.perf_counter()
    applicability = metric_applicability(record)
    faithfulness = None
    factual_correctness = None
    errors: list[str] = []
    if applicability["faithfulness"]:
        try:
            result = await faithfulness_metric.ascore(
                user_input=record["question"],
                response=record["response"],
                retrieved_contexts=record["retrieved_contexts"],
            )
            faithfulness = float(result.value)
        except Exception as exc:
            errors.append(f"faithfulness:{type(exc).__name__}:{exc}")
    if applicability["factual_correctness"]:
        try:
            result = await factual_metric.ascore(
                response=record["response"], reference=record["reference"]
            )
            factual_correctness = float(result.value)
        except Exception as exc:
            errors.append(f"factual_correctness:{type(exc).__name__}:{exc}")
    try:
        if behavior_client is None:
            behavior_score, behavior_rationale, behavior_usage = await asyncio.to_thread(
                judge_behavior, record, model=judge_model
            )
        else:
            behavior_score, behavior_rationale, behavior_usage = await judge_behavior_openai(
                record,
                client=behavior_client,
                model=judge_model,
                seed=JUDGE_SEED,
                max_tokens=judge_max_tokens,
                reasoning_effort=judge_reasoning_effort,
            )
    except Exception as exc:
        behavior_score = None
        behavior_rationale = None
        behavior_usage = {}
        errors.append(f"behavior_judge:{type(exc).__name__}:{exc}")
    deterministic = score_deterministic_dimensions(record)
    return {
        **record,
        "faithfulness": faithfulness,
        "factual_correctness": factual_correctness,
        **deterministic,
        "behavior_judge_score": behavior_score,
        "behavior_judge_rationale": behavior_rationale,
        **behavior_usage,
        "evaluation_latency_ms": (time.perf_counter() - started) * 1000,
        "evaluation_errors": errors,
        "ragas_version": "0.4.3",
        "judge_provider": judge_provider,
        "judge_model": judge_model,
        "judge_seed": JUDGE_SEED,
        "judge_max_tokens": judge_max_tokens,
        "judge_reasoning_effort": judge_reasoning_effort,
        "evaluation_prompt_version": (
            "rag_behavior_rubric_v2"
            if behavior_client is not None
            else "rag_behavior_rubric_v1"
        ),
    }


def build_ragas_llm(
    llm_factory,
    *,
    model: str,
    client,
    max_tokens: int,
    reasoning_effort: str | None = None,
):
    """Configura el modelo de RAGAS con los parámetros fijados para el juez."""
    model_args = {
        "client": client,
        "temperature": 0,
        "seed": JUDGE_SEED,
        "max_tokens": max_tokens,
    }
    if reasoning_effort is not None:
        model_args["reasoning_effort"] = reasoning_effort
    return llm_factory(model, **model_args)


async def run_evaluation(
    *,
    input_paths: list[Path],
    output_path: Path,
    summary_path: Path,
    risk_path: Path,
    judge_model: str,
    judge_provider: str = "ollama",
    judge_base_url: str | None = None,
    judge_api_key_env: str | None = None,
    judge_max_tokens: int | None = None,
    judge_reasoning_effort: str | None = None,
    judge_session_id: str | None = None,
) -> dict:
    """Reanuda la evaluación y guarda resultados, resumen y cola de riesgo."""
    from openai import AsyncOpenAI
    from ragas.llms import llm_factory
    from ragas.metrics.collections import Faithfulness, FactualCorrectness

    connection = resolve_judge_connection(
        provider=judge_provider,
        base_url=judge_base_url,
        api_key_env=judge_api_key_env,
    )
    ragas_max_tokens = judge_max_tokens if judge_max_tokens is not None else 1024
    behavior_max_tokens = judge_max_tokens if judge_max_tokens is not None else 250
    records = [row for path in input_paths for row in read_jsonl(path)]
    keys = [(row["retrieval_condition"], row["qid"]) for row in records]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate retrieval condition and qid")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    completed: set[tuple[str, str]] = set()
    # La clave condición-pregunta permite reanudar sin repetir juicios guardados.
    if output_path.exists():
        completed = {
            (row["retrieval_condition"], row["qid"]) for row in read_jsonl(output_path)
        }

    client = AsyncOpenAI(
        **openai_client_kwargs(
            connection, judge_session_id=judge_session_id
        )
    )
    llm = build_ragas_llm(
        llm_factory,
        model=judge_model,
        client=client,
        max_tokens=ragas_max_tokens,
        reasoning_effort=judge_reasoning_effort,
    )
    faithfulness_metric = Faithfulness(llm=llm)
    factual_metric = FactualCorrectness(llm=llm)
    try:
        with output_path.open("a", encoding="utf-8") as handle:
            for record in records:
                key = (record["retrieval_condition"], record["qid"])
                if key in completed:
                    continue
                evaluated = await evaluate_record(
                    record,
                    faithfulness_metric,
                    factual_metric,
                    judge_model,
                    behavior_client=client if connection["external"] else None,
                    judge_provider=judge_provider,
                    judge_max_tokens=behavior_max_tokens,
                    judge_reasoning_effort=judge_reasoning_effort,
                )
                handle.write(json.dumps(evaluated, ensure_ascii=False) + "\n")
                handle.flush()
    finally:
        await client.close()

    evaluated_rows = read_jsonl(output_path)
    summary = {
        "experiment_id": records[0]["experiment_id"],
        "judge_provider": judge_provider,
        "judge_model": judge_model,
        "judge_seed": JUDGE_SEED,
        "ragas_max_tokens": ragas_max_tokens,
        "behavior_max_tokens": behavior_max_tokens,
        "judge_reasoning_effort": judge_reasoning_effort,
        "ragas_version": "0.4.3",
        "row_count": len(evaluated_rows),
        "conditions": aggregate_scores(evaluated_rows),
        "evaluation_error_count": sum(bool(row["evaluation_errors"]) for row in evaluated_rows),
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    risks = build_risk_queue(evaluated_rows)
    risk_path.parent.mkdir(parents=True, exist_ok=True)
    risk_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in risks),
        encoding="utf-8",
    )
    return summary


def parse_args() -> argparse.Namespace:
    """Recoge las rutas y los parámetros del juez para la evaluación RAG."""
    parser = argparse.ArgumentParser(description="Evaluate controlled RAG outputs with RAGAS and a behavior rubric")
    parser.add_argument("--input", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--risk-queue", type=Path, required=True)
    parser.add_argument("--judge-model", default="gemma3:4b")
    parser.add_argument("--judge-provider", default="ollama")
    parser.add_argument("--judge-base-url")
    parser.add_argument("--judge-api-key-env")
    parser.add_argument("--judge-max-tokens", type=int)
    parser.add_argument(
        "--judge-reasoning-effort", choices=("low", "high", "max")
    )
    parser.add_argument("--judge-session-id")
    return parser.parse_args()


def main() -> None:
    """Ejecuta la evaluación RAG y comprueba que haya puntuaciones utilizables."""
    args = parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="evaluate_rag")
    summary = asyncio.run(
        run_evaluation(
            input_paths=args.input,
            output_path=args.output,
            summary_path=args.summary,
            risk_path=args.risk_queue,
            judge_model=args.judge_model,
            judge_provider=args.judge_provider,
            judge_base_url=args.judge_base_url,
            judge_api_key_env=args.judge_api_key_env,
            judge_max_tokens=args.judge_max_tokens,
            judge_reasoning_effort=args.judge_reasoning_effort,
            judge_session_id=args.judge_session_id,
        )
    )
    ensure_usable_evaluation(summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
