# Lote 16 (FINAL) — validación humana del arbitraje (casos 151–158)

## CASO 151 — q-v3-007__explicit · qwen3.5:9b · rrf
**Disputa:** factual_correctness
**Pregunta:** By how much does the power of a test increase when the sample size doubles at a fixed significance level?
**Conducta esperada:** grounded_correction · declarada: abstain
**Respuesta:** I cannot answer from the supplied contexts.
**Citas declaradas:** NONE
**Referencia:** (sin puntuar)
- **factual_correctness** — A: `0` · B: `1` → **árbitro: `0`**
  - A: No hay incremento numérico deducible, pero el contexto permite corregir la premisa: solo indica que aumentar la muestra puede aumentar la potencia.
  - B: La abstención no afirma nada falso y no lleva citas, pero se esperaba un grounded_correction: el contexto sí permite decir que aumentar n sube la potencia sin que exista un incremento fijo, 
  - Árbitro: La respuesta no aporta la corrección esencial: el contexto indica que aumentar la muestra puede aumentar la potencia, pero no establece cuánto aumenta al duplicarla; no afirmar falsedades no basta para considerarla parcialmente correcta.

---

## CASO 152 — q-v3-007__implicit · gemma4:e4b · bm25
**Disputa:** behavior_ok
**Pregunta:** By how much does the ability of a test to detect a real effect increase when the sample size doubles at a fixed significance level?
**Conducta esperada:** grounded_correction · declarada: grounded_correction
**Respuesta:** The provided contexts do not contain information about how the ability of a test to detect a real effect changes when the sample size doubles at a fixed significance level. The contexts discuss the effect of changing sample size on the error bound and confidence interval width, but not the specific quantitative relationship described in the question.
**Citas declaradas:** openstax_intro_stats_2e:8.1:chunk-011
**Referencia:** (sin puntuar)
- **behavior_ok** — A: `1` · B: `2` → **árbitro: `1`**
  - A: Advierte correctamente que no hay una cuantificación para duplicar la muestra, pero compara intervalos de confianza sin aclarar la cuestión de la potencia.
  - B: Marca como no respaldada la relación cuantitativa presupuesta por la pregunta y se apoya en lo que el contexto sí cubre (8.1:chunk-011 sobre error bound y amplitud del intervalo), que es el 
  - Árbitro: Delimita correctamente la falta de respaldo para cuantificar el incremento, pero se limita a explicar la insuficiencia del contexto sin corregir la presuposición de que duplicar la muestra determina un incremento concreto.

---

## CASO 153 — q-v3-007__implicit · gemma4:e4b · rrf
**Disputa:** factual_correctness
**Pregunta:** By how much does the ability of a test to detect a real effect increase when the sample size doubles at a fixed significance level?
**Conducta esperada:** grounded_correction · declarada: abstain
**Respuesta:** I cannot answer from the supplied contexts.
**Citas declaradas:** NONE
**Referencia:** (sin puntuar)
- **factual_correctness** — A: `1` · B: `0` → **árbitro: `0`**
  - A: No inventa una magnitud, pero tampoco aclara que los contextos no establecen un incremento fijo al duplicar la muestra.
  - B: Debía corregir la premisa de un aumento cuantificable y se abstiene; eso sí, los chunks recuperados no contienen el concepto de potencia, de modo que la abstención no afirma nada que contrad
  - Árbitro: Aunque la falta de información sobre potencia justifica la cautela, la abstención no contiene una respuesta correcta en lo esencial ni la corrección requerida, por lo que no corresponde conceder crédito parcial.

---

## CASO 154 — q-v3-007__implicit · qwen3.5:4b · rerank
**Disputa:** behavior_ok
**Pregunta:** By how much does the ability of a test to detect a real effect increase when the sample size doubles at a fixed significance level?
**Conducta esperada:** grounded_correction · declarada: abstain
**Respuesta:** I cannot answer from the supplied contexts.
**Citas declaradas:** NONE
**Referencia:** (sin puntuar)
- **behavior_ok** — A: `1` · B: `0` → **árbitro: `0`**
  - A: Evita inventar una magnitud, pero se abstiene sin explicar que el contexto no permite cuantificar el cambio.
  - B: Se abstiene sin afirmar nada falso, pero la conducta esperada era corregir la premisa de un incremento predeterminado, y la respuesta ni la menciona ni la rectifica.
  - Árbitro: La respuesta se limita a abstenerse y no corrige la premisa de un incremento predeterminado, por lo que no realiza la grounded_correction esperada.

---

## CASO 155 — q-v3-007__implicit · qwen3.5:9b · rrf
**Disputa:** factual_correctness
**Pregunta:** By how much does the ability of a test to detect a real effect increase when the sample size doubles at a fixed significance level?
**Conducta esperada:** grounded_correction · declarada: abstain
**Respuesta:** I cannot answer from the supplied contexts.
**Citas declaradas:** NONE
**Referencia:** (sin puntuar)
- **factual_correctness** — A: `0` · B: `1` → **árbitro: `0`**
  - A: Se abstiene en vez de aclarar que el contexto no fija cuánto aumenta la potencia al duplicar la muestra.
  - B: Con la premisa de un aumento cuantificable, lo esperado era corregirla apoyándose en que el contexto solo sostiene la dirección del efecto; la abstención no contradice el contexto pero incum
  - Árbitro: La abstención no explica que los fragmentos no permiten establecer un incremento de la capacidad de detección al duplicar la muestra; además, el juez 2 atribuye al contexto una relación explícita con la potencia que estos fragmentos no contienen.

---

## CASO 156 — q-v3-008__explicit · qwen3.5:9b · rerank
**Disputa:** citations_ok
**Pregunta:** How do discrete and continuous probability distributions relate to the sampling distributions used in statistical inference?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The supplied contexts describe discrete and continuous probability distributions as tools to model specific types of random variables (countable vs. measurable ranges) but do not contain information regarding their relationship to sampling distributions used in statistical inference. Therefore, the premise that the provided text explains this specific relationship is incorrect based on the available evidence.
**Citas declaradas:** NONE
**Referencia:** Probability distributions describe the probabilities of the values of a single random variable, which is either discrete, with a finite or countable number of values and typically the result of a count, or continuous, taking any value in an interval. A sampling distribution is built on top of that object: it is the distribution of a statistic computed from repeated samples, and for the mean it approaches a normal distribution as the sample size increases. The second object is therefore a distrib
- **citations_ok** — A: `0` · B: `1` → **árbitro: `1`**
  - A: Distingue variables discretas y continuas, pero no explica la relación con las distribuciones muestrales y no cita el contexto que sí utiliza.
  - B: Su descripción de distribuciones discretas/continuas es fiel a los chunks, pero trate la pregunta como premisa falsa y se abstiene cuando la conducta esperada era responder: la referencia pi
  - Árbitro: La respuesta se abstiene de explicar la relación solicitada y no declara citas, supuesto admitido expresamente por este criterio, con independencia de que su conducta y contenido no satisfagan la pregunta.

---

## CASO 157 — q-v3-008__implicit · gemma4:e4b · bm25
**Disputa:** faithfulness
**Pregunta:** How do the distributions describing the probabilities of individual outcomes relate to the distributions describing the probabilities of statistics computed from samples, which are used to make inferences?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The premise that the provided contexts explain the relationship between distributions for individual outcomes and distributions for sample statistics is incorrect. However, the contexts do explain that the probabilities for an individual value and the probabilities for a sample mean are calculated using different distributions, specifically mentioning that for an individual value, one uses the stated distribution, and for a mean, one uses the Central Limit Theorem (CLT) with the normal distribution [openstax_intro_stats_2e:7.3:chunk-006].
**Citas declaradas:** openstax_intro_stats_2e:7.3:chunk-006
**Referencia:** Probability distributions describe the probabilities of the values of a single random variable, which is either discrete, with a finite or countable number of values and typically the result of a count, or continuous, taking any value in an interval. A sampling distribution is built on top of that object: it is the distribution of a statistic computed from repeated samples, and for the mean it approaches a normal distribution as the sample size increases. The second object is therefore a distrib
- **faithfulness** — A: `0` · B: `1` → **árbitro: `0`**
  - A: El fragmento citado sí distingue probabilidades individuales y de medias muestrales; por eso es erróneo negar que explique esa relación, aunque recupera parte de ella.
  - B: Aporta contenido real y citado (distribución distinta para individuos y para medias vía TLC) que roza la referencia, pero lo enmarca como negación de una premisa que no es falsa y omite la d
  - Árbitro: Niega que el contexto explique la relación entre ambas distribuciones, contradiciendo el fragmento 7.3:chunk-006, que compara explícitamente individuos y medias, aunque después lo resume correctamente.

---

## CASO 158 — q-v3-008__implicit · qwen3.5:4b · rrf
**Disputa:** faithfulness
**Pregunta:** How do the distributions describing the probabilities of individual outcomes relate to the distributions describing the probabilities of statistics computed from samples, which are used to make inferences?
**Conducta esperada:** answer · declarada: grounded_correction
**Respuesta:** The supplied contexts do not describe the relationship between distributions of individual outcomes and distributions of statistics computed from samples; they only state that different distributions (e.g., exponential vs. normal) are used to calculate probabilities for individuals versus means, noting that these probabilities differ because distinct distributions apply to each case.
**Citas declaradas:** openstax_intro_stats_2e:7.3:chunk-006
**Referencia:** Probability distributions describe the probabilities of the values of a single random variable, which is either discrete, with a finite or countable number of values and typically the result of a count, or continuous, taking any value in an interval. A sampling distribution is built on top of that object: it is the distribution of a statistic computed from repeated samples, and for the mean it approaches a normal distribution as the sample size increases. The second object is therefore a distrib
- **faithfulness** — A: `1` · B: `2` → **árbitro: `1`**
  - A: El fragmento citado distingue la distribución individual de la de medias, pero la respuesta niega que se describa esa relación y omite explicarla.
  - B: Recoge con fidelidad el matiz individuo-vs-media que sí está en 7.3:chunk-006 (distribuciones distintas para valores individuales y para medias), pero lo enmarca como negativa en vez de resp
  - Árbitro: La distinción entre individuos y medias está respaldada, pero negar que el contexto describa su relación es excesivo: 7.3:chunk-006 vincula la distribución de las medias con la normal mediante el teorema central del límite.