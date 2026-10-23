# Lote 7 — validación humana del arbitraje (casos 61–70)

## CASO 61 — q-v3-005__implicit · qwen3.5:9b · dense
**Disputa:** faithfulness, factual_correctness
**Pregunta:** What does the stated percentage attached to an interval estimate represent?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** The stated percentage represents the probability that the calculated confidence interval will contain the true population parameter when repeated samples are taken; it is not the probability that a specific interval contains the parameter.
**Citas declaradas:** openstax_intro_stats_2e:8.3:chunk-001, openstax_intro_stats_2e:8.1:chunk-002
**Referencia:** It is often taken as the probability that the calculated interval contains the true population parameter, but the more accurate statement is that it is the percentage of confidence intervals that contain the true parameter when repeated samples are taken. Its complement is alpha, the probability that the interval does not contain the parameter, so the two add up to one.
- **faithfulness** — A: `2` · B: `1` → **árbitro: `2`**
  - A: Expresa la interpretación mediante muestras repetidas y descarta la interpretación para un intervalo específico; el fragmento 8.1 la respalda.
  - B: Mantiene el encuadre de muestras repetidas, pero afirma que el porcentaje es 'la probabilidad de que el intervalo calculado contenga el parámetro', que es la formulación que el contexto seña
  - Árbitro: La condición de muestreo repetido y la exclusión explícita de una probabilidad para el intervalo específico sostienen la interpretación frecuentista expuesta en 8.1:chunk-002.
- **factual_correctness** — A: `2` · B: `1` → **árbitro: `2`**
  - A: Expresa la interpretación mediante muestras repetidas y descarta la interpretación para un intervalo específico; el fragmento 8.1 la respalda.
  - B: Mantiene el encuadre de muestras repetidas, pero afirma que el porcentaje es 'la probabilidad de que el intervalo calculado contenga el parámetro', que es la formulación que el contexto seña
  - Árbitro: Leída completa, la respuesta distingue la cobertura bajo muestreo repetido de una probabilidad atribuida al intervalo observado, coincidiendo con lo esencial de la referencia.

---

## CASO 62 — q-v3-006__implicit · qwen3.5:4b · rerank
**Disputa:** faithfulness, factual_correctness
**Pregunta:** How is the regression model used for an outcome that takes only two values fitted, and how are its coefficients interpreted?
**Conducta esperada:** abstain · declarada: grounded_correction
**Respuesta:** The supplied contexts do not describe how a regression model is fitted for an outcome with only two values (binary data); they exclusively discuss linear regression for continuous numeric variables using the least squares method to minimize squared distances. Consequently, the premise that the provided text explains fitting a binary regression model is false.
**Citas declaradas:** openstax_principles_ds:4.3:chunk-002, openstax_principles_ds:4.3:chunk-016
**Referencia:** (sin puntuar)
- **faithfulness** — A: `2` · B: `1` → **árbitro: `1`**
  - A: No inventa un ajuste para resultados binarios, pero acompaña la abstención con afirmaciones sobre regresión lineal.
  - B: Se abstiene en lo esencial, pero desvía el marco al afirmar que 'la premisa es falsa', presupuesto que la pregunta no plantea y que el contexto no sostiene; las citas sí respaldan la descrip
  - Árbitro: El contexto respalda la falta de información sobre regresión binaria, pero no sustenta atribuir a la pregunta la premisa de que los fragmentos explican ese modelo.
- **factual_correctness** — A: `2` · B: `1` → **árbitro: `1`**
  - A: No inventa un ajuste para resultados binarios, pero acompaña la abstención con afirmaciones sobre regresión lineal.
  - B: Se abstiene en lo esencial, pero desvía el marco al afirmar que 'la premisa es falsa', presupuesto que la pregunta no plantea y que el contexto no sostiene; las citas sí respaldan la descrip
  - Árbitro: Con referencia None, reconoce correctamente la insuficiencia del material, pero añade una corrección improcedente: la pregunta solicita un procedimiento y no afirma que el texto lo contenga.

---

## CASO 63 — q-v3-007__explicit · gemma4:e4b · rrf
**Disputa:** faithfulness, factual_correctness
**Pregunta:** By how much does the power of a test increase when the sample size doubles at a fixed significance level?
**Conducta esperada:** grounded_correction · declarada: abstain
**Respuesta:** I cannot answer from the supplied contexts.
**Citas declaradas:** NONE
**Referencia:** (sin puntuar)
- **faithfulness** — A: `2` · B: `1` → **árbitro: `2`**
  - A: Evita dar una cifra sin respaldo, pero no corrige la presuposición de que duplicar la muestra produce un aumento cuantificable fijo de la potencia.
  - B: Chunk-9.2 contiene la relación entre tamaño muestral y potencia (1−β), suficiente para corregir que el aumento no es una cifra fija, y en lugar de corregir se abstiene; la abstención sin cit
  - Árbitro: La abstención no introduce afirmaciones estadísticas sin respaldo y el contexto no permite cuantificar el aumento solicitado; omitir la corrección disponible es un fallo de conducta, no de fidelidad.
- **factual_correctness** — A: `1` · B: `0` → **árbitro: `0`**
  - A: Evita dar una cifra sin respaldo, pero no corrige la presuposición de que duplicar la muestra produce un aumento cuantificable fijo de la potencia.
  - B: Chunk-9.2 contiene la relación entre tamaño muestral y potencia (1−β), suficiente para corregir que el aumento no es una cifra fija, y en lugar de corregir se abstiene; la abstención sin cit
  - Árbitro: No ofrece ninguna respuesta sustantiva ni aclara que el contexto solo establece que aumentar la muestra puede aumentar la potencia, sin determinar una magnitud al duplicarla.

---

## CASO 64 — q-v3-008__explicit · gemma4:e4b · bm25
**Disputa:** factual_correctness, behavior_ok
**Pregunta:** How do discrete and continuous probability distributions relate to the sampling distributions used in statistical inference?
**Conducta esperada:** answer · declarada: abstain
**Respuesta:** I cannot answer from the supplied contexts.
**Citas declaradas:** NONE
**Referencia:** Probability distributions describe the probabilities of the values of a single random variable, which is either discrete, with a finite or countable number of values and typically the result of a count, or continuous, taking any value in an interval. A sampling distribution is built on top of that object: it is the distribution of a statistic computed from repeated samples, and for the mean it approaches a normal distribution as the sample size increases. The second object is therefore a distrib
- **factual_correctness** — A: `0` · B: `1` → **árbitro: `0`**
  - A: Se abstiene por completo pese a que el contexto permite al menos explicar las distribuciones discretas y continuas, como exige la respuesta.
  - B: La abstención es comprensible porque ningún chunk llega a las distribuciones muestrales, pero la conducta esperada era responder y el contexto cubría de sobra la mitad discreta/continua de l
  - Árbitro: La abstención no aporta ningún contenido de la referencia, por lo que no constituye una respuesta esencialmente correcta pero incompleta.
- **behavior_ok** — A: `0` · B: `1` → **árbitro: `0`**
  - A: Se abstiene por completo pese a que el contexto permite al menos explicar las distribuciones discretas y continuas, como exige la respuesta.
  - B: La abstención es comprensible porque ningún chunk llega a las distribuciones muestrales, pero la conducta esperada era responder y el contexto cubría de sobra la mitad discreta/continua de l
  - Árbitro: Aunque falta evidencia sobre distribuciones muestrales, la abstención total no cumple la conducta esperada de responder ni aprovecha la explicación disponible sobre distribuciones discretas y continuas.

---

## CASO 65 — q-v1-001__explicit · gemma4:e4b · rrf
**Disputa:** behavior_ok
**Pregunta:** How does increasing the sample size affect the sampling distribution of the sample mean?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** Increasing the sample size causes the error bound to decrease, making the confidence interval narrower, and it decreases the standard deviation of the sampling distribution of the sample means [openstax_intro_stats_2e:8.1:chunk-011, openstax_principles_ds:4.1:chunk-006].
**Citas declaradas:** openstax_intro_stats_2e:8.1:chunk-011, openstax_principles_ds:4.1:chunk-006
**Referencia:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Describe correctamente la menor dispersión y cita su evidencia, pero omite que la distribución se aproxima a la normal y conserva la media poblacional.
  - B: Todo lo afirmado está respaldado por los chunks citados y responde directamente, pero omite que la distribución se vuelve más normal y conserva la media, que son componentes esenciales de la
  - Árbitro: Explica la reducción de la dispersión, pero omite la aproximación a la normalidad y la conservación de la media poblacional, componentes materiales de la respuesta respaldados por 7.1:chunk-002.

---

## CASO 66 — q-v1-001__explicit · qwen3.5:4b · bm25
**Disputa:** behavior_ok
**Pregunta:** How does increasing the sample size affect the sampling distribution of the sample mean?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** Increasing the sample size decreases the standard error of the mean, which makes the sampling distribution narrower (less spread out).
**Citas declaradas:** openstax_intro_stats_2e:7.1:chunk-003, openstax_intro_stats_2e:8.1:chunk-011
**Referencia:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Explica correctamente la menor dispersión, pero omite que la media se mantiene y que la distribución se aproxima a la normal.
  - B: El efecto sobre la dispersión (menor error estándar, distribución más estrecha) está respaldado por los chunks citados, pero omite dos de los tres efectos de la referencia (tendencia a la no
  - Árbitro: Responde sobre la menor dispersión, pero omite componentes materiales del efecto solicitado: la aproximación a la normalidad y la conservación de la media poblacional, presentes en el contexto y la referencia.

---

## CASO 67 — q-v1-001__explicit · qwen3.5:4b · rerank
**Disputa:** behavior_ok
**Pregunta:** How does increasing the sample size affect the sampling distribution of the sample mean?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** Increasing the sample size decreases the spread (standard deviation) of the sampling distribution of the sample mean, making it narrower and more concentrated around the population mean.
**Citas declaradas:** openstax_intro_stats_2e:7.1:chunk-002, openstax_intro_stats_2e:7.1:chunk-003
**Referencia:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Explica correctamente que disminuye la dispersión, pero omite que la distribución se aproxima a la normal al crecer la muestra.
  - B: Responde en el modo esperado y con evidencia directa (la dispersión disminuye y las medias se concentran en la media poblacional), pero omite la convergencia a la normal, que es un component
  - Árbitro: Responde sobre la disminución de la dispersión, pero omite la aproximación a la normalidad que el fragmento 7.1:chunk-002 y la referencia presentan como otro efecto central del aumento muestral.

---

## CASO 68 — q-v1-001__explicit · qwen3.5:4b · rrf
**Disputa:** behavior_ok
**Pregunta:** How does increasing the sample size affect the sampling distribution of the sample mean?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** Increasing the sample size decreases the error bound and makes the sampling distribution of the sample mean narrower (smaller standard deviation), while the mean of the sample means remains approximately the same.
**Citas declaradas:** openstax_intro_stats_2e:8.1:chunk-011, openstax_intro_stats_2e:7.1:chunk-002
**Referencia:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Acertó al señalar menor dispersión y centro estable, pero omitió la aproximación a la normalidad y la relación σ/√n.
  - B: Todo lo afirmado está respaldado y responde a lo preguntado, pero omite la tendencia a la normalidad y la relación σ/√n de la referencia, e introduce el error bound de intervalos de confianz
  - Árbitro: Responde sobre el centro y la dispersión, pero omite un componente material del efecto solicitado: la aproximación a la normalidad descrita en 7.1:chunk-002.

---

## CASO 69 — q-v1-001__explicit · qwen3.5:9b · dense
**Disputa:** factual_correctness
**Pregunta:** How does increasing the sample size affect the sampling distribution of the sample mean?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** Increasing the sample size causes the sampling distribution of the sample mean to become more normally distributed, reduces its spread (standard deviation), and makes the graph steeper and thinner.
**Citas declaradas:** openstax_intro_stats_2e:7.intro:chunk-002, openstax_intro_stats_2e:7.1:chunk-002
**Referencia:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Describe la aproximación a la normalidad y la menor dispersión, pero omite que la media se conserva y la expresión de la desviación estándar.
  - B: Cubre los efectos esenciales (más normal, menor dispersión, gráfico más estrecho) respaldados por 7.1:chunk-002 y 7.intro:chunk-002, que son las citas declaradas.
  - Árbitro: Describe correctamente la mayor normalidad y la menor dispersión, pero omite que la media permanece igual a la poblacional y que la desviación estándar disminuye como σ/√n, propiedades incluidas en la referencia y en 7.1:chunk-002.

---

## CASO 70 — q-v1-001__explicit · qwen3.5:9b · rrf
**Disputa:** behavior_ok
**Pregunta:** How does increasing the sample size affect the sampling distribution of the sample mean?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** Increasing the sample size decreases the spread (standard deviation) of the sampling distribution, making it narrower and steeper, while the mean of the sample means remains approximately the same.
**Citas declaradas:** openstax_intro_stats_2e:7.1:chunk-002, openstax_principles_ds:4.1:chunk-006
**Referencia:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Describe correctamente la menor dispersión y la estabilidad de la media, pero omite que la distribución se aproxima a la normal.
  - B: Todo lo afirmado está respaldado por los chunks citados, pero omite que la distribución se aproxima más a una normal, un componente esencial de la referencia.
  - Árbitro: Responde sobre la dispersión y el centro, pero omite la aproximación a la normalidad que recoge 7.1:chunk-002, un componente material del efecto solicitado.