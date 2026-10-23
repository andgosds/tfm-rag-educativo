# Revisión humana del primer lote del golden set v1

## Estado

Este documento presenta diez propuestas en estado `draft`. El archivo canónico es `data/golden/golden_set_pilot_v1.jsonl`. Las casillas de esta hoja sirven para revisar redacción, respondibilidad, respuesta y evidencia; no constituyen adjudicación hasta que la decisión se incorpore al JSONL.

- Registros: 10
- Respondibles: 6
- No respondibles: 4
- Tipos: factual 2, explanatory 3, comparative 3, procedural 2
- Idioma: inglés
- Revisiones automáticas registradas: 2 por pregunta (jueces de familias distintas)
- Revisión humana inicial: completada; 7 aceptadas, 3 revisadas y ninguna excluida
- Adjudicación humana final: completada; 10 registros adjudicados como `accept` por `andres` el 2026-08-17
- Estado final del lote: `adjudicated`

## Vista general

| QID | Tipo | Respondibilidad | Categoría | Pregunta |
|---|---|---|---|---|
| q-v1-001 | explanatory | answerable | — | How does increasing the sample size affect the sampling distribution of the sample mean? |
| q-v1-002 | comparative | answerable | — | How do Type I and Type II errors differ in terms of the truth of the null hypothesis and the decision made? |
| q-v1-003 | procedural | answerable | — | What sequence of steps should be followed to conduct a hypothesis test? |
| q-v1-004 | explanatory | answerable | — | Why is the median a suitable measure of center when a dataset contains extreme outliers? |
| q-v1-005 | factual | answerable | — | What two aspects of the relationship between an independent and a dependent variable are summarized by the correlation coefficient? |
| q-v1-006 | comparative | answerable | — | If all other inputs remain unchanged, how does increasing the confidence level from 90% to 95% affect the width of the confidence interval, and why? |
| q-v1-007 | factual | unanswerable | missing_evidence | According to the selected sources, what is the Pearson correlation between weekly study time and final exam score? |
| q-v1-008 | explanatory | unanswerable | false_premise | Why does the standard error of the sample mean increase as the sample size becomes larger? |
| q-v1-009 | comparative | unanswerable | insufficient_evidence | How do Pearson correlation and Spearman rank correlation differ in their assumptions and sensitivity to outliers? |
| q-v1-010 | procedural | unanswerable | out_of_scope | How should a Bayesian credible interval for a population mean be computed using a conjugate prior? |

## Revisión automática 1

- **Revisor:** `judge-1-gpt-5.6-sol-high`
- **Modelo:** `openai-codex/gpt-5.6-sol; reasoning_effort=high`
- **Prompt:** `golden_set_review_prompt_v1`
- **Fecha:** 2026-08-17
- **Salida bruta:** `data/golden/reviews/judge1_golden_reviews_2026-08-17.json`
- **Resultado:** seis preguntas respondibles con evidencia suficiente y respuesta aceptada; cuatro preguntas no respondibles con evidencia insuficiente y respuesta de referencia no aplicable.
- **Acuerdo con las etiquetas propuestas:** 10 de 10 registros.
- **Confianza declarada:** entre 0,99 y 1,00; no debe interpretarse como confianza calibrada.

El juez se ejecutó en una sesión aislada sin acceso a esta hoja de revisión humana. Pertenece, no obstante, a la misma familia de modelo que colaboró en la creación inicial del lote. Su dictamen es una revisión auxiliar y no una validación plenamente independiente.

## Revisión automática 2

- **Revisor:** `judge-2-glm-5.3-xhigh`
- **Modelo:** `opencode-go/glm-5.3; reasoning_effort=xhigh`
- **Prompt:** `golden_set_review_prompt_v1`
- **Fecha:** 2026-08-17
- **Salida bruta:** `data/golden/reviews/judge2_golden_reviews_2026-08-17.json`
- **Resultado:** seis preguntas respondibles con evidencia suficiente y respuesta aceptada; cuatro preguntas no respondibles con evidencia insuficiente y respuesta de referencia no aplicable.
- **Acuerdo con las etiquetas propuestas:** 10 de 10 registros.
- **Confianza declarada:** entre 0,93 y 0,97.

El juez se ejecutó en una sesión aislada, sobre una copia del golden set con `reviews` vacío, sin acceso a esta hoja ni a la salida del juez 1. Pertenece a una familia de modelo distinta, lo que reduce el riesgo de errores correlacionados entre jueces.

## Comparación entre jueces

| QID | Etiqueta propuesta | Juez 1 | Juez 2 | Desacuerdo |
|---|---|---|---|---|
| q-v1-001 | answerable | answerable · accept | answerable · accept | No |
| q-v1-002 | answerable | answerable · accept | answerable · accept | No |
| q-v1-003 | answerable | answerable · accept | answerable · accept | No |
| q-v1-004 | answerable | answerable · accept | answerable · accept | No |
| q-v1-005 | answerable | answerable · accept | answerable · accept | No |
| q-v1-006 | answerable | answerable · accept | answerable · accept | No |
| q-v1-007 | unanswerable | unanswerable · n/a | unanswerable · n/a | No |
| q-v1-008 | unanswerable | unanswerable · n/a | unanswerable · n/a | No |
| q-v1-009 | unanswerable | unanswerable · n/a | unanswerable · n/a | No |
| q-v1-010 | unanswerable | unanswerable · n/a | unanswerable · n/a | No |

Ambos jueces coincidieron entre sí y con las etiquetas propuestas en los diez registros. No hay desacuerdos que resolver. Ese consenso total no debe leerse como acuerdo interanotador humano: los dos jueces son automáticos y pueden compartir sesgos, y uno de ellos pertenece a la familia del anotador inicial.

## Adjudicación humana final

Tras la revisión inicial y las dos revisiones automáticas, Andrés adjudicó los diez registros con decisión `accept`. La adjudicación confirma las etiquetas de respondibilidad, la suficiencia de la evidencia y las respuestas de referencia vigentes tras las tres revisiones de redacción (q-v1-003, q-v1-006 y q-v1-007). La decisión queda registrada en el campo `human_adjudication` de cada registro y el lote pasa a estado `adjudicated`.

## Fichas de revisión

### q-v1-001

**Question:** How does increasing the sample size affect the sampling distribution of the sample mean?

**Semantic type:** explanatory

**Answerability:** answerable

**Gold answer:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.

**Canonical evidence:**

- **Chunk:** `openstax_intro_stats_2e:7.1:chunk-002`
- **Source:** *Introductory Statistics 2e*, The Central Limit Theorem — The Central Limit Theorem for Sample Means (Averages)
- **Supports:** Explains the limiting shape, center, and spread of the sampling distribution as sample size increases.
- **Exact quote:**

> The central limit theorem for sample means says that if you repeatedly draw samples of a given size (such as
> repeatedly rolling ten dice) and calculate their means, those means tend to follow a normal distribution (the sampling
> distribution). As sample sizes increase, the distribution of means more closely follows the normal distribution. The
> normal distribution has the same mean as the original distribution and a variance that equals the original variance
> divided by the sample size. Standard deviation is the square root of variance, so the standard deviation of the sampling
> distribution is the standard deviation of the original distribution divided by the square root of n.

**Annotation note:** Tests explanation of three linked effects of sample size rather than recall of a single formula.

**Human review:**

- [x] Accept
- [ ] Revise
- [ ] Exclude

**Review notes:** Accepted by Andrés during human review.

---

### q-v1-002

**Question:** How do Type I and Type II errors differ in terms of the truth of the null hypothesis and the decision made?

**Semantic type:** comparative

**Answerability:** answerable

**Gold answer:** A Type I error occurs when a true null hypothesis is rejected. A Type II error occurs when a false null hypothesis is not rejected.

**Canonical evidence:**

- **Chunk:** `openstax_intro_stats_2e:9.2:chunk-001`
- **Source:** *Introductory Statistics 2e*, Hypothesis Testing with One Sample — Outcomes and the Type I and Type II Errors
- **Supports:** Defines both error types using the actual status of the null hypothesis and the statistical decision.
- **Exact quote:**

> The four possible outcomes in the table are:
>
> 1. The decision is not to reject H0 when H0 is true (correct decision). 2. The decision is to reject H0 when H0 is true (incorrect decision known as aType I error). 3. The decision is not to reject H0 when, in fact, H0 is false (incorrect decision known as a Type II error). 4. The decision is to reject H0 when H0 is false (correct decision whose probability is called the Power of the Test).

**Annotation note:** Uses a symmetric comparison to reduce confusion between the two error types.

**Human review:**

- [x] Accept
- [ ] Revise
- [ ] Exclude

**Review notes:** Accepted by Andrés during human review.

---

### q-v1-003

**Question:** What sequence of steps should be followed to conduct a hypothesis test?

**Semantic type:** procedural

**Answerability:** answerable

**Gold answer:** Formulate null and alternative hypotheses from the claim, collect relevant sample data, select the appropriate sampling distribution, analyze the data using a test statistic and p-value, and then reject or fail to reject the null hypothesis according to whether the sample is inconsistent with it.

**Canonical evidence:**

- **Chunk:** `openstax_principles_ds:4.2:chunk-003`
- **Source:** *Principles of Data Science*, Inferential Statistics and Regression Analysis — Hypothesis Testing
- **Supports:** Provides the ordered five-step hypothesis-testing procedure and the two possible decisions.
- **Exact quote:**

> The steps for hypothesis testing are as follows:
>
> 1. Set up a null and alternative hypothesis based on the claim. Identify whether the null or the alternative
> hypothesis represents the claim. 2. Collect relevant sample data to investigate the claim. 3. Determine the correct distribution to be used to analyze the hypothesis test (e.g., normal distribution or t-
> distribution). 4. Analyze the sample data to determine if the sample data is consistent with the null hypothesis. This will
> involve statistical calculations involving what is called a test statistic and a p-value (discussed in the next
> section). 5. If the sample data is inconsistent with the null hypothesis, then the decision is to “reject the null
> hypothesis.” If the sample data is consistent with the null hypothesis, then the decision is to “fail to reject
> the null hypothesis.”

**Annotation note:** Requires an ordered procedure rather than isolated definitions of null hypothesis or p-value.

**Human review:**

- [ ] Accept
- [x] Revise
- [ ] Exclude

**Review notes:** Revised at Andrés's request to remove the unsupported one-sample restriction and the word “complementary”.

---

### q-v1-004

**Question:** Why is the median a suitable measure of center when a dataset contains extreme outliers?

**Semantic type:** explanatory

**Answerability:** answerable

**Gold answer:** The median depends on the middle position of the ordered data and is not affected by the numerical magnitude of extreme values.

**Canonical evidence:**

- **Chunk:** `openstax_principles_ds:3.1:chunk-008`
- **Source:** *Principles of Data Science*, Descriptive Statistics: Statistical Measurements and Probability Distributions — Measures of Center
- **Supports:** States that the median is based on the middle value and is not affected by the numerical values of outliers.
- **Exact quote:**

> Since the median
> focuses on the middle value of the ordered dataset, the median is preferred when outliers are present because
> the median is not affected by the numerical values of the outliers.

**Annotation note:** The reference answer stays within the two claims stated directly in the canonical evidence.

**Human review:**

- [x] Accept
- [ ] Revise
- [ ] Exclude

**Review notes:** Accepted by Andrés during human review. The obsolete annotation note was cleaned up without changing the question, answer or evidence.

---

### q-v1-005

**Question:** What two aspects of the relationship between an independent and a dependent variable are summarized by the correlation coefficient?

**Semantic type:** factual

**Answerability:** answerable

**Gold answer:** The correlation coefficient summarizes the strength and the direction of the correlation.

**Canonical evidence:**

- **Chunk:** `openstax_principles_ds:4.3:chunk-006`
- **Source:** *Principles of Data Science*, Inferential Statistics and Regression Analysis — Correlation and Linear Regression Analysis
- **Supports:** Directly identifies strength and direction as the two aspects represented by the coefficient.
- **Exact quote:**

> The correlation coefficient is a measure of the strength and direction of the correlation between the
> independent variable  and the dependent variable .

**Annotation note:** A short factual item from Principles of Data Science without relying on degraded formula symbols.

**Human review:**

- [x] Accept
- [ ] Revise
- [ ] Exclude

**Review notes:** Accepted by Andrés during human review.

---

### q-v1-006

**Question:** If all other inputs remain unchanged, how does increasing the confidence level from 90% to 95% affect the width of the confidence interval, and why?

**Semantic type:** comparative

**Answerability:** answerable

**Gold answer:** The 95% confidence interval is wider than the 90% interval because greater confidence requires an interval that covers a larger range of plausible values for the population parameter.

**Canonical evidence:**

- **Chunk:** `openstax_principles_ds:4.1:chunk-010`
- **Source:** *Principles of Data Science*, Inferential Statistics and Regression Analysis — Statistical Inference and Confidence Intervals
- **Supports:** Directly compares the interval widths and explains why greater confidence requires a wider interval.
- **Exact quote:**

> Notice that the 95% confidence interval is wider. If the confidence level is increased, with all other
>
> parameters held constant, we should expect that the confidence interval will become wider. Another way to
> consider this: the wider the confidence interval, the more likely the interval is to contain the true population
> mean. This makes intuitive sense in that if you want to be more certain that the true value of the parameter
> is within an interval, then the interval needs to be wider to account for a larger range of potential values. As
> an analogy, consider a person trying to catch a fish. The wider the net used, the higher the probability of
> catching a fish.

**Annotation note:** Compares confidence levels conceptually without requiring reconstruction of a formula.

**Human review:**

- [ ] Accept
- [x] Revise
- [ ] Exclude

**Review notes:** Revised at Andrés's request to replace “range of plausible values” with the more precise term “width of the confidence interval” and to ask explicitly for the reason.

---

### q-v1-007

**Question:** According to the selected sources, what is the Pearson correlation between weekly study time and final exam score?

**Semantic type:** factual

**Answerability:** unanswerable

**Unanswerable category:** missing_evidence

**Corpus-boundary rationale:** The corpus explains Pearson correlation but reports no coefficient relating weekly study time to final exam score. A corpus-wide search found no such empirical result.

**Expected behavior:** Abstain and state that the provided sources do not contain sufficient evidence.

**Human review:**

- [ ] Accept
- [x] Revise
- [ ] Exclude

**Review notes:** Revised at Andrés's request to remove the presupposition that the coefficient had been reported and preserve the `missing_evidence` category.

---

### q-v1-008

**Question:** Why does the standard error of the sample mean increase as the sample size becomes larger?

**Semantic type:** explanatory

**Answerability:** unanswerable

**Unanswerable category:** false_premise

**Corpus-boundary rationale:** The premise contradicts the corpus: the standard error decreases as sample size increases. The expected system behavior is to reject the premise rather than invent an explanation.

**Expected behavior:** Reject the premise, state the direction supported by the corpus, and avoid fabricating a causal explanation.

**Human review:**

- [x] Accept
- [ ] Revise
- [ ] Exclude

**Review notes:** Accepted by Andrés during human review.

---

### q-v1-009

**Question:** How do Pearson correlation and Spearman rank correlation differ in their assumptions and sensitivity to outliers?

**Semantic type:** comparative

**Answerability:** unanswerable

**Unanswerable category:** insufficient_evidence

**Corpus-boundary rationale:** The corpus discusses Pearson correlation but does not cover Spearman rank correlation, its assumptions, or its sensitivity to outliers. One side of the requested comparison is therefore absent.

**Expected behavior:** Abstain and state that the provided sources do not contain sufficient evidence.

**Human review:**

- [x] Accept
- [ ] Revise
- [ ] Exclude

**Review notes:** Accepted by Andrés during human review.

---

### q-v1-010

**Question:** How should a Bayesian credible interval for a population mean be computed using a conjugate prior?

**Semantic type:** procedural

**Answerability:** unanswerable

**Unanswerable category:** out_of_scope

**Corpus-boundary rationale:** The selected chapters cover frequentist confidence intervals but not Bayesian priors, posterior distributions, conjugacy, or credible-interval procedures. A corpus-wide search found no supporting evidence.

**Expected behavior:** Abstain and state that the provided sources do not contain sufficient evidence.

**Human review:**

- [x] Accept
- [ ] Revise
- [ ] Exclude

**Review notes:** Accepted by Andrés during human review.

---
