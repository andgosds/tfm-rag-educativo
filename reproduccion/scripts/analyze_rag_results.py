from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import defaultdict
from itertools import combinations
from pathlib import Path


QUALITY_METRICS = [
    "faithfulness",
    "factual_correctness",
    "reported_behavior_match",
    "citation_validity",
    "citation_presence",
    "behavior_judge_score",
]


def read_jsonl(path: Path) -> list[dict]:
    """Lee los registros JSONL omitiendo las líneas vacías."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def valid_values(rows: list[dict], metric: str) -> list[float]:
    """Extrae los valores de una métrica que no sean nulos ni NaN."""
    return [
        float(row[metric])
        for row in rows
        if row.get(metric) is not None
        and not (isinstance(row.get(metric), float) and math.isnan(row[metric]))
    ]


def paired_comparison(
    rows: list[dict], metric: str, baseline: str = "rrf", contender: str = "rrf_rerank"
) -> dict:
    """Compara dos estrategias por pregunta mediante diferencias y recuentos de victorias."""
    indexed = {(row["retrieval_condition"], row["qid"]): row for row in rows}
    qids = sorted({row["qid"] for row in rows})
    deltas = []
    wins = ties = losses = 0
    per_query = []
    for qid in qids:
        left = indexed.get((baseline, qid), {}).get(metric)
        right = indexed.get((contender, qid), {}).get(metric)
        if left is None or right is None:
            continue
        delta = float(right) - float(left)
        deltas.append(delta)
        if delta > 1e-12:
            wins += 1
        elif delta < -1e-12:
            losses += 1
        else:
            ties += 1
        per_query.append(
            {
                "qid": qid,
                "baseline_condition": baseline,
                "contender_condition": contender,
                "baseline_score": left,
                "contender_score": right,
                "delta_contender_minus_baseline": delta,
            }
        )
    result = {
        "metric": metric,
        "baseline": baseline,
        "contender": contender,
        "n": len(deltas),
        "contender_wins": wins,
        "rerank_wins": wins,
        "ties": ties,
        "baseline_wins": losses,
        "rrf_wins": losses,
        "mean_delta_contender_minus_baseline": (
            statistics.fmean(deltas) if deltas else None
        ),
        "mean_delta_rerank_minus_rrf": statistics.fmean(deltas) if deltas else None,
        "per_query": per_query,
    }
    return result


def all_pairwise_comparisons(rows: list[dict]) -> dict[str, dict]:
    """Calcula los contrastes de calidad para todos los pares de estrategias presentes."""
    conditions = sorted({row["retrieval_condition"] for row in rows})
    return {
        f"{baseline}__vs__{contender}": {
            metric: paired_comparison(rows, metric, baseline, contender)
            for metric in QUALITY_METRICS
        }
        for baseline, contender in combinations(conditions, 2)
    }


def summarize_by_behavior(rows: list[dict], metrics: list[str]) -> dict:
    """Resume las métricas por estrategia y conducta esperada."""
    grouped: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        grouped[row["retrieval_condition"]][row["expected_behavior"]].append(row)
    output = {}
    for condition, behaviors in sorted(grouped.items()):
        output[condition] = {}
        for behavior, behavior_rows in sorted(behaviors.items()):
            stats: dict[str, object] = {"row_count": len(behavior_rows)}
            for metric in metrics:
                values = valid_values(behavior_rows, metric)
                stats[f"{metric}_n"] = len(values)
                stats[f"{metric}_mean"] = statistics.fmean(values) if values else None
            output[condition][behavior] = stats
    return output


def summarize_overall(rows: list[dict]) -> dict:
    """Resume calidad, latencias, tokens y reintentos por estrategia."""
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["retrieval_condition"]].append(row)
    output = {}
    for condition, condition_rows in sorted(grouped.items()):
        stats: dict[str, object] = {"row_count": len(condition_rows)}
        for metric in QUALITY_METRICS:
            values = valid_values(condition_rows, metric)
            stats[f"{metric}_n"] = len(values)
            stats[f"{metric}_mean"] = statistics.fmean(values) if values else None
        for field in ("generation_latency_ms", "prompt_tokens", "completion_tokens"):
            values = valid_values(condition_rows, field)
            stats[f"{field}_n"] = len(values)
            stats[f"{field}_mean"] = statistics.fmean(values) if values else None
            stats[f"{field}_total"] = sum(values) if values else None
            if values:
                ordered = sorted(values)
                stats[f"{field}_p95"] = ordered[math.ceil(0.95 * len(ordered)) - 1]
            else:
                stats[f"{field}_p95"] = None
        stats["responses_requiring_retry"] = sum(
            int(row.get("generation_attempts", 1) > 1) for row in condition_rows
        )
        output[condition] = stats
    return output


def analyze(rows: list[dict]) -> dict:
    """Valida la unicidad de las celdas y reúne resúmenes y comparaciones emparejadas."""
    keys = [(row["retrieval_condition"], row["qid"]) for row in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate retrieval condition and qid")
    return {
        "row_count": len(rows),
        "overall": summarize_overall(rows),
        "by_expected_behavior": summarize_by_behavior(rows, QUALITY_METRICS),
        "paired": {
            metric: paired_comparison(rows, metric) for metric in QUALITY_METRICS
        },
        "all_pairwise": all_pairwise_comparisons(rows),
        "evaluation_error_count": sum(bool(row.get("evaluation_errors")) for row in rows),
    }


def analyze_applicable_content(rows: list[dict]) -> dict:
    """Diagnostic content subset by expected task, not generated behavior.

    Expected abstentions must be audited separately for substantive claims.
    Keeping answer tasks includes unsupported abstentions rather than rewarding
    a generator for avoiding an answer. This never rewrites frozen judge scores.
    """
    selected = [row for row in rows if row["expected_behavior"] != "abstain"]
    result = analyze(selected)
    result["selection"] = "expected_answer_or_grounded_correction"
    result["excluded_expected_abstention_count"] = len(rows) - len(selected)
    return result


def main() -> None:
    """Analiza el JSONL de resultados RAG y guarda el resumen protegido."""
    parser = argparse.ArgumentParser(description="Analyze paired RAG and RAGAS results")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="analyze_rag_results")
    result = analyze(read_jsonl(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
