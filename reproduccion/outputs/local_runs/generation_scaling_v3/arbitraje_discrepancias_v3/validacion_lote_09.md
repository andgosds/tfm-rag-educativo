# Lote 9 — validación humana del arbitraje (casos 81–90)

## CASO 81 — q-v1-004__implicit · qwen3.5:9b · bm25
**Disputa:** citations_ok
**Pregunta:** Why is the middle value of the ordered dataset a suitable measure of center when a dataset contains extreme outliers?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** The middle value of the ordered dataset (the median) is a suitable measure of center when outliers are present because it focuses on the middle position and is not affected by the numerical values of extreme data points at either end of the dataset.
**Citas declaradas:** openstax_principles_ds:3.1:chunk-007, openstax_principles_ds:3.1:chunk-010, openstax_principles_ds:3.1:chunk-008
**Referencia:** The median depends on the middle position of the ordered data and is not affected by the numerical magnitude of extreme values.
- **citations_ok** — A: `1` · B: `None` → **árbitro: `1`**
  - A: Identifica el valor central como la mediana y explica su resistencia a los extremos.
  - B: La respuesta identifica correctamente la mediana y da la razón esperada, respaldada por 3.1:chunk-007/008/010, todos citados.
  - Árbitro: Los fragmentos citados 3.1:chunk-007/010/008 identifican el valor central como la mediana y explican que no depende de la magnitud de los valores extremos.

---

## CASO 82 — q-v1-005__explicit · qwen3.5:9b · bm25
**Disputa:** citations_ok
**Pregunta:** What two aspects of the relationship between an independent and a dependent variable are summarized by the correlation coefficient?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** The correlation coefficient summarizes the strength and direction of the relationship between an independent and a dependent variable.
**Citas declaradas:** openstax_principles_ds:4.3:chunk-005
**Referencia:** The correlation coefficient summarizes the strength and the direction of the correlation.
- **citations_ok** — A: `1` · B: `None` → **árbitro: `1`**
  - A: Da los dos aspectos —fuerza y dirección— que indica expresamente el fragmento citado.
  - B: Responde exactamente fuerza y dirección, tal como define el coeficiente de correlación 4.3:chunk-005, fragmento citado.
  - Árbitro: El fragmento citado 4.3:chunk-005 define expresamente el coeficiente de correlación como una medida de fuerza y dirección.

---

## CASO 83 — q-v1-005__implicit · qwen3.5:4b · rerank
**Disputa:** behavior_ok
**Pregunta:** What two aspects of the relationship between an independent and a dependent variable are summarized by the measure of linear association between them?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The measure of linear association (the correlation coefficient) summarizes the strength and direction of the relationship between an independent variable and a dependent variable; it does not summarize two specific aspects like causality or prediction capability on its own, though regression uses this to predict.
**Citas declaradas:** NONE
**Referencia:** The correlation coefficient summarizes the strength and the direction of the correlation.
- **behavior_ok** — A: `2` · B: `1` → **árbitro: `2`**
  - A: Da los dos aspectos correctos, pero añade una salvedad sobre causalidad no explicitada en el contexto y no aporta citas.
  - B: Da la respuesta correcta (fuerza y dirección), pero añade una aclaración sobre causalidad no contenida en el contexto, se desvía del answer puro y no declara ninguna cita pese a apoyarse en 
  - Árbitro: Identifica explícitamente fuerza y dirección, los dos aspectos solicitados y respaldados por 4.3:chunk-005; la salvedad adicional y la falta de citas no impiden que cumpla la conducta de responder.

---

## CASO 84 — q-v1-005__implicit · qwen3.5:4b · rrf
**Disputa:** factual_correctness
**Pregunta:** What two aspects of the relationship between an independent and a dependent variable are summarized by the measure of linear association between them?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The measure of linear association (the correlation coefficient) summarizes the strength and direction of the relationship between an independent variable and a dependent variable; it does not summarize two specific aspects like "causation" and "correlation."
**Citas declaradas:** NONE
**Referencia:** The correlation coefficient summarizes the strength and the direction of the correlation.
- **factual_correctness** — A: `2` · B: `1` → **árbitro: `2`**
  - A: Da los dos aspectos pedidos, pero añade una corrección sobre causalidad que nadie planteó y no declara citas.
  - B: Contiene la respuesta correcta (fuerza y dirección), pero añade una negación sobre «causation» que el contexto no contiene y que enmarca una corrección que nadie pidió; además responde sin c
  - Árbitro: Identifica fuerza y dirección, exactamente los dos aspectos de la referencia; la observación innecesaria sobre causalidad no altera esa respuesta ni introduce un error factual.

---

## CASO 85 — q-v1-005__implicit · qwen3.5:9b · bm25
**Disputa:** citations_ok
**Pregunta:** What two aspects of the relationship between an independent and a dependent variable are summarized by the measure of linear association between them?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The measure of linear association (correlation) summarizes the strength and direction of the relationship between an independent and a dependent variable; it does not summarize causation or predictability alone without regression.
**Citas declaradas:** openstax_principles_ds:4.3:chunk-005, openstax_principles_ds:4.3:chunk-012
**Referencia:** The correlation coefficient summarizes the strength and the direction of the correlation.
- **citations_ok** — A: `1` · B: `None` → **árbitro: `1`**
  - A: Responde fuerza y dirección; añade una precisión sobre causalidad que el contexto no fundamenta.
  - B: Fuerza y dirección es correcto y está respaldado, pero la coletilla sobre causalidad no aparece en el contexto; además la etiqueta declarada (grounded_correction) contradice lo que hace, que
  - Árbitro: Las citas corresponden a la evidencia sobre fuerza y dirección en 4.3:chunk-005 y predicción mediante regresión en 4.3:chunk-012, aunque no sustentan la coletilla sobre causalidad, ya penalizada en faithfulness.

---

## CASO 86 — q-v1-005__implicit · qwen3.5:9b · rerank
**Disputa:** citations_ok
**Pregunta:** What two aspects of the relationship between an independent and a dependent variable are summarized by the measure of linear association between them?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The measure of linear association (correlation) summarizes the strength and direction of the relationship between an independent and a dependent variable; it does not summarize other aspects such as causation or non-linear patterns.
**Citas declaradas:** openstax_principles_ds:4.3:chunk-005, openstax_principles_ds:4.3:chunk-012
**Referencia:** The correlation coefficient summarizes the strength and the direction of the correlation.
- **citations_ok** — A: `0` · B: `1` → **árbitro: `1`**
  - A: Responde correctamente, pero añade una afirmación sobre causalidad que las citas no sustentan.
  - B: Pese a la etiqueta grounded_correction, la respuesta contesta (fuerza y dirección), que es lo esperado; la idea principal coincide con la referencia, pero la coletilla sobre causalidad y pat
  - Árbitro: Chunk-005 respalda explícitamente fuerza y dirección, los dos aspectos solicitados; la coletilla no respaldada afecta a faithfulness, pero no convierte esa cita en una referencia ajena a la evidencia utilizada.

---

## CASO 87 — q-v1-006__explicit · gemma4:e4b · rrf
**Disputa:** faithfulness
**Pregunta:** If all other inputs remain unchanged, how does increasing the confidence level from 90% to 95% affect the width of the confidence interval, and why?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The premise that increasing the confidence level from 90% to 95% causes the confidence interval to become wider is correct, but the provided contexts do not explain *why* this happens in terms of the mathematical relationship between the confidence level and the interval width, other than stating that a wider interval is needed to be more confident.
**Citas declaradas:** openstax_intro_stats_2e:8.1:chunk-010, openstax_principles_ds:4.1:chunk-010
**Referencia:** The 95% confidence interval is wider than the 90% interval because greater confidence requires an interval that covers a larger range of plausible values for the population parameter.
- **faithfulness** — A: `2` · B: `1` → **árbitro: `1`**
  - A: Acertó al decir que el intervalo se ensancha, pero eludió explicar que debe cubrir un rango mayor de valores plausibles.
  - B: Confirma que el intervalo se ensancha, pero se niega a dar el porqué alegando que el contexto no lo explica, cuando los propios chunks citados dicen que mayor confianza exige cubrir un rango
  - Árbitro: El ensanchamiento está respaldado, pero la supuesta ausencia de explicación matemática desatiende que 8.1:chunk-010 relaciona la mayor área de confianza con un mayor margen de error.

---

## CASO 88 — q-v1-006__implicit · gemma4:e4b · rerank
**Disputa:** faithfulness
**Pregunta:** If all other inputs remain unchanged, how does increasing the confidence level from 90% to 95% affect the width of the range estimated from sample data for a population parameter, and why?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The premise that the context describes the effect of increasing the confidence level from 90% to 95% is partially correct, but the context also provides a direct summary of the effect. The context states that increasing the confidence level increases the error bound, which makes the confidence interval wider [openstax_intro_stats_2e:8.1:chunk-011, openstax_principles_ds:4.1:chunk-010].
**Citas declaradas:** openstax_intro_stats_2e:8.1:chunk-011, openstax_principles_ds:4.1:chunk-010
**Referencia:** The 95% confidence interval is wider than the 90% interval because greater confidence requires an interval that covers a larger range of plausible values for the population parameter.
- **faithfulness** — A: `2` · B: `1` → **árbitro: `1`**
  - A: Da el efecto correcto, pero presenta innecesariamente como solo parcialmente válida una premisa que el contexto confirma.
  - B: Despliega una corrección de premisa injustificada (la pregunta no tiene premisa falsa y se esperaba una respuesta directa) y esa caracterización no se sostiene en el contexto, aunque la afir
  - Árbitro: El ensanchamiento está respaldado, pero calificar la premisa como parcialmente correcta carece de sustento: 8.1:chunk-010 compara explícitamente los intervalos del 90% y del 95%.

---

## CASO 89 — q-v1-006__implicit · qwen3.5:9b · bm25
**Disputa:** citations_ok
**Pregunta:** If all other inputs remain unchanged, how does increasing the confidence level from 90% to 95% affect the width of the range estimated from sample data for a population parameter, and why?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** Increasing the confidence level from 90% to 95% increases the width of the estimated range because a higher confidence level requires capturing more of the distribution's area, which necessitates a larger margin of error and thus wider interval bounds.
**Citas declaradas:** openstax_intro_stats_2e:8.1:chunk-010, openstax_principles_ds:4.1:chunk-010
**Referencia:** The 95% confidence interval is wider than the 90% interval because greater confidence requires an interval that covers a larger range of plausible values for the population parameter.
- **citations_ok** — A: `1` · B: `None` → **árbitro: `1`**
  - A: Relaciona el mayor nivel de confianza con un margen de error y un intervalo más amplios.
  - B: Traduce correctamente intervalo de confianza como rango estimado y la explicación (más área, mayor margen de error) está en 8.1:chunk-010 y 4.1:chunk-010, ambos citados.
  - Árbitro: Ambos fragmentos citados respaldan que aumentar la confianza amplía el intervalo, y 8.1:chunk-010 relaciona explícitamente este cambio con una mayor área y un mayor margen de error.

---

## CASO 90 — q-v1-007__explicit · qwen3.5:9b · bm25
**Disputa:** citations_ok
**Pregunta:** According to the selected sources, what is the Pearson correlation between weekly study time and final exam score?
**Conducta esperada:** abstain · declarada: abstain
**Respuesta:** I cannot answer from the supplied contexts.
**Citas declaradas:** NONE
**Referencia:** (sin puntuar)
- **citations_ok** — A: `1` · B: `None` → **árbitro: `1`**
  - A: Se abstiene sin inventar una correlación: no hay datos de estudio semanal y nota final.
  - B: El contexto no contiene ninguna correlación entre tiempo de estudio y nota de examen, y la abstención es limpia, sin afirmaciones ni citas.
  - Árbitro: La respuesta es una abstención sin citas, supuesto que la rúbrica califica explícitamente con 1.