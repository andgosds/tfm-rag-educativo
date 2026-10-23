"""Construye el fichero golden de generación para las 52 formulaciones de v3.

`run_rag_generation.py` espera por registro `answerability`, `expected_behavior` y
`reference`. Esos campos no conviven en un único fichero: `question_design_v3` trae los
tres pero solo para las 8 preguntas nuevas, y `golden_set_pilot_v1` trae `answerability`
y `gold_answer` sin `expected_behavior`. Este script los une sobre `formulations.jsonl`
y **deriva** la conducta esperada donde falta.

La derivación sigue la rúbrica del prompt de generación, que reconoce exactamente tres
conductas:

    answerable                                -> answer
    unanswerable con premisa falsa o refutada  -> grounded_correction
    unanswerable en cualquier otro caso        -> abstain

La marca de premisa se toma de `question_premise_audit_v3.jsonl`, nunca se infiere del
texto: es una decisión humana ya tomada y debe conservarse como tal.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: Path) -> list[dict]:
    """Carga los registros JSONL ignorando las líneas vacías."""
    with path.open(encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


def derive_behavior(answerability: str, premisa: dict | None) -> str:
    """Deriva la conducta esperada a partir de la respondibilidad y la marca de premisa."""
    if answerability == "answerable":
        return "answer"
    if premisa is not None:
        return "grounded_correction"
    return "abstain"


def main() -> int:
    """Une formulaciones y fuentes adjudicadas para construir el golden de generación v3."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--formulations", type=Path, default=ROOT / "outputs/local_runs/explicitness_v3/formulations.jsonl")
    ap.add_argument("--design", type=Path, default=ROOT / "data/golden/expansion_v3/question_design_v3.jsonl")
    ap.add_argument("--draft", type=Path, default=ROOT / "data/golden/expansion_v3/golden_set_v3_draft.jsonl")
    ap.add_argument("--golden-v1", type=Path, default=ROOT / "data/golden/golden_set_pilot_v1.jsonl")
    ap.add_argument("--premises", type=Path, default=ROOT / "data/golden/variants/question_premise_audit_v3.jsonl")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    form = read_jsonl(args.formulations)
    diseno = {r["qid"]: r for r in read_jsonl(args.design)}
    v1 = {r["qid"]: r for r in read_jsonl(args.golden_v1)}
    draft = {r["qid"]: r for r in read_jsonl(args.draft)}
    premisa = {r["base_qid"]: r for r in read_jsonl(args.premises)}

    filas = []
    for f in form:
        base = f["base_qid"]
        if base in diseno:
            src = diseno[base]
            answerability = src["answerability"]
            # `question_design_v3.reference_answer` está vacío en parte de las preguntas
            # respondibles; `golden_set_v3_draft.gold_answer` es la fuente adjudicada.
            reference = (draft.get(base) or {}).get("gold_answer") or src.get("reference_answer")
            categoria = src.get("unanswerable_category")
        elif base in v1:
            src = v1[base]
            answerability = src["answerability"]
            reference = src.get("gold_answer")
            categoria = src.get("unanswerable_category")
        else:
            raise KeyError(f"base_qid sin fuente: {base}")

        marca = premisa.get(base)
        filas.append({
            "qid": f["qid"],
            "base_qid": base,
            "explicitness": f["explicitness"],
            "question": f["question"],
            "answerability": answerability,
            "expected_behavior": derive_behavior(answerability, marca),
            "reference": reference,
            "unanswerable_category": categoria,
            "premise_mark": (marca or {}).get("premise_flag"),
            "procedencia": "question_design_v3" if base in diseno else "golden_set_pilot_v1",
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as fh:
        for r in filas:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    conteo = {}
    for r in filas:
        conteo[r["expected_behavior"]] = conteo.get(r["expected_behavior"], 0) + 1
    print(f"golden de generación: {len(filas)} registros → {args.output}")
    print(f"  conductas esperadas: {conteo}")
    print(f"  procedencia: v3={sum(1 for r in filas if r['procedencia'] == 'question_design_v3')}, "
          f"v1={sum(1 for r in filas if r['procedencia'] == 'golden_set_pilot_v1')}")
    sin_ref = sum(1 for r in filas if not r["reference"])
    if sin_ref:
        print(f"  ⚠ {sin_ref} registros sin referencia")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
