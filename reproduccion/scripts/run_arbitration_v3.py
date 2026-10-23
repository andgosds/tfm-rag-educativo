"""Arbitraje ciego de discrepancias con `gpt-6-astra`, por lotes y en sesiones aisladas.

Mismo patrón que ``run_qrels_judges_v3.py``: cada lote se envía con
``hermes chat --oneshot --query-file`` para que cada juicio nazca y muera en una sesión
aislada, sin acceso a la conversación de trabajo, a la clave ciega ni a los veredictos
originales más allá de los dos que se le muestran anonimizados.

    hermes chat --oneshot --query-file <lote> -m gpt-6-astra --provider openai-codex --reasoning high

Reanudable: los lotes ya arbitrados se omiten en la siguiente ejecución.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PROMPT_VERSION = "arbitration_prompt_v3.md"
JUDGE = dict(provider="openai-codex", model="gpt-6-astra", reasoning="high")

JSON_LINE = re.compile(r"\{[^{}\n]*\"unit_id\"[^{}\n]*\}")


def extract_verdicts(text: str) -> dict[str, dict]:
    """Extrae laudos JSON con grado válido y conserva el primero de cada unidad."""
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
            side=str(obj.get("side", "")),
            confidence=str(obj.get("confidence", "low")),
            rationale=str(obj.get("rationale", ""))[:500],
        )
    return out


def main() -> int:
    """Arbitra los lotes pendientes y registra sus laudos y unidades ausentes."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--subdir", default="judging/arbitration")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--timeout", type=int, default=1800)
    args = ap.parse_args()

    run = args.run_dir
    arb = run / args.subdir
    manifest = json.loads((arb / "manifest.json").read_text(encoding="utf-8"))
    out_path = arb / "verdicts_gpt-6-astra.jsonl"

    done = set()
    if out_path.exists():
        done = {json.loads(l)["batch_id"] for l in out_path.read_text(encoding="utf-8").splitlines() if l.strip()}
    pending = [b for b in manifest["batches"] if b["batch_id"] not in done]
    if args.limit:
        pending = pending[: args.limit]
    print(f"árbitro: {JUDGE['model']} sobre {JUDGE['provider']} (reasoning {JUDGE['reasoning']})")
    print(f"lotes: {len(manifest['batches'])} | decididos: {len(done)} | por decidir: {len(pending)}")

    stamp = datetime.now(timezone.utc).isoformat()
    with out_path.open("a", encoding="utf-8") as out:
        for n, batch in enumerate(pending, 1):
            query_file = arb / "batches" / f"{batch['batch_id']}.md"
            row = dict(batch_id=batch["batch_id"], judge=JUDGE["model"], provider=JUDGE["provider"],
                       reasoning=JUDGE["reasoning"], prompt_version=PROMPT_VERSION,
                       execution_date=stamp, expected_units=batch["units"], verdicts={}, status="pending")
            try:
                proc = subprocess.run(
                    ["hermes", "chat", "--oneshot", "--query-file", str(query_file),
                     "-m", JUDGE["model"], "--provider", JUDGE["provider"],
                     "--reasoning", JUDGE["reasoning"], "--safe-mode"],
                    capture_output=True, text=True, timeout=args.timeout)
                verdicts = extract_verdicts(proc.stdout)
                row["verdicts"] = verdicts
                missing = [u for u in batch["units"] if u not in verdicts]
                row["missing_units"] = missing
                row["status"] = "complete" if not missing else "partial"
                row["raw_chars"] = len(proc.stdout)
            except Exception as exc:  # noqa: BLE001
                row["status"] = "error"
                row["error"] = repr(exc)[:400]
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            out.flush()
            print(f"  [{n}/{len(pending)}] {batch['batch_id']}: {row['status']} "
                  f"({len(row.get('verdicts', {}))}/{len(batch['units'])} laudos)")
    print(f"fin. salida: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
