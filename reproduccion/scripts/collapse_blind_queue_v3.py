"""Colapsa la cola ciega del pool v3 por par base × chunk y prepara las hojas de gradación.

La cola que produce ``build_pool`` está en unidades de formulación × chunk, pero la
relevancia de un fragmento es una propiedad del par pregunta base × fragmento. Como la
rúbrica de equivalencia ya ratificó R1 y R2 —misma intención y misma conducta esperada—,
el grado es único para las dos formulaciones de una pareja y se juzga una sola vez.

Se colapsan así 630 unidades ciegas en 462 juicios, sin pérdida: cada unidad colapsada
cubre explícitamente los dos ``pool_id`` que la originan.

La hoja de revisión queda ciega: sin scores, sin método de origen y sin ranking. Se
muestran las dos redacciones de la pregunta de forma deliberada, para que el juez pueda
detectar un caso en que no sea posible asignar un único grado. Eso convertiría una
discrepancia de R2, que se registrará como conflicto en vez de promediarla.

Además se separa la cola de reutilización, cuyas unidades no piden un juicio nuevo sino
la confirmación de que el grado histórico del piloto sigue siendo válido para la pareja.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    """Carga los registros JSONL de las colas del pool."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    """Guarda las unidades agrupadas en JSONL conservando sus textos Unicode."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def collapse_blind(blind: list[dict]) -> list[dict]:
    """Una unidad por (base_qid, chunk_id), cubriendo las dos formulaciones."""
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in blind:
        groups[(row["base_qid"], row["chunk_id"])].append(row)

    out = []
    for (base_qid, chunk_id), rows in sorted(groups.items()):
        formulations = sorted({r["explicitness"] for r in rows})
        questions = {}
        for r in rows:
            questions[r["explicitness"]] = r["question"]
        assert len({r["question"] for r in rows}) == len(questions), "redacciones divergentes"
        out.append(
            dict(
                unit_id=f"{base_qid}::{chunk_id}",
                base_qid=base_qid,
                chunk_id=chunk_id,
                covered_pool_ids=sorted(r["pool_id"] for r in rows),
                covered_formulations=formulations,
                question_explicit=questions.get("explicit"),
                question_implicit=questions.get("implicit"),
                retrieval_text=rows[0]["retrieval_text"],
                reviews=[],
                human_decision=None,
                annotation_status="pending",
                grade_applies_to="both_formulations",
                equivalence_conflict=None,
            )
        )
    return out


def collapse_reuse(reuse: list[dict]) -> list[dict]:
    """Agrupa reutilizaciones por pregunta base y fragmento con propuesta de grado histórico máximo."""
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in reuse:
        groups[(row["base_qid"], row["chunk_id"])].append(row)

    out = []
    for (base_qid, chunk_id), rows in sorted(groups.items()):
        hist = rows[0]["historical_decisions"]
        out.append(
            dict(
                unit_id=f"{base_qid}::{chunk_id}",
                base_qid=base_qid,
                chunk_id=chunk_id,
                covered_pool_ids=sorted(r["pool_id"] for r in rows),
                historical_decisions=hist,
                proposed_grade=max(d["grade"] for d in hist),
                human_decision=None,
                annotation_status="pending_equivalence_confirmation",
            )
        )
    return out


def main() -> int:
    """Agrupa las colas ciega e histórica y verifica la cobertura exacta del pool técnico."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-dir", type=Path, required=True)
    args = ap.parse_args()
    run = args.run_dir

    blind = load_jsonl(run / "pools" / "blind_review_queue.jsonl")
    reuse = load_jsonl(run / "pools" / "pending_judgment_reuse.jsonl")

    blind_c = collapse_blind(blind)
    reuse_c = collapse_reuse(reuse)

    write_jsonl(run / "pools" / "blind_review_queue_collapsed.jsonl", blind_c)
    write_jsonl(run / "pools" / "reuse_confirmation_queue.jsonl", reuse_c)

    covered = {pid for r in blind_c for pid in r["covered_pool_ids"]}
    reuse_ids = {pid for r in reuse_c for pid in r["covered_pool_ids"]}
    assert covered | reuse_ids == {r["pool_id"] for r in load_jsonl(run / "pools" / "technical_pool.jsonl")}
    assert not (covered & reuse_ids)
    assert sum(len(r["covered_pool_ids"]) for r in blind_c) == len(blind)
    assert sum(len(r["covered_pool_ids"]) for r in reuse_c) == len(reuse)

    summary = dict(
        blind_units_declared=len(blind),
        blind_judgments_after_collapse=len(blind_c),
        blind_units_saved=len(blind) - len(blind_c),
        reuse_units_declared=len(reuse),
        reuse_confirmations=len(reuse_c),
        total_judgments_required=len(blind_c) + len(reuse_c),
        coverage_exact=True,
    )
    (run / "pools" / "collapse_report.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
