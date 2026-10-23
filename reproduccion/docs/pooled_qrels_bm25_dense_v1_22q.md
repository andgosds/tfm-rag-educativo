> **Recetas desde la raíz del paquete v2.** Los resultados descritos son históricos. Para operaciones de escritura usar destinos nuevos bajo `outputs/local_runs/`; los defaults congelados se rechazan. Recetas vigentes seguras: `standalone_operations.md`. No ejecutar inferencia mientras siga abierta la adjudicación.

# Qrels pooled y reevaluación BM25–dense

## Alcance

Esta fase amplía los qrels a partir de la adjudicación cerrada del pool BM25+dense y vuelve a evaluar ambos recuperadores con el mismo conjunto de relevancia. No modifica el corpus, las 22 preguntas, el texto indexado, los rankings top-10 ni los parámetros de los métodos.

Los 24 qrels originales se conservan sin cambios en `qrels_golden_set_v1_22q.tsv`. El constructor genera un archivo nuevo, `qrels_golden_set_pooled_v1_22q.tsv`, y una matriz JSONL de procedencia y canonicidad.

## Construcción de los qrels

El script `build_pooled_qrels.py` combina los qrels originales con las 109 decisiones adjudicadas mediante `three_judge_risk_directed_v1`. Los grados 1 y 2 se incorporan como qrels positivos; los 14 grados 0 permanecen auditados en el informe, pero no se escriben en el TSV. Precision, Recall y MRR consideran relevante únicamente el grado 2; nDCG mantiene la escala 0/1/2.

| Componente | Cantidad |
|---|---:|
| Qrels originales | 24 |
| Qrels añadidos | 95 |
| Decisiones de grado 0 auditadas | 14 |
| Qrels pooled | 119 |
| Grado 1 | 47 |
| Grado 2 | 72 |
| Evidencias canónicas | 33 |
| QID con algún qrel positivo | 20 |

La matriz de procedencia conserva 17 evidencias canónicas del golden set original y 16 incorporadas durante la adjudicación del pool. Los hashes principales son:

```text
qrels pooled:
6a5cf811fd15ddf07a6b7fb39932c6917b99f781b450b950593cafc6cc0ad871

procedencia:
29cf387b1618ea4b1fc3fbd3b60777eadce4121d4bd8afa66e8e1b5d3faf4fd7
```

## Resolución de las premisas falsas

Seis qrels de grado 2 pertenecen a preguntas etiquetadas como no respondibles: tres en q-v1-008 y tres en q-v1-020. Ambas contienen una premisa falsa. La revisión independiente mantuvo su etiqueta de respondibilidad y clasificó los seis chunks como evidencia de contradicción mediante `answerability_resolutions_v1_22q.json`.

En estos casos, el comportamiento correcto consiste en rechazar la premisa y ofrecer una corrección fundamentada. Esto se distingue tanto de responder como si la premisa fuera verdadera como de abstenerse por falta de evidencia. Las nueve preguntas no respondibles permanecen en los runs para el análisis posterior y se excluyen de los agregados ordinarios de retrieval. La evaluación comparativa continúa utilizando las mismas 13 preguntas respondibles con qrels de grado 2.

## Resultados con qrels pooled

| Métrica | BM25 @5 | Dense @5 | BM25 @10 | Dense @10 |
|---|---:|---:|---:|---:|
| Precision | 0,4769 | 0,6154 | 0,3923 | 0,3923 |
| Recall | 0,5128 | 0,6635 | 0,8077 | 0,8301 |
| MRR | 0,7885 | 0,7436 | 0,7885 | 0,7436 |
| nDCG | 0,5907 | 0,7155 | 0,7052 | 0,7491 |

Dense obtiene mayor Precision, Recall y nDCG en top-5. En top-10 mantiene una ventaja pequeña en Recall y nDCG, mientras Precision empata. BM25 sitúa antes la primera evidencia relevante y obtiene mayor MRR en ambos cortes. El patrón no permite declarar un ganador general: dense reúne más evidencia y la ordena mejor en conjunto, mientras BM25 presenta una ventaja en primer acierto.

## Cambio respecto a los qrels originales

| Métrica | Δ BM25 @5 | Δ Dense @5 | Δ BM25 @10 | Δ Dense @10 |
|---|---:|---:|---:|---:|
| Precision | +0,3231 | +0,4462 | +0,2615 | +0,2692 |
| Recall | +0,0513 | +0,0737 | −0,0513 | +0,0096 |
| MRR | +0,4551 | +0,2436 | +0,3846 | +0,2131 |
| nDCG | +0,2499 | +0,2482 | +0,2137 | +0,1983 |

Estos cambios no representan una mejora de los recuperadores: sus rankings son los mismos. Reflejan que muchos candidatos antes tratados como no juzgados ahora tienen una etiqueta. La caída de Recall@10 de BM25 también es informativa: el denominador crece con qrels de grado 2 aportados por dense que BM25 no recupera en su top-10.

## Cobertura completa de evidencia

| Método | Consultas completas @5 | Consultas completas @10 |
|---|---:|---:|
| BM25 | 0/13 | 5/13 |
| Dense | 3/13 | 6/13 |

La cobertura completa exige recuperar todos los qrels de grado 2 de una pregunta dentro del corte. Dense mejora este diagnóstico, pero ninguno de los métodos resuelve la evidencia distribuida de forma general. Esta limitación mantiene justificada la siguiente fase híbrida.

## Amenazas a la validez

El pool se construyó con la unión top-10 de los mismos BM25 y dense que se evalúan. Por ello reduce el sesgo de usar qrels iniciales incompletos y permite una comparación común entre ambos, pero no constituye una evaluación exhaustiva ni independiente. Los resultados absolutos pueden favorecer a los sistemas que contribuyeron candidatos al pool y no deben extrapolarse a otros recuperadores sin ampliar nuevamente los juicios.

La adjudicación tampoco equivale a 109 anotaciones humanas independientes. Conserva 23 decisiones directas del usuario, 70 decisiones delegadas al asistente bajo criterios explícitos y 16 discrepancias fuertes resueltas con consejo del usuario. Los tres jueces automáticos se utilizaron solo para priorizar la revisión.

## Reproducción

Desde la raíz del proyecto:

```bash
uv run python scripts/build_pooled_qrels.py

uv run python scripts/run_bm25.py \
  --run-id bm25_pooled_v1_22q \
  --qrels-input data/golden/qrels_golden_set_pooled_v1_22q.tsv

uv run --project environments/dense \
  python scripts/run_dense.py \
  --run-id dense_e5_base_v2_pooled_v1_22q \
  --qrels-input data/golden/qrels_golden_set_pooled_v1_22q.tsv

uv run python scripts/compare_pooled_retrieval.py
```

El comparador guarda métricas, deltas y cobertura completa en `retrieval_comparison_bm25_dense_pooled_22q.json`.
