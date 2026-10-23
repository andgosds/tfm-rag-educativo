# Híbrido RRF con reranking MiniLM

## Alcance

La cuarta condición experimental aplica un cross-encoder sobre los diez candidatos producidos por RRF. El reranker solo modifica el orden: conserva los mismos 288 chunks, 22 preguntas, 220 pares pregunta–chunk y qrels pooled. Esta restricción permite atribuir los cambios en Precision@5, Recall@5, MRR y nDCG a la reordenación, sin confundirlos con una ampliación del conjunto candidato.

El modelo se fijó antes de examinar las métricas:

- modelo: `cross-encoder/ms-marco-MiniLM-L6-v2`;
- revisión: `233902d25c440f23af6f7d6e94d2946bac0bee0a`;
- licencia: Apache-2.0;
- idioma declarado: inglés;
- dataset de entrenamiento declarado: MS MARCO;
- profundidad candidata: 10;
- longitud máxima: 512 tokens;
- batch size: 16;
- dispositivo: CUDA;
- desempate: score descendente y después `chunk_id`.

MiniLM-L6 se eligió como primera condición de reranking porque es un cross-encoder ligero para ranking en inglés y puede ejecutarse en la RTX 2060 SUPER disponible. No se compararon varios rerankers ni se ajustó la profundidad sobre las 22 preguntas.

## Artefactos

- Runner: `scripts/run_reranker.py`.
- Pruebas: `tests/test_run_reranker.py`.
- Run: `outputs/runs/hybrid_rrf_k60_minilm_l6_rerank_pooled_v1_22q.jsonl`.
- Métricas agregadas: `outputs/metrics/hybrid_rrf_k60_minilm_l6_rerank_pooled_v1_22q_metrics.csv`.
- Métricas por pregunta: `outputs/metrics/hybrid_rrf_k60_minilm_l6_rerank_pooled_v1_22q_per_query.csv`.
- Auditoría: `outputs/metrics/hybrid_rrf_k60_minilm_l6_rerank_pooled_v1_22q_audit.json`.
- Resumen: `outputs/metrics/hybrid_rrf_k60_minilm_l6_rerank_pooled_v1_22q_summary.json`.
- Metadatos del modelo y entorno: `outputs/rerankers/hybrid_rrf_k60_minilm_l6_rerank_pooled_v1_22q_metadata.json`.

El run conserva el rango y el score de RRF, los rangos de BM25 y dense, el score del cross-encoder y la nueva posición. Los hashes del corpus, golden set, qrels y run híbrido permiten reconstruir la entrada exacta.

## Resultados

| Métrica | BM25 @5 | Dense @5 | RRF @5 | RRF + reranker @5 | BM25 @10 | Dense @10 | RRF @10 | RRF + reranker @10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Precision | 0,4769 | 0,6154 | 0,5846 | **0,6308** | 0,3923 | 0,3923 | **0,4231** | **0,4231** |
| Recall | 0,5128 | 0,6635 | 0,6506 | **0,7083** | 0,8077 | 0,8301 | **0,8846** | **0,8846** |
| MRR | 0,7885 | 0,7436 | 0,8846 | **0,9231** | 0,7885 | 0,7436 | 0,8846 | **0,9231** |
| nDCG | 0,5907 | 0,7155 | 0,7431 | **0,7976** | 0,7052 | 0,7491 | 0,8167 | **0,8483** |

El reranker obtiene el mejor valor observado en todas las métricas a cinco documentos, MRR@10 y nDCG@10. Frente a RRF, aumenta Precision@5 en 0,0462, Recall@5 en 0,0577, MRR en 0,0385 y nDCG@5 en 0,0545. La reordenación concentra más evidencia relevante en las primeras posiciones.

Precision@10 y Recall@10 permanecen exactamente iguales a RRF. Este resultado es necesario, no accidental: el reranker conserva los mismos diez chunks y solo cambia su orden. MRR@10 y nDCG@10 sí mejoran porque dependen de la posición de los resultados relevantes.

## Cobertura completa

| Método | Cobertura completa @5 | Cobertura completa @10 |
|---|---:|---:|
| BM25 | 0/13 (0,0%) | 5/13 (38,5%) |
| Dense | 3/13 (23,1%) | 6/13 (46,2%) |
| RRF | 3/13 (23,1%) | 8/13 (61,5%) |
| RRF + reranker | **4/13 (30,8%)** | **8/13 (61,5%)** |

El reranker lleva toda la evidencia de q-v1-012 a las cinco primeras posiciones y mantiene la cobertura completa de q-v1-004, q-v1-006 y q-v1-011. La cobertura a diez no puede cambiar porque el conjunto candidato es idéntico.

## Resultados por pregunta

Las mejoras más claras aparecen en q-v1-001 y q-v1-012. En ambas, Precision@5 pasa de 0,4 a 0,8. Recall@5 sube de 0,3333 a 0,6667 en q-v1-001 y de 0,5 a 1,0 en q-v1-012. También mejoran q-v1-014, q-v1-015 y q-v1-016 en posición o concentración temprana de evidencia.

La mejora agregada convive con dos retrocesos. En q-v1-013, Precision@5 baja de 1,0 a 0,6 y Recall@5 de 0,4167 a 0,25; el primer relevante pasa del rango 1 al 2. En q-v1-017, Recall@5 baja de 0,75 a 0,5, aunque el primer relevante sube del rango 2 al 1. El cross-encoder favorece el primer acierto de q-v1-017, pero concentra menos evidencia total en el top-5.

## Truncación

Diecisiete de los 220 pares superan 512 tokens antes de truncarse. La longitud máxima observada es de 747 tokens. Cuatro pares truncados tienen qrels positivos: uno de grado 1 en q-v1-005 y los tres chunks de grado 2 de q-v1-013 que aparecen en el top-10 híbrido. También se trunca un contexto de grado 1 de q-v1-019, que pertenece a una pregunta no respondible.

La coincidencia entre los tres chunks relevantes truncados y el retroceso de q-v1-013 es metodológicamente importante. No permite atribuir el descenso únicamente a la truncación, porque el cross-encoder también puede asignar scores deficientes por sus propios sesgos de dominio. Sí impide interpretar ese caso como evidencia limpia de que el modelo comprende peor el contenido completo: parte de la información no entra en la ventana de 512 tokens.

No se amplía la longitud ni se sustituye el modelo después de observar este resultado. Esa intervención convertiría q-v1-013 en señal de ajuste. La truncación queda registrada como amenaza a la validez y como posible factor para un experimento posterior predefinido.

## Latencia

| Componente o condición | Latencia media observada/estimada |
|---|---:|
| Reranking de 10 pares | 44,69 ms |
| RRF + reranker, recuperación serial estimada | 53,11 ms |
| RRF + reranker, recuperación paralela estimada | 51,04 ms |
| Carga del cross-encoder | 1,88 s |

El reranker domina la latencia online de la cuarta condición. Frente a RRF, añade alrededor de 44,69 ms por consulta en esta ejecución. El aumento compra una mejor concentración de evidencia en top-5 y un mejor orden graduado, pero no amplía Recall@10.

Estas cifras proceden de una sola ejecución local en la RTX 2060 SUPER. Son útiles para describir la escala del coste, pero la comparación final de eficiencia requiere calentamiento, varias repeticiones y un protocolo común.

## Interpretación

La cuarta condición ofrece la mejor calidad de ranking observada en el piloto. RRF aporta el conjunto candidato con mayor cobertura y MiniLM mejora su orden, sobre todo en las primeras cinco posiciones. El resultado apoya la hipótesis de que la combinación híbrida con reranking puede superar a los recuperadores individuales bajo una colección educativa en inglés.

La recomendación no es universal. La mejora se estima sobre trece preguntas respondibles y qrels derivados de un pool BM25+dense con adjudicación dirigida por riesgo. El coste online aumenta de forma clara y la truncación afecta precisamente al caso con mayor retroceso. Por tanto, el reranker es la mejor condición de calidad del piloto, mientras RRF sin reranking conserva una relación más favorable entre calidad, latencia y complejidad.
