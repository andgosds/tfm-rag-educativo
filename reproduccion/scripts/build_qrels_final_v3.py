"""Consolida los qrels definitivos de v3 a partir de las dos pasadas de gradación.

Precedencia de fuentes, de mayor a menor:

1. **Validación humana** (`human_validation_v3.jsonl`, `human_validation_premise_v3.jsonl`) —
   incluye los casos en que el usuario corrigió al árbitro. Siempre prevalece.
2. **Laudos del árbitro** (`verdicts_gpt-6-astra.jsonl`), para las unidades donde los dos
   jueces discreparon.
3. **Consenso de los dos jueces**, cuando coinciden.

La gradación de las 120 unidades con premisa marcada se toma de la pasada `judging_premise`
—que corrió con la instrucción enmendada—; el resto, de la pasada `judging`. Cada registro
lleva `grade_source` para que se pueda reconstruir de dónde salió cada grado.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_verdicts(path: Path) -> dict[str, dict]:
    """Reúne los veredictos por unidad o devuelve un índice vacío si no existe el archivo."""
    out: dict[str, dict] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.update(json.loads(line).get("verdicts", {}))
    return out


def load_jsonl(path: Path) -> list[dict]:
    """Carga los registros JSONL omitiendo las líneas vacías."""
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> int:
    """Consolida los grados v3 por precedencia de fuentes y separa la pasada de premisas."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-dir", type=Path, required=True)
    args = ap.parse_args()

    run = args.run_dir
    prem = {r["base_qid"] for r in load_jsonl(
        ROOT / "data" / "golden" / "variants" / "question_premise_audit_v3.jsonl")}

    human: dict[str, dict] = {}
    for f in ("judging/arbitration/human_validation_v3.jsonl",
              "judging_premise/human_validation_premise_v3.jsonl"):
        for r in load_jsonl(run / f):
            human[r["unit_id"]] = r

    rows = []
    for subdir, tag in (("judging", "main"), ("judging_premise", "premise")):
        q = run / subdir
        a, b = load_verdicts(q / "verdicts_gpt-6-sol.jsonl"), load_verdicts(q / "verdicts_mimo-v2.6-pro.jsonl")
        arb = load_verdicts(q / "arbitration" / "verdicts_gpt-6-astra.jsonl")
        for uid in sorted(set(a) | set(b)):
            if (uid.split("::")[0] in prem) != (tag == "premise"):
                continue
            va, vb = a.get(uid), b.get(uid)
            if uid in human:
                grade, source = human[uid]["human_grade"], "human_validation"
            elif uid in arb:
                grade, source = arb[uid]["grade"], "arbitration"
            elif va and vb and va["grade"] == vb["grade"]:
                grade, source = va["grade"], "judge_consensus"
            else:
                solo = va or vb
                assert solo is not None
                grade, source = solo["grade"], "single_judge"
            rows.append(dict(
                unit_id=uid, base_qid=uid.split("::")[0], chunk_id="::".join(uid.split("::")[1:]),
                grade=grade, grade_source=source, pass_tag=tag,
                judge_a=va["grade"] if va else None, judge_b=vb["grade"] if vb else None,
                arbitration=arb.get(uid, {}).get("grade"),
            ))

    out = run / "qrels_final_v3.jsonl"
    out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")

    print(f"qrels finales: {len(rows)}  -> {out.name}")
    print("procedencia del grado:", dict(sorted(Counter(r["grade_source"] for r in rows).items())))
    print("distribución final:", dict(sorted(Counter(r["grade"] for r in rows).items())))
    print("humanas aplicadas:", sum(1 for r in rows if r["grade_source"] == "human_validation"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
