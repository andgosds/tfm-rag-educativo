"""Ejecuta la gradación de qrels v3 con los dos jueces, por lotes y en sesiones aisladas.

Cada lote se envía con ``hermes chat --oneshot --query-file`` a cada juez, de modo que
cada juicio se emite en una sesión que nace y muere sin acceso a esta conversación, a la
hoja humana ni a las decisiones del otro juez. Los dos jueces reciben los mismos 58
ficheros, idénticos byte a byte, para que la discrepancia A−B sea el subconjunto de
riesgo por construcción.

Identificadores exactos del catálogo del proveedor, registrados en el pre-registro §13:

    hermes chat --oneshot --query-file <lote> -m gpt-6-sol     --provider openai-codex --reasoning high
    hermes chat --oneshot --query-file <lote> -m mimo-v2.6-pro --provider opencode-go

Reanudable: los lotes ya decididos por cada juez se omiten en la siguiente ejecución.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PROMPT_VERSION = "qrels_review_prompt_v3.md"

JUDGES = {
    "gpt-6-sol": dict(provider="openai-codex", model="gpt-6-sol", reasoning="high"),
    "mimo-v2.6-pro": dict(provider="opencode-go", model="mimo-v2.6-pro", reasoning=None),
}

JSON_LINE = re.compile(r"\{[^{}\n]*\"unit_id\"[^{}\n]*\}")


def extract_verdicts(text: str) -> dict[str, dict]:
    """Una línea JSON por unidad, tolerando prosa alrededor y marcas de código."""
    out: dict[str, dict] = {}
    for m in JSON_LINE.finditer(text):
        try:
            obj = json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        uid = obj.get("unit_id")
        if not uid or uid in out:
            continue
        grade = obj.get("grade")
        if grade not in (0, 1, 2):
            continue
        out[uid] = dict(
            grade=int(grade),
            confidence=str(obj.get("confidence", "low")),
            equivalence_conflict=bool(obj.get("equivalence_conflict", False)),
            rationale=str(obj.get("rationale", ""))[:500],
        )
    return out


def invoke(judge: dict, query_file: Path, timeout: int) -> str:
    """Envía el lote al juez en una sesión aislada y devuelve la salida estándar."""
    cmd = ["hermes", "chat", "--oneshot", "--query-file", str(query_file),
           "-m", judge["model"], "--provider", judge["provider"], "--safe-mode"]
    if judge.get("reasoning"):
        cmd += ["--reasoning", judge["reasoning"]]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return proc.stdout


def main() -> int:
    """Procesa los lotes pendientes del juez elegido y registra su cobertura y errores."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--judge", choices=sorted(JUDGES), required=True)
    ap.add_argument("--subdir", default="judging")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--timeout", type=int, default=1800)
    args = ap.parse_args()

    run = args.run_dir
    queue = run / args.subdir
    judge = JUDGES[args.judge]
    manifest = json.loads((queue / "manifest.json").read_text(encoding="utf-8"))
    out_path = queue / f"verdicts_{args.judge}.jsonl"

    done: set[str] = set()
    if out_path.exists():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["batch_id"])
    pending = [b for b in manifest["batches"] if b["batch_id"] not in done]
    if args.limit:
        pending = pending[: args.limit]
    print(f"juez: {args.judge} ({judge['model']} sobre {judge['provider']})")
    print(f"lotes: {len(manifest['batches'])} | decididos: {len(done)} | por decidir: {len(pending)}")

    stamp = datetime.now(timezone.utc).isoformat()
    out = out_path.open("a", encoding="utf-8")
    for n, batch in enumerate(pending, 1):
        query_file = run / batch["file"]
        row = dict(
            batch_id=batch["batch_id"], judge=args.judge, model=judge["model"],
            provider=judge["provider"], reasoning=judge.get("reasoning"),
            prompt_version=PROMPT_VERSION, execution_date=stamp,
            expected_units=batch["units"], verdicts={}, status="pending",
        )
        try:
            text = invoke(judge, query_file, args.timeout)
            verdicts = extract_verdicts(text)
            row["verdicts"] = verdicts
            missing = [u for u in batch["units"] if u not in verdicts]
            row["missing_units"] = missing
            row["status"] = "complete" if not missing else "partial"
            row["raw_chars"] = len(text)
        except Exception as exc:  # noqa: BLE001 - se registra y se continúa
            row["status"] = "error"
            row["error"] = repr(exc)[:400]
        out.write(json.dumps(row, ensure_ascii=False) + "\n")
        out.flush()
        n_ok = len(row.get("verdicts", {}))
        print(f"  [{n}/{len(pending)}] {batch['batch_id']}: {row['status']} "
              f"({n_ok}/{len(batch['units'])} veredictos)")
    out.close()
    print(f"fin. salida: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
