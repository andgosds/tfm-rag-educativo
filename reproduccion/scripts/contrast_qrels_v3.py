"""Contrasta los veredictos de los dos jueces de qrels v3 y construye la cola de riesgo.

Cruzado por ``unit_id``, produce tres cosas:

1. el desacuerdo entre jueces —que es el núcleo del subconjunto de riesgo, sin que haya
   que construirlo después porque los dos juzgaron los mismos lotes byte a byte—;
2. la distribución de grados por juez, para ver si uno es sistemáticamente más generoso;
3. la cola de riesgo ampliada: todo grado 2, todo desacuerdo, todo conflicto de
   equivalencia y una muestra determinista de consensos, para poder auditar que el
   acuerdo no sea un error compartido.

La muestra determinista se basa en un hash estable del ``unit_id``, de modo que el
subconjunto auditado sea reproducible y no dependa del orden de lectura.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

AUDIT_SAMPLE = 60


def load_verdicts(path: Path) -> dict[str, dict]:
    """Indexa los veredictos por unidad y añade el lote y el modelo de origen."""
    out: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        for uid, v in row.get("verdicts", {}).items():
            out[uid] = dict(v, batch_id=row["batch_id"], model=row["model"])
    return out


def audit_key(unit_id: str) -> str:
    """Obtiene un hash estable para ordenar la muestra de auditoría de consensos."""
    return hashlib.sha256(unit_id.encode("utf-8")).hexdigest()


def main() -> int:
    """Contrasta los grados de ambos jueces y exporta la cola ampliada de riesgo."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--judge-a", default="gpt-6-sol")
    ap.add_argument("--judge-b", default="mimo-v2.6-pro")
    ap.add_argument("--audit-sample", type=int, default=AUDIT_SAMPLE)
    args = ap.parse_args()

    run = args.run_dir
    a = load_verdicts(run / "judging" / f"verdicts_{args.judge_a}.jsonl")
    b = load_verdicts(run / "judging" / f"verdicts_{args.judge_b}.jsonl")

    common = sorted(set(a) & set(b))
    print(f"{args.judge_a}: {len(a)} unidades | {args.judge_b}: {len(b)} | comunes: {len(common)}")
    only_a, only_b = sorted(set(a) - set(b)), sorted(set(b) - set(a))
    if only_a or only_b:
        print(f"  sin cubrir: solo {args.judge_a} {len(only_a)}, solo {args.judge_b} {len(only_b)}")

    mat = Counter((a[u]["grade"], b[u]["grade"]) for u in common)
    agree = sum(n for (ga, gb), n in mat.items() if ga == gb)
    print(f"\nacuerdo: {agree}/{len(common)} = {agree / len(common):.3f}")
    print("matriz (A=filas, B=columnas):")
    for ga in (0, 1, 2):
        print(f"   grado {ga}: " + "  ".join(f"{mat.get((ga, gb), 0):>4}" for gb in (0, 1, 2)))
    for name, j in ((args.judge_a, a), (args.judge_b, b)):
        dist = Counter(j[u]["grade"] for u in common)
        print(f"{name}: " + "  ".join(f"grado {g} = {dist.get(g, 0)}" for g in (0, 1, 2)))

    conflicts = [u for u in common if a[u]["equivalence_conflict"] or b[u]["equivalence_conflict"]]
    disagree = [u for u in common if a[u]["grade"] != b[u]["grade"]]
    any_two = [u for u in common if a[u]["grade"] == 2 or b[u]["grade"] == 2]
    consensus = [u for u in common if a[u]["grade"] == b[u]["grade"]]
    sample = sorted(consensus, key=audit_key)[: args.audit_sample]

    risk, motivo = [], {}
    for u in common:
        razones = []
        if u in disagree:
            razones.append("discrepancia")
        if u in any_two:
            razones.append("grado2")
        if u in conflicts:
            razones.append("equivalence_conflict")
        if u in sample:
            razones.append("muestra_consenso")
        if razones:
            risk.append(u)
            motivo[u] = razones

    out = run / "judging" / "risk_queue_v3.jsonl"
    with out.open("w", encoding="utf-8") as fh:
        for u in risk:
            fh.write(json.dumps(dict(
                unit_id=u, base_qid=a[u]["unit_id"].split("::")[0] if False else u.split("::")[0],
                chunk_id="::".join(u.split("::")[1:]),
                verdict_judge_a=a[u], verdict_judge_b=b[u],
                risk_reasons=motivo[u],
            ), ensure_ascii=False) + "\n")

    print(f"\nsubconjunto de riesgo: {len(risk)} unidades -> {out}")
    print(f"   discrepancias: {len(disagree)}")
    print(f"   con algún grado 2: {len(any_two)}")
    print(f"   conflicto de equivalencia: {len(conflicts)}")
    print(f"   muestra de consensos: {len(sample)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
