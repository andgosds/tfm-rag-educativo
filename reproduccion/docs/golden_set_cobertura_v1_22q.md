# Cobertura del golden set piloto y dimensiones de análisis

## Alcance y procedencia

Inventario de las 22 preguntas del piloto, sus evidencias canónicas y los qrels pooled. La conducta esperada incorpora las resoluciones adjudicadas de premisas falsas. No se modifican preguntas, qrels ni adjudicaciones. Tema, resumen, explicitud y ausencia de cálculo solicitado son propuestas del asistente pendientes de revisión humana; los demás campos se derivan de los archivos originales. Los hashes de entrada están en golden_set_cobertura_v1_22q_provenance.json. No se han usado los resultados de los recuperadores ni las respuestas generadas para asignar etiquetas. El análisis es retrospectivo: no constituye una hipótesis preregistrada.

## Tabla por pregunta

IS = Introductory Statistics 2e; DS = Principles of Data Science. Las secciones son las de evidencia canónica, salvo las correcciones, donde se muestran evidencias de contradicción. Un guion no demuestra ausencia de contexto relacionado.

| ID | Contenido (resumen propuesto) | Tipo | Conducta | Chunks canónicos | Secciones de evidencia | Grados 1 / 2 pooled |
|---|---|---|---|---:|---|---:|
| q-v1-001 | Efecto del tamaño muestral | Explicativa | Responder | 1 | IS 7.1 | 2 / 6 |
| q-v1-002 | Errores de tipo I y II | Comparativa | Responder | 1 | IS 9.2 | 6 / 4 |
| q-v1-003 | Pasos de un contraste | Procedimental | Responder | 1 | DS 4.2 | 4 / 8 |
| q-v1-004 | Robustez de la mediana | Explicativa | Responder | 1 | DS 3.1 | 0 / 4 |
| q-v1-005 | Interpretación de la correlación | Factual | Responder | 1 | DS 4.3 | 3 / 3 |
| q-v1-006 | Nivel de confianza y anchura | Comparativa | Responder | 1 | DS 4.1 | 3 / 3 |
| q-v1-007 | Correlación de un caso no documentado | Factual | Abstenerse | — | — | 1 / 0 |
| q-v1-008 | Premisa falsa sobre error estándar | Explicativa | Corregir premisa | — | IS 7.1, IS 7.3 | 2 / 3 |
| q-v1-009 | Pearson frente a Spearman | Comparativa | Abstenerse | — | — | 6 / 0 |
| q-v1-010 | Intervalo creíble bayesiano | Procedimental | Abstenerse | — | — | 0 / 0 |
| q-v1-011 | Normal estándar y z-score | Factual | Responder | 1 | IS 6.1 | 1 / 3 |
| q-v1-012 | Tamaño muestral y margen de error | Explicativa | Responder | 1 | IS 8.1 | 2 / 4 |
| q-v1-013 | Normal frente a t de Student | Comparativa | Responder | 2 | IS 8.1, IS 8.2 | 3 / 12 |
| q-v1-014 | Detección de atípicos mediante IQR | Procedimental | Responder | 2 | DS 3.3 | 1 / 3 |
| q-v1-015 | Media, media recortada y mediana | Comparativa | Responder | 2 | DS 3.1 | 0 / 6 |
| q-v1-016 | Discretas frente a continuas | Comparativa | Responder | 1 | DS 3.5 | 1 / 6 |
| q-v1-017 | Uso e hipótesis de ANOVA | Procedimental | Responder | 2 | DS 4.4 | 1 / 4 |
| q-v1-018 | Concepto no definido en el corpus | Factual | Abstenerse | — | — | 1 / 0 |
| q-v1-019 | p-valor no documentado | Factual | Abstenerse | — | — | 1 / 0 |
| q-v1-020 | Premisa falsa sobre anchura del intervalo | Explicativa | Corregir premisa | — | IS 8.1, DS 4.1 | 4 / 3 |
| q-v1-021 | ANOVA frente a Kruskal–Wallis | Comparativa | Abstenerse | — | — | 5 / 0 |
| q-v1-022 | Procedimiento chi-cuadrado | Procedimental | Abstenerse | — | — | 0 / 0 |

## Cobertura del corpus por capítulo

Se cuentan preguntas respondibles con evidencia canónica en cada capítulo, no todas las menciones temáticas. Un capítulo sin evidencia canónica seleccionada no implica ausencia de contenido útil.

| Libro y capítulo | Título | Chunks del corpus | Preguntas respondibles con evidencia canónica |
|---|---|---:|---:|
| IS 6 | The Normal Distribution | 23 | 1 |
| IS 7 | The Central Limit Theorem | 31 | 1 |
| IS 8 | Confidence Intervals | 43 | 2 |
| IS 9 | Hypothesis Testing with One Sample | 42 | 1 |
| DS 3 | Descriptive Statistics: Statistical Measurements and Probability Distributions | 58 | 4 |
| DS 4 | Inferential Statistics and Regression Analysis | 91 | 4 |

## Lectura de cobertura

- Conducta: 13 respuestas ordinarias, dos correcciones fundamentadas y siete abstenciones. No juntar las nueve preguntas no respondibles en una sola conducta.
- Entre las respondibles, nueve tienen un chunk canónico y cuatro tienen varios. Tres conjuntos multichunk están en una misma sección y uno cruza secciones. Esto describe la anotación existente, no demuestra que sean conjuntos mínimos globales frente a todas las alternativas del pool.
- La explicitud conceptual propuesta distingue dos preguntas que describen el concepto sin nombrarlo: q-v1-014 y q-v1-016. Las otras veinte nombran el objeto principal. Es una rúbrica estrecha, no una medida de dificultad ni de similitud léxica.
- Ninguna pregunta solicita ejecutar un cálculo numérico con datos aportados. Hablar de fórmulas, porcentajes o procedimientos no equivale a pedir un cálculo. Etiqueta propuesta pendiente de revisión.
- Hay familias temáticas relacionadas: 001/008; 006/012/013/020; 004/015; 005/007/009; 017/021. Conviene anotar esta dependencia antes de ampliar: compartir tema no equivale a ser variantes semánticamente equivalentes.

## Dimensiones recomendadas

| Dimensión | Regla de anotación | Utilidad y cautela |
|---|---|---|
| Tema y familia informativa | Tema principal y, por separado, familia de preguntas relacionadas. La pertenencia a variantes exige equivalencia revisada. | Cobertura y dependencia entre preguntas; no asumir independencia de variantes. |
| Explicitud conceptual | Explícita: nombra el concepto central. Implícita: lo describe sin nombrarlo. Mixta: varios conceptos principales y solo algunos nombrados. | Hipótesis exploratoria sobre recuperación léxica/semántica. No confundir con solapamiento de palabras. |
| Estructura de evidencia | Derivar número de chunks, secciones y documentos del conjunto canónico. Revisar alternativas suficientes antes de afirmar necesidad multichunk. | Distinguir localización de evidencia de integración; no llamar multi-hop a cualquier caso multichunk. |
| Componentes requeridos de respuesta | Lista de proposiciones o pasos mínimos, cada uno enlazado a evidencia. El número se deriva de esa lista. | Conectar cobertura de evidencia con completitud de respuesta y diagnosticar omisiones. Requiere revisión de granularidad. |
| Aplicación y cálculo | Separar aplicar a un caso concreto (sí/no) de ejecutar un cálculo numérico (sí/no). | Distinguir explicar un procedimiento de ejecutarlo; no usar una escala vaga de dificultad. |

### La dimensión más útil para conectar IR y generación

Anotar componentes requeridos y su respaldo permite distinguir: (a) se recuperó evidencia de todos los componentes; (b) la respuesta expresó todos los componentes. Así puede identificarse una omisión del generador aunque el contexto sea suficiente, o una limitación de recuperación. Esta comparación es diagnóstica, no una identificación causal automática.

Ejemplo propuesto para q-v1-013: elegir normal cuando se conoce la desviación poblacional; elegir t cuando se estima con la desviación muestral; indicar n−1 grados de libertad y las condiciones pertinentes. La rúbrica definitiva debe decidir si condiciones y explicación de grados de libertad son componentes separados, sin cambiarla tras ver respuestas.

Guardar estas anotaciones en un archivo complementario unido por qid, con versión de rúbrica, autor, estado de revisión y justificación. No sustituir el gold_answer ni promover propuestas a adjudicaciones humanas. Para abstenciones, componentes factuales de respuesta es no aplicable; evaluar conducta y justificación por separado. En correcciones, definir componentes de rechazo y corrección con evidencia de contradicción.

## Qué no añadir como etiqueta principal todavía

- Dificultad fácil/media/difícil: mezcla conocimiento previo, explicitud, integración y esfuerzo de cálculo; no está validada con estudiantes.
- Nivel académico o Bloom: exigirían un marco y anotación adicional; no se deducen del tipo factual/procedimental.
- Dificultad basada en fallos de BM25 o del generador: circular si después se usa para explicar esos mismos fallos.
- Solapamiento léxico alto/bajo manual: si interesa, calcular una medida reproducible sobre la pregunta y evidencia fijada, declarar tokenización y tratarla como variable continua exploratoria. No sustituye la explicitud.

## Uso en el análisis y siguiente paso

Revisar primero la tabla y las etiquetas propuestas. Después anotar componentes de respuesta y familias informativas. Seleccionar nuevas preguntas por huecos temáticos y demandas de aplicación, manteniendo corpus y protocolo. No forzar una cuota para cada combinación: el piloto no permite cruces de muchas dimensiones.

Mostrar tamaño de cada grupo, resultados por pregunta y diferencias emparejadas entre estrategias. Reservar las etiquetas nuevas para análisis descriptivo exploratorio; no elegir umbrales según qué separación mejora una técnica. La estructura canónica se analiza sobre respondibles y las conductas se mantienen separadas. En variantes, la unidad independiente es la pregunta base.

Los recuentos de grados 1/2 son juicios positivos conocidos del pool, no número de evidencias necesarias ni relevancia exhaustiva. Precision y Recall pueden verse afectadas por qrels incompletos y redundancia; la cobertura de componentes propuesta complementa estas métricas sin reemplazarlas.
