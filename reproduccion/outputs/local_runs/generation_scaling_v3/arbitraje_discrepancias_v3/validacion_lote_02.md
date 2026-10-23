# Lote 2 — validación humana del arbitraje (casos 11–20)

## CASO 11 — q-v1-006__explicit · gemma4:e4b · dense
**Disputa:** faithfulness, factual_correctness, behavior_ok
**Pregunta:** If all other inputs remain unchanged, how does increasing the confidence level from 90% to 95% affect the width of the confidence interval, and why?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The premise that increasing the confidence level from 90% to 95% will cause the confidence interval to become narrower is incorrect.
**Citas declaradas:** openstax_principles_ds:4.1:chunk-010, openstax_intro_stats_2e:8.1:chunk-010
**Referencia:** The 95% confidence interval is wider than the 90% interval because greater confidence requires an interval that covers a larger range of plausible values for the population parameter.
- **faithfulness** — A: `2` · B: `1` → **árbitro: `1`**
  - A: Descarta que el intervalo se estreche, pero atribuye esa premisa a la pregunta y no explica por qué se ensancha.
  - B: La pregunta no contiene ninguna premisa de estrechamiento: la respuesta inventa y rebate una premisa inexistente, y jamás indica que el intervalo se ensancha ni por qué, que era lo preguntad
  - Árbitro: El contexto respalda negar que el intervalo se estreche, pero no respalda atribuir esa premisa a la pregunta, que no la plantea.
- **factual_correctness** — A: `1` · B: `0` → **árbitro: `1`**
  - A: Descarta que el intervalo se estreche, pero atribuye esa premisa a la pregunta y no explica por qué se ensancha.
  - B: La pregunta no contiene ninguna premisa de estrechamiento: la respuesta inventa y rebate una premisa inexistente, y jamás indica que el intervalo se ensancha ni por qué, que era lo preguntad
  - Árbitro: Descarta correctamente el estrechamiento, pero no afirma expresamente que el intervalo se ensancha ni explica la necesidad de cubrir un rango mayor.
- **behavior_ok** — A: `1` · B: `0` → **árbitro: `1`**
  - A: Descarta que el intervalo se estreche, pero atribuye esa premisa a la pregunta y no explica por qué se ensancha.
  - B: La pregunta no contiene ninguna premisa de estrechamiento: la respuesta inventa y rebate una premisa inexistente, y jamás indica que el intervalo se ensancha ni por qué, que era lo preguntad
  - Árbitro: Aporta una respuesta parcial sobre la dirección del cambio, pero la presenta como corrección de una premisa inexistente y omite el porqué solicitado.

---

## CASO 12 — q-v1-006__explicit · qwen3.5:9b · bm25
**Disputa:** faithfulness, factual_correctness, citations_ok
**Pregunta:** If all other inputs remain unchanged, how does increasing the confidence level from 90% to 95% affect the width of the confidence interval, and why?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** Increasing the confidence level from 90% to 95% increases the width of the confidence interval because a higher confidence level requires capturing more area under the normal distribution curve, which necessitates wider tails and thus a larger error bound.
**Citas declaradas:** openstax_intro_stats_2e:8.1:chunk-010, openstax_intro_stats_2e:8.4:chunk-002
**Referencia:** The 95% confidence interval is wider than the 90% interval because greater confidence requires an interval that covers a larger range of plausible values for the population parameter.
- **faithfulness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Acertadamente dice que el intervalo se ensancha, pero «colas más anchas» describe mal el cambio de área en las colas.
  - B: El ensanchamiento por mayor nivel de confianza vía error bound mayor está explícito en 8.1:chunk-010, citado, y coincide con la referencia.
  - Árbitro: 8.1:chunk-010 respalda el aumento del ancho y del margen de error, pero no la afirmación de que se necesitan colas más anchas.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Acertadamente dice que el intervalo se ensancha, pero «colas más anchas» describe mal el cambio de área en las colas.
  - B: El ensanchamiento por mayor nivel de confianza vía error bound mayor está explícito en 8.1:chunk-010, citado, y coincide con la referencia.
  - Árbitro: La conclusión coincide con la referencia, pero la explicación sobre colas más anchas es imprecisa: aumenta el área central cubierta y disminuye el área que queda en las colas.
- **citations_ok** — A: `1` · B: `None` → **árbitro: `1`**
  - A: Acertadamente dice que el intervalo se ensancha, pero «colas más anchas» describe mal el cambio de área en las colas.
  - B: El ensanchamiento por mayor nivel de confianza vía error bound mayor está explícito en 8.1:chunk-010, citado, y coincide con la referencia.
  - Árbitro: La cita 8.1:chunk-010 compara explícitamente los intervalos del 90% y del 95% y respalda el ensanchamiento por un mayor margen de error.

---

## CASO 13 — q-v1-011__explicit · qwen3.5:4b · bm25
**Disputa:** faithfulness, factual_correctness, behavior_ok
**Pregunta:** For a standardized normal variable, what values define its center and spread, and how should the sign and magnitude of its standardized score be interpreted?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** For a standardized normal variable, the center is defined by a mean of 0 and the spread by a standard deviation of 1; its standardized score (z-score) indicates how many standard deviations a value lies from the mean, with positive values above the mean and negative values below it. The supplied contexts do not contain information regarding the interpretation of the sign and magnitude of standardized scores for a standardized normal variable.
**Citas declaradas:** NONE
**Referencia:** The standard normal distribution has mean 0 and standard deviation 1. A z-score states how many standard deviations a value lies from the mean: a positive score is above the mean, a negative score is below it, and zero corresponds to the mean.
- **faithfulness** — A: `0` · B: `1` → **árbitro: `0`**
  - A: Da los valores y signos principales, pero niega erróneamente que el contexto explique los z-scores, omite el caso cero y no cita fuentes.
  - B: El contenido (media 0, desviación 1, signo y magnitud del z-score) coincide con la referencia y está en 6.1:chunk-002, pero la coletilla de que el contexto no cubre la interpretación contrad
  - Árbitro: La afirmación final de que falta información sobre signo y magnitud contradice directamente 6.1:chunk-002, que explica ambos aspectos.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Da los valores y signos principales, pero niega erróneamente que el contexto explique los z-scores, omite el caso cero y no cita fuentes.
  - B: El contenido (media 0, desviación 1, signo y magnitud del z-score) coincide con la referencia y está en 6.1:chunk-002, pero la coletilla de que el contexto no cubre la interpretación contrad
  - Árbitro: Explica correctamente el centro, la dispersión y los signos positivo y negativo, pero omite el caso cero y añade una negación injustificada del respaldo de esa interpretación.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Da los valores y signos principales, pero niega erróneamente que el contexto explique los z-scores, omite el caso cero y no cita fuentes.
  - B: El contenido (media 0, desviación 1, signo y magnitud del z-score) coincide con la referencia y está en 6.1:chunk-002, pero la coletilla de que el contexto no cubre la interpretación contrad
  - Árbitro: Responde sustancialmente a la pregunta, pero se desvía al declarar insuficiente un contexto que permite explicar íntegramente la interpretación solicitada.

---

## CASO 14 — q-v1-015__implicit · qwen3.5:4b · bm25
**Disputa:** faithfulness, behavior_ok, citations_ok
**Pregunta:** How do the ordinary mean, the mean computed after discarding a fixed fraction of the lowest and highest values, and the median respond differently to extreme observations?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The supplied contexts do not contain information regarding how the ordinary mean, trimmed mean, and median respond differently to extreme observations; they only provide a specific example where removing outliers makes the trimmed mean more representative than the ordinary mean, and state generally that the median is better when outliers are present because it is not affected by their numerical values.
**Citas declaradas:** NONE
**Referencia:** Extreme observations can disproportionately skew the ordinary mean. A trimmed mean reduces their influence by removing a selected percentage of values from both tails before averaging. The median depends on the middle position of the ordered data and is not affected by the numerical magnitude of the outliers.
- **faithfulness** — A: `0` · B: `1` → **árbitro: `0`**
  - A: Afirma que falta información que el contexto sí proporciona y solo ofrece una comparación parcial, sin citas.
  - B: Se abstiene alegando que el contexto no basta cuando sí contiene la comparación (media sesgada por outliers, recorte de colas, mediana no afectada por la magnitud), lo que resume es incomple
  - Árbitro: Niega que exista información sobre la comparación solicitada, aunque 3.1:chunk-007 explica expresamente el efecto de los extremos sobre la media, la media recortada y la mediana.
- **behavior_ok** — A: `1` · B: `0` → **árbitro: `1`**
  - A: Afirma que falta información que el contexto sí proporciona y solo ofrece una comparación parcial, sin citas.
  - B: Se abstiene alegando que el contexto no basta cuando sí contiene la comparación (media sesgada por outliers, recorte de colas, mediana no afectada por la magnitud), lo que resume es incomple
  - Árbitro: Pese a alegar insuficiencia del contexto, sí ofrece una comparación sustantiva de las tres medidas, por lo que responde parcialmente en lugar de abstenerse por completo.
- **citations_ok** — A: `0` · B: `1` → **árbitro: `0`**
  - A: Afirma que falta información que el contexto sí proporciona y solo ofrece una comparación parcial, sin citas.
  - B: Se abstiene alegando que el contexto no basta cuando sí contiene la comparación (media sesgada por outliers, recorte de colas, mediana no afectada por la magnitud), lo que resume es incomple
  - Árbitro: Formula afirmaciones sobre la representatividad de la media recortada y la resistencia de la mediana sin citar 3.1:chunk-007, por lo que no constituye una mera abstención sin citas.

---

## CASO 15 — q-v1-016__implicit · gemma4:e4b · dense
**Disputa:** faithfulness, behavior_ok, citations_ok
**Pregunta:** How do count-based outcomes differ from measurement-based outcomes in the kinds of numerical values they can take?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The premise that count-based outcomes and measurement-based outcomes are being compared regarding the kinds of numerical values they can take is not addressed in the supplied contexts. The contexts discuss discrete random variables, such as those modeled by the binomial distribution, which count the number of successes [openstax_principles_ds:3.5:chunk-006]. In contrast, the contexts mention a continuous random variable, such as the number of inches of rain, which can take on any value like 2.0563 [openstax_principles_ds:3.5:chunk-005].
**Citas declaradas:** openstax_principles_ds:3.5:chunk-006, openstax_principles_ds:3.5:chunk-005
**Referencia:** A discrete random variable takes a finite or countably infinite set of distinct values and typically results from counting. A continuous random variable can take any value within an interval and typically results from measurement.
- **faithfulness** — A: `1` · B: `0` → **árbitro: `1`**
  - A: Afirma erróneamente que la comparación no está abordada, aunque los contextos citados sí permiten responderla mediante ejemplos.
  - B: Afirmar que el contexto no trata la comparación contradice los propios chunks citados (conteos 0-3 frente a 2.0563), y se abstiene pudiendo responder; los fragmentos que describe son correct
  - Árbitro: La descripción de los conteos discretos y de la lluvia continua está respaldada por los fragmentos, aunque la afirmación inicial de que no permiten abordar la comparación es injustificada.
- **behavior_ok** — A: `1` · B: `0` → **árbitro: `1`**
  - A: Afirma erróneamente que la comparación no está abordada, aunque los contextos citados sí permiten responderla mediante ejemplos.
  - B: Afirmar que el contexto no trata la comparación contradice los propios chunks citados (conteos 0-3 frente a 2.0563), y se abstiene pudiendo responder; los fragmentos que describe son correct
  - Árbitro: No se abstiene por completo, pues contrasta conteos discretos y mediciones continuas mediante ejemplos, pero introduce una reserva injustificada y omite explicitar los valores posibles de los conteos.
- **citations_ok** — A: `1` · B: `0` → **árbitro: `1`**
  - A: Afirma erróneamente que la comparación no está abordada, aunque los contextos citados sí permiten responderla mediante ejemplos.
  - B: Afirmar que el contexto no trata la comparación contradice los propios chunks citados (conteos 0-3 frente a 2.0563), y se abstiene pudiendo responder; los fragmentos que describe son correct
  - Árbitro: Las citas corresponden a las afirmaciones que acompañan: el fragmento 3.5:chunk-006 vincula conteo y variable discreta, y el 3.5:chunk-005 presenta la lluvia como variable continua.

---

## CASO 16 — q-v1-001__explicit · qwen3.5:4b · dense
**Disputa:** factual_correctness, behavior_ok
**Pregunta:** How does increasing the sample size affect the sampling distribution of the sample mean?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** Increasing the sample size decreases the standard deviation (spread) of the sampling distribution of the sample mean, making it narrower and more normal, while also decreasing the error bound in confidence intervals.
**Citas declaradas:** openstax_intro_stats_2e:7.intro:chunk-002, openstax_intro_stats_2e:8.1:chunk-011, openstax_intro_stats_2e:7.1:chunk-002
**Referencia:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Explica la menor dispersión y la aproximación normal, pero omite que la media se mantiene y la relación σ/√n.
  - B: Recoge la menor dispersión y la mayor normalidad al crecer n, más el efecto sobre el error bound, todo respaldado por las citas; responde correctamente aunque declare otra etiqueta.
  - Árbitro: Describe correctamente la menor dispersión y la aproximación normal, pero omite la conservación de la media poblacional, una propiedad esencial incluida en la referencia.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Explica la menor dispersión y la aproximación normal, pero omite que la media se mantiene y la relación σ/√n.
  - B: Recoge la menor dispersión y la mayor normalidad al crecer n, más el efecto sobre el error bound, todo respaldado por las citas; responde correctamente aunque declare otra etiqueta.
  - Árbitro: Responde a la pregunta, pero deja sin describir el efecto sobre el centro de la distribución, explícitamente recogido en 7.1:chunk-002.

---

## CASO 17 — q-v1-001__explicit · qwen3.5:9b · bm25
**Disputa:** factual_correctness, behavior_ok
**Pregunta:** How does increasing the sample size affect the sampling distribution of the sample mean?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** Increasing the sample size decreases the error bound, making the confidence interval narrower.
**Citas declaradas:** openstax_intro_stats_2e:8.1:chunk-011
**Referencia:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.
- **factual_correctness** — A: `0` · B: `1` → **árbitro: `0`**
  - A: La cita respalda el estrechamiento del intervalo de confianza, pero la pregunta pide cómo cambia la distribución de las medias muestrales.
  - B: Lo afirmado (intervalo más estrecho al aumentar n) está respaldado por el chunk citado, pero responde sobre el error límite y el intervalo en vez de la distribución muestral, omitiendo la ap
  - Árbitro: La afirmación sobre el intervalo de confianza es correcta, pero responde sobre otro objeto y no describe ningún cambio de la distribución muestral solicitado en la pregunta.
- **behavior_ok** — A: `0` · B: `1` → **árbitro: `0`**
  - A: La cita respalda el estrechamiento del intervalo de confianza, pero la pregunta pide cómo cambia la distribución de las medias muestrales.
  - B: Lo afirmado (intervalo más estrecho al aumentar n) está respaldado por el chunk citado, pero responde sobre el error límite y el intervalo en vez de la distribución muestral, omitiendo la ap
  - Árbitro: Sustituye la explicación solicitada por una afirmación sobre intervalos de confianza, aunque los fragmentos 7.1:chunk-003 y 7.1:chunk-006 permiten responder directamente.

---

## CASO 18 — q-v1-001__implicit · qwen3.5:4b · rerank
**Disputa:** factual_correctness, behavior_ok
**Pregunta:** How does increasing the sample size affect the distribution of the averages obtained by repeatedly drawing samples of that size?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** Increasing the sample size causes the distribution of averages to become more normally distributed (closer to a normal bell curve) and reduces the spread (standard deviation) of those averages, making the distribution steeper and thinner.
**Citas declaradas:** openstax_intro_stats_2e:7.1:chunk-002, openstax_intro_stats_2e:7.1:chunk-004
**Referencia:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Recoge la mayor normalidad y la menor dispersión, pero no indica que la media se mantiene ni precisa cómo cambia la desviación estándar.
  - B: Cubre los dos efectos centrales de la referencia (más normalidad y menor desviación típica, con el 'más empinada y estrecha' literal del chunk) y solo echa en falta que la media se mantiene,
  - Árbitro: Describe correctamente la mayor normalidad y la menor dispersión, pero queda incompleta respecto a la referencia al omitir la conservación de la media poblacional y la relación de la desviación con la raíz del tamaño muestral.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `2`**
  - A: Recoge la mayor normalidad y la menor dispersión, pero no indica que la media se mantiene ni precisa cómo cambia la desviación estándar.
  - B: Cubre los dos efectos centrales de la referencia (más normalidad y menor desviación típica, con el 'más empinada y estrecha' literal del chunk) y solo echa en falta que la media se mantiene,
  - Árbitro: Explica directamente los dos cambios centrales preguntados, forma y dispersión, sin que la ausencia de una expresión cuantitativa o de la propiedad invariante de la media constituya una omisión material del comportamiento solicitado.

---

## CASO 19 — q-v1-001__implicit · qwen3.5:9b · bm25
**Disputa:** factual_correctness, behavior_ok
**Pregunta:** How does increasing the sample size affect the distribution of the averages obtained by repeatedly drawing samples of that size?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** Increasing the sample size causes the spread (standard deviation) of the distribution of averages to get smaller, making the graph steeper and thinner, while the mean remains approximately the same.
**Citas declaradas:** openstax_intro_stats_2e:7.1:chunk-002
**Referencia:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Describe correctamente la menor dispersión y la estabilidad de la media, pero omite que la distribución se aproxima a la normal.
  - B: Reproduce fielmente el chunk citado (media estable, menor dispersión, gráfico más estrecho y alto), que coincide con la referencia en lo esencial.
  - Árbitro: Describe correctamente la menor dispersión y la estabilidad de la media, pero omite la aproximación a la normal, un componente esencial de la referencia.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Describe correctamente la menor dispersión y la estabilidad de la media, pero omite que la distribución se aproxima a la normal.
  - B: Reproduce fielmente el chunk citado (media estable, menor dispersión, gráfico más estrecho y alto), que coincide con la referencia en lo esencial.
  - Árbitro: Responde directamente sobre la distribución de las medias, pero omite el cambio hacia la normalidad que el fragmento 7.1:chunk-002 explica expresamente.

---

## CASO 20 — q-v1-002__explicit · qwen3.5:4b · bm25
**Disputa:** faithfulness, factual_correctness
**Pregunta:** How do Type I and Type II errors differ in terms of the truth of the null hypothesis and the decision made?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** A Type I error occurs when you reject a true null hypothesis (deciding H0 is false when it is actually true), while a Type II error occurs when you fail to reject a false null hypothesis (deciding H0 is true when it is actually false).
**Citas declaradas:** openstax_intro_stats_2e:9.2:chunk-001, openstax_intro_stats_2e:9.5:chunk-015
**Referencia:** A Type I error occurs when a true null hypothesis is rejected. A Type II error occurs when a false null hypothesis is not rejected.
- **faithfulness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Distingue bien ambos errores, pero equipara indebidamente no rechazar la hipótesis nula con decidir que es verdadera.
  - B: Define ambos errores exactamente como la referencia (rechazar H0 verdadero / no rechazar H0 falso) y las citas contienen esas definiciones.
  - Árbitro: Las definiciones principales están respaldadas, pero el inciso que equipara no rechazar H0 con decidir que es verdadera excede lo establecido en los fragmentos.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Distingue bien ambos errores, pero equipara indebidamente no rechazar la hipótesis nula con decidir que es verdadera.
  - B: Define ambos errores exactamente como la referencia (rechazar H0 verdadero / no rechazar H0 falso) y las citas contienen esas definiciones.
  - Árbitro: Distingue correctamente ambos errores, pero introduce un desajuste conceptual al interpretar la ausencia de rechazo como una decisión de que H0 es verdadera.