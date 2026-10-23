# Lote 13 — validación humana del arbitraje (casos 121–130)

## CASO 121 — q-v1-020__implicit · gemma4:e4b · rerank
**Disputa:** faithfulness
**Pregunta:** Why does increasing the probability attached to the interval make the confidence interval narrower when all other inputs are fixed?
**Conducta esperada:** grounded_correction · declarada: abstain
**Respuesta:** I cannot answer from the supplied contexts.
**Citas declaradas:** NONE
**Referencia:** (sin puntuar)
- **faithfulness** — A: `0` · B: `1` → **árbitro: `0`**
  - A: Se abstiene pese a que el contexto permite corregir la premisa falsa; la abstención no lleva citas.
  - B: Se abstiene injustificadamente: el contexto basta para traducir 'probability attached to the interval' a nivel de confianza y corregir la premisa (8.1:chunk-011 y 4.1:chunk-010), pero la res
  - Árbitro: La afirmación de que no puede responderse con el contexto contradice 8.1:chunk-011 y 4.1:chunk-010, que establecen explícitamente que aumentar el nivel de confianza ensancha el intervalo.

---

## CASO 122 — q-v1-020__implicit · qwen3.5:4b · bm25
**Disputa:** factual_correctness
**Pregunta:** Why does increasing the probability attached to the interval make the confidence interval narrower when all other inputs are fixed?
**Conducta esperada:** grounded_correction · declarada: grounded_correction
**Respuesta:** The premise is false; increasing the probability (confidence level) attached to an interval makes it wider, not narrower.
**Citas declaradas:** openstax_intro_stats_2e:8.1:chunk-010, openstax_intro_stats_2e:8.1:chunk-011
**Referencia:** (sin puntuar)
- **factual_correctness** — A: `2` · B: `1` → **árbitro: `1`**
  - A: Rechaza la premisa falsa y señala, conforme a las citas, que el intervalo se ensancha.
  - B: Detecta y corrige la premisa falsa sin el término explícito, pero omite el mecanismo causal que la pregunta pedía explicar.
  - Árbitro: Rechaza correctamente la premisa falsa, pero deja incompleta la explicación al no mencionar que el aumento del nivel de confianza exige un mayor margen de error.

---

## CASO 123 — q-v1-022__explicit · qwen3.5:4b · bm25
**Disputa:** faithfulness
**Pregunta:** How should a chi-square test of independence be conducted for a contingency table?
**Conducta esperada:** abstain · declarada: grounded_correction
**Respuesta:** The supplied contexts do not describe how to conduct a chi-square test of independence; they only explain how to perform a one-way ANOVA, calculate correlation coefficients, and construct confidence intervals for proportions or means.
**Citas declaradas:** NONE
**Referencia:** (sin puntuar)
- **faithfulness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Se abstiene justificadamente, aunque su descripción del contexto omite la información general sobre hipótesis y valores p.
  - B: Abstención limpia y fiel: describe lo que sí contienen los chunks (ANOVA, correlación, IC) y no añade nada externo.
  - Árbitro: La ausencia del procedimiento solicitado está respaldada, pero afirmar que los fragmentos solo tratan ANOVA, correlación e intervalos excluye indebidamente el contenido sobre hipótesis y valores p.

---

## CASO 124 — q-v1-022__implicit · qwen3.5:4b · rerank
**Disputa:** faithfulness
**Pregunta:** How should one proceed to test whether two categorical variables are related in a contingency table?
**Conducta esperada:** abstain · declarada: grounded_correction
**Respuesta:** The supplied contexts do not describe how to test for relationships between two categorical variables in a contingency table; they only discuss hypothesis testing for comparing two population means or proportions using independent or dependent samples.
**Citas declaradas:** openstax_principles_ds:4.2:chunk-025, openstax_principles_ds:4.2:chunk-023
**Referencia:** (sin puntuar)
- **faithfulness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Se abstiene correctamente porque falta el procedimiento, aunque exagera al decir que los fragmentos solo tratan comparaciones de medias o proporciones.
  - B: Se abstiene de forma justificada y acotando con precisión lo que sí contiene el contexto (comparación de medias y proporciones), pese a declarar grounded_correction; los chunks citados respa
  - Árbitro: La ausencia del procedimiento solicitado justifica la abstención, pero afirmar que los contextos solo tratan comparaciones de medias o proporciones omite el fragmento sobre interpretación de pendiente e intercepto.

---

## CASO 125 — q-v3-002__explicit · gemma4:e4b · rerank
**Disputa:** behavior_ok
**Pregunta:** Is it true that about 95% of the values of a normally distributed variable lie within one standard deviation of the mean?
**Conducta esperada:** grounded_correction · declarada: grounded_correction
**Respuesta:** The empirical rule states that about 68% of the values lie within one standard deviation of the mean, and about 95% of the values lie within two standard deviations of the mean.
**Citas declaradas:** openstax_principles_ds:3.5:chunk-016, openstax_intro_stats_2e:6.1:chunk-006
**Referencia:** (sin puntuar)
- **behavior_ok** — A: `2` · B: `1` → **árbitro: `2`**
  - A: Sustituye el 95 % a una desviación por el 68 % a una y el 95 % a dos, tal como indican ambas citas.
  - B: Los datos que aporta (68% en una desviación, 95% en dos) contradicen la premisa y están respaldados, pero nunca niega explícitamente la afirmación de la pregunta, componente material de una 
  - Árbitro: Corrige inequívocamente la premisa al situar el 68 % en una desviación y el 95 % en dos, con respaldo en ambos fragmentos citados; no necesita añadir una negación explícita.

---

## CASO 126 — q-v3-002__explicit · qwen3.5:4b · dense
**Disputa:** citations_ok
**Pregunta:** Is it true that about 95% of the values of a normally distributed variable lie within one standard deviation of the mean?
**Conducta esperada:** grounded_correction · declarada: grounded_correction
**Respuesta:** No, the empirical rule states that about 95% of values lie within two standard deviations of the mean, not one.
**Citas declaradas:** openstax_principles_ds:3.5:chunk-016
**Referencia:** (sin puntuar)
- **citations_ok** — A: `1` · B: `None` → **árbitro: `1`**
  - A: Corrige la premisa falsa: el 95 % corresponde a dos desviaciones estándar, según el fragmento citado.
  - B: Corrige la premisa falsa apoyándose exactamente en la regla empírica del chunk citado (95% en dos desviaciones típicas).
  - Árbitro: El fragmento citado, openstax_principles_ds:3.5:chunk-016, establece expresamente que aproximadamente el 95 % de los valores queda dentro de dos desviaciones estándar.

---

## CASO 127 — q-v3-002__implicit · gemma4:e4b · bm25
**Disputa:** behavior_ok
**Pregunta:** Is it true that about 95% of the values of a variable following the classic bell-shaped distribution lie within one standard deviation of the mean?
**Conducta esperada:** grounded_correction · declarada: answer
**Respuesta:** About 68% of the values lie within one standard deviation of the mean.
**Citas declaradas:** openstax_principles_ds:3.5:chunk-016, openstax_intro_stats_2e:6.1:chunk-006
**Referencia:** (sin puntuar)
- **behavior_ok** — A: `2` · B: `1` → **árbitro: `2`**
  - A: Aunque no dice «no», corrige efectivamente la premisa al indicar 68 % en lugar de 95 %.
  - B: El dato del 68% es correcto y las citas lo respaldan, pero la respuesta no señala ni corrige la premisa falsa —el núcleo de la corrección esperada—, sino que da una afirmación suelta como si
  - Árbitro: Sustituir el 95 % por el 68 % para una desviación estándar corrige directamente la premisa con respaldo del contexto, aunque no incluya una negación explícita.

---

## CASO 128 — q-v3-003__explicit · gemma4:e4b · rerank
**Disputa:** behavior_ok
**Pregunta:** How is the required sample size determined when a study must estimate a population mean within a given error bound, and how does the calculation differ when it must estimate a population proportion?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** When estimating a population mean, the required sample size ($n$) can be calculated using the formula $n = (\frac{z}{EBM})^2 \sigma^2 / \sigma^2$ (or $n = (\frac{z}{EBM})^2 \sigma^2$ if the formula provided in the context is interpreted as $n = (\frac{z}{EBM})^2 \sigma^2$ based on the structure of the provided formula and example) where $z$ is the critical value corresponding to the desired confidence level, $EBM$ is the desired margin of error, and $\sigma$ is the population standard deviation.

When estimating a population proportion, the required sample size ($n$) is determined using the formula $n = (\frac{z}{EBP})^2 \hat{p}(1-\hat{p})$. 
**Citas declaradas:** openstax_intro_stats_2e:8.2:chunk-001
**Referencia:** In both cases the required sample size is obtained by solving the error bound formula for n, and in both it depends on the desired error bound and on the z-score for the chosen confidence level. What differs is the measure of variability that enters the calculation. For a mean the formula uses the population standard deviation, so a planning study needs a value for it, and the result is rounded up to the next higher integer to make sure the sample is large enough. For a proportion the formula us
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Incluye una primera fórmula errónea antes de ofrecer la correcta, omite el redondeo y solo cita un fragmento sobre medias para explicar también proporciones.
  - B: Responde a ambas partes, pero la fórmula de la media aparece desdibujada e internamente errónea («/σ²») y solo cita la fuente de la media, dejando sin citar la fórmula de proporción y la reg
  - Árbitro: Aborda la comparación entre medias y proporciones, pero omite el redondeo hacia arriba, que 8.2:chunk-001 y la referencia exigen para garantizar un tamaño muestral suficiente.

---

## CASO 129 — q-v3-003__explicit · qwen3.5:4b · bm25
**Disputa:** behavior_ok
**Pregunta:** How is the required sample size determined when a study must estimate a population mean within a given error bound, and how does the calculation differ when it must estimate a population proportion?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The required sample size for estimating a population mean within a given error bound is calculated using n = [(z * σ) / EBM]^2, where z is the critical value for the desired confidence level, σ is the population standard deviation, and EBM is the error bound. For estimating a population proportion, the formula differs to n = [ (z^2 * p̂ * (1-p̂)) / EBP^2 ], which assumes a prior estimate for the sample proportion (p̂) is available; if not, 0.5 should be used instead.
**Citas declaradas:** openstax_intro_stats_2e:8.2:chunk-001, openstax_principles_ds:4.1:chunk-018
**Referencia:** In both cases the required sample size is obtained by solving the error bound formula for n, and in both it depends on the desired error bound and on the z-score for the chosen confidence level. What differs is the measure of variability that enters the calculation. For a mean the formula uses the population standard deviation, so a planning study needs a value for it, and the result is rounded up to the next higher integer to make sure the sample is large enough. For a proportion the formula us
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Da ambas fórmulas y el uso de 0,5, pero omite redondear hacia arriba y explicar por qué 0,5 produce el tamaño más conservador.
  - B: Las dos fórmulas y la regla del 0.5 están respaldadas por los chunks citados, pero omite el redondeo al alza y la razón de usar 0.5 que la referencia incluye; responde pese a declarar ground
  - Árbitro: Responde con ambas fórmulas, pero omite el redondeo al alza que el contexto exige para obtener un número suficiente de observaciones.

---

## CASO 130 — q-v3-003__explicit · qwen3.5:4b · rerank
**Disputa:** behavior_ok
**Pregunta:** How is the required sample size determined when a study must estimate a population mean within a given error bound, and how does the calculation differ when it must estimate a population proportion?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The sample size for a mean is calculated using n = (z*σ/EBM)², whereas for a proportion it uses n = (z²p(1-p))/EBP², assuming a prior estimate or defaulting to 0.5 if unknown.
**Citas declaradas:** openstax_intro_stats_2e:8.2:chunk-001, openstax_principles_ds:4.1:chunk-017, openstax_intro_stats_2e:8.3:chunk-010, openstax_principles_ds:4.1:chunk-018
**Referencia:** In both cases the required sample size is obtained by solving the error bound formula for n, and in both it depends on the desired error bound and on the z-score for the chosen confidence level. What differs is the measure of variability that enters the calculation. For a mean the formula uses the population standard deviation, so a planning study needs a value for it, and the result is rounded up to the next higher integer to make sure the sample is large enough. For a proportion the formula us
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Da ambas fórmulas y la estimación previa de la proporción, pero omite redondear el tamaño hacia arriba y explicar por qué se usa 0,5.
  - B: Responde con las dos fórmulas correctas y su diferencia esencial, pero omite detalles de la referencia como redondear al alza y por qué 0.5 maximiza el producto p(1-p); pese a declarar groun
  - Árbitro: Responde a ambos supuestos con sus fórmulas, pero omite el redondeo al alza que el contexto exige para obtener un número de observaciones suficiente, un componente material del procedimiento solicitado.