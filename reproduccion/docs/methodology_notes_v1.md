# Notas metodológicas v1

## 2026-08-17 — Ejecución temprana de BM25

Se decidió ejecutar BM25 después de adjudicar el primer lote de diez preguntas y antes de ampliar el golden set a 20–30. El objetivo no era obtener una estimación definitiva, sino comprobar el pipeline completo y utilizar errores reales para orientar la siguiente fase de anotación.

La ejecución confirmó que el diseño funciona de extremo a extremo: corpus congelado, preguntas adjudicadas, qrels, run top-10 y métricas agregadas. BM25 recuperó los seis chunks canónicos en top-10, pero solo dos en top-5. Los rangos fueron 6, 1, 4, 6, 6 y 6.

La lectura manual mostró que varios resultados no juzgados contienen evidencia parcial o potencialmente suficiente. Esto no debe corregirse añadiendo juicios obtenidos únicamente del run de BM25, porque introduciría una ventaja retrospectiva para el baseline. La vía metodológica adecuada es conservar las métricas canónicas como resultado preliminar y ampliar los qrels más adelante mediante pooling de varios recuperadores o revisión independiente con procedencia explícita.

Las cuatro preguntas no respondibles recibieron scores y candidatos plausibles. Los intervalos de score máximo y margen se solapan con los de las preguntas respondibles, por lo que no se adoptará un umbral de abstención basado únicamente en BM25. Cualquier política de rechazo deberá combinar señales y evaluarse mediante cobertura y riesgo.

## Decisiones que se mantienen

- `retrieval_text` es la representación indexada para todas las técnicas.
- BM25 usa $k_1=1{,}5$ y $b=0{,}75$ sin ajuste oportunista sobre este lote.
- La tokenización inicial no aplica stemming ni stopwords.
- Las métricas de retrieval excluyen las preguntas sin qrels positivos.
- Los rankings de las preguntas no respondibles se conservan para el análisis de abstención.
- Los resultados actuales son preliminares por el tamaño del lote y la falta de qrels exhaustivos.

## Próxima decisión experimental

Ampliar el golden set aprovechando los errores observados. Conviene incluir más preguntas con bajo solapamiento léxico, evidencia distribuida en varios chunks y cobertura de capítulos todavía infrarepresentados. Después se implementará recuperación densa sobre la misma colección y se construirá un pool conjunto para ampliar los juicios de relevancia sin favorecer a una sola técnica.

## 2026-08-17 — Umbral de relevancia para métricas

Las métricas binarias utilizarán un criterio estricto. Recall@k y MRR@k considerarán relevantes exclusivamente los chunks con grado 2. nDCG@k conservará la escala graduada 0/1/2. Esta decisión evita que recuperar contexto de grado 1, insuficiente para responder, se contabilice como acceso satisfactorio a la evidencia. La implementación deberá actualizarse antes de recalcular BM25 sobre el conjunto ampliado.

## 2026-08-17 — Primera ejecución dense

Se implementó `dense_e5_base_v2_22q` sobre los mismos 288 chunks, 22 preguntas y qrels independientes del método. Se utilizó `intfloat/e5-base-v2`, revisión `f52bf8ec8c7124536f0efb74aca902b2995e5bcd`, prefijos `query:`/`passage:`, embeddings normalizados y búsqueda exacta. La ejecución se realizó en una RTX 2060 SUPER mediante un entorno Python 3.12 separado.

Dense mejora MRR y nDCG frente a BM25 en los cortes 5 y 10, y también Recall@5. BM25 mantiene Recall@10 y recupera algún grado 2 en las 13 preguntas respondibles, mientras dense falla en q-v1-016. Dense tampoco resuelve por sí solo la cobertura multichunk: q-v1-013 recupera una evidencia en rango 1 y deja otras en 13 y 25.

El encoder trunca 15 pasajes por superar 512 tokens, pero ninguno corresponde a un qrel conocido. La comparación sigue siendo provisional. El siguiente paso es crear un pool conjunto BM25+dense con origen oculto, revisar candidatos nuevos y recalcular ambos métodos con qrels ampliados.

## 2026-08-17 — Pool y triage de candidatos

El pool se construyó como la unión determinista de los top-10 de `bm25_v1_22q` y `dense_e5_base_v2_22q`. Contiene 340 candidatos únicos: 220 procedentes de cada run y 100 recuperados por ambos métodos. Diecinueve ya tenían juicio en los qrels actuales y 321 quedaron pendientes.

La copia ciega `data/golden/pool_bm25_dense_blind_v1_22q.jsonl` no contiene scores ni método de origen. El prompt versionado `config/pool_review_prompt_v1.md` se aplicó con GPT y GLM como triage auxiliar. GPT asignó 108 grados 0, 147 grados 1 y 66 grados 2; GLM asignó 62 grados 0, 199 grados 1 y 60 grados 2. Coincidieron exactamente en 200 candidatos y discreparon en 121. Seis candidatos fueron marcados por GPT como posibles conflictos de respondibilidad.

La primera priorización con dos jueces incluyó 163 candidatos. Posteriormente se incorporó un tercer juez independiente, Kimi k3 con razonamiento max. Kimi asignó 173 grados 0, 121 grados 1 y 27 grados 2. Los tres jueces coincidieron en 120 de 321 candidatos, formaron mayoría en 308 y asignaron tres grados distintos en 13. El acuerdo exacto por pares fue 200 para GPT–GLM, 185 para GPT–Kimi y 163 para GLM–Kimi.

La observación de que la adjudicación humana no coincidió con la mayoría automática en tres de los primeros siete casos desaconsejó sustituirla por votación automática. En su lugar se adoptó `three_judge_risk_directed_v1`: revisión de cualquier posible grado 2, de los desacuerdos 0/1/2, de los conflictos de respondibilidad y de una auditoría determinista de diez consensos 0/0/0 y diez consensos 1/1/1. La unión contiene 109 candidatos y quedó cerrada el 2026-08-24 con 14 grados 0, 45 grados 1, 50 grados 2 y 16 evidencias canónicas.

La trazabilidad diferencia 23 decisiones realizadas directamente por el usuario, 70 decisiones delegadas al asistente bajo el criterio explícito 0/1/2 y 16 casos de discrepancia máxima o conflicto de respondibilidad resueltos con consejo del usuario. Esta procedencia impide describir el resultado como acuerdo interanotador humano o como 109 etiquetas humanas independientes. Los consensos no auditados permanecen como señal auxiliar y no se convierten en qrels.

Los prompts utilizados en esta fase son reproducibles y quedan conservados en `config/golden_set_review_prompt_v1.md`, `config/pool_review_prompt_v1.md`, `config/pool_review_prompt_v1_kimi_2026-08-24.md` y `config/kimi_judge3_run_2026-08-24.md`. Las salidas auxiliares y el resumen comparativo se preservan en `data/golden/reviews/`.

## 2026-08-24 — Qrels pooled y reevaluación común

`build_pooled_qrels.py` conserva los 24 qrels originales y añade 95 decisiones positivas adjudicadas. El archivo pooled contiene 119 qrels: 47 de grado 1 y 72 de grado 2. La procedencia y la canonicidad se conservan en un JSONL separado; los 14 grados 0 quedan auditados en el informe, pero no se escriben como qrels positivos.

Seis qrels de grado 2 pertenecen a q-v1-008 y q-v1-020, ambas con una premisa falsa. La revisión independiente mantuvo su etiqueta no respondible y clasificó esos chunks como evidencia de contradicción: el comportamiento esperado es rechazar la premisa y ofrecer una corrección fundamentada. `answerability_resolutions_v1_22q.json` conserva la decisión, las respuestas correctivas de referencia y los seis chunks afectados. Estas consultas permanecen fuera de los agregados ordinarios de retrieval y se reservan para evaluar corrección fundamentada frente a abstención por falta de evidencia.

BM25 y dense se recalcularon con el mismo TSV pooled. Dense alcanza Recall@10 = 0,8301 y nDCG@10 = 0,7491; BM25 obtiene Recall@10 = 0,8077 y nDCG@10 = 0,7052. BM25 conserva mayor MRR, 0,7885 frente a 0,7436, y Precision@10 empata en 0,3923. Dense cubre toda la evidencia de seis consultas en top-10 y BM25 de cinco. El resultado indica complementariedad y justifica la fase híbrida, no un ganador general.

Las métricas absolutas deben interpretarse con cautela porque el pool se formó con los top-10 de los mismos dos sistemas evaluados. La expansión reduce el problema de qrels incompletos, pero puede favorecer a los métodos contribuyentes y no constituye una evaluación exhaustiva de nuevos recuperadores.
