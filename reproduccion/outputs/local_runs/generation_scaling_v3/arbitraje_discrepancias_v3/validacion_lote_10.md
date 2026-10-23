# Lote 10 — validación humana del arbitraje (casos 91–100)

## CASO 91 — q-v1-007__implicit · gemma4:e4b · rerank
**Disputa:** factual_correctness
**Pregunta:** According to the selected sources, what value describes how strongly weekly study time and final exam score move together in a straight-line pattern?
**Conducta esperada:** abstain · declarada: answer
**Respuesta:** The correlation coefficient is a measure of the strength and direction of the correlation between the independent variable and the dependent variable [openstax_principles_ds:4.3:chunk-005].
**Citas declaradas:** openstax_principles_ds:4.3:chunk-005
**Referencia:** (sin puntuar)
- **factual_correctness** — A: `0` · B: `1` → **árbitro: `0`**
  - A: La definición citada es correcta, pero responde con una definición en vez de reconocer que no consta el valor para esas variables.
  - B: La definición del coeficiente de correlación está respaldada por el chunk citado, pero en vez de abstenerse responde con una definición genérica sin aportar el valor pedido ni señalar que la
  - Árbitro: Ofrece una definición general en lugar del valor solicitado para tiempo de estudio y nota final, sin reconocer que las fuentes no proporcionan esa asociación.

---

## CASO 92 — q-v1-007__implicit · qwen3.5:4b · rerank
**Disputa:** behavior_ok
**Pregunta:** According to the selected sources, what value describes how strongly weekly study time and final exam score move together in a straight-line pattern?
**Conducta esperada:** abstain · declarada: grounded_correction
**Respuesta:** The supplied contexts do not provide data on weekly study time or final exam scores to calculate their correlation; they only discuss general concepts of normal distributions, confidence intervals, and measures of variability like range and standard deviation.
**Citas declaradas:** NONE
**Referencia:** (sin puntuar)
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `2`**
  - A: La abstención está justificada, pero su descripción del contexto omite erróneamente que también trata la correlación.
  - B: Se abstiene de hecho y sin citas, que es lo esperado pese a la etiqueta grounded_correction, pero su descripción del contexto como 'solo' distribuciones normales, intervalos y dispersión pas
  - Árbitro: Se abstiene de proporcionar la correlación solicitada porque faltan datos conjuntos; la descripción incompleta del contexto afecta a faithfulness, no al cumplimiento de la abstención esperada.

---

## CASO 93 — q-v1-007__implicit · qwen3.5:9b · bm25
**Disputa:** citations_ok
**Pregunta:** According to the selected sources, what value describes how strongly weekly study time and final exam score move together in a straight-line pattern?
**Conducta esperada:** abstain · declarada: abstain
**Respuesta:** I cannot answer from the supplied contexts.
**Citas declaradas:** NONE
**Referencia:** (sin puntuar)
- **citations_ok** — A: `1` · B: `None` → **árbitro: `1`**
  - A: Se abstiene sin citas porque los fragmentos no aportan el valor solicitado ni los pares de datos para calcularlo.
  - B: Los fragmentos recuperados solo hablan de correlaciones de otros ejemplos (Nike/S&P, publicidad/ingresos), no de estudio y examen; abstención justificada y sin citas.
  - Árbitro: La abstención no incluye citas ni atribuye a los fragmentos un valor que estos no proporcionan, por lo que corresponde 1.

---

## CASO 94 — q-v1-008__explicit · gemma4:e4b · bm25
**Disputa:** citations_ok
**Pregunta:** Why does the standard error of the sample mean increase as the sample size becomes larger?
**Conducta esperada:** grounded_correction · declarada: grounded_correction
**Respuesta:** The premise is incorrect; the standard error of the sample mean *decreases* as the sample size becomes larger.
**Citas declaradas:** openstax_principles_ds:4.1:chunk-011
**Referencia:** (sin puntuar)
- **citations_ok** — A: `1` · B: `0` → **árbitro: `0`**
  - A: Corrige la premisa falsa: al aumentar el tamaño muestral, disminuye el error estándar; la cita respalda esa dirección mediante el efecto del tamaño sobre el margen de error.
  - B: Corrige bien la premisa falsa (el error estándar de la media decrece al crecer n, según 7.3:chunk-002), pero cita 4.1:chunk-011, que habla del margen de error y no del error estándar.
  - Árbitro: El fragmento citado describe la disminución del margen de error, pero no explicita su relación con el error estándar; el respaldo directo de la corrección está en 7.3:chunk-002, que no se cita.

---

## CASO 95 — q-v1-008__explicit · gemma4:e4b · dense
**Disputa:** citations_ok
**Pregunta:** Why does the standard error of the sample mean increase as the sample size becomes larger?
**Conducta esperada:** grounded_correction · declarada: grounded_correction
**Respuesta:** The premise is incorrect; the standard error of the sample mean decreases as the sample size becomes larger.
**Citas declaradas:** openstax_intro_stats_2e:8.1:chunk-011, openstax_principles_ds:4.1:chunk-011
**Referencia:** (sin puntuar)
- **citations_ok** — A: `1` · B: `None` → **árbitro: `1`**
  - A: Corrige la premisa falsa: al aumentar el tamaño muestral, disminuye el error estándar; las citas respaldan esa relación.
  - B: Corrige la premisa falsa con la relación correcta (mayor n, menor error), respaldada por los chunks citados que sitúan n en el denominador del error bound.
  - Árbitro: Los fragmentos citados respaldan la corrección al mostrar que, manteniendo las demás condiciones, aumentar el tamaño muestral reduce el margen de error.

---

## CASO 96 — q-v1-008__explicit · gemma4:e4b · rrf
**Disputa:** citations_ok
**Pregunta:** Why does the standard error of the sample mean increase as the sample size becomes larger?
**Conducta esperada:** grounded_correction · declarada: grounded_correction
**Respuesta:** The premise is incorrect; the standard deviation of the sample means (the standard error) decreases as the sample size increases, which causes the confidence interval to become narrower [openstax_intro_stats_2e:7.1:chunk-002].
**Citas declaradas:** openstax_intro_stats_2e:7.1:chunk-002
**Referencia:** (sin puntuar)
- **citations_ok** — A: `0` · B: `1` → **árbitro: `0`**
  - A: Corrige la premisa, pero su única cita no respalda la afirmación adicional sobre el estrechamiento del intervalo.
  - B: Corrige la premisa falsa (el error estándar disminuye al crecer n, como dice 7.1:chunk-002) y añade la consecuencia sobre el intervalo, presente en el contexto; la cita sostiene la correcció
  - Árbitro: La única cita respalda la disminución del error estándar, pero no la afirmación adicional sobre el estrechamiento del intervalo, cuya evidencia aparece en otros fragmentos no citados.

---

## CASO 97 — q-v1-008__explicit · qwen3.5:4b · bm25
**Disputa:** faithfulness
**Pregunta:** Why does the standard error of the sample mean increase as the sample size becomes larger?
**Conducta esperada:** grounded_correction · declarada: grounded_correction
**Respuesta:** The premise is false; the standard error of the sample mean decreases as the sample size becomes larger because it is inversely proportional to the square root of n (σ/√n).
**Citas declaradas:** openstax_intro_stats_2e:7.3:chunk-002, openstax_principles_ds:4.1:chunk-011
**Referencia:** (sin puntuar)
- **faithfulness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Corrige la premisa y la disminución está respaldada, aunque la fórmula exacta no se ve completa en los fragmentos recuperados.
  - B: Corrige la premisa falsa con la relación σ/√n y la disminución del error con n mayor, respaldada por 7.3:chunk-002 y 4.1:chunk-011.
  - Árbitro: 7.3:chunk-002 respalda que la desviación de las medias disminuye al aumentar n, pero la fórmula σ/√n y la proporcionalidad exacta no aparecen legibles en los fragmentos suministrados.

---

## CASO 98 — q-v1-011__explicit · qwen3.5:4b · dense
**Disputa:** citations_ok
**Pregunta:** For a standardized normal variable, what values define its center and spread, and how should the sign and magnitude of its standardized score be interpreted?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** For a standardized normal variable, the center is defined by a mean of 0 and the spread by a standard deviation of 1; its standardized score (z-score) indicates how many standard deviations a value lies from the mean, where a positive sign means right of the mean and negative means left.
**Citas declaradas:** openstax_principles_ds:3.5:chunk-014
**Referencia:** The standard normal distribution has mean 0 and standard deviation 1. A z-score states how many standard deviations a value lies from the mean: a positive score is above the mean, a negative score is below it, and zero corresponds to the mean.
- **citations_ok** — A: `0` · B: `1` → **árbitro: `0`**
  - A: Da la media, la desviación y la interpretación del signo, pero la cita declarada no explica explícitamente los signos del z-score.
  - B: Media 0, desviación 1 e interpretación del z-score coinciden con la referencia y están respaldadas por chunk-014 y la explicación de puntajes z de 6.1:chunk-005; solo omite el caso z = 0, de
  - Árbitro: El fragmento citado respalda la media, la desviación y la magnitud del z-score, pero no interpreta su signo; el juez 2 completa ese respaldo con 6.1:chunk-005, que no figura entre las citas declaradas.

---

## CASO 99 — q-v1-011__explicit · qwen3.5:9b · rerank
**Disputa:** factual_correctness
**Pregunta:** For a standardized normal variable, what values define its center and spread, and how should the sign and magnitude of its standardized score be interpreted?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** For a standardized normal variable (standard normal distribution), the center is defined by a mean of 0 and the spread by a standard deviation of 1. A positive z-score indicates a value above the mean, a negative z-score indicates a value below the mean, and the magnitude represents the number of standard deviations from the mean.
**Citas declaradas:** openstax_principles_ds:3.5:chunk-014, openstax_intro_stats_2e:6.1:chunk-002
**Referencia:** The standard normal distribution has mean 0 and standard deviation 1. A z-score states how many standard deviations a value lies from the mean: a positive score is above the mean, a negative score is below it, and zero corresponds to the mean.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `2`**
  - A: Da la media, la desviación y el sentido de los signos, pero omite que una puntuación cero corresponde a la media.
  - B: Media 0, desviación 1 e interpretación del signo y la magnitud del z-score coinciden con la referencia y con chunk-6.1:002, que las dos citas contienen.
  - Árbitro: Coincide con la referencia en el centro, la dispersión y la interpretación del signo y la magnitud; no explicitar el caso cero no constituye una omisión esencial, pues queda implícito como distancia nula a la media.

---

## CASO 100 — q-v1-011__implicit · gemma4:e4b · dense
**Disputa:** factual_correctness
**Pregunta:** For the normal distribution in its reference form, what values define its center and spread, and how should the sign and magnitude of its standardized score be interpreted?
**Conducta esperada:** answer · declarada: answer
**Respuesta:** For the standard normal distribution, the center is a mean of 0 and the spread is a standard deviation of 1. A standardized score indicates how many standard deviations a measurement is from the mean; positive scores are to the right of the mean, and negative scores are to the left of the mean [openstax_principles_ds:3.5:chunk-014].
**Citas declaradas:** openstax_principles_ds:3.5:chunk-014
**Referencia:** The standard normal distribution has mean 0 and standard deviation 1. A z-score states how many standard deviations a value lies from the mean: a positive score is above the mean, a negative score is below it, and zero corresponds to the mean.
- **factual_correctness** — A: `1` · B: `2` → **árbitro: `2`**
  - A: Da la media 0, la desviación 1 y la interpretación del z-score; solo omite mencionar expresamente el caso z = 0.
  - B: Da los valores 0 y 1 e interpreta el signo de la puntuación tipificada tal como pide la referencia, todo apoyado en el chunk citado.
  - Árbitro: Identifica correctamente la media 0, la desviación estándar 1 y la interpretación del signo y la magnitud; no explicitar el caso de puntuación cero no altera la coincidencia esencial con la referencia.