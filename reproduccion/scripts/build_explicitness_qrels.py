"""Constructor de qrels v2 para la campaña de explicitud.

Fusiona decisiones humanas de reutilización y revisión asistente delegada en un qrels definitivo por
formulación (qid de variante) sin tocar los qrels históricos de v1:

1. Libro de reutilizaciones (data/golden/variants/explicitness_reuse_adjudications_v1.jsonl):
   98 unidades cuyo grado se hereda de la adjudicación histórica del piloto
   (golden set v1.1 y, en su defecto, qrels pooled v1 22q), con las dos
   excepciones degradadas a grado 1 en q-v1-002 (opción A del lote 3).
2. Cola ciega (outputs/local_runs/blind_review_queue_work.jsonl):
   122 unidades decididas en revisión ciega vía explicitness_blind_review_app.

Cobertura obligatoria: la unión de ambas fuentes debe ser exactamente el pool
técnico congelado (220 unidades). Los grados 0 no generan fila de qrel; se
auditan en el informe. Las filas de qrel usan qid de variante
(q-v1-XXX__explicit / __implicit) para que las métricas emparejadas comparen
formulaciones sobre el mismo espacio de chunks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

# Unidades del lote 3 degradadas a grado 1 (opción A, confirmada por el usuario
# el 2026-09-21): conservan rol de contexto, no de respuesta.
DEGRADED_POOL_IDS = {
    "q-v1-002__implicit::openstax_intro_stats_2e:9.4:chunk-006",
    "q-v1-002__implicit::openstax_principles_ds:4.2:chunk-007",
}


def _sha256(path: Path) -> str:
    """Calcula el SHA-256 del archivo para registrar su procedencia."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _atomic_write(path: Path, text: str) -> None:
    """Escribe el texto en un temporal y lo sustituye en la ruta de destino."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Carga las líneas JSON no vacías del archivo de anotaciones."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_historic_grades(
    golden_path: Path, pooled_qrels_path: Path
) -> tuple[dict[tuple[str, str], int], dict[tuple[str, str], bool]]:
    """Grados históricos del piloto por (base_qid, chunk_id) y canonicidad del golden set."""
    grades: dict[tuple[str, str], int] = {}
    canonical: dict[tuple[str, str], bool] = {}
    for row in _load_jsonl(golden_path):
        for ev in row.get("evidence", []):
            key = (row["qid"], ev["chunk_id"])
            grades[key] = int(ev["relevance_grade"])
            canonical[key] = bool(ev.get("is_canonical", False))
    for line in pooled_qrels_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        qid, _, chunk_id, raw = line.split("\t")
        grades.setdefault((qid, chunk_id), int(raw))
    return grades, canonical


def collect_decisions(
    reuse_book_path: Path,
    blind_work_path: Path,
    historic_grades: dict[tuple[str, str], int],
    historic_canonical: dict[tuple[str, str], bool],
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    """Devuelve {pool_id: unidad decidida} y la lista de excepciones aplicadas."""
    book = json.loads(reuse_book_path.read_text(encoding="utf-8"))
    reuse_units = book["adjudications"] + book["grade_1_2_proposals"]
    if not reuse_units:
        raise ValueError(f"reuse book has no units: {reuse_book_path}")
    decisions: dict[str, dict[str, Any]] = {}
    notes: list[dict[str, Any]] = []

    for unit in reuse_units:
        pool_id = unit["pool_id"]
        key = (unit["base_qid"], unit["chunk_id"])
        if pool_id in DEGRADED_POOL_IDS:
            grade = 1
            notes.append({"pool_id": pool_id, "rule": "lote3_option_a_downgrade", "final_grade": 1})
        elif key in historic_grades:
            grade = historic_grades[key]
        elif unit.get("human_decision", {}).get("decision") == "confirm_grade_0":
            grade = 0
        else:
            raise ValueError(f"reuse unit without historic grade: {pool_id}")
        decisions[pool_id] = {
            "qid": unit["qid"],
            "base_qid": unit["base_qid"],
            "chunk_id": unit["chunk_id"],
            "explicitness": unit["explicitness"],
            "grade": grade,
            # La canonicidad es un estatus del golden set original: nunca se
            # crea en reutilización ni en revisión ciega.
            "canonical": False,
            "source": "reuse_book",
            "reviewer": unit.get("human_decision", {}).get("reviewer", "unknown"),
            "decision_provenance": unit.get("decision_provenance", {"adjudication_mode": "human_confirmation"}),
        }

    for row in _load_jsonl(blind_work_path):
        pool_id = row["pool_id"]
        if pool_id in decisions:
            raise ValueError(f"duplicate pool_id across sources: {pool_id}")
        decision = row.get("human_decision") or {}
        if decision.get("grade") not in (0, 1, 2):
            raise ValueError(f"blind unit without final grade: {pool_id}")
        decisions[pool_id] = {
            "qid": row["qid"],
            "base_qid": row["base_qid"],
            "chunk_id": row["chunk_id"],
            "explicitness": row["explicitness"],
            "grade": decision["grade"],
            "canonical": False,
            "source": "blind_review",
            "reviewer": decision.get("reviewer", "unknown"),
            "decision_provenance": row.get("decision_provenance", {"adjudication_mode": "unverified"}),
        }
    return decisions, notes


def build_explicitness_qrels(
    *,
    reuse_book_path: Path,
    blind_work_path: Path,
    technical_pool_path: Path,
    golden_path: Path,
    pooled_qrels_path: Path,
    output_qrels_path: Path,
    provenance_path: Path,
    report_path: Path,
) -> dict[str, Any]:
    """Fusiona las decisiones con cobertura exacta del pool y exporta qrels y procedencia."""
    historic_grades, historic_canonical = load_historic_grades(golden_path, pooled_qrels_path)
    decisions, notes = collect_decisions(
        reuse_book_path, blind_work_path, historic_grades, historic_canonical
    )

    pool_rows = _load_jsonl(technical_pool_path)
    pool_ids = {row["pool_id"] for row in pool_rows}
    decided_ids = set(decisions)
    if decided_ids != pool_ids:
        raise ValueError(
            "coverage mismatch: "
            f"undecided={sorted(pool_ids - decided_ids)[:5]} "
            f"outside_pool={sorted(decided_ids - pool_ids)[:5]}"
        )

    # Sin grados duplicados dentro de una variante para el mismo chunk.
    seen: dict[tuple[str, str], str] = {}
    for pool_id, unit in decisions.items():
        key = (unit["qid"], unit["chunk_id"])
        if key in seen:
            raise ValueError(f"duplicate (qid, chunk): {key}")
        seen[key] = pool_id

    positive = {
        pool_id: unit for pool_id, unit in decisions.items() if unit["grade"] in (1, 2)
    }
    audited_grade_0 = sum(1 for unit in decisions.values() if unit["grade"] == 0)

    ordered = sorted(positive.items(), key=lambda item: (item[1]["qid"], item[1]["chunk_id"]))
    qrels_text = "".join(
        f"{unit['qid']}\t0\t{unit['chunk_id']}\t{unit['grade']}\n" for _, unit in ordered
    )
    provenance_rows = [
        {
            "pool_id": pool_id,
            "qid": unit["qid"],
            "base_qid": unit["base_qid"],
            "chunk_id": unit["chunk_id"],
            "explicitness": unit["explicitness"],
            "grade": unit["grade"],
            "canonical": unit["canonical"],
            "decision_source": unit["source"],
            "reviewer": unit["reviewer"],
            "decision_provenance": unit["decision_provenance"],
        }
        for pool_id, unit in ordered
    ]
    provenance_text = "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in provenance_rows
    )
    _atomic_write(output_qrels_path, qrels_text)
    _atomic_write(provenance_path, provenance_text)

    by_qid: dict[str, Counter[int]] = defaultdict(Counter)
    for unit in positive.values():
        by_qid[unit["qid"]][unit["grade"]] += 1
    grade_counts = Counter(unit["grade"] for unit in decisions.values())
    report: dict[str, Any] = {
        "protocol_id": "explicitness_qrels_v2_from_adjudication_campaign_v1",
        "decided_units_total": len(decisions),
        "decided_units_by_source": {
            "reuse_book": sum(1 for u in decisions.values() if u["source"] == "reuse_book"),
            "blind_review": sum(1 for u in decisions.values() if u["source"] == "blind_review"),
        },
        "decided_units_by_grade": {str(g): grade_counts.get(g, 0) for g in (0, 1, 2)},
        "audited_grade_0_count": audited_grade_0,
        "qrel_rows_total": len(positive),
        "qrel_rows_by_qid": {
            qid: {"1": c.get(1, 0), "2": c.get(2, 0)} for qid, c in sorted(by_qid.items())
        },
        "variant_qids": sorted(by_qid),
        "grade_2_total": sum(c.get(2, 0) for c in by_qid.values()),
        "binary_relevance_grade": 2,
        "ndcg_relevance_grades": [0, 1, 2],
        "lot3_downgrades_applied": notes,
        "input_paths": {
            "reuse_book": str(reuse_book_path),
            "blind_work": str(blind_work_path),
            "technical_pool": str(technical_pool_path),
            "golden_set": str(golden_path),
            "pooled_qrels_v1_22q": str(pooled_qrels_path),
        },
        "input_sha256": {
            "reuse_book": _sha256(reuse_book_path),
            "blind_work": _sha256(blind_work_path),
            "technical_pool": _sha256(technical_pool_path),
            "golden_set": _sha256(golden_path),
            "pooled_qrels_v1_22q": _sha256(pooled_qrels_path),
        },
        "output_qrels_path": str(output_qrels_path),
        "provenance_path": str(provenance_path),
        "output_sha256": _sha256(output_qrels_path),
        "provenance_sha256": _sha256(provenance_path),
    }
    _atomic_write(report_path, json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return report


def build_parser(root: Path) -> argparse.ArgumentParser:
    """Define las rutas de decisiones, fuentes históricas y salidas de los qrels de explicitud."""
    parser = argparse.ArgumentParser(description="Build explicitness v2 qrels from human adjudications")
    parser.add_argument("--reuse-book", type=Path, default=root / "data/golden/variants/explicitness_reuse_adjudications_v1.jsonl")
    parser.add_argument("--blind-work", type=Path, default=root / "outputs/local_runs/blind_review_queue_work.jsonl")
    parser.add_argument("--technical-pool", type=Path, default=root / "outputs/explicitness_v2/pools/technical_pool.jsonl")
    parser.add_argument("--golden", type=Path, default=root / "data/golden/golden_set_pilot_v1_1.jsonl")
    parser.add_argument("--pooled-qrels", type=Path, default=root / "data/golden/qrels_golden_set_pooled_v1_22q.tsv")
    parser.add_argument("--output", type=Path, default=root / "data/golden/variants/qrels_explicitness_v2.tsv")
    parser.add_argument("--provenance", type=Path, default=root / "data/golden/variants/qrels_explicitness_v2_provenance.jsonl")
    parser.add_argument("--report", type=Path, default=root / "data/golden/variants/qrels_explicitness_v2_report.json")
    return parser


def main() -> int:
    """Construye los qrels de explicitud y muestra el informe de cobertura."""
    root = Path(__file__).resolve().parents[1]
    args = build_parser(root).parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="build_explicitness_qrels")
    report = build_explicitness_qrels(
        reuse_book_path=args.reuse_book,
        blind_work_path=args.blind_work,
        technical_pool_path=args.technical_pool,
        golden_path=args.golden,
        pooled_qrels_path=args.pooled_qrels,
        output_qrels_path=args.output,
        provenance_path=args.provenance,
        report_path=args.report,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
