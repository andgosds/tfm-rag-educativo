"""Construye los lotes de gradación de qrels v3 para los dos jueces.

Reparte los 578 pares base × chunk en lotes de 10 unidades, cada uno como un fichero
de consulta independiente para ``hermes chat --oneshot --query-file``. Cada juez recibe
**los mismos lotes con el mismo texto**, de modo que la discrepancia A−B sea directamente
el subconjunto de riesgo y no un artefacto de haber preparado el material de otra forma.

Incluye también las unidades de reutilización, no solo las ciegas. El pre-registro fija
que la gradación se rehace íntegra para que el conjunto sea homogéneo, y que las
adjudicaciones humanas del piloto prevalecen después, al consolidar.

La copia que recibe el juez es ciega: sin scores, sin método de origen y sin ranking.
Las dos redacciones de la pregunta se muestran a la vez, para que el juez pueda señalar
un caso en que no quepa un único grado —conflicto de equivalencia— en vez de promediar.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

BATCH_SIZE = 10
PROMPT_VERSION = "qrels_review_prompt_v3.md"
ROOT = Path(__file__).resolve().parents[1]

HEADER = """{instruction}

---

# Unidades por gradar

Devuelve **una línea JSON por unidad**, en el mismo orden, sin texto adicional y sin
marcas de código. Usa el `unit_id` tal cual:

{{"unit_id": "...", "grade": 0|1|2, "confidence": "low"|"medium"|"high", "equivalence_conflict": false, "rationale": "una frase"}}

"""


def load_jsonl(path: Path) -> list[dict]:
    """Carga los registros JSONL de las colas y fuentes de gradación."""
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> int:
    """Genera lotes comunes para ambos jueces con las dos formulaciones de cada pregunta."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--chunks", type=Path, required=True)
    ap.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    args = ap.parse_args()

    run = args.run_dir
    out_dir = run / "judging" / "batches"
    out_dir.mkdir(parents=True, exist_ok=True)

    instruction = (Path(__file__).resolve().parents[1] / "config" / PROMPT_VERSION).read_text(encoding="utf-8")
    chunks = {r["chunk_id"]: r for r in load_jsonl(args.chunks)}

    blind = load_jsonl(run / "pools" / "blind_review_queue_collapsed.jsonl")
    reuse = load_jsonl(run / "pools" / "reuse_confirmation_queue.jsonl")

    units = []
    for r in blind:
        units.append(dict(
            unit_id=r["unit_id"], base_qid=r["base_qid"], chunk_id=r["chunk_id"],
            question_explicit=r.get("question_explicit"), question_implicit=r.get("question_implicit"),
            retrieval_text=r["retrieval_text"], origin="blind",
        ))
    for r in reuse:
        c = chunks[r["chunk_id"]]
        units.append(dict(
            unit_id=r["unit_id"], base_qid=r["base_qid"], chunk_id=r["chunk_id"],
            question_explicit=None, question_implicit=None,
            retrieval_text=c["retrieval_text"], origin="reuse",
        ))
    units.sort(key=lambda u: (u["base_qid"], u["chunk_id"]))

    # Las dos redacciones se toman SIEMPRE del fichero de parejas. Un mismo par base ×
    # chunk puede haber sido recuperado solo por una de las dos formulaciones, en cuyo
    # caso la otra redacción no viene en la cola; el grado es único igualmente, porque
    # R1 y R2 garantizan la equivalencia.
    pairs = {r["base_qid"]: r for r in load_jsonl(
        ROOT / "data" / "golden" / "variants" / "explicitness_pairs_v3_all26.jsonl")}
    for u in units:
        p = pairs[u["base_qid"]]
        for key, want in (("question_explicit", p["explicit_question"]),
                          ("question_implicit", p["implicit_question"])):
            if u[key] is not None and u[key] != want:
                raise ValueError(f"{u['unit_id']}: la redacción de la cola difiere de la del par")
            u[key] = want

    assert all(u["question_explicit"] and u["question_implicit"] for u in units)
    assert len({u["unit_id"] for u in units}) == len(units)

    manifest = []
    for i in range(0, len(units), args.batch_size):
        batch = units[i : i + args.batch_size]
        bid = f"batch-{i // args.batch_size + 1:03d}"
        body = HEADER.format(instruction=instruction.strip())
        for n, u in enumerate(batch, 1):
            body += (
                f"\n## Unidad {n} — `{u['unit_id']}`\n\n"
                f"### Pregunta explícita\n{u['question_explicit']}\n\n"
                f"### Pregunta implícita\n{u['question_implicit']}\n\n"
                f"### Fragmento candidato\n{u['retrieval_text']}\n"
            )
        path = out_dir / f"{bid}.md"
        path.write_text(body, encoding="utf-8")
        manifest.append(dict(batch_id=bid, file=str(path.relative_to(run)),
                             units=[u["unit_id"] for u in batch],
                             n_units=len(batch), n_chars=len(body)))

    (run / "judging" / "manifest.json").write_text(
        json.dumps(dict(
            batch_size=args.batch_size, n_units=len(units), n_batches=len(manifest),
            prompt_version=PROMPT_VERSION, batches=manifest,
        ), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"unidades: {len(units)}  (ciegas {len(blind)} + reutilización {len(reuse)})")
    print(f"lotes de {args.batch_size}: {len(manifest)}  -> {run / 'judging' / 'batches'}")
    sizes = [m["n_chars"] for m in manifest]
    print(f"tamaño de lote en caracteres: min {min(sizes)} / max {max(sizes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
