# Benchmark controlado de latencia de retrieval

## Objetivo

El benchmark compara la latencia online de BM25, dense, RRF y RRF con reranking bajo un único proceso y en el mismo hardware. Los índices, embeddings y modelos se cargan antes del calentamiento, por lo que los tiempos no incluyen inicialización ni codificación offline del corpus.

## Protocolo

| Elemento | Configuración |
|---|---|
| Corpus | 288 chunks |
| Preguntas | 22 |
| Profundidad | top-10 |
| Calentamiento | 5 rondas completas, 110 consultas |
| Medición | 30 repeticiones, 660 muestras por condición |
| Orden | aleatorio por ronda, semilla 20260831 |
| Reloj | `time.perf_counter_ns` |
| Ejecución | serial |
| GPU | NVIDIA GeForce RTX 2060 SUPER |
| Sincronización | CUDA antes y después de dense y reranking |
| Dense | E5-base-v2, revisión `f52bf8ec8c7124536f0efb74aca902b2995e5bcd` |
| Reranker | MiniLM-L6-v2, revisión `233902d25c440f23af6f7d6e94d2946bac0bee0a` |

Cada consulta ejecuta las cuatro etapas en el mismo orden: BM25, dense, fusión RRF y reranking. La latencia híbrida serial es la suma de BM25, dense y fusión. La cuarta condición añade el tiempo del cross-encoder. No se presenta una latencia paralela medida, porque el benchmark no ejecuta BM25 y dense de forma concurrente.

## Resultados

| Condición | Media (ms) | Mediana (ms) | p95 (ms) | Desv. estándar (ms) | Mínimo (ms) | Máximo (ms) |
|---|---:|---:|---:|---:|---:|---:|
| BM25 | 2,67 | 2,51 | 3,42 | 0,63 | 1,98 | 5,32 |
| Dense | 6,81 | 6,64 | 7,74 | 0,46 | 6,25 | 9,84 |
| RRF serial | 9,49 | 9,28 | 11,78 | 0,88 | 8,31 | 13,53 |
| RRF + reranker serial | 47,29 | 47,46 | 52,22 | 3,36 | 38,58 | 56,98 |

Los tiempos controlados sustituyen las estimaciones derivadas de los runs individuales. RRF necesita 2,68 ms más que dense y multiplica su latencia media por 1,39. El reranker añade 37,80 ms sobre RRF y multiplica la latencia completa por 4,98.

## Calidad y latencia

| Condición | Recall@10 | MRR@10 | nDCG@10 | Media (ms) | p95 (ms) |
|---|---:|---:|---:|---:|---:|
| BM25 | 0,8077 | 0,7885 | 0,7052 | 2,67 | 3,42 |
| Dense | 0,8301 | 0,7436 | 0,7491 | 6,81 | 7,74 |
| RRF | 0,8846 | 0,8846 | 0,8167 | 9,49 | 11,78 |
| RRF + reranker | 0,8846 | 0,9231 | 0,8483 | 47,29 | 52,22 |

Frente a dense, RRF aumenta Recall@10 en 0,0545, MRR@10 en 0,1410 y nDCG@10 en 0,0676 con 2,68 ms adicionales. Es la mejora marginal más equilibrada del experimento.

El reranker mantiene Recall@10 porque conserva los candidatos. Su ganancia se concentra en el orden: MRR@10 aumenta 0,0385 y nDCG@10 aumenta 0,0316. Esta mejora exige 37,80 ms adicionales por consulta. La ganancia relativa de nDCG@10 es del 3,87 %, mientras la latencia se multiplica casi por cinco.

## Recomendación

RRF es la configuración recomendada cuando se busca equilibrio entre cobertura, orden y latencia. Su p95 queda por debajo de 12 ms en el hardware probado y supera a BM25 y dense en las métricas principales a diez resultados.

RRF con reranking es la mejor configuración si la prioridad es maximizar la calidad del ranking y un p95 cercano a 52 ms es compatible con el servicio. No puede presentarse como opción universalmente preferible porque el estudio no predefinió un umbral de latencia aceptable y su ganancia no aumenta la cobertura a diez resultados.

La recomendación se limita a retrieval. Las métricas actuales no demuestran que RRF o el reranker maximicen por sí solos la corrección y el groundedness de la respuesta generada. Esa parte de la pregunta de investigación requiere una evaluación RAG end-to-end con el generador y el prompt controlados.

## Coste y límites

Las cuatro condiciones se ejecutan localmente, sin coste variable por API. Este dato no equivale a coste cero: dense y reranking requieren GPU, memoria y energía, pero el benchmark no mide consumo eléctrico ni amortización de hardware.

Los tiempos dependen de una RTX 2060 SUPER, un corpus pequeño y batch size 1 para consultas dense. No deben extrapolarse a otro hardware, concurrencia elevada o corpus grande. El pooling también procede de BM25 y dense, por lo que las diferencias de calidad no son una evaluación independiente de esos recuperadores.

## Artefactos

- `scripts/benchmark_retrieval_latency.py`
- `tests/test_benchmark_retrieval_latency.py`
- `outputs/latency/retrieval_latency_controlled_v1_22q_raw.csv`
- `outputs/latency/retrieval_latency_controlled_v1_22q_summary.csv`
- `outputs/latency/retrieval_latency_controlled_v1_22q_summary.json`
