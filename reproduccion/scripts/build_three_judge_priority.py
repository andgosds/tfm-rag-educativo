from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

HUMAN_FIELDS = (
    "human_grade",
    "human_canonical",
    "human_note",
    "human_reviewer_id",
    "human_status",
    "human_reviewed_at",
)
FORBIDDEN_FIELDS = {
    "source_system",
    "source_systems",
    "bm25_rank",
    "dense_rank",
    "bm25_score",
    "dense_score",
    "provenance",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Carga los registros JSONL del pool o de decisiones humanas."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_json(path: Path) -> list[dict[str, Any]]:
    """Carga una revisión de juez y exige que su contenido sea un array JSON."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise ValueError(f"{path} must contain a JSON array")
    return value


def _stable_sample(
    candidates: list[str], count: int, seed: str, stratum: str
) -> set[str]:
    """Selecciona una muestra estable por hashes de semilla, estrato e identificador."""
    ranked = sorted(
        candidates,
        key=lambda pool_id: hashlib.sha256(
            f"{seed}|{stratum}|{pool_id}".encode("utf-8")
        ).hexdigest(),
    )
    return set(ranked[: min(count, len(ranked))])


def select_priority_candidates(
    pool: list[dict[str, Any]],
    judges: list[list[dict[str, Any]]],
    existing_human: dict[str, dict[str, Any]],
    *,
    audit_per_stratum: int = 10,
    seed: str = "three-judge-risk-directed-v1",
) -> list[dict[str, Any]]:
    """Prioriza riesgos de tres jueces y añade auditorías de consensos de grado cero y uno."""
    if len(judges) != 3:
        raise ValueError("Exactly three judge review arrays are required")
    expected_ids = [row["pool_id"] for row in pool]
    judge_maps: list[dict[str, dict[str, Any]]] = []
    for index, reviews in enumerate(judges, start=1):
        if [row["pool_id"] for row in reviews] != expected_ids:
            raise ValueError(f"Judge {index} order does not match the blind pool")
        judge_maps.append({row["pool_id"]: row for row in reviews})

    reasons_by_id: dict[str, list[str]] = {pool_id: [] for pool_id in expected_ids}
    unanimous_candidates: dict[int, list[str]] = {0: [], 1: []}

    for pool_row in pool:
        pool_id = pool_row["pool_id"]
        reviews = [mapping[pool_id] for mapping in judge_maps]
        grades = [review["relevance_grade"] for review in reviews]
        if 2 in grades:
            reasons_by_id[pool_id].append("any_judge_grade_2")
        if set(grades) == {0, 1, 2}:
            reasons_by_id[pool_id].append("all_judges_disagree")
        if any(review.get("answerability_conflict", False) for review in reviews):
            reasons_by_id[pool_id].append("answerability_conflict")
        if pool_id in existing_human and existing_human[pool_id].get("human_grade") in {
            0,
            1,
            2,
        }:
            reasons_by_id[pool_id].append("existing_human_decision")
        if len(set(grades)) == 1 and grades[0] in {0, 1}:
            unanimous_candidates[grades[0]].append(pool_id)

    # La auditoría de consensos añade casos que no estaban seleccionados por riesgo.
    already_selected = {
        pool_id for pool_id, reasons in reasons_by_id.items() if reasons
    }
    for grade in (0, 1):
        eligible = [
            pool_id
            for pool_id in unanimous_candidates[grade]
            if pool_id not in already_selected
        ]
        sampled = _stable_sample(
            eligible, audit_per_stratum, seed, f"unanimous-grade-{grade}"
        )
        for pool_id in sampled:
            reasons_by_id[pool_id].append(f"audit_unanimous_grade_{grade}")

    selected: list[dict[str, Any]] = []
    for pool_row in pool:
        pool_id = pool_row["pool_id"]
        reasons = reasons_by_id[pool_id]
        if not reasons:
            continue
        row = {
            key: value
            for key, value in pool_row.items()
            if key not in FORBIDDEN_FIELDS
        }
        previous = existing_human.get(pool_id, {})
        for field in HUMAN_FIELDS:
            if field in previous:
                row[field] = previous[field]
        row.setdefault("human_grade", None)
        row.setdefault("human_canonical", None)
        row.setdefault("human_note", "")
        row["selection_protocol"] = "three_judge_risk_directed_v1"
        row["selection_reasons"] = reasons
        reviews = [mapping[pool_id] for mapping in judge_maps]
        for index, review in enumerate(reviews, start=1):
            row[f"judge{index}_grade"] = review["relevance_grade"]
            row[f"judge{index}_canonical"] = review["canonical_candidate"]
            row[f"judge{index}_answerability_conflict"] = review.get(
                "answerability_conflict", False
            )
        row["answerability_conflict"] = any(
            review.get("answerability_conflict", False) for review in reviews
        )
        selected.append(row)

    return selected


def atomic_write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    """Guarda la selección en JSONL mediante un temporal sincronizado y reemplazo atómico."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def parse_args() -> argparse.Namespace:
    """Lee las fuentes de los tres jueces y los parámetros de auditoría estratificada."""
    root = Path(__file__).resolve().parents[1]
    golden = root / "data/golden"
    parser = argparse.ArgumentParser(
        description="Build a risk-directed human review set from three blind judges"
    )
    parser.add_argument(
        "--pool", type=Path, default=golden / "pool_bm25_dense_blind_v1_22q.jsonl"
    )
    parser.add_argument(
        "--judge1",
        type=Path,
        default=golden / "reviews/pool_judge1_reviews_2026-08-17.json",
    )
    parser.add_argument(
        "--judge2",
        type=Path,
        default=golden / "reviews/pool_judge2_reviews_2026-08-17.json",
    )
    parser.add_argument(
        "--judge3",
        type=Path,
        default=golden / "reviews/pool_judge3_reviews_2026-08-24.json",
    )
    parser.add_argument(
        "--existing-human",
        type=Path,
        default=golden / "pool_human_priority_v1_22q.jsonl",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=golden / "pool_human_priority_three_judge_v1_22q.jsonl",
    )
    parser.add_argument("--audit-per-stratum", type=int, default=10)
    parser.add_argument("--seed", default="three-judge-risk-directed-v1")
    return parser.parse_args()


def main() -> None:
    """Genera la selección de revisión humana y muestra sus motivos y pendientes."""
    args = parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="build_three_judge_priority")
    pool = load_jsonl(args.pool)
    judges = [load_json(args.judge1), load_json(args.judge2), load_json(args.judge3)]
    existing_rows = load_jsonl(args.existing_human)
    existing_human = {row["pool_id"]: row for row in existing_rows}
    selected = select_priority_candidates(
        pool,
        judges,
        existing_human,
        audit_per_stratum=args.audit_per_stratum,
        seed=args.seed,
    )
    atomic_write_jsonl(args.output, selected)
    reason_counts = Counter(
        reason for row in selected for reason in row["selection_reasons"]
    )
    reviewed = sum(row.get("human_grade") in {0, 1, 2} for row in selected)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "candidate_count": len(selected),
                "already_reviewed": reviewed,
                "pending": len(selected) - reviewed,
                "reason_counts": dict(sorted(reason_counts.items())),
                "audit_per_stratum": args.audit_per_stratum,
                "seed": args.seed,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
