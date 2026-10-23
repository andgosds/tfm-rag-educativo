"""Prepara las discrepancias A−B para el arbitraje ciego con `gpt-6-astra`.

Presenta cada discrepancia con los dos veredictos **anonimizados y en orden aleatorizado por
unidad**, de modo que el árbitro no pueda inferir cuál procede de cuál modelo ni anclarse en la
posición de una opción. El árbitro emite su propio grado, no una elección entre dos.

La correspondencia etiqueta ↔ modelo se guarda en un fichero aparte (`blind_key.jsonl`) que el
árbrito nunca ve. El aleatorizado es determinista —semilla fija sobre el ``unit_id``—, de modo que
la preparación sea reproducible aunque sea ciega para el juez.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

PROMPT_VERSION = "arbitration_prompt_v3.md"
JUDGE_LABELS = ("Opción alfa", "Opción beta")

HEADER = """A continuación tienes casos en los que **dos evaluadores independientes han discrepado** sobre
el grado de relevancia de un fragmento candidato respecto de una pregunta.

Tu tarea: emitir **tu propio grado**, según la misma escala, y decidir cuál de los dos veredictos
presentados consideras correcto. No sabes de qué evaluador procede cada uno, ni importa: juzga
únicamente por el contenido.

## Escala

- **0**: no contiene nada que responda a la pregunta.
- **1**: toca el tema o aporta algún elemento, pero no permite responderla.
- **2**: permite responder a la pregunta sin necesidad de información externa.

## Formato de salida

Devuelve **una línea JSON por caso**, en el mismo orden, sin texto adicional y sin marcas de código:

{{"unit_id": "...", "grade": 0|1|2, "side": "alfa"|"beta", "confidence": "low"|"medium"|"high", "rationale": "una frase"}}

`side` indica cuál de los dos veredictos presentados consideras correcto.

---

# Casos

"""


def main() -> int:
    """Prepara lotes de discrepancias anonimizadas y guarda por separado la clave ciega."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--chunks", type=Path, required=True)
    ap.add_argument("--queue", default="judging/risk_queue_v3_ordered.jsonl")
    ap.add_argument("--out-subdir", default="judging/arbitration")
    ap.add_argument("--batch-size", type=int, default=10)
    args = ap.parse_args()

    run = args.run_dir
    out_dir = run / args.out_subdir / "batches"
    out_dir.mkdir(parents=True, exist_ok=True)

    chunks = {r["chunk_id"]: r for r in
              (json.loads(l) for l in args.chunks.read_text(encoding="utf-8").splitlines() if l.strip())}
    pairs = {r["base_qid"]: r for r in
             (json.loads(l) for l in (Path(__file__).resolve().parents[1] / "data" / "golden" /
                                      "variants" / "explicitness_pairs_v3_all26.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}

    rows = [json.loads(l) for l in (run / args.queue).read_text(encoding="utf-8").splitlines() if l.strip()]
    disc = [r for r in rows if "discrepancia" in r["risk_reasons"]]

    key, manifest = [], []
    for i in range(0, len(disc), args.batch_size):
        batch = disc[i : i + args.batch_size]
        bid = f"arb-{i // args.batch_size + 1:03d}"
        body = HEADER
        for n, r in enumerate(batch, 1):
            u = r["unit_id"]
            qid, chunk_id = u.split("::", 1)
            # orden aleatorizado determinista por unidad
            rng = random.Random(int(hashlib.sha256(u.encode()).hexdigest(), 16))
            flip = rng.random() < 0.5
            va, vb = r["verdict_judge_a"], r["verdict_judge_b"]
            first, second = (vb, va) if flip else (va, vb)
            key.append(dict(unit_id=u, flipped=flip))

            body += (
                f"\n## Caso {n} — `{u}`\n\n"
                f"### Pregunta\n{pairs[qid]['explicit_question']}\n\n"
                f"### Fragmento candidato\n{chunks[chunk_id]['retrieval_text']}\n\n"
                f"### Veredicto {JUDGE_LABELS[0]} — grado {first['grade']} ({first['confidence']})\n{first['rationale']}\n\n"
                f"### Veredicto {JUDGE_LABELS[1]} — grado {second['grade']} ({second['confidence']})\n{second['rationale']}\n"
            )
        (out_dir / f"{bid}.md").write_text(body, encoding="utf-8")
        manifest.append(dict(batch_id=bid, units=[r["unit_id"] for r in batch], n_chars=len(body)))

    (run / args.out_subdir / "blind_key.jsonl").write_text(
        "\n".join(json.dumps(dict(unit_id=k["unit_id"],
                                  alfa=("mimo-v2.6-pro" if k["flipped"] else "gpt-6-sol"),
                                  beta=("gpt-6-sol" if k["flipped"] else "mimo-v2.6-pro"),
                                  flipped=k["flipped"]), ensure_ascii=False) for k in key) + "\n", encoding="utf-8")
    (run / args.out_subdir / "manifest.json").write_text(
        json.dumps(dict(prompt_version=PROMPT_VERSION, n_cases=len(disc), n_batches=len(manifest),
                        batches=manifest), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"discrepancias: {len(disc)} | lotes de {args.batch_size}: {len(manifest)}")
    print(f"inversión de orden aplicada en {sum(k['flipped'] for k in key)}/{len(key)} casos")
    print(f"clave ciega: {run / args.out_subdir / 'blind_key.jsonl'}  (el árbitro no la ve)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
