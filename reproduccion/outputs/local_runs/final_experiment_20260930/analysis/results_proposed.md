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
