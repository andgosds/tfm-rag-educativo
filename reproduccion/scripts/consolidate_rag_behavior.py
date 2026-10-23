from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any


def _index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    """Indexa las puntuaciones por estrategia y pregunta sin admitir duplicados."""
    indexed = {(row["retrieval_condition"], row["qid"]): row for row in rows}
    if len(indexed) != len(rows):
        raise ValueError("duplicate retrieval condition and qid")
    return indexed


def _pairwise_behavior(
    cases: list[dict[str, Any]], baseline: str, contender: str
) -> dict[str, Any]:
    """Contrasta las puntuaciones finales de conducta de dos estrategias en preguntas comunes."""
    by_key = {
        (case["retrieval_condition"], case["qid"]): case for case in cases
    }
    qids = sorted({case["qid"] for case in cases})
    deltas = []
    for qid in qids:
        left = by_key.get((baseline, qid))
        right = by_key.get((contender, qid))
        if left and right:
            deltas.append(
                right["final_behavior_score"] - left["final_behavior_score"]
            )
    return {
        "baseline": baseline,
        "contender": contender,
        "common_qid_count": len(deltas),
        "contender_wins": sum(delta > 0 for delta in deltas),
        "ties": sum(delta == 0 for delta in deltas),
        "baseline_wins": sum(delta < 0 for delta in deltas),
        "mean_delta_contender_minus_baseline": (
            statistics.fmean(deltas) if deltas else None
        ),
    }


def consolidate_behavior(
    full_rows: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    *,
    primary_judge: str,
) -> dict[str, Any]:
    """Sustituye las puntuaciones auditadas por el juicio humano y conserva el juez en las demás."""
    full = _index(full_rows)
    audit = _index(audit_rows)
    if not set(audit).issubset(full):
        raise ValueError("audited cases must be a subset of full judge results")

    cases = []
    for key, row in sorted(full.items()):
        automatic = float(row["behavior_judge_score"])
        if key in audit:
            human = audit[key].get("human_adjudication", {})
            if human.get("status") != "adjudicated":
                raise ValueError("all audit rows must be adjudicated")
            final = float(human["behavior_score"])
            source = "human_adjudication"
        else:
            final = automatic
            source = primary_judge
        cases.append(
            {
                "retrieval_condition": key[0],
                "qid": key[1],
                "automatic_behavior_score": automatic,
                "final_behavior_score": final,
                "final_behavior_source": source,
            }
        )

    conditions = sorted({case["retrieval_condition"] for case in cases})
    by_condition = {}
    for condition in conditions:
        selected = [case for case in cases if case["retrieval_condition"] == condition]
        by_condition[condition] = {
            "n": len(selected),
            "automatic_mean": statistics.fmean(
                case["automatic_behavior_score"] for case in selected
            ),
            "final_mean": statistics.fmean(
                case["final_behavior_score"] for case in selected
            ),
            "human_override_n": sum(
                case["final_behavior_source"] == "human_adjudication"
                for case in selected
            ),
        }

    all_pairwise = {
        f"{baseline}__vs__{contender}": _pairwise_behavior(
            cases, baseline, contender
        )
        for baseline, contender in combinations(conditions, 2)
    }
    legacy_pair = all_pairwise.get("rrf__vs__rrf_rerank")

    return {
        "primary_judge_for_unaudited_cases": primary_judge,
        "case_count": len(cases),
        "source_counts": dict(
            Counter(case["final_behavior_source"] for case in cases)
        ),
        "by_retrieval_condition": by_condition,
        "paired": {
            "common_qid_count": legacy_pair["common_qid_count"] if legacy_pair else 0,
            "rerank_wins": legacy_pair["contender_wins"] if legacy_pair else 0,
            "ties": legacy_pair["ties"] if legacy_pair else 0,
            "rrf_wins": legacy_pair["baseline_wins"] if legacy_pair else 0,
            "mean_delta_rerank_minus_rrf": (
                legacy_pair["mean_delta_contender_minus_baseline"]
                if legacy_pair
                else None
            ),
        },
        "all_pairwise": all_pairwise,
        "per_case": cases,
    }


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Carga las líneas JSON no vacías de puntuaciones o auditorías."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def generate_consolidated_report(
    full_paths: list[Path],
    audit_path: Path,
    output_path: Path,
    *,
    primary_judge: str,
) -> dict[str, Any]:
    """Lee puntuaciones y auditoría y guarda el informe de conducta consolidada."""
    full_rows = [row for path in full_paths for row in _read_jsonl(path)]
    result = consolidate_behavior(
        full_rows, _read_jsonl(audit_path), primary_judge=primary_judge
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return result


def parse_args() -> argparse.Namespace:
    """Lee las puntuaciones, la auditoría y el juez que se conserva en casos no revisados."""
    parser = argparse.ArgumentParser(
        description="Consolidate human and primary-judge RAG behavior scores"
    )
    parser.add_argument("--input", type=Path, action="append", required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--primary-judge", default="glm53flash_low")
    return parser.parse_args()


def main() -> None:
    """Exporta el informe de conducta con adjudicaciones humanas y juez principal."""
    args = parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="consolidate_rag_behavior")
    result = generate_consolidated_report(
        args.input,
        args.audit,
        args.output,
        primary_judge=args.primary_judge,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
