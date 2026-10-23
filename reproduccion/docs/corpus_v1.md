# Corpus v1

## Propósito

El corpus v1 se concentra en un subconjunto técnico de estadística y ciencia de datos que permita evaluar la recuperación y la corrección factual con criterios explícitos. La selección prioriza conceptos con definiciones canónicas, condiciones de aplicación, fórmulas, procedimientos e interpretaciones verificables.

La unidad de procedencia es el libro, pero la inclusión efectiva se define por capítulos y secciones. Los PDF completos se conservan como fuentes brutas inmutables; solo el contenido seleccionado pasará a las etapas de extracción, limpieza y chunking.

## Fuentes seleccionadas

| `doc_id` | Fuente | Capítulos incluidos | Extensión del PDF | Licencia |
|---|---|---|---:|---|
| `openstax_intro_stats_2e` | *Introductory Statistics 2e* | 6–9 | 847 páginas | CC BY-NC-SA 4.0 |
| `openstax_principles_ds` | *Principles of Data Science* | 3–4 | 569 páginas | CC BY-NC-SA 4.0 |

Los metadatos completos, las URL oficiales, las fechas y los hashes se registran en `../config/corpus_sources.csv`.

## Criterios de selección

Las fuentes se incluyen porque cumplen las condiciones siguientes:

1. proceden de una editorial educativa identificable;
2. disponen de una licencia explícita y documentable;
3. pueden obtenerse desde páginas oficiales;
4. contienen una capa de texto extraíble sin OCR;
5. presentan contenido técnico con respuestas verificables;
6. ofrecen suficiente solapamiento temático para comparar estrategias de recuperación;
7. contienen diferencias de redacción, profundidad y organización útiles para el experimento.

Ambos libros están publicados por OpenStax, perteneciente a Rice University. El texto está sujeto a una licencia Creative Commons Attribution-NonCommercial-ShareAlike 4.0. Los logotipos y algunos elementos gráficos de terceros pueden tener condiciones diferentes, por lo que v1 se centrará en el texto y conservará la atribución y procedencia de cada fragmento.

## Subconjunto de *Introductory Statistics 2e*

### Capítulo 6. The Normal Distribution

Introduce la distribución normal estándar, la transformación mediante puntuaciones z y el cálculo e interpretación de probabilidades. El capítulo permite formular preguntas factuales, procedimentales y numéricas con respuestas contrastables.

Se incluyen las secciones 6.1–6.4. En la paginación impresa, el capítulo ocupa aproximadamente las páginas 335–364.

### Capítulo 7. The Central Limit Theorem

Desarrolla la distribución muestral de la media, el error estándar y las condiciones de aplicación del teorema central del límite. Permite evaluar distinciones precisas entre población, muestra, parámetro y estadístico.

Se incluyen las secciones 7.1–7.5. En la paginación impresa, el capítulo ocupa aproximadamente las páginas 365–404.

### Capítulo 8. Confidence Intervals

Cubre intervalos de confianza para medias y proporciones, distribución normal, distribución t de Student y margen de error. Ofrece criterios objetivos para evaluar definiciones, selección de procedimiento, interpretación y cálculos breves.

Se incluyen las secciones 8.1–8.6. En la paginación impresa, el capítulo ocupa aproximadamente las páginas 405–460.

### Capítulo 9. Hypothesis Testing with One Sample

Introduce las hipótesis nula y alternativa, los errores de tipo I y II, el nivel de significación, el p-valor, las reglas de decisión y los contrastes para una media o proporción. Este capítulo es especialmente adecuado para construir preguntas conceptuales y procedimentales con evidencia localizada.

Se incluyen las secciones 9.1–9.6. En la paginación impresa, el capítulo ocupa aproximadamente las páginas 461–510.

## Subconjunto de *Principles of Data Science*

### Capítulo 3. Descriptive Statistics: Statistical Measurements and Probability Distributions

Cubre medidas de centro, variación y posición, teoría de la probabilidad y distribuciones discretas y continuas. Proporciona una formulación más condensada de conceptos relacionados con la distribución normal y la variabilidad.

Se incluyen las secciones 3.1–3.5. En la paginación impresa, el capítulo ocupa aproximadamente las páginas 103–144.

### Capítulo 4. Inferential Statistics and Regression Analysis

Desarrolla inferencia, intervalos de confianza, contraste de hipótesis, correlación, regresión lineal y ANOVA. El solapamiento con los capítulos 8 y 9 de *Introductory Statistics 2e* es deliberado: permite observar cómo responde el retrieval cuando una pregunta dispone de evidencia relevante en dos fuentes con distinta redacción y profundidad.

Se incluyen las secciones 4.1–4.4. En la paginación impresa, el capítulo ocupa aproximadamente las páginas 145–212.

## Contenido incluido

Dentro de los capítulos seleccionados se conservan:

- introducciones de capítulo;
- secciones numeradas;
- definiciones y explicaciones;
- texto matemático cuando la extracción es legible, marcando los posibles fallos;
- ejemplos desarrollados;
- tablas textuales cuando la extracción sea legible;
- fragmentos de código vinculados a la explicación;
- pies de figura necesarios para interpretar el contenido.

## Contenido excluido en v1

Para reducir duplicación, ruido y respuestas sin contexto, inicialmente se excluirán:

- prefacios e índices generales;
- páginas comerciales o institucionales;
- referencias bibliográficas internas;
- soluciones y claves de respuesta;
- tareas, homework y baterías de ejercicios;
- group projects, critical thinking y quantitative problems;
- capítulos no incluidos en la selección;
- logotipos, ilustraciones decorativas y contenido gráfico sin texto interpretable.

Las exclusiones se aplicarán durante la extracción estructurada, no modificando los PDF originales.

## Justificación del alcance técnico

La selección reúne seis capítulos y cubre una secuencia coherente: distribuciones, muestreo, teorema central del límite, estimación, contraste de hipótesis y modelización inferencial básica. Estos contenidos permiten diseñar preguntas cuya corrección puede evaluarse mediante conceptos requeridos, condiciones de aplicación, procedimientos, fórmulas o valores numéricos con tolerancia.

El solapamiento entre los dos libros es metodológicamente útil. Una misma pregunta puede disponer de evidencia relevante en más de un documento, lo que permite evaluar cobertura, ranking y redundancia. Las diferencias de redacción también ofrecen un escenario apropiado para comparar BM25 con recuperadores densos e híbridos en fases posteriores.

Se excluyen de v1 los capítulos introductorios generales, la recogida y preparación de datos, las series temporales, machine learning, deep learning, ética, visualización y reporting. Aunque son contenidos relevantes para ciencia de datos, tienden a producir preguntas más abiertas o ampliar demasiado el dominio del golden set piloto.

## Implicaciones para el golden set

El subconjunto técnico permite combinar varios tipos de preguntas:

1. definiciones y condiciones de aplicación;
2. interpretación de parámetros y resultados;
3. comparación entre procedimientos;
4. selección de la técnica adecuada;
5. cálculos breves con respuesta verificable;
6. preguntas sin evidencia suficiente.

Los cálculos no deben dominar el golden set, porque el objetivo principal sigue siendo evaluar recuperación y fundamentación, no únicamente razonamiento matemático. Para las preguntas numéricas se registrarán el valor esperado, la unidad y una tolerancia. Para las preguntas conceptuales se podrán registrar conceptos obligatorios, variantes aceptables y afirmaciones incompatibles con la respuesta correcta.

## Riesgos de extracción

Las fórmulas, símbolos, tablas y elementos gráficos pueden degradarse durante la extracción del PDF. Antes del chunking se revisó una muestra del corpus para comprobar:

- conservación de símbolos matemáticos;
- orden de lectura;
- separación entre fórmulas y explicación;
- eliminación de encabezados y pies repetidos;
- correspondencia entre página impresa y página del PDF;
- legibilidad de tablas y ejemplos.

Si una fórmula no se extrae de forma fiable, el fragmento deberá corregirse de manera trazable, excluirse o contrastarse con la versión web oficial.

## Limitaciones iniciales

El corpus v1 está compuesto únicamente por fuentes de OpenStax y texto en inglés. Esta homogeneidad facilita la trazabilidad, pero limita la diversidad editorial, lingüística y de estilo. Además, la licencia restringe la reutilización a fines no comerciales y exige compartir las adaptaciones bajo la misma licencia.

El subconjunto favorece contenidos estadísticos con respuestas relativamente canónicas. Por ello, los resultados no podrán generalizarse directamente a preguntas educativas abiertas, explicaciones pedagógicas extensas o dominios menos formalizados. v1 servirá para validar el pipeline y el protocolo de evaluación antes de ampliar el corpus.
