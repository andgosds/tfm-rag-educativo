"""Arbitraje delegado de las discrepancias A−B en la evaluación de generación v3.

Los dos evaluadores (juez 1 = `gpt-6-sol`, juez 2 = `mimo-v2.6-pro`; el mapeo vive en este
docstring y en los metadatos de salida) discreparon en 158 celdas. Bajo delegación explícita
del usuario, un árbitro externo (`gpt-6-astra`, `--reasoning high`) **resuelve solo los
criterios en discrepancia** de cada celda, juzgando por su cuenta con el contexto recuperado
y la referencia. Los jueces se presentan anonimizados como «juez 1» y «juez 2» para que la
marca no ancle la decisión.

Las decisiones del árbitro **no son juicio humano**: se registran con
`decision_source: arbitro_delegado` y `status: pending_human_validation`, y el usuario las
validará después por lotes. Nada de lo que salga de aquí entra en la memoria como revisión
humana.

Cada caso lleva el texto completo de los fragmentos recuperados (mismo arreglo que en la
evaluación: lookup por id en el corpus) y los razonamientos de ambos jueces. La ejecución es
reanudable por la clave generador + estrategia + pregunta, y cada intento crudo se conserva.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHUNKS = ROOT / "data" / "processed" / "chunks_v1.jsonl"
RUN = ROOT / "outputs" / "local_runs" / "generation_scaling_v3"

JUEZ1 = "gpt-6-sol"          # juez A de la evaluación
JUEZ2 = "mimo-v2.6-pro"      # juez B de la evaluación

RUBRICA = """Eres el árbitro de una evaluación de respuestas de un sistema RAG educativo. Dos
evaluadores independientes han puntuado las mismas respuestas y han discrepado en algunos
criterios. Tu tarea es resolver SOLO los criterios en discrepancia de cada respuesta,
juzgando por ti mismo con el contexto recuperado y la referencia: puedes dar la razón al
juez 1, al juez 2 o fijar un valor distinto si ambos se salen de lo que sostiene la evidencia.

Cada respuesta viene con: la pregunta, el contexto recuperado (texto completo de los
fragmentos), la respuesta generada, las citas declaradas, la conducta esperada, la referencia
y las puntuaciones y razonamientos de los dos jueces.

CRITERIOS (misma escala que los evaluadores; puntúa solo los que estén en discrepancia)

1. faithfulness (0–2): ¿la respuesta se sostiene en el contexto recuperado?
   2 = todo lo afirmado está respaldado por el contexto.
   1 = la idea principal está respaldada, pero hay algún detalle sin sostener.
   0 = contradice el contexto o afirma cosas que el contexto no contiene.

2. factual_correctness (0–2): ¿la respuesta es correcta en relación con la referencia?
   2 = coincide con la referencia en lo esencial.
   1 = correcta en lo esencial pero incompleta o con algún desajuste menor.
   0 = incorrecta, o responde a otra cosa distinta de lo preguntado.

3. behavior_ok (0–2): ¿el comportamiento real de la respuesta corresponde a la conducta
   esperada? Juzga lo que la respuesta hace, no la etiqueta que declare.
   2 = la respuesta se comporta como exige la conducta esperada.
   1 = se comporta así en lo esencial, pero omite un componente material de lo pedido o se
   desvía en algún detalle.
   0 = no se comporta como exige la conducta esperada.
   Una pregunta de premisa falsa espera `grounded_correction`, no `abstain`, y aceptar la
   premisa sin corregirla es 0; abstenerse cuando el contexto basta para responder es 0; una
   abstención justificada y sin afirmaciones, cuando la abstención es lo esperado, es 2.

4. citations_ok (0–1): ¿las citas sostienen la respuesta?
   1 = las citas apuntan a la evidencia que respalda la respuesta, o la abstención no lleva
   citas. 0 = las citas no corresponden a la evidencia usada.

FORMATO DE SALIDA
Devuelve un objeto JSON por cada respuesta, en un array JSON, en el mismo orden en que se
presentan, con las claves:
- `id`: el identificador de la respuesta, copiado tal cual.
- `resolutions`: objeto con una entrada por cada criterio en discrepancia; cada entrada tiene
  `final` (tu puntuación, entera, dentro del rango del criterio) y `rationale` (una frase
  breve y concreta que justifique la decisión refiriéndote a la evidencia o a los dos
  razonamientos).
- `note`: opcional, una frase si el caso es dudoso.
No puntúes criterios que no estén en discrepancia.
"""

RANGOS = {"faithfulness": (0, 2), "factual_correctness": (0, 2),
          "behavior_ok": (0, 2), "citations_ok": (0, 1)}


def cargar_corpus() -> dict[str, str]:
    """Indexa el texto de los fragmentos del corpus por su identificador."""
    indice: dict[str, str] = {}
    with CHUNKS.open(encoding="utf-8") as fh:
        for l in fh:
            if l.strip():
                c = json.loads(l)
                indice[c["chunk_id"]] = c.get("text") or c.get("retrieval_text") or ""
    return indice


def cargar_casos(corpus: dict[str, str]) -> list[dict]:
    """Une el contraste con las filas de generación para armar la unidad completa."""
    with (RUN / "contraste_jueces_v3.jsonl").open(encoding="utf-8") as fh:
        contrastes = [json.loads(l) for l in fh if l.strip()]
    gen: dict[tuple, dict] = {}
    for p in sorted(RUN.glob("rag_*_top5_*.jsonl")):
        if "_failures" in p.name or "metadata" in p.name:
            continue
        with p.open(encoding="utf-8") as fh:
            for l in fh:
                if l.strip():
                    d = json.loads(l)
                    gen[(d["generator_model"], d["retrieval_condition"], d["qid"])] = d
    casos = []
    for c in contrastes:
        k = (c["generator_model"], c["retrieval_condition"], c["qid"])
        g = gen.get(k)
        if g is None:
            raise ValueError(f"caso del contraste sin fila de generación: {k}")
        c["_gen"] = g
        c["_key"] = k
        casos.append(c)
    return casos


def build_prompt(casos: list[dict], corpus: dict[str, str]) -> str:
    """Compone los casos de arbitraje con evidencia y puntuaciones de jueces anonimizados."""
    partes = ["Resuelve las discrepancias de los siguientes casos. Devuelve un único array JSON.\n"]
    for i, c in enumerate(casos, 1):
        g = c["_gen"]
        ids = g.get("retrieved_chunk_ids", []) or []
        ctxs = g.get("retrieved_contexts") or []
        bloques = []
        for k, cid in enumerate(ids):
            texto = corpus.get(cid)
            if texto is None and k < len(ctxs):
                texto = ctxs[k]
            bloques.append(f"  [{cid}]\n  {texto if texto is not None else '(texto no disponible)'}")
        ctx = "\n".join(bloques)
        a, b = c["juezA"], c["juezB"]
        partes.append(
            f"--- caso {i} ---\n"
            f"id: {c['generator_model']}|{c['retrieval_condition']}|{c['qid']}\n"
            f"pregunta: {g['question']}\n"
            f"conducta esperada: {g.get('expected_behavior')}\n"
            f"contexto recuperado:\n{ctx}\n"
            f"respuesta generada: {g.get('response', '')}\n"
            f"citas declaradas: {', '.join(g.get('citations', []) or ['NONE'])}\n"
            f"referencia: {g.get('reference')}\n"
            f"juez 1: faithfulness={a.get('faithfulness')} factual_correctness={a.get('factual_correctness')} "
            f"behavior_ok={a.get('behavior_ok')} citations_ok={a.get('citations_ok')}\n"
            f"  razonamiento: {c.get('rationaleA')}\n"
            f"juez 2: faithfulness={b.get('faithfulness')} factual_correctness={b.get('factual_correctness')} "
            f"behavior_ok={b.get('behavior_ok')} citations_ok={b.get('citations_ok')}\n"
            f"  razonamiento: {c.get('rationaleB')}\n"
            f"criterios en discrepancia: {', '.join(c['criterios'])}\n"
        )
    return "\n".join(partes)


def invocar(query_path: Path, model: str, provider: str, reasoning: str | None) -> str:
    """Invoca el árbitro mediante Hermes y devuelve su salida textual."""
    cmd = ["hermes", "chat", "--oneshot", "--query-file", str(query_path),
           "-m", model, "--provider", provider]
    if reasoning:
        cmd += ["--reasoning", reasoning]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    if proc.returncode != 0:
        raise RuntimeError(f"hermes chat falló: {proc.stderr[:300]}")
    return proc.stdout


def extraer_array(txt: str) -> list | None:
    """Busca el array de resoluciones por su contenido, no por el primer corchete."""
    pos = txt.rfind('"resolutions"')
    if pos == -1:
        pos = txt.rfind('"final"')
    inicio, fin = txt.rfind('[', 0, pos), txt.find(']', pos)
    while pos != -1 and inicio != -1 and fin != -1:
        try:
            candidato = json.loads(txt[inicio:fin + 1])
            return candidato if isinstance(candidato, list) else None
        except json.JSONDecodeError:
            fin = txt.find(']', fin + 1)
    return None


def validar(veredictos: list, lote: list[dict]) -> list[dict]:
    """Comprueba forma, rangos y cobertura de los criterios en discrepancia."""
    if len(veredictos) != len(lote):
        raise ValueError(f"{len(veredictos)} resoluciones para {len(lote)} casos")
    out = []
    for c, v in zip(lote, veredictos):
        res = v.get("resolutions")
        if not isinstance(res, dict):
            raise ValueError(f"{c['_key']}: falta resolutions")
        faltan = [cr for cr in c["criterios"] if cr not in res]
        if faltan:
            raise ValueError(f"{c['_key']}: sin resolver {faltan}")
        for cr, r in res.items():
            if cr not in RANGOS:
                raise ValueError(f"{c['_key']}: criterio desconocido {cr}")
            lo, hi = RANGOS[cr]
            fin = r.get("final")
            if not isinstance(fin, int) or not (lo <= fin <= hi):
                raise ValueError(f"{c['_key']}: {cr} fuera de rango ({fin})")
            if not str(r.get("rationale", "")).strip():
                raise ValueError(f"{c['_key']}: {cr} sin rationale")
        out.append(v)
    return out


def main() -> int:
    """Arbitra las discrepancias pendientes por lotes y conserva intentos y resoluciones."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--batches-dir", type=Path, required=True)
    ap.add_argument("--model", default="gpt-6-astra")
    ap.add_argument("--provider", default="openai-codex")
    ap.add_argument("--reasoning", default="high")
    ap.add_argument("--batch-size", type=int, default=5)
    ap.add_argument("--max-cells", type=int, default=None,
                    help="limita los casos (sonda de humo)")
    args = ap.parse_args()

    corpus = cargar_corpus()
    casos = cargar_casos(corpus)
    if args.max_cells:
        casos = casos[: args.max_cells]
    print(f"casos a arbitrar: {len(casos)}")

    lotes_dir = args.batches_dir / "lotes"
    raw_dir = args.batches_dir / "raw"
    lotes_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    hechos: set[tuple] = set()
    if args.output.exists():
        with args.output.open(encoding="utf-8") as fh:
            for l in fh:
                if l.strip():
                    d = json.loads(l)
                    hechos.add((d.get("generator_model"), d.get("retrieval_condition"), d.get("qid")))
        if hechos:
            print(f"reanudación: {len(hechos)} casos ya arbitrados, se omiten")
    pendientes = [c for c in casos if c["_key"] not in hechos]
    if not pendientes:
        print("nada por arbitrar")
        return 0

    lotes = [pendientes[i:i + args.batch_size] for i in range(0, len(pendientes), args.batch_size)]
    for n, lote in enumerate(lotes, 1):
        (lotes_dir / f"lote-{n:03d}.txt").write_text(RUBRICA + "\n\n" + build_prompt(lote, corpus), encoding="utf-8")
    print(f"lotes generados: {len(lotes)}")

    hechos_n = 0
    with args.output.open("a", encoding="utf-8") as out:
        for n, lote in enumerate(lotes, 1):
            qf = lotes_dir / f"lote-{n:03d}.txt"
            resueltos = None
            for intento in range(1, 4):
                try:
                    txt = invocar(qf, args.model, args.provider, args.reasoning)
                    (raw_dir / f"lote-{n:03d}-intento{intento}.txt").write_text(txt, encoding="utf-8")
                    candidato = extraer_array(txt)
                    if candidato is None:
                        raise ValueError("no se encontró el array de resoluciones")
                    resueltos = validar(candidato, lote)
                    break
                except Exception as exc:  # noqa: BLE001
                    print(f"  lote {n:03d}: intento {intento} falló — {repr(exc)[:120]}")
            if resueltos is None:
                print(f"  lote {n:03d}: DESCARTADO tras 3 intentos")
                continue
            for c, v in zip(lote, resueltos):
                out.write(json.dumps({
                    "qid": c["qid"], "generator_model": c["generator_model"],
                    "retrieval_condition": c["retrieval_condition"],
                    "disputed_criteria": c["criterios"],
                    "juezA": c["juezA"], "juezB": c["juezB"],
                    "rationaleA": c.get("rationaleA"), "rationaleB": c.get("rationaleB"),
                    "resolutions": v.get("resolutions"), "note": v.get("note"),
                    "decision_source": "arbitro_delegado",
                    "status": "pending_human_validation",
                    "juez1_model": JUEZ1, "juez2_model": JUEZ2,
                    "arbitrator_model": args.model, "arbitrator_provider": args.provider,
                    "reasoning": args.reasoning,
                    "prompt_version": "arbitration_rubric_v1", "batch": n,
                }, ensure_ascii=False) + "\n")
                hechos_n += 1
            out.flush()
            print(f"  lote {n:03d}: {len(resueltos)} casos resueltos")
    print(f"resoluciones escritas: {hechos_n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
