# Informe reproducible — experimento FINAL

## Reproducción offline

Desde la raíz v2, con uv y el entorno ya sincronizado:

```sh
uv run --no-sync python scripts/analyze_final_experiment.py --output-dir outputs/local_runs/final_experiment_20260930/analysis
uv run --no-sync python scripts/analyze_final_experiment.py --output-dir outputs/local_runs/final_experiment_20260930/verificationsecond
uv run --no-sync pytest tests/test_final_experiment.py -q
```

Cada destino debe ser nuevo. No se permiten destinos externos, históricos ni sobrescrituras. La segunda ejecución conserva nombres y hashes sin rutas absolutas, reloj o metadatos volátiles. hash_manifest.json contiene hashes SHA-256 de cada fuente y de cada salida excepto sí mismo. La comparación byte-exacta cubre también el manifiesto.

Python registrado: 3.14.0. Bootstrap: 5000 réplicas; random.Random(20260928) reiniciado por contraste, IC percentil en índices floor(0,025B), floor(0,975B), diferencias de medias por base. Semilla y algoritmo reutilizados sin modificar analysis_capacity_v3.py.

Fuentes activas: solo doce archivos rag_<estrategia>_top5_<generador>.jsonl de los tres generadores elegibles, sus ledgers de fallos y eval_final_v3.jsonl. Se excluyen modelos no elegibles, evaluaciones invalidada/diagnóstica, piloto y exploración. El pre-registro, las decisiones y las fuentes permanecen congelados.

## Comparación final de recuperadores dentro de cada generador

La campaña final es la evidencia empírica principal. Se comparan bm25, dense, rrf y rerank dentro de cada generador; no se combinan sus puntuaciones ni se toma el piloto como ancla de la recomendación. El piloto y la exploración quedan como material suplementario separado.

Se cerraron 624 unidades previstas: 604 respuestas aceptadas y 20 fallos de contrato. La evaluación final cubre todas las aceptadas. Las puntuaciones consolidadas combinan consenso entre jueces y decisiones humanas sobre las discrepancias, no una revisión humana exhaustiva ni métricas RAGAS estándar. Los fallos no se convierten en ceros de calidad.

Para cada generador y criterio se intersectan las formulaciones disponibles y numéricas de las cuatro estrategias antes de agregar. Cada pregunta base aporta la media de sus formulaciones retenidas; la media final asigna el mismo peso a cada base. Puede quedar una sola formulación de una base. Fundamentación y corrección incluyen solo tareas esperadas answer o grounded_correction; conducta y citas incluyen todas las tareas. Los soportes son específicos del generador y criterio, por lo que los niveles no establecen una comparación directa entre generadores.

| Modelo | Método | Fundamentación | Corrección | Conducta | Citas |
|---|---|---:|---:|---:|---:|
| Gemma | bm25 | 1,806 (34) | 1,500 (33) | 1,568 (41) | 0,955 (41) |
| Gemma | dense | 1,833 (34) | 1,583 (33) | 1,591 (41) | 0,932 (41) |
| Gemma | rrf | 1,750 (34) | 1,556 (33) | 1,591 (41) | 1,000 (41) |
| Gemma | rerank | 1,861 (34) | 1,472 (33) | 1,500 (41) | 0,932 (41) |
| Qwen4 | bm25 | 1,523 (44) | 1,591 (43) | 1,615 (52) | 0,904 (52) |
| Qwen4 | dense | 1,773 (44) | 1,614 (43) | 1,577 (52) | 0,904 (52) |
| Qwen4 | rrf | 1,773 (44) | 1,636 (43) | 1,712 (52) | 0,904 (52) |
| Qwen4 | rerank | 1,932 (44) | 1,682 (43) | 1,692 (52) | 0,904 (52) |
| Qwen9 | bm25 | 1,886 (44) | 1,568 (43) | 1,673 (52) | 0,981 (52) |
| Qwen9 | dense | 1,795 (44) | 1,614 (43) | 1,750 (52) | 0,962 (52) |
| Qwen9 | rrf | 1,977 (44) | 1,705 (43) | 1,750 (52) | 0,981 (52) |
| Qwen9 | rerank | 1,932 (44) | 1,727 (43) | 1,788 (52) | 0,942 (52) |

: Calidad final sobre soporte común de las cuatro estrategias: media macro por pregunta base (n_cells por estrategia). {#tbl-final-recuperadores}

Nota: fundamentación, corrección y conducta tienen escala 0–2; citas, 0–1. Los paréntesis cuentan formulaciones por estrategia, no unidades independientes. Los denominadores por criterio (n_cells / n_base) son:
- Gemma: fundamentación 34 / 18; corrección 33 / 18; conducta 41 / 22; citas 41 / 22.
- Qwen4: fundamentación 44 / 22; corrección 43 / 22; conducta 52 / 26; citas 52 / 26.
- Qwen9: fundamentación 44 / 22; corrección 43 / 22; conducta 52 / 26; citas 52 / 26.

### Lectura descriptiva y recomendación condicionada

- Gemma, máximos observados: fundamentación: rerank (1,861); corrección: dense (1,583); conducta: dense, rrf (1,591); citas: rrf (1,000).
- Qwen4, máximos observados: fundamentación: rerank (1,932); corrección: rerank (1,682); conducta: rrf (1,712); citas: bm25, dense, rrf, rerank (0,904).
- Qwen9, máximos observados: fundamentación: rrf (1,977); corrección: rerank (1,727); conducta: rerank (1,788); citas: bm25, rrf (0,981).

Con Gemma, dense ofrece el máximo descriptivo de corrección, mientras rerank lo ofrece en fundamentación y rrf en citas: no se optimizan a la vez. Con Qwen4, rerank es una opción si la prioridad es el contenido (fundamentación y corrección), pero rrf conserva el mayor nivel de conducta. Con Qwen9, rrf es una opción si se prioriza fundamentación y citas; rerank si se prioriza corrección y conducta, con una menor puntuación de citas. Estas son recomendaciones condicionadas al experimento final, no al piloto, y no una demostración de superioridad.

Estos máximos son descriptivos, no pruebas de superioridad estadística. La recomendación debe condicionarse al generador y al criterio prioritario, sin construir un índice compuesto ni decidir pesos después de observar los resultados. No hay base para declarar un ganador universal a partir de un único máximo. Los seis contrastes por generador y criterio se publican sin seleccionar extremos: diferencia destino − origen, primero por formulación y después por base. Los IC percentiles del 95 % usan 5000 réplicas y semilla 20260928; son intervalos puntuales post-hoc/descriptivos, no ajustados por multiplicidad. No acreditan superioridad familiar y un intervalo que contiene cero no demuestra equivalencia.

### Tiempo y tokens registrados en la generación final

| Modelo | Método | Latencia (s) | Prompt (tokens) | Completion (tokens) | Aceptadas | Fallidas |
|---|---|---:|---:|---:|---:|---:|
| Gemma | bm25 | 2,810 | 2405,9 | 126,3 | 48 | 4 |
| Gemma | dense | 3,135 | 2491,1 | 153,4 | 49 | 3 |
| Gemma | rrf | 2,985 | 2436,4 | 141,9 | 44 | 8 |
| Gemma | rerank | 2,974 | 2415,0 | 138,0 | 47 | 5 |
| Qwen4 | bm25 | 2,731 | 2391,6 | 97,9 | 52 | 0 |
| Qwen4 | dense | 2,537 | 2398,4 | 86,9 | 52 | 0 |
| Qwen4 | rrf | 2,556 | 2369,7 | 94,9 | 52 | 0 |
| Qwen4 | rerank | 2,632 | 2507,4 | 98,3 | 52 | 0 |
| Qwen9 | bm25 | 3,906 | 2343,6 | 88,1 | 52 | 0 |
| Qwen9 | dense | 3,867 | 2306,2 | 96,2 | 52 | 0 |
| Qwen9 | rrf | 3,841 | 2322,4 | 93,9 | 52 | 0 |
| Qwen9 | rerank | 3,945 | 2363,1 | 96,9 | 52 | 0 |

: Descriptivos operacionales de generación final: medias aritméticas de unidades aceptadas y cobertura de fallos separada. {#tbl-final-operacion}

Nota: los denominadores de las tres medias son las aceptadas de cada fila; su disponibilidad se conserva en el CSV. Son observaciones de la campaña, no un benchmark controlado ni mediciones de latencia end-to-end del RAG. Proceden de generation_latency_ms / 1000, prompt_tokens y completion_tokens de los doce JSONL finales. Son totales registrados acumulados sobre los intentos de la unidad, no solo el último intento. Los costes de recuperación, evaluación, energía y amortización no están medidos; no se estima coste monetario. Las diferencias pueden reflejar longitud de respuesta, contexto, reintentos, carga y orden de ejecución, además del generador. Los fallos, sus tiempos y tokens se publican por separado en operational_summary.csv. Las aceptadas no conservan un desglose numérico por intento, de modo que sus acumulados no pueden reconstruirse de forma independiente a partir del texto bruto. Los fallos sí conservan attempt_usage; solo se recuperan totales ausentes si ese ledger está completo.

El estudio evalúa fiabilidad informacional bajo este corpus, conjunto de preguntas y contrato, no efectividad pedagógica. El replay offline reproduce el análisis, no otra campaña de inferencia.


## Auditoría de cobertura y disponibilidad

| Modelo | Método | Previstas | Aceptadas | Fallidas | Faith num. | Factual num. | Conducta num. | Citas num. |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Gemma | bm25 | 52 | 48 | 4 | 48 | 48 | 48 | 48 |
| Gemma | dense | 52 | 49 | 3 | 49 | 48 | 49 | 49 |
| Gemma | rrf | 52 | 44 | 8 | 44 | 43 | 44 | 44 |
| Gemma | rerank | 52 | 47 | 5 | 47 | 47 | 47 | 47 |
| Qwen4 | bm25 | 52 | 52 | 0 | 52 | 51 | 52 | 52 |
| Qwen4 | dense | 52 | 52 | 0 | 52 | 52 | 52 | 52 |
| Qwen4 | rrf | 52 | 52 | 0 | 52 | 52 | 52 | 52 |
| Qwen4 | rerank | 52 | 52 | 0 | 52 | 52 | 52 | 52 |
| Qwen9 | bm25 | 52 | 52 | 0 | 52 | 52 | 52 | 52 |
| Qwen9 | dense | 52 | 52 | 0 | 52 | 52 | 52 | 52 |
| Qwen9 | rrf | 52 | 52 | 0 | 52 | 51 | 52 | 52 |
| Qwen9 | rerank | 52 | 52 | 0 | 52 | 52 | 52 | 52 |

Disponibilidad anterior calculada sobre todas las aceptadas; no confundir con aplicabilidad ni soporte común. availability.csv informa por generador, estrategia y criterio: aceptadas, dentro/fuera del ámbito, numéricas, no disponibles, comunes y numéricas excluidas, con qids. analysis.json y support_cells.csv permiten reconstruir las medias y sus denominadores. Los fallos no reciben puntuación.

### Intentos y disponibilidad operacional

| Modelo | Método | Estado | Unidades | Intentos | Reintentadas | Ledger completo | Latencia n | Prompt n | Completion n |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| Gemma | bm25 | accepted | 48 | 48 | 0 | 0 | 48 | 48 | 48 |
| Gemma | bm25 | failed | 4 | 12 | 4 | 4 | 4 | 4 | 4 |
| Gemma | dense | accepted | 49 | 51 | 2 | 0 | 49 | 49 | 49 |
| Gemma | dense | failed | 3 | 9 | 3 | 3 | 3 | 3 | 3 |
| Gemma | rrf | accepted | 44 | 45 | 1 | 0 | 44 | 44 | 44 |
| Gemma | rrf | failed | 8 | 24 | 8 | 8 | 8 | 8 | 8 |
| Gemma | rerank | accepted | 47 | 47 | 0 | 0 | 47 | 47 | 47 |
| Gemma | rerank | failed | 5 | 15 | 5 | 5 | 5 | 5 | 5 |
| Qwen4 | bm25 | accepted | 52 | 53 | 1 | 0 | 52 | 52 | 52 |
| Qwen4 | bm25 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Qwen4 | dense | accepted | 52 | 54 | 2 | 0 | 52 | 52 | 52 |
| Qwen4 | dense | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Qwen4 | rrf | accepted | 52 | 53 | 1 | 0 | 52 | 52 | 52 |
| Qwen4 | rrf | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Qwen4 | rerank | accepted | 52 | 55 | 3 | 0 | 52 | 52 | 52 |
| Qwen4 | rerank | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Qwen9 | bm25 | accepted | 52 | 52 | 0 | 0 | 52 | 52 | 52 |
| Qwen9 | bm25 | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Qwen9 | dense | accepted | 52 | 52 | 0 | 0 | 52 | 52 | 52 |
| Qwen9 | dense | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Qwen9 | rrf | accepted | 52 | 52 | 0 | 0 | 52 | 52 | 52 |
| Qwen9 | rrf | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Qwen9 | rerank | accepted | 52 | 52 | 0 | 0 | 52 | 52 | 52 |
| Qwen9 | rerank | failed | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Los acumulados se leen una sola vez: nunca se añade el total de attempt_usage al total ya registrado. Los 20 ledgers fallidos permiten comprobar las sumas de cada intento. Los descriptivos completos incluyen media, mediana, p95 por nearest-rank (ceil(0,95n)), mínimo, máximo, desviación poblacional, suma y disponibilidad; son aritméticos por unidad, no macro por base.

## Los seis contrastes no seleccionados por generador y criterio

Signo: destino − origen. Pos/neg/empates se cuentan sobre preguntas base tras promediar las diferencias de sus formulaciones comunes a las CUATRO estrategias. No se interpreta la exclusión del cero como superioridad ajustada. No hay corrección por multiplicidad ni conclusión de equivalencia.

### Gemma

| Criterio | Origen → destino | Delta | IC95 puntual | n_cells | n_base | Pos | Neg | Empates |
|---|---|---:|---|---:|---:|---:|---:|---:|
| faithfulness | bm25 → dense | 0,028 | [-0,194; 0,278] | 34 | 18 | 2 | 3 | 13 |
| faithfulness | bm25 → rrf | -0,056 | [-0,222; 0,083] | 34 | 18 | 2 | 3 | 13 |
| faithfulness | bm25 → rerank | 0,056 | [-0,194; 0,333] | 34 | 18 | 4 | 3 | 11 |
| faithfulness | dense → rrf | -0,083 | [-0,222; 0,056] | 34 | 18 | 1 | 3 | 14 |
| faithfulness | dense → rerank | 0,028 | [-0,139; 0,194] | 34 | 18 | 2 | 1 | 15 |
| faithfulness | rrf → rerank | 0,111 | [-0,083; 0,278] | 34 | 18 | 5 | 1 | 12 |
| factual_correctness | bm25 → dense | 0,083 | [-0,194; 0,361] | 33 | 18 | 4 | 2 | 12 |
| factual_correctness | bm25 → rrf | 0,056 | [-0,083; 0,222] | 33 | 18 | 3 | 2 | 13 |
| factual_correctness | bm25 → rerank | -0,028 | [-0,278; 0,250] | 33 | 18 | 3 | 5 | 10 |
| factual_correctness | dense → rrf | -0,028 | [-0,250; 0,194] | 33 | 18 | 4 | 5 | 9 |
| factual_correctness | dense → rerank | -0,111 | [-0,361; 0,111] | 33 | 18 | 3 | 5 | 10 |
| factual_correctness | rrf → rerank | -0,083 | [-0,306; 0,139] | 33 | 18 | 3 | 5 | 10 |
| behavior_ok | bm25 → dense | 0,023 | [-0,227; 0,273] | 41 | 22 | 4 | 4 | 14 |
| behavior_ok | bm25 → rrf | 0,023 | [-0,045; 0,091] | 41 | 22 | 2 | 1 | 19 |
| behavior_ok | bm25 → rerank | -0,068 | [-0,318; 0,205] | 41 | 22 | 4 | 6 | 12 |
| behavior_ok | dense → rrf | 0,000 | [-0,227; 0,227] | 41 | 22 | 4 | 4 | 14 |
| behavior_ok | dense → rerank | -0,091 | [-0,318; 0,114] | 41 | 22 | 4 | 5 | 13 |
| behavior_ok | rrf → rerank | -0,091 | [-0,318; 0,159] | 41 | 22 | 4 | 6 | 12 |
| citations_ok | bm25 → dense | -0,023 | [-0,136; 0,068] | 41 | 22 | 1 | 1 | 20 |
| citations_ok | bm25 → rrf | 0,045 | [0,000; 0,114] | 41 | 22 | 2 | 0 | 20 |
| citations_ok | bm25 → rerank | -0,023 | [-0,159; 0,091] | 41 | 22 | 2 | 2 | 18 |
| citations_ok | dense → rrf | 0,068 | [0,000; 0,182] | 41 | 22 | 2 | 0 | 20 |
| citations_ok | dense → rerank | 0,000 | [-0,068; 0,068] | 41 | 22 | 1 | 1 | 20 |
| citations_ok | rrf → rerank | -0,068 | [-0,182; 0,000] | 41 | 22 | 0 | 2 | 20 |

### Qwen4

| Criterio | Origen → destino | Delta | IC95 puntual | n_cells | n_base | Pos | Neg | Empates |
|---|---|---:|---|---:|---:|---:|---:|---:|
| faithfulness | bm25 → dense | 0,250 | [0,045; 0,477] | 44 | 22 | 9 | 3 | 10 |
| faithfulness | bm25 → rrf | 0,250 | [0,091; 0,432] | 44 | 22 | 8 | 1 | 13 |
| faithfulness | bm25 → rerank | 0,409 | [0,205; 0,614] | 44 | 22 | 10 | 0 | 12 |
| faithfulness | dense → rrf | 0,000 | [-0,159; 0,159] | 44 | 22 | 4 | 4 | 14 |
| faithfulness | dense → rerank | 0,159 | [0,000; 0,341] | 44 | 22 | 5 | 1 | 16 |
| faithfulness | rrf → rerank | 0,159 | [0,023; 0,318] | 44 | 22 | 6 | 1 | 15 |
| factual_correctness | bm25 → dense | 0,023 | [-0,182; 0,227] | 43 | 22 | 6 | 5 | 11 |
| factual_correctness | bm25 → rrf | 0,045 | [-0,136; 0,227] | 43 | 22 | 4 | 3 | 15 |
| factual_correctness | bm25 → rerank | 0,091 | [-0,114; 0,295] | 43 | 22 | 7 | 5 | 10 |
| factual_correctness | dense → rrf | 0,023 | [-0,091; 0,136] | 43 | 22 | 4 | 3 | 15 |
| factual_correctness | dense → rerank | 0,068 | [-0,091; 0,227] | 43 | 22 | 4 | 3 | 15 |
| factual_correctness | rrf → rerank | 0,045 | [-0,114; 0,205] | 43 | 22 | 7 | 5 | 10 |
| behavior_ok | bm25 → dense | -0,038 | [-0,192; 0,115] | 52 | 26 | 4 | 5 | 17 |
| behavior_ok | bm25 → rrf | 0,096 | [-0,058; 0,269] | 52 | 26 | 6 | 3 | 17 |
| behavior_ok | bm25 → rerank | 0,077 | [-0,096; 0,269] | 52 | 26 | 7 | 5 | 14 |
| behavior_ok | dense → rrf | 0,135 | [0,000; 0,269] | 52 | 26 | 7 | 2 | 17 |
| behavior_ok | dense → rerank | 0,115 | [-0,038; 0,288] | 52 | 26 | 5 | 3 | 18 |
| behavior_ok | rrf → rerank | -0,019 | [-0,173; 0,135] | 52 | 26 | 6 | 7 | 13 |
| citations_ok | bm25 → dense | 0,000 | [-0,077; 0,077] | 52 | 26 | 2 | 2 | 22 |
| citations_ok | bm25 → rrf | 0,000 | [-0,096; 0,096] | 52 | 26 | 3 | 3 | 20 |
| citations_ok | bm25 → rerank | 0,000 | [-0,096; 0,096] | 52 | 26 | 3 | 3 | 20 |
| citations_ok | dense → rrf | 0,000 | [-0,077; 0,077] | 52 | 26 | 2 | 2 | 22 |
| citations_ok | dense → rerank | 0,000 | [-0,115; 0,115] | 52 | 26 | 4 | 4 | 18 |
| citations_ok | rrf → rerank | 0,000 | [-0,096; 0,096] | 52 | 26 | 3 | 3 | 20 |

### Qwen9

| Criterio | Origen → destino | Delta | IC95 puntual | n_cells | n_base | Pos | Neg | Empates |
|---|---|---:|---|---:|---:|---:|---:|---:|
| faithfulness | bm25 → dense | -0,091 | [-0,250; 0,068] | 44 | 22 | 2 | 6 | 14 |
| faithfulness | bm25 → rrf | 0,091 | [0,000; 0,205] | 44 | 22 | 3 | 0 | 19 |
| faithfulness | bm25 → rerank | 0,045 | [-0,045; 0,159] | 44 | 22 | 2 | 1 | 19 |
| faithfulness | dense → rrf | 0,182 | [0,068; 0,318] | 44 | 22 | 6 | 0 | 16 |
| faithfulness | dense → rerank | 0,136 | [0,045; 0,227] | 44 | 22 | 6 | 0 | 16 |
| faithfulness | rrf → rerank | -0,045 | [-0,114; 0,000] | 44 | 22 | 0 | 2 | 20 |
| factual_correctness | bm25 → dense | 0,045 | [-0,159; 0,227] | 43 | 22 | 6 | 3 | 13 |
| factual_correctness | bm25 → rrf | 0,136 | [-0,023; 0,318] | 43 | 22 | 7 | 3 | 12 |
| factual_correctness | bm25 → rerank | 0,159 | [-0,023; 0,364] | 43 | 22 | 6 | 3 | 13 |
| factual_correctness | dense → rrf | 0,091 | [0,000; 0,227] | 43 | 22 | 2 | 0 | 20 |
| factual_correctness | dense → rerank | 0,114 | [0,000; 0,250] | 43 | 22 | 3 | 0 | 19 |
| factual_correctness | rrf → rerank | 0,023 | [-0,114; 0,159] | 43 | 22 | 2 | 1 | 19 |
| behavior_ok | bm25 → dense | 0,077 | [-0,115; 0,269] | 52 | 26 | 5 | 4 | 17 |
| behavior_ok | bm25 → rrf | 0,077 | [-0,077; 0,231] | 52 | 26 | 5 | 2 | 19 |
| behavior_ok | bm25 → rerank | 0,115 | [-0,058; 0,308] | 52 | 26 | 5 | 2 | 19 |
| behavior_ok | dense → rrf | 0,000 | [-0,096; 0,077] | 52 | 26 | 2 | 1 | 23 |
| behavior_ok | dense → rerank | 0,038 | [0,000; 0,096] | 52 | 26 | 2 | 0 | 24 |
| behavior_ok | rrf → rerank | 0,038 | [0,000; 0,115] | 52 | 26 | 1 | 0 | 25 |
| citations_ok | bm25 → dense | -0,019 | [-0,058; 0,000] | 52 | 26 | 0 | 1 | 25 |
| citations_ok | bm25 → rrf | 0,000 | [0,000; 0,000] | 52 | 26 | 0 | 0 | 26 |
| citations_ok | bm25 → rerank | -0,038 | [-0,096; 0,000] | 52 | 26 | 0 | 2 | 24 |
| citations_ok | dense → rrf | 0,019 | [0,000; 0,058] | 52 | 26 | 1 | 0 | 25 |
| citations_ok | dense → rerank | -0,019 | [-0,096; 0,038] | 52 | 26 | 1 | 2 | 23 |
| citations_ok | rrf → rerank | -0,038 | [-0,096; 0,000] | 52 | 26 | 0 | 2 | 24 |

## Artefactos y contrato

- main_table.csv: 12 filas, medias a precisión completa y n_cells/n_base por criterio; fuente de tbl-final-recuperadores (96 cifras visibles).
- operational_table.csv: 12 filas; medias de aceptadas y conteos de aceptadas/fallidas; fuente de tbl-final-operacion (60 cifras visibles).
- per_retriever.csv y operational.csv: copias de los dos CSV anteriores para integración con el contrato documental.
- quality_levels.csv (48) y paired_contrasts.csv (72): niveles y todos los contrastes; trazas completas en analysis.json.
- coverage.csv, availability.csv, failures.csv y joined_cells.csv: cobertura, disponibilidad, fallos y puntuaciones consolidadas.
- support_cells.csv: cada celda de soporte y puntuación que contribuye a cada nivel.
- operational_cells.csv (624) y operational_summary.csv (24): procedencia fila/archivo y descriptivos separados por estado.
- results_proposed.md: propuesta generada para integrar en memoria; no modifica tfm.qmd.
- analysis.json y hash_manifest.json: parámetros, resultados, trazas y hashes; no se usa un eje externo de capacidad.

La calidad es condicional a respuestas aceptadas y a soporte común. Fallos asimétricos pueden producir sesgo de supervivencia; no se eliminan de la auditoría ni se imputan. Las variantes no son réplicas independientes. Los IC puntuales no proporcionan control de error familiar. El corpus y golden set limitan la generalización. El replay determinista no verifica disponibilidad actual de modelos/API y no añade datos ni reevalúa decisiones humanas.
