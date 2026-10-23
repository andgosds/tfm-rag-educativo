# Lote 4 — validación humana del arbitraje (casos 31–40)

## CASO 31 — q-v1-012__implicit · qwen3.5:9b · bm25
**Disputa:** faithfulness, citations_ok
**Pregunta:** With confidence level and population variability held constant, how does a larger sample affect the error bound and the width of the range estimated from sample data for a population parameter?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** A larger sample decreases the error bound and results in a narrower (wider) confidence interval.
**Citas declaradas:** openstax_principles_ds:4.1:chunk-010
**Referencia:** A larger sample decreases the error bound and therefore makes the confidence interval narrower, provided that the confidence level and population variability remain fixed.
- **faithfulness** — A: `0` · B: `1` → **árbitro: `0`**
  - A: Afirma que el intervalo se estrecha, pero el paréntesis «wider» introduce la conclusión contraria, que la cita no respalda.
  - B: La idea principal (menor error, intervalo más estrecho) es correcta y está respaldada, pero el añadido «(wider)» se contradice y desdice el contexto, que solo sostiene estrechamiento.
  - Árbitro: El añadido «wider» contradice explícitamente el estrechamiento establecido en 4.1:chunk-010 sobre el efecto central preguntado, aunque el resto de la respuesta sea correcto.
- **citations_ok** — A: `0` · B: `1` → **árbitro: `1`**
  - A: Afirma que el intervalo se estrecha, pero el paréntesis «wider» introduce la conclusión contraria, que la cita no respalda.
  - B: La idea principal (menor error, intervalo más estrecho) es correcta y está respaldada, pero el añadido «(wider)» se contradice y desdice el contexto, que solo sostiene estrechamiento.
  - Árbitro: La cita apunta al fragmento pertinente que respalda la disminución del error y el estrechamiento; «wider» es una contradicción de la respuesta, no una selección de evidencia ajena.

---

## CASO 32 — q-v1-013__explicit · qwen3.5:4b · dense
**Disputa:** faithfulness, citations_ok
**Pregunta:** Which distribution should be used to construct a confidence interval for a population mean when the population standard deviation is known versus when it is estimated by the sample standard deviation, and how do degrees of freedom enter the latter case?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** When the population standard deviation is known, use the normal distribution; when it is estimated by the sample standard deviation, use the Student's t-distribution. Degrees of freedom (df) in the latter case equal n – 1 because calculating the sample standard deviation requires knowing all n deviations, but their sum is zero, meaning only n – 1 can vary freely.
**Citas declaradas:** openstax_intro_stats_2e:8.2:chunk-003, openstax_intro_stats_2e:8.2:chunk-004
**Referencia:** Use the normal distribution when the population standard deviation is known. When it is unknown and estimated by the sample standard deviation, use Student's t-distribution. For a simple random sample from an approximately normal population, the t-distribution has n − 1 degrees of freedom, which determine its exact shape.
- **faithfulness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: La explicación de t y n − 1 está respaldada, pero los fragmentos citados no establecen expresamente el uso de la normal cuando σ es conocida.
  - B: Cubre normal vs. t y el origen de los grados de libertad n−1, presentes de forma explícita en los chunks citados; la etiqueta declarada grounded_correction no corresponde, pero la conducta r
  - Árbitro: El contexto respalda el uso de t cuando se estima la desviación poblacional y los grados de libertad n − 1, pero no establece el uso de la normal cuando la desviación poblacional es conocida.
- **citations_ok** — A: `0` · B: `1` → **árbitro: `0`**
  - A: La explicación de t y n − 1 está respaldada, pero los fragmentos citados no establecen expresamente el uso de la normal cuando σ es conocida.
  - B: Cubre normal vs. t y el origen de los grados de libertad n−1, presentes de forma explícita en los chunks citados; la etiqueta declarada grounded_correction no corresponde, pero la conducta r
  - Árbitro: Los fragmentos citados justifican la distribución t y sus grados de libertad, pero no respaldan la elección de la normal con desviación poblacional conocida, contrariamente a lo afirmado por el juez 2.

---

## CASO 33 — q-v1-013__implicit · gemma4:e4b · rerank
**Disputa:** behavior_ok, citations_ok
**Pregunta:** Which distribution should be used to construct a confidence interval for a population mean when the population standard deviation is known versus when it is estimated by the sample standard deviation, and how does the number of deviations that are free to vary enter the latter case?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** When the population standard deviation is known, a normal distribution is used to calculate the error bound for a population mean [openstax_intro_stats_2e:8.1:chunk-003]. When the population standard deviation is estimated by the sample standard deviation, the Student's-t distribution is used, and the number of deviations that are free to vary is incorporated into this distribution [openstax_intro_stats_2e:8.intro:chunk-002].
**Citas declaradas:** openstax_intro_stats_2e:8.1:chunk-003, openstax_intro_stats_2e:8.intro:chunk-002
**Referencia:** Use the normal distribution when the population standard deviation is known. When it is unknown and estimated by the sample standard deviation, use Student's t-distribution. For a simple random sample from an approximately normal population, the t-distribution has n − 1 degrees of freedom, which determine its exact shape.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Distingue ambas distribuciones, pero omite n−1 y la cita sobre la t no respalda cómo intervienen los grados de libertad.
  - B: Responde como corresponde (la etiqueta declarada contradice lo que hace, pero cuenta lo que hace), pero la explicación de cómo entran las desviaciones libres es vaga —no dice n−1 ni que fija
  - Árbitro: Distingue las distribuciones, pero no explica cómo intervienen los grados de libertad: omite que son n − 1 y que determinan la forma de la distribución t.
- **citations_ok** — A: `0` · B: `1` → **árbitro: `0`**
  - A: Distingue ambas distribuciones, pero omite n−1 y la cita sobre la t no respalda cómo intervienen los grados de libertad.
  - B: Responde como corresponde (la etiqueta declarada contradice lo que hace, pero cuenta lo que hace), pero la explicación de cómo entran las desviaciones libres es vaga —no dice n−1 ni que fija
  - Árbitro: 8.intro:chunk-002 menciona la distribución t y la estimación de la desviación poblacional, pero no respalda la afirmación sobre las desviaciones libres ni su incorporación a esa distribución.

---

## CASO 34 — q-v1-014__implicit · qwen3.5:4b · bm25
**Disputa:** faithfulness, citations_ok
**Pregunta:** What sequence should be followed to flag unusually low or high observations using the middle 50% of an ordered dataset?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The premise that the middle 50% of a dataset is used to flag outliers is incorrect; the interquartile range (IQR), which represents the spread of the middle 50%, is used to calculate the bounds for flagging outliers, but the IQR itself does not directly flag them. To flag unusually low or high observations, you must first find the first quartile (Q1) and third quartile (Q3) to determine the IQR, then apply a formula using 1.5 times the IQR to establish lower and upper bounds; any data values below the lower bound or above the upper bound are flagged as outliers.
**Citas declaradas:** openstax_principles_ds:3.3:chunk-005, openstax_principles_ds:3.3:chunk-004
**Referencia:** Order the data and determine the first and third quartiles. Compute the interquartile range as the difference between the third and first quartiles, use the quartiles and a 1.5-IQR cutoff to define lower and upper bounds, and flag values below the lower bound or above the upper bound for further investigation.
- **faithfulness** — A: `0` · B: `1` → **árbitro: `0`**
  - A: Presenta como falsa una premisa válida sobre el 50 % central; después describe el procedimiento, aunque sin concretar ambos límites.
  - B: El procedimiento es correcto y las citas lo sostienen, pero tildar de falsa la premisa contradice el propio contexto (los cuartiles y el IQR sí se usan para marcar outliers) y desvía la cond
  - Árbitro: Aunque describe después el procedimiento, declara falsa una premisa que los fragmentos 3.3:chunk-004 y 3.3:chunk-005 respaldan expresamente: utilizar los cuartiles y el IQR para detectar posibles valores atípicos.
- **citations_ok** — A: `0` · B: `1` → **árbitro: `1`**
  - A: Presenta como falsa una premisa válida sobre el 50 % central; después describe el procedimiento, aunque sin concretar ambos límites.
  - B: El procedimiento es correcto y las citas lo sostienen, pero tildar de falsa la premisa contradice el propio contexto (los cuartiles y el IQR sí se usan para marcar outliers) y desvía la cond
  - Árbitro: Los fragmentos citados corresponden a la evidencia sobre el IQR y los límites para detectar valores atípicos; la corrección injustificada de la premisa es un problema de fidelidad, no de selección de citas.

---

## CASO 35 — q-v1-014__implicit · qwen3.5:4b · rrf
**Disputa:** factual_correctness, behavior_ok
**Pregunta:** What sequence should be followed to flag unusually low or high observations using the middle 50% of an ordered dataset?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** To flag unusually low or high observations (outliers), calculate the Interquartile Range (IQR) as the difference between the third and first quartiles, then use the formula Lower Bound = Q1 - 1.5*IQR and Upper Bound = Q3 + 1.5*IQR; any data values below the lower bound or above the upper bound are flagged.
**Citas declaradas:** openstax_principles_ds:3.3:chunk-004, openstax_principles_ds:3.3:chunk-005
**Referencia:** Order the data and determine the first and third quartiles. Compute the interquartile range as the difference between the third and first quartiles, use the quartiles and a 1.5-IQR cutoff to define lower and upper bounds, and flag values below the lower bound or above the upper bound for further investigation.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `2`**
  - A: Da los límites y la regla de detección, pero no explicita cómo obtener los cuartiles ni que los valores señalados requieren investigación.
  - B: Resuelve la paráfrasis 'middle 50%' como IQR y entrega la secuencia con los límites de 1.5·IQR, respaldada por 3.3:chunk-004/005; se comporta como respuesta pese a declarar otra etiqueta.
  - Árbitro: Coincide con la referencia en lo esencial: calcular el IQR, establecer los límites con 1.5·IQR y señalar los valores externos; la pregunta ya parte de datos ordenados.
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `2`**
  - A: Da los límites y la regla de detección, pero no explicita cómo obtener los cuartiles ni que los valores señalados requieren investigación.
  - B: Resuelve la paráfrasis 'middle 50%' como IQR y entrega la secuencia con los límites de 1.5·IQR, respaldada por 3.3:chunk-004/005; se comporta como respuesta pese a declarar otra etiqueta.
  - Árbitro: Proporciona la secuencia operativa solicitada para señalar observaciones extremas; explicar el cálculo de los cuartiles o la investigación posterior no es necesario para cumplir ese objetivo.

---

## CASO 36 — q-v1-015__explicit · qwen3.5:4b · dense
**Disputa:** faithfulness, factual_correctness
**Pregunta:** How do the ordinary mean, a trimmed mean, and the median respond differently to extreme observations?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The supplied contexts contradict the premise that these measures respond differently; they state that the median is not affected by outliers, while the mean can be skewed by them, and the trimmed mean removes outliers to provide a more representative measure.
**Citas declaradas:** openstax_principles_ds:3.1:chunk-007, openstax_principles_ds:3.1:chunk-006, openstax_principles_ds:3.1:chunk-003
**Referencia:** Extreme observations can disproportionately skew the ordinary mean. A trimmed mean reduces their influence by removing a selected percentage of values from both tails before averaging. The median depends on the middle position of the ordered data and is not affected by the numerical magnitude of the outliers.
- **faithfulness** — A: `0` · B: `1` → **árbitro: `0`**
  - A: Describe bien las tres medidas, pero afirma falsamente que el contexto contradice la premisa de la pregunta.
  - B: La comparación (media sensible, media recortada robusta, mediana inmune) coincide con la referencia y con los chunks citados, pero enmarca falsamente la pregunta como una premisa que el cont
  - Árbitro: Afirmar que el contexto contradice las diferencias entre las medidas contradice directamente los fragmentos, que describen precisamente esas diferencias, aunque después la respuesta las resuma.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Describe bien las tres medidas, pero afirma falsamente que el contexto contradice la premisa de la pregunta.
  - B: La comparación (media sensible, media recortada robusta, mediana inmune) coincide con la referencia y con los chunks citados, pero enmarca falsamente la pregunta como una premisa que el cont
  - Árbitro: La comparación sustantiva coincide en lo esencial con la referencia, pero la afirmación inicial niega erróneamente la premisa que esa misma comparación confirma.

---

## CASO 37 — q-v1-015__implicit · qwen3.5:4b · dense
**Disputa:** faithfulness, factual_correctness
**Pregunta:** How do the ordinary mean, the mean computed after discarding a fixed fraction of the lowest and highest values, and the median respond differently to extreme observations?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The supplied contexts contradict the premise that the ordinary mean is unaffected by extreme observations; they state that the mean can be significantly skewed by outliers (extreme values), whereas both the trimmed mean and the median are designed to be less affected or unaffected by them.
**Citas declaradas:** openstax_principles_ds:3.1:chunk-006, openstax_principles_ds:3.1:chunk-007, openstax_principles_ds:3.1:chunk-010
**Referencia:** Extreme observations can disproportionately skew the ordinary mean. A trimmed mean reduces their influence by removing a selected percentage of values from both tails before averaging. The median depends on the middle position of the ordered data and is not affected by the numerical magnitude of the outliers.
- **faithfulness** — A: `0` · B: `1` → **árbitro: `1`**
  - A: Las diferencias entre las medidas están respaldadas, pero inventa una premisa sobre la media ordinaria para corregirla.
  - B: El contenido sustantivo es correcto y está respaldado, pero inventa una premisa falsa ('la media ordinaria no se ve afectada por valores extremos') para corregirla en lugar de responder dire
  - Árbitro: Los fragmentos respaldan la sensibilidad de la media y la resistencia de las otras medidas, pero la respuesta atribuye a la pregunta una premisa que esta no contiene.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Las diferencias entre las medidas están respaldadas, pero inventa una premisa sobre la media ordinaria para corregirla.
  - B: El contenido sustantivo es correcto y está respaldado, pero inventa una premisa falsa ('la media ordinaria no se ve afectada por valores extremos') para corregirla en lugar de responder dire
  - Árbitro: La comparación es esencialmente correcta, pero no distingue cómo el recorte reduce la influencia de los extremos y cómo la posición central protege a la mediana, distinción que sí recoge la referencia.

---

## CASO 38 — q-v1-015__implicit · qwen3.5:9b · dense
**Disputa:** faithfulness, factual_correctness
**Pregunta:** How do the ordinary mean, the mean computed after discarding a fixed fraction of the lowest and highest values, and the median respond differently to extreme observations?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The ordinary mean is significantly affected by extreme observations (outliers), pulling it toward them. In contrast, the median is not affected by the numerical values of outliers because it focuses on the middle value of an ordered dataset. A trimmed mean reduces the influence of outliers by discarding a fixed fraction of the lowest and highest values before calculating the average, making it more representative than the ordinary mean when outliers are present but less robust than the median which ignores them entirely.
**Citas declaradas:** openstax_principles_ds:3.1:chunk-006, openstax_principles_ds:3.1:chunk-007, openstax_intro_stats_2e:9.4:chunk-004, openstax_principles_ds:3.1:chunk-010
**Referencia:** Extreme observations can disproportionately skew the ordinary mean. A trimmed mean reduces their influence by removing a selected percentage of values from both tails before averaging. The median depends on the middle position of the ordered data and is not affected by the numerical magnitude of the outliers.
- **faithfulness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: La comparación principal es correcta, pero afirmar que la mediana ignora por completo los valores extremos excede lo respaldado.
  - B: Las tres medidas y su respuesta a los extremos se sostienen en los chunks 3.1:006 y 3.1:007 (con la comparación con la mediana también respaldada), aunque dos de las cuatro citas (9.4:004 y 
  - Árbitro: Los fragmentos respaldan la sensibilidad de la media y la resistencia de la media recortada y la mediana, pero no establecen una jerarquía general de robustez entre estas dos últimas.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `2`**
  - A: La comparación principal es correcta, pero afirmar que la mediana ignora por completo los valores extremos excede lo respaldado.
  - B: Las tres medidas y su respuesta a los extremos se sostienen en los chunks 3.1:006 y 3.1:007 (con la comparación con la mediana también respaldada), aunque dos de las cuatro citas (9.4:004 y 
  - Árbitro: La comparación coincide en lo esencial con la referencia, y la expresión sobre ignorar los extremos se entiende, por la explicación previa, como insensibilidad a su magnitud numérica.

---

## CASO 39 — q-v1-016__implicit · gemma4:e4b · bm25
**Disputa:** faithfulness, factual_correctness
**Pregunta:** How do count-based outcomes differ from measurement-based outcomes in the kinds of numerical values they can take?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The premise that count-based outcomes and measurement-based outcomes are the only difference is incorrect. The difference lies in whether the variable can take on a finite or countable number of distinct values (count-based/discrete) or any value within a given range or interval (measurement-based/continuous).
**Citas declaradas:** openstax_principles_ds:3.5:chunk-002
**Referencia:** A discrete random variable takes a finite or countably infinite set of distinct values and typically results from counting. A continuous random variable can take any value within an interval and typically results from measurement.
- **faithfulness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Da la distinción correcta entre valores discretos y continuos, pero corrige una premisa que la pregunta no plantea.
  - B: El contenido sustantivo es correcto y está respaldado por chunk-002, pero inventa una premisa exclusiva que la pregunta no plantea y la 'corrige', cuando lo esperado era responder.
  - Árbitro: La distinción entre valores discretos y continuos está respaldada por 3.5:chunk-002, pero la respuesta añade una supuesta premisa de exclusividad que la pregunta no plantea.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `2`**
  - A: Da la distinción correcta entre valores discretos y continuos, pero corrige una premisa que la pregunta no plantea.
  - B: El contenido sustantivo es correcto y está respaldado por chunk-002, pero inventa una premisa exclusiva que la pregunta no plantea y la 'corrige', cuando lo esperado era responder.
  - Árbitro: La respuesta expresa íntegramente la distinción esencial de la referencia entre valores finitos o numerables y cualquier valor de un intervalo; la corrección inicial improcedente no altera esa distinción.

---

## CASO 40 — q-v1-016__implicit · qwen3.5:4b · bm25
**Disputa:** faithfulness, factual_correctness
**Pregunta:** How do count-based outcomes differ from measurement-based outcomes in the kinds of numerical values they can take?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The supplied contexts do not contain information distinguishing count-based outcomes from measurement-based outcomes regarding the specific kinds of numerical values they can take; however, the text states that discrete random variables (typically results of a count) take on a finite or countably infinite number of distinct values, while continuous random variables (typically results of a measurement) can take on any value within a given range.
**Citas declaradas:** openstax_principles_ds:3.5:chunk-002, openstax_principles_ds:3.5:chunk-003
**Referencia:** A discrete random variable takes a finite or countably infinite set of distinct values and typically results from counting. A continuous random variable can take any value within an interval and typically results from measurement.
- **faithfulness** — A: `0` · B: `1` → **árbitro: `0`**
  - A: Niega que el contexto distinga ambos tipos de resultados, aunque acto seguido reproduce la distinción que sí aparece en los fragmentos citados.
  - B: El contenido que entrega en la segunda frase coincide con la referencia y las citas lo respaldan, pero el aviso de que el contexto no distingue count-based de measurement-based es falso, pue
  - Árbitro: La negación inicial contradice directamente 3.5:chunk-002 y 3.5:chunk-003, que distinguen los valores posibles de los resultados de conteo y de medición.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `2`**
  - A: Niega que el contexto distinga ambos tipos de resultados, aunque acto seguido reproduce la distinción que sí aparece en los fragmentos citados.
  - B: El contenido que entrega en la segunda frase coincide con la referencia y las citas lo respaldan, pero el aviso de que el contexto no distingue count-based de measurement-based es falso, pue
  - Árbitro: La explicación sustantiva coincide con toda la distinción esencial de la referencia: valores finitos o numerables para variables discretas y cualquier valor de un intervalo para continuas.