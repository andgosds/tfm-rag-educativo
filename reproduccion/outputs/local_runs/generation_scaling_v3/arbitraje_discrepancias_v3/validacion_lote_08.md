# Lote 8 — validación humana del arbitraje (casos 71–80)

## CASO 71 — q-v1-001__implicit · gemma4:e4b · rerank
**Disputa:** behavior_ok
**Pregunta:** How does increasing the sample size affect the distribution of the averages obtained by repeatedly drawing samples of that size?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** As sample sizes increase, the distribution of sample means tends to become more closely normal, and the standard deviation of the sample means decreases [openstax_intro_stats_2e:7.1:chunk-002].
**Citas declaradas:** openstax_intro_stats_2e:7.1:chunk-002
**Referencia:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Explica la mayor normalidad y la menor dispersión, pero omite que la media permanece igual.
  - B: Lo afirmado (tendencia a la normalidad y menor dispersión) está respaldado por 7.1:chunk-002, pero omite un componente de la referencia: que la media muestral conserva la media poblacional (
  - Árbitro: Responde sobre la normalidad y la dispersión, pero omite un componente material de la descripción solicitada: que la distribución conserva la media poblacional, como indica 7.1:chunk-002.

---

## CASO 72 — q-v1-001__implicit · gemma4:e4b · rrf
**Disputa:** behavior_ok
**Pregunta:** How does increasing the sample size affect the distribution of the averages obtained by repeatedly drawing samples of that size?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** As the number of dice rolled increases, the mean of the sample means remains approximately the same, the spread of the sample means gets smaller, and the graph appears steeper and thinner [openstax_intro_stats_2e:7.1:chunk-001].
**Citas declaradas:** openstax_intro_stats_2e:7.1:chunk-001
**Referencia:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: La cita respalda la estabilidad del centro y la menor dispersión, pero la respuesta omite la aproximación a la normalidad.
  - B: La cita sostiene fielmente lo dicho (media estable, dispersión menor), aunque la respuesta queda anclada al ejemplo de los dados y no explicita la tendencia a la normalidad de la referencia.
  - Árbitro: Responde sobre el centro y la dispersión, pero omite la aproximación a la normalidad, un componente material del cambio en la distribución explicado en 7.1:chunk-002.

---

## CASO 73 — q-v1-001__implicit · qwen3.5:4b · dense
**Disputa:** factual_correctness
**Pregunta:** How does increasing the sample size affect the distribution of the averages obtained by repeatedly drawing samples of that size?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** Increasing the sample size causes the distribution of averages to become more normally distributed (bell-shaped), while the mean remains approximately the same and the spread (standard deviation) decreases.
**Citas declaradas:** openstax_intro_stats_2e:7.intro:chunk-002, openstax_intro_stats_2e:7.1:chunk-001, openstax_intro_stats_2e:7.1:chunk-002, openstax_principles_ds:4.1:chunk-006
**Referencia:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `2`**
  - A: Recoge la forma más normal, el centro estable y la menor dispersión; solo falta cuantificar esta última como σ/√n.
  - B: Cubre los tres efectos documentados (media estable, menor dispersión y forma más normal) coincidiendo con la referencia, con citas que los respaldan.
  - Árbitro: Recoge los tres aspectos esenciales de la referencia —mayor normalidad, centro estable y menor dispersión— y la pregunta no exige cuantificar esta última mediante una fórmula.

---

## CASO 74 — q-v1-001__implicit · qwen3.5:4b · rrf
**Disputa:** factual_correctness
**Pregunta:** How does increasing the sample size affect the distribution of the averages obtained by repeatedly drawing samples of that size?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** Increasing the sample size causes the distribution of averages to become more normally distributed, with a mean that remains approximately the same and a spread (standard deviation) that gets smaller.
**Citas declaradas:** openstax_intro_stats_2e:7.1:chunk-002, openstax_intro_stats_2e:7.1:chunk-001
**Referencia:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `2`**
  - A: Explica los tres cambios principales y los cita, aunque no precisa que la desviación estándar es σ/√n.
  - B: Cubre los tres elementos de la referencia (más normal, media retenida, menor dispersión) con citas que los respaldan literalmente.
  - Árbitro: Recoge los tres efectos esenciales de la referencia —mayor normalidad, centro estable y menor dispersión—, y la pregunta cualitativa no exige explicitar la fórmula de la desviación estándar.

---

## CASO 75 — q-v1-001__implicit · qwen3.5:9b · dense
**Disputa:** factual_correctness
**Pregunta:** How does increasing the sample size affect the distribution of the averages obtained by repeatedly drawing samples of that size?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** Increasing the sample size causes the distribution of the averages to more closely follow a normal distribution, with the spread (standard deviation) decreasing and the graph becoming steeper and thinner.
**Citas declaradas:** openstax_intro_stats_2e:7.intro:chunk-002, openstax_intro_stats_2e:7.1:chunk-001, openstax_intro_stats_2e:7.1:chunk-002, openstax_intro_stats_2e:7.4:chunk-002, openstax_principles_ds:4.1:chunk-006
**Referencia:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Las citas sostienen los cambios de forma y dispersión; falta indicar que el centro permanece igual y cómo disminuye la desviación estándar.
  - B: Respuesta correcta y respaldada por los chunks citados sobre el CLT y la distribución muestral; las citas apuntan a la evidencia usada, incluido 4.1:chunk-006 que refuerza la reducción de la
  - Árbitro: La explicación es correcta pero incompleta respecto a la referencia: no menciona la conservación de la media poblacional ni la relación σ/√n, aunque ambas aparecen en los fragmentos citados.

---

## CASO 76 — q-v1-001__implicit · qwen3.5:9b · rrf
**Disputa:** behavior_ok
**Pregunta:** How does increasing the sample size affect the distribution of the averages obtained by repeatedly drawing samples of that size?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** Increasing the sample size causes the spread of the sample means to get smaller, making the distribution steeper and thinner while the mean remains approximately the same.
**Citas declaradas:** openstax_intro_stats_2e:7.1:chunk-002, openstax_intro_stats_2e:7.1:chunk-001
**Referencia:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Explica el estrechamiento y la estabilidad de la media, pero no menciona la aproximación progresiva a la normal.
  - B: Reproduce fielmente los tres puntos del contexto (media estable, menor dispersión, forma más empinada), pero no menciona la tendencia a la normalidad que recoge la referencia.
  - Árbitro: Explica el estrechamiento y la estabilidad de la media, pero describir la distribución como más estrecha y empinada no cubre la aproximación a la normalidad indicada en 7.1:chunk-002.

---

## CASO 77 — q-v1-003__explicit · qwen3.5:9b · bm25
**Disputa:** citations_ok
**Pregunta:** What sequence of steps should be followed to conduct a hypothesis test?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** The steps are: 1) Set up null and alternative hypotheses; 2) Collect relevant sample data; 3) Determine the correct distribution to use; 4) Analyze the data to calculate a test statistic and p-value; 5) Decide to reject or fail to reject the null hypothesis based on whether the data is inconsistent with it.
**Citas declaradas:** openstax_principles_ds:4.2:chunk-003
**Referencia:** Formulate null and alternative hypotheses from the claim, collect relevant sample data, select the appropriate sampling distribution, analyze the data using a test statistic and p-value, and then reject or fail to reject the null hypothesis according to whether the sample is inconsistent with it.
- **citations_ok** — A: `1` · B: `None` → **árbitro: `1`**
  - A: Reproduce la secuencia de cinco pasos del fragmento citado.
  - B: Los cinco pasos reproducen literalmente el procedimiento de openstax_principles_ds:4.2:chunk-003 y coinciden con la referencia; la única cita apunta a ese fragmento.
  - Árbitro: La cita a 4.2:chunk-003 respalda los cinco pasos enumerados, incluida la decisión de rechazar o no rechazar la hipótesis nula.

---

## CASO 78 — q-v1-004__explicit · qwen3.5:4b · dense
**Disputa:** factual_correctness
**Pregunta:** Why is the median a suitable measure of center when a dataset contains extreme outliers?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The premise that the median is suitable because it is unaffected by extreme values is correct; however, the provided contexts do not explicitly state this specific reason, though they imply it by noting the mean is affected while the median focuses on the middle value.
**Citas declaradas:** NONE
**Referencia:** The median depends on the middle position of the ordered data and is not affected by the numerical magnitude of extreme values.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `2`**
  - A: Reconoce la resistencia de la mediana a los extremos, pero afirma erróneamente que el contexto no explica esa razón de forma explícita.
  - B: La razón que da (la mediana no se ve afectada por la magnitud de los extremos) coincide con la referencia, pero contradice el contexto al afirmar que no la expresa, cuando 3.1:chunk-008 lo d
  - Árbitro: La explicación estadística coincide con la referencia: la mediana se centra en el valor intermedio y resiste los extremos; negar que el contexto lo explicite es un fallo de fidelidad, ya recogido en faithfulness.

---

## CASO 79 — q-v1-004__explicit · qwen3.5:9b · bm25
**Disputa:** citations_ok
**Pregunta:** Why is the median a suitable measure of center when a dataset contains extreme outliers?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** The median is suitable because it focuses on the middle value of an ordered dataset and is not affected by the numerical values of outliers at either end, whereas the mean can be skewed by them.
**Citas declaradas:** openstax_principles_ds:3.1:chunk-007, openstax_principles_ds:3.1:chunk-010, openstax_principles_ds:3.1:chunk-011
**Referencia:** The median depends on the middle position of the ordered data and is not affected by the numerical magnitude of extreme values.
- **citations_ok** — A: `1` · B: `None` → **árbitro: `1`**
  - A: Explica que la mediana depende de la posición central y no de la magnitud de los valores extremos.
  - B: La idea de que la mediana se basa en el valor central y no se ve afectada por la magnitud de los outliers está en 3.1:chunk-007/010/011, que son las citas declaradas.
  - Árbitro: Los fragmentos citados 3.1:chunk-007/010/011 respaldan que la mediana depende del centro de los datos ordenados y resiste la magnitud de los extremos, mientras la media puede verse distorsionada.

---

## CASO 80 — q-v1-004__implicit · qwen3.5:4b · dense
**Disputa:** factual_correctness
**Pregunta:** Why is the middle value of the ordered dataset a suitable measure of center when a dataset contains extreme outliers?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The premise that extreme outliers affect the median is false; the median is preferred when outliers are present because it focuses on the middle value of an ordered dataset and is not affected by the numerical values of those outliers, whereas the mean can be significantly skewed by them.
**Citas declaradas:** openstax_principles_ds:3.1:chunk-008, openstax_principles_ds:3.1:chunk-007
**Referencia:** The median depends on the middle position of the ordered data and is not affected by the numerical magnitude of extreme values.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `2`**
  - A: Da la explicación correcta y bien citada, pero inventa una premisa falsa que la pregunta no plantea.
  - B: La explicación es correcta y está respaldada por 3.1:chunk-008, pero se desvía al corregir un supuesto inexistente (que la pregunta afirme que los extremos afectan a la mediana) en lugar de 
  - Árbitro: Explica correctamente la posición central y la insensibilidad a la magnitud de los extremos, como la referencia; atribuir a la pregunta una premisa inexistente es la desviación ya recogida en behavior_ok.