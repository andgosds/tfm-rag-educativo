from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from typing import cast


METRICS = (
    "faithfulness",
    "factual_correctness",
    "behavior_judge_score",
)


def read_jsonl(path: Path) -> list[dict]:
    """Carga los registros JSONL de una ejecución de evaluación RAG."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def read_many_jsonl(paths: list[Path]) -> list[dict]:
    """Concatena las evaluaciones de varias rutas respetando su orden."""
    return [row for path in paths for row in read_jsonl(path)]


def is_value(value) -> bool:
    """Comprueba que el valor no sea nulo ni NaN."""
    return value is not None and not (
        isinstance(value, float) and math.isnan(value)
    )


def execution_summary(rows: list[dict]) -> dict:
    """Resume las latencias, los tokens observados y los reintentos de evaluación."""
    latencies = [
        float(row["evaluation_latency_ms"])
        for row in rows
        if is_value(row.get("evaluation_latency_ms"))
    ]
    prompt_tokens = sum(
        int(row["behavior_judge_prompt_tokens"])
        for row in rows
        if is_value(row.get("behavior_judge_prompt_tokens"))
    )
    completion_tokens = sum(
        int(row["behavior_judge_completion_tokens"])
        for row in rows
        if is_value(row.get("behavior_judge_completion_tokens"))
    )
    attempts = [
        int(row["behavior_judge_attempts"])
        for row in rows
        if is_value(row.get("behavior_judge_attempts"))
    ]
    return {
        "row_count": len(rows),
        "evaluation_latency_ms_total": sum(latencies),
        "evaluation_latency_ms_mean": statistics.fmean(latencies) if latencies else None,
        "behavior_prompt_tokens_observed": prompt_tokens,
        "behavior_completion_tokens_observed": completion_tokens,
        "behavior_total_tokens_observed": prompt_tokens + completion_tokens,
        "behavior_attempts_total": sum(attempts),
        "behavior_retried_case_count": sum(attempt > 1 for attempt in attempts),
        "ragas_token_usage_available": False,
    }


def metric_comparison(
    baseline: dict[tuple[str, str], dict],
    alternative: dict[tuple[str, str], dict],
    metric: str,
) -> dict:
    """Compara las puntuaciones disponibles de dos jueces y sus diferencias por caso común."""
    baseline_values = [
        float(cast(float | int, row[metric]))
        for row in baseline.values()
        if is_value(row.get(metric))
    ]
    alternative_values = [
        float(cast(float | int, row[metric]))
        for row in alternative.values()
        if is_value(row.get(metric))
    ]
    paired = []
    for key in sorted(baseline):
        baseline_value = baseline[key].get(metric)
        alternative_value = alternative[key].get(metric)
        if not is_value(baseline_value) or not is_value(alternative_value):
            continue
        baseline_number = float(cast(float | int, baseline_value))
        alternative_number = float(cast(float | int, alternative_value))
        delta = alternative_number - baseline_number
        paired.append(
            {
                "retrieval_condition": key[0],
                "qid": key[1],
                "baseline": baseline_number,
                "alternative": alternative_number,
                "delta": delta,
            }
        )
    return {
        "baseline_n": len(baseline_values),
        "baseline_mean": statistics.fmean(baseline_values) if baseline_values else None,
        "alternative_n": len(alternative_values),
        "alternative_mean": (
            statistics.fmean(alternative_values) if alternative_values else None
        ),
        "common_n": len(paired),
        "alternative_wins": sum(row["delta"] > 0 for row in paired),
        "ties": sum(row["delta"] == 0 for row in paired),
        "baseline_wins": sum(row["delta"] < 0 for row in paired),
        "mean_delta_alternative_minus_baseline": (
            statistics.fmean(row["delta"] for row in paired) if paired else None
        ),
        "per_case": paired,
    }


def compare_judges(
    baseline_rows: list[dict],
    alternative_rows: list[dict],
    *,
    baseline_name: str,
    alternative_name: str,
) -> dict:
    """Valida la alineación entre jueces y compara sus métricas globales y por estrategia."""
    baseline = {
        (row["retrieval_condition"], row["qid"]): row for row in baseline_rows
    }
    alternative = {
        (row["retrieval_condition"], row["qid"]): row for row in alternative_rows
    }
    if len(baseline) != len(baseline_rows) or len(alternative) != len(alternative_rows):
        raise ValueError("duplicate condition and qid within judge results")
    if set(baseline) != set(alternative):
        raise ValueError("judge case sets differ")

    conditions = sorted({key[0] for key in baseline})
    by_condition = {}
    for condition in conditions:
        baseline_condition = {
            key: row for key, row in baseline.items() if key[0] == condition
        }
        alternative_condition = {
            key: row for key, row in alternative.items() if key[0] == condition
        }
        by_condition[condition] = {
            metric: metric_comparison(
                baseline_condition, alternative_condition, metric
            )
            for metric in METRICS
        }

    return {
        "baseline_judge": baseline_name,
        "alternative_judge": alternative_name,
        "aligned_case_count": len(baseline),
        "baseline_error_case_count": sum(
            bool(row.get("evaluation_errors")) for row in baseline.values()
        ),
        "alternative_error_case_count": sum(
            bool(row.get("evaluation_errors")) for row in alternative.values()
        ),
        "baseline_execution": execution_summary(baseline_rows),
        "alternative_execution": execution_summary(alternative_rows),
        "metrics": {
            metric: metric_comparison(baseline, alternative, metric)
            for metric in METRICS
        },
        "by_retrieval_condition": by_condition,
    }


def parse_args() -> argparse.Namespace:
    """Lee los archivos y nombres de los dos jueces y la ruta del informe."""
    parser = argparse.ArgumentParser(description="Compare two RAG judge executions")
    parser.add_argument("--baseline", type=Path, action="append", required=True)
    parser.add_argument("--alternative", type=Path, action="append", required=True)
    parser.add_argument("--baseline-name", required=True)
    parser.add_argument("--alternative-name", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    """Exporta la comparación de dos ejecuciones de evaluación RAG."""
    args = parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="compare_rag_judges")
    result = compare_judges(
        read_many_jsonl(args.baseline),
        read_many_jsonl(args.alternative),
        baseline_name=args.baseline_name,
        alternative_name=args.alternative_name,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
