# Lote 11 — validación humana del arbitraje (casos 101–110)

## CASO 101 — q-v1-011__implicit · qwen3.5:4b · dense
**Disputa:** behavior_ok
**Pregunta:** For the normal distribution in its reference form, what values define its center and spread, and how should the sign and magnitude of its standardized score be interpreted?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The center of the normal distribution is defined by its mean (μ), and the spread is defined by its standard deviation (σ). A standardized score (z-score) indicates how many standard deviations a value is from the mean; a positive sign means the value is above the mean, while a negative sign means it is below.
**Citas declaradas:** openstax_principles_ds:3.5:chunk-014, openstax_intro_stats_2e:6.intro:chunk-001
**Referencia:** The standard normal distribution has mean 0 and standard deviation 1. A z-score states how many standard deviations a value lies from the mean: a positive score is above the mean, a negative score is below it, and zero corresponds to the mean.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Explica qué representan μ, σ y el z-score, pero omite los valores 0 y 1 que definen la distribución normal estándar.
  - B: Todo lo afirmado está respaldado por los contextos, pero responde con los parámetros generales (μ, σ) en vez de los valores 0 y 1 de la forma de referencia que pide la pregunta, con lo que s
  - Árbitro: La respuesta explica los parámetros y el z-score, pero omite los valores 0 y 1 solicitados para la forma de referencia, un componente material de la pregunta.

---

## CASO 102 — q-v1-011__implicit · qwen3.5:9b · rerank
**Disputa:** factual_correctness
**Pregunta:** For the normal distribution in its reference form, what values define its center and spread, and how should the sign and magnitude of its standardized score be interpreted?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** For the reference (standard) normal distribution, the center is defined by a mean of 0 and the spread by a standard deviation of 1; a standardized score (z-score) indicates how many standard deviations a value lies above (positive sign) or below (negative sign) the mean.
**Citas declaradas:** openstax_principles_ds:3.5:chunk-014, openstax_intro_stats_2e:6.1:chunk-002
**Referencia:** The standard normal distribution has mean 0 and standard deviation 1. A z-score states how many standard deviations a value lies from the mean: a positive score is above the mean, a negative score is below it, and zero corresponds to the mean.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `2`**
  - A: Describe correctamente la normal estándar y las puntuaciones positivas y negativas, pero no menciona el caso cero.
  - B: Interpreta correctamente la forma de referencia como la normal estándar y reproduce la definición de z-score del contexto, con citas que apuntan a esa evidencia.
  - Árbitro: Identifica correctamente la normal estándar y explica los valores de sus parámetros y el significado del z-score; el caso cero queda implícito en la distancia a la media y no altera la coincidencia esencial con la referencia.

---

## CASO 103 — q-v1-012__implicit · gemma4:e4b · rrf
**Disputa:** factual_correctness
**Pregunta:** With confidence level and population variability held constant, how does a larger sample affect the error bound and the width of the range estimated from sample data for a population parameter?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The premise that the contexts describe how a larger sample affects the error bound and the width of the range is partially correct, but the provided contexts state that as the sample size increases, the margin of error will decrease, resulting in a narrower confidence interval.
**Citas declaradas:** openstax_principles_ds:4.1:chunk-010
**Referencia:** A larger sample decreases the error bound and therefore makes the confidence interval narrower, provided that the confidence level and population variability remain fixed.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `2`**
  - A: Describe bien la disminución del error y de la anchura, pero presenta injustificadamente la premisa como solo parcialmente correcta.
  - B: La sustancia (n mayor reduce el error y estrecha el intervalo) es correcta y está respaldada por chunk-010, pero la respuesta se enmarca como corrección de una premisa inexistente y su frase
  - Árbitro: Coincide con la referencia en los dos efectos solicitados, menor margen de error e intervalo más estrecho; el preámbulo injustificado no altera esa conclusión.

---

## CASO 104 — q-v1-013__explicit · qwen3.5:4b · rrf
**Disputa:** citations_ok
**Pregunta:** Which distribution should be used to construct a confidence interval for a population mean when the population standard deviation is known versus when it is estimated by the sample standard deviation, and how do degrees of freedom enter the latter case?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** When the population standard deviation is known, use the normal distribution; when it is estimated by the sample standard deviation, use the Student's t-distribution with degrees of freedom equal to n – 1.
**Citas declaradas:** openstax_intro_stats_2e:8.2:chunk-006, openstax_principles_ds:4.1:chunk-011, openstax_intro_stats_2e:8.2:chunk-003
**Referencia:** Use the normal distribution when the population standard deviation is known. When it is unknown and estimated by the sample standard deviation, use Student's t-distribution. For a simple random sample from an approximately normal population, the t-distribution has n − 1 degrees of freedom, which determine its exact shape.
- **citations_ok** — A: `0` · B: `1` → **árbitro: `0`**
  - A: La distinción normal/t y los n − 1 grados son correctos, pero las citas declaradas no sustentan el caso de desviación poblacional conocida.
  - B: Cubre normal con σ conocida, t de Student con s y df = n−1, todo presente en las tres citas; la conducta real es de respuesta, que es lo esperado, pese a la etiqueta declarada.
  - Árbitro: Las citas declaradas sustentan el uso de t y sus grados de libertad, pero el respaldo explícito para usar la normal con desviación poblacional conocida aparece en 4.1:chunk-025/026, que no se citan.

---

## CASO 105 — q-v1-013__implicit · qwen3.5:4b · bm25
**Disputa:** citations_ok
**Pregunta:** Which distribution should be used to construct a confidence interval for a population mean when the population standard deviation is known versus when it is estimated by the sample standard deviation, and how does the number of deviations that are free to vary enter the latter case?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** When the population standard deviation is known, the normal distribution is used; when it is estimated by the sample standard deviation, the Student's-t distribution is used. The number of deviations that are free to vary in the latter case is determined by the degrees of freedom, which equals the sample size minus one (n - 1).
**Citas declaradas:** openstax_intro_stats_2e:8.intro:chunk-002, openstax_principles_ds:4.2:chunk-011
**Referencia:** Use the normal distribution when the population standard deviation is known. When it is unknown and estimated by the sample standard deviation, use Student's t-distribution. For a simple random sample from an approximately normal population, the t-distribution has n − 1 degrees of freedom, which determine its exact shape.
- **citations_ok** — A: `0` · B: `1` → **árbitro: `0`**
  - A: Responde correctamente, pero los fragmentos recuperados y citados no establecen que los grados de libertad sean n−1.
  - B: Contesta de plano y coincide con la referencia (normal con σ conocida, t con σ estimada, n−1), pero ni la identificación de 'desviaciones libres' con grados de libertad ni df = n−1 aparecen 
  - Árbitro: Las citas respaldan la elección entre normal y t, pero ninguna sostiene la explicación sobre desviaciones libres ni n − 1, un componente explícitamente solicitado.

---

## CASO 106 — q-v1-013__implicit · qwen3.5:4b · rerank
**Disputa:** factual_correctness
**Pregunta:** Which distribution should be used to construct a confidence interval for a population mean when the population standard deviation is known versus when it is estimated by the sample standard deviation, and how does the number of deviations that are free to vary enter the latter case?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** When the population standard deviation is known, use the normal distribution; when it is estimated by the sample standard deviation, use the Student's-t distribution because the sample mean and sample standard deviation are both statistics that vary from sample to sample. The number of deviations free to vary in the latter case is n - 1 (degrees of freedom), which determines the shape of the t-distribution used for the confidence interval.
**Citas declaradas:** openstax_intro_stats_2e:8.intro:chunk-002, openstax_intro_stats_2e:8.intro:chunk-003
**Referencia:** Use the normal distribution when the population standard deviation is known. When it is unknown and estimated by the sample standard deviation, use Student's t-distribution. For a simple random sample from an approximately normal population, the t-distribution has n − 1 degrees of freedom, which determine its exact shape.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `2`**
  - A: Responde a los tres puntos, pero los fragmentos citados no establecen n − 1 ni que ese valor determine la forma de t; además, la explicación causal es imprecisa.
  - B: La idea principal (normal vs t) se sostiene, pero el detalle df = n − 1 y la justificación de que ambos estadísticos varían no aparecen en el contexto recuperado, y las citas 8.intro:chunk-0
  - Árbitro: Coincide con la referencia en la elección de normal frente a t y en que los n − 1 grados de libertad determinan su forma; la justificación poco precisa no invalida esos elementos esenciales.

---

## CASO 107 — q-v1-013__implicit · qwen3.5:9b · dense
**Disputa:** citations_ok
**Pregunta:** Which distribution should be used to construct a confidence interval for a population mean when the population standard deviation is known versus when it is estimated by the sample standard deviation, and how does the number of deviations that are free to vary enter the latter case?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** When the population standard deviation is known, use the normal distribution; when it is estimated by the sample standard deviation, use the Student's-t distribution. The number of deviations free to vary (degrees of freedom) in the latter case equals n - 1, where n is the sample size.
**Citas declaradas:** openstax_intro_stats_2e:8.intro:chunk-002, openstax_intro_stats_2e:8.1:chunk-003, openstax_principles_ds:4.1:chunk-011
**Referencia:** Use the normal distribution when the population standard deviation is known. When it is unknown and estimated by the sample standard deviation, use Student's t-distribution. For a simple random sample from an approximately normal population, the t-distribution has n − 1 degrees of freedom, which determine its exact shape.
- **citations_ok** — A: `0` · B: `1` → **árbitro: `1`**
  - A: La respuesta acierta y realmente responde pese a su etiqueta, pero el valor n − 1 no consta legible en los fragmentos citados.
  - B: Actúa como respuesta correcta (la etiqueta declarada grounded_correction no se corresponde con lo que hace, y no hay premisa falsa que corregir), pero la explicación sobre desviaciones libre
  - Árbitro: Las citas corresponden a la evidencia sobre la distribución normal, la t y sus grados de libertad; la ausencia de una fórmula legible para n − 1 limita la fidelidad, pero no convierte las citas en referencias ajenas a la evidencia utilizada.

---

## CASO 108 — q-v1-014__implicit · gemma4:e4b · dense
**Disputa:** factual_correctness
**Pregunta:** What sequence should be followed to flag unusually low or high observations using the middle 50% of an ordered dataset?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The context states that the interquartile range (IQR) is calculated using the first quartile ($Q_1$) and the third quartile ($Q_3$), which represent the middle 50% of the data, and that the process involves finding the middle value of the lower half ($Q_1$) and the middle value of the upper half ($Q_3$) after finding the median ($Q_2$) [openstax_principles_ds:3.3:chunk-004].
**Citas declaradas:** openstax_principles_ds:3.3:chunk-004
**Referencia:** Order the data and determine the first and third quartiles. Compute the interquartile range as the difference between the third and first quartiles, use the quartiles and a 1.5-IQR cutoff to define lower and upper bounds, and flag values below the lower bound or above the upper bound for further investigation.
- **factual_correctness** — A: `1` · B: `0` → **árbitro: `1`**
  - A: Explica cómo localizar los cuartiles, pero no establece límites ni indica cómo señalar observaciones inusuales.
  - B: Solo describe cómo calcular los cuartiles e IQR y nunca aborda la detección de atípicos, que es lo preguntado; lo que afirma sí está respaldado por el chunk citado.
  - Árbitro: Describe correctamente la obtención de los cuartiles como parte del procedimiento solicitado, pero deja la respuesta incompleta al omitir la diferencia Q3 − Q1, los límites de 1,5 IQR y la identificación de valores fuera de ellos.

---

## CASO 109 — q-v1-014__implicit · qwen3.5:4b · dense
**Disputa:** citations_ok
**Pregunta:** What sequence should be followed to flag unusually low or high observations using the middle 50% of an ordered dataset?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** To flag unusually low or high observations (outliers), calculate the interquartile range (IQR) by subtracting the first quartile from the third quartile, then compare data points to these bounds; the provided contexts do not specify the exact numerical thresholds for flagging outliers.
**Citas declaradas:** openstax_principles_ds:3.3:chunk-004
**Referencia:** Order the data and determine the first and third quartiles. Compute the interquartile range as the difference between the third and first quartiles, use the quartiles and a 1.5-IQR cutoff to define lower and upper bounds, and flag values below the lower bound or above the upper bound for further investigation.
- **citations_ok** — A: `0` · B: `1` → **árbitro: `1`**
  - A: Calcula el IQR, pero no define los límites ni el corte de 1,5 IQR; la única cita tampoco respalda esos límites.
  - B: Solo aporta el cálculo del IQR y remite a unos 'bounds' que nunca define, omitiendo el componente material de la referencia (límites con corte de 1,5·IQR y regla de marcado), aunque no contr
  - Árbitro: La cita respalda la definición del IQR y su uso para señalar posibles atípicos; la respuesta reconoce que faltan los umbrales y no atribuye al fragmento ningún corte numérico.

---

## CASO 110 — q-v1-014__implicit · qwen3.5:9b · rerank
**Disputa:** behavior_ok
**Pregunta:** What sequence should be followed to flag unusually low or high observations using the middle 50% of an ordered dataset?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** To flag unusually low or high observations, calculate the Interquartile Range (IQR), which is the difference between the third quartile ($Q_3$) and the first quartile ($Q_1$). Then, determine lower and upper bounds using the formulas $Q_1 - 1.5 \times IQR$ and $Q_3 + 1.5 \times IQR$. Any data values below the lower bound or above the upper bound are flagged as outliers.
**Citas declaradas:** openstax_principles_ds:3.3:chunk-005
**Referencia:** Order the data and determine the first and third quartiles. Compute the interquartile range as the difference between the third and first quartiles, use the quartiles and a 1.5-IQR cutoff to define lower and upper bounds, and flag values below the lower bound or above the upper bound for further investigation.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Da los límites y la regla para señalar valores, pero omite el paso de determinar los cuartiles y la investigación posterior.
  - B: El procedimiento de cotas es correcto y está respaldado por 3.3:chunk-005, pero la secuencia queda incompleta: no incluye ordenar los datos ni determinar Q1 y Q3 como pasos iniciales, que la
  - Árbitro: Explica el IQR, las cotas y el marcado de valores, pero omite cómo determinar Q1 y Q3, un paso material de la secuencia solicitada que los fragmentos 3.3:chunk-003 y 3.3:chunk-004 sí describen.