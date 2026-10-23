"""Evalúa las respuestas de generación con un juez remoto vía `hermes chat --oneshot`.

Replica el patrón de la gradación de qrels, ya probado: cada lote se invoca en una sesión
aislada, de modo que el juez no ve la conversación ni otros lotes. Se usa sobre los tres
generadores incluidos y el mismo juez para todas las condiciones, para que las diferencias
observadas se atribuyan al generador y no al evaluador.

El contrato de salida es un veredicto por respuesta, con:

- `faithfulness` y `factual_correctness` en escala 0–2
- `behavior_ok`: si la conducta declarada corresponde a la esperada
- `citations_ok`: si las citas sostienen la respuesta

Las escalas son discretas y se gradúan por criterio explícito, no por parecer: una métrica
automática no se presenta como verdad absoluta, y el registro conserva el razonamiento del
juez para poder auditarlo después.

Cada celda del lote incluye el **texto completo** de los fragmentos recuperados, tomado del
corpus por id. La versión anterior mandaba solo los ids y los jueces no podían verificar
nada contra el contexto: el pase entero quedó invalidado y se repite. En `ragas_rubric_v3.2`
el criterio `behavior_ok` pasa además a graduar el **comportamiento real de la respuesta**
(0–2) en lugar de comparar la etiqueta declarada con la esperada, que era una igualdad de
strings sin valor de juicio; la conformidad de la etiqueta se registra aparte como
`label_ok`, calculada de forma determinista sin gastar juez. Los otros tres criterios no
cambian.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHUNKS = ROOT / "data" / "processed" / "chunks_v1.jsonl"

RUBRICA = """Eres un evaluador de un sistema RAG educativo. Para cada respuesta valorarás cuatro
criterios con una escala entera y sin decimales. No uses el conocimiento del mundo: juzga
únicamente con el contexto recuperado que se te facilita.

Cada respuesta viene con: la pregunta, el contexto recuperado, la respuesta generada, las
citas declaradas, la conducta esperada y la conducta declarada.

CRITERIOS

1. faithfulness (0–2): ¿la respuesta se sostiene en el contexto recuperado?
   2 = todo lo afirmado está respaldado por el contexto.
   1 = la idea principal está respaldada, pero hay algún detalle sin sostener.
   0 = contradice el contexto o afirma cosas que el contexto no contiene.

2. factual_correctness (0–2): ¿la respuesta es correcta en relación con la referencia?
   2 = coincide con la referencia en lo esencial.
   1 = correcta en lo esencial pero incompleta o con algún desajuste menor.
   0 = incorrecta, o responde a otra cosa distinta de lo preguntado.

3. behavior_ok (0–2): ¿el comportamiento real de la respuesta corresponde a la conducta
   esperada? Juzga lo que la respuesta hace, no la etiqueta que declare: si la etiqueta
   declarada contradice lo que la respuesta hace, cuenta lo que hace.
   2 = la respuesta se comporta como exige la conducta esperada.
   1 = se comporta así en lo esencial, pero omite un componente material de lo pedido o se
   desvía en algún detalle.
   0 = no se comporta como exige la conducta esperada.
   Recuerda: una pregunta de premisa falsa espera `grounded_correction`, no `abstain`, y
   aceptar la premisa sin corregirla es 0; abstenerse cuando el contexto basta para responder
   es 0; una abstención justificada y sin afirmaciones, cuando la abstención es lo esperado,
   es 2.

4. citations_ok (0–1): ¿las citas sostienen la respuesta?
   1 = las citas apuntan a la evidencia que respalda la respuesta, o la abstención no lleva
   citas. 0 = las citas no corresponden a la evidencia usada.

FORMATO DE SALIDA

Devuelve un objeto JSON por cada respuesta, en un array JSON, en el mismo orden en que se
presentan, con las claves: `id`, `faithfulness`, `factual_correctness`, `behavior_ok`,
`citations_ok`, `rationale`. La `rationale` es una frase breve y concreta, no una
justificación genérica.
"""


def cargar_corpus() -> dict[str, str]:
    """Índice id → texto de cada fragmento, para presentar el contexto entero al juez."""
    indice: dict[str, str] = {}
    with CHUNKS.open(encoding="utf-8") as fh:
        for l in fh:
            if l.strip():
                c = json.loads(l)
                indice[c["chunk_id"]] = c.get("text") or c.get("retrieval_text") or ""
    return indice


def build_prompt(rows: list[dict], corpus: dict[str, str] | None = None) -> str:
    """Prepara el lote de respuestas con el texto de sus contextos y referencias."""
    corpus = corpus or {}
    partes = ["Evalúa las siguientes respuestas. Devuelve un único array JSON.\n"]
    for i, r in enumerate(rows, 1):
        ids = r.get("retrieved_chunk_ids", []) or []
        ctxs = r.get("retrieved_contexts") or []
        bloques = []
        for k, cid in enumerate(ids):
            # el texto sale del corpus por id; si faltara, se recupera del contexto que
            # la propia fila de generación conserva (es el mismo texto, ya verificado)
            texto = corpus.get(cid)
            if texto is None and k < len(ctxs):
                texto = ctxs[k]
            if texto is None:
                texto = "(texto no disponible)"
            bloques.append(f"  [{cid}]\n  {texto}")
        ctx = "\n".join(bloques)
        partes.append(
            f"--- respuesta {i} ---\n"
            f"id: {r['qid']}\n"
            f"pregunta: {r['question']}\n"
            f"contexto recuperado:\n{ctx}\n"
            f"respuesta generada: {r.get('response', '')}\n"
            f"citas declaradas: {', '.join(r.get('citations', []) or ['NONE'])}\n"
            f"conducta esperada: {r.get('expected_behavior')}\n"
            f"conducta declarada: {r.get('reported_behavior')}\n"
            f"referencia: {r.get('reference')}\n"
        )
    return "\n".join(partes)


def invocar(query_path: Path, model: str, provider: str, reasoning: str | None) -> str:
    """Invoca al juez en una sesión aislada y devuelve su salida."""
    cmd = ["hermes", "chat", "--oneshot", "--query-file", str(query_path),
           "-m", model, "--provider", provider]
    if reasoning:
        cmd += ["--reasoning", reasoning]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    if proc.returncode != 0:
        raise RuntimeError(f"hermes chat falló: {proc.stderr[:300]}")
    return proc.stdout


def main() -> int:
    """Genera los lotes pendientes y guarda los veredictos del juez remoto."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inputs", nargs="+", type=Path, required=True)
    ap.add_argument("--batches-dir", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--model", default="gpt-6-sol")
    ap.add_argument("--provider", default="openai-codex")
    ap.add_argument("--reasoning", default="high")
    ap.add_argument("--batch-size", type=int, default=10)
    ap.add_argument("--subdir", default=None)
    ap.add_argument("--only-batches", action="store_true",
                    help="escribe los lotes y termina sin invocar a ningún juez")
    args = ap.parse_args()

    corpus = cargar_corpus()
    print(f"corpus: {len(corpus)} fragmentos con texto")

    rows: list[dict] = []
    for p in args.inputs:
        with p.open(encoding="utf-8") as fh:
            for l in fh:
                if l.strip():
                    r = json.loads(l)
                    if not r.get("base_qid"):
                        # los registros de generación no traen la pregunta base: se deriva
                        # del identificador de formulación, quitando el sufijo de explicitud
                        r["base_qid"] = r.get("qid", "").split("__")[0]
                    r["_origen"] = p.name
                    rows.append(r)
    print(f"respuestas a evaluar: {len(rows)}")

    lotes_dir = args.batches_dir / (args.subdir or "batches")
    lotes_dir.mkdir(parents=True, exist_ok=True)
    lotes = [rows[i:i + args.batch_size] for i in range(0, len(rows), args.batch_size)]
    for n, lote in enumerate(lotes, 1):
        (lotes_dir / f"lote-{n:03d}.txt").write_text(RUBRICA + "\n\n" + build_prompt(lote, corpus), encoding="utf-8")
    print(f"lotes generados: {len(lotes)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    # reanudable: si el fichero de salida ya existe, solo se evalúan las celdas ausentes
    # y se **anexa** en vez de truncar. Sin esto, relanzar tras un descarte de lote
    # borraría todo lo ya emitido.
    ya_hechos: set[tuple] = set()
    if args.output.exists():
        with args.output.open(encoding="utf-8") as fh:
            for l in fh:
                if l.strip():
                    d = json.loads(l)
                    # la celda la identifica el trío generador + estrategia + pregunta; el
                    # `qid` solo se repite entre estrategias y generadores
                    ya_hechos.add((d.get("generator_model"), d.get("retrieval_condition"), d.get("qid")))
        if ya_hechos:
            print(f"reanudación: {len(ya_hechos)} celdas ya evaluadas, se omiten")
    pendientes = [r for r in rows
                  if (r.get("generator_model"), r.get("retrieval_condition"), r["qid"]) not in ya_hechos]
    if not pendientes:
        print("nada por evaluar")
        return 0
    lotes = [pendientes[i:i + args.batch_size] for i in range(0, len(pendientes), args.batch_size)]
    for n, lote in enumerate(lotes, 1):
        (lotes_dir / f"lote-{n:03d}.txt").write_text(RUBRICA + "\n\n" + build_prompt(lote, corpus), encoding="utf-8")
    print(f"lotes generados: {len(lotes)}")

    if args.only_batches:
        print("solo lotes: no se invoca a ningún juez")
        return 0

    hechos = 0
    with args.output.open("a", encoding="utf-8") as out:
        for n, lote in enumerate(lotes, 1):
            qf = lotes_dir / f"lote-{n:03d}.txt"
            veredictos = None
            # el juez remoto devuelve a veces salida que no es un array JSON válido; se
            # reintenta en vez de descartar el lote, porque una celda perdida sería un
            # hueco silencioso en el diseño pareado
            for intento in range(1, 4):
                try:
                    txt = invocar(qf, args.model, args.provider, args.reasoning)
                    # `hermes chat --oneshot` devuelve la transcripción entera: el prompt
                    # al principio —que ya contiene corchetes—, la respuesta en medio y los
                    # metadatos de sesión al final. Buscar el array por su contenido: el
                    # campo `faithfulness` solo aparece en los veredictos.
                    pos = txt.rfind('"faithfulness"')
                    if pos == -1:
                        pos = txt.rfind('"id"')
                    inicio, fin = txt.rfind('[', 0, pos), txt.find(']', pos)
                    candidato = None
                    while pos != -1 and inicio != -1 and fin != -1:
                        try:
                            candidato = json.loads(txt[inicio:fin + 1])
                            break
                        except json.JSONDecodeError:
                            fin = txt.find(']', fin + 1)
                    if candidato is None:
                        raise ValueError('no se encontró el array de veredictos en la salida')
                    if isinstance(candidato, list) and len(candidato) == len(lote):
                        veredictos = candidato
                        break
                    print(f"  lote {n:03d}: intento {intento}, {len(candidato)} veredictos para {len(lote)} celdas")
                except Exception as exc:  # noqa: BLE001
                    print(f"  lote {n:03d}: intento {intento} falló — {repr(exc)[:120]}")
            if veredictos is None:
                print(f"  lote {n:03d}: DESCARTADO tras 3 intentos")
                continue
            for r, v in zip(lote, veredictos):
                out.write(json.dumps({
                    "qid": r["qid"], "base_qid": r.get("base_qid"),
                    "generator_model": r.get("generator_model"),
                    "retrieval_condition": r.get("retrieval_condition"),
                    "faithfulness": v.get("faithfulness"),
                    "factual_correctness": v.get("factual_correctness"),
                    "behavior_ok": v.get("behavior_ok"),
                    "citations_ok": v.get("citations_ok"),
                    "rationale": v.get("rationale"),
                    "judge_model": args.model, "judge_provider": args.provider,
                    "prompt_version": "ragas_rubric_v3.2", "batch": n,
                    # conformidad de la etiqueta declarada: determinista, sin juez
                    "label_ok": int(r.get("reported_behavior") == r.get("expected_behavior")),
                }, ensure_ascii=False) + "\n")
                hechos += 1
            out.flush()
            print(f"  lote {n:03d}: {len(veredictos)} veredictos")
    print(f"veredictos escritos: {hechos}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
