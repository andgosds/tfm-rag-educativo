# Lote 12 — validación humana del arbitraje (casos 111–120)

## CASO 111 — q-v1-014__implicit · qwen3.5:9b · rrf
**Disputa:** behavior_ok
**Pregunta:** What sequence should be followed to flag unusually low or high observations using the middle 50% of an ordered dataset?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** To flag unusually low or high observations, calculate the Interquartile Range (IQR) as the difference between the third quartile ($Q_3$) and the first quartile ($Q_1$). Then determine lower and upper bounds using the formulas $Q_1 - 1.5 \times IQR$ and $Q_3 + 1.5 \times IQR$. Any data values below the lower bound or above the upper bound are flagged as outliers.
**Citas declaradas:** openstax_principles_ds:3.3:chunk-004, openstax_principles_ds:3.3:chunk-005
**Referencia:** Order the data and determine the first and third quartiles. Compute the interquartile range as the difference between the third and first quartiles, use the quartiles and a 1.5-IQR cutoff to define lower and upper bounds, and flag values below the lower bound or above the upper bound for further investigation.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Da los límites y la regla para señalar valores, pero omite ordenar los datos y determinar los cuartiles.
  - B: Las cotas y el criterio 1,5×IQR se sostienen en el contexto, pero la respuesta omite el paso inicial de ordenar los datos y determinar Q1 y Q3 que la referencia incluye como comienzo de la s
  - Árbitro: Explica el IQR, los límites y la detección, pero omite determinar primero los cuartiles del conjunto ordenado, un paso material de la secuencia solicitada.

---

## CASO 112 — q-v1-015__explicit · qwen3.5:4b · rrf
**Disputa:** factual_correctness
**Pregunta:** How do the ordinary mean, a trimmed mean, and the median respond differently to extreme observations?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The supplied contexts do not contain information regarding how the median responds to extreme observations; they only state that the median is generally a better measure when outliers are present because it is not affected by their numerical values, while the mean can be skewed by them.
**Citas declaradas:** NONE
**Referencia:** Extreme observations can disproportionately skew the ordinary mean. A trimmed mean reduces their influence by removing a selected percentage of values from both tails before averaging. The median depends on the middle position of the ordered data and is not affected by the numerical magnitude of the outliers.
- **factual_correctness** — A: `0` · B: `1` → **árbitro: `1`**
  - A: Afirma que falta información sobre la mediana aunque el contexto la explica, y no compara las tres medidas; no declara citas.
  - B: La abstención es injustificada y se contradice con el contexto: 3.1:chunk-007 afirma que la mediana no se ve afectada por los valores extremos y describe el trimmed mean; además omite por co
  - Árbitro: Aunque comienza negando información que sí existe, describe correctamente la sensibilidad de la media y la resistencia de la mediana, por lo que ofrece una respuesta parcialmente correcta que omite la media recortada.

---

## CASO 113 — q-v1-015__implicit · gemma4:e4b · bm25
**Disputa:** faithfulness
**Pregunta:** How do the ordinary mean, the mean computed after discarding a fixed fraction of the lowest and highest values, and the median respond differently to extreme observations?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** The median is generally a better measure of central tendency than the mean or the trimmed mean when outliers are present because it is not affected by the numerical values of the outliers, as it focuses on the middle value of the ordered dataset [openstax_principles_ds:3.1:chunk-007].
**Citas declaradas:** openstax_principles_ds:3.1:chunk-007
**Referencia:** Extreme observations can disproportionately skew the ordinary mean. A trimmed mean reduces their influence by removing a selected percentage of values from both tails before averaging. The median depends on the middle position of the ordered data and is not affected by the numerical magnitude of the outliers.
- **faithfulness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Explica la resistencia de la mediana, pero no compara el efecto sobre las otras dos medias y no sustenta que sea preferible a la media recortada.
  - B: Lo que dice sobre la mediana es fiel a chunk-007, pero ignora por completo la media y la media recortada, dos tercios de lo preguntado.
  - Árbitro: 3.1:chunk-007 respalda la resistencia de la mediana a la magnitud de los valores extremos, pero no establece que sea generalmente mejor que la media recortada.

---

## CASO 114 — q-v1-015__implicit · gemma4:e4b · dense
**Disputa:** factual_correctness
**Pregunta:** How do the ordinary mean, the mean computed after discarding a fixed fraction of the lowest and highest values, and the median respond differently to extreme observations?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** The median is generally better than the mean when outliers are present because it focuses on the middle value and is not affected by the numerical values of the outliers. The trimmed mean addresses this by deleting a specified percentage of data values from both the lower and upper ends, which can result in a more representative measure of the center compared to the standard mean when outliers are present.
**Citas declaradas:** openstax_principles_ds:3.1:chunk-010, openstax_principles_ds:3.1:chunk-007
**Referencia:** Extreme observations can disproportionately skew the ordinary mean. A trimmed mean reduces their influence by removing a selected percentage of values from both tails before averaging. The median depends on the middle position of the ordered data and is not affected by the numerical magnitude of the outliers.
- **factual_correctness** — A: `2` · B: `1` → **árbitro: `2`**
  - A: Explica cómo el recorte y la mediana reducen el efecto de los valores extremos frente a la media ordinaria, con citas pertinentes.
  - B: Responde y todo está respaldado, pero describe solo la mediana y la media recortada; el efecto de los valores extremos sobre la media ordinaria queda implícito, incompleto frente a la refere
  - Árbitro: La comparación expresa la resistencia de la mediana y la reducción de la influencia de los extremos mediante el recorte, dejando suficientemente clara por contraste la mayor sensibilidad de la media ordinaria.

---

## CASO 115 — q-v1-016__implicit · gemma4:e4b · rrf
**Disputa:** factual_correctness
**Pregunta:** How do count-based outcomes differ from measurement-based outcomes in the kinds of numerical values they can take?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The premise that count-based outcomes and measurement-based outcomes are being compared in terms of the kinds of numerical values they can take is partially correct, but the contexts explain the difference between discrete (count-based) and continuous (measurement-based) random variables. Count-based outcomes are associated with discrete random variables, which take on a finite or countably infinite number of distinct values, whereas measurement-based outcomes are associated with continuous random variables, which can take on any value within a given range or interval.
**Citas declaradas:** openstax_principles_ds:3.5:chunk-003
**Referencia:** A discrete random variable takes a finite or countably infinite set of distinct values and typically results from counting. A continuous random variable can take any value within an interval and typically results from measurement.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `2`**
  - A: La distinción entre conteo y medición es correcta, pero la supuesta corrección parcial de la premisa no está justificada.
  - B: La sustancia es correcta y está respaldada por chunk-003, pero la respuesta se enmarca como corrección de una premisa que no es falsa y añade una valoración de esa premisa que el contexto no
  - Árbitro: Reproduce la distinción esencial de la referencia entre valores discretos finitos o numerables y valores continuos dentro de un intervalo, pese al preámbulo injustificado.

---

## CASO 116 — q-v1-017__explicit · qwen3.5:9b · bm25
**Disputa:** behavior_ok
**Pregunta:** When is one-way ANOVA an appropriate choice, and how are its null and alternative hypotheses framed?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** One-way ANOVA is appropriate when comparing three or more means to determine if they are all statistically the same or if at least one is different, provided samples are random, independent, from approximately normal distributions, and have approximately equal population variances. The null hypothesis (H0) states that all population means are equal, while the alternative hypothesis (Ha) states that at least one population mean is different from the others.
**Citas declaradas:** openstax_principles_ds:4.4:chunk-003
**Referencia:** One-way ANOVA is appropriate for comparing three or more population means when there is one independent variable. Its null hypothesis states that all population means are equal, while its alternative states that at least one population mean differs from the others.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Expone bien la comparación y las hipótesis, pero omite que el ANOVA de una vía se aplica a una sola variable independiente.
  - B: Las hipótesis H0/Ha son exactas y las condiciones están en el contexto, pero omite que el ANOVA de una vía se aplica con una sola variable independiente, que la referencia incluye como parte
  - Árbitro: Responde sobre los requisitos y las hipótesis, pero omite la condición de una sola variable independiente, que chunk-002 y la referencia incluyen para precisar cuándo corresponde el ANOVA de una vía.

---

## CASO 117 — q-v1-017__implicit · qwen3.5:9b · bm25
**Disputa:** behavior_ok
**Pregunta:** When is one-way ANOVA an appropriate choice, and how are the two competing claims that it tests framed?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** One-way ANOVA is appropriate for comparing three or more means when samples are random, independent, drawn from approximately normal distributions, and have approximately equal population variances. The two competing claims are framed as: (1) Null Hypothesis ($H_0$): All population means are equal; and (2) Alternative Hypothesis ($H_a$): At least one population mean is different from the others.
**Citas declaradas:** openstax_principles_ds:4.4:chunk-003, openstax_principles_ds:4.4:chunk-005
**Referencia:** One-way ANOVA is appropriate for comparing three or more population means when there is one independent variable. Its null hypothesis states that all population means are equal, while its alternative states that at least one population mean differs from the others.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Formula correctamente ambas hipótesis y los requisitos, pero no explicita la condición de una sola variable independiente; en la práctica responde, no corrige.
  - B: Contenido correcto y respaldado por chunk-003, aunque etiquetado como grounded_correction responde con normalidad; incompleto por la misma omisión de la variable independiente única.
  - Árbitro: La conducta real es responder, pero falta una condición material de aplicabilidad: que haya una sola variable independiente, como establece chunk-002.

---

## CASO 118 — q-v1-019__implicit · gemma4:e4b · bm25
**Disputa:** citations_ok
**Pregunta:** According to the selected sources, what is the p-value of the formal test of normality applied to the women's heights dataset?
**Conducta esperada:** abstain · declarada: grounded_correction
**Respuesta:** The provided contexts discuss p-values in the context of hypothesis testing, but they do not provide a p-value for a formal test of normality applied to a women's heights dataset.
**Citas declaradas:** openstax_intro_stats_2e:9.4:chunk-003
**Referencia:** (sin puntuar)
- **citations_ok** — A: `0` · B: `1` → **árbitro: `1`**
  - A: Aunque declara otra conducta, en realidad se abstiene justificadamente; la cita sobre valores p generales no acredita el resultado solicitado.
  - B: Abstiene correctamente y su única afirmación sobre lo que contienen los chunks es cierta; la etiqueta grounded_correction no cambia que la conducta real es una abstención justificada.
  - Árbitro: 9.4:chunk-003 respalda la afirmación sobre el tratamiento general de los valores p, y la respuesta no lo presenta como evidencia de un resultado de normalidad, sino que señala correctamente su ausencia.

---

## CASO 119 — q-v1-019__implicit · gemma4:e4b · dense
**Disputa:** behavior_ok
**Pregunta:** According to the selected sources, what is the p-value of the formal test of normality applied to the women's heights dataset?
**Conducta esperada:** abstain · declarada: grounded_correction
**Respuesta:** The provided contexts discuss p-values for different scenarios, including one where the p-value is stated as "approximately zero" for a bread rising test [openstax_intro_stats_2e:9.4:chunk-005, openstax_intro_stats_2e:9.4:chunk-004], and another where a p-value of 0.0013 is given for a test involving a sample mean of 12.5 [openstax_intro_stats_2e:9.4:chunk-005]. However, none of the supplied contexts provide the p-value for a formal test of normality applied specifically to a "women's heights dataset."
**Citas declaradas:** openstax_intro_stats_2e:9.4:chunk-005, openstax_intro_stats_2e:9.4:chunk-004
**Referencia:** (sin puntuar)
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `2`**
  - A: Concluye correctamente que falta el valor solicitado, pero añade resultados de pruebas ajenas en lugar de limitarse a la abstención.
  - B: Concluye correctamente que ningún contexto aporta ese p-value; los p-values que cita son reales de esos chunks, aunque la etiqueta declarada (grounded_correction) no corresponda a lo que hac
  - Árbitro: Se abstiene de proporcionar el p-valor solicitado y distingue explícitamente los ejemplos ajenos del contraste de normalidad de las alturas de mujeres, sin atribuirle sus resultados.

---

## CASO 120 — q-v1-020__explicit · qwen3.5:4b · bm25
**Disputa:** factual_correctness
**Pregunta:** Why does increasing the confidence level make the confidence interval narrower when all other inputs are fixed?
**Conducta esperada:** grounded_correction · declarada: grounded_correction
**Respuesta:** Increasing the confidence level makes the confidence interval wider, not narrower; decreasing the confidence level makes it narrower.
**Citas declaradas:** openstax_intro_stats_2e:8.1:chunk-010, openstax_intro_stats_2e:8.1:chunk-011
**Referencia:** (sin puntuar)
- **factual_correctness** — A: `2` · B: `1` → **árbitro: `1`**
  - A: Corrige la premisa: el texto indica que mayor confianza implica un intervalo más ancho.
  - B: Corrige bien la premisa falsa apoyándose en los chunks citados, pero no explica el porqué (aumento del error bound) que era el contenido de la pregunta.
  - Árbitro: Corrige correctamente la dirección del cambio, pero omite explicar que una mayor confianza aumenta el margen de error, mecanismo que los fragmentos proporcionan y que responde al porqué solicitado.