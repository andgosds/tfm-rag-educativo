# Análisis de sensibilidad del juez RAG: Gemma 3 4B y GLM 5.3 Flash

## Diseño

El análisis mantiene fijas las 44 respuestas generadas con Qwen 3.5 9B, las preguntas, las referencias y los contextos recuperados. Se comparan las mismas 22 preguntas bajo RRF y RRF con reranking. Gemma 3 4B actúa como juez canónico local y GLM 5.3 Flash como juez alternativo remoto mediante OpenCode Go, con esfuerzo de razonamiento bajo. RAGAS 0.4.3 calcula Faithfulness y Factual Correctness; la conducta se valora mediante una rúbrica ciega de 0 a 2.

La comparación usa pares alineados por condición de recuperación y qid. Las medias no emparejadas solo se conservan como descripción, porque Gemma no produjo Faithfulness en siete casos. Factual Correctness dispone de treinta pares válidos: trece respuestas ordinarias y dos correcciones fundamentadas por condición.

## Comparación RRF y reranking según GLM

| Métrica | RRF | RRF + reranking | Delta reranking − RRF | Victorias reranking | Empates | Victorias RRF |
|---|---:|---:|---:|---:|---:|---:|
| Faithfulness | 0,7432 | 0,7215 | −0,0216 | 4 | 12 | 6 |
| Factual Correctness | 0,8547 | 0,8093 | −0,0453 | 3 | 6 | 6 |
| Conducta declarada correcta | 0,8636 | 0,9091 | +0,0455 | 1 | 21 | 0 |
| Puntuación del juez de conducta | 1,9091 | 1,9545 | +0,0455 | 1 | 21 | 0 |
| Validez de citas | 1,0000 | 1,0000 | 0,0000 | 0 | 22 | 0 |
| Presencia de citas | 1,0000 | 1,0000 | 0,0000 | 0 | 22 | 0 |

El reranking no mejora de forma consistente la calidad end-to-end. RRF obtiene una media superior y más victorias en Faithfulness y Factual Correctness, mientras el reranking mejora una sola decisión de conducta, q-v1-015. La validez y la presencia de citas son idénticas. Con 22 preguntas, estas diferencias deben interpretarse como evidencia descriptiva del piloto, no como una estimación estable del efecto poblacional.

El desglose por conducta ayuda a localizar el resultado. Las siete abstenciones son idénticas en conducta y obtienen 2/2 con GLM en ambas condiciones. En las trece respuestas ordinarias, RRF supera al reranking en Faithfulness y Factual Correctness, aunque el reranking mejora la adecuación de la conducta declarada. En las dos correcciones fundamentadas, RRF obtiene 1,00 de Factual Correctness frente a 0,80 con reranking.

## Sensibilidad al juez

| Métrica | Gemma | GLM | Casos comunes | Victorias GLM | Empates | Victorias Gemma | Delta GLM − Gemma |
|---|---:|---:|---:|---:|---:|---:|---:|
| Faithfulness | 0,7056 | 0,7324 | 37 | 4 | 26 | 7 | +0,0122 |
| Factual Correctness | 0,9007 | 0,8320 | 30 | 6 | 14 | 10 | −0,0687 |
| Conducta | 1,2727 | 1,9318 | 44 | 16 | 25 | 3 | +0,6591 |

La disponibilidad difiere: Gemma acumula siete casos con errores de evaluación, mientras GLM completa los 44 sin errores. En los 37 pares comunes de Faithfulness, la diferencia media es pequeña y hay 26 empates, aunque Gemma gana siete casos frente a cuatro de GLM. En Factual Correctness, Gemma asigna puntuaciones más altas con mayor frecuencia. El caso q-v1-005 demuestra que esto no implica necesariamente mayor validez: GLM asigna 0 a dos respuestas que expresan exactamente la fuerza y dirección de la correlación y que ambos jueces de conducta consideran plenamente correctas.

La discrepancia de conducta es principalmente un fallo sistemático de Gemma. En las abstenciones, sus justificaciones reconocen que los contextos son insuficientes y que no puede responderse, pero asignan 0 a la respuesta «I cannot answer from the supplied contexts». GLM asigna 2 porque la abstención coincide con el comportamiento esperado. El mismo problema aparece en q-v1-020: Gemma afirma que la respuesta sostiene que el intervalo se estrecha, aunque el texto dice explícitamente que se ensancha. Por tanto, la media de conducta de Gemma no debe utilizarse como resultado canónico sin corrección humana.

GLM también aporta distinciones útiles. En q-v1-014 rebaja la respuesta porque omite ordenar los datos y determinar Q1 y Q3 antes de aplicar el criterio de 1,5 IQR. En la respuesta RRF de q-v1-015 señala que describir la mediana solo como resistente no explica que dependa de la posición central y no de la magnitud de los valores extremos. Estas observaciones son coherentes con las referencias y justifican conservar esos casos en la auditoría.

## Latencia y tokens del juez

Gemma registra 37,84 segundos por caso y GLM, 73,55 segundos. Esta diferencia es observacional: Gemma se ejecutó localmente y GLM remotamente, con las dos condiciones lanzadas en paralelo. No constituye un benchmark controlado de latencia. La rúbrica de conducta consumió 110.947 tokens observados con Gemma y 107.917 con GLM, pero RAGAS no expone su consumo total; por ello no puede calcularse el coste completo de evaluación ni compararse el coste económico de ambos jueces.

## Auditoría humana dirigida por riesgo

La cola dirigida por riesgo contiene 28 pares condición–pregunta correspondientes a 15 qids únicos: 13 casos RRF y 15 casos con reranking. Incluye las catorce abstenciones, las cuatro correcciones fundamentadas, siete errores de Gemma, diecinueve desacuerdos de conducta, cinco incumplimientos del comportamiento declarado y cuatro desacuerdos interjuez de al menos 0,5 en métricas RAGAS.

La adjudicación humana se completó para los 28 pares. Las etiquetas humanas se conservaron como una capa separada y no sustituyeron silenciosamente las métricas automáticas. Para contrastar Faithfulness y Factual Correctness con las decisiones categóricas se usó una equivalencia ordinal explícita: 0 para `unsupported` o `incorrect`, 0,5 para las categorías parciales y 1 para `supported` o `correct`. Los casos `not_applicable` se excluyeron del error numérico y se analizaron como un problema separado de aplicabilidad. Dado que la cola es una muestra no aleatoria seleccionada por riesgo, los acuerdos observados describen los casos sensibles y no estiman la precisión de los jueces sobre una población independiente.

| Indicador en la cola de riesgo | Gemma 3 4B | GLM 5.3 Flash |
|---|---:|---:|
| Errores explícitos de evaluación | 7 | 0 |
| Acuerdo exacto en conducta | 12/28 (42,9 %) | 25/28 (89,3 %) |
| MAE de conducta | 1,1429 | 0,1071 |
| Acuerdo en respuestas ordinarias | 10/10 (100,0 %) | 7/10 (70,0 %) |
| Acuerdo en abstenciones | 0/14 (0,0 %) | 14/14 (100,0 %) |
| Acuerdo en correcciones fundamentadas | 2/4 (50,0 %) | 4/4 (100,0 %) |
| Faithfulness aplicable disponible | 9/14 | 14/14 |
| MAE de Faithfulness aplicable | 0,0000 | 0,0560 |
| MAE de Factual Correctness aplicable | 0,1093 | 0,2129 |

Gemma se aproxima más a las etiquetas ordinales humanas en las métricas RAGAS cuando consigue producir una puntuación, especialmente en Factual Correctness. Sin embargo, pierde cinco resultados de Faithfulness en casos aplicables y sus fallos de conducta son sistemáticos: asigna 0 a las catorce abstenciones correctas de la cola y falla dos correcciones de q-v1-020. GLM completa todos los casos y reproduce correctamente todas las abstenciones y correcciones, aunque resulta demasiado estricto en tres respuestas ordinarias de q-v1-014 y q-v1-015. Ningún juez sustituye la revisión humana dirigida por riesgo.

La auditoría marca Faithfulness como no aplicable en las catorce abstenciones sin afirmaciones sustantivas. Pese a ello, Gemma emite una puntuación en doce y GLM en las catorce. Estas salidas se consideran diagnósticas y no deben agregarse como si midieran fundamentación. Factual Correctness también se mantiene no aplicable en las catorce abstenciones y ambos pipelines respetan esa exclusión.

## Conducta consolidada de los 44 casos

Para cerrar la dimensión de conducta se creó una capa final explícita: la adjudicación humana prevalece en los 28 casos auditados y GLM se conserva en los 16 casos no seleccionados. El artefacto mantiene por separado la puntuación automática, la puntuación final y su fuente.

| Condición | Conducta GLM original | Conducta consolidada | Casos humanos |
|---|---:|---:|---:|
| RRF | 1,9091 | 2,0000 | 13/22 |
| RRF + reranking | 1,9545 | 2,0000 | 15/22 |

En la comparación emparejada consolidada hay 22 empates y ninguna victoria de una condición sobre la otra. El delta medio reranking menos RRF es 0,0000. Por tanto, la pequeña ventaja automática del reranking en conducta no se sostiene tras la adjudicación y ambas configuraciones cumplen por igual la conducta esperada.

## Decisión del juez

GLM 5.3 Flash con esfuerzo de razonamiento bajo se adopta como **juez automático principal** para esta fase por tres razones: completa los 44 casos sin errores, se ajusta a la rúbrica corregida y muestra una alineación muy superior con la conducta humana en los casos metodológicamente sensibles. Gemma 3 4B se conserva como análisis de sensibilidad, no como juez canónico.

Esta elección no implica que GLM sea superior en todas las métricas. En Faithfulness y Factual Correctness, las puntuaciones RAGAS siguen siendo sensibles al modelo y las etiquetas humanas muestran una mejor aproximación numérica de Gemma en los casos donde está disponible. Por ello, GLM se usa como ejecución principal por completitud y validez de conducta; Gemma se reporta en paralelo; las abstenciones quedan fuera de Faithfulness y Factual Correctness cuando no contienen afirmaciones evaluables; y la adjudicación humana prevalece en la cola de riesgo.

## Conclusión final del piloto

La evaluación automática y la auditoría humana convergen en que la mejora de MRR y nDCG obtenida por el reranker no se traduce en respuestas RAG más correctas o fundamentadas. RRF mantiene mejores medias automáticas de Faithfulness y Factual Correctness con GLM, mientras que la conducta consolidada empata en 2,0000. También usa menos tiempo y tokens de generación y conserva una latencia de retrieval muy inferior.

En este piloto, RRF es la configuración recomendada por equilibrio entre calidad y coste operativo. La conclusión se limita a 22 preguntas, a un único corpus educativo y a una auditoría humana dirigida por riesgo; no constituye una estimación poblacional ni demuestra que el reranking carezca de utilidad en otros corpus o presupuestos de contexto.

Los resultados reproducibles se conservan en `outputs/rag_eval/rag_judge_human_alignment_gemma3_4b_vs_glm53flash_low_v1_22q.json` y `outputs/rag_eval/rag_behavior_human_glm53flash_low_consolidated_v1_22q.json`.
