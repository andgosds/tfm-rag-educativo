#!/usr/bin/env python3
"""Construye los registros de anotación de la ampliación v3 del golden set.

Las citas se extraen por corte sobre el texto real del chunk (`text.index`), nunca
transcritas a mano: el texto de los chunks acumula espacios antes de salto de línea y
una cita tecleada no casa. Si un ancla no aparece, el script falla en vez de emitir
una cita aproximada.

Uso:
    python scripts/build_expansion_v3_golden.py \
        --chunks data/processed/chunks_v1.jsonl \
        --output data/golden/expansion_v3/golden_set_v3_draft.jsonl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

SCHEMA_VERSION = "golden_set_v1"
CORPUS_VERSION = "corpus_v1"
CHUNKING = "section_paragraphs_300w_overlap60_v1"

# chunk_id, inicio_del_corte, final_del_corte, grado, canónico, papel, aporta
EVIDENCE = {
    "q-v3-001": [
        (
            "openstax_intro_stats_2e:7.intro:chunk-002",
            "The size of the sample, n, that is required",
            "behaves in a predictable way is a powerful tool.",
            2,
            True,
            "contradiction",
            "Refuta la premisa: los datos se comportan de forma predecible aunque su distribución no sea "
            "normal, y una población lejana de la normalidad solo exige más observaciones.",
        ),
    ],
    "q-v3-002": [
        (
            "openstax_intro_stats_2e:6.1:chunk-006",
            "The Empirical Rule",
            "The empirical rule is also known as the 68-95-99.7 rule.",
            2,
            True,
            "contradiction",
            "Refuta la premisa con la regla empírica: 68% en ±1σ y 95% en ±2σ, no 95% en ±1σ.",
        ),
    ],
    "q-v3-003": [
        (
            "openstax_intro_stats_2e:8.2:chunk-001",
            "Calculating the Sample Size n",
            "Therefore, 217 Foothill College students should be surveyed",
            2,
            True,
            "answer",
            "Tamaño muestral para una media: se despeja n de la fórmula del error bound, interviene la "
            "desviación típica poblacional y el resultado se redondea al alza.",
        ),
        (
            "openstax_intro_stats_2e:8.3:chunk-010",
            "Calculating the Sample Size n",
            "Suppose a mobile phone company wants to determine the current percentage",
            2,
            True,
            "answer",
            "Tamaño muestral para una proporción: epígraje homónimo en otra sección, con la fórmula del error "
            "bound de la proporción despejada para n. No contiene la fórmula de la media.",
        ),
        (
            "openstax_intro_stats_2e:8.3:chunk-011",
            "However, in order to find n, we need to know the estimated (sample) proportion",
            "This gives us a large enough sample so that we can be 90% confident",
            2,
            True,
            "answer",
            "El matiz que no está en el lado de la media: sin estimación previa se fijan p′ y q′ en 0,5 por "
            "ser el producto máximo, lo que maximiza n.",
        ),
    ],
    "q-v3-004": [
        (
            "openstax_principles_ds:4.3:chunk-012",
            "Method of Least Squares and Residuals",
            "The slope measures the steepness of the line, and the y-intercept",
            2,
            True,
            "answer",
            "Criterio de ajuste por mínimos cuadrados y significado de pendiente y ordenada.",
        ),
        (
            "openstax_principles_ds:4.3:chunk-013",
            "In this format,",
            "we can use a regression line to predict",
            2,
            True,
            "answer",
            "Notación del modelo, y-hat como valor predicho, signo de la pendiente, y la secuencia del "
            "análisis con la condición para trazar la recta: que una variable ayude a explicar o predecir "
            "la otra. Una sola cita por fragmento.",
        ),
        (
            "openstax_principles_ds:4.3:chunk-014",
            "As an example of a regression equation",
            "the company determines the regression equation is of the form",
            2,
            True,
            "answer",
            "La ecuación de regresión trabajada sobre un caso concreto, que muestra cómo se usa la recta "
            "ajustada para predecir.",
        ),
    ],
    "q-v3-005": [
        (
            "openstax_intro_stats_2e:8.1:chunk-002",
            "The margin of error (EBM) depends on the confidence level",
            "Mathematically, α + CL = 1.",
            2,
            True,
            "answer",
            "Definición del nivel de confianza, su lectura más precisa y su relación con α.",
        ),
    ],
    "q-v3-006": [],
    "q-v3-007": [
        (
            "openstax_intro_stats_2e:9.2:chunk-001",
            "The four possible outcomes in the table are:",
            "The Power of the Test is 1 – β",
            1,
            False,
            "context",
            "Define la potencia como la probabilidad de rechazar una hipótesis nula falsa, pero no cuantifica "
            "cómo cambia con el tamaño muestral. Aporta contexto, no respuesta.",
        ),
    ],
    "q-v3-008": [
        (
            "openstax_principles_ds:3.5:chunk-002",
            "Overview of Probability Distributions",
            "Continuous random variable",
            2,
            True,
            "answer",
            "Define variable aleatoria y distingue los casos discreto y continuo: el punto de partida de la "
            "cadena.",
        ),
        (
            "openstax_intro_stats_2e:7.1:chunk-003",
            "To put it more formally, if you draw random samples of size n",
            "The sampling distribution of the mean approaches a",
            2,
            True,
            "answer",
            "Define la distribución de muestreo de la media y su convergencia: el otro extremo de la cadena. "
            "Pertenece a un manual distinto, de ahí la síntesis transversal.",
        ),
    ],
}

RECORDS = [
    {
        "qid": "q-v3-001",
        "question": (
            "Is it true that the Central Limit Theorem can only be applied when the population from which "
            "the samples are drawn follows a normal distribution?"
        ),
        "question_type": "factual",
        "answerability": "unanswerable",
        "unanswerable_category": "false_premise",
        "gold_answer": None,
        "evidence_sufficient": False,
        "notes": (
            "Premisa falsa: el corpus la refuta. Se espera corrección con base en lugar de una explicación "
            "inventada. La corrección de referencia vive en el sidecar de resolución, no aquí."
        ),
    },
    {
        "qid": "q-v3-002",
        "question": (
            "Is it true that about 95% of the values of a normally distributed variable lie within one "
            "standard deviation of the mean?"
        ),
        "question_type": "factual",
        "answerability": "unanswerable",
        "unanswerable_category": "false_premise",
        "gold_answer": None,
        "evidence_sufficient": False,
        "notes": (
            "Premisa falsa: la regla empírica del corpus da 68% en ±1σ. Se espera corrección con base. "
            "Corrección de referencia en el sidecar de resolución."
        ),
    },
    {
        "qid": "q-v3-003",
        "question": (
            "How is the required sample size determined when a study must estimate a population mean "
            "within a given error bound, and how does the calculation differ when it must estimate a "
            "population proportion?"
        ),
        "question_type": "comparative",
        "answerability": "answerable",
        "unanswerable_category": None,
        "gold_answer": (
            "In both cases the required sample size is obtained by solving the error bound formula for n, "
            "and in both it depends on the desired error bound and on the z-score for the chosen confidence "
            "level. What differs is the measure of variability that enters the calculation. For a mean the "
            "formula uses the population standard deviation, so a planning study needs a value for it, and "
            "the result is rounded up to the next higher integer to make sure the sample is large enough. "
            "For a proportion the formula uses the product of the estimated proportion and its complement, "
            "and when no prior estimate exists both are set to 0.5, because that product is the largest "
            "possible and therefore yields the largest, safest sample size."
        ),
        "evidence_sufficient": True,
        "notes": (
            "Multichunk por construcción: las dos secciones tienen un epígraje homónimo, 'Calculating the "
            "Sample Size n', cada una con su fórmula y ninguna con la del otro caso. Sustituye a la "
            "formulación anterior, que comparaba los márgenes de error y resultó no ser multichunk porque "
            "8.3:chunk-003 ya contenía el contraste entre ambas desviaciones apropiadas."
        ),
    },
    {
        "qid": "q-v3-004",
        "question": (
            "How is a straight-line regression model fitted to a scatterplot and used for prediction, and "
            "what do its slope and intercept represent?"
        ),
        "question_type": "procedural",
        "answerability": "answerable",
        "unanswerable_category": None,
        "gold_answer": (
            "The analysis starts with the scatterplot and the correlation coefficient, and the line is only "
            "calculated when one variable helps to explain or predict the other. The model is fitted with the "
            "least squares method, which minimizes the squared distances from the data points to the fitted "
            "line, and it uses all the points rather than two. The slope measures the steepness of the line "
            "and is positive when the line rises to the right and negative when it falls; the intercept is "
            "where the graph crosses the vertical axis. The predicted value of the dependent variable is "
            "written with a hat over the variable and is obtained from the fitted equation for a given value "
            "of the independent variable."
        ),
        "evidence_sufficient": True,
        "notes": "Multichunk: criterio de ajuste, notación del modelo y condición de predicción viven en fragmentos distintos.",
    },
    {
        "qid": "q-v3-005",
        "question": "What does the confidence level of an interval estimate represent?",
        "question_type": "factual",
        "answerability": "answerable",
        "unanswerable_category": None,
        "gold_answer": (
            "It is often taken as the probability that the calculated interval contains the true population "
            "parameter, but the more accurate statement is that it is the percentage of confidence intervals "
            "that contain the true parameter when repeated samples are taken. Its complement is alpha, the "
            "probability that the interval does not contain the parameter, so the two add up to one."
        ),
        "evidence_sufficient": True,
        "notes": (
            "Diseñada como redundante: la misma idea se reformula en 34 chunks de ocho secciones y dos "
            "manuales. El conjunto canónico se mantiene mínimo a propósito, para exponer que Recall@k no "
            "mide diversidad cuando el pool contiene reescrituras."
        ),
    },
    {
        "qid": "q-v3-006",
        "question": (
            "How is a logistic regression model fitted to a binary outcome, and how are its coefficients "
            "interpreted?"
        ),
        "question_type": "procedural",
        "answerability": "unanswerable",
        "unanswerable_category": "out_of_scope",
        "gold_answer": None,
        "evidence_sufficient": False,
        "notes": (
            "Fuera de alcance: 0 menciones de 'logistic' en los 288 chunks, verificado por cómputo. La "
            "regresión lineal sí está cubierta, de modo que el negativo es plausible y de dominio cercano. "
            "Se espera abstención, sin evidencia de contradicción."
        ),
    },
    {
        "qid": "q-v3-007",
        "question": (
            "By how much does the power of a test increase when the sample size doubles at a fixed "
            "significance level?"
        ),
        "question_type": "procedural",
        "answerability": "unanswerable",
        "unanswerable_category": "insufficient_evidence",
        "gold_answer": None,
        "evidence_sufficient": False,
        "notes": (
            "Evidencia insuficiente: el corpus define la potencia pero no la relaciona cuantitativamente con "
            "el tamaño muestral. El fragmento anotado aporta contexto, no respuesta, y por eso va a grado 1 "
            "sin canonicidad."
        ),
    },
    {
        "qid": "q-v3-008",
        "question": (
            "How do discrete and continuous probability distributions relate to the sampling distributions "
            "used in statistical inference?"
        ),
        "question_type": "explanatory",
        "answerability": "answerable",
        "unanswerable_category": None,
        "gold_answer": (
            "Probability distributions describe the probabilities of the values of a single random variable, "
            "which is either discrete, with a finite or countable number of values and typically the result "
            "of a count, or continuous, taking any value in an interval. A sampling distribution is built on "
            "top of that object: it is the distribution of a statistic computed from repeated samples, and "
            "for the mean it approaches a normal distribution as the sample size increases. The second "
            "object is therefore a distribution over the values of the first, and that is what allows "
            "inference about the population."
        ),
        "evidence_sufficient": True,
        "notes": (
            "Transversal entre manuales: los dos fragmentos canónicos pertenecen a openstax_principles_ds y "
            "a openstax_intro_stats_2e. Ninguno basta por sí solo para cerrar la cadena."
        ),
    },
]

CORRECTIVE = [
    {
        "qid": "q-v3-001",
        "expected_response_behavior": "grounded_correction",
        "unanswerable_category": "false_premise",
        "corrective_reference": (
            "The premise does not hold. The source states that the data behave in a predictable way even "
            "when their distribution is not normal, which is exactly what it presents as the importance of "
            "the theorem. A population far from normal does not prevent its application: it only means that "
            "more observations are needed for the sample means or sums to become normal. What the theorem "
            "requires is a sample large enough —at least 30, or data from a normal distribution— and "
            "sampling with replacement."
        ),
        "contradiction_chunks": ["openstax_intro_stats_2e:7.intro:chunk-002"],
    },
    {
        "qid": "q-v3-002",
        "expected_response_behavior": "grounded_correction",
        "unanswerable_category": "false_premise",
        "corrective_reference": (
            "The premise does not hold. For a normally distributed variable about 68% of the values lie "
            "within one standard deviation of the mean. The 95% figure corresponds to within two standard "
            "deviations, and 99.7% to within three."
        ),
        "contradiction_chunks": ["openstax_intro_stats_2e:6.1:chunk-006"],
    },
    {
        "qid": "q-v3-006",
        "expected_response_behavior": "abstain",
        "unanswerable_category": "out_of_scope",
        "corrective_reference": None,
        "contradiction_chunks": [],
    },
    {
        "qid": "q-v3-007",
        "expected_response_behavior": "abstain",
        "unanswerable_category": "insufficient_evidence",
        "corrective_reference": None,
        "contradiction_chunks": [],
    },
]


def _norm_with_map(text: str) -> tuple[str, list[int]]:
    """Vista normalizada en espacios y mapa de cada carácter a su offset original.

    El texto de los chunks acumula saltos de línea y espacios dobles antes de
    salto que la transcripción de un ancla no reproduce. Normalizar permite
    encontrar el ancla; conservar el mapa permite devolver un corte literal.
    """
    out: list[str] = []
    pos: list[int] = []
    prev_space = True
    for i, ch in enumerate(text):
        if ch.isspace():
            if not prev_space:
                out.append(" ")
                pos.append(i)
            prev_space = True
        else:
            out.append(ch)
            pos.append(i)
            prev_space = False
    if out and out[-1] == " ":
        out.pop()
        pos.pop()
    return "".join(out), pos


def slice_quote(text: str, start: str, end: str) -> str:
    """Extrae la cita literal por corte sobre el texto real del chunk.

    La localización se hace sobre una vista normalizada en espacios; el corte se
    hace sobre el texto original, de modo que la cita resultante es literal y
    casa con el chunk sin normalizar. Si el ancla no aparece, falla.
    """
    norm, pos = _norm_with_map(text)
    ns, _ = _norm_with_map(start)
    ne, _ = _norm_with_map(end)
    i = norm.index(ns)
    j = norm.index(ne, i) + len(ne) - 1
    return text[pos[i] : pos[j] + 1]


def main() -> int:
    """Construye los registros de ampliación y sus resoluciones con citas literales del corpus."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--chunks", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    chunks = {
        r["chunk_id"]: r
        for r in (
            json.loads(line)
            for line in args.chunks.read_text().splitlines()
            if line.strip()
        )
    }

    out_rows = []
    sidecar_rows = {r["qid"]: dict(r) for r in CORRECTIVE}
    for rec in RECORDS:
        unanswerable = rec["answerability"] != "answerable"
        evidence = []
        for chunk_id, start, end, grade, canonical, role, supports in EVIDENCE[rec["qid"]]:
            text = chunks[chunk_id]["text"]
            quote = slice_quote(text, start, end)
            item = {
                "chunk_id": chunk_id,
                "relevance_grade": grade,
                "is_canonical": canonical,
                "role": role,
                "quote": quote,
                "supports": supports,
                "source_verified": True,
                "verification_note": "Extraída por corte sobre el texto del chunk; no transcrita.",
            }
            # El contrato exige que un registro no respondible quede con evidence
            # vacío: la evidencia de contradicción o de contexto se preserva en el
            # sidecar de resolución, nunca como soporte de respuesta.
            if unanswerable:
                sidecar_rows[rec["qid"]].setdefault("evidence", []).append(item)
            else:
                evidence.append(item)
        row = {
            "schema_version": SCHEMA_VERSION,
            "corpus_version": CORPUS_VERSION,
            "chunking_method": CHUNKING,
            "qid": rec["qid"],
            "question": rec["question"],
            "question_language": "en",
            "question_type": rec["question_type"],
            "answerability": rec["answerability"],
            "unanswerable_category": rec["unanswerable_category"],
            "gold_answer": rec["gold_answer"],
            "answer_language": None if unanswerable else "en",
            "evidence_sufficient": rec["evidence_sufficient"],
            "evidence": evidence,
            "notes": rec["notes"],
            "question_origin": "llm_assisted",
            "annotator_id": "hermes-agent",
            "reviews": [],
            "human_adjudication": None,
            "annotation_status": "draft",
        }
        out_rows.append(row)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in out_rows) + "\n"
    )

    sidecar = args.output.with_name(args.output.stem + "_resolutions.jsonl")
    sidecar.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in sidecar_rows.values()) + "\n"
    )

    n_canon = sum(1 for r in out_rows for e in r["evidence"] if e["is_canonical"])
    print(f"registros: {len(out_rows)}")
    print(f"evidencia: {sum(len(r['evidence']) for r in out_rows)} citas, {n_canon} canónicas")
    print(f"sin evidencia: {[r['qid'] for r in out_rows if not r['evidence']]}")
    print(f"salida: {args.output}")
    print(f"sidecar de resolución: {sidecar}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
