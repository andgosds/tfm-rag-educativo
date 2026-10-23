"""Triaje automático de la gradación de qrels v3 con un juez local aislado.

Aplica la instrucción versionada ``config/qrels_review_prompt_v3.md`` sobre las unidades
colapsadas de la hoja ciega y propone un grado 0/1/2 por unidad. Los resultados **no**
pasan a los qrels: sirven para priorizar la adjudicación humana dirigida por riesgo.

Reglas de trazabilidad que respeta el diseño:

- Un juez por sesión, sin acceso a la hoja humana ni a otros jueces: cada unidad se envía
  en una llamada independiente, sin historial.
- La entrada es una copia con las revisiones vacías; nunca se reescribe el original.
- Se guardan modelo, versión del prompt, fecha de ejecución y parámetros junto a cada
  decisión, para que el juicio pueda repetirse y auditarse.
- La copia que recibe el juez no contiene scores, método de origen ni posición.

El script es reanudable: si se interrumpe, las unidades ya decididas se conservan y la
siguiente ejecución continúa por donde se quedó.
"""
from __future__ import annotations

import argparse
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PROMPT_VERSION = "qrels_review_prompt_v3.md"
MODEL = "qwen3.8:27b"
THINK = "medium"
TEMPERATURE = 0.0
NUM_PREDICT = 4096


def call_ollama(host: str, messages: list[dict], think, temperature: float) -> dict:
    """Solicita al juez local una respuesta con los parámetros fijados para el triaje."""
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "think": think,
        "options": {"temperature": temperature, "num_predict": NUM_PREDICT},
    }
    req = urllib.request.Request(
        host + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        return json.loads(resp.read())


def parse_verdict(text: str) -> dict:
    """Extrae el objeto JSON de la respuesta, tolerando ruido y truncación del final."""
    start = text.find("{")
    if start < 0:
        raise ValueError(f"sin objeto JSON en la respuesta: {text[:200]!r}")
    end = text.rfind("}")
    body = text[start : end + 1] if end > start else text[start:]
    try:
        obj = json.loads(body)
    except json.JSONDecodeError:
        # Recortado por num_predict: se cierra lo que falta y se conserva lo leído.
        candidate = body
        for cut in range(len(candidate), 0, -1):
            frag = candidate[:cut].rstrip().rstrip(",") + "}"
            try:
                obj = json.loads(frag)
                break
            except json.JSONDecodeError:
                continue
        else:
            raise ValueError(f"JSON ilegible: {body[:200]!r}")
    grade = obj.get("grade")
    if grade not in (0, 1, 2):
        raise ValueError(f"grado fuera de rango: {grade!r}")
    return {
        "grade": int(grade),
        "confidence": obj.get("confidence", "low"),
        "equivalence_conflict": bool(obj.get("equivalence_conflict", False)),
        "rationale": str(obj.get("rationale", ""))[:500],
    }


def main() -> int:
    """Propone grados para las unidades pendientes sin convertirlos en adjudicaciones humanas."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--host", default="http://127.0.0.1:11434")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--think", default=THINK)
    ap.add_argument("--output", type=Path, default=None,
                    help="fichero de salida; por defecto, dentro de pools/")
    args = ap.parse_args()

    run = args.run_dir
    queue_path = run / "pools" / "blind_review_queue_collapsed.jsonl"
    out_path = args.output or (run / "pools" / "blind_triage_qwen38_27b.jsonl")
    instruction = (Path(__file__).resolve().parents[1] / "config" / PROMPT_VERSION).read_text(encoding="utf-8")

    units = [json.loads(l) for l in queue_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    done: dict[str, dict] = {}
    if out_path.exists():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                done[r["unit_id"]] = r

    pending = [u for u in units if u["unit_id"] not in done]
    if args.limit:
        pending = pending[: args.limit]
    print(f"unidades: {len(units)} | ya decididas: {len(done)} | por decidir: {len(pending)}")

    started = datetime.now(timezone.utc).isoformat()
    out = out_path.open("a", encoding="utf-8")
    errors = 0
    consecutive_errors = 0
    for i, u in enumerate(pending, 1):
        user = (
            f"## Pregunta explícita\n{u['question_explicit']}\n\n"
            f"## Pregunta implícita\n{u['question_implicit']}\n\n"
            f"## Fragmento candidato\n{u['retrieval_text']}\n\n"
            "Asigna el grado único que vale para las dos redacciones."
        )
        try:
            resp = call_ollama(args.host, [
                {"role": "system", "content": instruction},
                {"role": "user", "content": user},
            ], think=args.think, temperature=TEMPERATURE)
            content = (resp.get("message") or {}).get("content") or ""
            thinking = (resp.get("message") or {}).get("thinking") or ""
            if not content.strip() and thinking.strip():
                # El modelo agotó num_predict razonando: el veredicto suele estar al final.
                content = thinking
            verdict = parse_verdict(content)
            row = dict(
                unit_id=u["unit_id"], base_qid=u["base_qid"], chunk_id=u["chunk_id"],
                covered_pool_ids=u["covered_pool_ids"], reviews=[dict(
                    reviewer=MODEL, reviewer_role="triage_assistant",
                    prompt_version=PROMPT_VERSION, think=args.think,
                    temperature=TEMPERATURE, execution_date=started,
                    thinking_chars=len((resp.get("message") or {}).get("thinking") or ""),
                    **verdict,
                )],
                human_decision=None, annotation_status="triaged_pending_human",
                triage_model=MODEL, triage_prompt_version=PROMPT_VERSION,
            )
        except Exception as exc:  # noqa: BLE001 - se registra y se continúa
            errors += 1
            row = dict(
                unit_id=u["unit_id"], base_qid=u["base_qid"], chunk_id=u["chunk_id"],
                covered_pool_ids=u["covered_pool_ids"], reviews=[],
                human_decision=None, annotation_status="triage_error",
                triage_model=MODEL, triage_prompt_version=PROMPT_VERSION,
                error=repr(exc)[:400],
            )
        out.write(json.dumps(row, ensure_ascii=False) + "\n")
        out.flush()
        if row["annotation_status"] == "triage_error":
            errors += 1
            consecutive_errors += 1
            if consecutive_errors >= 5:
                out.close()
                raise SystemExit(
                    f"abortado tras {consecutive_errors} errores consecutivos: "
                    f"el juez no responde. Cola conservada para reanudar ({i - consecutive_errors} decididas)."
                )
        else:
            consecutive_errors = 0
    out.close()
    print(f"fin. errores: {errors} | salida: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
