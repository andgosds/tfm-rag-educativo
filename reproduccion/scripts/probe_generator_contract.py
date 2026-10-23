"""Prueba el contrato de tres campos antes de lanzar la generación.

Un modelo de baja capacidad puede entender la tarea y aun así no sostener el formato,
que es un fallo distinto de una mala respuesta. Este script separa ambos: reporta por
caso si el texto cumple el contrato exacto `BEHAVIOR / ANSWER / CITATIONS`, y si la
conducta declarada corresponde al caso.

Sirve como barrera previa: un modelo que no cumple el contrato no puede entrar en las
métricas de generación, porque su fallo mediría capacidad de seguir instrucciones y no
calidad de respuesta.
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.request

SYSTEM = (
    "You are an educational assistant in a controlled RAG experiment. "
    "Use only the supplied contexts; do not use outside knowledge. "
    "If the contexts support the question, answer concisely and cite the supporting chunk IDs. "
    "If the question contains a false premise that the contexts contradict, correct the premise and cite the contradiction evidence. "
    "If the contexts are insufficient, answer exactly 'I cannot answer from the supplied contexts.' and use no citations. "
    "Citations must be exact chunk IDs from the supplied contexts. "
    "Use exactly three fields and no other text: "
    "'BEHAVIOR: answer OR grounded_correction OR abstain', then "
    "'ANSWER: one concise answer', then "
    "'CITATIONS: comma-separated chunk IDs, or NONE'."
)

CASOS = [
    # Los identificadores son los reales del corpus: `fichero:sección:chunk-nnn`. Una sonda
    # con identificadores cortos daría falsos positivos, porque el fallo observado en modelos
    # pequeños consiste precisamente en recortar la referencia al sufijo final.
    ("ordinaria", "answer",
     "How does increasing the sample size affect the sampling distribution of the sample mean?",
     "[openstax_intro_stats_2e:7.1:chunk-003]\nStandard deviation is the square root of variance, so the standard deviation of the "
     "sampling distribution is the standard deviation of the original distribution divided by the square root of n. The variable n is the "
     "number of values that are averaged together, not the number of times the experiment is done.\n\nTo put it more formally, if you draw "
     "random samples of size n, the distribution of the random variable  , which consists of sample means, is called the sampling "
     "distribution of the mean. The sampling distribution of the mean approaches a normal distribution as n, the sample size, increases."),
    ("premisa_falsa", "grounded_correction",
     "Why does increasing the confidence level make the confidence interval narrower when all other inputs are fixed?",
     "[openstax_intro_stats_2e:8.1:chunk-011]\nSummary: Effect of Changing the Confidence Level\n\n• Increasing the confidence level "
     "increases the error bound, making the confidence interval wider.\n• Decreasing the confidence level decreases the error bound, "
     "making the confidence interval narrower."),
    ("no_respondible", "abstain",
     "What is the boiling point of water on the surface of Mars?",
     "[openstax_principles_ds:4.1:chunk-016]\nThe mean of a dataset is computed by adding all values and dividing by the count."),
]

PAT = re.compile(r"\s*BEHAVIOR:\s*(answer|grounded_correction|abstain)\s*\n"
                 r"ANSWER:\s*(.*?)\s+CITATIONS:\s*(.*?)\s*", re.DOTALL)


def call(model: str, question: str, context: str, num_ctx: int | None = None) -> str:
    """Consulta Ollama con el contrato de respuesta y el contexto de la sonda."""
    user = f"Question:\n{question}\n\nSupplied contexts:\n{context}"
    options: dict = {"temperature": 0.0}
    if num_ctx:
        options["num_ctx"] = num_ctx
    body = json.dumps({"model": model, "stream": False, "options": options,
                       "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]}).encode()
    req = urllib.request.Request("http://127.0.0.1:11434/api/chat", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as r:
        return json.load(r)["message"]["content"]


def main() -> int:
    """Prueba el formato y la conducta declarada de cada modelo en los casos de control."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--models", default="qwen3.5:2b,qwen3.5:4b,qwen3.5:9b")
    ap.add_argument("--num-ctx", type=int, default=None,
                    help="Techo de contexto. Sin él, Ollama usa el suyo (4096), que se queda corto "
                         "en los casos con varios fragmentos largos.")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    filas = []
    for model in args.models.split(","):
        ok = 0
        print(f"=== {model} ===")
        for etiqueta, esperado, q, ctx in CASOS:
            try:
                txt = call(model, q, ctx, args.num_ctx)
            except Exception as exc:  # noqa: BLE001
                print(f"   ❌ {etiqueta:14s} → error: {exc!r}")
                filas.append(dict(model=model, caso=etiqueta, contrato=False, esperado=esperado, error=repr(exc)[:200]))
                continue
            m = PAT.fullmatch(txt)
            if m:
                ok += 1
                conducta = m.group(1)
                citas = [c.strip() for c in m.group(3).split(",") if c.strip() and c.strip().upper() != "NONE"]
                exactas = all(c.startswith("openstax_") and ":chunk-" in c for c in citas)
                aviso = []
                if conducta != esperado:
                    aviso.append("conducta distinta")
                if citas and not exactas:
                    aviso.append("citas: " + " | ".join(citas))
                marca = ("  ⚠ " + "; ".join(aviso)) if aviso else ""
                print(f"   ✅ {etiqueta:14s} → {conducta:21s} (esperado {esperado}){marca}")
                filas.append(dict(model=model, caso=etiqueta, contrato=True, conducta=conducta,
                                  esperado=esperado, coincide=conducta == esperado, citas=citas,
                                  citas_exactas=exactas))
            else:
                print(f"   ❌ {etiqueta:14s} → contrato ROTO, salida: {txt[:110]!r}")
                filas.append(dict(model=model, caso=etiqueta, contrato=False, esperado=esperado, salida=txt[:300]))
        print(f"   → {ok}/{len(CASOS)} cumplen el contrato\n")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            for f in filas:
                fh.write(json.dumps(f, ensure_ascii=False) + "\n")
        print(f"registro: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
