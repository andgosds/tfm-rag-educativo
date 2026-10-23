# Dense retrieval con E5-base-v2 sobre 22 preguntas

## Alcance

La ejecución `dense_e5_base_v2_22q` compara una condición de recuperación densa con el baseline `bm25_v1_22q` sobre la misma colección congelada, las mismas 22 preguntas adjudicadas y los mismos qrels independientes del método. Trece preguntas son respondibles y nueve no respondibles.

El recuperador utiliza `intfloat/e5-base-v2`, un encoder en inglés con revisión fijada a `f52bf8ec8c7124536f0efb74aca902b2995e5bcd`. Los documentos se codifican con el prefijo `passage: ` y las consultas con `query: `. Los embeddings se normalizan y se comparan mediante producto escalar.

Precision, Recall y MRR consideran relevante solo el grado 2. nDCG utiliza la escala 0/1/2. La evaluación es provisional porque los 24 juicios conocidos siguen sin constituir un pool exhaustivo del corpus.

## Entorno y configuración

| Parámetro | Valor |
|---|---|
| Modelo | `intfloat/e5-base-v2` |
| Revisión | `f52bf8ec8c7124536f0efb74aca902b2995e5bcd` |
| Dimensión | 768 |
| Idioma | inglés |
| Campo documentado | `retrieval_text` |
| Prefijo de documento | `passage: ` |
| Prefijo de consulta | `query: ` |
| Normalización | sí |
| Longitud máxima | 512 tokens |
| Batch size | 16 |
| Dispositivo | RTX 2060 SUPER, CUDA |
| Búsqueda | exhaustiva sobre 288 vectores |
| Top-k | 10 |

El entorno está separado del Python 3.14 del proyecto en `environments/dense`, con Python 3.12, PyTorch, Sentence Transformers y NumPy fijados mediante `uv.lock`. No se utiliza FAISS porque una matriz de 288 vectores permite una búsqueda exacta y transparente.

## Truncación

El modelo admite como máximo 512 tokens. La auditoría de entrada detectó 15 chunks que superan ese límite y ninguna pregunta truncada. No se ha cambiado el chunking ni se han reconstruido esos textos. La truncación forma parte de esta condición dense y queda registrada en el resumen del run.

Ninguno de los qrels conocidos de grado 1 o 2 pertenece a esos 15 chunks truncados. Por tanto, la evaluación actual no pierde directamente una evidencia juzgada por este motivo, aunque la limitación debe mantenerse como amenaza a la validez para chunks no anotados.

## Resultados agregados

| Métrica | $k=5$ | $k=10$ |
|---|---:|---:|
| Precision | 0,1692 | 0,1231 |
| Recall | 0,5897 | 0,8205 |
| MRR | 0,5000 | 0,5305 |
| nDCG | 0,4673 | 0,5508 |

Dense recupera algún chunk de grado 2 en top-5 para nueve de las trece preguntas respondibles y en top-10 para doce. Recupera todos los grados 2 conocidos en top-5 para siete preguntas y en top-10 para nueve.

## Comparación provisional con BM25

| Métrica | BM25 @5 | Dense @5 | BM25 @10 | Dense @10 |
|---|---:|---:|---:|---:|
| Precision | 0,1538 | **0,1692** | **0,1308** | 0,1231 |
| Recall | 0,4615 | **0,5897** | **0,8590** | 0,8205 |
| MRR | 0,3333 | **0,5000** | 0,4038 | **0,5305** |
| nDCG | 0,3408 | **0,4673** | 0,4916 | **0,5508** |

En estos qrels, dense mejora la posición y calidad del primer acierto, especialmente en top-5, y obtiene mayor MRR y nDCG. BM25 conserva mayor Recall@10 y recupera algún grado 2 en las trece preguntas, frente a doce en dense. Estas diferencias son descriptivas: no constituyen todavía una conclusión de superioridad porque el pool de relevancia no es exhaustivo y solo contiene 13 consultas evaluables.

## Resultados por pregunta

| QID | Grados 2 | Rangos completos | Recall@10 |
|---|---:|---|---:|
| q-v1-001 | 1 | 3 | 1,00 |
| q-v1-002 | 1 | 1 | 1,00 |
| q-v1-003 | 1 | 2 | 1,00 |
| q-v1-004 | 1 | 3 | 1,00 |
| q-v1-005 | 1 | 7 | 1,00 |
| q-v1-006 | 1 | 1 | 1,00 |
| q-v1-011 | 1 | 9 | 1,00 |
| q-v1-012 | 2 | 1, 3 | 1,00 |
| q-v1-013 | 3 | 1, 13, 25 | 0,33 |
| q-v1-014 | 3 | 3, 7, 14 | 0,67 |
| q-v1-015 | 3 | 7, 9, 74 | 0,67 |
| q-v1-016 | 2 | 11, 33 | 0,00 |
| q-v1-017 | 2 | 1, 5 | 1,00 |

Dense mejora claramente q-v1-012, al recuperar las dos evidencias directas en las posiciones 1 y 3. También adelanta una evidencia de q-v1-013 a la primera posición, aunque deja las otras dos en 13 y 25. En q-v1-016 ocurre el fallo más llamativo: BM25 recuperaba los dos chunks de grado 2 en posiciones 1 y 2, mientras que dense no recupera ninguno en top-10.

El caso q-v1-015 muestra una limitación distinta: dense recupera dos evidencias en 7 y 9, pero deja una tercera en el rango 74. El resultado confirma que la recuperación semántica tampoco garantiza por sí sola la cobertura completa de conjuntos multichunk.

## Abstención y scores

Dense devuelve candidatos para las nueve preguntas no respondibles. Sus scores de similitud coseno están en una escala muy comprimida y se solapan entre grupos. En consecuencia, el valor absoluto del coseno y el margen entre los dos primeros candidatos no deben interpretarse como confianza calibrada ni como política de abstención.

El contraste con BM25 es metodológicamente útil: la señal densa cambia de escala, pero no resuelve automáticamente la identificación de preguntas no respondibles. La abstención requerirá una señal específica de suficiencia, una calibración sobre datos separados o una regla evaluada mediante cobertura y riesgo selectivo.

## Eficiencia observada

| Indicador | Resultado |
|---|---:|
| Carga del modelo | 12,46 s |
| Codificación de 288 chunks | 5,69 s |
| 22 consultas | 143,98 ms |
| Media por consulta | 6,54 ms |
| Coste de API | 0 |

La latencia online medida incluye la codificación individual de cada pregunta y la búsqueda exacta sobre los 288 vectores, pero no la carga del modelo ni la codificación offline del corpus. Las cifras proceden de una ejecución local en GPU y deben compararse con BM25 teniendo en cuenta que utilizan hardware y operaciones diferentes.

## Reproducibilidad

Una segunda ejecución en GPU reprodujo los embeddings, rankings, scores, qrels y métricas de calidad dentro de una tolerancia de $10^{-6}$. Las latencias se excluyeron de la comparación. La revisión del modelo, los hashes del corpus y del golden set se almacenan en los metadatos del embedding.

Hashes SHA-256 de la ejecución documentada:

| Artefacto | SHA-256 |
|---|---|
| `dense/pyproject.toml` | `e3b82e43e155b3382a9816ba9e44c02f400c537c14296d5fabd0716eda79c3b8` |
| `dense/uv.lock` | `f082efc815e88a8bc03ec4b01e52cca7d90af0d16ee42d708f45440ac8e33c9d` |
| `dense_e5_base_v2_22q_documents.npy` | `744672a4b94a1bce8729e51c187cf77a87fcc1c536e2a3201c91d6acbc439b73` |
| `dense_e5_base_v2_22q_metadata.json` | `fea9411919937fd4cff254c4b3243161c13bfd943617622137adc9cbe94f3665` |
| `dense_e5_base_v2_22q_metrics.csv` | `a27415eb720db4bacd49ce24a6a67d237f28ed8bab8a9f096478f043e3abb04a` |
| `dense_e5_base_v2_22q_summary.json` | `640c0add9ed03c1d4ceac60c7305948546cddd36b3c73e611d7ceaf7057e9fc8` |

## Artefactos

| Artefacto | Función |
|---|---|
| `../environments/dense/pyproject.toml` | Dependencias del entorno aislado |
| `../environments/dense/uv.lock` | Resolución reproducible de dependencias |
| `../scripts/run_dense.py` | Encoder E5, ranking exacto y CLI |
| `../outputs/embeddings/dense_e5_base_v2_22q_documents.npy` | Embeddings normalizados de los 288 chunks |
| `../outputs/embeddings/dense_e5_base_v2_22q_metadata.json` | Modelo, revisión, truncación y hashes de entrada |
| `../outputs/runs/dense_e5_base_v2_22q.jsonl` | Ranking top-10 de las 22 consultas |
| `../outputs/metrics/dense_e5_base_v2_22q_metrics.csv` | Métricas agregadas |
| `../outputs/metrics/dense_e5_base_v2_22q_per_query.csv` | Métricas, scores y latencias por consulta |
| `../outputs/metrics/dense_e5_base_v2_22q_summary.json` | Configuración y tiempos |
| `../outputs/metrics/dense_e5_base_v2_22q_audit.json` | Rangos completos y qrels truncados |
| `../outputs/metrics/retrieval_comparison_bm25_dense_22q.json` | Comparación provisional entre métodos |

## Siguiente paso metodológico

El siguiente paso no debe ser declarar un ganador, sino construir un pool conjunto BM25+dense. Se combinarán sus candidatos top-10 o top-20, se eliminarán duplicados y se revisarán de forma independiente con el origen del candidato oculto. Después se recalcularán ambos métodos sobre qrels ampliados.
