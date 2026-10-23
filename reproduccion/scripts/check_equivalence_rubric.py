#!/usr/bin/env python3
"""Comprueba el criterio R3 de la rúbrica de equivalencia (solape léxico diferenciado).

R3 verifica que cada pareja manipule realmente la explicitud del término técnico: el
término declarado debe aparecer en la versión explícita y **no** aparecer en la
implícita. La coincidencia se decide por lemas, de modo que un plural o una flexión
del término cuentan como presencia.

La comprobación es por término declarado y no por un ratio de solape global porque
este último queda confundido por la propia paráfrasis: al sustituir un término técnico
compacto por una descripción, la descripción reutiliza vocabulario general del
fragmento y el ratio puede subir aunque el término manipulado se haya retirado. El
ratio de solape de lemas de contenido se informa como dato descriptivo, no como
criterio.

La lematización es determinista: para cada token se toma el primer lemma nominal,
verbal, adjetivo o adverbial disponible, y en su defecto la propia forma.

Uso:
    python scripts/check_equivalence_rubric.py \
        --golden data/golden/golden_set_pilot_v1_1.jsonl \
        --chunks data/processed/chunks_v1.jsonl \
        --questions <jsonl con base_qid, explicitness, question> \
        --pairs config/equivalence_pairs_pilot_v2.jsonl \
        --output outputs/local_runs/<campaña>/equivalence_rubric_pairs.jsonl
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from lemminflect import getLemma

STOP = set(
    """a an and are as at be but by for from has have how if in into is it its of on or that the
    their this to was were what when where which who why with does do did than then these those can
    could may might must shall should will would about above after before between during over under
    up down out not no nor only own same so too very don now many much more most other some such only
    own same than then there here when where how all any both each few""".split()
)

TOKEN = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")


def lemmas(text: str) -> set[str]:
    """Obtiene los lemas de contenido con una prioridad gramatical fija y sin palabras vacías."""
    out: set[str] = set()
    for tok in TOKEN.findall(text.lower()):
        if tok in STOP or len(tok) < 2:
            continue
        lem = None
        for upos in ("NOUN", "VERB", "ADJ", "ADV"):
            res = getLemma(tok, upos=upos)
            if res:
                lem = res[0]
                break
        out.add(lem or tok)
    return out


def has_term(text: str, term: str) -> bool:
    """Cierto si todos los lemas de contenido del término aparecen en el texto."""
    need = lemmas(term)
    return bool(need) and need <= lemmas(text)


def load_jsonl(path: Path) -> list[dict]:
    """Lee los registros JSONL de preguntas, parejas o evidencia."""
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main() -> int:
    """Comprueba la retirada de términos técnicos en las variantes implícitas e informa el solape."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--golden", required=True, type=Path)
    ap.add_argument("--chunks", required=True, type=Path)
    ap.add_argument("--questions", required=True, type=Path)
    ap.add_argument("--pairs", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    golden = {r["qid"]: r for r in load_jsonl(args.golden)}
    chunks = {r["chunk_id"]: r for r in load_jsonl(args.chunks)}

    questions: dict[tuple[str, str], str] = {}
    for r in load_jsonl(args.questions):
        questions[(r["base_qid"], r["explicitness"])] = r["question"]

    def overlap(question: str, chunk_ids: list[str]) -> float:
        """Mide la fracción de lemas de la pregunta presentes en la evidencia indicada."""
        qn = lemmas(question)
        ct: set[str] = set()
        for cid in chunk_ids:
            ct |= lemmas(chunks[cid]["retrieval_text"])
        return len(qn & ct) / len(qn) if qn else 0.0


    def overlap_or_none(question: str, chunk_ids: list[str]) -> float | None:
        """Solape descriptivo; None cuando no hay canónicos que medir."""
        return overlap(question, chunk_ids) if chunk_ids else None

    pairs = {r["base_qid"]: r for r in load_jsonl(args.pairs)}

    base_ids = sorted({b for b, _ in questions})
    results = []
    for bq in base_ids:
        if (bq, "explicit") not in questions or (bq, "implicit") not in questions:
            continue
        canon = [e["chunk_id"] for e in golden.get(bq, {}).get("evidence", []) if e.get("is_canonical")]
        # R3 no depende de evidencia canónica y se evalúa siempre: una pregunta sin
        # evidencia, como una fuera de dominio, también tiene pareja que validar.
        # Solo el solape descriptivo requiere canónicos contra los que medirse.
        spec = pairs.get(bq, {})
        terms = spec.get("manipulated_terms", [])
        in_exp = [t for t in terms if has_term(questions[(bq, "explicit")], t)]
        in_imp = [t for t in terms if has_term(questions[(bq, "implicit")], t)]
        ok = bool(terms) and len(in_exp) == len(terms) and not in_imp
        o_exp = overlap_or_none(questions[(bq, "explicit")], canon)
        o_imp = overlap_or_none(questions[(bq, "implicit")], canon)
        results.append(
            {
                "base_qid": bq,
                "canonical": canon,
                "manipulated_terms": terms,
                "terms_in_explicit": in_exp,
                "terms_in_implicit": in_imp,
                "R3": "pass" if ok else "fail",
                "overlap_lemmas_explicit": None if o_exp is None else round(o_exp, 4),
                "overlap_lemmas_implicit": None if o_imp is None else round(o_imp, 4),
                "overlap_delta_implicit_minus_explicit": (
                    None if o_exp is None or o_imp is None else round(o_imp - o_exp, 4)
                ),
                "overlap_note": (
                    "no aplicable: la pareja carece de fragmento canónico"
                    if o_exp is None
                    else "dato descriptivo del solape léxico, no criterio de R3"
                ),
                "note": spec.get("note"),
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in results) + "\n"
    )

    npass = sum(1 for r in results if r["R3"] == "pass")
    print(f"{'pareja':12s} {'R3':6s} {'término(s) manipulado(s)':40s} {'solape expl→impl':>18s}")
    for r in results:
        terms = ", ".join(r["manipulated_terms"])
        if r["overlap_lemmas_explicit"] is None:
            shown = "sin canónicos"
        else:
            shown = f"{r['overlap_lemmas_explicit']:.3f}→{r['overlap_lemmas_implicit']:.3f}"
        print(f"{r['base_qid']:12s} {r['R3'].upper():6s} {terms[:40]:40s} {shown}")
        if r["terms_in_implicit"]:
            print(f"{'':18s} !! sigue presente en la implícita: {r['terms_in_implicit']}")
    print(f"\nR3: {npass}/{len(results)} parejas aprueban")
    print(f"artefacto: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
