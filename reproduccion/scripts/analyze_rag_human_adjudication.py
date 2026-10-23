from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any


HUMAN_METRICS = {
    "faithfulness": {
        "field": "faithfulness_assessment",
        "values": {"unsupported": 0.0, "partially_supported": 0.5, "supported": 1.0},
    },
    "factual_correctness": {
        "field": "factual_correctness_assessment",
        "values": {"incorrect": 0.0, "partially_correct": 0.5, "correct": 1.0},
    },
}
JUDGES = {
    "gemma3_4b": "Gemma 3 4B",
    "glm53flash_low": "GLM 5.3 Flash (low)",
}


def is_number(value: Any) -> bool:
    """Comprueba si el valor es numérico, excluyendo booleanos y NaN."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) and not (
        isinstance(value, float) and math.isnan(value)
    )


def _behavior_summary(cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Resume el acuerdo de conducta con el juicio humano y los valores ausentes."""
    available = [case for case in cases if is_number(case["judge"])]
    disagreements = [case for case in available if case["human"] != case["judge"]]
    exact = len(available) - len(disagreements)
    return {
        "human_applicable_n": len(cases),
        "judge_available_on_applicable_n": len(available),
        "missing_on_applicable_n": len(cases) - len(available),
        "exact_agreement_n": exact,
        "exact_agreement_rate": exact / len(available) if available else None,
        "mae_on_applicable": (
            statistics.fmean(abs(case["judge"] - case["human"]) for case in available)
            if available
            else None
        ),
        "disagreements": disagreements,
    }


def _metric_summary(
    rows: list[dict[str, Any]], judge_key: str, metric: str
) -> dict[str, Any]:
    """Compara una métrica del juez con etiquetas humanas separando los casos no aplicables."""
    contract = HUMAN_METRICS[metric]
    applicable = []
    not_applicable = []
    for row in rows:
        human_label = row["human_adjudication"][contract["field"]]
        judge_value = row.get(judge_key, {}).get(metric)
        case = {
            "qid": row["qid"],
            "retrieval_condition": row["retrieval_condition"],
            "human_label": human_label,
            "human": contract["values"].get(human_label),
            "judge": float(judge_value) if is_number(judge_value) else None,
        }
        if human_label == "not_applicable":
            not_applicable.append(case)
        elif human_label in contract["values"]:
            applicable.append(case)
        else:
            raise ValueError(f"invalid human label for {metric}: {human_label}")
    available = [case for case in applicable if case["judge"] is not None]
    return {
        "human_applicable_n": len(applicable),
        "judge_available_on_applicable_n": len(available),
        "missing_on_applicable_n": len(applicable) - len(available),
        "human_not_applicable_n": len(not_applicable),
        "judge_scored_not_applicable_n": sum(
            case["judge"] is not None for case in not_applicable
        ),
        "mae_on_applicable": (
            statistics.fmean(abs(case["judge"] - case["human"]) for case in available)
            if available
            else None
        ),
        "applicable_cases": applicable,
        "not_applicable_cases": not_applicable,
    }


def analyze_human_alignment(
    rows: list[dict[str, Any]], judge_key: str, judge_name: str
) -> dict[str, Any]:
    """Evalúa el acuerdo de un juez con los casos adjudicados por humanos."""
    behavior_cases = []
    by_expected: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        human = row.get("human_adjudication", {})
        if human.get("status") != "adjudicated":
            raise ValueError("all risk-queue rows must be human-adjudicated")
        case = {
            "qid": row["qid"],
            "retrieval_condition": row["retrieval_condition"],
            "expected_behavior": row["expected_behavior"],
            "human": float(human["behavior_score"]),
            "judge": (
                float(row.get(judge_key, {}).get("behavior_judge_score"))
                if is_number(row.get(judge_key, {}).get("behavior_judge_score"))
                else None
            ),
        }
        behavior_cases.append(case)
        by_expected[row["expected_behavior"]].append(case)

    behavior = _behavior_summary(behavior_cases)
    behavior["by_expected_behavior"] = {
        expected: _behavior_summary(cases) for expected, cases in sorted(by_expected.items())
    }
    return {
        "judge_key": judge_key,
        "judge_name": judge_name,
        "risk_queue_case_count": len(rows),
        "faithfulness": _metric_summary(rows, judge_key, "faithfulness"),
        "factual_correctness": _metric_summary(
            rows, judge_key, "factual_correctness"
        ),
        "behavior": behavior,
    }


def analyze_judges(
    rows: list[dict[str, Any]], judges: dict[str, str]
) -> dict[str, Any]:
    """Reúne el acuerdo y los errores de cada juez sobre la cola de riesgo."""
    all_adjudicated = all(
        row.get("human_adjudication", {}).get("status") == "adjudicated"
        for row in rows
    )
    results = {}
    for judge_key, judge_name in judges.items():
        result = analyze_human_alignment(rows, judge_key, judge_name)
        result["evaluation_error_case_count"] = sum(
            bool(row.get(judge_key, {}).get("evaluation_errors")) for row in rows
        )
        results[judge_key] = result
    return {
        "audit_scope": {
            "risk_queue_case_count": len(rows),
            "unique_qid_count": len({row["qid"] for row in rows}),
            "all_cases_adjudicated": all_adjudicated,
            "selection": "risk_directed_nonrandom_subset",
        },
        "judges": results,
    }


def generate_report(input_path: Path, output_path: Path) -> dict[str, Any]:
    """Lee la cola adjudicada y guarda el informe de acuerdo en JSON."""
    rows = [
        json.loads(line)
        for line in input_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    result = analyze_judges(rows, JUDGES)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return result


def parse_args() -> argparse.Namespace:
    """Lee las rutas de entrada y salida del análisis de adjudicación humana."""
    parser = argparse.ArgumentParser(
        description="Compare RAG judges against the human-adjudicated risk queue"
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    """Ejecuta el análisis de acuerdo humano con protección de las salidas."""
    args = parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="analyze_rag_human_adjudication")
    result = generate_report(args.input, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
