# Recuperación híbrida BM25+dense mediante RRF

## Alcance

La condición híbrida combina los rankings top-10 de BM25 y E5-base-v2 ya calculados sobre los mismos 288 chunks y las mismas 22 preguntas. No modifica el corpus, el chunking, las consultas ni los qrels pooled. La evaluación ordinaria mantiene las trece preguntas respondibles con evidencia de grado 2; las nueve no respondibles permanecen en el run para el análisis posterior de corrección fundamentada y abstención.

La fusión utiliza Reciprocal Rank Fusion (RRF). Para cada chunk se suman las contribuciones de los dos rankings:

\[
\operatorname{RRF}(d)=\sum_{m\in\{BM25,dense\}}\frac{1}{60+r_m(d)}.
\]

El parámetro se fija en $k_0=60$ antes de examinar el resultado. Se fusionan diez posiciones por método y se conservan los diez primeros chunks. Los empates se resuelven de forma determinista por `chunk_id`. RRF evita comparar directamente los scores de BM25 y dense, cuyas escalas no son homogéneas.

## Artefactos

- Runner: `scripts/run_hybrid_rrf.py`.
- Pruebas: `tests/test_run_hybrid_rrf.py`.
- Run: `outputs/runs/hybrid_rrf_k60_pooled_v1_22q.jsonl`.
- Métricas agregadas: `outputs/metrics/hybrid_rrf_k60_pooled_v1_22q_metrics.csv`.
- Métricas por pregunta: `outputs/metrics/hybrid_rrf_k60_pooled_v1_22q_per_query.csv`.
- Auditoría de rangos: `outputs/metrics/hybrid_rrf_k60_pooled_v1_22q_audit.json`.
- Resumen reproducible: `outputs/metrics/hybrid_rrf_k60_pooled_v1_22q_summary.json`.
- Informe del pool incremental: `data/golden/pool_hybrid_rrf_incremental_v1_22q_report.json`.

El run registra los rangos de origen de BM25 y dense para cada resultado. También conserva los hashes de ambos runs, del corpus, del golden set y de los qrels pooled. El hash de estos últimos es `6a5cf811fd15ddf07a6b7fb39932c6917b99f781b450b950593cafc6cc0ad871`, el mismo utilizado en la reevaluación de los recuperadores individuales.

## Resultados

| Métrica | BM25 @5 | Dense @5 | RRF @5 | BM25 @10 | Dense @10 | RRF @10 |
|---|---:|---:|---:|---:|---:|---:|
| Precision | 0,4769 | **0,6154** | 0,5846 | 0,3923 | 0,3923 | **0,4231** |
| Recall | 0,5128 | **0,6635** | 0,6506 | 0,8077 | 0,8301 | **0,8846** |
| MRR | 0,7885 | 0,7436 | **0,8846** | 0,7885 | 0,7436 | **0,8846** |
| nDCG | 0,5907 | 0,7155 | **0,7431** | 0,7052 | 0,7491 | **0,8167** |

RRF mejora frente a BM25 y dense en las cuatro métricas a diez resultados. La ganancia es especialmente visible en MRR y nDCG: la fusión combina primeros aciertos fuertes de ambas señales y ordena mejor el conjunto recuperado. También eleva Recall@10 hasta 0,8846 y Precision@10 hasta 0,4231.

La ventaja no se mantiene en todas las métricas a cinco resultados. Dense conserva mayor Precision@5 y Recall@5, con diferencias de 0,0308 y 0,0128 respecto a RRF. La fusión, por tanto, mejora el primer acierto y la calidad global del orden, pero puede desplazar alguna evidencia semántica útil fuera de las primeras cinco posiciones.

## Cobertura de evidencia

| Método | Cobertura completa @5 | Cobertura completa @10 |
|---|---:|---:|
| BM25 | 0/13 (0,0%) | 5/13 (38,5%) |
| Dense | 3/13 (23,1%) | 6/13 (46,2%) |
| RRF | 3/13 (23,1%) | **8/13 (61,5%)** |

RRF reúne todos los chunks de grado 2 para ocho preguntas en top-10. Añade cobertura completa en q-v1-001 y q-v1-002 respecto a dense, y conserva q-v1-012 y q-v1-017, donde dense complementaba a BM25. También aumenta el recall de q-v1-016 de 0,6667 a 0,8333.

La mejora agregada oculta un retroceso relevante. En q-v1-003, Recall@10 baja a 0,50, frente a 0,75 en BM25 y 0,625 en dense. La unión de señales no garantiza conservar cada evidencia de los rankings de origen porque RRF vuelve a ordenar el conjunto y mantiene solo diez posiciones. Este caso debe preservarse en el análisis de errores y evita presentar la fusión como una mejora uniforme.

## Latencia

La fusión sobre rankings ya calculados tarda una media observada de 0,0077 ms por consulta. Esta cifra no representa la latencia completa del sistema híbrido. Al combinar las latencias registradas por los runs de origen, la estimación media es de 8,42 ms si BM25 y dense se ejecutan en serie y de 6,35 ms si se ejecutan en paralelo, más las condiciones de carga y hardware propias de cada recuperador.

Estas estimaciones sirven para documentar el coste operativo del pipeline actual, pero no son un benchmark controlado. Una comparación final de eficiencia requeriría calentamiento, varias repeticiones y medición conjunta de los recuperadores bajo un mismo protocolo.

## Pool incremental

El run híbrido contiene 220 pares pregunta–chunk. Todos pertenecen al pool técnico BM25+dense previo, que contiene 340 pares únicos. El pool incremental aporta, por tanto, cero candidatos nuevos.

Este resultado es coherente con el diseño: el híbrido fusiona exclusivamente candidatos procedentes de los top-10 de los dos recuperadores que originaron el pool. “Ausente del TSV de qrels” no se utiliza como criterio de novedad, porque la adjudicación fue dirigida por riesgo y el TSV solo conserva grados positivos. La comparación correcta se realiza contra el pool técnico completo, incluidos los candidatos no seleccionados para revisión humana.

## Interpretación

En este piloto, RRF ofrece el mejor equilibrio observado a diez resultados. Supera a BM25 y dense en posición del primer acierto, calidad graduada del ranking y cobertura media, sin añadir coste de modelo más allá de ejecutar ambos recuperadores. La mejora respalda la complementariedad de las señales léxica y semántica.

La conclusión sigue limitada por el tamaño del golden set y por el origen de los juicios. Los qrels pooled se construyeron a partir de BM25 y dense, y la adjudicación humana se concentró en candidatos de riesgo. Como RRF no aporta documentos fuera de ese pool, su evaluación no introduce nuevos juicios, pero tampoco elimina el sesgo hacia los dos recuperadores de origen. El siguiente contraste metodológicamente útil es un reranker aplicado a un conjunto de candidatos explícitamente fijado.
