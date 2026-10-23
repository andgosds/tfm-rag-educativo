"""Regenera los lotes de gradación SOLO para las preguntas con premisa falsa o enunciado cuestionado.

Reutiliza ``build_qrels_batches_v3.py`` pero restringiendo a las unidades marcadas en
``question_premise_audit_v3.jsonl``, y escribiendo en una carpeta aparte para no pisar los
lotes ya decididos. La instrucción es la misma, enmendada con el criterio de premisa falsa.
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
    """Lee las líneas JSON no vacías de una cola o fuente de revisión."""
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> int:
    """Prepara lotes de revisión restringidos a las preguntas con premisa marcada."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--chunks", type=Path, required=True)
    args = ap.parse_args()

    run = args.run_dir
    out_dir = run / "judging_premise" / "batches"
    out_dir.mkdir(parents=True, exist_ok=True)

    instruction = (ROOT / "config" / PROMPT_VERSION).read_text(encoding="utf-8")
    chunks = {r["chunk_id"]: r for r in load_jsonl(args.chunks)}
    pairs = {r["base_qid"]: r for r in load_jsonl(ROOT / "data" / "golden" / "variants" / "explicitness_pairs_v3_all26.jsonl")}
    flagged = {r["base_qid"]: r for r in load_jsonl(ROOT / "data" / "golden" / "variants" / "question_premise_audit_v3.jsonl")}

    units = []
    for src in ("pools/blind_review_queue_collapsed.jsonl", "pools/reuse_confirmation_queue.jsonl"):
        for r in load_jsonl(run / src):
            if r["base_qid"] not in flagged:
                continue
            c = chunks[r["chunk_id"]]
            p = pairs[r["base_qid"]]
            units.append(dict(unit_id=r["unit_id"], base_qid=r["base_qid"], chunk_id=r["chunk_id"],
                              question_explicit=p["explicit_question"], question_implicit=p["implicit_question"],
                              retrieval_text=c["retrieval_text"],
                              premise_flag=flagged[r["base_qid"]]["premise_flag"]))
    units.sort(key=lambda u: (u["base_qid"], u["chunk_id"]))
    assert len({u["unit_id"] for u in units}) == len(units)

    manifest = []
    for i in range(0, len(units), BATCH_SIZE):
        batch = units[i : i + BATCH_SIZE]
        bid = f"pm-{i // BATCH_SIZE + 1:03d}"
        body = HEADER.format(instruction=instruction.strip())
        for n, u in enumerate(batch, 1):
            body += (
                f"\n## Unidad {n} — `{u['unit_id']}`\n\n"
                f"### Pregunta explícita\n{u['question_explicit']}\n\n"
                f"### Pregunta implícita\n{u['question_implicit']}\n\n"
                f"### Fragmento candidato\n{u['retrieval_text']}\n"
            )
        (out_dir / f"{bid}.md").write_text(body, encoding="utf-8")
        manifest.append(dict(batch_id=bid, file=str((out_dir / f"{bid}.md").relative_to(run)),
                             units=[u["unit_id"] for u in batch], n_units=len(batch)))

    (run / "judging_premise" / "manifest.json").write_text(
        json.dumps(dict(batch_size=BATCH_SIZE, n_units=len(units), n_batches=len(manifest),
                        prompt_version=PROMPT_VERSION, criterion="false_premise_v1", batches=manifest),
                   indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"unidades con premisa marcada: {len(units)}")
    print(f"lotes de {BATCH_SIZE}: {len(manifest)} -> {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
