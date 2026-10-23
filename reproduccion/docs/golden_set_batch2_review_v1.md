# Revisión humana del segundo lote del golden set v1

## Estado

Este documento presenta doce propuestas en estado `draft`. El archivo canónico es `data/golden/golden_set_pilot_v1.jsonl`; los diez primeros registros adjudicados no se modifican. Las casillas sirven para revisar el segundo lote y no constituyen adjudicación final.

- Registros nuevos: 12
- Respondibles: 7
- No respondibles: 5
- Tipos: factual 3, explanatory 2, comparative 4, procedural 3
- Preguntas con conjunto canónico multichunk: 4
- Idioma: inglés
- Revisiones automáticas registradas: 2 por pregunta (jueces de familias distintas)
- Revisión humana inicial: completada; 7 aceptadas, 5 revisadas y ninguna excluida
- Adjudicación humana final: completada; 12 registros adjudicados como `accept` por `andres`
- Estado final del segundo lote: `adjudicated`

## Vista general

| QID | Tipo | Respondibilidad | Categoría | Pregunta |
|---|---|---|---|---|
| q-v1-011 | factual | answerable | — | For a standardized normal variable, what values define its center and spread, and how should the sign and magnitude of its standardized score be interpreted? |
| q-v1-012 | explanatory | answerable | — | With confidence level and population variability held constant, how does a larger sample affect the error bound and the width of a confidence interval? |
| q-v1-013 | comparative | answerable | — | Which distribution should be used to construct a confidence interval for a population mean when the population standard deviation is known versus when it is estimated by the sample standard deviation, and how do degrees of freedom enter the Student t case? |
| q-v1-014 | procedural | answerable | — | What sequence should be followed to flag unusually low or high observations using the middle 50% of an ordered dataset? |
| q-v1-015 | comparative | answerable | — | How do the ordinary mean, a trimmed mean, and the median respond differently to extreme observations? |
| q-v1-016 | comparative | answerable | — | How do count-based outcomes differ from measurement-based outcomes in the kinds of numerical values they can take? |
| q-v1-017 | procedural | answerable | — | When is one-way ANOVA an appropriate choice, and how are its null and alternative hypotheses framed? |
| q-v1-018 | factual | unanswerable | nonexistent_entity_or_concept | What is the quartile-normalized z-score, and how does it combine the interquartile range with the standard deviation? |
| q-v1-019 | factual | unanswerable | missing_evidence | According to the selected sources, what is the Shapiro-Wilk p-value for the women's heights dataset? |
| q-v1-020 | explanatory | unanswerable | false_premise | Why does increasing the confidence level make the confidence interval narrower when all other inputs are fixed? |
| q-v1-021 | comparative | unanswerable | insufficient_evidence | How do one-way ANOVA and the Kruskal-Wallis test differ in their distributional assumptions and interpretation? |
| q-v1-022 | procedural | unanswerable | out_of_scope | How should a chi-square test of independence be conducted for a contingency table? |

## Revisión automática 1

- **Revisor:** `judge-1-gpt-5.6-sol-high`
- **Modelo:** `openai-codex/gpt-5.6-sol; reasoning_effort=high`
- **Prompt:** `golden_set_review_prompt_v1`
- **Fecha:** 2026-08-17
- **Salida bruta:** `data/golden/reviews/judge1_batch2_reviews_2026-08-17.json`
- **Respondibilidad:** siete `answerable` y cinco `unanswerable`, sin discrepancias.
- **Respuesta/anotación:** cinco `accept`, dos `revise` y cinco `not_applicable`.

El juez solicita revisar dos gradaciones. En q-v1-011 considera que el chunk 6.1:chunk-003 aporta evidencia directa sobre signo y magnitud del z-score y debería pasar de grado 1 a 2. En q-v1-013 considera que 8.1:chunk-002 restablece directamente el caso de desviación poblacional conocida y también debería pasar de grado 1 a 2. Las etiquetas no se modifican todavía; las discrepancias se conservarán para contrastarlas con el juez 2 y la adjudicación humana.

## Revisión automática 2

- **Revisor:** `judge-2-glm-5.3-xhigh`
- **Modelo:** `opencode-go/glm-5.3; reasoning_effort=xhigh`
- **Prompt:** `golden_set_review_prompt_v1`
- **Fecha:** 2026-08-17
- **Salida bruta:** `data/golden/reviews/judge2_batch2_reviews_2026-08-17.json`
- **Respondibilidad:** siete `answerable` y cinco `unanswerable`, sin discrepancias.
- **Respuesta/anotación:** siete `accept` y cinco `not_applicable`.
- **Confianza declarada:** entre 0,90 y 0,95.

El juez 2 validó las 19 citas de las preguntas respondibles como subcadenas exactas de sus chunks y confirmó los cinco negativos con búsquedas corpus-wide activas.

## Comparación entre jueces

| QID | Etiqueta propuesta | Juez 1 (GPT) | Juez 2 (GLM) | Desacuerdo |
|---|---|---|---|---|
| q-v1-011 | answerable | answerable · revise (grado del chunk 6.1:chunk-003) | answerable · accept | Sí, gradación |
| q-v1-012 | answerable | answerable · accept | answerable · accept | No |
| q-v1-013 | answerable | answerable · revise (grado del chunk 8.1:chunk-002) | answerable · accept | Sí, gradación |
| q-v1-014 | answerable | answerable · accept | answerable · accept | No |
| q-v1-015 | answerable | answerable · accept | answerable · accept | No |
| q-v1-016 | answerable | answerable · accept | answerable · accept | No |
| q-v1-017 | answerable | answerable · accept | answerable · accept | No |
| q-v1-018 | unanswerable | unanswerable · n/a | unanswerable · n/a | No |
| q-v1-019 | unanswerable | unanswerable · n/a | unanswerable · n/a | No |
| q-v1-020 | unanswerable | unanswerable · n/a | unanswerable · n/a | No |
| q-v1-021 | unanswerable | unanswerable · n/a | unanswerable · n/a | No |
| q-v1-022 | unanswerable | unanswerable · n/a | unanswerable · n/a | No |

Ambos jueces coinciden en la respondibilidad de los doce registros y en las cinco categorías de no respondibilidad. El único desacuerdo afectaba a la gradación de dos chunks no canónicos. Andrés resolvió mantener 6.1:chunk-003 en grado 1 para q-v1-011, porque no cubre el centro y la dispersión solicitados, y promover 8.1:chunk-002 a grado 2 para q-v1-013, porque restablece directamente el caso de desviación poblacional conocida. Ninguna decisión modifica el conjunto canónico ni las respuestas de referencia.

## Adjudicación humana final

Andrés adjudicó los doce registros con decisión `accept`. La adjudicación confirma la respondibilidad, la suficiencia del conjunto canónico, las respuestas de referencia y las gradaciones finales tras resolver los dos desacuerdos. Los registros q-v1-011 a q-v1-022 pasan a estado `adjudicated`.

## Pool BM25+dense y triage auxiliar

Para ampliar los qrels se unieron los top-10 de `bm25_v1_22q` y `dense_e5_base_v2_22q`. El pool contiene 340 candidatos únicos; 19 ya estaban juzgados y 321 son nuevos. La procedencia de los métodos se ocultó en `pool_bm25_dense_blind_v1_22q.jsonl`.

El triage inicial utilizó el prompt versionado `pool_review_prompt_v1.md` con GPT y GLM. Los jueces coincidieron en 200 de 321 grados y discreparon en 121; seis candidatos fueron marcados por GPT como posibles conflictos de respondibilidad. Esta primera hoja de 163 candidatos quedó sustituida por `three_judge_risk_directed_v1` tras incorporar a Kimi k3 y reducir la adjudicación a 109 candidatos. La selección reducida se completó el 2026-08-24, pero todavía no se ha incorporado a los qrels.

Hoja de adjudicación humana:

`docs/pool_bm25_dense_human_adjudication_v1.md`

## Fichas de revisión

### q-v1-011

**Question:** For a standardized normal variable, what values define its center and spread, and how should the sign and magnitude of its standardized score be interpreted?

**Semantic type:** factual

**Answerability:** answerable

**Gold answer:** The standard normal distribution has mean 0 and standard deviation 1. A z-score states how many standard deviations a value lies from the mean: a positive score is above the mean, a negative score is below it, and zero corresponds to the mean.

**Annotated evidence:**

- **Chunk:** `openstax_intro_stats_2e:6.1:chunk-002`
- **Judgement:** grade 2, canonical
- **Source:** *Introductory Statistics 2e*, The Normal Distribution — The Standard Normal Distribution
- **Supports:** Defines the standard normal distribution, gives its mean and standard deviation, and interprets z-score magnitude and sign.
- **Exact quote:**

> The standard normal distribution is a normal distribution of standardized values called z-scores. A z-score is
> measured in units of the standard deviation. For example, if the mean of a normal distribution is five and the
> standard deviation is two, the value 11 is three standard deviations above (or to the right of) the mean. The calculation is
> as follows:
>
> x = μ + (z)(σ) = 5 + (3)(2) = 11
>
> The z-score is three.
>
> The mean for the standard normal distribution is zero, and the standard deviation is one. The transformation z =
>
> produces the distribution Z ~ N(0, 1). The value x in the given equation comes from a normal distribution with mean μ
> and standard deviation σ.
>
> Z-Scores
>
> If X is a normally distributed random variable and X ~ N(μ, σ), then the z-score is:
>
> The z-score tells you how many standard deviations the value x is above (to the right of) or below (to the left of)
> the mean, μ. Values of x that are larger than the mean have positive z-scores, and values of x that are smaller than the
> mean have negative z-scores. If x equals the mean, then x has a z-score of zero.

- **Chunk:** `openstax_intro_stats_2e:6.1:chunk-003`
- **Judgement:** grade 1, noncanonical
- **Source:** *Introductory Statistics 2e*, The Normal Distribution — The Standard Normal Distribution
- **Supports:** Provides redundant context for the sign of a z-score but does not define the standard normal center and spread.
- **Exact quote:**

> Values of x that are larger than the mean have positive z-scores, and values of x that are smaller than the
> mean have negative z-scores. If x equals the mean, then x has a z-score of zero.
>
> EXAMPLE 6.1
>
> Suppose X ~ N(5, 6). This says that X is a normally distributed random variable with mean μ = 5 and standard deviation σ
> = 6. Suppose x = 17. Then:
>
> This means that x = 17 is two standard deviations (2σ) above or to the right of the mean μ = 5.
>
> Notice that: 5 + (2)(6) = 17 (The pattern is μ + zσ = x)
>
> Now suppose x = 1. Then: z =
>  =
>  = –0.67 (rounded to two decimal places)
>
> This means that x = 1 is 0.67 standard deviations (–0.67σ) below or to the left of the mean μ = 5. Notice that: 5 +
> (–0.67)(6) is approximately equal to one (This has the pattern μ + (–0.67)σ = 1)
>
> Summarizing, when z is positive, x is above or to the right of μ and when z is negative, x is to the left of or below μ. Or,
> when z is positive, x is greater than μ, and when z is negative x is less than μ.

**Annotation note:** Covers an underrepresented chapter and separates parameter recall from interpretation of the standardized score.

**Human review:**

- [x] Accept
- [ ] Revise
- [ ] Exclude

**Review notes:** Accepted by Andrés during human review.

---

### q-v1-012

**Question:** With confidence level and population variability held constant, how does a larger sample affect the error bound and the width of a confidence interval?

**Semantic type:** explanatory

**Answerability:** answerable

**Gold answer:** A larger sample decreases the error bound and therefore makes the confidence interval narrower, provided that the confidence level and population variability remain fixed.

**Annotated evidence:**

- **Chunk:** `openstax_intro_stats_2e:8.1:chunk-011`
- **Judgement:** grade 2, canonical
- **Source:** *Introductory Statistics 2e*, Confidence Intervals — A Single Population Mean using the Normal Distribution
- **Supports:** Directly states the relationship between sample size, error bound, and interval width in both directions.
- **Exact quote:**

> If we increase the sample size n to 100, we decrease the error bound.
>
> When n = 100: EBM =
>  = (1.645)
>  = 0.4935.
>
> Solution
> If we decrease the sample size n to 25, we increase the error bound.
>
> When n = 25: EBM =
>  = (1.645)
>  = 0.987.
>
> Summary: Effect of Changing the Sample Size
>
> • Increasing the sample size causes the error bound to decrease, making the confidence interval narrower.
> • Decreasing the sample size causes the error bound to increase, making the confidence interval wider.

- **Chunk:** `openstax_intro_stats_2e:8.1:chunk-012`
- **Judgement:** grade 2, noncanonical
- **Source:** *Introductory Statistics 2e*, Confidence Intervals — A Single Population Mean using the Normal Distribution
- **Supports:** Repeats the direct relationship in an overlapping chunk.
- **Exact quote:**

> Summary: Effect of Changing the Sample Size
>
> • Increasing the sample size causes the error bound to decrease, making the confidence interval narrower.
> • Decreasing the sample size causes the error bound to increase, making the confidence interval wider.

**Annotation note:** Uses a relationship stated verbally and does not depend on reconstructing the degraded formula.

**Human review:**

- [ ] Accept
- [x] Revise
- [ ] Exclude

**Review notes:** Revised at Andrés's request to keep the reference answer proportional to the question and remove the unrequested inverse case.

---

### q-v1-013

**Question:** Which distribution should be used to construct a confidence interval for a population mean when the population standard deviation is known versus when it is estimated by the sample standard deviation, and how do degrees of freedom enter the Student t case?

**Semantic type:** comparative

**Answerability:** answerable

**Gold answer:** Use the normal distribution when the population standard deviation is known. When it is unknown and estimated by the sample standard deviation, use Student's t-distribution. For a simple random sample from an approximately normal population, the t-distribution has n − 1 degrees of freedom, which determine its exact shape.

**Annotated evidence:**

- **Chunk:** `openstax_intro_stats_2e:8.1:chunk-001`
- **Judgement:** grade 2, canonical
- **Source:** *Introductory Statistics 2e*, Confidence Intervals — A Single Population Mean using the Normal Distribution
- **Supports:** Establishes the normal-distribution case when the population standard deviation is known.
- **Exact quote:**

> A confidence interval for a population mean, when the population standard deviation is known, is based on the
> conclusion of the Central Limit Theorem that the sampling distribution of the sample means follow an approximately
> normal distribution. Suppose that our sample has a mean of
>  and we have constructed the 90% confidence
> interval (5, 15) where EBM = 5.
>
> Calculating the Confidence Interval
>
> To construct a confidence interval for a single unknown population mean μ, where the population standard deviation
> is known, we need  as an estimate for μ and we need the margin of error. Here, the margin of error (EBM) is called the
> error bound for a population mean (abbreviated EBM). The sample mean  is the point estimate of the unknown
> population mean μ.

- **Chunk:** `openstax_intro_stats_2e:8.2:chunk-003`
- **Judgement:** grade 2, canonical
- **Source:** *Introductory Statistics 2e*, Confidence Intervals — A Single Population Mean using the Student t Distribution
- **Supports:** Establishes when to use Student's t-distribution and explains the n − 1 degrees of freedom.
- **Exact quote:**

> With graphing calculators and computers, the practice
> now is to use the Student's t-distribution whenever s is used as an estimate for σ.
>
> If you draw a simple random sample of size n from a population that has an approximately normal distribution with
>
> mean μ and unknown population standard deviation σ and calculate the t-score t =
> , then the t-scores follow a
>
> Student's t-distribution with n – 1 degrees of freedom. The t-score has the same interpretation as the z-score. It
> measures how far  is from its mean μ. For each sample size n, there is a different Student's t-distribution.
>
> The degrees of freedom, n – 1, come from the calculation of the sample standard deviation s. This calculation requires n
> deviations
> . Because the sum of the deviations is zero, we can find the last deviation once we know the other
> n – 1 deviations. The other n – 1 deviations can change or vary freely. We call the number n – 1 the degrees of freedom
> (df).

- **Chunk:** `openstax_intro_stats_2e:8.2:chunk-002`
- **Judgement:** grade 1, noncanonical
- **Source:** *Introductory Statistics 2e*, Confidence Intervals — A Single Population Mean using the Student t Distribution
- **Supports:** Provides historical and methodological context for replacing the unknown population standard deviation with the sample estimate.
- **Exact quote:**

> In practice, we rarely know the population standard deviation. In the past, when the sample size was large, this did not
> present a problem to statisticians. They used the sample standard deviation s as an estimate for σ and proceeded as
> before to calculate a confidence interval with close enough results. However, statisticians ran into problems when the
> sample size was small. A small sample size caused inaccuracies in the confidence interval.
>
> William S. Gosset (1876–1937) of the Guinness brewery in Dublin, Ireland ran into this problem. His experiments with
> hops and barley produced very few samples. Just replacing σ with s did not produce accurate results when he tried to
> calculate a confidence interval. He realized that he could not use a normal distribution for the calculation; he found that
>
> the actual distribution depends on the sample size. This problem led him to "discover" what is called the Student's t-
> distribution. The name comes from the fact that Gosset wrote under the pen name "Student."

- **Chunk:** `openstax_intro_stats_2e:8.1:chunk-002`
- **Judgement:** grade 2, noncanonical
- **Source:** *Introductory Statistics 2e*, Confidence Intervals — A Single Population Mean using the Normal Distribution
- **Supports:** Provides a shorter redundant statement for the known-standard-deviation side only.
- **Exact quote:**

> A confidence interval for a population mean with a known standard deviation is based on the fact that the sample means
> follow an approximately normal distribution.

**Annotation note:** Multichunk comparison across two sections; the canonical set is the minimum pair needed to cover both cases.

**Human review:**

- [ ] Accept
- [x] Revise
- [ ] Exclude

**Review notes:** Revised at Andrés's request to replace the vague term “population variability” with “population standard deviation” and explicitly frame the task as confidence-interval construction.

---

### q-v1-014

**Question:** What sequence should be followed to flag unusually low or high observations using the middle 50% of an ordered dataset?

**Semantic type:** procedural

**Answerability:** answerable

**Gold answer:** Order the data and determine the first and third quartiles. Compute the interquartile range as the difference between the third and first quartiles, use the quartiles and a 1.5-IQR cutoff to define lower and upper bounds, and flag values below the lower bound or above the upper bound for further investigation.

**Annotated evidence:**

- **Chunk:** `openstax_principles_ds:3.3:chunk-004`
- **Judgement:** grade 2, canonical
- **Source:** *Principles of Data Science*, Descriptive Statistics: Statistical Measurements and Probability Distributions — Measures of Position
- **Supports:** Defines how to locate the quartiles, defines the IQR, and states its use for flagging outliers.
- **Exact quote:**

> To find the first quartile,
> , locate the middle value of the lower half of the data (5.4, 6.0, 6.3, 6.8, 7.1). The
> middle value of the lower half of the dataset is 6.3. Notice that one-fourth, or 25%, of the data values are
> below this first quartile, and 75% of the data values are above this first quartile.
>
> To find the third quartile,
> , locate the middle value of the upper half of the data (7.4, 7.5, 7.9, 8.2, 8.7). The middle value of the upper half of the dataset is 7.9. Notice that one-fourth, or 25%, of the data values
> are above this third quartile, and 75% of the data values are below this third quartile.
>
> Thus, the quartiles
> ,
> ,
>  for this dataset are 6.3, 7.2, 7.9, respectively.
>
> The interquartile range (IQR) is a number that indicates the spread of the middle half, or the middle 50%, of
> the data. It is the difference between the third quartile,
> , and the first quartile,
> .
>
> Note that the IQR provides a measure of variability that excludes outliers.
>
> In Example 3.11, the IQR can be calculated as:
>
> Quartiles and the IQR can be used to flag possible outliers in a dataset.

- **Chunk:** `openstax_principles_ds:3.3:chunk-005`
- **Judgement:** grade 2, canonical
- **Source:** *Principles of Data Science*, Descriptive Statistics: Statistical Measurements and Probability Distributions — Measures of Position
- **Supports:** Provides the lower/upper-bound rule and the 1.5-IQR cutoff.
- **Exact quote:**

> To detect outliers, you can use the quartiles and the IQR to calculate a lower and an upper bound for outliers. Then any data values below the lower bound or above the upper bound will be flagged as outliers. These data
> values should be further investigated to determine the nature of the outlier condition and whether the data
> values are valid or not.
>
> To calculate the lower and upper bounds for outliers, use the following formulas:
>
> These formulas typically use 1.5 as a cutoff value to identify outliers in a dataset.

- **Chunk:** `openstax_principles_ds:3.3:chunk-006`
- **Judgement:** grade 2, noncanonical
- **Source:** *Principles of Data Science*, Descriptive Statistics: Statistical Measurements and Probability Distributions — Measures of Position
- **Supports:** Applies the procedure to a worked example but does not replace the general rule.
- **Exact quote:**

> First, determine the median of the dataset. There are 13 data values, so the median is the middle data
> value, which is 488,800.
>
> Next, calculate the
>  and
> .
>
> For the first quartile, look at the data values below the median. The two middle data values in this lower half
> of the data are 230,500 and 387,000. To determine the first quartile, find the mean of these two data values.
>
> For the third quartile, look at the data values above the median. The two middle data values in this upper
> half of the data are 639,000 and 659,000. To determine the third quartile, find the mean of these two data
> values.
>
> Now, calculate the interquartile range (IQR):
>
> Calculate the value of 1.5 interquartile range (IQR):
>
> Calculate the lower and upper bound for outliers:
>
> The lower bound for outliers is −201,625. Of course, no home price is less than −201,625, so no outliers are
> present for the lower end of the dataset.
>
> The upper bound for outliers is 1,159,375. The data value of 5,500,000 is greater than the upper bound of
> 1,159,375. Therefore, the home price of $5,500,000 is a potential outlier.

**Annotation note:** Multichunk procedure. The answer states the verbal 1.5-IQR rule without reconstructing missing formula glyphs.

**Human review:**

- [ ] Accept
- [x] Revise
- [ ] Exclude

**Review notes:** Revised at Andrés's request: the worked example is directly sufficient to reconstruct the procedure, so its relevance changes from grade 1 to grade 2 while remaining noncanonical.

---

### q-v1-015

**Question:** How do the ordinary mean, a trimmed mean, and the median respond differently to extreme observations?

**Semantic type:** comparative

**Answerability:** answerable

**Gold answer:** Extreme observations can disproportionately skew the ordinary mean. A trimmed mean reduces their influence by removing a selected percentage of values from both tails before averaging. The median depends on the middle position of the ordered data and is not affected by the numerical magnitude of the outliers.

**Annotated evidence:**

- **Chunk:** `openstax_principles_ds:3.1:chunk-005`
- **Judgement:** grade 2, canonical
- **Source:** *Principles of Data Science*, Descriptive Statistics: Statistical Measurements and Probability Distributions — Measures of Center
- **Supports:** Explains how outliers distort the mean and how a trimmed mean reduces their influence.
- **Exact quote:**

> A trimmed mean helps mitigate the effects of outliers, which are data values that are significantly different
> from most of the other data values in the dataset. In the dataset given in Example 3.1, a pulse rate of 35 or 120
> would be considered outlier data values since these pulse rates are significantly different as compared to the
> rest of the values in Example 3.1. We will see that there is a formal method for determining outliers, and in fact
> there are several methods to identify outliers in a dataset.
>
> The presence of outlier data values tends to disproportionally skew the mean and produce a potentially
> misleading result for the mean.
>
> To calculate the trimmed mean for a dataset, first sort the data in ascending order (from smallest to largest). Then decide on a certain percentage of data values to be deleted from the lower and upper ends of the
> dataset. This might represent the extent of outliers in the dataset; trimmed mean percentages of 10% and 20%
> are common.

- **Chunk:** `openstax_principles_ds:3.1:chunk-008`
- **Judgement:** grade 2, canonical
- **Source:** *Principles of Data Science*, Descriptive Statistics: Statistical Measurements and Probability Distributions — Measures of Center
- **Supports:** Explains why the median is resistant to the numerical magnitude of outliers.
- **Exact quote:**

> Since the median
> focuses on the middle value of the ordered dataset, the median is preferred when outliers are present because
> the median is not affected by the numerical values of the outliers.

- **Chunk:** `openstax_principles_ds:3.1:chunk-011`
- **Judgement:** grade 2, noncanonical
- **Source:** *Principles of Data Science*, Descriptive Statistics: Statistical Measurements and Probability Distributions — Measures of Center
- **Supports:** Provides a noncanonical example contrasting mean and median under one extreme salary.
- **Exact quote:**

> The following example illustrates the point
> that the median is a better measure of central tendency when potential outliers are present.
>
> EXAMPLE 3.5
>
> Problem
>
> Suppose that in a small company of 40 employees, one person earns a salary of $3 million per year, and the
> other 39 individuals each earn $40,000. Which is the better measure of center: the mean or the median?
>
> Solution
>
> The mean, in dollars, would be arrived at mathematically as follows:
>
> However, the median would be $40,000 since this is the middle data value in the ordered dataset. There are
> 39 people who earn $40,000 and one person who earns $3,000,000.
>
> Notice that the mean is not representative of the typical value in the dataset since $114,000 is not reflective
> of the average salary for most employees (who are earning $40,000). The median is a much better measure
> of the “average” than the mean in this case because 39 of the values are $40,000 and one is $3,000,000. The
> data value of $3,000,000 is an outlier. The median result of $40,000 gives us a better sense of the center of
> the dataset.

**Annotation note:** Multichunk comparison that extends the earlier median item by contrasting three measures rather than repeating a single definition.

**Human review:**

- [x] Accept
- [ ] Revise
- [ ] Exclude

**Review notes:** Accepted by Andrés during human review.

---

### q-v1-016

**Question:** How do count-based outcomes differ from measurement-based outcomes in the kinds of numerical values they can take?

**Semantic type:** comparative

**Answerability:** answerable

**Gold answer:** A discrete random variable takes a finite or countably infinite set of distinct values and typically results from counting. A continuous random variable can take any value within an interval and typically results from measurement.

**Annotated evidence:**

- **Chunk:** `openstax_principles_ds:3.5:chunk-002`
- **Judgement:** grade 2, canonical
- **Source:** *Principles of Data Science*, Descriptive Statistics: Statistical Measurements and Probability Distributions — Discrete and Continuous Probability Distributions
- **Supports:** Defines both variable types, their possible values, and their typical count-versus-measurement origins.
- **Exact quote:**

> Discrete random variable—a random variable is considered discrete if there is a finite or countable
> number of values that the random variable can take on. (If there are infinitely many values, the number of
> values is countable if it possible to count them individually.) Typically, a discrete random variable is the
> result of a count of some kind. For example, if the random variable  represents the number of cars in a
>
> parking lot, then the values that x can take on can only be whole numbers since it would not make sense
> to have
>  cars in the parking lot.
> • Continuous random variable—a random variable is considered continuous if the value of the random
> variable can take on any value within an interval. Typically, a continuous random variable is the result of a
> measurement of some kind. For example, if the random variable  represents the weight of a bag of
> apples, then  can take on any value such as
>  pounds of apples.

- **Chunk:** `openstax_principles_ds:3.5:chunk-003`
- **Judgement:** grade 2, noncanonical
- **Source:** *Principles of Data Science*, Descriptive Statistics: Statistical Measurements and Probability Distributions — Discrete and Continuous Probability Distributions
- **Supports:** Provides a redundant summary of the distinction between countable values and values within an interval.
- **Exact quote:**

> To summarize, the difference between discrete and continuous probability distributions has to do with the
> nature of the random variables they represent. Discrete probability distributions are associated with
> variables that take on a finite or countably infinite number of distinct values. Continuous probability
> distributions deal with random variables that can take on any value within a given range or interval. It is
> important to identify and distinguish between discrete and continuous random variables since different
> statistical methods are used to analyze each type.

**Annotation note:** Covers probability distributions with one direct definition and one known redundant chunk.

**Human review:**

- [ ] Accept
- [x] Revise
- [ ] Exclude

**Review notes:** Revised at Andrés's request: the operation contrasts two categories, so the semantic type changes from `explanatory` to `comparative`.

---

### q-v1-017

**Question:** When is one-way ANOVA an appropriate choice, and how are its null and alternative hypotheses framed?

**Semantic type:** procedural

**Answerability:** answerable

**Gold answer:** One-way ANOVA is appropriate for comparing three or more population means when there is one independent variable. Its null hypothesis states that all population means are equal, while its alternative states that at least one population mean differs from the others.

**Annotated evidence:**

- **Chunk:** `openstax_principles_ds:4.4:chunk-002`
- **Judgement:** grade 2, canonical
- **Source:** *Principles of Data Science*, Inferential Statistics and Regression Analysis — Analysis of Variance (ANOVA)
- **Supports:** Defines the use of one-way ANOVA for three or more means and one independent variable.
- **Exact quote:**

> In Testing Claims Based on One Sample, we reviewed methods to conduct hypothesis testing for two means;
> however, there are scenarios where a researcher might want to compare three or more means to determine if
> any of the means are different from one another. For example, a medical researcher might want to compare
> three different pain relief medications to compare the average time to provide relief from a migraine
> headache. Analysis of variance (ANOVA) is a statistical method that allows a researcher to compare three or
> more means and determine if the means are all statistically the same or if at least one mean is different from
> the others. The one-way ANOVA focuses on one independent variable. For two independent variables, a
> method called “two-way ANOVA” is applicable, but this method is beyond the scope of this text. We explore the
> one-way ANOVA next.
>
> One-Way ANOVA
>
> To compare three or more means, the sample sizes for each group can be different sample sizes (samples
> sizes do not need to be identical). For one-way ANOVA hypothesis testing, we will follow the same general
>
> outline of steps for hypothesis testing that was discussed in Hypothesis Testing.
>
> The first step will be to write the null and alternative hypotheses.

- **Chunk:** `openstax_principles_ds:4.4:chunk-003`
- **Judgement:** grade 2, canonical
- **Source:** *Principles of Data Science*, Inferential Statistics and Regression Analysis — Analysis of Variance (ANOVA)
- **Supports:** States the null and alternative hypotheses for one-way ANOVA.
- **Exact quote:**

> The first step will be to write the null and alternative hypotheses. For one-way ANOVA, the null and alternative
> hypotheses are always stated as the following:
>
> : All population means are equal:
>
> : At least one population mean is different from the others.

**Annotation note:** Multichunk procedural-selection item that extends corpus coverage to the ANOVA section.

**Human review:**

- [x] Accept
- [ ] Revise
- [ ] Exclude

**Review notes:** Accepted by Andrés during human review.

---

### q-v1-018

**Question:** What is the quartile-normalized z-score, and how does it combine the interquartile range with the standard deviation?

**Semantic type:** factual

**Answerability:** unanswerable

**Unanswerable category:** nonexistent_entity_or_concept

**Corpus-boundary rationale:** The corpus defines quartiles, IQR, and z-scores separately but contains no concept named a quartile-normalized z-score. A corpus-wide search found no occurrence of that term or an equivalent combined statistic.

**Expected behavior:** Abstain and state that the named concept is not defined in the provided sources.

**Human review:**

- [x] Accept
- [ ] Revise
- [ ] Exclude

**Review notes:** Accepted by Andrés during human review.

---

### q-v1-019

**Question:** According to the selected sources, what is the Shapiro-Wilk p-value for the women's heights dataset?

**Semantic type:** factual

**Answerability:** unanswerable

**Unanswerable category:** missing_evidence

**Corpus-boundary rationale:** The corpus contains a women's heights confidence-interval activity but reports no Shapiro-Wilk test or p-value for that dataset. A corpus-wide search found no occurrence of Shapiro or Wilk.

**Expected behavior:** Abstain and state that the provided sources do not contain sufficient evidence.

**Human review:**

- [ ] Accept
- [x] Revise
- [ ] Exclude

**Review notes:** Revised at Andrés's request to remove the presupposition that a Shapiro-Wilk p-value had been reported and preserve the `missing_evidence` category.

---

### q-v1-020

**Question:** Why does increasing the confidence level make the confidence interval narrower when all other inputs are fixed?

**Semantic type:** explanatory

**Answerability:** unanswerable

**Unanswerable category:** false_premise

**Corpus-boundary rationale:** The premise contradicts the corpus: increasing the confidence level increases the error bound and makes the interval wider. The expected behavior is to reject the premise rather than explain it.

**Expected behavior:** Reject the premise, state the direction supported by the corpus, and avoid fabricating an explanation.

**Human review:**

- [x] Accept
- [ ] Revise
- [ ] Exclude

**Review notes:** Accepted by Andrés during human review.

---

### q-v1-021

**Question:** How do one-way ANOVA and the Kruskal-Wallis test differ in their distributional assumptions and interpretation?

**Semantic type:** comparative

**Answerability:** unanswerable

**Unanswerable category:** insufficient_evidence

**Corpus-boundary rationale:** The corpus explains one-way ANOVA but contains no Kruskal-Wallis test, its assumptions, or its interpretation. One complete side of the requested comparison is absent.

**Expected behavior:** Abstain and state that the provided sources do not contain sufficient evidence.

**Human review:**

- [x] Accept
- [ ] Revise
- [ ] Exclude

**Review notes:** Accepted by Andrés during human review.

---

### q-v1-022

**Question:** How should a chi-square test of independence be conducted for a contingency table?

**Semantic type:** procedural

**Answerability:** unanswerable

**Unanswerable category:** out_of_scope

**Corpus-boundary rationale:** The selected chapters do not cover chi-square tests of independence or contingency-table procedures. A corpus-wide search found no occurrence of chi-square test, test of independence, or contingency table.

**Expected behavior:** Abstain and state that the provided sources do not contain sufficient evidence.

**Human review:**

- [x] Accept
- [ ] Revise
- [ ] Exclude

**Review notes:** Accepted by Andrés during human review.

---
