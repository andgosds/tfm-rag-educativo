# Revisión del pool BM25+dense v1

> Revisión humana ciega de candidatos no juzgados. No se muestra el método que recuperó cada chunk.

## Protocolo

Asignar a cada candidato una relevancia respecto a la pregunta:

- **Grado 0:** no contribuye a responder.
- **Grado 1:** relacionado o útil, pero insuficiente por sí solo.
- **Grado 2:** evidencia directa y suficiente o necesaria junto a otros chunks.

Para los candidatos de preguntas no respondibles, comprobar si existe evidencia material que contradiga la abstención esperada. No usar conocimiento externo al corpus.

## Resumen

- Preguntas: 22
- Candidatos únicos en el pool: 340
- Candidatos ya juzgados: 19
- Candidatos pendientes de revisión: 321
- Preguntas respondibles: 13
- Preguntas no respondibles: 9

La procedencia BM25/dense se conserva únicamente en `pool_bm25_dense_v1_22q.jsonl` y no aparece en esta hoja.

## q-v1-001

**Pregunta:** How does increasing the sample size affect the sampling distribution of the sample mean?

**Respondibilidad de referencia:** answerable

### q-v1-001-pool-001

**Chunk:** `openstax_intro_stats_2e:7.intro:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 7: The Central Limit Theorem
> Section 7.intro: Introduction
>
> The second alternative says that if we again
> collect samples of size n that are "large enough," calculate the sum of each sample and create a histogram, then the
> resulting histogram will again tend to have a normal bell-shape.
>
> The size of the sample, n, that is required in order to be "large enough" depends on the original population from which
> the samples are drawn (the sample size should be at least 30 or the data should come from a normal distribution). If the
> original population is far from normal, then more observations are needed for the sample means or sums to be normal. Sampling is done with replacement.
>
> It would be difficult to overstate the importance of the central limit theorem in statistical theory. Knowing that data, even
> if its distribution is not normal, behaves in a predictable way is a powerful tool.
>
> COLLABORATIVE EXERCISE
>
> Suppose eight of you roll one fair die ten times, seven of you roll two fair dice ten times, nine of you roll five fair dice
> ten times, and 11 of you roll ten fair dice ten times.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-001-pool-002

**Chunk:** `openstax_principles_ds:4.1:chunk-016`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Calculate a 95% confidence interval for the true population proportion of adults who smoke. Also,
> determine if there has been a statistically significant change in the proportion of smokers as compared to
> five years ago.
>
> Solution
>
> For a 95% confidence interval, the corresponding critical value is
> .
>
> Start off by calculating the sample proportion :
>
> Verify that the normal approximation to the binomial distribution is appropriate by ensuring that both
> and
>  are both at least 5, where  represents the sample proportion.
>
> For this example,
> , and
> . Both of these
> results are at least 5, which verifies that the normal approximation to the binomial distribution is
> appropriate.
>
> The margin of error is then calculated as follows:
>
> The 95% confidence interval is calculated as follows:
>
> Concluding statement:
>
> The researcher can be 95% confident that the true population of adult smokers in the United States is
> between 0.218 and 0.262, which can also be written as 21.8% to 26.2%. Since this 95% confidence interval
> excludes the previous value of 28% from five years ago, the researcher can state that there has been a
> statistically significant decrease in the proportion of smokers as compared to five years ago.
>
> Sample Size Determination
>
> When collecting sample data in order to construct a confidence interval for a mean or proportion, how does
> the researcher determine the optimal sample size? Too small of a sample size may lead to a wide confidence
> interval that is not very useful. Too large of a sample size can result in wasted resources if a smaller sample
> size would be sufficient. Sampling is covered in some depth in Handling Large Datasets. Here, we review
> methods to determine minimum sample size requirements when constructing confidence intervals for means
> or proportions.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-001-pool-003

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-011`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> Figure 8.5
>
> Summary: Effect of Changing the Confidence Level
>
> • Increasing the confidence level increases the error bound, making the confidence interval wider.
> • Decreasing the confidence level decreases the error bound, making the confidence interval narrower.
>
> TRY IT 8.4
>
> Refer back to the pizza-delivery Try It exercise. The population standard deviation is six minutes and the sample mean
> deliver time is 36 minutes. Use a sample size of 20. Find a 95% confidence interval estimate for the true mean pizza
> delivery time.
>
> EXAMPLE 8.5
>
> Suppose we change the original problem in Example 8.2 to see what happens to the error bound if the sample size is
> changed.
>
> Problem
> Leave everything the same except the sample size. Use the original 90% confidence level. What happens to the error
> bound and the confidence interval if we increase the sample size and use n = 100 instead of n = 36? What happens if we
>
> decrease the sample size to n = 25 instead of n = 36?
>
> •
>  = 68
>
> • EBM =
>
> • σ = 3; The confidence level is 90% (CL=0.90);
>  = z0.05 = 1.645.
>
> Solution
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
>
> TRY IT 8.5
>
> Refer back to the pizza-delivery Try It exercise.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-001-pool-005

**Chunk:** `openstax_intro_stats_2e:9.2:chunk-004`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.2: Outcomes and the Type I and Type II Errors
>
> In the context of this scenario, we would state that we
> believe that Genetic Labs influences the sex outcome, when in fact it has no effect. The probability of this error occurring
> is denoted by the Greek letter alpha, α.
>
> Type II error: This results when we fail to reject a false null hypothesis. In context, we would state that Genetic Labs
> does not influence the sex outcome of a pregnancy when, in fact, it does. The probability of this error occurring is
> denoted by the Greek letter beta, β.
>
> The error of greater consequence would be the Type I error since people would use the Genetic Labs product in hopes of
> increasing the chances of having a male.
>
> TRY IT 9.7
>
> “Red tide” is a bloom of poison-producing algae–a few different species of a class of plankton called dinoflagellates. When the weather and water conditions cause these blooms, shellfish such as clams living in the area develop
> dangerous levels of a paralysis-inducing toxin. In Massachusetts, the Division of Marine Fisheries (DMF) monitors
> levels of the toxin in shellfish by regular sampling of shellfish along the coastline. If the mean level of toxin in clams
> exceeds 800 μg (micrograms) of toxin per kg of clam meat in any area, clam harvesting is banned there until the
> bloom is over and levels of toxin in clams subside. Describe both a Type I and a Type II error in this context, and state
> which error has the greater consequence.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-001-pool-006

**Chunk:** `openstax_intro_stats_2e:7.1:chunk-006`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 7: The Central Limit Theorem
> Section 7.1: The Central Limit Theorem for Sample Means (Averages)
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> To find percentiles for means on the calculator, follow these steps.
>
> 2nd DIStR
>
> 3:invNorm
>
> k = invNorm
>
> where:
>
> • k = the kth percentile
> • mean is the mean of the original distribution
> • standard deviation is the standard deviation of the original distribution
> • sample size = n
>
> EXAMPLE 7.3
>
> Problem
> In a recent study, it was reported that the mean age of iPad users is 34 years. Suppose the standard deviation is 15
> years. Take a sample of size n = 100.
>
> a. What are the mean and standard deviation for the sample mean ages of iPad users?
> b. What does the distribution look like?
>
> c. Find the probability that the sample mean age is more than 30 years (the reported mean age of iPad users in this
>
> particular study).
> d. Find the 95th percentile for the sample mean age (to one decimal place).
>
> Solution
> a. Since the sample mean tends to target the population mean, we have μχ = μ = 34. The sample standard deviation is
>
> given by σχ =
>  =
>  =
>  = 1.5
>
> b. The central limit theorem states that for large sample sizes(n), the sampling distribution will be approximately
>
> normal.
> c. The probability that the sample mean age is more than 30 is given by
>  = normalcdf(30,E99,34,1.5) =
>
> 0.9962
> d. Let k = the 95th percentile.
>
> k = invNorm
>  = 36.5

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-001-pool-007

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> Use n = 217: Always round the answer UP to the next higher integer to ensure that the sample size is large enough.
>
> Therefore, 217 Foothill College students should be surveyed in order to be 95% confident that we are within two years of
> the true population mean age of Foothill College students.
>
> TRY IT 8.7
>
> The population standard deviation for the height of high school basketball players is three inches. If we want to be
> 95% confident that the sample mean height is within one inch of the true population mean height, how many
> randomly selected students must be surveyed?
>
> 8.2 A Single Population Mean using the Student t Distribution
>
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

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-001-pool-008

**Chunk:** `openstax_intro_stats_2e:7.1:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 7: The Central Limit Theorem
> Section 7.1: The Central Limit Theorem for Sample Means (Averages)
>
> Standard deviation is the square root of variance, so the standard deviation of the sampling
> distribution is the standard deviation of the original distribution divided by the square root of n. The variable n is the
> number of values that are averaged together, not the number of times the experiment is done.
>
> To put it more formally, if you draw random samples of size n, the distribution of the random variable
> , which consists
> of sample means, is called the sampling distribution of the mean. The sampling distribution of the mean approaches a
> normal distribution as n, the sample size, increases.
>
> The random variable
>  has a different z-score associated with it from that of the random variable X. The mean  is the
> value of
>  in one sample.
>
> μX is the average of both X and
> .
>
> standard deviation of
>  and is called the standard error of the mean.
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> To find probabilities for means on the calculator, follow these steps.
>
> 2nd DISTR
>
> 2:normalcdf
>
> where:
>
> • mean is the mean of the original distribution
> • standard deviation is the standard deviation of the original distribution
> • sample size = n
>
> EXAMPLE 7.1
>
> An unknown distribution has a mean of 90 and a standard deviation of 15. Samples of size n = 25 are drawn randomly
> from the population.
>
> Problem
>
> a. Find the probability that the sample mean is between 85 and 92.
>
> Solution
> a. Let X = one value from the original unknown population. The probability question asks you to find a probability for the
> sample mean.
>
> Let  = the mean of a sample of size 25. Since μX = 90, σX = 15, and n = 25,
>
> ~ N
> .
>
> Find P(85 <  < 92). Draw a graph.
>
> P(85 <  < 92) = 0.6997

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-001-pool-009

**Chunk:** `openstax_principles_ds:4.1:chunk-017`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Too large of a sample size can result in wasted resources if a smaller sample
> size would be sufficient. Sampling is covered in some depth in Handling Large Datasets. Here, we review
> methods to determine minimum sample size requirements when constructing confidence intervals for means
> or proportions. Note that the desired margin of error plays a key role in this sample size determination.
>
> Sample Size for Confidence Interval for the Mean
>
> When determining a confidence interval for a mean, a researcher can use the margin of error formula for the
> mean; solving this formula algebraically for the sample size ( ), the following minimum sample size formula
> can be used to determine the minimum sample size needed to achieve a certain margin of error:
>
> Sample size formula for confidence interval for mean:
>
> Where:
>
> is the critical value of the normal distribution.
>  is the population standard deviation.
>
> is the desired margin of error.
>
> Note that for sample size calculations, sample size results are rounded up to the next higher whole number.
>
> For example, if the formula previously shown results in a sample size of 59.2, then the sample size will be
> rounded to 60.
>
> EXAMPLE 4.6
>
> Problem
>
> A benefits analyst is interested in a 90% confidence interval for the mean salary for chemical engineers. What sample size should the analyst use if a margin of error of $1,000 is desired? Assume a population
> standard deviation of $8,000.
>
> Solution
>
> For a 90% confidence interval, the corresponding critical value is
> . The population standard
> deviation is given as $8,000, and the margin of error is given as $1,000.
>
> Using the sample size formula:
>
> Round to the next higher whole number, so the desired sample size is 174.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-001-pool-010

**Chunk:** `openstax_principles_ds:3.2:chunk-004`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.2: Measures of Variation
>
> The more the individual data values differ from the mean, the larger the variance.
>
> A financial advisor might use variance to determine the volatility of an investment and therefore help guide
> financial decisions. For example, a more cautious investor might opt for investments with low volatility.
>
> The formula used to calculate variance also depends on whether the data is collected from a sample or a
>
> population. The notation
>  is used to represent the sample variance, and the notation
>  is used to represent
> the population variance.
>
> Formula for the sample variance:
>
> Formula for the population variance:
>
> In these formulas:
>
> represents the individual data values
>  represents the sample mean
>  represents the sample size
>  represents the population mean
>
> represents the population size
>
> ALTERNATE FORMULA FOR VARIANCE
>
> An alternate formula for the variance is available. It is sometimes used for more efficient computations:
>
> In the formulas for sample variance and population variance, notice the denominator for the sample variance
> is
> , whereas the denominator for the population variance is
> . The use of
>  in the denominator of the
> sample variance is used to provide the best estimate for the population variance, in the sense that if repeated
> samples of size  are taken and the sample mean computed each time, then the average of those sample
> means will tend to the population mean as the number of repeated samples increase.
>
> It is important to note that in many data science applications, population data is unavailable, and so we
> typically calculate the sample variance. For example, if a researcher wanted to estimate the percentage of
> smokers for all adults in the United States, it would be impractical to collect data from every adult in the United
> States.
>
> Notice that the sample variance is a sum of squares.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-001-pool-011

**Chunk:** `openstax_intro_stats_2e:9.4:chunk-004`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.4: Rare Events, the Sample, Decision and Conclusion
>
> To persuade his customers that he is right, the baker decides to do a hypothesis test. He bakes 10 loaves of bread. The mean height of the sample loaves is 17 cm. The baker knows from baking hundreds of loaves of bread that the
> standard deviation for the height is 0.5 cm. and the distribution of heights is normal.
>
> The null hypothesis could be H0: μ ≤ 15 The alternate hypothesis is Ha: μ > 15
>
> The words "is more than" translates as a ">" so "μ > 15" goes into the alternate hypothesis. The null hypothesis must
> contradict the alternate hypothesis.
>
> By the Central Limit Theorem, the distribution of sample means, for samples of 10 loaves, will be normal with mean μ =
> 15 and standard deviation
> .
>
> Suppose the null hypothesis is true (the mean height of the loaves is no more than 15 cm). Then is the mean height (17
> cm) calculated from the sample unexpectedly large? The hypothesis test works by asking the question how unlikely the
> sample mean would be if the null hypothesis were true. The graph shows how far out the sample mean is on the normal
> curve. The p-value is the probability that, if we were to take other samples, any other sample mean would fall at least as
> far out as 17 cm.
>
> The p-value, then, is the probability that a sample mean is the same or greater than 17 cm. when the population
> mean is, in fact, 15 cm. We can calculate this probability using the normal distribution for means.
>
> Figure 9.2
>
> p-value= P( > 17) which is approximately zero.
>
> A p-value of approximately zero tells us that it is highly unlikely that a loaf of bread rises no more than 15 cm, on
> average.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-001-pool-012

**Chunk:** `openstax_principles_ds:4.1:chunk-022`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Collect many random bootstrap samples of size —for example,
> hundreds or thousands of such samples. Keep in mind that the sampling is done with replacement. 2. For each sample, calculate the sample statistic, which is the sample mean  or the sample proportion . 3. Rank order the sample statistics from smallest to largest. 4. For a 95% confidence interval, find the percentiles P2.5 and P97.5 in the ranked data. These values establish
> the 95% confidence interval. 5. For a 90% confidence interval, find the percentiles P5 and P95. These values establish the 90% confidence
> interval.
>
> EXAMPLE 4.8
>
> Problem
>
> A college administrator is developing new marketing materials to increase enrollment at the college, and
> the administrator is interested in a 90% confidence interval for the mean age of students attending the
> college.
>
> The administrator believes the underlying distribution of ages is skewed (does not follow a normal
> distribution), so a bootstrapping method will be used to construct the confidence interval. The
> administrator selects a random sample of 20 students and records their ages as shown in Table 4.4. Use the
> bootstrapping method to construct the 90% confidence interval by taking repeated samples of size 10.
>
> Student ID
> Student
>
> Age
>
> 001
> 22
>
> 002
> 24
>
> 003
> 21
>
> 004
> 34
>
> Table 4.4 Ages of 20 Randomly
>
> Student ID
> Student
>
> Age
>
> 005
> 29
>
> 006
> 23
>
> 007
> 21
>
> 008
> 20
>
> 009
> 19
>
> 010
> 21
>
> 011
> 25
>
> 012
> 28
>
> 013
> 22
>
> 014
> 37
>
> 015
> 24
>
> 016
> 31
>
> 017
> 23
>
> 018
> 19
>
> 019
> 26
>
> 020
> 20
>
> Table 4.4 Ages of 20 Randomly
> Selected Students from One College
>
> Solution
>
> For the bootstrapping process, we will form samples of size 10 for convenience.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-001-pool-013

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-012`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> When n = 25: EBM =
>  = (1.645)
>  = 0.987.
>
> Summary: Effect of Changing the Sample Size
>
> • Increasing the sample size causes the error bound to decrease, making the confidence interval narrower.
> • Decreasing the sample size causes the error bound to increase, making the confidence interval wider.
>
> TRY IT 8.5
>
> Refer back to the pizza-delivery Try It exercise. The mean delivery time is 36 minutes and the population standard
> deviation is six minutes. Assume the sample size is changed to 50 restaurants with the same sample mean. Find a
> 90% confidence interval estimate for the population mean delivery time.
>
> Working Backwards to Find the Error Bound or Sample Mean
>
> When we calculate a confidence interval, we find the sample mean, calculate the error bound, and use them to calculate
> the confidence interval. However, sometimes when we read statistical studies, the study may state the confidence
> interval only. If we know the confidence interval, we can work backwards to find both the error bound and the sample
> mean.
>
> Finding the Error Bound
>
> • From the upper value for the interval, subtract the sample mean,
> • OR, from the upper value for the interval, subtract the lower value. Then divide the difference by two.
>
> Finding the Sample Mean
>
> • Subtract the error bound from the upper value of the confidence interval,
> • OR, average the upper and lower endpoints of the confidence interval.
>
> Notice that there are two methods to perform each calculation. You can choose the method that is easier to use with the
> information you know.
>
> EXAMPLE 8.6
>
> Suppose we know that a confidence interval is (67.18, 68.82) and we want to find the error bound.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-001-pool-014

**Chunk:** `openstax_principles_ds:4.1:chunk-006`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> A researcher takes repeated samples of size 1,000 from the residents of New York to collect data on mean
> income of residents of New York.
>
> For each sample of size 1,000, we can calculate a sample mean, . If the researcher were to take 50 such
> samples (each of sample size 1,000), a series of sample means can be calculated:
>
> A probability distribution based on all possible random samples of a certain size from a population—or
> sampling (or sample) distribution—can then be analyzed. For example, we can calculate the mean of these
> sample means, and we can calculate the standard deviation of these sample means.
>
> There are two important properties of the sample distribution of these sample means:
>
> 1. The mean of the sample means (notated as
> ) is equal to the population mean .
>
> a. Written mathematically:
>
> 2. The standard deviation of the sample means (notated as
> ) is equal to the population standard deviation
>
> divided by the square root of the sample size .
> a. Written mathematically:
>
> The central limit theorem describes the relationship between the sample distribution of sample means and
>
> the underlying population. This theorem is an important tool that allows data scientists and researchers to use
> sample data to generate inferences for population parameters.
>
> Conditions of the central limit theorem:
>
> • If random samples are taken from any population with mean  and standard deviation, where the sample
> size is at least 30, then the distribution of the sample means approximates a normal (bell-shaped)
> distribution.
> • If random samples are taken from a population that is normally distributed with mean  and standard
> deviation , then the distribution of the sample means approximates a normal (bell-shaped) distribution
> for any sample size
>
> EXAMPLE 4.2
>
> Problem

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-001-pool-015

**Chunk:** `openstax_principles_ds:4.1:chunk-015`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Some terminology will be helpful:
>
> represents the population proportion, which is typically unknown.
>
> represents the sample proportion.
>  represents the number of successes in the sample.
>  represents the sample size.
>
> Here are the requirements to use this procedure:
>
> a. A random sample is selected from the population.
> b. Verify that the normal approximation to the binomial distribution is appropriate by ensuring that both
>
> and
>  are both at least 5, where  represents the sample proportion.
>
> The sample proportion  is calculated as the number of successes divided by the sample size:
>
> When these requirements are met, the margin of error (E) for a confidence interval for proportions is
> calculated according to the following formula:
>
> Where:
>
> is called the critical value of the normal distribution and is calculated as the z-score, which includes the area
> corresponding to the confidence level between
>  and
> .
>
> represents the sample proportion.
>
> is the sample size.
>
> Once the margin of error is calculated, the confidence interval is formed in the same way as the previous
> section. In this case, the point estimate is the sample proportion :
>
> EXAMPLE 4.5
>
> Problem
>
> A medical researcher wants to know if there has been a statistically significant change in the proportion of
> smokers from five years ago, when the proportion of adult smokers in the United States was approximately
> 28%. The researcher selects a random sample of 1,500 adults, and of those, 360 respond that they are
> smokers. Calculate a 95% confidence interval for the true population proportion of adults who smoke. Also,
> determine if there has been a statistically significant change in the proportion of smokers as compared to
> five years ago.
>
> Solution
>
> For a 95% confidence interval, the corresponding critical value is
> .
>
> Start off by calculating the sample proportion :

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-001-pool-016

**Chunk:** `openstax_principles_ds:4.1:chunk-021`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> replaced back in the dataset and is eligible to be selected again for the sample.
>
> For example, a researcher who has collected 100 samples to use for inference may want to estimate a
> confidence interval for the population mean. The researcher can then resample, with replacement, from this
> limited set of 100 observations. They would repeatedly sample 100 and calculate the sample mean. These
> means would then represent the distribution of means (remember the discussion of sampling distribution). Typically, for bootstrapping, repeated samples are taken hundreds or thousands of times and then the sample
> mean is calculated for each sample.
>
> The term “bootstrapping” comes from the old saying “pull yourself up by your bootstraps” to imply a task that
> was accomplished without any outside help. In the statistical sense, bootstrapping refers to the ability to
> estimate parameters based solely on one sample of data from the population without any other assumptions.
>
> The bootstrapping method is considered a nonparametric method since the technique makes no
> assumptions about the probability distribution from which the data are sampled. (Parametric methods, by
> contrast, assume a specific form for the underlying distribution and require estimating parameters.)
>
> Since bootstrapping requires a large number of repeated samples, software (such as Excel, Python, or R) is
> often used to automate the repetitive sampling procedures and construct the confidence intervals.
>
> The bootstrapping procedure for confidence interval estimation for a mean or proportion is as follows:
>
> 1. Start out with a random sample of size . Collect many random bootstrap samples of size —for example,
> hundreds or thousands of such samples. Keep in mind that the sampling is done with replacement. 2. For each sample, calculate the sample statistic, which is the sample mean  or the sample proportion . 3. Rank order the sample statistics from smallest to largest. 4.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-001-pool-017

**Chunk:** `openstax_principles_ds:3.2:chunk-005`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.2: Measures of Variation
>
> For example, if a researcher wanted to estimate the percentage of
> smokers for all adults in the United States, it would be impractical to collect data from every adult in the United
> States.
>
> Notice that the sample variance is a sum of squares. Its units of measurement are squares of the units of
> measurement of the original data. Since these square units are different than the units in the original data,
> this can be confusing. By contrast, standard deviation is measured in the same units as the original dataset,
> and thus the standard deviation is more commonly used to measure the spread of a dataset.
>
> Standard Deviation
>
> The standard deviation of a dataset provides a numerical measure of the overall amount of variation in a
> dataset in the same units as the data; it can be used to determine whether a particular data value is close to or
>
> far from the mean, relative to the typical distance from the mean.
>
> The standard deviation is always positive or zero. It is small when the data values are all concentrated close to
> the mean, exhibiting little variation, or spread. It is larger when the data values are spread out more from the
> mean, exhibiting more variation. A smaller standard deviation implies less variability in a dataset, and a larger
> standard deviation implies more variability in a dataset.
>
> Suppose that we are studying the variability of two companies (A and B) with respect to employee salaries. The
> average salary for both companies is $60,000. For Company A, the standard deviation of salaries is $8,000,
> whereas the standard deviation for salaries for Company B is $19,000. Because Company B has a higher
> standard deviation, we know that there is more variation in the employee salaries for Company B as compared
> to Company A.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-002

**Pregunta:** How do Type I and Type II errors differ in terms of the truth of the null hypothesis and the decision made?

**Respondibilidad de referencia:** answerable

### q-v1-002-pool-002

**Chunk:** `openstax_intro_stats_2e:9.2:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.2: Outcomes and the Type I and Type II Errors
>
> β = probability of a Type II error = P(Type II error) = probability of not rejecting the null hypothesis when the null
> hypothesis is false.
>
> α and β should be as small as possible because they are probabilities of errors. They are rarely zero.
>
> The Power of the Test is 1 – β. Ideally, we want a high power that is as close to one as possible. Increasing the sample
> size can increase the Power of the Test.
>
> The following are examples of Type I and Type II errors.
>
> EXAMPLE 9.5
>
> Suppose the null hypothesis, H0, is: Navah's rock climbing equipment is safe.
>
> Type I error: Navah thinks that her rock climbing equipment may not be safe when, in fact, it really is safe. Type II error:
> Navah thinks that her rock climbing equipment may be safe when, in fact, it is not safe.
>
> α = probability that Navah thinks her rock climbing equipment may not be safe when, in fact, it really is safe. β =
> probability that Navah thinks her rock climbing equipment may be safe when, in fact, it is not safe.
>
> Notice that, in this case, the error with the greater consequence is the Type II error. (If Navah thinks her rock climbing
> equipment is safe, she will go ahead and use it.)
>
> TRY IT 9.5
>
> Suppose the null hypothesis, H0, is: the blood cultures contain no traces of pathogen X. State the Type I and Type II
>
> errors.
>
> EXAMPLE 9.6
>
> Suppose the null hypothesis, H0, is: The victim of an automobile accident is alive when they arrive at the emergency
> room of a hospital.
>
> Type I error: The emergency crew thinks that the victim is dead when, in fact, the victim is alive.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-002-pool-003

**Chunk:** `openstax_intro_stats_2e:9.2:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.2: Outcomes and the Type I and Type II Errors
>
> State the Type I and Type II
>
> errors.
>
> EXAMPLE 9.6
>
> Suppose the null hypothesis, H0, is: The victim of an automobile accident is alive when they arrive at the emergency
> room of a hospital.
>
> Type I error: The emergency crew thinks that the victim is dead when, in fact, the victim is alive. Type II error: The
> emergency crew does not know if the victim is alive when, in fact, the victim is dead.
>
> α = probability that the emergency crew thinks the victim is dead when, in fact, the victim is really alive = P(Type I error).
> β = probability that the emergency crew does not know if the victim is alive when, in fact, the victim is dead = P(Type II
> error).
>
> The error with the greater consequence is the Type I error. (If the emergency crew thinks the victim is dead, they will not
> treat them.)
>
> TRY IT 9.6
>
> Suppose the null hypothesis, H0, is: a patient is not sick. Which type of error has the greater consequence, Type I or
> Type II?
>
> EXAMPLE 9.7
>
> A company called Genetic Labs claims to be able to increase the likelihood that a pregnancy will result in a male being
> born. Statisticians want to test the claim. Suppose that the null hypothesis, H0, is: Genetic Labs has no effect on sex
> outcome.
>
> Type I error: This results when a true null hypothesis is rejected. In the context of this scenario, we would state that we
> believe that Genetic Labs influences the sex outcome, when in fact it has no effect. The probability of this error occurring
> is denoted by the Greek letter alpha, α.
>
> Type II error: This results when we fail to reject a false null hypothesis.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-002-pool-004

**Chunk:** `openstax_intro_stats_2e:9.5:chunk-015`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.5: Additional Information and Full Hypothesis Test Examples
>
> Arrow down to
>
> Prop and arrow to not equals p0. Press ENTER. Arrow down to Calculate and press ENTER. The calculator
>
> calculates the p-value (p = 0.5485) and the test statistic (z-score). Prop not equals .5 is the alternate hypothesis. Do
>
> this set of instructions again except arrow to Draw (instead of Calculate). Press ENTER. A shaded graph appears with
>
> z = 0.6 (test statistic) and p = 0.5485 (p-value). Make sure when you use Draw that no other equations are highlighted
>
> in Y = and the plots are turned off.
>
> The Type I and Type II errors are as follows:
>
> The Type I error is to conclude that the proportion of first-time brides who are younger than their grooms is different
> from 50% when, in fact, the proportion is actually 50%. (Reject the null hypothesis when the null hypothesis is true).
>
> The Type II error is there is not enough evidence to conclude that the proportion of first time brides who are younger
> than their grooms differs from 50% when, in fact, the proportion does differ from 50%. (Do not reject the null hypothesis
> when the null hypothesis is false.)
>
> TRY IT 9.17
>
> A teacher believes that 85% of students in the class will want to go on a field trip to the local zoo. The teacher
> performs a hypothesis test to determine if the percentage is the same or different from 85%. The teacher samples 50
> students and 39 reply that they would want to go to the zoo. For the hypothesis test, use a 1% level of significance.
>
> First, determine what type of test this is, set up the hypothesis test, find the p-value, sketch the graph, and state your
> conclusion.
>
> EXAMPLE 9.18

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-002-pool-005

**Chunk:** `openstax_intro_stats_2e:9.2:chunk-004`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.2: Outcomes and the Type I and Type II Errors
>
> In the context of this scenario, we would state that we
> believe that Genetic Labs influences the sex outcome, when in fact it has no effect. The probability of this error occurring
> is denoted by the Greek letter alpha, α.
>
> Type II error: This results when we fail to reject a false null hypothesis. In context, we would state that Genetic Labs
> does not influence the sex outcome of a pregnancy when, in fact, it does. The probability of this error occurring is
> denoted by the Greek letter beta, β.
>
> The error of greater consequence would be the Type I error since people would use the Genetic Labs product in hopes of
> increasing the chances of having a male.
>
> TRY IT 9.7
>
> “Red tide” is a bloom of poison-producing algae–a few different species of a class of plankton called dinoflagellates. When the weather and water conditions cause these blooms, shellfish such as clams living in the area develop
> dangerous levels of a paralysis-inducing toxin. In Massachusetts, the Division of Marine Fisheries (DMF) monitors
> levels of the toxin in shellfish by regular sampling of shellfish along the coastline. If the mean level of toxin in clams
> exceeds 800 μg (micrograms) of toxin per kg of clam meat in any area, clam harvesting is banned there until the
> bloom is over and levels of toxin in clams subside. Describe both a Type I and a Type II error in this context, and state
> which error has the greater consequence.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-002-pool-006

**Chunk:** `openstax_intro_stats_2e:9.3:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.3: Probability Distribution Needed for Hypothesis Testing
>
> EXAMPLE 9.8
>
> A certain experimental drug claims a cure rate of at least 75% for males with prostate cancer. Describe both the Type I
> and Type II errors in context. Which error is the more serious?
>
> Type I: A cancer patient believes the cure rate for the drug is less than 75% when it actually is at least 75%.
>
> Type II: A cancer patient believes the experimental drug has at least a 75% cure rate when it has a cure rate that is less
> than 75%.
>
> In this scenario, the Type II error contains the more severe consequence. If a patient believes the drug works at least
> 75% of the time, this most likely will influence the patient’s (and doctor’s) choice about whether to use the drug as a
> treatment option.
>
> TRY IT 9.8
>
> Determine both Type I and Type II errors for the following scenario:
>
> Assume a null hypothesis, H0, that states the percentage of adults with jobs is at least 88%.
>
> Identify the Type I and Type II errors from these four statements.
>
> a. Not to reject the null hypothesis that the percentage of adults who have jobs is at least 88% when that
>
> percentage is actually less than 88%
> b. Not to reject the null hypothesis that the percentage of adults who have jobs is at least 88% when the percentage
>
> is actually at least 88%.
> c. Reject the null hypothesis that the percentage of adults who have jobs is at least 88% when the percentage is
>
> actually at least 88%.
> d. Reject the null hypothesis that the percentage of adults who have jobs is at least 88% when that percentage is
>
> actually less than 88%.
>
> 9.3 Probability Distribution Needed for Hypothesis Testing
>
> Earlier in the course, we discussed sampling distributions.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-002-pool-007

**Chunk:** `openstax_principles_ds:4.2:chunk-007`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> A less
> than or equals symbol must be used in the null hypothesis. The complement of less than or equals is a
> greater than symbol, which will be used in the alternative hypothesis. The claim refers to the population
> proportion of smokers, so the symbol  will be used. Notice that this setup will correspond to Setup E from
> Table 4.7. Thus, the setup of the null and alternative hypotheses will be as follows:
>
> The basis of the hypothesis test procedure is to assume that the null hypothesis is true to begin with and then
> examine the sample data to determine if the sample data is consistent with the null hypothesis. Based on this
> analysis, you will decide to either reject the null hypothesis or fail to reject the null hypothesis.
>
> It is important to note that these are the only two possible decisions for any hypothesis test, namely:
>
> • Reject the null hypothesis, or
> • Fail to reject the null hypothesis.
>
> Keep in mind that this decision will be based on statistical analysis of sample data, so there is a small chance of
> coming to a wrong decision. The only way to be absolutely certain of your decision is to test the entire
> population, which is typically not feasible. Since the hypothesis test decision is based on a sample, there are
> two possible errors that can be made by the researcher:
>
> • The researcher rejects the null hypothesis when in fact the null hypothesis is actually true, or a Type I
> error.
> • A researcher fails to reject the null hypothesis when the null hypothesis is actually false, or a Type II error.
>
> In hypothesis testing, the maximum allowed probability of making a Type I error is called the level of
> significance, denoted by the Greek letter alpha, .

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-002-pool-008

**Chunk:** `openstax_intro_stats_2e:9.5:chunk-005`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.5: Additional Information and Full Hypothesis Test Examples
>
> Interpretation of the p-value: If H0 is true, there is a 0.0187 probability (1.87%)that Jeffrey's mean time to swim the
> 25-yard freestyle is 16 seconds or less. Because a 1.87% chance is small, the mean time of 16 seconds or less is unlikely
> to have happened randomly. It is a rare event.
>
> Compare α and the p-value:
>
> α = 0.05 p-value = 0.0187 α > p-value
>
> Make a decision: Since
> p-value, reject H0.
>
> This indicates that you reject the null hypothesis that the mean time to swim the 25-yard freestyle is at least 16.43
> seconds.
>
> Conclusion: At the 5% significance level, there is sufficient evidence that Jeffrey's mean time to swim the 25-yard
> freestyle is less than 16.43 seconds. Thus, based on the sample data, we conclude that Jeffrey swims faster using the new
> goggles.
>
> The Type I and Type II errors for this problem are as follows:
> The Type I error is to conclude that Jeffrey swims the 25-yard freestyle, on average, in less than 16.43 seconds when, in
> fact, he actually swims the 25-yard freestyle, on average, in at least 16.43 seconds. (Reject the null hypothesis when the
> null hypothesis is true.)
>
> The Type II error is that there is not evidence to conclude that Jeffrey swims the 25-yard freestyle, on average, in less
> than 16.43 seconds when, in fact, he actually does swim the 25-yard free-style, on average, in less than 16.43 seconds.
> (Do not reject the null hypothesis when the null hypothesis is false.)
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> Press STAT and arrow over to TESTS. Press 1:Z-Test. Arrow over to Stats and press ENTER. Arrow down and enter
>
> 16.43 for μ0 (null hypothesis), .8 for σ, 16 for the sample mean, and 15 for n.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-002-pool-009

**Chunk:** `openstax_intro_stats_2e:9.5:chunk-017`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.5: Additional Information and Full Hypothesis Test Examples
>
> x = 43, n = 150
>
> p′ =
>
> b. A success is having three cell phones in a household.
>
> c. The level of significance is the preset α. Since α is not given, assume that α = 0.05.
>
> d. p-value = 0.7216
>
> e. Assuming that α = 0.05, α < p-value. The decision is do not reject H0 because there is not sufficient evidence to
> conclude that the proportion of households that have three cell phones is not 30%.
>
> TRY IT 9.18
>
> Marketers believe that 92% of adults in the United States own a cell phone. A cell phone manufacturer believes that
> number is actually lower. 200 American adults are surveyed, of which, 174 report having cell phones. Use a 5% level of
> significance. State the null and alternative hypothesis, find the p-value, state your conclusion, and identify the Type I
> and Type II errors.
>
> The next example is a poem written by a statistics student named Nicole Hart. The solution to the problem follows the
> poem. Notice that the hypothesis test is for a single population proportion. This means that the null and alternate
> hypotheses use the parameter p. The distribution for the test is normal. The estimated proportion p′ is the proportion of
> fleas killed to the total fleas found on Fido. This is sample information. The problem gives a preconceived α = 0.01, for
> comparison, and a 95% confidence interval computation. The poem is clever and humorous, so please enjoy it!
>
> EXAMPLE 9.19
>
> Problem
> My dog has so many fleas,
> They do not come off with ease. As for shampoo, I have tried many types
>
> Even one called Bubble Hype,
> Which only killed 25% of the fleas,
> Unfortunately I was not pleased.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-002-pool-010

**Chunk:** `openstax_principles_ds:4.2:chunk-033`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> Thus the setup
>
> of the null and alternative hypotheses will be as follows:
>
> The mean of the differences is average of the differences column shown in Table 4.13. The mean of the
> differences column is 13.9, and the standard deviation of the differences column is 12.414.
>
> Next, calculate the standardized test statistic as follows:
>
> Notice that since the alternative hypothesis contains a “greater than” symbol, the hypothesis test is called a
> “right tailed” test and the p-value will be calculated as the area under the t-distribution curve to the right of
> the test statistic. The area under the t-distribution curve to the right of a t-score of 3.541 (using degrees of
> freedom
> ) is approximately 0.003. Thus the p-value for this hypothesis test is 0.003.
>
> The final step in the hypothesis testing procedure is to come to a final decision regarding the null
> hypothesis. This is accomplished by comparing the p-value with the level of significance. In this example,
> the p-value is 0.003 and the level of significance is 0.05: since the p-value  level of significance, then the
> decision is to “reject the null hypothesis.”
>
> Conclusion: The decision is to reject the null hypothesis; the claim corresponds to the alternative
> hypothesis. This scenario corresponds to Row 2 in Table 4.8, and “there is enough evidence to support the
> claim that the medication helps to lower cholesterol levels.”
>
> Testing Claims for Two Proportions
>
> Data scientists and researchers are often interested in comparing two proportions. For example, a medical
> researcher might be interested in comparing the percentage of people contracting a respiratory virus for
> those taking a vaccine versus not taking a vaccine.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-002-pool-011

**Chunk:** `openstax_intro_stats_2e:9.1:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.1: Null and Alternative Hypotheses
>
> 5. Make a decision and write a meaningful conclusion.
>
> NOTE
>
> To do the hypothesis test homework problems for this chapter and later chapters, make copies of the appropriate
> special solution sheets. See Appendix E.
>
> 9.1 Null and Alternative Hypotheses
>
> The actual test begins by considering two hypotheses. They are called the null hypothesis and the alternative
> hypothesis. These hypotheses contain opposing viewpoints.
>
> H0: The null hypothesis: It is a statement of no difference between the variables—they are not related. This can often be
> considered the status quo and as a result if you cannot accept the null it requires some action.
>
> Ha: The alternative hypothesis: It is a claim about the population that is contradictory to H0 and what we conclude
> when we reject H0. This is usually what the researcher is trying to prove.
>
> Since the null and alternative hypotheses are contradictory, you must examine evidence to decide if you have enough
> evidence to reject the null hypothesis or not. The evidence is in the form of sample data.
>
> After you have determined which hypothesis the sample supports, you make a decision. There are two options for a
> decision. They are "reject H0" if the sample information favors the alternative hypothesis or "do not reject H0" or "decline
> to reject H0" if the sample information is insufficient to reject the null hypothesis.
>
> Mathematical Symbols Used in H0 and Ha:
>
> H0
> Ha
>
> equal (=)
> not equal (≠) or greater than (>) or less than (<)
>
> greater than or equal to (≥)
> less than (<)
>
> less than or equal to (≤)
> more than (>)
>
> Table 9.1
>
> NOTE
>
> H0 always has a symbol with an equal in it. Ha never has a symbol with an equal in it. The choice of symbol depends
> on the wording of the hypothesis test.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-002-pool-012

**Chunk:** `openstax_intro_stats_2e:9.4:chunk-006`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.4: Rare Events, the Sample, Decision and Conclusion
>
> It may or may not be given to you at the beginning of the problem.
>
> When you make a decision to reject or not reject H0, do as follows:
>
> • If α > p-value, reject H0. The results of the sample data are significant. There is sufficient evidence to conclude that
> H0 is an incorrect belief and that the alternative hypothesis, Ha, may be correct.
> • If α ≤ p-value, do not reject H0. The results of the sample data are not significant.There is not sufficient evidence to
> conclude that the alternative hypothesis,Ha, may be correct.
> • When you "do not reject H0", it does not mean that you should believe that H0 is true. It simply means that the
> sample data have failed to provide sufficient evidence to cast serious doubt about the truthfulness of Ho.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-002-pool-013

**Chunk:** `openstax_intro_stats_2e:9.5:chunk-013`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.5: Additional Information and Full Hypothesis Test Examples
>
> It is believed that a stock price for a particular company will grow at a rate of $5 per week with a standard deviation of
> $1. An investor believes the stock won’t grow as quickly. The changes in stock price is recorded for ten weeks and are
> as follows: $4, $3, $2, $3, $1, $7, $2, $1, $1, $2. Perform a hypothesis test using a 5% level of significance. State the
> null and alternative hypotheses, find the p-value, state your conclusion, and identify the Type I and Type II errors.
>
> EXAMPLE 9.17
>
> Problem
> Joon believes that 50% of first-time brides in the United States are younger than their grooms. She performs a
> hypothesis test to determine if the percentage is the same or different from 50%. Joon samples 100 first-time brides
> and 53 reply that they are younger than their grooms. For the hypothesis test, she uses a 1% level of significance.
>
> Solution
> Set up the hypothesis test:
>
> The 1% level of significance means that α = 0.01. This is a test of a single population proportion.
>
> H0: p = 0.50    Ha: p ≠ 0.50
>
> The words "is the same or different from" tell you this is a two-tailed test.
>
> Calculate the distribution needed:
>
> Random variable: P′ = the percent of of first-time brides who are younger than their grooms.
>
> Distribution for the test: The problem contains no mention of a mean. The information is given in terms of
> percentages. Use the distribution for P′, the estimated proportion.
>
> Therefore,
>
> where p = 0.50, q = 1−p = 0.50, and n = 100
>
> Calculate the p-value using the normal distribution for proportions:
>
> p-value = P (p′ < 0.47 or p′ > 0.53) = 0.5485
>
> where x = 53, p′ =
>  = 0.53.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-003

**Pregunta:** What sequence of steps should be followed to conduct a hypothesis test?

**Respondibilidad de referencia:** answerable

### q-v1-003-pool-001

**Chunk:** `openstax_intro_stats_2e:9.intro:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.intro: Introduction
>
> A statistician will make a decision about these claims. This process is called "hypothesis testing." A hypothesis test
> involves collecting data from a sample and evaluating the data. Then, the statistician makes a decision as to whether or
> not there is sufficient evidence, based upon analyses of the data, to reject the null hypothesis.
>
> In this chapter, you will conduct hypothesis tests on single means and single proportions. You will also learn about the
> errors associated with these tests.
>
> Hypothesis testing consists of two contradictory hypotheses or statements, a decision based on the data, and a
> conclusion. To perform a hypothesis test, a statistician will:
>
> 1. Set up two contradictory hypotheses. 2. Collect sample data (in homework problems, the data or summary statistics will be given to you). 3. Determine the correct distribution to perform the hypothesis test. 4. Analyze sample data by performing the calculations that ultimately will allow you to reject or decline to reject the
> null hypothesis.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-003-pool-002

**Chunk:** `openstax_principles_ds:4.4:chunk-002`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.4: Analysis of Variance (ANOVA)
>
> In this case, we should not assign any interpretation to the
> y-intercept.
>
> In the previous example, the range of data collected for the -variable was from $49,000 to $153,000 spent per
> month on advertising. Since this interval does not include an x-value of zero, we would not provide any
> interpretation for the intercept.
>
> 4.4 Analysis of Variance (ANOVA)
>
> Learning Outcomes
> By the end of this section, you should be able to:
>
> • 4.4.1 Set up and apply one-way analysis of variance hypothesis test.
> • 4.4.2 Use Python to conduct one-way analysis of variance.
>
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

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-003-pool-003

**Chunk:** `openstax_intro_stats_2e:9.intro:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.intro: Introduction
>
> 9
> HYPOTHESIS TESTING WITH ONE
> SAMPLE
>
> Figure 9.1 You can use a hypothesis test to decide if a dog breeder’s claim that every Dalmatian has 35 spots is
> statistically sound. (credit: modification of work “black and white, view, dog, animal, fur, mammal, garden, head,
> vertebrate, beautiful, elegant, rush, attention, dalmatian, dog breed, dog head, noble, stains, animal portrait, head
> drawing, spotty, hundeportrait, dalmatians”/ Pxhere, Public Domain)
>
> Chapter Objectives
>
> By the end of this chapter, the student should be able to:
>
> Differentiate between Type I and Type II Errors
> Describe hypothesis testing in general and in practice
> Conduct and interpret hypothesis tests for a single population mean, population standard deviation
> known. Conduct and interpret hypothesis tests for a single population mean, population standard deviation
> unknown. Conduct and interpret hypothesis tests for a single population proportion.
>
> Introduction
>
> One job of a statistician is to make statistical inferences about populations based on samples taken from the population. Confidence intervals are one way to estimate a population parameter. Another way to make a statistical inference is to
> make a decision about a parameter. For instance, a car dealer advertises that its new small truck gets 35 miles per gallon,
> on average. A tutoring service claims that its method of tutoring helps 90% of its students get an A or a B. A company
> says that women managers in their company earn an average of $60,000 per year.
>
> A statistician will make a decision about these claims. This process is called "hypothesis testing." A hypothesis test
> involves collecting data from a sample and evaluating the data. Then, the statistician makes a decision as to whether or
> not there is sufficient evidence, based upon analyses of the data, to reject the null hypothesis.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-003-pool-005

**Chunk:** `openstax_intro_stats_2e:9.6:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.6: Hypothesis Testing of a Single Mean and Single Proportion
>
> 4. Since the p-value, p = 0.00063, is less than the alpha level of 0.01, the sample data indicates that we should reject
> the null hypothesis. In conclusion, the sample data support the claim that the proportion of individuals with blood
> type AB- in the local province is different from the proportion of individuals in the entire country.
>
> TRY IT 9.22
>
> According to the U.S. Census, there are approximately 201,456,463 residents 20 and older. Statistics from the Criminal
> National Network indicate that, on average, 104,354 murders occur each year for people aged 20 and older. This
> translates into a percentage of murder of 0.052%. In Ohio, there were reported 127 murders for a population of
> 427,648. Conduct an appropriate hypothesis test to determine if there is a statistically significant difference between
> the local murder percentage and the national murder percentage. Use a significance level of 0.01.
>
> 9.6 Hypothesis Testing of a Single Mean and Single Proportion
>
> Stats Lab
>
> Hypothesis Testing of a Single Mean and Single Proportion
> Class Time:
>
> Names:
>
> Student Learning Outcomes
>
> • The student will select the appropriate distributions to use in each case.
> • The student will conduct hypothesis tests and interpret the results.
>
> Television Survey
> In a recent survey, it was stated that Americans watch television on average four hours per day. Assume that σ = 2. Using
> your class as the sample, conduct a hypothesis test to determine if the average for students at your school is lower.
>
> 1. H0: _____________
> 2. Ha: _____________
>
> 3. In words, define the random variable. __________ = ______________________
> 4. The distribution to use for the test is _______________________. 5. Determine the test statistic using your data. 6. Draw a graph and label it appropriately. Shade the actual level of significance.
> a. Graph:
>
> Figure 9.15
>
> b. Determine the p-value.
>
> 7.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-003-pool-006

**Chunk:** `openstax_principles_ds:4.2:chunk-002`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> Using hypothesis
> testing methods, the online retailer can come to a conclusion regarding the marketing campaign to transmit
> ads via text messaging. Hypothesis testing involves setting up a null hypothesis and alternative hypotheses
> based on a claim to be tested and then collecting sample data. A null hypothesis represents a statement of no
> effect or no change in the population; the null hypothesis provides a statement that the value of a population
> parameter is equal to a value. An alternative hypothesis is a complementary statement to the null hypothesis
> and makes a statement that the population parameter has a value that differs from the null hypothesis.
>
> Hypothesis testing allows a data scientist to assess the likelihood of observing results under the assumption of
> the null hypothesis and make judgements about the strength of the evidence against the null hypothesis. It
> provides the foundation for various data science investigations and plays a role at different stages of the
> analyses such as data collection and validation, modeling related tasks, and determination of statistical
> significance.
>
> For example, a local restaurant might claim that the average delivery time for food orders is 30 minutes or
> less. To test the claim, food orders can be placed and corresponding delivery times recorded. If the sample
> data appears to be inconsistent with the null hypothesis, then the decision is to reject the null hypothesis.
>
> Testing Claims Based on One Sample
>
> For our discussion, we will examine hypothesis testing methods for claims involving means or proportions.
> (Hypothesis testing can also be performed for standard deviation or variance, though that is beyond the scope
> of this text.)
>
> The steps for hypothesis testing are as follows:
>
> 1. Set up a null and alternative hypothesis based on the claim. Identify whether the null or the alternative
> hypothesis represents the claim. 2.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-003-pool-007

**Chunk:** `openstax_intro_stats_2e:9.5:chunk-016`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.5: Additional Information and Full Hypothesis Test Examples
>
> The teacher samples 50
> students and 39 reply that they would want to go to the zoo. For the hypothesis test, use a 1% level of significance.
>
> First, determine what type of test this is, set up the hypothesis test, find the p-value, sketch the graph, and state your
> conclusion.
>
> EXAMPLE 9.18
>
> Problem
> Suppose a consumer group suspects that the proportion of households that have three cell phones is 30%. A cell phone
>
> company has reason to believe that the proportion is not 30%. Before they start a big advertising campaign, they
> conduct a hypothesis test. Their marketing people survey 150 households with the result that 43 of the households have
> three cell phones.
>
> a. The value that helps determine the p-value is p′. Calculate p′.
>
> b. What is a success for this problem?
>
> c. What is the level of significance?
>
> d. Draw the graph for this problem. Draw the horizontal axis. Label and shade appropriately. Calculate the p-value.
>
> e. Make a decision. _____________(Reject/Do not reject) H0 because____________.
>
> Solution
> Set up the Hypothesis Test:
>
> H0: p = 0.30 Ha: p ≠ 0.30
>
> Determine the distribution needed:
>
> The random variable is P′ = proportion of households that have three cell phones.
>
> The distribution for the hypothesis test is
>
> a. p′ =
>  where x is the number of successes and n is the total number in the sample.
>
> x = 43, n = 150
>
> p′ =
>
> b. A success is having three cell phones in a household.
>
> c. The level of significance is the preset α. Since α is not given, assume that α = 0.05.
>
> d. p-value = 0.7216
>
> e. Assuming that α = 0.05, α < p-value.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-003-pool-008

**Chunk:** `openstax_principles_ds:4.2:chunk-024`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> As a reminder, the general hypothesis testing method introduced in the previous section includes the following
> steps:
>
> 1. Set up a null and an alternative hypothesis based on the claim. 2. Collect relevant sample data to investigate the claim. 3. Determine the correct distribution to be used to analyze the hypothesis test (e.g., normal distribution or t-
> distribution). 4. Analyze the sample data to determine if the sample data is consistent with the null hypothesis. This will
> involve statistical calculations involving a test statistic and a p-value, which are discussed next. 5. If the sample data is inconsistent with the null hypothesis, then the decision is to “reject the null
> hypothesis.” If the sample data is consistent with the null hypothesis, then the decision is to “fail to reject
> the null hypothesis.”
>
> As discussed for one-sample hypothesis testing, when writing the null and alternative hypotheses, start off by
> translating the claim into a mathematical statement involving the unknown population parameters. The claim
> could correspond to either the null or the alternative hypothesis. Then write the complement of this statement
> in order to write the other hypothesis. The difference now as compared to the previous section is that the
> hypotheses will be comparing two means or two proportions instead of just one mean or one proportion.
>
> When translating claims about a population mean, use the symbols
>  and
>  as part of the null and
> alternative hypotheses to represent the two unknown population means. When translating claims about a
> population proportions, use the symbols p1 and p2 as part of the null and alternative hypotheses to represent
> the two unknown population proportions. Refer to Table 4.9 and Table 4.10 for the various setups to construct
>
> the null and alternative hypotheses for two-sample hypothesis testing.
>
> Setup A
> Setup B
> Setup C

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-003-pool-009

**Chunk:** `openstax_principles_ds:4.2:chunk-021`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> Using Python to Conduct Hypothesis Tests
>
> Python provides several functions to assist with hypothesis testing, as the ztest() can be used for hypothesis
>
> testing for the mean when population standard deviation is known and another Python function called
> ttest_1samp() can be used for hypothesis testing for the mean when population standard deviation is
>
> unknown. See the example:
>
> EXAMPLE 4.16
>
> Problem
>
> A medical researcher wants to test a claim that the average oxygen level for females is greater than 75 mm
> Hg. In order to test the claim, a sample of 15 female patients is selected and the following oxygen levels are
> recorded:
>
> 76, 75, 74, 81, 76, 77, 71, 74, 73, 79
>
> Use the ttest_1samp() function in Python to conduct a hypothesis test to test the claim. Assume a level of
>
> significance of 0.05.
>
> Solution
>
> The first step in the hypothesis testing procedure is to write the null and alternative hypotheses based on
> the claim. Notice that the claim involves the phrase “greater than 75 mm Hg,” where “greater than” will
> translate to a greater than symbol. A greater than symbol must be used in the alternative hypothesis. The
> complement of a “greater than” symbol is a “less than or equals” symbol, which will be used in the null
> hypothesis. The claim refers to the population mean oxygen level, so the symbol  will be used. The claim
> corresponds to the alternative hypothesis. Notice that this setup will correspond to Setup B from Table 4.6. Thus the setup of the null and alternative hypotheses will be as follows:
>
> Since the population standard deviation is unknown in this example, the t-distribution will be used to
> conduct the hypothesis test.
>
> To use the ttest_1samp() function in Python, the syntax is as follows:
>
> Ttest_1samp(data_array, null_hypothesis_mean)

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-003-pool-010

**Chunk:** `openstax_principles_ds:4.2:chunk-035`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> Here is a step-by-step example to illustrate this hypothesis testing process.
>
> EXAMPLE 4.21
>
> Problem
>
> A drug is under investigation to address lung cancer. As part of a clinical trial, 250 people took the drug and
> 230 people took a placebo (a substance with no therapeutic effect ). From the results of the study, 211
> people taking the drug were cancer free, and 172 taking the placebo were cancer free. At a level of
> significance of 0.01, can you support the claim by the pharmaceutical company that the proportion of
> subjects who are cancer free after taking the actual cancer drug is greater than the proportion for those
> who took the placebo?
>
> Solution
>
> The first step in the hypothesis testing procedure is to write the null and alternative hypotheses based on
> the claim. Notice that the claim mentions “proportion of subjects who are cancer free after taking the actual
> cancer drug is greater than the proportion for those who took the placebo,” where “greater than” will
> translate to a greater than symbol. A greater than symbol must be used in the alternative hypothesis. The
> complement of a “greater than” symbol is a “less than or equals” symbol, which will be used in the null
> hypothesis. Let
>  represent the proportion of people who take the medication and are cancer free, and let
>  represent the proportion of people who take the placebo and are cancer free. The null hypothesis
> assumes there is no difference in the two proportions such that
>  is equal to
>  (which can also be
> considered as
> ). This setup will correspond to Setup E from Table 4.10. The claim corresponds to
> the alternative hypothesis. Thus the setup of the null and alternative hypotheses will be as follows:
>
> First, check that the requirements for this hypothesis test are met.
>
> Calculate the weighted estimate ( ) for
>  and
> , as follows:
>
> Check that the following four quantities are all at least 5:
> ,
> ,
> ,
> .

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-003-pool-011

**Chunk:** `openstax_principles_ds:4.2:chunk-014`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> The resulting output will look like this:
>
> 0.0324
>
> The final step in the hypothesis testing procedure is to come to a final decision regarding the null
>
> hypothesis. This is accomplished by comparing the p-value with the level of significance. In this example,
> the p-value is 0.032 and the level of significance is 0.05: since the p-value  level of significance, then the
> decision is to “reject the null hypothesis.”
>
> Conclusion: The decision is to reject the null hypothesis; the claim corresponds to the null hypothesis. This
> scenario corresponds to Row 1 in Table 4.8, which means “there is enough evidence to reject the claim” that
> college students spend at least 15 hours per week on social media.
>
> Testing Claims for the Mean When the Population Standard Deviation Is Unknown
>
> In this section, we discuss one sample hypothesis testing for the mean when the population standard
> deviation is unknown. This is a more common application of hypothesis testing for the mean in that the
> population standard deviation is typically unknown; however, the sample standard deviation can be calculated
> based on the sample data.
>
> Here are the requirements to use this procedure:
>
> a. A random sample is selected from the population.
> b. The sample size is at least 30, or the underlying population is known to follow a normal distribution.
>
> c. The population standard deviation ( ) is unknown; the sample standard deviation ( ) is known.
>
> When these requirements are met, the t-distribution is used as the basis for conducting the hypothesis test.
>
> For this procedure, the test statistic will be a t-score and the standardized test statistic is calculated as follows:
>
> Where:
>
> is the sample mean.
>  is the hypothesized value of the population mean, which comes from the null hypothesis.
>  is the sample standard deviation.
>
> is the sample size.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-003-pool-012

**Chunk:** `openstax_principles_ds:4.2:chunk-023`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> This is accomplished by comparing the p-value with the level of significance. In this example,
> the p-value is 0.266 and the level of significance is 0.05: since the p-value  level of significance, the
> decision is to “fail to reject the null hypothesis.”
>
> Conclusion: The decision is to fail to reject the null hypothesis; the claim corresponds to the alternative
> hypothesis. This scenario corresponds to Row 4 in Table 4.8, which means “there is not enough evidence to
> support the claim” that the average oxygen level for female patients is greater than 75 mm Hg.
>
> Hypothesis Testing for Two Samples
>
> In the previous section, we examined methods to conduct hypothesis testing for one sample. Researchers and
> data scientists are also often interested in conducting hypothesis tests for two samples. A researcher might
> want to compare two means or two proportions to determine if two groups are significantly different from one
> another. For example, a medical researcher might be interested in comparing the mean blood pressure
> between two groups of individuals: one group that is taking a blood pressure–lowering medication and
> another group that is taking a placebo. A government researcher might be interested in comparing the
> proportion of smokers for male versus female adults.
>
> The same general hypothesis testing procedure will be used for two samples, but the setup of the null and
> alternative hypotheses will be structured to reflect the comparison of two means or two proportions.
>
> As a reminder, the general hypothesis testing method introduced in the previous section includes the following
> steps:
>
> 1. Set up a null and an alternative hypothesis based on the claim. 2. Collect relevant sample data to investigate the claim. 3. Determine the correct distribution to be used to analyze the hypothesis test (e.g., normal distribution or t-
> distribution). 4.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-003-pool-013

**Chunk:** `openstax_principles_ds:4.2:chunk-001`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> # Calculate confidence interval using t.interval function
> t.interval(confidence_level, degrees_of_freedom, sample_mean, standard_error)
>
> The resulting output will look like this:
>
> (14.050684356083625, 17.549315643916376)
>
> 4.2 Hypothesis Testing
>
> Learning Outcomes
> By the end of this section, you should be able to:
>
> • 4.2.1 Apply hypothesis testing methods to test statistical claims involving one sample.
> • 4.2.2 Use Python to assist with hypothesis testing calculations.
> • 4.2.3 Conduct hypothesis tests to compare two means, two proportions, and matched pairs data.
>
> Constructing confidence intervals is one method used to estimate population parameters. Another important
> statistical method to test claims regarding population parameters is called hypothesis testing.
>
> Hypothesis testing is an important tool for data scientists in that it is used to draw conclusions using sample
> data, and it is also used to quantify uncertainty associated with these conclusions.
>
> As an example to illustrate the use of hypothesis testing in a data science applications, consider an online
> retailer seeking to increase revenue though a text messaging ad campaign. The retailer is interested in
> examining the hypothesis that a text messaging ad campaign leads to a corresponding increase in revenue. To
> test out the hypothesis, the retailer sends out targeted text messages to certain customers but does not send
> the text messages to another group of customers. The retailer then collects data for purchases made by
> customers who received the text message ads versus customers who did not receive the ads. Using hypothesis
> testing methods, the online retailer can come to a conclusion regarding the marketing campaign to transmit
> ads via text messaging. Hypothesis testing involves setting up a null hypothesis and alternative hypotheses
> based on a claim to be tested and then collecting sample data.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-003-pool-014

**Chunk:** `openstax_principles_ds:4.2:chunk-010`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> The smaller the p-value, the more the sample data deviates from the null hypothesis, and this is more evidence
> to indicate that the null hypothesis should be rejected.
>
> The final step in the hypothesis testing procedure is to come to a final decision regarding the null hypothesis. This is accomplished by comparing the p-value with the level of significance and applying the following rule:
>
> • If the p-value  level of significance, then the decision is to “reject the null hypothesis.”
> • If the p-value  level of significance, then the decision is to “fail to reject the null hypothesis.”
>
> Recall that these are the only two possible decisions that a researcher can deduce when conducting a
> hypothesis test.
>
> Often, we would like to translate these decisions into a conclusion that is easier to interpret for someone
> without a statistical background. For example, a decision to “fail to reject the null hypothesis” might be difficult
> to interpret for those not familiar with the terminology of hypothesis testing. These decisions can be
> translated into concluding statements such as those shown in Table 4.8.
>
> Is the claim in the null or
>
> Select the decision
> from the hypothesis
>
> the alternative
>
> Then, use this
> concluding statement:
>
> test:
>
> hypothesis?
>
> Row 1
> Reject the null
> hypothesis
>
> Claim is the null
> hypothesis
>
> There is enough
> evidence to reject the
> claim.
>
> Row 2
> Reject the null
> hypothesis
>
> Claim is the alternative
> hypothesis
>
> There is enough
> evidence to support the
> claim.
>
> Row 3
> Fail to reject the null
> hypothesis
>
> Claim is the null
> hypothesis
>
> There is not enough
> evidence to reject the
> claim.
>
> Row 4
> Fail to reject the null
> hypothesis
>
> Claim is the alternative
> hypothesis
>
> There is not enough
> evidence to support the
> claim.
>
> Table 4.8 How to Establish a Conclusion from a Hypothesis Test

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-003-pool-015

**Chunk:** `openstax_intro_stats_2e:9.5:chunk-022`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.5: Additional Information and Full Hypothesis Test Examples
>
> 1. We need to conduct a hypothesis test on the claimed cancer rate. Our hypotheses will be
>
> a. H0: p ≤ 0.00034
> b. Ha: p > 0.00034
>
> If we commit a Type I error, we are essentially accepting a false claim. Since the claim describes cancer-causing
> environments, we want to minimize the chances of incorrectly identifying causes of cancer.
>
> 2. We will be testing a sample proportion with x = 172 and n = 420,019. The sample is sufficiently large because we
> have np = 420,019(0.00034) = 142.8, nq = 420,019(0.99966) = 419,876.2, two independent outcomes, and a fixed
> probability of success p = 0.00034. Thus we will be able to generalize our results to the population. 3. The associated TI results are
>
> Figure 9.13
>
> Figure 9.14
>
> 4. Since the p-value = 0.0073 is greater than our alpha value = 0.005, we cannot reject the null. Therefore, we conclude
> that there is not enough evidence to support the claim of higher brain cancer rates for the cell phone users.
>
> TRY IT 9.21
>
> In a study of 390,000 moisturizer users, 138 of the subjects developed skin diseases. Test the claim that moisturizer
> users developed skin diseases at a greater rate than that for non-moisturizer users (the rate of skin diseases for non-
> moisturizer users is 0.041%). Since this is a critical issue, use a 0.005 significance level. Explain why the significance
> level should be so low in terms of a Type I error.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-003-pool-016

**Chunk:** `openstax_intro_stats_2e:9.5:chunk-021`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.5: Additional Information and Full Hypothesis Test Examples
>
> To calculate the p-value, note that this is a right-tailed test. Then, find the area under the t-distribution to the right
> of the test statistic 2.014 (using 10 degrees of freedom). This area in the right tail is 0.036, and thus the p-value =
> 0.036.
>
> 4. State the Conclusions: Since the p-value (p = 0.036) is less than our alpha value, we will reject the null hypothesis. It
> is reasonable to state that the data supports the claim that the average conductivity level is greater than one.
>
> TRY IT 9.20
>
> The boiling point of a specific liquid is measured for 15 samples, and the boiling points are obtained as follows:
>
> 205; 206; 206; 202; 199; 194; 197; 198; 198; 201; 201; 202; 207; 211; 205
>
> Is there convincing evidence that the average boiling point is greater than 200? Use a significance level of 0.1. Assume
> the population is normal.
>
> EXAMPLE 9.21
>
> Problem
> In a study of 420,019 cell phone users, 172 of the subjects developed brain cancer. Test the claim that cell phone users
> developed brain cancer at a greater rate than that for non-cell phone users (the rate of brain cancer for non-cell phone
> users is 0.0340%). Since this is a critical issue, use a 0.005 significance level. Explain why the significance level should be
> so low in terms of a Type I error.
>
> Solution
> We will follow the four-step process.
>
> 1. We need to conduct a hypothesis test on the claimed cancer rate. Our hypotheses will be
>
> a. H0: p ≤ 0.00034
> b. Ha: p > 0.00034
>
> If we commit a Type I error, we are essentially accepting a false claim. Since the claim describes cancer-causing
> environments, we want to minimize the chances of incorrectly identifying causes of cancer.
>
> 2.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-003-pool-017

**Chunk:** `openstax_principles_ds:4.2:chunk-005`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> Notice that for each setup, the null and alternative hypotheses
> are complements of one another. Note that the value of “ ” will be replaced by some numerical constant taken
> from the stated claim.
>
> Setup A
> Setup B
> Setup C
>
> Table 4.6 Possible Setups for the Null and
> Alternative Hypotheses for a Population Mean (One
> Sample)
>
> Table 4.7 provides the three possible setups for the null and alternative hypotheses when conducting a one-
> sample hypothesis test for a population proportion. Note that the value of “ ” will be replaced by some
> numerical constant taken from the stated claim.
>
> Setup D
> Setup E
> Setup F
>
> Table 4.7 Possible Setups for the Null and
> Alternative Hypotheses for a Population Proportion
> (One Sample)
>
> Follow these steps to determine which of these setups to use for a given hypothesis test:
>
> 1. Determine if the hypothesis test involves a claim for a population mean or population proportion. If the
> hypothesis test involves a population mean, use either Setup A, B, or C. 2. If the hypothesis test involves a population proportion, use either Setup D, E, or F. 3. Translate a phrase from the claim into a mathematical symbol and then match this mathematical symbol
> with one of the setups in Table 4.6 and Table 4.7.
>
> For example, if a claim for a hypothesis test for a mean references the phrase “at least,” note that the phrase
> “at least” corresponds to a greater than or equals symbol. A greater than or equals symbol appears in Setup C
> in Table 4.6, so that would be the correct setup to use.
>
> If a claim for a hypothesis test for a proportion references the phrase “different than,” note that the phrase
> “different than” corresponds to a not equals symbol.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-004

**Pregunta:** Why is the median a suitable measure of center when a dataset contains extreme outliers?

**Respondibilidad de referencia:** answerable

### q-v1-004-pool-001

**Chunk:** `openstax_principles_ds:3.1:chunk-007`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> For the mean, add the 15 data values, and the sum is 10,777,090. Divide this sum by the number of
> data values, which is 15. The result is:
>
> 2. For the trimmed mean, first order the data from smallest to largest. The sorted dataset is:
>
> 385000, 397900, 403890, 452600, 488300, 499000, 507400, 525000, 573200, 599000, 612300, 623400,
> 675000, 1689300, 2345800
>
> Twenty percent of 15 data values is 3, and this indicates that 3 data values are to be deleted from each
> of the lower end and upper end of the dataset. The resulting 9 undeleted data values are:
>
> 452600, 488300, 499000, 507400, 525000, 573200, 599000, 612300, 623400
>
> Then find the mean for the remaining data values. The sum of these 9 data values is 4,880,200. Divide
> this sum by the number of data values (9). The result is:
>
> Notice how the mean calculated in Part (a) is significantly larger as compared to the trimmed mean
> calculated in Part (b). The reason is the presence of several large outlier home prices. Once these outlier
> data values are removed by the trimmed mean calculation, the resulting trimmed mean is more
> representative of the typical home price in this neighborhood as compared to the mean.
>
> Median
>
> The median provides another measure of central tendency for a dataset. The median is generally a better
> measure of the central tendency when there are outliers (extreme values) in the dataset. Since the median
> focuses on the middle value of the ordered dataset, the median is preferred when outliers are present because
> the median is not affected by the numerical values of the outliers.
>
> To determine the median of a dataset, first order the data from smallest to largest, and then find the middle
> value in the ordered dataset.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-004-pool-002

**Chunk:** `openstax_principles_ds:3.1:chunk-011`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> Note: A formal method for identifying outliers is presented
> in Measures of Position when measures of position are discussed. The following example illustrates the point
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
>
> Using Python for Measures of Center
>
> We learned in What Are Data and Data Science? how the DataFrame.describe() method is used to

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-004-pool-003

**Chunk:** `openstax_principles_ds:3.1:chunk-010`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> For example, assume that the
> weekly closing stock price for a technology stock, in dollars, is recorded for 20 consecutive weeks as follows:
>
> 50, 53, 59, 59, 63, 63, 72, 72, 72, 72, 72, 76, 78, 81, 83, 84, 84, 84, 90, 93
>
> To find the mode, determine the most frequent score, which is 72, which occurs five times. Thus, the mode of
> this dataset is 72.
>
> The mode can also be applied to non-numeric (qualitative) data, whereas the mean and the median can only
> be applied for numeric (quantitative) data. For example, a restaurant manager might want to determine the
> mode for responses to customer surveys on the quality of the service of a restaurant, as shown in Table 3.1.
>
> Customer
>
> Service
>
> Number of
> Respondents
>
> Rating
>
> Excellent
> 267
>
> Very Good
> 410
>
> Good
> 392
>
> Fair
> 107
>
> Poor
> 18
>
> Table 3.1 Customer Survey Results for
> Customer Survey Rating
>
> Based on the survey responses, the mode is the Customer Service Rating of “Very Good,” since this is the data
> value with the greatest frequency.
>
> Influence of Outliers on Measures of Center
>
> As mentioned earlier, when outliers are present in a dataset, the mean may not represent the center of the
> dataset, and the median will provide a better measure of center. The reason is that the median focuses on the
> middle value of the ordered dataset. Thus, any outliers at the lower end of the dataset or any outliers at the
> upper end of the dataset will not affect the median. Note: A formal method for identifying outliers is presented
> in Measures of Position when measures of position are discussed. The following example illustrates the point
> that the median is a better measure of central tendency when potential outliers are present.
>
> EXAMPLE 3.5
>
> Problem

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-004-pool-005

**Chunk:** `openstax_principles_ds:3.1:chunk-002`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> Probability theory helps
> us deal with quantifying uncertainty, which is always inherent in real-world data. We will see that in real-world
> datasets we often have to deal with noise and randomness that will be analyzed using statistical analyses.
>
> Probability analysis provides the tools to model, understand, and quantify uncertainties, allowing data
> scientists to make informed decisions from data. Probability theory also forms the basis for different types of
> analyses, such as confidence intervals and hypothesis testing, which will be discussed further in Inferential
> Statistics and Regression Analysis. Such methods rely on probability models to make predictions and detect
> patterns. In addition, machine learning (discussed in Time Series and Forecasting) uses probabilistic models to
> help represent uncertainty and make predictions based on the collected data. Probability analysis helps data
> scientists to select data models, interpret the results, and assess the reliability of these conclusions. For a more
> detailed review of statistical concepts, please refer to Introductory Statistics 2e (https://openstax.org/books/
> introductory-statistics-2e/pages/1-introduction).
>
> 3.1 Measures of Center
>
> Learning Outcomes
> By the end of this section, you should be able to:
>
> • 3.1.1 Define and calculate mean, trimmed mean, median, and mode for a dataset.
> • 3.1.2 Determine the effect of outliers on the mean and the median.
> • 3.1.3 Use Python to calculate measures of center for a dataset.
>
> Measures of center are statistical measurements that provide a central, or typical, representation of a dataset. These measures can help indicate where the bulk of the data is concentrated and are often called the data’s
> central tendency. The most widely used measures of the center of a dataset are the mean (average), the
> median, and the mode.
>
> Mean and Trimmed Mean
>
> The mean, or average, (sometimes referred to as the arithmetic mean) is the most commonly used measure of
> the center of a dataset.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-004-pool-006

**Chunk:** `openstax_principles_ds:3.1:chunk-003`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> The most widely used measures of the center of a dataset are the mean (average), the
> median, and the mode.
>
> Mean and Trimmed Mean
>
> The mean, or average, (sometimes referred to as the arithmetic mean) is the most commonly used measure of
> the center of a dataset. Sometimes the mean can be skewed by the presence of outliers, or data values that
> are significantly different as compared to the remainder of the dataset. In these instances, the trimmed mean
> is often used to provide a more representative measure of the center of the dataset, as we will discuss in the
> following section.
>
> Mean
>
> To calculate the mean, add the values of all the items in a dataset and divide by the number of items. For
> example, if the scores on your last three exams were 87, 92, and 73, then the mean score would be
>
> . If you had a large number of data values, you would proceed in the same way. For example, to
>
> calculate the mean value of 50 exam scores, add the 50 scores together and divide by 50. If the 50 scores add
>
> up to 4,050, for example, the mean score is
> , or 81.
>
> In data science applications, you will encounter two types of datasets: sample data and population data. Population data represents all the outcomes or measurements that are of interest. Sample data represents
> outcomes or measurements collected from a subset, or part, of the population of interest. Of course in many
> applications, collecting data from an entire population is not practical or feasible, and so we often rely on
> sample data.
>
> The notation  is used to indicate the sample mean, where the mean is calculated based on data taken from a
> sample.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-004-pool-007

**Chunk:** `openstax_principles_ds:3.3:chunk-005`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.3: Measures of Position
>
> Quartiles and the IQR can be used to flag possible outliers in a dataset. For example, if most employees at a
> company earn about $50,000 and the CEO of the company earns $2.5 million, then we consider the CEO’s
> salary to be an outlier data value because this salary is significantly different from all the other salaries in the
> dataset. An outlier data value can also be a value much lower than the other data values in a dataset, so if one
> employee only makes $15,000, then this employee’s low salary might also be considered an outlier.
>
> To detect outliers, you can use the quartiles and the IQR to calculate a lower and an upper bound for outliers. Then any data values below the lower bound or above the upper bound will be flagged as outliers. These data
> values should be further investigated to determine the nature of the outlier condition and whether the data
> values are valid or not.
>
> To calculate the lower and upper bounds for outliers, use the following formulas:
>
> These formulas typically use 1.5 as a cutoff value to identify outliers in a dataset.
>
> EXAMPLE 3.12
>
> Problem
>
> Calculate the IQR for the following 13 home prices and determine if any of the home prices values are
> potential outliers. Data values are in US dollars.
>
> 389950, 230500, 158000, 479000, 639000, 114950, 5500000, 387000, 659000, 529000, 575000, 488800,
> 1095000
>
> Solution
>
> Order the data from smallest to largest.
>
> 114950, 158000, 230500, 387000, 389950, 479000, 488800, 529000, 575000, 639000, 659000, 1095000,
> 5500000
>
> First, determine the median of the dataset. There are 13 data values, so the median is the middle data
> value, which is 488,800.
>
> Next, calculate the
>  and
> .
>
> For the first quartile, look at the data values below the median.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-004-pool-008

**Chunk:** `openstax_principles_ds:3.2:chunk-002`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.2: Measures of Variation
>
> Providing some measure of the spread, or variation, in a dataset is crucial to a comprehensive summary of the
> dataset. Two datasets may have the same mean but can exhibit very different spread, and so a measure of
> dispersion for a dataset is very important. While measures of central tendency (like mean, median, and mode)
> describe the center or average value of a distribution, measures of dispersion give insights into how much
> individual data points deviate from this central value.
>
> The following two datasets are the exam scores for a group of three students in a biology course and in a
> statistics course.
>
> Dataset A: Exam scores for students in a biology course: 40, 70, 100
> Dataset B: Exam scores for students in a statistics course: 69, 70, 71
>
> Notice that the mean score for both Dataset A and Dataset B is 70.
>
> However, the datasets are significantly different from one another:
>
> Dataset A has larger variability where one student scored 30 points below the mean and another student
> scored 30 points above the mean. Dataset B has smaller variability where the exam scores are much more tightly clustered around the mean of
> 70.
>
> This example illustrates that publishing the mean of a dataset is often inadequate to fully communicate the
> characteristics of the dataset. Instead, data scientists will typically include a measure of variation as well.
>
> The three primary measures of variability are range, variance, and standard deviation, and these are described
> next.
>
> Range
>
> Range is a measure of dispersion for a dataset that is calculated by subtracting the minimum from the
> maximum of the dataset:
>
> Range is a straightforward calculation but makes use of only two of the data values in a dataset. The range can
> also be affected by outliers.
>
> EXAMPLE 3.6
>
> Problem

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-004-pool-009

**Chunk:** `openstax_principles_ds:3.3:chunk-006`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.3: Measures of Position
>
> Order the data from smallest to largest.
>
> 114950, 158000, 230500, 387000, 389950, 479000, 488800, 529000, 575000, 639000, 659000, 1095000,
> 5500000
>
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
> 1,159,375. Therefore, the home price of $5,500,000 is a potential outlier. This is important because the
> presence of outliers could potentially indicate data errors or some other anomalies in the dataset that
> should be investigated. For example, there may have been a data entry error and a home price of $550,000
> was erroneously entered as $5,500,000.
>
> -scores
>
> The -score is a measure of the position of an entry in a dataset that makes use of the mean and standard
> deviation of the data. It represents the number of standard deviations by which a data value differs from the
> mean.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-004-pool-010

**Chunk:** `openstax_principles_ds:3.1:chunk-005`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> EXAMPLE 3.1
>
> Problem
>
> During a clinical trial, a sample is taken of 10 patients and pulse rates are measured in beats per minute:
>
> 68, 92, 76, 51, 65, 83, 94, 72, 88, 59
>
> Calculate the mean pulse rate for this sample.
>
> Solution
>
> Add the 10 data values, and the sum is 748. Divide this sum by the number of data values, which is 10. The
> result is:
>
> EXAMPLE 3.2
>
> Problem
>
> A college professor records the ages of 25 students in a data science class as shown:
>
> Student Age
> Number of
>
> Students
> (Frequency)
>
> 19
> 3
>
> 20
> 4
>
> 21
> 8
>
> 22
> 6
>
> 23
> 2
>
> 27
> 1
>
> 31
> 1
>
> Total
> 25
>
> Calculate the mean age for this sample of students.
>
> Solution
>
> Substitute the values from the table in the following formula:
>
> Trimmed Mean
>
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

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-004-pool-011

**Chunk:** `openstax_principles_ds:3.1:chunk-006`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> To calculate the trimmed mean for a dataset, first sort the data in ascending order (from smallest to largest). Then decide on a certain percentage of data values to be deleted from the lower and upper ends of the
> dataset. This might represent the extent of outliers in the dataset; trimmed mean percentages of 10% and 20%
> are common. Then delete the specified percentage of data values from both the lower end and upper end of
> the dataset. Then find the mean for the remaining undeleted data values.
>
> As an example, to calculate a 10% trimmed mean, first sort the data values from smallest to largest. Then
> delete the lower 10% of the data values and delete the upper 10% of the data values. Then calculate the mean
> for the resulting dataset. Any outliers would tend to be deleted as part of the trimmed mean calculation, and
> thus the trimmed mean would then be a more representative measure of the center of the data for datasets
> containing outliers.
>
> EXAMPLE 3.3
>
> Problem
>
> A real estate agent collects data on a sample of recently sold homes in a certain neighborhood, and the
> data are shown in the following dataset:
>
> 397900, 452600, 507400, 488300, 623400, 573200, 1689300, 403890, 612300, 599000, 2345800, 499000,
> 525000, 675000, 385000
>
> 1. Calculate the mean of the dataset. 2. Calculate a 20% trimmed mean rate for the dataset.
>
> Solution
>
> 1. For the mean, add the 15 data values, and the sum is 10,777,090. Divide this sum by the number of
> data values, which is 15. The result is:
>
> 2. For the trimmed mean, first order the data from smallest to largest. The sorted dataset is:
>
> 385000, 397900, 403890, 452600, 488300, 499000, 507400, 525000, 573200, 599000, 612300, 623400,
> 675000, 1689300, 2345800

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-004-pool-012

**Chunk:** `openstax_principles_ds:3.1:chunk-009`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> 51, 59, 65, 68, 72, 76, 83, 88, 92, 94
>
> Since there is an even number of data values, add the two middle values together and divide by 2. The two middle values are 72 and 76.
>
> You can also quickly find the sample median of a dataset as follows.
>
> Let  represent the number of data values in the sample.
>
> • If  is odd, then the median is the data value in position
> .
>
> • If  is even, the median is the mean of the observations in position
>  and position
> .
>
> For example, let’s say a dataset has 25 data values. Since  is odd, to identify the position of the median,
>
> calculate
> , which is
> , or 13. This indicates that the median is located in the 13th data position.
>
> As another example, let’s say a dataset has 100 data values. Since  is even, to identify the position of the
>
> median, calculate
> , which is
> , which is 50, and also calculate
> , which is
> , which is 51. This
>
> indicates that the median is calculated as the mean of the 50th and 51st data values.
>
> Mode
>
> Another measure of center is the mode. The mode is the data value that occurs with the greatest frequency. If
> there are no repeating data values in a dataset, then there is no mode. If two data values occur with same
> greatest frequency, then there are two modes, and we say the data is bimodal. For example, assume that the
> weekly closing stock price for a technology stock, in dollars, is recorded for 20 consecutive weeks as follows:
>
> 50, 53, 59, 59, 63, 63, 72, 72, 72, 72, 72, 76, 78, 81, 83, 84, 84, 84, 90, 93

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-005

**Pregunta:** What two aspects of the relationship between an independent and a dependent variable are summarized by the correlation coefficient?

**Respondibilidad de referencia:** answerable

### q-v1-005-pool-001

**Chunk:** `openstax_principles_ds:4.3:chunk-002`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> • 4.3.1 Create scatterplots and calculate and interpret correlation coefficients.
> • 4.3.2 Perform linear regression and determine the best-fit linear equation.
> • 4.3.3 Use Python to calculate correlation coefficients and determine equations of linear regression
> models.
>
> We briefly introduced correlation analysis at the beginning of this chapter, but now we want to dig in a little
> deeper. Data scientists are often interested in knowing if there are relationships, or a correlation, between two
> numeric quantities. For example, a medical researcher might be interested in investigating if there is a
> relationship between age and blood pressure. A college professor might be interested to know if there is a
> relationship between time spent on social media by students and corresponding academic grades.
>
> Correlation analysis allows for the determination of a statistical relationship between two numeric quantities,
> or variables—an independent variable and a dependent variable. The independent variable is the variable
> that you can change or control, while the dependent variable is what you measure or observe to see how it
>
> responds to those changes. Regression analysis takes this a step further by quantifying the relationship
> between the two variables, and it can be used to predict one quantity based on a second quantity, assuming
> there is a significant correlation between the two quantities. For example, the value of a car can be predicted
> based on the age of the car.
>
> Earlier we noted many business-related applications where correlation and regression analysis are used. For
> instance, regression analysis can be used to establish a mathematical equation that relates a dependent
> variable (such as sales) to an independent variable (such as advertising expenditure). But it has many
> applications apart from business as well. An automotive engineer is interested in the correlation between
> outside temperature and battery life for an electric vehicle, for instance.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-005-pool-002

**Chunk:** `openstax_principles_ds:4.3:chunk-005`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> Table 4.14 Nike Stock Price ($) and Value of S&P 500 over a
> One-Year Time Period
> (source: Yahoo! Finance)
>
> To assess linear correlation, examine the graphical trend of the data points on the scatterplot to determine if
> a straight-line pattern exists (see Figure 4.5). If a linear pattern exists, the correlation may indicate either a
> positive or a negative correlation. A positive correlation indicates that as the independent variable increases,
> the dependent variable tends to increase as well, or as the independent variable decreases, the dependent
> variable tends to decrease (the two quantities move in the same direction). A negative correlation indicates
> that as the independent variable increases, the dependent variable decreases, or as the independent variable
> decreases, the dependent variable increases (the two quantities move in opposite directions). If there is no
> relationship or association between the two quantities, where one quantity changing does not affect the other
> quantity, we conclude that there is no correlation between the two variables.
>
> Figure 4.5 Scatterplot of Nike Stock Price ($) and Value of S&P 500
> (source: Yahoo! Finance)
>
> From the scatterplot in the Nike stock versus S&P 500 example, we note that the trend reflects a positive
> correlation in that as the value of the S&P 500 increases, the price of Nike stock tends to increase as well.
>
> When inspecting a scatterplot, it may be difficult to assess a correlation based on a visual inspection of the
> graph alone. A more precise assessment of the correlation between the two quantities can be obtained by
> calculating the numeric correlation coefficient (referred to using the symbol ).
>
> The correlation coefficient is a measure of the strength and direction of the correlation between the
> independent variable  and the dependent variable .

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-005-pool-003

**Chunk:** `openstax_principles_ds:4.3:chunk-003`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> For
> instance, regression analysis can be used to establish a mathematical equation that relates a dependent
> variable (such as sales) to an independent variable (such as advertising expenditure). But it has many
> applications apart from business as well. An automotive engineer is interested in the correlation between
> outside temperature and battery life for an electric vehicle, for instance.
>
> Our discussion here will focus on linear regression—analyzing the relationship between one dependent
> variable and one independent variable, where the relationship can be modeled using a linear equation.
>
> Scatterplots and Correlation
>
> In correlation analysis, we study the relationship between bivariate data, which is data collected on two
> variables where the data values are paired with one another. Correlation measures the association between
> two numeric variables. We may be interested in knowing if there is a correlation between bond prices and
> interest rates or between the age of a car and the value of the car. To investigate the correlation between two
> numeric quantities, the first step is to collect
>  data for the two numeric quantities of interest and then
> create a scatterplot that will graph the
>  ordered pairs. The independent, or explanatory, quantity is
> labeled the -variable, and the dependent, or response, quantity is labeled the -variable.
>
> For example, let’s say that a financial analyst wants to know if the price of Nike stock is correlated with the
> value of the S&P 500 (Standard & Poor’s 500 stock market index). To investigate this, monthly data can be
> collected for Nike stock prices and value of the S&P 500 for a period of time, and a scatterplot can be created
> and examined. A scatterplot, or scatter diagram, is a graphical display intended to show the relationship
> between two variables.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-005-pool-004

**Chunk:** `openstax_principles_ds:4.3:chunk-008`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> a. the strength of the correlation based on the value of
> b. the direction of the correlation based on the sign of
>
> The value of  gives us this information:
>
> • The value of  is always between
>  and
> :
> .
> • The size of the correlation  indicates the strength of the linear relationship between the two variables. Values of  close to
>  or to
>  indicate a stronger linear relationship.
> • If
> , there is no linear relationship between the two variables (no linear correlation).
> • If
> , there is perfect positive correlation. If
> , there is perfect negative correlation. In both of
> these cases, all the original data points lie on a straight line.
>
> The sign of  gives us this information:
>
> • A positive value of  means that when  increases,  tends to increase, and when  decreases,  tends to
> decrease (positive correlation).
> • A negative value of  means that when  increases,  tends to decrease, and when  decreases,  tends to
> increase (negative correlation).
>
> From the statistical results shown in the Python output, the correlation coefficient  is 0.923, which indicates
> that the relationship between Nike stock and the value of the S&P 500 over this time period represents a
> strong, positive correlation.
>
> Test a Correlation Coefficient for Significance
>
> The correlation coefficient, , tells us about the strength and direction of the linear relationship between  and
>
> . The sample data are used to compute , the correlation coefficient for the sample. If we had data for the
> entire population (that is, all measurements of interest), we could find the population correlation coefficient,
> which is labeled as the Greek letter  (pronounced “rho”). But because we have only sample data, we cannot
> calculate the population correlation coefficient. The sample correlation coefficient, , is our estimate of the
> unknown population correlation coefficient.
>
> •
> •

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-005-pool-005

**Chunk:** `openstax_principles_ds:4.3:chunk-012`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> correlation is deemed significant.
>
> Linear Regression
>
> A regression model is typically developed once the correlation coefficient has been calculated and a
> determination has been made that the correlation is significant. The regression model can then be used to
> predict one quantity (the dependent variable) based on the other (the independent variable). For example, a
> business may want to establish a correlation between the amount the company spent on advertising (the
> independent variable) versus its recorded sales (the dependent variable). If a strong enough correlation is
> established, then the business manager can predict sales based on the amount spent on advertising for a
> given period. In this discussion we will focus on linear regression, where a straight line is used to model the
> relationship between the two variables. Once a straight-line model is developed, this model can then be used
> to predict the value of the dependent variable for a specific value of the independent variable.
>
> Method of Least Squares and Residuals
>
> To create a linear model that best fits the
>  points on a scatterplot, researchers generally use the least
> squares method based on a mathematical algorithm designed to minimize the squared distances from the
>
> data points to the fitted line.
>
> Recall from algebra that the equation of a straight line is given by:
>
> where
>  is the slope of the line and  is the y-intercept of the line.
>
> The slope measures the steepness of the line, and the y-intercept is that point on the -axis where the graph
> crosses, or intercepts, the -axis.
>
> In linear regression analysis, the equation of the straight line is written in a slightly different way using the
> model
>
> In this format,  is the slope of the line, and  is the y-intercept of the line.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-005-pool-006

**Chunk:** `openstax_principles_ds:4.3:chunk-009`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> If we had data for the
> entire population (that is, all measurements of interest), we could find the population correlation coefficient,
> which is labeled as the Greek letter  (pronounced “rho”). But because we have only sample data, we cannot
> calculate the population correlation coefficient. The sample correlation coefficient, , is our estimate of the
> unknown population correlation coefficient.
>
> •
> •
>
> An important step in the correlation analysis is to determine if the correlation is significant. By this, we are
> asking if the correlation is strong enough to allow meaningful predictions for  based on values of . One
> method to test the significance of the correlation is to employ a hypothesis test. The hypothesis test lets us
> decide whether the value of the population correlation coefficient  is close to zero or significantly different
> from zero. We decide this based on the sample correlation coefficient  and the sample size n.
>
> If the test concludes that the correlation coefficient is significantly different from zero, we say that the
> correlation coefficient is significant.
>
> • Conclusion: There is sufficient evidence to conclude that there is a significant linear relationship between
> the two variables because the correlation coefficient is significantly different from zero.
> • What the conclusion means: There is a significant linear relationship between the two variables. If the test
> concludes that the correlation coefficient is not significantly different from zero (it is close to zero), we say
> that correlation coefficient is not significant.
>
> A hypothesis test can be performed to test if the correlation is significant. A hypothesis test is a statistical
> method that uses sample data to test a claim regarding the value of a population parameter. In this case, the
> hypothesis test will be used to test the claim that the population correlation coefficient  is equal to zero.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-005-pool-007

**Chunk:** `openstax_principles_ds:4.3:chunk-011`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> INTERPRETING THE SIGNIFICANCE OF THE SAMPLE CORRELATION COEFFICIENT
>
> • If  is significant and the scatterplot shows a linear trend, the line can be used to predict the value of
> for values of  that are within the domain of observed x-values.
>
> • If  is not significant OR if the scatterplot does not show a linear trend, the line should not be used for
> prediction.
> • If  is significant and the scatterplot shows a linear trend, the line may not be appropriate or reliable for
> prediction outside the domain of observed x-values in the data.
>
> EXAMPLE 4.22
>
> Problem
>
> Suppose that the chief financial officer (CFO) of a corporation is investigating the correlation between stock
> prices and unemployment rate over a period of 10 years and finds the correlation coefficient to be
> . There are 10
>  data points in the dataset. Should the CFO conclude that the correlation is significant for
> the relationship between stock prices and unemployment rate based on a level of significance of 0.05?
>
> Solution
>
> When using a level of significance of 0.05, if
> , then this implies that the correlation between the
>
> two variables demonstrates a linear relationship that is statistically significant at approximately the 0.05
>
> level of significance. In this example, we check if
>  is greater than or equal to
>  where
> . Since
>
> is approximately 0.632, this indicates that the r-value of
>  is greater than
> , and thus the
>
> correlation is deemed significant.
>
> Linear Regression
>
> A regression model is typically developed once the correlation coefficient has been calculated and a
> determination has been made that the correlation is significant. The regression model can then be used to
> predict one quantity (the dependent variable) based on the other (the independent variable).

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-005-pool-009

**Chunk:** `openstax_principles_ds:4.3:chunk-013`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> In linear regression analysis, the equation of the straight line is written in a slightly different way using the
> model
>
> In this format,  is the slope of the line, and  is the y-intercept of the line. The notation  is called -hat and is
> used to indicate a predicted value of the dependent variable  for a certain value of the independent variable
> .
>
> If a line extends uphill from left to right, the slope is a positive value (see Figure 4.6; if the line extends downhill
> from left to right, the slope is a negative value).
>
> Figure 4.6 Three examples of graphs of
> . (a) If
> , the line slopes upward to the right. (b) If
> , the line is horizontal.
> (c) If
> , the line slopes downward to the right.
>
> When generating the equation of a line in algebra using
> , two
>  points were required to
> generate the equation. However, in regression analysis, all the
>  points in the dataset will be utilized to
> develop the linear regression model.
>
> The first step in any regression analysis is to create the scatterplot. Then proceed to calculate the correlation
> coefficient  and check this value for significance. If we think that the points show a linear relationship, we
> would like to draw a line on the scatterplot. This line can be calculated through a process called linear
> regression. However, we only calculate a regression line if one of the variables helps to explain or predict the
> other variable. If  is the independent variable and  the dependent variable, then we can use a regression line
> to predict  for a given value of .
>
> As an example of a regression equation, assume that a correlation exists between the monthly amount spent
> on advertising and the monthly revenue for a Fortune 500 company.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-005-pool-010

**Chunk:** `openstax_principles_ds:4.3:chunk-021`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> #pearson r returns both value of r and corresponding p-value
> r, p = pearsonr(x, y)
>
> #print value of r, rounded to 3 decimal places
>
> print("Correlation coefficient: ", round(r, 3))
>
> The resulting output will look like this:
>
> Correlation coefficient: 0.981
> This value of
>  indicates a strong, positive correlation between
> advertising spend and revenue.
>
> c. When using a level of significance of 0.05, if
> , then this implies that the correlation between
>
> the two variables demonstrates a linear relationship that is statistically significant at approximately the
>
> 0.05 level of significance. In this example, we check if
>  is greater than or equal to
>  where
>
> . Since
>  is approximately 0.577, this indicates that the r-value of 0.981 is greater than
> ,
>
> and thus the correlation is deemed significant.
> d. The linear regression model will be of the form:
>
> To determine the slope and y-intercept of the regression model, the Python function linregress()
>
> can be used. This function takes the  and  data as inputs and provides the slope and intercept as well as other
> regression-related output.
>
> Here is the Python code to generate the slope and y-intercept of the best-fit line:
>
> PYTHON CODE
>
> # import libraries
> import numpy as np
> from scipy.stats  import linregress
>
> # define the x-data, which is amount spent on advertising
> x = [49, 145, 57, 153, 92, 83, 117, 142, 69, 106, 109, 121]
>
> # define the y-data, which is revenue
> y = [12210, 17590, 13215, 19200, 14600, 14100, 17100, 18400, 14100, 15500, 16300,
> 17020]
>
> #pearson r returns both value of r and corresponding p-value
> slope, intercept, r_value, p_value, std_err  = linregress(x, y)
>
> print ("slope  =", slope)
> print("intercept = ", intercept)
>
> The resulting output will look like this:
>
> slope = 61.79775818816664
> intercept = 9376.698881009072
>
> Based on this Python equation, the regression equation can be written as

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-005-pool-011

**Chunk:** `openstax_principles_ds:4.3:chunk-007`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> As mentioned, given the complexity of this calculation, software is typically used to calculate the correlation
> coefficient. There are several options for calculating the correlation coefficient in Python. The example shown
> uses the scipy.stats library in Python which includes the function pearsonr() for calculating the Pearson
>
> correlation coefficient ( ).
>
> We will create two numerical arrays in Python using the np.array() function and then use the pearsonr()
>
> function to calculate the Pearson correlation coefficient for the
>  data shown in Table 4.15.
>
> The following Python code provides the correlation coefficient for the Nike Stock Price dataset as 0.923.
>
> PYTHON CODE
>
> # import libraries
> import numpy as np
> from scipy.stats  import pearsonr
>  
> # establish x and y data, x-data is S&P500 value, y-data is Nike Stock Price
>
> SP500 = np.array([2912.43, 3044.31, 3100.29, 3271.12, 3500.31, 3363.00, 3269.96,
> 3621.63, 3756.07, 3714.24, 3811.15, 3943.34])
>
> Nike = np.array([87.18, 98.58, 98.05, 97.61, 111.89, 125.54, 120.08, 134.70,
> 141.47, 133.59, 134.78, 140.45])
>
> #pearson r returns both value of r and corresponding p-value
>
> r, p = pearsonr(SP500, Nike)
>
> #print value of r , rounded to 3 decimal places
>
> print("Correlation coefficient: ", round(r, 3))
>
> The resulting output will look like this:
>
> Correlation coefficient: 0.923
>
> Interpret a Correlation Coefficient
>
> Once the value of  is calculated, this measurement provides two indicators for the correlation:
>
> a. the strength of the correlation based on the value of
> b. the direction of the correlation based on the sign of
>
> The value of  gives us this information:
>
> • The value of  is always between
>  and
> :
> .
> • The size of the correlation  indicates the strength of the linear relationship between the two variables.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-005-pool-012

**Chunk:** `openstax_principles_ds:4.3:chunk-019`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> • Create a scatterplot.
> • Calculate the correlation coefficient.
> • Construct the best-fit linear equation.
> • Predict values of the dependent variable for given values of the independent variable.
>
> There are various ways to accomplish these tasks in Python, but we will use several functions available within
> the scipy library, such as:
>
> Pearsonr() for correlation coefficient
>
> linregress() for linear regression model
>
> plt.scatter() for scatterplot generation
>
> EXAMPLE 4.24
>
> Problem
>
> A marketing manager is interested in studying the correlation between the amount spent on advertising
> and revenue at a certain company. Twelve months of data were collected as shown in Table 4.16. (Dollar
> amounts are in thousands of dollars.)
>
> Use Python to perform the following analysis:
>
> a. Generate a scatterplot.
> b. Calculate the correlation coefficient .
>
> c. Determine if the correlation is significant (use level of significance of 0.05).
> d. Construct a linear regression model.
> e. Use the model to predict the revenue for a certain month where the amount spent on advertising is
>
> $100.
>
> Month
> Advertising
>
> Revenue
>
> Spend
>
> Jan
> 49
> 12210
>
> Feb
> 145
> 17590
>
> Mar
> 57
> 13215
>
> Apr
> 153
> 19200
>
> May
> 92
> 14600
>
> Jun
> 83
> 14100
>
> Jul
> 117
> 17100
>
> Aug
> 142
> 18400
>
> Table 4.16 Revenue versus Advertising for a Company
> (in $000s)
>
> Month
> Advertising
>
> Revenue
>
> Spend
>
> Sep
> 69
> 14100
>
> Oct
> 106
> 15500
>
> Nov
> 109
> 16300
>
> Dec
> 121
> 17020
>
> Table 4.16 Revenue versus Advertising for a Company
> (in $000s)
>
> Solution
>
> a. The first step in the analysis is to generate a scatterplot. (Recall that scatterplots were also discussed in
>
> Scatterplots and Correlation.)
> The Python function plt.scatter() can be used to generate the scatterplot for the
>  data. Note
>
> that we consider advertising to be the independent variable ( -data) and revenue to be the dependent
> variable ( -data) since revenue depends on the amount of advertising.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-006

**Pregunta:** If all other inputs remain unchanged, how does increasing the confidence level from 90% to 95% affect the width of the confidence interval, and why?

**Respondibilidad de referencia:** answerable

### q-v1-006-pool-001

**Chunk:** `openstax_intro_stats_2e:8.4:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.4: Confidence Interval (Home Costs)
>
> c. n = _____
>
> 2. In words, define the random variable
> . 3. State the estimated distribution to use. Use both words and symbols.
>
> Find the Confidence Interval
>
> 1. Calculate the confidence interval and the error bound.
> a. Confidence Interval: _____
> b. Error Bound: _____
>
> 2. How much area is in both tails (combined)? α = _____
> 3. How much area is in each tail?
>  = _____
>
> 4. Fill in the blanks on the graph with the area in each section. Then, fill in the number line with the upper and lower
> limits of the confidence interval and the sample mean.
>
> Figure 8.6
>
> 5. Some students think that a 90% confidence interval contains 90% of the data. Use the list of data on the first page
> and count how many of the data values lie within the confidence interval. What percent is this? Is this percent close
> to 90%? Explain why this percent should or should not be close to 90%.
>
> Describe the Confidence Interval
>
> 1. In two to three complete sentences, explain what a confidence interval means (in general), as if you were talking to
> someone who has not taken statistics. 2. In one to two complete sentences, explain what this confidence interval means for this particular study.
>
> Use the Data to Construct Confidence Intervals
>
> 1. Using the given information, construct a confidence interval for each confidence level given.
>
> Confidence level
> EBM/Error Bound
> Confidence Interval
>
> 50%
>
> 80%
>
> 95%
>
> 99%
>
> Table 8.6
>
> 2. What happens to the EBM as the confidence level increases? Does the width of the confidence interval increase or
> decrease? Explain why this happens.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-006-pool-003

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-010`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> = 68
>
> EBM =
>
> σ = 3; n = 36; The confidence level is 95% (CL = 0.95).
>
> CL = 0.95 so α = 1 – CL = 1 – 0.95 = 0.05
>
> The area to the right of z0.025 is 0.025 and the area to the left of z0.025 is 1 – 0.025 = 0.975.
>
> when using invnorm(0.975,0,1) on the TI-83, 83+, or 84+ calculators. (This can also be found using appropriate
> commands on other calculators, using a computer, or using a probability table for the standard normal distribution.)
>
> EBM = (1.96)
>  = 0.98
>
> – EBM = 68 – 0.98 = 67.02
>
> + EBM = 68 + 0.98 = 68.98
>
> Notice that the EBM is larger for a 95% confidence level in the original problem.
>
> We estimate with 95% confidence that the true population mean for all statistics exam scores is between 67.02 and
> 68.98.
>
> Explanation of 95% Confidence Level: Ninety-five percent of all confidence intervals constructed in this way contain the
> true value of the population mean statistics exam score.
>
> Comparing the results: The 90% confidence interval is (67.18, 68.82). The 95% confidence interval is (67.02, 68.98). The
> 95% confidence interval is wider. If you look at the graphs, because the area 0.95 is larger than the area 0.90, it makes
> sense that the 95% confidence interval is wider. To be more confident that the confidence interval actually does contain
> the true value of the population mean for all statistics exam scores, the confidence interval necessarily needs to be
> wider.
>
> Figure 8.5
>
> Summary: Effect of Changing the Confidence Level
>
> • Increasing the confidence level increases the error bound, making the confidence interval wider.
> • Decreasing the confidence level decreases the error bound, making the confidence interval narrower.
>
> TRY IT 8.4
>
> Refer back to the pizza-delivery Try It exercise.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-006-pool-004

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-011`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> Figure 8.5
>
> Summary: Effect of Changing the Confidence Level
>
> • Increasing the confidence level increases the error bound, making the confidence interval wider.
> • Decreasing the confidence level decreases the error bound, making the confidence interval narrower.
>
> TRY IT 8.4
>
> Refer back to the pizza-delivery Try It exercise. The population standard deviation is six minutes and the sample mean
> deliver time is 36 minutes. Use a sample size of 20. Find a 95% confidence interval estimate for the true mean pizza
> delivery time.
>
> EXAMPLE 8.5
>
> Suppose we change the original problem in Example 8.2 to see what happens to the error bound if the sample size is
> changed.
>
> Problem
> Leave everything the same except the sample size. Use the original 90% confidence level. What happens to the error
> bound and the confidence interval if we increase the sample size and use n = 100 instead of n = 36? What happens if we
>
> decrease the sample size to n = 25 instead of n = 36?
>
> •
>  = 68
>
> • EBM =
>
> • σ = 3; The confidence level is 90% (CL=0.90);
>  = z0.05 = 1.645.
>
> Solution
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
>
> TRY IT 8.5
>
> Refer back to the pizza-delivery Try It exercise.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-006-pool-005

**Chunk:** `openstax_intro_stats_2e:8.6:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.6: Confidence Interval (Women's Heights)
>
> 5. When we construct a 90% confidence interval, we say that we are 90% confident that the true population mean
> lies within the confidence interval. Using complete sentences, explain what we mean by this phrase. 6. Some students think that a 90% confidence interval contains 90% of the data. Use the list of data given (the heights
> of women) and count how many of the data values lie within the confidence interval that you generated based on
> that data. How many of the 100 data values lie within your confidence interval? What percent is this? Is this percent
> close to 90%? 7. Explain why it does not make sense to count data values that lie in a confidence interval. Think about the random
> variable that is being used in the problem. 8. Suppose you obtained the heights of ten women and calculated a confidence interval from this information. Without knowing the population mean μ, would you have any way of knowing for certain if your interval actually
> contained the value of μ? Explain.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-006-pool-006

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-012`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> When n = 25: EBM =
>  = (1.645)
>  = 0.987.
>
> Summary: Effect of Changing the Sample Size
>
> • Increasing the sample size causes the error bound to decrease, making the confidence interval narrower.
> • Decreasing the sample size causes the error bound to increase, making the confidence interval wider.
>
> TRY IT 8.5
>
> Refer back to the pizza-delivery Try It exercise. The mean delivery time is 36 minutes and the population standard
> deviation is six minutes. Assume the sample size is changed to 50 restaurants with the same sample mean. Find a
> 90% confidence interval estimate for the population mean delivery time.
>
> Working Backwards to Find the Error Bound or Sample Mean
>
> When we calculate a confidence interval, we find the sample mean, calculate the error bound, and use them to calculate
> the confidence interval. However, sometimes when we read statistical studies, the study may state the confidence
> interval only. If we know the confidence interval, we can work backwards to find both the error bound and the sample
> mean.
>
> Finding the Error Bound
>
> • From the upper value for the interval, subtract the sample mean,
> • OR, from the upper value for the interval, subtract the lower value. Then divide the difference by two.
>
> Finding the Sample Mean
>
> • Subtract the error bound from the upper value of the confidence interval,
> • OR, average the upper and lower endpoints of the confidence interval.
>
> Notice that there are two methods to perform each calculation. You can choose the method that is easier to use with the
> information you know.
>
> EXAMPLE 8.6
>
> Suppose we know that a confidence interval is (67.18, 68.82) and we want to find the error bound.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-006-pool-007

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-009`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> 79
> 145
> 147
> 160
> 116
> 100
> 159
> 151
> 156
> 126
>
> 137
> 83
> 156
> 94
> 121
> 144
> 123
> 114
> 139
> 99
>
> Table 8.3
>
> Use this sample data to construct a 90% confidence interval for the mean number of targeted industrial chemicals to be
> found in an in infant’s blood.
>
> Solution
> From the sample, you can calculate  = 127.45 and s = 25.965. There are 20 infants in the sample, so n = 20, and df = 20 –
> 1 = 19.
>
> You are asked to calculate a 90% confidence interval: CL = 0.90, so α = 1 – CL = 1 – 0.90 = 0.10
>
> By definition, the area to the right of t0.05 is 0.05 and so the area to the left of t0.05 is 1 – 0.05 = 0.95.
>
> Use a table, calculator, or computer to find that t0.05 = 1.729.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-006-pool-008

**Chunk:** `openstax_intro_stats_2e:8.6:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.6: Confidence Interval (Women's Heights)
>
> Confidence level
> EBP/Error Bound
> Confidence Interval
>
> 95%
>
> 99%
>
> Table 8.7
>
> 4. What happens to the EBP as the confidence level increases? Does the width of the confidence interval increase or
> decrease? Explain why this happens.
>
> 8.6 Confidence Interval (Women's Heights)
>
> Stats Lab
>
> Confidence Interval (Women's Heights)
> Class Time:
>
> Names:
>
> Student Learning Outcomes
>
> • The student will calculate a 90% confidence interval using the given data.
> • The student will determine the relationship between the confidence level and the percentage of constructed
> intervals that contain the population mean.
>
> Given:
>
> 59.4
> 71.6
> 69.3
> 65.0
> 62.9
> 66.5
> 61.7
> 55.2
>
> 67.5
> 67.2
> 63.8
> 62.9
> 63.0
> 63.9
> 68.7
> 65.5
>
> 61.9
> 69.6
> 58.7
> 63.4
> 61.8
> 60.6
> 69.8
> 60.0
>
> 64.9
> 66.1
> 66.8
> 60.6
> 65.6
> 63.8
> 61.3
> 59.2
>
> 64.1
> 59.3
> 64.9
> 62.4
> 63.5
> 60.9
> 63.3
> 66.3
>
> 61.5
> 64.3
> 62.9
> 60.6
> 63.8
> 58.8
> 64.9
> 65.7
>
> 62.5
> 70.9
> 62.9
> 63.1
> 62.2
> 58.7
> 64.7
> 66.0
>
> 60.5
> 64.7
> 65.4
> 60.2
> 65.0
> 64.1
> 61.1
> 65.3
>
> 64.6
> 59.2
> 61.4
> 62.0
> 63.5
> 61.4
> 65.5
> 62.3
>
> 65.5
> 64.7
> 58.8
> 66.1
> 64.9
> 66.9
> 57.9
> 69.8
>
> 58.5
> 63.4
> 69.2
> 65.9
> 62.2
> 60.0
> 58.1
> 62.5
>
> Table 8.8 Heights of 100 Women (in Inches)
>
> 62.4
> 59.1
> 66.4
> 61.2
> 60.4
> 58.7
> 66.7
> 67.5
>
> 63.2
> 56.6
> 67.7
> 62.5
>
> Table 8.8 Heights of 100 Women (in Inches)
>
> 1. Table 8.8 lists the heights of 100 women. Use a random number generator to select ten data values randomly. 2. Calculate the sample mean and the sample standard deviation. Assume that the population standard deviation is
> known to be 3.3 inches. With these values, construct a 90% confidence interval for your sample of ten values. Write
> the confidence interval you obtained in the first space of Table 8.9. 3. Now write your confidence interval on the board. As others in the class write their confidence intervals on the board,
> copy them into Table 8.9.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-006-pool-009

**Chunk:** `openstax_intro_stats_2e:8.intro:chunk-004`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.intro: Introduction
>
> For the Apple Music example, suppose that a sample produced a sample mean
> . Then the unknown population
> mean μ is between
>
> and
>
> We say that we are 95% confident that the unknown population mean number of songs downloaded from Apple Music
> per month is between 1.8 and 2.2. The 95% confidence interval is (1.8, 2.2).
>
> The 95% confidence interval implies two possibilities. Either the interval (1.8, 2.2) contains the true mean μ or our sample
> produced an  that is not within 0.2 units of the true mean μ. The first possibility happens for 95% of well-chosen
> samples. It is important to remember that the second possibility happens for 5% of samples, even though correct
> procedures are followed.
>
> Remember that a confidence interval is created for an unknown population parameter like the population mean, μ. Confidence intervals for some parameters have the form:
>
> (point estimate – margin of error, point estimate + margin of error)
>
> The margin of error depends on the confidence level or percentage of confidence and the standard error of the mean.
>
> When you read newspapers and journals, some reports will use the phrase "margin of error." Other reports will not use
> that phrase, but include a confidence interval as the point estimate plus or minus the margin of error. These are two
> ways of expressing the same concept.
>
> NOTE
>
> Although the text only covers symmetrical confidence intervals, there are non-symmetrical confidence intervals (for
> example, a confidence interval for the standard deviation).
>
> COLLABORATIVE EXERCISE
>
> Have your instructor record the number of meals each student in your class eats out in a week. Assume that the

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-006-pool-010

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> The margin of error (EBM) depends on the confidence level (abbreviated CL). The confidence level is often considered
> the probability that the calculated confidence interval estimate will contain the true population parameter. However, it is
> more accurate to state that the confidence level is the percent of confidence intervals that contain the true population
> parameter when repeated samples are taken. Most often, it is the choice of the person constructing the confidence
> interval to choose a confidence level of 90% or higher because that person wants to be reasonably certain of their
> conclusions.
>
> There is another probability called alpha (α). α is related to the confidence level, CL. α is the probability that the interval
> does not contain the unknown population parameter. Mathematically, α + CL = 1.
>
> EXAMPLE 8.1
>
> Suppose we have collected data from a sample. We know the sample mean but we do not know the mean for the entire
> population. The sample mean is seven, and the error bound for the mean is 2.5.
>
> = 7 and EBM = 2.5
>
> The confidence interval is (7 – 2.5, 7 + 2.5), and calculating the values gives (4.5, 9.5).
>
> If the confidence level (CL) is 95%, then we say that, "We estimate with 95% confidence that the true value of the
> population mean is between 4.5 and 9.5."
>
> TRY IT 8.1
>
> Suppose we have data from a sample. The sample mean is 15, and the error bound for the mean is 3.2.
>
> What is the confidence interval estimate for the population mean?
>
> A confidence interval for a population mean with a known standard deviation is based on the fact that the sample means
> follow an approximately normal distribution.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-006-pool-011

**Chunk:** `openstax_intro_stats_2e:8.3:chunk-005`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.3: A Population Proportion
>
> Since CL = 0.95, then α = 1 – CL = 1 – 0.95 = 0.05
>  = 0.025.
>
> Then
>
> Use the TI-83, 83+, or 84+ calculator command invNorm(0.975,0,1) to find z0.025. Remember that the area to the right of
> z0.025 is 0.025 and the area to the left of z0.025 is 0.975. This can also be found using appropriate commands on other
> calculators, using a computer, or using a Standard Normal probability table.
>
> The confidence interval for the true binomial population proportion is
>
> Interpretation: We estimate with 95% confidence that between 81% and 87.4% of all adult residents of this city have
> smartphones.
>
> Explanation of 95% Confidence Level: Ninety-five percent of the confidence intervals constructed in this way would
> contain the true value for the population proportion of all adult residents of this city who have smartphones.
>
> Solution
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> Press STAT and arrow over to TESTS.
>
> Arrow down to A:1-PropZint. Press ENTER.
>
> Arrow down to  and enter 421. Arrow down to  and enter 500. Arrow down to C-Level and enter .95.
>
> Arrow down to Calculate and press ENTER.
>
> The confidence interval is (0.81003, 0.87397).
>
> TRY IT 8.10
>
> Suppose 250 randomly selected people are surveyed to determine if they own a tablet. Of the 250 surveyed, 98
>
> reported owning a tablet. Using a 95% confidence level, compute a confidence interval estimate for the true
> proportion of people who own tablets.
>
> EXAMPLE 8.11
>
> Problem
> For a class project, a political science student at a large university wants to estimate the percent of students who are
> registered voters. He surveys 500 students and finds that 300 are registered voters. Compute a 90% confidence interval
> for the true percent of students who are registered voters, and interpret the confidence interval.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-006-pool-012

**Chunk:** `openstax_intro_stats_2e:8.3:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.3: A Population Proportion
>
> – EBM = 127.45 – 10.038 = 117.412
>
> + EBM = 127.45 + 10.038 = 137.488
>
> We estimate with 90% confidence that the mean number of all targeted industrial chemicals found in cord blood in the
> United States is between 117.412 and 137.488.
>
> Solution
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> Enter the data as a list. Press STAT and arrow over to TESTS.
>
> Arrow down to 8:TInterval and press ENTER (or you can just press 8). Arrow to Data and press ENTER.
>
> Arrow down to List and enter the list name where you put the data.
>
> Arrow down to Freq and enter 1.
>
> Arrow down to C-level and enter 0.90
>
> Arrow down to Calculate and press ENTER.
>
> The 90% confidence interval is (117.41, 137.49).
>
> TRY IT 8.9
>
> A random sample of statistics students were asked to estimate the total number of hours they spend watching
> television in an average week. The responses are recorded in Table 8.4. Use this sample data to construct a 98%
> confidence interval for the mean number of hours statistics students will spend watching television in one week.
>
> 0
> 3
> 1
> 20
> 9
>
> 5
> 10
> 1
> 10
> 4
>
> 14
> 2
> 4
> 4
> 5
>
> Table 8.4
>
> 8.3 A Population Proportion
>
> During an election year, we see articles in the newspaper that state confidence intervals in terms of proportions or
> percentages. For example, a poll for a particular candidate running for president might show that the candidate has 40%
> of the vote within three percentage points (if the sample is large enough). Often, election polls are calculated with 95%
> confidence, so, the pollsters would be 95% confident that the true proportion of voters who favored the candidate would
> be between 0.37 and 0.43: (0.40 – 0.03,0.40 + 0.03).

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-006-pool-013

**Chunk:** `openstax_intro_stats_2e:8.3:chunk-006`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.3: A Population Proportion
>
> EXAMPLE 8.11
>
> Problem
> For a class project, a political science student at a large university wants to estimate the percent of students who are
> registered voters. He surveys 500 students and finds that 300 are registered voters. Compute a 90% confidence interval
> for the true percent of students who are registered voters, and interpret the confidence interval.
>
> Solution
> • The first solution is step-by-step.
> • The second solution uses a function of the TI-83, 83+, or 84 calculators.
>
> x = 300 and n = 500
>
> Since CL = 0.90, then α = 1 – CL = 1 – 0.90 = 0.10
>  = 0.05
>
> = z0.05 = 1.645
>
> Use the TI-83, 83+, or 84+ calculator command invNorm(0.95,0,1) to find z0.05. Remember that the area to the right of
> z0.05 is 0.05 and the area to the left of z0.05 is 0.95. This can also be found using appropriate commands on other
> calculators, using a computer, or using a standard normal probability table.
>
> The confidence interval for the true binomial population proportion is (
>  – EBP,
>  + EBP) = (0.564,0.636).
>
> • Interpretation: We estimate with 90% confidence that the true percent of all students that are registered voters is
> between 56.4% and 63.6%.
> • Alternate Wording: We estimate with 90% confidence that between 56.4% and 63.6% of ALL students are registered
> voters.
>
> Explanation of 90% Confidence Level: Ninety percent of all confidence intervals constructed in this way contain the true
> value for the population percent of students that are registered voters.
>
> Solution
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> Press STAT and arrow over to TESTS.
>
> Arrow down to A:1-PropZint. Press ENTER.
>
> Arrow down to  and enter 300. Arrow down to  and enter 500. Arrow down to C-Level and enter 0.90.
>
> Arrow down to Calculate and press ENTER.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-006-pool-014

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-005`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> Random sampling is assumed, but that is a completely separate assumption from normality.
>
> Calculators and computers can easily calculate any Student's t-probabilities. The TI-83,83+, and 84+ have a tcdf function
> to find the probability for given values of t. The grammar for the tcdf command is tcdf(lower bound, upper bound,
> degrees of freedom). However for confidence intervals, we need to use inverse probability to find the value of t when we
> know the probability.
>
> For the TI-84+ you can use the invT command on the DISTRibution menu. The invT command works similarly to the
> invnorm. The invT command requires two inputs: invT(area to the left, degrees of freedom) The output is the t-score
> that corresponds to the area we specified.
>
> The TI-83 and 83+ do not have the invT command. (The TI-89 has an inverse T command.)
>
> A probability table for the Student's t-distribution can also be used. The table gives t-scores that correspond to the
> confidence level (column) and degrees of freedom (row). (The TI-86 does not have an invT program or command, so if
> you are using that calculator, you need to use a probability table for the Student's t-Distribution.) When using a t-table,
> note that some tables are formatted to show the confidence level in the column headings, while the column headings in
> some tables may show only corresponding area in one or both tails.
>
> A Student's t table (See Appendix H Tables) gives t-scores given the degrees of freedom and the right-tailed probability. The table is very limited. Calculators and computers can easily calculate any Student's t-probabilities.
>
> The notation for the Student's t-distribution (using T as the random variable) is:

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-006-pool-015

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-008`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> NOTE
>
> When calculating the error bound, a probability table for the Student's t-distribution can also be used to find the value
> of t. The table gives t-scores that correspond to the confidence level (column) and degrees of freedom (row); the
> t-score is found where the row and column intersect in the table.
>
> TRY IT 8.8
>
> You do a study of hypnotherapy to determine how effective it is in increasing the number of hours of sleep subjects
> get each night. You measure hours of sleep for 12 subjects with the following results. Construct a 95% confidence
> interval for the mean number of hours slept for the population (assumed normal) from which you took the data.
>
> 8.2; 9.1; 7.7; 8.6; 6.9; 11.2; 10.1; 9.9; 8.9; 9.2; 7.5; 10.5
>
> EXAMPLE 8.9
>
> Problem
> The Human Toxome Project (HTP) is working to understand the scope of industrial pollution in the human body. Industrial chemicals may enter the body through pollution or as ingredients in consumer products. The scientists at HTP
> tested cord blood samples for 20 newborn infants in the United States. The cord blood of the "In utero/newborn" group
> was tested for 430 industrial compounds, pollutants, and other chemicals, including chemicals linked to brain and
> nervous system toxicity, immune system toxicity, and reproductive toxicity, and fertility problems. There are health
> concerns about the effects of some chemicals on the brain and nervous system. Table 8.3 shows how many of the
> targeted chemicals were found in each infant’s cord blood.
>
> 79
> 145
> 147
> 160
> 116
> 100
> 159
> 151
> 156
> 126
>
> 137
> 83
> 156
> 94
> 121
> 144
> 123
> 114
> 139
> 99
>
> Table 8.3
>
> Use this sample data to construct a 90% confidence interval for the mean number of targeted industrial chemicals to be
> found in an in infant’s blood.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-006-pool-016

**Chunk:** `openstax_intro_stats_2e:8.3:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.3: A Population Proportion
>
> Often, election polls are calculated with 95%
> confidence, so, the pollsters would be 95% confident that the true proportion of voters who favored the candidate would
> be between 0.37 and 0.43: (0.40 – 0.03,0.40 + 0.03).
>
> Investors in the stock market are interested in the true proportion of stocks that go up and down each week. Businesses
> that sell personal computers are interested in the proportion of households in the United States that own personal
> computers. Confidence intervals can be calculated for the true proportion of stocks that go up or down each week and
> for the true proportion of households in the United States that own personal computers.
>
> The procedure to find the confidence interval, the sample size, the error bound, and the confidence level for a
> proportion is similar to that for the population mean, but the formulas are different.
>
> How do you know you are dealing with a proportion problem? First, the underlying distribution is a binomial
> distribution. (There is no mention of a mean or average.) If X is a binomial random variable, then X ~ B(n, p) where n is
> the number of trials and p is the probability of a success. To form a proportion, take X, the random variable for the
> number of successes and divide it by n, the number of trials (or the sample size). The random variable
>  (read "P prime")
>
> is that proportion,
>
> (Sometimes the random variable is denoted as
> , read "P hat".)
>
> When n is large and p is not close to zero or one, we can use the normal distribution to approximate the binomial.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-006-pool-017

**Chunk:** `openstax_principles_ds:4.1:chunk-004`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> An unbiased estimator is a statistic that provides an
> accurate estimate for the corresponding population parameter without overestimating or underestimating the
> parameter.
>
> In order to calculate a confidence interval, two quantities are needed:
>
> • The point estimate
> • The margin of error
>
> As noted, the point estimate is a single number that is used to estimate the population parameter. The margin
> of error (usually denoted by E) provides an indication of the maximum error of the estimate. The margin of
> error can be viewed as the maximum distance around the point estimate where the population parameter
> exists based on a specified confidence.
>
> Once the point estimate and margin of error are determined, the confidence interval is calculated as follows:
>
> The margin of error reflects the desired confidence level of the researcher. The confidence level is the
> probability that the interval estimate will contain the population parameter, given that the estimation process
> on the parameter is repeated over and over. Confidence levels typically range from 80% to 95% confidence.
>
> In addition to the confidence level, both the variability of the sample and the sample size will affect the margin
> of error.
>
> Once the confidence interval has been calculated, a concluding statement is made that reflects both the
> confidence level and the unknown population parameter. The concluding statement indicates that there is a
> certain level of confidence that the population parameter is contained within the bounds of the confidence
> interval.
>
> As an example, consider a data scientist who is interested in forecasting the median income for all residents of
> California. Income data is collected from a sample of 1,000 residents, and the median income level is $68,500. Also assume the margin of error for a 95% confidence interval is $4,500 (more details on the calculation of
> margin of error are provided next).

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-007

**Pregunta:** According to the selected sources, what is the Pearson correlation between weekly study time and final exam score?

**Respondibilidad de referencia:** unanswerable

### q-v1-007-pool-001

**Chunk:** `openstax_intro_stats_2e:6.2:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 6: The Normal Distribution
> Section 6.2: Using the Normal Distribution
>
> TRY IT 6.7
>
> If the area to the left of x is 0.012, then what is the area to the right?
>
> EXAMPLE 6.8
>
> The final exam scores in a statistics class were normally distributed with a mean of 63 and a standard deviation of five.
>
> Problem
> a. Find the probability that a randomly selected student scored more than 65 on the exam.
>
> Solution
> a. Let X = a score on the final exam. X ~ N(63, 5), where μ = 63 and σ = 5.
>
> Draw a graph.
>
> Then, find P(x > 65).
>
> P(x > 65) = 0.3446
>
> Figure 6.5
>
> The probability that any student selected at random scores more than 65 is 0.3446.
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> Go into 2nd DISTR.
>
> After pressing 2nd DISTR, press 2:normalcdf.
>
> The syntax for the instructions are as follows:
>
> normalcdf(lower value, upper value, mean, standard deviation) For this problem: normalcdf(65,1E99,63,5) = 0.3446. You get 1E99 (= 1099) by pressing 1, the EE key (a 2nd key) and then 99. Or, you can enter 10^99 instead. The number
>
> 1099 is way out in the right tail of the normal curve. We are calculating the area between 65 and 1099. In some
>
> instances, the lower number of the area might be –1E99 (= –1099). The number –1099 is way out in the left tail of the
> normal curve.
>
> Historical Note
>
> The TI probability program calculates a z-score and then the probability from the z-score. Before technology, the
> z-score was looked up in a standard normal probability table (because the math involved is too cumbersome) to find
> the probability. In this example, a standard normal table with area to the left of the z-score was used. You calculate
> the z-score and look up the area to the left.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-007-pool-002

**Chunk:** `openstax_principles_ds:4.3:chunk-007`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> As mentioned, given the complexity of this calculation, software is typically used to calculate the correlation
> coefficient. There are several options for calculating the correlation coefficient in Python. The example shown
> uses the scipy.stats library in Python which includes the function pearsonr() for calculating the Pearson
>
> correlation coefficient ( ).
>
> We will create two numerical arrays in Python using the np.array() function and then use the pearsonr()
>
> function to calculate the Pearson correlation coefficient for the
>  data shown in Table 4.15.
>
> The following Python code provides the correlation coefficient for the Nike Stock Price dataset as 0.923.
>
> PYTHON CODE
>
> # import libraries
> import numpy as np
> from scipy.stats  import pearsonr
>  
> # establish x and y data, x-data is S&P500 value, y-data is Nike Stock Price
>
> SP500 = np.array([2912.43, 3044.31, 3100.29, 3271.12, 3500.31, 3363.00, 3269.96,
> 3621.63, 3756.07, 3714.24, 3811.15, 3943.34])
>
> Nike = np.array([87.18, 98.58, 98.05, 97.61, 111.89, 125.54, 120.08, 134.70,
> 141.47, 133.59, 134.78, 140.45])
>
> #pearson r returns both value of r and corresponding p-value
>
> r, p = pearsonr(SP500, Nike)
>
> #print value of r , rounded to 3 decimal places
>
> print("Correlation coefficient: ", round(r, 3))
>
> The resulting output will look like this:
>
> Correlation coefficient: 0.923
>
> Interpret a Correlation Coefficient
>
> Once the value of  is calculated, this measurement provides two indicators for the correlation:
>
> a. the strength of the correlation based on the value of
> b. the direction of the correlation based on the sign of
>
> The value of  gives us this information:
>
> • The value of  is always between
>  and
> :
> .
> • The size of the correlation  indicates the strength of the linear relationship between the two variables.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-007-pool-003

**Chunk:** `openstax_intro_stats_2e:9.1:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.1: Null and Alternative Hypotheses
>
> a. H0: μ __ 66
> b. Ha: μ __ 66
>
> EXAMPLE 9.3
>
> We want to test if college students take less than five years to graduate from college, on the average. The null and
> alternative hypotheses are:
> H0: μ ≥ 5
> Ha: μ < 5
>
> TRY IT 9.3
>
> We want to test if it takes fewer than 45 minutes to teach a lesson plan. State the null and alternative hypotheses. Fill
> in the correct symbol ( =, ≠, ≥, <, ≤, >) for the null and alternative hypotheses.
>
> a. H0: μ __ 45
> b. Ha: μ __ 45
>
> EXAMPLE 9.4
>
> In an issue of U. S. News and World Report, an article on school standards stated that about half of all students in France,
> Germany, and Israel take advanced placement exams and a third pass. The same article stated that 6.6% of U.S. students
> take advanced placement exams and 4.4% pass. Test if the percentage of U.S. students who take advanced placement
> exams is more than 6.6%. State the null and alternative hypotheses. H0: p ≤ 0.066
> Ha: p > 0.066
>
> TRY IT 9.4
>
> On a state driver’s test, about 40% pass the test on the first try. We want to test if more than 40% pass on the first try. Fill in the correct symbol (=, ≠, ≥, <, ≤, >) for the null and alternative hypotheses.
>
> a. H0: p __ 0.40
> b. Ha: p __ 0.40

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-007-pool-004

**Chunk:** `openstax_principles_ds:4.1:chunk-009`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Thus, the critical value is that z-score which cuts off an area of 0.025 in the upper tail of the standard normal
> curve.
>
> Figure 4.2 Critical Values of zc Marked on Standard Normal Curve for 95% Confidence Interval
>
> Once the margin of error has been calculated, the confidence interval can be calculated as follows:
>
> Note that this is the general format for constructing any confidence interval, namely the margin of error is
> added and subtracted to the sample statistic to generate the upper and lower bounds of the confidence
> interval, respectively. A sample statistic describes some aspect of the sample, such as a sample mean or
> sample proportion.
>
> General Form of a Confidence Interval:
>
> EXAMPLE 4.3
>
> Problem
>
> A college professor collects data on the amount of time spent on homework assignments per week for a
>
> sample of 50 students in a statistics course. From the sample of 50 students, the mean amount of time
> spent on homework assignments per week is 12.5 hours. The population standard deviation is known to be
> 6.3 hours.
>
> The professor would like to forecast the amount of time spent on homework in future semesters. Create a
> forecasted confidence interval using both a 90% and 95% confidence interval and provide a conclusion
> regarding the confidence interval. Also compare the widths of the two confidence intervals. Which
> confidence interval is wider?
>
> Solution
>
> Calculation for 90% Confidence Interval
>
> For a 90% confidence interval, the corresponding critical value is
> .
>
> The margin of error is calculated as follows:
>
> The 90% confidence interval is calculated as follows:
>
> Concluding statement:
>
> The college professor can forecast with 90% confident that the mean amount of time spent on homework
> assignments in a future semester is the interval from 11.03 to 13.97 hours per week.
>
> Calculation for 95% Confidence Interval

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-007-pool-005

**Chunk:** `openstax_principles_ds:4.3:chunk-006`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> A more precise assessment of the correlation between the two quantities can be obtained by
> calculating the numeric correlation coefficient (referred to using the symbol ).
>
> The correlation coefficient is a measure of the strength and direction of the correlation between the
> independent variable  and the dependent variable .
>
> The formula for  is shown; however, software is typically used to calculate the correlation coefficient.
>
> where  refers to the number of data pairs and the symbol
>  indicates to sum the x-values.
>
> Note that this value of “ ” is sometimes referred to as the “Pearson correlation coefficient.”
>
> Table 4.15 provides a step-by-step procedure on how to calculate the correlation coefficient .
>
> Step
> Representation in Symbols
>
> 1. Calculate the sum of the x-values.
>
> 2. Calculate the sum of the y-values.
>
> 3. Multiply each x-value by the corresponding
> y-value and calculate the sum of these
>  products.
>
> 4. Square each x-value and then calculate the sum
> of these squared values.
>
> 5. Square each y-value and then calculate the sum
> of these squared values.
>
> n
>
> 6. Determine the value of , which is the number of
> data pairs.
>
> 7. Use these results to then substitute into the
> formula for the correlation coefficient.
>
> Table 4.15 Steps for Calculating the Correlation Coefficient
>
> Note that since  is calculated using sample data,  is considered a sample statistic and is used to measure the
> strength of the correlation for the two population variables. Recall that sample data indicates data based on a
> subset of the entire population.
>
> As mentioned, given the complexity of this calculation, software is typically used to calculate the correlation
> coefficient. There are several options for calculating the correlation coefficient in Python. The example shown
> uses the scipy.stats library in Python which includes the function pearsonr() for calculating the Pearson
>
> correlation coefficient ( ).

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-007-pool-006

**Chunk:** `openstax_principles_ds:4.3:chunk-021`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> #pearson r returns both value of r and corresponding p-value
> r, p = pearsonr(x, y)
>
> #print value of r, rounded to 3 decimal places
>
> print("Correlation coefficient: ", round(r, 3))
>
> The resulting output will look like this:
>
> Correlation coefficient: 0.981
> This value of
>  indicates a strong, positive correlation between
> advertising spend and revenue.
>
> c. When using a level of significance of 0.05, if
> , then this implies that the correlation between
>
> the two variables demonstrates a linear relationship that is statistically significant at approximately the
>
> 0.05 level of significance. In this example, we check if
>  is greater than or equal to
>  where
>
> . Since
>  is approximately 0.577, this indicates that the r-value of 0.981 is greater than
> ,
>
> and thus the correlation is deemed significant.
> d. The linear regression model will be of the form:
>
> To determine the slope and y-intercept of the regression model, the Python function linregress()
>
> can be used. This function takes the  and  data as inputs and provides the slope and intercept as well as other
> regression-related output.
>
> Here is the Python code to generate the slope and y-intercept of the best-fit line:
>
> PYTHON CODE
>
> # import libraries
> import numpy as np
> from scipy.stats  import linregress
>
> # define the x-data, which is amount spent on advertising
> x = [49, 145, 57, 153, 92, 83, 117, 142, 69, 106, 109, 121]
>
> # define the y-data, which is revenue
> y = [12210, 17590, 13215, 19200, 14600, 14100, 17100, 18400, 14100, 15500, 16300,
> 17020]
>
> #pearson r returns both value of r and corresponding p-value
> slope, intercept, r_value, p_value, std_err  = linregress(x, y)
>
> print ("slope  =", slope)
> print("intercept = ", intercept)
>
> The resulting output will look like this:
>
> slope = 61.79775818816664
> intercept = 9376.698881009072
>
> Based on this Python equation, the regression equation can be written as

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-007-pool-007

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-008`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> NOTE
>
> When calculating the error bound, a probability table for the Student's t-distribution can also be used to find the value
> of t. The table gives t-scores that correspond to the confidence level (column) and degrees of freedom (row); the
> t-score is found where the row and column intersect in the table.
>
> TRY IT 8.8
>
> You do a study of hypnotherapy to determine how effective it is in increasing the number of hours of sleep subjects
> get each night. You measure hours of sleep for 12 subjects with the following results. Construct a 95% confidence
> interval for the mean number of hours slept for the population (assumed normal) from which you took the data.
>
> 8.2; 9.1; 7.7; 8.6; 6.9; 11.2; 10.1; 9.9; 8.9; 9.2; 7.5; 10.5
>
> EXAMPLE 8.9
>
> Problem
> The Human Toxome Project (HTP) is working to understand the scope of industrial pollution in the human body. Industrial chemicals may enter the body through pollution or as ingredients in consumer products. The scientists at HTP
> tested cord blood samples for 20 newborn infants in the United States. The cord blood of the "In utero/newborn" group
> was tested for 430 industrial compounds, pollutants, and other chemicals, including chemicals linked to brain and
> nervous system toxicity, immune system toxicity, and reproductive toxicity, and fertility problems. There are health
> concerns about the effects of some chemicals on the brain and nervous system. Table 8.3 shows how many of the
> targeted chemicals were found in each infant’s cord blood.
>
> 79
> 145
> 147
> 160
> 116
> 100
> 159
> 151
> 156
> 126
>
> 137
> 83
> 156
> 94
> 121
> 144
> 123
> 114
> 139
> 99
>
> Table 8.3
>
> Use this sample data to construct a 90% confidence interval for the mean number of targeted industrial chemicals to be
> found in an in infant’s blood.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-007-pool-008

**Chunk:** `openstax_principles_ds:4.3:chunk-020`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> Scatterplots and Correlation.)
> The Python function plt.scatter() can be used to generate the scatterplot for the
>  data. Note
>
> that we consider advertising to be the independent variable ( -data) and revenue to be the dependent
> variable ( -data) since revenue depends on the amount of advertising.
>
> Here is the Python code to generate the scatterplot:
>
> PYTHON CODE
>
> # import the matplotlib library
> import matplotlib.pyplot as plt
>
> # define the x-data, which is amount spent on advertising
> x = [49, 145, 57, 153, 92, 83, 117, 142, 69, 106, 109, 121]
>
> # define the y-data, which is revenue
> y = [12210, 17590, 13215, 19200, 14600, 14100, 17100, 18400, 14100, 15500, 16300,
> 17020]
>
> # use the scatter function to generate a time series graph
> plt.scatter(x, y)
>
> # Add a title using the title function
> plt.title("Revenue versus Advertising for a Company")
>
> # Add labels to the x and y axes by using xlabel and ylabel functions
> plt.xlabel("Advertising $000")
> plt.ylabel ("Revenue $000")
>
> The resulting output will look like this:
>
> b. The Python function pearsonr() can be used to generate the correlation coefficient, .
>
> Here is the Python code to calculate the correlation coefficient:
>
> PYTHON CODE
>
> # import libraries
> import numpy as np
> from scipy.stats  import pearsonr
>
> # define the x-data, which is amount spent on advertising
> x = [49, 145, 57, 153, 92, 83, 117, 142, 69, 106, 109, 121]
>
> # define the y-data, which is revenue
> y = [12210, 17590, 13215, 19200, 14600, 14100, 17100, 18400, 14100, 15500, 16300,
> 17020]
>
> #pearson r returns both value of r and corresponding p-value
> r, p = pearsonr(x, y)
>
> #print value of r, rounded to 3 decimal places
>
> print("Correlation coefficient: ", round(r, 3))
>
> The resulting output will look like this:
>
> Correlation coefficient: 0.981
> This value of
>  indicates a strong, positive correlation between
> advertising spend and revenue.
>
> c.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-007-pool-009

**Chunk:** `openstax_intro_stats_2e:8.3:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.3: A Population Proportion
>
> – EBM = 127.45 – 10.038 = 117.412
>
> + EBM = 127.45 + 10.038 = 137.488
>
> We estimate with 90% confidence that the mean number of all targeted industrial chemicals found in cord blood in the
> United States is between 117.412 and 137.488.
>
> Solution
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> Enter the data as a list. Press STAT and arrow over to TESTS.
>
> Arrow down to 8:TInterval and press ENTER (or you can just press 8). Arrow to Data and press ENTER.
>
> Arrow down to List and enter the list name where you put the data.
>
> Arrow down to Freq and enter 1.
>
> Arrow down to C-level and enter 0.90
>
> Arrow down to Calculate and press ENTER.
>
> The 90% confidence interval is (117.41, 137.49).
>
> TRY IT 8.9
>
> A random sample of statistics students were asked to estimate the total number of hours they spend watching
> television in an average week. The responses are recorded in Table 8.4. Use this sample data to construct a 98%
> confidence interval for the mean number of hours statistics students will spend watching television in one week.
>
> 0
> 3
> 1
> 20
> 9
>
> 5
> 10
> 1
> 10
> 4
>
> 14
> 2
> 4
> 4
> 5
>
> Table 8.4
>
> 8.3 A Population Proportion
>
> During an election year, we see articles in the newspaper that state confidence intervals in terms of proportions or
> percentages. For example, a poll for a particular candidate running for president might show that the candidate has 40%
> of the vote within three percentage points (if the sample is large enough). Often, election polls are calculated with 95%
> confidence, so, the pollsters would be 95% confident that the true proportion of voters who favored the candidate would
> be between 0.37 and 0.43: (0.40 – 0.03,0.40 + 0.03).

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-007-pool-010

**Chunk:** `openstax_principles_ds:4.3:chunk-003`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> For
> instance, regression analysis can be used to establish a mathematical equation that relates a dependent
> variable (such as sales) to an independent variable (such as advertising expenditure). But it has many
> applications apart from business as well. An automotive engineer is interested in the correlation between
> outside temperature and battery life for an electric vehicle, for instance.
>
> Our discussion here will focus on linear regression—analyzing the relationship between one dependent
> variable and one independent variable, where the relationship can be modeled using a linear equation.
>
> Scatterplots and Correlation
>
> In correlation analysis, we study the relationship between bivariate data, which is data collected on two
> variables where the data values are paired with one another. Correlation measures the association between
> two numeric variables. We may be interested in knowing if there is a correlation between bond prices and
> interest rates or between the age of a car and the value of the car. To investigate the correlation between two
> numeric quantities, the first step is to collect
>  data for the two numeric quantities of interest and then
> create a scatterplot that will graph the
>  ordered pairs. The independent, or explanatory, quantity is
> labeled the -variable, and the dependent, or response, quantity is labeled the -variable.
>
> For example, let’s say that a financial analyst wants to know if the price of Nike stock is correlated with the
> value of the S&P 500 (Standard & Poor’s 500 stock market index). To investigate this, monthly data can be
> collected for Nike stock prices and value of the S&P 500 for a period of time, and a scatterplot can be created
> and examined. A scatterplot, or scatter diagram, is a graphical display intended to show the relationship
> between two variables.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-007-pool-011

**Chunk:** `openstax_principles_ds:4.3:chunk-002`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> • 4.3.1 Create scatterplots and calculate and interpret correlation coefficients.
> • 4.3.2 Perform linear regression and determine the best-fit linear equation.
> • 4.3.3 Use Python to calculate correlation coefficients and determine equations of linear regression
> models.
>
> We briefly introduced correlation analysis at the beginning of this chapter, but now we want to dig in a little
> deeper. Data scientists are often interested in knowing if there are relationships, or a correlation, between two
> numeric quantities. For example, a medical researcher might be interested in investigating if there is a
> relationship between age and blood pressure. A college professor might be interested to know if there is a
> relationship between time spent on social media by students and corresponding academic grades.
>
> Correlation analysis allows for the determination of a statistical relationship between two numeric quantities,
> or variables—an independent variable and a dependent variable. The independent variable is the variable
> that you can change or control, while the dependent variable is what you measure or observe to see how it
>
> responds to those changes. Regression analysis takes this a step further by quantifying the relationship
> between the two variables, and it can be used to predict one quantity based on a second quantity, assuming
> there is a significant correlation between the two quantities. For example, the value of a car can be predicted
> based on the age of the car.
>
> Earlier we noted many business-related applications where correlation and regression analysis are used. For
> instance, regression analysis can be used to establish a mathematical equation that relates a dependent
> variable (such as sales) to an independent variable (such as advertising expenditure). But it has many
> applications apart from business as well. An automotive engineer is interested in the correlation between
> outside temperature and battery life for an electric vehicle, for instance.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-007-pool-012

**Chunk:** `openstax_principles_ds:3.2:chunk-002`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.2: Measures of Variation
>
> Providing some measure of the spread, or variation, in a dataset is crucial to a comprehensive summary of the
> dataset. Two datasets may have the same mean but can exhibit very different spread, and so a measure of
> dispersion for a dataset is very important. While measures of central tendency (like mean, median, and mode)
> describe the center or average value of a distribution, measures of dispersion give insights into how much
> individual data points deviate from this central value.
>
> The following two datasets are the exam scores for a group of three students in a biology course and in a
> statistics course.
>
> Dataset A: Exam scores for students in a biology course: 40, 70, 100
> Dataset B: Exam scores for students in a statistics course: 69, 70, 71
>
> Notice that the mean score for both Dataset A and Dataset B is 70.
>
> However, the datasets are significantly different from one another:
>
> Dataset A has larger variability where one student scored 30 points below the mean and another student
> scored 30 points above the mean. Dataset B has smaller variability where the exam scores are much more tightly clustered around the mean of
> 70.
>
> This example illustrates that publishing the mean of a dataset is often inadequate to fully communicate the
> characteristics of the dataset. Instead, data scientists will typically include a measure of variation as well.
>
> The three primary measures of variability are range, variance, and standard deviation, and these are described
> next.
>
> Range
>
> Range is a measure of dispersion for a dataset that is calculated by subtracting the minimum from the
> maximum of the dataset:
>
> Range is a straightforward calculation but makes use of only two of the data values in a dataset. The range can
> also be affected by outliers.
>
> EXAMPLE 3.6
>
> Problem

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-007-pool-013

**Chunk:** `openstax_principles_ds:4.3:chunk-001`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> Since these results are at least 5, the requirements are met.
>
> Calculate the sample proportions as follows:
>
> Next, calculate the standardized test statistic as follows:
>
> Notice that since the alternative hypothesis contains a “greater than” symbol, the hypothesis test is called a
> “right tailed” test and the p-value will be calculated as the area under the normal distribution curve to the
> right of the test statistic. The area under the normal distribution curve to the right of a z-score of 2.621 is
> approximately 0.004. Thus the p-value for this hypothesis test is 0.004.
>
> The final step in the hypothesis testing procedure is to come to a final decision regarding the null
> hypothesis. This is accomplished by comparing the p-value with the level of significance. In this example,
> the p-value is 0.004 and the level of significance is 0.01: since the p-value  level of significance, then the
> decision is to “reject the null hypothesis.”
>
> Conclusion: The decision is to reject the null hypothesis; the claim corresponds to the alternative
> hypothesis. This scenario corresponds to row #2 in Table 4.8, and “there is enough evidence to support the
> claim” that the proportion of subjects who are cancer free after taking the actual cancer drug is greater
> than the proportion for those who took the placebo. This indicates that the medication is effective in
> addressing lung cancer.
>
> 4.3 Correlation and Linear Regression Analysis
>
> Learning Outcomes
> By the end of this section, you should be able to:
>
> • 4.3.1 Create scatterplots and calculate and interpret correlation coefficients.
> • 4.3.2 Perform linear regression and determine the best-fit linear equation.
> • 4.3.3 Use Python to calculate correlation coefficients and determine equations of linear regression
> models.
>
> We briefly introduced correlation analysis at the beginning of this chapter, but now we want to dig in a little
> deeper.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-007-pool-014

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> He realized that he could not use a normal distribution for the calculation; he found that
>
> the actual distribution depends on the sample size. This problem led him to "discover" what is called the Student's t-
> distribution. The name comes from the fact that Gosset wrote under the pen name "Student."
>
> Up until the mid-1970s, some statisticians used the normal distribution approximation for large sample sizes and used
> the Student's t-distribution only for sample sizes of at most 30. With graphing calculators and computers, the practice
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
>
> Properties of the Student's t-Distribution

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-007-pool-015

**Chunk:** `openstax_principles_ds:4.2:chunk-003`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> The steps for hypothesis testing are as follows:
>
> 1. Set up a null and alternative hypothesis based on the claim. Identify whether the null or the alternative
> hypothesis represents the claim. 2. Collect relevant sample data to investigate the claim. 3. Determine the correct distribution to be used to analyze the hypothesis test (e.g., normal distribution or t-
> distribution). 4. Analyze the sample data to determine if the sample data is consistent with the null hypothesis. This will
> involve statistical calculations involving what is called a test statistic and a p-value (discussed in the next
> section). 5. If the sample data is inconsistent with the null hypothesis, then the decision is to “reject the null
> hypothesis.” If the sample data is consistent with the null hypothesis, then the decision is to “fail to reject
> the null hypothesis.”
>
> The first step in the hypothesis testing process is to write what is a called a “null” hypothesis and an
> “alternative” hypothesis. These hypotheses will be statements regarding an unknown population parameter,
> such as a population mean or a population proportion. These two hypotheses are based on the claim under
> study and will be written as complementary statements to each other. When one of the hypotheses is true, the
> other hypothesis must be false (since they are complements of one another). Note that either the null or
> alternative hypothesis can represent the claim.
>
> The null hypothesis is labeled as
>  and is a statement of equality—for example, the null hypothesis might
> state that the mean time to complete an exam is 42 minutes. For this example, the null hypothesis would be
> written as:
>
> Where the notation  refers to the population mean time to complete an exam. The null hypothesis will always contain one of the following three symbols:
> .

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-007-pool-016

**Chunk:** `openstax_intro_stats_2e:6.2:chunk-008`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 6: The Normal Distribution
> Section 6.2: Using the Normal Distribution
>
> TRY IT 6.10
>
> Use the information in Example 6.10 to answer the following questions.
>
> a. Find the 30th percentile, and interpret it in a complete sentence.
> b. What is the probability that the age of a randomly selected smartphone user in the range 13 to 55+ is less than
>
> 27 years old.
>
> EXAMPLE 6.11
>
> In the United States the ages 13 to 55+ of smartphone users approximately follow a normal distribution with
> approximate mean and standard deviation of 36.9 years and 13.9 years respectively. Using this information, answer the
> following questions (round answers to one decimal place).
>
> Problem
> a. Calculate the interquartile range (IQR).
>
> b. Forty percent of the smartphone users from 13 to 55+ are at least what age?
>
> Solution
> a.
>
> IQR = Q3 – Q1
> Calculate Q3 = 75th percentile and Q1 = 25th percentile.
> invNorm(0.75,36.9,13.9) = Q3 = 46.2754
> invNorm(0.25,36.9,13.9) = Q1 = 27.5246
> IQR = Q3 – Q1 = 18.8
>
> b.
>
> Find k where P(x ≥ k) = 0.40 ("At least" translates to "greater than or equal to.")
> 0.40 = the area to the right. Area to the left = 1 – 0.40 = 0.60. The area to the left of k = 0.60.
>
> invNorm(0.60,36.9,13.9) = 40.4215.
> k = 40.4. Forty percent of the smartphone users from 13 to 55+ are at least 40.4 years.
>
> TRY IT 6.11
>
> Two thousand students took an exam. The scores on the exam have an approximate normal distribution with a mean
> μ = 81 points and standard deviation σ = 15 points.
>
> a. Calculate the first- and third-quartile scores for this exam.
> b. The middle 50% of the exam scores are between what two values?
>
> EXAMPLE 6.12

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-008

**Pregunta:** Why does the standard error of the sample mean increase as the sample size becomes larger?

**Respondibilidad de referencia:** unanswerable

### q-v1-008-pool-001

**Chunk:** `openstax_intro_stats_2e:7.intro:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 7: The Central Limit Theorem
> Section 7.intro: Introduction
>
> The second alternative says that if we again
> collect samples of size n that are "large enough," calculate the sum of each sample and create a histogram, then the
> resulting histogram will again tend to have a normal bell-shape.
>
> The size of the sample, n, that is required in order to be "large enough" depends on the original population from which
> the samples are drawn (the sample size should be at least 30 or the data should come from a normal distribution). If the
> original population is far from normal, then more observations are needed for the sample means or sums to be normal. Sampling is done with replacement.
>
> It would be difficult to overstate the importance of the central limit theorem in statistical theory. Knowing that data, even
> if its distribution is not normal, behaves in a predictable way is a powerful tool.
>
> COLLABORATIVE EXERCISE
>
> Suppose eight of you roll one fair die ten times, seven of you roll two fair dice ten times, nine of you roll five fair dice
> ten times, and 11 of you roll ten fair dice ten times.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-008-pool-002

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-011`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> Figure 8.5
>
> Summary: Effect of Changing the Confidence Level
>
> • Increasing the confidence level increases the error bound, making the confidence interval wider.
> • Decreasing the confidence level decreases the error bound, making the confidence interval narrower.
>
> TRY IT 8.4
>
> Refer back to the pizza-delivery Try It exercise. The population standard deviation is six minutes and the sample mean
> deliver time is 36 minutes. Use a sample size of 20. Find a 95% confidence interval estimate for the true mean pizza
> delivery time.
>
> EXAMPLE 8.5
>
> Suppose we change the original problem in Example 8.2 to see what happens to the error bound if the sample size is
> changed.
>
> Problem
> Leave everything the same except the sample size. Use the original 90% confidence level. What happens to the error
> bound and the confidence interval if we increase the sample size and use n = 100 instead of n = 36? What happens if we
>
> decrease the sample size to n = 25 instead of n = 36?
>
> •
>  = 68
>
> • EBM =
>
> • σ = 3; The confidence level is 90% (CL=0.90);
>  = z0.05 = 1.645.
>
> Solution
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
>
> TRY IT 8.5
>
> Refer back to the pizza-delivery Try It exercise.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-008-pool-003

**Chunk:** `openstax_intro_stats_2e:8.4:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.4: Confidence Interval (Home Costs)
>
> c. n = _____
>
> 2. In words, define the random variable
> . 3. State the estimated distribution to use. Use both words and symbols.
>
> Find the Confidence Interval
>
> 1. Calculate the confidence interval and the error bound.
> a. Confidence Interval: _____
> b. Error Bound: _____
>
> 2. How much area is in both tails (combined)? α = _____
> 3. How much area is in each tail?
>  = _____
>
> 4. Fill in the blanks on the graph with the area in each section. Then, fill in the number line with the upper and lower
> limits of the confidence interval and the sample mean.
>
> Figure 8.6
>
> 5. Some students think that a 90% confidence interval contains 90% of the data. Use the list of data on the first page
> and count how many of the data values lie within the confidence interval. What percent is this? Is this percent close
> to 90%? Explain why this percent should or should not be close to 90%.
>
> Describe the Confidence Interval
>
> 1. In two to three complete sentences, explain what a confidence interval means (in general), as if you were talking to
> someone who has not taken statistics. 2. In one to two complete sentences, explain what this confidence interval means for this particular study.
>
> Use the Data to Construct Confidence Intervals
>
> 1. Using the given information, construct a confidence interval for each confidence level given.
>
> Confidence level
> EBM/Error Bound
> Confidence Interval
>
> 50%
>
> 80%
>
> 95%
>
> 99%
>
> Table 8.6
>
> 2. What happens to the EBM as the confidence level increases? Does the width of the confidence interval increase or
> decrease? Explain why this happens.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-008-pool-004

**Chunk:** `openstax_principles_ds:4.1:chunk-017`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Too large of a sample size can result in wasted resources if a smaller sample
> size would be sufficient. Sampling is covered in some depth in Handling Large Datasets. Here, we review
> methods to determine minimum sample size requirements when constructing confidence intervals for means
> or proportions. Note that the desired margin of error plays a key role in this sample size determination.
>
> Sample Size for Confidence Interval for the Mean
>
> When determining a confidence interval for a mean, a researcher can use the margin of error formula for the
> mean; solving this formula algebraically for the sample size ( ), the following minimum sample size formula
> can be used to determine the minimum sample size needed to achieve a certain margin of error:
>
> Sample size formula for confidence interval for mean:
>
> Where:
>
> is the critical value of the normal distribution.
>  is the population standard deviation.
>
> is the desired margin of error.
>
> Note that for sample size calculations, sample size results are rounded up to the next higher whole number.
>
> For example, if the formula previously shown results in a sample size of 59.2, then the sample size will be
> rounded to 60.
>
> EXAMPLE 4.6
>
> Problem
>
> A benefits analyst is interested in a 90% confidence interval for the mean salary for chemical engineers. What sample size should the analyst use if a margin of error of $1,000 is desired? Assume a population
> standard deviation of $8,000.
>
> Solution
>
> For a 90% confidence interval, the corresponding critical value is
> . The population standard
> deviation is given as $8,000, and the margin of error is given as $1,000.
>
> Using the sample size formula:
>
> Round to the next higher whole number, so the desired sample size is 174.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-008-pool-005

**Chunk:** `openstax_intro_stats_2e:7.3:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 7: The Central Limit Theorem
> Section 7.3: Using the Central Limit Theorem
>
> P(Σx ≥ 600) = normalcdf(600,E99,(70)(8.2),
> (1)) = 0.0009
>
> TRY IT 7.7
>
> The mean number of minutes for app engagement by a table use is 8.2 minutes. Suppose the standard deviation is
> one minute. Take a sample size of 70.
>
> a. What is the probability that the sum of the sample is between seven hours and ten hours? What does this mean
>
> in context of the problem?
> b. Find the 84th and 16th percentiles for the sum of the sample. Interpret these values in context.
>
> 7.3 Using the Central Limit Theorem
>
> It is important for you to understand when to use the central limit theorem. If you are being asked to find the
> probability of the mean, use the clt for the mean. If you are being asked to find the probability of a sum or total, use the
> clt for sums. This also applies to percentiles for means and sums.
>
> NOTE
>
> If you are being asked to find the probability of an individual value, do not use the clt. Use the distribution of its
> random variable.
>
> Examples of the Central Limit Theorem
>
> Law of Large Numbers
> The law of large numbers says that if you take samples of larger and larger size from any population, then the mean
> of the sample tends to get closer and closer to μ. From the central limit theorem, we know that as n gets larger and
> larger, the sample means follow a normal distribution. The larger n gets, the smaller the standard deviation gets.
> (Remember that the standard deviation for
>  is
> .) This means that the sample mean  must be close to the
>
> population mean μ. We can say that μ is the value that the sample means approach as n gets larger. The central limit
> theorem illustrates the law of large numbers.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-008-pool-006

**Chunk:** `openstax_principles_ds:4.1:chunk-011`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> The wider the net used, the higher the probability of
> catching a fish.
>
> You might notice that the sample size  is located in the denominator of the formula for margin of error. This indicates that as the sample size increases, the margin of error will decrease, which will then result in a
> narrower confidence interval. On the other hand, as the sample size decreases, the margin of error
> increases and the confidence interval becomes wider.
>
> Confidence Interval for the Mean When the Population Standard Deviation Is
> Unknown
>
> A confidence interval can still be determined when the population standard deviation is unknown by
> calculating a sample standard deviation based on the sample data. This is actually the more common
> application of confidence intervals.
>
> Here are the conditions required to use this procedure:
>
> a. A random sample is selected from the population.
> b. The sample size is at least 30, or the underlying population is known to follow a normal distribution.
>
> c. The population standard deviation ( ) is unknown; the sample standard deviation
>  can be calculated.
>
> Once these requirements are met, the margin of error (E) is calculated according to the following formula:
>
> is called the critical value of the t-distribution. The t-distribution is a bell-shaped, symmetric distribution
> similar to the normal distribution, though the t-distribution has “thicker tails” as compared to the normal
> distribution. The comparison of the normal and t-distribution curves is shown in Figure 4.3.
>
> Figure 4.3 Comparison of t-Distribution and Normal Distribution Curves
>
> The t-distribution is actually a family of curves, determined by a parameter called degrees of freedom (df),
> where df is equal to
> . The critical value
>  is similar to a z-score and specifies the area under the t-
> distribution curve corresponding to the confidence level between
>  and
> .

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-008-pool-007

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-012`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> When n = 25: EBM =
>  = (1.645)
>  = 0.987.
>
> Summary: Effect of Changing the Sample Size
>
> • Increasing the sample size causes the error bound to decrease, making the confidence interval narrower.
> • Decreasing the sample size causes the error bound to increase, making the confidence interval wider.
>
> TRY IT 8.5
>
> Refer back to the pizza-delivery Try It exercise. The mean delivery time is 36 minutes and the population standard
> deviation is six minutes. Assume the sample size is changed to 50 restaurants with the same sample mean. Find a
> 90% confidence interval estimate for the population mean delivery time.
>
> Working Backwards to Find the Error Bound or Sample Mean
>
> When we calculate a confidence interval, we find the sample mean, calculate the error bound, and use them to calculate
> the confidence interval. However, sometimes when we read statistical studies, the study may state the confidence
> interval only. If we know the confidence interval, we can work backwards to find both the error bound and the sample
> mean.
>
> Finding the Error Bound
>
> • From the upper value for the interval, subtract the sample mean,
> • OR, from the upper value for the interval, subtract the lower value. Then divide the difference by two.
>
> Finding the Sample Mean
>
> • Subtract the error bound from the upper value of the confidence interval,
> • OR, average the upper and lower endpoints of the confidence interval.
>
> Notice that there are two methods to perform each calculation. You can choose the method that is easier to use with the
> information you know.
>
> EXAMPLE 8.6
>
> Suppose we know that a confidence interval is (67.18, 68.82) and we want to find the error bound.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-008-pool-008

**Chunk:** `openstax_intro_stats_2e:9.4:chunk-004`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.4: Rare Events, the Sample, Decision and Conclusion
>
> To persuade his customers that he is right, the baker decides to do a hypothesis test. He bakes 10 loaves of bread. The mean height of the sample loaves is 17 cm. The baker knows from baking hundreds of loaves of bread that the
> standard deviation for the height is 0.5 cm. and the distribution of heights is normal.
>
> The null hypothesis could be H0: μ ≤ 15 The alternate hypothesis is Ha: μ > 15
>
> The words "is more than" translates as a ">" so "μ > 15" goes into the alternate hypothesis. The null hypothesis must
> contradict the alternate hypothesis.
>
> By the Central Limit Theorem, the distribution of sample means, for samples of 10 loaves, will be normal with mean μ =
> 15 and standard deviation
> .
>
> Suppose the null hypothesis is true (the mean height of the loaves is no more than 15 cm). Then is the mean height (17
> cm) calculated from the sample unexpectedly large? The hypothesis test works by asking the question how unlikely the
> sample mean would be if the null hypothesis were true. The graph shows how far out the sample mean is on the normal
> curve. The p-value is the probability that, if we were to take other samples, any other sample mean would fall at least as
> far out as 17 cm.
>
> The p-value, then, is the probability that a sample mean is the same or greater than 17 cm. when the population
> mean is, in fact, 15 cm. We can calculate this probability using the normal distribution for means.
>
> Figure 9.2
>
> p-value= P( > 17) which is approximately zero.
>
> A p-value of approximately zero tells us that it is highly unlikely that a loaf of bread rises no more than 15 cm, on
> average.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-008-pool-009

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> Use n = 217: Always round the answer UP to the next higher integer to ensure that the sample size is large enough.
>
> Therefore, 217 Foothill College students should be surveyed in order to be 95% confident that we are within two years of
> the true population mean age of Foothill College students.
>
> TRY IT 8.7
>
> The population standard deviation for the height of high school basketball players is three inches. If we want to be
> 95% confident that the sample mean height is within one inch of the true population mean height, how many
> randomly selected students must be surveyed?
>
> 8.2 A Single Population Mean using the Student t Distribution
>
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

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-008-pool-010

**Chunk:** `openstax_intro_stats_2e:8.6:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.6: Confidence Interval (Women's Heights)
>
> Confidence level
> EBP/Error Bound
> Confidence Interval
>
> 95%
>
> 99%
>
> Table 8.7
>
> 4. What happens to the EBP as the confidence level increases? Does the width of the confidence interval increase or
> decrease? Explain why this happens.
>
> 8.6 Confidence Interval (Women's Heights)
>
> Stats Lab
>
> Confidence Interval (Women's Heights)
> Class Time:
>
> Names:
>
> Student Learning Outcomes
>
> • The student will calculate a 90% confidence interval using the given data.
> • The student will determine the relationship between the confidence level and the percentage of constructed
> intervals that contain the population mean.
>
> Given:
>
> 59.4
> 71.6
> 69.3
> 65.0
> 62.9
> 66.5
> 61.7
> 55.2
>
> 67.5
> 67.2
> 63.8
> 62.9
> 63.0
> 63.9
> 68.7
> 65.5
>
> 61.9
> 69.6
> 58.7
> 63.4
> 61.8
> 60.6
> 69.8
> 60.0
>
> 64.9
> 66.1
> 66.8
> 60.6
> 65.6
> 63.8
> 61.3
> 59.2
>
> 64.1
> 59.3
> 64.9
> 62.4
> 63.5
> 60.9
> 63.3
> 66.3
>
> 61.5
> 64.3
> 62.9
> 60.6
> 63.8
> 58.8
> 64.9
> 65.7
>
> 62.5
> 70.9
> 62.9
> 63.1
> 62.2
> 58.7
> 64.7
> 66.0
>
> 60.5
> 64.7
> 65.4
> 60.2
> 65.0
> 64.1
> 61.1
> 65.3
>
> 64.6
> 59.2
> 61.4
> 62.0
> 63.5
> 61.4
> 65.5
> 62.3
>
> 65.5
> 64.7
> 58.8
> 66.1
> 64.9
> 66.9
> 57.9
> 69.8
>
> 58.5
> 63.4
> 69.2
> 65.9
> 62.2
> 60.0
> 58.1
> 62.5
>
> Table 8.8 Heights of 100 Women (in Inches)
>
> 62.4
> 59.1
> 66.4
> 61.2
> 60.4
> 58.7
> 66.7
> 67.5
>
> 63.2
> 56.6
> 67.7
> 62.5
>
> Table 8.8 Heights of 100 Women (in Inches)
>
> 1. Table 8.8 lists the heights of 100 women. Use a random number generator to select ten data values randomly. 2. Calculate the sample mean and the sample standard deviation. Assume that the population standard deviation is
> known to be 3.3 inches. With these values, construct a 90% confidence interval for your sample of ten values. Write
> the confidence interval you obtained in the first space of Table 8.9. 3. Now write your confidence interval on the board. As others in the class write their confidence intervals on the board,
> copy them into Table 8.9.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-008-pool-011

**Chunk:** `openstax_intro_stats_2e:7.1:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 7: The Central Limit Theorem
> Section 7.1: The Central Limit Theorem for Sample Means (Averages)
>
> 1. The mean of the sample means remains approximately the same. 2. The spread of the sample means (the standard deviation of the sample means) gets smaller. 3. The graph appears steeper and thinner.
>
> You have just demonstrated the central limit theorem (clt).
>
> The central limit theorem tells you that as you increase the number of dice, the sample means tend toward a
> normal distribution (the sampling distribution).
>
> 7.1 The Central Limit Theorem for Sample Means (Averages)
>
> Suppose X is a random variable with a distribution that may be known or unknown (it can be any distribution). Using a
> subscript that matches the random variable, suppose:
>
> a. μX = the mean of X
> b. σX = the standard deviation of X
>
> If you draw random samples of size n, then as n increases, the random variable  which consists of sample means, tends
> to be normally distributed and
>
> The central limit theorem for sample means says that if you repeatedly draw samples of a given size (such as
> repeatedly rolling ten dice) and calculate their means, those means tend to follow a normal distribution (the sampling
> distribution). As sample sizes increase, the distribution of means more closely follows the normal distribution. The
> normal distribution has the same mean as the original distribution and a variance that equals the original variance
> divided by the sample size. Standard deviation is the square root of variance, so the standard deviation of the sampling
> distribution is the standard deviation of the original distribution divided by the square root of n. The variable n is the
> number of values that are averaged together, not the number of times the experiment is done.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-008-pool-012

**Chunk:** `openstax_principles_ds:4.1:chunk-026`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Calculate confidence interval for
> a proportion (uses normal
> distribution).
>
> proportion_confint()
> proportion_confint(success,
> sample_size,
> 1 – confidence_level)
>
> Table 4.5 Python Functions for Confidence Intervals
>
> EXAMPLE 4.9
>
> Problem
>
> Repeat Example 4.3 to calculate a 90% confidence interval, but use Python functions to calculate the
> confidence interval.
>
> Recall from Example 4.3, the sample mean is 12.5 hours with a population standard deviation of 6.3 hours. The sample size is 50 students, and we are interested in calculating a 90% confidence interval.
>
> Solution
>
> Use the Python function norm.interval() as shown:
>
> PYTHON CODE
>
> import scipy.stats as stats
> import numpy as np
> import math
>
> # Enter sample mean, population standard deviation and sample size
> sample_mean = 12.5
> population_standard_deviation = 6.3
> sample_size = 50
>
> # Confidence level
> confidence_level = 0.90
>
> # standard error
> standard_error = population_standard_deviation / math.sqrt(sample_size)
>
> # Calculate confidence interval using norm.interval function
> stats.norm.interval(confidence_level, sample_mean, standard_error)
>
> The resulting output will look like this:
>
> (11.03451018636739, 13.965489813632608)
>
> EXAMPLE 4.10
>
> Problem
>
> Repeat Example 4.4 to calculate a 99% confidence interval, but use Python functions to calculate the
> confidence interval.
>
> Recall from Example 4.4, the sample mean is 15.8 miles with a standard deviation of 3.2 miles. The sample
> size is 26 employees, and we are interested in calculating a 99% confidence interval.
>
> Solution
>
> Use the Python function t.interval() as shown:
>
> PYTHON CODE
>
> # Enter sample mean, sample standard deviation, and sample size
> sample_mean = 15.8
> sample_standard_deviation = 3.2
> sample_size = 26
>
> # Degrees of freedom (sample size - 1)
> degrees_of_freedom = sample_size - 1
>
> # Confidence level
> confidence_level = 0.99
>
> # standard error
> standard_error = sample_standard_deviation / math.sqrt(sample_size)

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-008-pool-013

**Chunk:** `openstax_principles_ds:4.1:chunk-018`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Assume a population
> standard deviation of $8,000.
>
> Solution
>
> For a 90% confidence interval, the corresponding critical value is
> . The population standard
> deviation is given as $8,000, and the margin of error is given as $1,000.
>
> Using the sample size formula:
>
> Round to the next higher whole number, so the desired sample size is 174.
>
> The analyst should target a sample size of 174 chemical engineers for a salary-related survey in order to
> them calculate a 90% confidence interval for the mean salary of chemical engineers.
>
> Sample Size for Confidence interval for a Proportion
>
> In Example 4.5, how would the researcher know the optimal sample size to use to collect sample data on the
> proportion of adults who are smokers? The margin of error formula can be used to derive the sample size for a
> proportion as follows:
>
> Where:
>
> is the critical value of the normal distribution.
>  is the sample proportion.
>
> is the desired margin of error.
>
> Notice in this formula, it’s assumed that some prior estimate for the sample proportion  is available, perhaps
> from historical data or previous studies. If a prior estimate for the sample proportion is not available, then use
> the value of 0.5 for .
>
> DETERMINING SAMPLE SIZE
>
> When determining sample size needed for a confidence interval for a proportion:
>
> If a prior estimate for the sample proportion is available, then that prior estimate should be utilized.
>
> • If a prior estimate for the sample proportion is not available, then use
> .
>
> EXAMPLE 4.7
>
> Problem
>
> Political candidate Smith is planning a survey to determine a 95% confidence interval for the proportion of
> voters who plan to vote for Smith. How many people should be surveyed? Assume a margin of error is 3%.
>
> a.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-008-pool-014

**Chunk:** `openstax_principles_ds:3.2:chunk-004`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.2: Measures of Variation
>
> The more the individual data values differ from the mean, the larger the variance.
>
> A financial advisor might use variance to determine the volatility of an investment and therefore help guide
> financial decisions. For example, a more cautious investor might opt for investments with low volatility.
>
> The formula used to calculate variance also depends on whether the data is collected from a sample or a
>
> population. The notation
>  is used to represent the sample variance, and the notation
>  is used to represent
> the population variance.
>
> Formula for the sample variance:
>
> Formula for the population variance:
>
> In these formulas:
>
> represents the individual data values
>  represents the sample mean
>  represents the sample size
>  represents the population mean
>
> represents the population size
>
> ALTERNATE FORMULA FOR VARIANCE
>
> An alternate formula for the variance is available. It is sometimes used for more efficient computations:
>
> In the formulas for sample variance and population variance, notice the denominator for the sample variance
> is
> , whereas the denominator for the population variance is
> . The use of
>  in the denominator of the
> sample variance is used to provide the best estimate for the population variance, in the sense that if repeated
> samples of size  are taken and the sample mean computed each time, then the average of those sample
> means will tend to the population mean as the number of repeated samples increase.
>
> It is important to note that in many data science applications, population data is unavailable, and so we
> typically calculate the sample variance. For example, if a researcher wanted to estimate the percentage of
> smokers for all adults in the United States, it would be impractical to collect data from every adult in the United
> States.
>
> Notice that the sample variance is a sum of squares.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-008-pool-015

**Chunk:** `openstax_principles_ds:4.1:chunk-010`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> The margin of error is calculated as follows:
>
> The 90% confidence interval is calculated as follows:
>
> Concluding statement:
>
> The college professor can forecast with 90% confident that the mean amount of time spent on homework
> assignments in a future semester is the interval from 11.03 to 13.97 hours per week.
>
> Calculation for 95% Confidence Interval
>
> For a 95% confidence interval, the corresponding critical value is
> .
>
> The margin of error is calculated as follows:
>
> The 95% confidence interval is calculated as follows:
>
> Concluding statement:
>
> The college professor can forecast with 95% confident that the mean amount of time spent on homework
> assignments in a future semester is the interval from 10.75 to 14.25 hours per week.
>
> Comparison of 90% and 95% confidence intervals:
>
> The 90% confidence interval extends from 11.03 to 13.97. The 95% confidence interval extends from 10.75 to 14.25.
>
> Notice that the 95% confidence interval is wider. If the confidence level is increased, with all other
>
> parameters held constant, we should expect that the confidence interval will become wider. Another way to
> consider this: the wider the confidence interval, the more likely the interval is to contain the true population
> mean. This makes intuitive sense in that if you want to be more certain that the true value of the parameter
> is within an interval, then the interval needs to be wider to account for a larger range of potential values. As
> an analogy, consider a person trying to catch a fish. The wider the net used, the higher the probability of
> catching a fish.
>
> You might notice that the sample size  is located in the denominator of the formula for margin of error. This indicates that as the sample size increases, the margin of error will decrease, which will then result in a
> narrower confidence interval.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-008-pool-016

**Chunk:** `openstax_intro_stats_2e:7.1:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 7: The Central Limit Theorem
> Section 7.1: The Central Limit Theorem for Sample Means (Averages)
>
> Each time a person rolls more than one die, they calculate the sample mean of the faces showing. For example, one
> person might roll five fair dice and get 2, 2, 3, 4, 6 on one roll.
>
> The mean is
>  = 3.4. The 3.4 is one mean when five fair dice are rolled. This same person would roll the
>
> five dice nine more times and calculate nine more means for a total of ten means.
>
> Your instructor will pass out the dice to several people. Roll your dice ten times. For each roll, record the faces, and
> find the mean. Round to the nearest 0.5.
>
> Your instructor (and possibly you) will produce one graph (it might be a histogram) for one die, one graph for two
> dice, one graph for five dice, and one graph for ten dice. Since the "mean" when you roll one die is just the face on the
> die, what distribution do these means appear to be representing?
>
> Draw the graph for the means using two dice. Do the sample means show any kind of pattern?
>
> Draw the graph for the means using five dice. Do you see any pattern emerging?
>
> Finally, draw the graph for the means using ten dice. Do you see any pattern to the graph? What can you conclude
> as you increase the number of dice?
>
> As the number of dice rolled increases from one to two to five to ten, the following is happening:
>
> 1. The mean of the sample means remains approximately the same. 2. The spread of the sample means (the standard deviation of the sample means) gets smaller. 3. The graph appears steeper and thinner.
>
> You have just demonstrated the central limit theorem (clt).

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-008-pool-017

**Chunk:** `openstax_principles_ds:4.2:chunk-001`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> # Calculate confidence interval using t.interval function
> t.interval(confidence_level, degrees_of_freedom, sample_mean, standard_error)
>
> The resulting output will look like this:
>
> (14.050684356083625, 17.549315643916376)
>
> 4.2 Hypothesis Testing
>
> Learning Outcomes
> By the end of this section, you should be able to:
>
> • 4.2.1 Apply hypothesis testing methods to test statistical claims involving one sample.
> • 4.2.2 Use Python to assist with hypothesis testing calculations.
> • 4.2.3 Conduct hypothesis tests to compare two means, two proportions, and matched pairs data.
>
> Constructing confidence intervals is one method used to estimate population parameters. Another important
> statistical method to test claims regarding population parameters is called hypothesis testing.
>
> Hypothesis testing is an important tool for data scientists in that it is used to draw conclusions using sample
> data, and it is also used to quantify uncertainty associated with these conclusions.
>
> As an example to illustrate the use of hypothesis testing in a data science applications, consider an online
> retailer seeking to increase revenue though a text messaging ad campaign. The retailer is interested in
> examining the hypothesis that a text messaging ad campaign leads to a corresponding increase in revenue. To
> test out the hypothesis, the retailer sends out targeted text messages to certain customers but does not send
> the text messages to another group of customers. The retailer then collects data for purchases made by
> customers who received the text message ads versus customers who did not receive the ads. Using hypothesis
> testing methods, the online retailer can come to a conclusion regarding the marketing campaign to transmit
> ads via text messaging. Hypothesis testing involves setting up a null hypothesis and alternative hypotheses
> based on a claim to be tested and then collecting sample data.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-009

**Pregunta:** How do Pearson correlation and Spearman rank correlation differ in their assumptions and sensitivity to outliers?

**Respondibilidad de referencia:** unanswerable

### q-v1-009-pool-001

**Chunk:** `openstax_principles_ds:4.3:chunk-006`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> A more precise assessment of the correlation between the two quantities can be obtained by
> calculating the numeric correlation coefficient (referred to using the symbol ).
>
> The correlation coefficient is a measure of the strength and direction of the correlation between the
> independent variable  and the dependent variable .
>
> The formula for  is shown; however, software is typically used to calculate the correlation coefficient.
>
> where  refers to the number of data pairs and the symbol
>  indicates to sum the x-values.
>
> Note that this value of “ ” is sometimes referred to as the “Pearson correlation coefficient.”
>
> Table 4.15 provides a step-by-step procedure on how to calculate the correlation coefficient .
>
> Step
> Representation in Symbols
>
> 1. Calculate the sum of the x-values.
>
> 2. Calculate the sum of the y-values.
>
> 3. Multiply each x-value by the corresponding
> y-value and calculate the sum of these
>  products.
>
> 4. Square each x-value and then calculate the sum
> of these squared values.
>
> 5. Square each y-value and then calculate the sum
> of these squared values.
>
> n
>
> 6. Determine the value of , which is the number of
> data pairs.
>
> 7. Use these results to then substitute into the
> formula for the correlation coefficient.
>
> Table 4.15 Steps for Calculating the Correlation Coefficient
>
> Note that since  is calculated using sample data,  is considered a sample statistic and is used to measure the
> strength of the correlation for the two population variables. Recall that sample data indicates data based on a
> subset of the entire population.
>
> As mentioned, given the complexity of this calculation, software is typically used to calculate the correlation
> coefficient. There are several options for calculating the correlation coefficient in Python. The example shown
> uses the scipy.stats library in Python which includes the function pearsonr() for calculating the Pearson
>
> correlation coefficient ( ).

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-009-pool-002

**Chunk:** `openstax_principles_ds:4.3:chunk-007`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> As mentioned, given the complexity of this calculation, software is typically used to calculate the correlation
> coefficient. There are several options for calculating the correlation coefficient in Python. The example shown
> uses the scipy.stats library in Python which includes the function pearsonr() for calculating the Pearson
>
> correlation coefficient ( ).
>
> We will create two numerical arrays in Python using the np.array() function and then use the pearsonr()
>
> function to calculate the Pearson correlation coefficient for the
>  data shown in Table 4.15.
>
> The following Python code provides the correlation coefficient for the Nike Stock Price dataset as 0.923.
>
> PYTHON CODE
>
> # import libraries
> import numpy as np
> from scipy.stats  import pearsonr
>  
> # establish x and y data, x-data is S&P500 value, y-data is Nike Stock Price
>
> SP500 = np.array([2912.43, 3044.31, 3100.29, 3271.12, 3500.31, 3363.00, 3269.96,
> 3621.63, 3756.07, 3714.24, 3811.15, 3943.34])
>
> Nike = np.array([87.18, 98.58, 98.05, 97.61, 111.89, 125.54, 120.08, 134.70,
> 141.47, 133.59, 134.78, 140.45])
>
> #pearson r returns both value of r and corresponding p-value
>
> r, p = pearsonr(SP500, Nike)
>
> #print value of r , rounded to 3 decimal places
>
> print("Correlation coefficient: ", round(r, 3))
>
> The resulting output will look like this:
>
> Correlation coefficient: 0.923
>
> Interpret a Correlation Coefficient
>
> Once the value of  is calculated, this measurement provides two indicators for the correlation:
>
> a. the strength of the correlation based on the value of
> b. the direction of the correlation based on the sign of
>
> The value of  gives us this information:
>
> • The value of  is always between
>  and
> :
> .
> • The size of the correlation  indicates the strength of the linear relationship between the two variables.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-009-pool-003

**Chunk:** `openstax_principles_ds:4.3:chunk-021`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> #pearson r returns both value of r and corresponding p-value
> r, p = pearsonr(x, y)
>
> #print value of r, rounded to 3 decimal places
>
> print("Correlation coefficient: ", round(r, 3))
>
> The resulting output will look like this:
>
> Correlation coefficient: 0.981
> This value of
>  indicates a strong, positive correlation between
> advertising spend and revenue.
>
> c. When using a level of significance of 0.05, if
> , then this implies that the correlation between
>
> the two variables demonstrates a linear relationship that is statistically significant at approximately the
>
> 0.05 level of significance. In this example, we check if
>  is greater than or equal to
>  where
>
> . Since
>  is approximately 0.577, this indicates that the r-value of 0.981 is greater than
> ,
>
> and thus the correlation is deemed significant.
> d. The linear regression model will be of the form:
>
> To determine the slope and y-intercept of the regression model, the Python function linregress()
>
> can be used. This function takes the  and  data as inputs and provides the slope and intercept as well as other
> regression-related output.
>
> Here is the Python code to generate the slope and y-intercept of the best-fit line:
>
> PYTHON CODE
>
> # import libraries
> import numpy as np
> from scipy.stats  import linregress
>
> # define the x-data, which is amount spent on advertising
> x = [49, 145, 57, 153, 92, 83, 117, 142, 69, 106, 109, 121]
>
> # define the y-data, which is revenue
> y = [12210, 17590, 13215, 19200, 14600, 14100, 17100, 18400, 14100, 15500, 16300,
> 17020]
>
> #pearson r returns both value of r and corresponding p-value
> slope, intercept, r_value, p_value, std_err  = linregress(x, y)
>
> print ("slope  =", slope)
> print("intercept = ", intercept)
>
> The resulting output will look like this:
>
> slope = 61.79775818816664
> intercept = 9376.698881009072
>
> Based on this Python equation, the regression equation can be written as

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-009-pool-004

**Chunk:** `openstax_principles_ds:3.3:chunk-005`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.3: Measures of Position
>
> Quartiles and the IQR can be used to flag possible outliers in a dataset. For example, if most employees at a
> company earn about $50,000 and the CEO of the company earns $2.5 million, then we consider the CEO’s
> salary to be an outlier data value because this salary is significantly different from all the other salaries in the
> dataset. An outlier data value can also be a value much lower than the other data values in a dataset, so if one
> employee only makes $15,000, then this employee’s low salary might also be considered an outlier.
>
> To detect outliers, you can use the quartiles and the IQR to calculate a lower and an upper bound for outliers. Then any data values below the lower bound or above the upper bound will be flagged as outliers. These data
> values should be further investigated to determine the nature of the outlier condition and whether the data
> values are valid or not.
>
> To calculate the lower and upper bounds for outliers, use the following formulas:
>
> These formulas typically use 1.5 as a cutoff value to identify outliers in a dataset.
>
> EXAMPLE 3.12
>
> Problem
>
> Calculate the IQR for the following 13 home prices and determine if any of the home prices values are
> potential outliers. Data values are in US dollars.
>
> 389950, 230500, 158000, 479000, 639000, 114950, 5500000, 387000, 659000, 529000, 575000, 488800,
> 1095000
>
> Solution
>
> Order the data from smallest to largest.
>
> 114950, 158000, 230500, 387000, 389950, 479000, 488800, 529000, 575000, 639000, 659000, 1095000,
> 5500000
>
> First, determine the median of the dataset. There are 13 data values, so the median is the middle data
> value, which is 488,800.
>
> Next, calculate the
>  and
> .
>
> For the first quartile, look at the data values below the median.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-009-pool-005

**Chunk:** `openstax_principles_ds:4.3:chunk-017`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> Assumptions for Linear Regression
>
> Testing the significance of the correlation coefficient requires that certain assumptions about the data are
> satisfied. The premise of this test is that the data are a sample of observed points taken from a larger
> population. We have not examined the entire population because it is not possible or feasible to do so. We are
> examining the sample to draw a conclusion about whether the linear relationship that we see between  and
> data in the sample data provides strong enough evidence that we can conclude that there actually is a linear
> relationship between  and  data in the population.
>
> The regression line equation that we calculate from the sample data gives the best-fit line for our particular
> sample. We want to use this best-fit line for the sample as an estimate of the best-fit line for the population
> (Figure 4.8). Examining the scatterplot and testing the significance of the correlation coefficient helps us
> determine if it is appropriate to do this.
>
> These are the assumptions underlying the test of significance:
>
> 1. There is a linear relationship in the population that models the average value of  for varying values of . In other words, the expected value of  for each particular value lies on a straight line in the population.
> (We do not know the equation for the line for the population. Our regression line from the sample is our
> best estimate of this line in the population.)
> 2. The y-values for any particular x-value are normally distributed about the line. This implies that there are
> more y-values scattered closer to the line than are scattered farther away. Assumption (1) implies that
> these normal distributions are centered on the line: the means of these normal distributions of y-values lie
> on the line. 3.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-009-pool-006

**Chunk:** `openstax_principles_ds:4.3:chunk-008`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> a. the strength of the correlation based on the value of
> b. the direction of the correlation based on the sign of
>
> The value of  gives us this information:
>
> • The value of  is always between
>  and
> :
> .
> • The size of the correlation  indicates the strength of the linear relationship between the two variables. Values of  close to
>  or to
>  indicate a stronger linear relationship.
> • If
> , there is no linear relationship between the two variables (no linear correlation).
> • If
> , there is perfect positive correlation. If
> , there is perfect negative correlation. In both of
> these cases, all the original data points lie on a straight line.
>
> The sign of  gives us this information:
>
> • A positive value of  means that when  increases,  tends to increase, and when  decreases,  tends to
> decrease (positive correlation).
> • A negative value of  means that when  increases,  tends to decrease, and when  decreases,  tends to
> increase (negative correlation).
>
> From the statistical results shown in the Python output, the correlation coefficient  is 0.923, which indicates
> that the relationship between Nike stock and the value of the S&P 500 over this time period represents a
> strong, positive correlation.
>
> Test a Correlation Coefficient for Significance
>
> The correlation coefficient, , tells us about the strength and direction of the linear relationship between  and
>
> . The sample data are used to compute , the correlation coefficient for the sample. If we had data for the
> entire population (that is, all measurements of interest), we could find the population correlation coefficient,
> which is labeled as the Greek letter  (pronounced “rho”). But because we have only sample data, we cannot
> calculate the population correlation coefficient. The sample correlation coefficient, , is our estimate of the
> unknown population correlation coefficient.
>
> •
> •

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-009-pool-007

**Chunk:** `openstax_principles_ds:4.3:chunk-016`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> Using the linear model, when interest rates are at 5%, the model predicts the value of the
> company stock to be $99. Calculate the residual for this data point.
>
> Solution
>
> A residual is the difference between an observed y-value and the predicted y-value obtained from the linear
> regression equation:
>
> The goal in regression analysis is to determine the coefficients  and  in the following regression equation:
>
> Once the
>  has been collected, the slope ( ) and y-intercept ( ) can be calculated using the following
> formulas:
>
> where  refers to the number of data pairs and
>  indicates sum of the x-values.
>
> Notice that the formula for the y-intercept requires the use of the slope result (b), and thus the slope should be
> calculated first, and the y-intercept should be calculated second.
>
> When making predictions for , it is always important to plot a scatter diagram first. If the scatterplot indicates
> that there is a linear relationship between the variables, then it is reasonable to use a best-fit line to make
> predictions for , given  is within the domain of x-values in the sample data, but not necessarily for x-values
> outside that domain.
>
> USING TECHNOLOGY FOR LINEAR REGRESSION
>
> Typically, technology is used to calculate the best-fit linear model as well as calculate correlation coefficients
> and scatterplot. Details of using Python for these calculations are provided in Using Python for Correlation
> and Linear Regression.
>
> Assumptions for Linear Regression
>
> Testing the significance of the correlation coefficient requires that certain assumptions about the data are
> satisfied. The premise of this test is that the data are a sample of observed points taken from a larger
> population. We have not examined the entire population because it is not possible or feasible to do so.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-009-pool-008

**Chunk:** `openstax_principles_ds:4.3:chunk-009`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> If we had data for the
> entire population (that is, all measurements of interest), we could find the population correlation coefficient,
> which is labeled as the Greek letter  (pronounced “rho”). But because we have only sample data, we cannot
> calculate the population correlation coefficient. The sample correlation coefficient, , is our estimate of the
> unknown population correlation coefficient.
>
> •
> •
>
> An important step in the correlation analysis is to determine if the correlation is significant. By this, we are
> asking if the correlation is strong enough to allow meaningful predictions for  based on values of . One
> method to test the significance of the correlation is to employ a hypothesis test. The hypothesis test lets us
> decide whether the value of the population correlation coefficient  is close to zero or significantly different
> from zero. We decide this based on the sample correlation coefficient  and the sample size n.
>
> If the test concludes that the correlation coefficient is significantly different from zero, we say that the
> correlation coefficient is significant.
>
> • Conclusion: There is sufficient evidence to conclude that there is a significant linear relationship between
> the two variables because the correlation coefficient is significantly different from zero.
> • What the conclusion means: There is a significant linear relationship between the two variables. If the test
> concludes that the correlation coefficient is not significantly different from zero (it is close to zero), we say
> that correlation coefficient is not significant.
>
> A hypothesis test can be performed to test if the correlation is significant. A hypothesis test is a statistical
> method that uses sample data to test a claim regarding the value of a population parameter. In this case, the
> hypothesis test will be used to test the claim that the population correlation coefficient  is equal to zero.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-009-pool-009

**Chunk:** `openstax_principles_ds:4.3:chunk-020`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> Scatterplots and Correlation.)
> The Python function plt.scatter() can be used to generate the scatterplot for the
>  data. Note
>
> that we consider advertising to be the independent variable ( -data) and revenue to be the dependent
> variable ( -data) since revenue depends on the amount of advertising.
>
> Here is the Python code to generate the scatterplot:
>
> PYTHON CODE
>
> # import the matplotlib library
> import matplotlib.pyplot as plt
>
> # define the x-data, which is amount spent on advertising
> x = [49, 145, 57, 153, 92, 83, 117, 142, 69, 106, 109, 121]
>
> # define the y-data, which is revenue
> y = [12210, 17590, 13215, 19200, 14600, 14100, 17100, 18400, 14100, 15500, 16300,
> 17020]
>
> # use the scatter function to generate a time series graph
> plt.scatter(x, y)
>
> # Add a title using the title function
> plt.title("Revenue versus Advertising for a Company")
>
> # Add labels to the x and y axes by using xlabel and ylabel functions
> plt.xlabel("Advertising $000")
> plt.ylabel ("Revenue $000")
>
> The resulting output will look like this:
>
> b. The Python function pearsonr() can be used to generate the correlation coefficient, .
>
> Here is the Python code to calculate the correlation coefficient:
>
> PYTHON CODE
>
> # import libraries
> import numpy as np
> from scipy.stats  import pearsonr
>
> # define the x-data, which is amount spent on advertising
> x = [49, 145, 57, 153, 92, 83, 117, 142, 69, 106, 109, 121]
>
> # define the y-data, which is revenue
> y = [12210, 17590, 13215, 19200, 14600, 14100, 17100, 18400, 14100, 15500, 16300,
> 17020]
>
> #pearson r returns both value of r and corresponding p-value
> r, p = pearsonr(x, y)
>
> #print value of r, rounded to 3 decimal places
>
> print("Correlation coefficient: ", round(r, 3))
>
> The resulting output will look like this:
>
> Correlation coefficient: 0.981
> This value of
>  indicates a strong, positive correlation between
> advertising spend and revenue.
>
> c.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-009-pool-010

**Chunk:** `openstax_principles_ds:4.3:chunk-018`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> The y-values for any particular x-value are normally distributed about the line. This implies that there are
> more y-values scattered closer to the line than are scattered farther away. Assumption (1) implies that
> these normal distributions are centered on the line: the means of these normal distributions of y-values lie
> on the line. 3. The standard deviations of the population y-values about the line are equal for each value of . In other
> words, each of these normal distributions of y-values has the same shape and spread about the line. 4. The residual errors are mutually independent (no pattern). 5. The data are produced from a well-designed random sample or randomized experiment.
>
> Figure 4.8 Best-Fit Line. Note that the y-values for each x-value are normally distributed about the line with the same standard
> deviation. For each x-value, the mean of the y-values lies on the regression line. More y-values lie near the line than are scattered
> farther away from the line
>
> Using Python for Correlation and Linear Regression
>
> Once a correlation has been deemed significant, a linear regression model is developed. The goal in the
> regression analysis is to determine the coefficients  and  in the following regression equation:
>
> These formulas can be quite cumbersome, especially for a significant number of data pairs, and thus software
> is often used (such as Excel, Python, or R).
>
> Develop a Linear Regression Model
>
> In the following example, Python will be used for the following analysis based on a given dataset of
>  data.
>
> • Create a scatterplot.
> • Calculate the correlation coefficient.
> • Construct the best-fit linear equation.
> • Predict values of the dependent variable for given values of the independent variable.
>
> There are various ways to accomplish these tasks in Python, but we will use several functions available within
> the scipy library, such as:

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-009-pool-011

**Chunk:** `openstax_principles_ds:4.3:chunk-022`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> #pearson r returns both value of r and corresponding p-value
> slope, intercept, r_value, p_value, std_err  = linregress(x, y)
>
> print ("slope  =", slope)
> print("intercept = ", intercept)
>
> The resulting output will look like this:
>
> slope = 61.79775818816664
> intercept = 9376.698881009072
>
> Based on this Python equation, the regression equation can be written as
>
> where  represents the amount spent on advertising (in thousands of dollars) and  represents the amount
> of revenue (in thousands of dollars).
>
> It is also useful to plot this best-fit line superimposed on the scatterplot to show the strong correlation
> between advertising spend and revenue, as follows (see Figure 4.9):
>
> Figure 4.9 Best-Fit Line Superimposed on the Scatterplot
>
> e. The regression equation is:
> . The given amount of advertising spend of $100 corresponds to a given x-value, so replace “ ” with 100
> in this regression equation to generate a predicted revenue:
>
> Since both advertising and revenue are expressed in thousands of dollars, the conclusion is that if
>
> advertising spend is $100,000, the predicted revenue for the company will be $15,556,700.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-009-pool-012

**Chunk:** `openstax_principles_ds:3.3:chunk-004`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.3: Measures of Position
>
> The upper half of the
> data values are 7.4, 7.5, 7.9, 8.2, 8.7, which are the data values above the median.
>
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
> Quartiles and the IQR can be used to flag possible outliers in a dataset. For example, if most employees at a
> company earn about $50,000 and the CEO of the company earns $2.5 million, then we consider the CEO’s
> salary to be an outlier data value because this salary is significantly different from all the other salaries in the
> dataset.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-009-pool-013

**Chunk:** `openstax_principles_ds:4.3:chunk-002`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> • 4.3.1 Create scatterplots and calculate and interpret correlation coefficients.
> • 4.3.2 Perform linear regression and determine the best-fit linear equation.
> • 4.3.3 Use Python to calculate correlation coefficients and determine equations of linear regression
> models.
>
> We briefly introduced correlation analysis at the beginning of this chapter, but now we want to dig in a little
> deeper. Data scientists are often interested in knowing if there are relationships, or a correlation, between two
> numeric quantities. For example, a medical researcher might be interested in investigating if there is a
> relationship between age and blood pressure. A college professor might be interested to know if there is a
> relationship between time spent on social media by students and corresponding academic grades.
>
> Correlation analysis allows for the determination of a statistical relationship between two numeric quantities,
> or variables—an independent variable and a dependent variable. The independent variable is the variable
> that you can change or control, while the dependent variable is what you measure or observe to see how it
>
> responds to those changes. Regression analysis takes this a step further by quantifying the relationship
> between the two variables, and it can be used to predict one quantity based on a second quantity, assuming
> there is a significant correlation between the two quantities. For example, the value of a car can be predicted
> based on the age of the car.
>
> Earlier we noted many business-related applications where correlation and regression analysis are used. For
> instance, regression analysis can be used to establish a mathematical equation that relates a dependent
> variable (such as sales) to an independent variable (such as advertising expenditure). But it has many
> applications apart from business as well. An automotive engineer is interested in the correlation between
> outside temperature and battery life for an electric vehicle, for instance.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-009-pool-014

**Chunk:** `openstax_principles_ds:4.intro:chunk-001`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.intro: Introduction
>
> Inferential Statistics and Regression Analysis
> 4
>
> Figure 4.1 Inferential statistics is used extensively in data science to draw conclusions about a larger population—and drive decision-
> making. (credit: modification of work “Compiling Health Statistics” by Ernie Branson/Wikimedia Commons, Public Domain)
>
> Chapter Outline
>
> 4.1 Statistical Inference and Confidence Intervals
> 4.2 Hypothesis Testing
> 4.3 Correlation and Linear Regression Analysis
> 4.4 Analysis of Variance (ANOVA)
>
> Introduction
>
> Inferential statistics plays a key role in data science applications, as its techniques allow researchers to infer
> or generalize observations from samples to the larger population from which they were selected. If the
> researcher had access to a full set of population data, then these methods would not be needed. But in most
> real-world scenarios, population data cannot be obtained or is impractical to obtain, making inferential
> analysis essential. This chapter will explore the techniques of inferential statistics and their applications in data
>
> science.
>
> Confidence intervals and hypothesis testing allow a data scientist to formulate conclusions regarding
> population parameters based on sample data.
>
> One technique, correlation analysis, allows the determination of a statistical relationship between two
> numeric quantities, often referred to as variables. A variable is a characteristic or attribute that can be
> measured or observed. A correlation between two variables is said to exist where there is an association
> between them. Finance professionals often use correlation analysis to predict future trends and mitigate risk
> in a stock portfolio. For example, if two investments are strongly correlated, an investor might not want to
> have both investments in a certain portfolio since the two investments would tend to move in the same
> direction as market prices rose or fell. To diversify a portfolio, an investor might seek investments that are not
> strongly correlated with one another.
>
> Regression analysis takes correlation analysis one step further by modeling the relationship between the two
> numeric quantities or variables when a correlation exists. In statistics, modeling refers specifically to the

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-009-pool-015

**Chunk:** `openstax_principles_ds:4.3:chunk-011`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> INTERPRETING THE SIGNIFICANCE OF THE SAMPLE CORRELATION COEFFICIENT
>
> • If  is significant and the scatterplot shows a linear trend, the line can be used to predict the value of
> for values of  that are within the domain of observed x-values.
>
> • If  is not significant OR if the scatterplot does not show a linear trend, the line should not be used for
> prediction.
> • If  is significant and the scatterplot shows a linear trend, the line may not be appropriate or reliable for
> prediction outside the domain of observed x-values in the data.
>
> EXAMPLE 4.22
>
> Problem
>
> Suppose that the chief financial officer (CFO) of a corporation is investigating the correlation between stock
> prices and unemployment rate over a period of 10 years and finds the correlation coefficient to be
> . There are 10
>  data points in the dataset. Should the CFO conclude that the correlation is significant for
> the relationship between stock prices and unemployment rate based on a level of significance of 0.05?
>
> Solution
>
> When using a level of significance of 0.05, if
> , then this implies that the correlation between the
>
> two variables demonstrates a linear relationship that is statistically significant at approximately the 0.05
>
> level of significance. In this example, we check if
>  is greater than or equal to
>  where
> . Since
>
> is approximately 0.632, this indicates that the r-value of
>  is greater than
> , and thus the
>
> correlation is deemed significant.
>
> Linear Regression
>
> A regression model is typically developed once the correlation coefficient has been calculated and a
> determination has been made that the correlation is significant. The regression model can then be used to
> predict one quantity (the dependent variable) based on the other (the independent variable).

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-010

**Pregunta:** How should a Bayesian credible interval for a population mean be computed using a conjugate prior?

**Respondibilidad de referencia:** unanswerable

### q-v1-010-pool-001

**Chunk:** `openstax_principles_ds:4.1:chunk-018`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Assume a population
> standard deviation of $8,000.
>
> Solution
>
> For a 90% confidence interval, the corresponding critical value is
> . The population standard
> deviation is given as $8,000, and the margin of error is given as $1,000.
>
> Using the sample size formula:
>
> Round to the next higher whole number, so the desired sample size is 174.
>
> The analyst should target a sample size of 174 chemical engineers for a salary-related survey in order to
> them calculate a 90% confidence interval for the mean salary of chemical engineers.
>
> Sample Size for Confidence interval for a Proportion
>
> In Example 4.5, how would the researcher know the optimal sample size to use to collect sample data on the
> proportion of adults who are smokers? The margin of error formula can be used to derive the sample size for a
> proportion as follows:
>
> Where:
>
> is the critical value of the normal distribution.
>  is the sample proportion.
>
> is the desired margin of error.
>
> Notice in this formula, it’s assumed that some prior estimate for the sample proportion  is available, perhaps
> from historical data or previous studies. If a prior estimate for the sample proportion is not available, then use
> the value of 0.5 for .
>
> DETERMINING SAMPLE SIZE
>
> When determining sample size needed for a confidence interval for a proportion:
>
> If a prior estimate for the sample proportion is available, then that prior estimate should be utilized.
>
> • If a prior estimate for the sample proportion is not available, then use
> .
>
> EXAMPLE 4.7
>
> Problem
>
> Political candidate Smith is planning a survey to determine a 95% confidence interval for the proportion of
> voters who plan to vote for Smith. How many people should be surveyed? Assume a margin of error is 3%.
>
> a.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-010-pool-002

**Chunk:** `openstax_principles_ds:4.1:chunk-019`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> • If a prior estimate for the sample proportion is not available, then use
> .
>
> EXAMPLE 4.7
>
> Problem
>
> Political candidate Smith is planning a survey to determine a 95% confidence interval for the proportion of
> voters who plan to vote for Smith. How many people should be surveyed? Assume a margin of error is 3%.
>
> a. Assume there is no prior estimate for the proportion of voters who plan to vote for candidate Smith.
> b. Assume that from prior election results, approximately 42% of people previously voted for candidate
>
> Smith.
>
> Solution
>
> a. For a 95% confidence interval, the corresponding critical value is
> . The margin of error is
> specified as 0.03. Since a prior estimate for the sample proportion is unknown, use a value of 0.5 for . Using the sample size formula:
>
> Round to the next higher whole number, so the desired sample size is 1,068 people to be surveyed.
> b. Since a prior estimate for the sample proportion is available, use the value of 0.42 for .
>
> Using the sample size formula:
>
> Round to the next higher whole number, so the desired sample size is 1,040 people to be surveyed. Note that having a prior estimate of the sample proportion will result in a smaller sample size
> requirement. This is a general conclusion, so if a researcher has a prior estimate for the population
> proportion, this will result in a smaller sample size requirement as compared to the situation where no
> prior estimate is available.
>
> Bootstrapping Methods
>
> In the earlier discussion of confidence intervals, certain requirements needed to be met in order to use the
> estimation methods. For example, when calculating the confidence interval for a mean, this requirement was
> indicated:

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-010-pool-003

**Chunk:** `openstax_principles_ds:4.1:chunk-025`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> #print the confidence interval
> print(conf_interval.confidence_interval)
>
> The resulting output will look like this:
>
> ConfidenceInterval(low=22.45, high=26.7)
>
> Using 50,000 bootstrapped samples, a 95% confidence interval is generated as (22.45, 26.7).
>
> EXPLORING FURTHER
>
> Simulating Confidence Intervals
>
> A number of websites and resources, such as the online textbook Online Statistics Education: A Multimedia
> Course of Study (https://openstax.org/r/estimation) (http://onlinestatbook.com/) (project leader: David M. Lane, Rice University), allow the user to simulate confidence intervals for means or proportions using
> simulated sample data. It is useful to observe how many intervals contain an assumed value for the
> population mean or population proportion. The Stapplet (https://openstax.org/r/stapplet) website provides
> a similar tool.
>
> Using Python to Calculate Confidence Intervals
>
> When calculating confidence intervals, data scientists typically make use of technology to help streamline and
> automate the analysis. Python provides built-in functions for confidence interval calculations, and several
> examples are shown in Table 4.5. Students are encouraged to try examples themselves and experiment to use
> Python to assist with these calculations.
>
> Table 4.5 provides a summary of various functions available within the SciPy library (https://openstax.org/
>
> r/spy) for confidence interval calculations:
>
> Usage
> Python Function Name
> Syntax
>
> norm.interval()
> norm.interval(conf_level,
> sample_mean,standard_dev/
> sqrt
>
> (n))
>
> Calculate confidence interval for
> the mean when population
> standard deviation is known,
> given sample mean, population
> standard deviation, and sample
> size (uses normal distribution).
>
> t.interval()
> t.interval(conf_level,
> degrees_freedom,
> sample_mean,standard_dev/
> sqrt
>
> (n))
>
> Calculate confidence interval for
> the mean when population
> standard deviation is unknown,
> given sample mean, sample
> standard deviation, and sample
> size (uses t-distribution).
>
> Calculate confidence interval for
> a proportion (uses normal
> distribution).
>
> proportion_confint()
> proportion_confint(success,
> sample_size,
> 1 – confidence_level)
>
> Table 4.5 Python Functions for Confidence Intervals
>
> EXAMPLE 4.9
>
> Problem
>
> Repeat Example 4.3 to calculate a 90% confidence interval, but use Python functions to calculate the
> confidence interval.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-010-pool-004

**Chunk:** `openstax_intro_stats_2e:8.4:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.4: Confidence Interval (Home Costs)
>
> c. n = _____
>
> 2. In words, define the random variable
> . 3. State the estimated distribution to use. Use both words and symbols.
>
> Find the Confidence Interval
>
> 1. Calculate the confidence interval and the error bound.
> a. Confidence Interval: _____
> b. Error Bound: _____
>
> 2. How much area is in both tails (combined)? α = _____
> 3. How much area is in each tail?
>  = _____
>
> 4. Fill in the blanks on the graph with the area in each section. Then, fill in the number line with the upper and lower
> limits of the confidence interval and the sample mean.
>
> Figure 8.6
>
> 5. Some students think that a 90% confidence interval contains 90% of the data. Use the list of data on the first page
> and count how many of the data values lie within the confidence interval. What percent is this? Is this percent close
> to 90%? Explain why this percent should or should not be close to 90%.
>
> Describe the Confidence Interval
>
> 1. In two to three complete sentences, explain what a confidence interval means (in general), as if you were talking to
> someone who has not taken statistics. 2. In one to two complete sentences, explain what this confidence interval means for this particular study.
>
> Use the Data to Construct Confidence Intervals
>
> 1. Using the given information, construct a confidence interval for each confidence level given.
>
> Confidence level
> EBM/Error Bound
> Confidence Interval
>
> 50%
>
> 80%
>
> 95%
>
> 99%
>
> Table 8.6
>
> 2. What happens to the EBM as the confidence level increases? Does the width of the confidence interval increase or
> decrease? Explain why this happens.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-010-pool-005

**Chunk:** `openstax_principles_ds:4.1:chunk-026`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Calculate confidence interval for
> a proportion (uses normal
> distribution).
>
> proportion_confint()
> proportion_confint(success,
> sample_size,
> 1 – confidence_level)
>
> Table 4.5 Python Functions for Confidence Intervals
>
> EXAMPLE 4.9
>
> Problem
>
> Repeat Example 4.3 to calculate a 90% confidence interval, but use Python functions to calculate the
> confidence interval.
>
> Recall from Example 4.3, the sample mean is 12.5 hours with a population standard deviation of 6.3 hours. The sample size is 50 students, and we are interested in calculating a 90% confidence interval.
>
> Solution
>
> Use the Python function norm.interval() as shown:
>
> PYTHON CODE
>
> import scipy.stats as stats
> import numpy as np
> import math
>
> # Enter sample mean, population standard deviation and sample size
> sample_mean = 12.5
> population_standard_deviation = 6.3
> sample_size = 50
>
> # Confidence level
> confidence_level = 0.90
>
> # standard error
> standard_error = population_standard_deviation / math.sqrt(sample_size)
>
> # Calculate confidence interval using norm.interval function
> stats.norm.interval(confidence_level, sample_mean, standard_error)
>
> The resulting output will look like this:
>
> (11.03451018636739, 13.965489813632608)
>
> EXAMPLE 4.10
>
> Problem
>
> Repeat Example 4.4 to calculate a 99% confidence interval, but use Python functions to calculate the
> confidence interval.
>
> Recall from Example 4.4, the sample mean is 15.8 miles with a standard deviation of 3.2 miles. The sample
> size is 26 employees, and we are interested in calculating a 99% confidence interval.
>
> Solution
>
> Use the Python function t.interval() as shown:
>
> PYTHON CODE
>
> # Enter sample mean, sample standard deviation, and sample size
> sample_mean = 15.8
> sample_standard_deviation = 3.2
> sample_size = 26
>
> # Degrees of freedom (sample size - 1)
> degrees_of_freedom = sample_size - 1
>
> # Confidence level
> confidence_level = 0.99
>
> # standard error
> standard_error = sample_standard_deviation / math.sqrt(sample_size)

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-010-pool-006

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> The margin of error (EBM) depends on the confidence level (abbreviated CL). The confidence level is often considered
> the probability that the calculated confidence interval estimate will contain the true population parameter. However, it is
> more accurate to state that the confidence level is the percent of confidence intervals that contain the true population
> parameter when repeated samples are taken. Most often, it is the choice of the person constructing the confidence
> interval to choose a confidence level of 90% or higher because that person wants to be reasonably certain of their
> conclusions.
>
> There is another probability called alpha (α). α is related to the confidence level, CL. α is the probability that the interval
> does not contain the unknown population parameter. Mathematically, α + CL = 1.
>
> EXAMPLE 8.1
>
> Suppose we have collected data from a sample. We know the sample mean but we do not know the mean for the entire
> population. The sample mean is seven, and the error bound for the mean is 2.5.
>
> = 7 and EBM = 2.5
>
> The confidence interval is (7 – 2.5, 7 + 2.5), and calculating the values gives (4.5, 9.5).
>
> If the confidence level (CL) is 95%, then we say that, "We estimate with 95% confidence that the true value of the
> population mean is between 4.5 and 9.5."
>
> TRY IT 8.1
>
> Suppose we have data from a sample. The sample mean is 15, and the error bound for the mean is 3.2.
>
> What is the confidence interval estimate for the population mean?
>
> A confidence interval for a population mean with a known standard deviation is based on the fact that the sample means
> follow an approximately normal distribution.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-010-pool-007

**Chunk:** `openstax_intro_stats_2e:8.4:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.4: Confidence Interval (Home Costs)
>
> gives
>
> Round the answer to the next higher value. The sample size should be 752 cell phone customers aged 50+ in order to be
> 90% confident that the estimated (sample) proportion is within three percentage points of the true population
> proportion of all customers aged 50+ who use text messaging on their cell phones.
>
> TRY IT 8.14
>
> Suppose an internet marketing company wants to determine the current percentage of customers who click on ads
> on their smartphones. How many customers should the company survey in order to be 90% confident that the
> estimated proportion is within five percentage points of the true population proportion of customers who click on ads
> on their smartphones?
>
> 8.4 Confidence Interval (Home Costs)
>
> Stats Lab
>
> Confidence Interval (Home Costs)
> Class Time:
>
> Names:
>
> Student Learning Outcomes
>
> • The student will calculate the 90% confidence interval for the mean cost of a home in the area in which this school is
> located.
> • The student will interpret confidence intervals.
> • The student will determine the effects of changing conditions on the confidence interval.
>
> Collect the Data
> Check the Real Estate section in your local newspaper. Record the sale prices for 35 randomly selected homes recently
> listed in the county.
>
> NOTE
>
> Many newspapers list them only one day per week. Also, we will assume that homes come up for sale randomly.
>
> 1. Complete the table:
>
> Table 8.5
>
> Describe the Data
>
> 1. Compute the following:
> a.
>  = _____
> b.
>  = _____
>
> c. n = _____
>
> 2. In words, define the random variable
> . 3. State the estimated distribution to use. Use both words and symbols.
>
> Find the Confidence Interval
>
> 1. Calculate the confidence interval and the error bound.
> a. Confidence Interval: _____
> b. Error Bound: _____
>
> 2. How much area is in both tails (combined)? α = _____
> 3.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-010-pool-008

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> Use n = 217: Always round the answer UP to the next higher integer to ensure that the sample size is large enough.
>
> Therefore, 217 Foothill College students should be surveyed in order to be 95% confident that we are within two years of
> the true population mean age of Foothill College students.
>
> TRY IT 8.7
>
> The population standard deviation for the height of high school basketball players is three inches. If we want to be
> 95% confident that the sample mean height is within one inch of the true population mean height, how many
> randomly selected students must be surveyed?
>
> 8.2 A Single Population Mean using the Student t Distribution
>
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

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-010-pool-009

**Chunk:** `openstax_principles_ds:4.1:chunk-002`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> In addition, inferential
> statistics is used by data scientists to assess model performance and compare different algorithms in machine
> learning application. Inferential statistics provides methods for generating predictive forecasting models, and
> this allows data scientists to generate predictions and trends to assist in effective and accurate decision-
> making. In this section, we explore the use of confidence intervals, which is used extensively in inferential
> statistical analysis.
>
> We begin by introducing confidence intervals, which are used to estimate the range within which a population
> parameter is likely to fall. We discuss estimation of parameters for the mean both when the standard deviation
> is known and when it is not known. We discuss sample size determination, building on the sampling
> techniques presented in Collecting and Preparing Data. And we discuss bootstrapping, a method used to
> construct a confidence interval based on repeated sampling. Hypothesis Testing will move on to hypothesis
> testing, which is used to make inferences about unknown parameters.
>
> Estimating Parameters with Confidence Intervals
>
> A point estimate is a single value that is used to estimate a population parameter. For example, a sample
> mean is a point estimate that is representative of the true population mean in that the sample mean is used
> as an estimate for the unknown population mean. When researchers collect data from a sample to make
> inferences about a population, they calculate a point estimate based on the observed sample data. (See Survey
> Design and Implementation for coverage of sampling techniques.) The point estimate serves as the best guess
> or approximation for the parameter's actual value.
>
> A confidence interval estimates the range within which a population parameter, such as a mean or a
> proportion, is likely to fall.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-010-pool-010

**Chunk:** `openstax_intro_stats_2e:8.6:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.6: Confidence Interval (Women's Heights)
>
> With these values, construct a 90% confidence interval for your sample of ten values. Write
> the confidence interval you obtained in the first space of Table 8.9. 3. Now write your confidence interval on the board. As others in the class write their confidence intervals on the board,
> copy them into Table 8.9.
>
> __________
> __________
> __________
> __________
> __________
>
> __________
> __________
> __________
> __________
> __________
>
> __________
> __________
> __________
> __________
> __________
>
> __________
> __________
> __________
> __________
> __________
>
> __________
> __________
> __________
> __________
> __________
>
> __________
> __________
> __________
> __________
> __________
>
> __________
> __________
> __________
> __________
> __________
>
> __________
> __________
> __________
> __________
> __________
>
> Table 8.9 90% Confidence Intervals
>
> Discussion Questions
>
> 1. The actual population mean for the 100 heights given Table 8.8 is μ = 63.4. Using the class listing of confidence
> intervals, count how many of them contain the population mean μ; i.e., for how many intervals does the value of μ
> lie between the endpoints of the confidence interval? 2. Divide this number by the total number of confidence intervals generated by the class to determine the percent of
>
> confidence intervals that contains the mean μ. Write this percent here: _____________. 3. Is the percent of confidence intervals that contain the population mean μ close to 90%? 4. Suppose we had generated 100 confidence intervals. What do you think would happen to the percent of confidence
> intervals that contained the population mean? 5. When we construct a 90% confidence interval, we say that we are 90% confident that the true population mean
> lies within the confidence interval. Using complete sentences, explain what we mean by this phrase. 6. Some students think that a 90% confidence interval contains 90% of the data.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-010-pool-011

**Chunk:** `openstax_principles_ds:4.1:chunk-003`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> A confidence interval estimates the range within which a population parameter, such as a mean or a
> proportion, is likely to fall. The confidence interval provides a level of uncertainty associated with the estimate
> and is expressed as a range of values. A confidence interval will provide both a lower and an upper bound for
> the population parameter, where the point estimate is centered within the interval.
>
> Table 4.1 describes the point estimates and corresponding population parameters for the mean and
> proportion.
>
> Population Parameter
> Point Estimate
>
> Mean
> Population mean is denoted
> as .
>
> Point estimate is the sample
> mean .
>
> Proportion
> Population proportion is
> denoted as .
>
> Point estimate is the sample
> proportion .
>
> Table 4.1 Population Parameters and Point Estimates for Mean and Proportion
>
> Let’s say a researcher is interested in estimating the mean income for all residents of California. Since it is not
> feasible to collect data from every resident of California, the researcher selects a random sample of 1,000
> residents and calculates the sample mean income for these 1,000 people. This average income estimate from
> the sample then provides an estimate for the population mean income of all California residents. The sample
> mean is chosen as the point estimate for the population mean in that the sample mean provides the most
> unbiased estimate for the population mean. In the same way, the sample proportion provides the most
> unbiased estimate for the population proportion. An unbiased estimator is a statistic that provides an
> accurate estimate for the corresponding population parameter without overestimating or underestimating the
> parameter.
>
> In order to calculate a confidence interval, two quantities are needed:
>
> • The point estimate
> • The margin of error
>
> As noted, the point estimate is a single number that is used to estimate the population parameter.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-010-pool-012

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-005`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> CL = 1 – α, so α is the area that is
> split equally between the two tails. Each of the tails contains an area equal to
> .
>
> The z-score that has an area to the right of
>  is denoted by
> .
>
> For example, when CL = 0.95, α = 0.05 and
>  = 0.025; we write
>  = z0.025.
>
> The area to the right of z0.025 is 0.025 and the area to the left of z0.025 is 1 – 0.025 = 0.975.
>
> , using a calculator, computer or a standard normal probability table.
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> invNorm(0.975, 0, 1) = 1.96
>
> NOTE
>
> Remember to use the area to the LEFT of
> ; in this chapter the last two inputs in the invNorm command are 0, 1,
>
> because you are using a standard normal distribution Z ~ N(0, 1).
>
> Writing the Interpretation
> The interpretation should clearly state the confidence level (CL), explain what population parameter is being estimated
> (here, a population mean), and state the confidence interval (both endpoints). "We estimate with ___% confidence that
> the true population mean (include the context of the problem) is between ___ and ___ (include appropriate units)."
>
> EXAMPLE 8.2
>
> Suppose scores on exams in statistics are normally distributed with an unknown population mean and a population
> standard deviation of three points. A random sample of 36 scores is taken and gives a sample mean (sample mean score)
> of 68. Find a confidence interval estimate for the population mean exam score (the mean score on all exams).
>
> Problem
> Find a 90% confidence interval for the true (population) mean of statistics exam scores.
>
> Solution
> • You can use technology to calculate the confidence interval directly.
> • The first solution is shown step-by-step.
> • The second solution uses the TI-83, 83+, and 84+ calculators.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-010-pool-013

**Chunk:** `openstax_intro_stats_2e:8.6:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.6: Confidence Interval (Women's Heights)
>
> 5. When we construct a 90% confidence interval, we say that we are 90% confident that the true population mean
> lies within the confidence interval. Using complete sentences, explain what we mean by this phrase. 6. Some students think that a 90% confidence interval contains 90% of the data. Use the list of data given (the heights
> of women) and count how many of the data values lie within the confidence interval that you generated based on
> that data. How many of the 100 data values lie within your confidence interval? What percent is this? Is this percent
> close to 90%? 7. Explain why it does not make sense to count data values that lie in a confidence interval. Think about the random
> variable that is being used in the problem. 8. Suppose you obtained the heights of ten women and calculated a confidence interval from this information. Without knowing the population mean μ, would you have any way of knowing for certain if your interval actually
> contained the value of μ? Explain.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-010-pool-014

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> Calculate the Sample Mean:
> • If we know the error bound:  = 68.82 – 0.82 = 68
>
> • If we don't know the error bound:  =
>  = 68.
>
> TRY IT 8.6
>
> Suppose we know that a confidence interval is (42.12, 47.88). Find the error bound and the sample mean.
>
> Calculating the Sample Size n
>
> If researchers desire a specific margin of error, then they can use the error bound formula to calculate the required
> sample size.
>
> The error bound formula for a population mean when the population standard deviation is known is
>
> EBM =
> .
>
> The formula for sample size is n =
> , found by solving the error bound formula for n.
>
> In this formula, z is
> , corresponding to the desired confidence level. A researcher planning a study who wants a
>
> specified confidence level and error bound can use this formula to calculate the size of the sample needed for the study.
>
> EXAMPLE 8.7
>
> The population standard deviation for the age of Foothill College students is 15 years. If we want to be 95% confident
> that the sample mean age is within two years of the true population mean age of Foothill College students, how many
> randomly selected Foothill College students must be surveyed?
>
> From the problem, we know that σ = 15 and EBM = 2.
> z = z0.025 = 1.96, because the confidence level is 95%.
>
> n =
>  =
>  = 216.09 using the sample size equation.
>
> Use n = 217: Always round the answer UP to the next higher integer to ensure that the sample size is large enough.
>
> Therefore, 217 Foothill College students should be surveyed in order to be 95% confident that we are within two years of
> the true population mean age of Foothill College students.
>
> TRY IT 8.7

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-010-pool-015

**Chunk:** `openstax_intro_stats_2e:8.3:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.3: A Population Proportion
>
> Often, election polls are calculated with 95%
> confidence, so, the pollsters would be 95% confident that the true proportion of voters who favored the candidate would
> be between 0.37 and 0.43: (0.40 – 0.03,0.40 + 0.03).
>
> Investors in the stock market are interested in the true proportion of stocks that go up and down each week. Businesses
> that sell personal computers are interested in the proportion of households in the United States that own personal
> computers. Confidence intervals can be calculated for the true proportion of stocks that go up or down each week and
> for the true proportion of households in the United States that own personal computers.
>
> The procedure to find the confidence interval, the sample size, the error bound, and the confidence level for a
> proportion is similar to that for the population mean, but the formulas are different.
>
> How do you know you are dealing with a proportion problem? First, the underlying distribution is a binomial
> distribution. (There is no mention of a mean or average.) If X is a binomial random variable, then X ~ B(n, p) where n is
> the number of trials and p is the probability of a success. To form a proportion, take X, the random variable for the
> number of successes and divide it by n, the number of trials (or the sample size). The random variable
>  (read "P prime")
>
> is that proportion,
>
> (Sometimes the random variable is denoted as
> , read "P hat".)
>
> When n is large and p is not close to zero or one, we can use the normal distribution to approximate the binomial.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-010-pool-016

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-004`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> In summary, as a result of the central limit theorem:
>
> •
>  is normally distributed, that is,
>  ~ N
> .
>
> • When the population standard deviation σ is known, we use a normal distribution to calculate the error
> bound.
>
> Calculating the Confidence Interval
> To construct a confidence interval estimate for an unknown population mean, we need data from a random sample. The
> steps to construct and interpret the confidence interval are:
>
> • Calculate the sample mean  from the sample data. Remember, in this section we already know the population
> standard deviation σ.
> • Find the z-score that corresponds to the confidence level.
> • Calculate the error bound EBM.
> • Construct the confidence interval.
> • Write a sentence that interprets the estimate in the context of the situation in the problem. (Explain what the
> confidence interval means, in the words of the problem.)
>
> We will first examine each step in more detail, and then illustrate the process with some examples.
>
> Finding the z-score for the Stated Confidence Level
> When we know the population standard deviation σ, we use a standard normal distribution to calculate the error bound
>
> EBM and construct the confidence interval. We need to find the value of z that puts an area equal to the confidence level
> (in decimal form) in the middle of the standard normal distribution Z ~ N(0, 1).
>
> The confidence level, CL, is the area in the middle of the standard normal distribution. CL = 1 – α, so α is the area that is
> split equally between the two tails. Each of the tails contains an area equal to
> .
>
> The z-score that has an area to the right of
>  is denoted by
> .
>
> For example, when CL = 0.95, α = 0.05 and
>  = 0.025; we write
>  = z0.025.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-010-pool-017

**Chunk:** `openstax_intro_stats_2e:8.3:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.3: A Population Proportion
>
> The random variable
>  (read "P prime")
>
> is that proportion,
>
> (Sometimes the random variable is denoted as
> , read "P hat".)
>
> When n is large and p is not close to zero or one, we can use the normal distribution to approximate the binomial.
>
> If we divide the random variable, the mean, and the standard deviation by n, we get a normal distribution of proportions
> with
> , called the estimated proportion, as the random variable. (Recall that a proportion as the number of successes
> divided by n.)
>
> Using algebra to simplify :
>
> follows a normal distribution for proportions:
>
> The confidence interval has the form (
>  – EBP,
>  + EBP). EBP is error bound for the proportion.
>
> =
>
> = the estimated proportion of successes (
>  is a point estimate for p, the true proportion.)
>
> x = the number of successes
>
> n = the size of the sample
>
> The error bound for a proportion is
>
> where
>  = 1 –
>
> This formula is similar to the error bound formula for a mean, except that the "appropriate standard deviation" is
> different. For a mean, when the population standard deviation is known, the appropriate standard deviation that we use
>
> is
> . For a proportion, the appropriate standard deviation is
> .
>
> However, in the error bound formula, we use
>  as the standard deviation, instead of
> .
>
> In the error bound formula, the sample proportions
>  and
>  are estimates of the unknown population proportions
> p and q. The estimated proportions
>  and
>  are used because p and q are not known. The sample proportions
>  and
>  are calculated from the data:
>  is the estimated proportion of successes, and
>  is the estimated proportion of
> failures.
>
> The confidence interval can be used only if the number of successes
>  and the number of failures
>  are both greater
> than five.
>
> NOTE

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-010-pool-018

**Chunk:** `openstax_principles_ds:3.2:chunk-004`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.2: Measures of Variation
>
> The more the individual data values differ from the mean, the larger the variance.
>
> A financial advisor might use variance to determine the volatility of an investment and therefore help guide
> financial decisions. For example, a more cautious investor might opt for investments with low volatility.
>
> The formula used to calculate variance also depends on whether the data is collected from a sample or a
>
> population. The notation
>  is used to represent the sample variance, and the notation
>  is used to represent
> the population variance.
>
> Formula for the sample variance:
>
> Formula for the population variance:
>
> In these formulas:
>
> represents the individual data values
>  represents the sample mean
>  represents the sample size
>  represents the population mean
>
> represents the population size
>
> ALTERNATE FORMULA FOR VARIANCE
>
> An alternate formula for the variance is available. It is sometimes used for more efficient computations:
>
> In the formulas for sample variance and population variance, notice the denominator for the sample variance
> is
> , whereas the denominator for the population variance is
> . The use of
>  in the denominator of the
> sample variance is used to provide the best estimate for the population variance, in the sense that if repeated
> samples of size  are taken and the sample mean computed each time, then the average of those sample
> means will tend to the population mean as the number of repeated samples increase.
>
> It is important to note that in many data science applications, population data is unavailable, and so we
> typically calculate the sample variance. For example, if a researcher wanted to estimate the percentage of
> smokers for all adults in the United States, it would be impractical to collect data from every adult in the United
> States.
>
> Notice that the sample variance is a sum of squares.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-011

**Pregunta:** For a standardized normal variable, what values define its center and spread, and how should the sign and magnitude of its standardized score be interpreted?

**Respondibilidad de referencia:** answerable

### q-v1-011-pool-001

**Chunk:** `openstax_principles_ds:3.5:chunk-014`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.5: Discrete and Continuous Probability Distributions
>
> The normal
> distribution has applications in many fields including engineering, science, finance, medicine, marketing, and
> psychology.
>
> The normal distribution has two parameters: the mean, , and the standard deviation, . The mean represents
> the center of the distribution, and the standard deviation measures the spread, or dispersion, of the
> distribution. The variable  represents the realization, or observed value, of the random variable
>  that
> follows a normal distribution.
>
> The typical notation used to indicate that a random variable follows a normal distribution is as follows:
>
> (see Figure 3.7). For example, the notation
>  indicates that the random variable
> follows a normal distribution with mean of 5.2 and standard deviation of 3.7.
>
> A normal distribution with mean of 0 and standard deviation of 1 is called the standard normal distribution
> and can be notated as
> . Any normal distribution can be standardized by converting its values to
> -scores. Recall that a -score tells you how many standard deviations from the mean there are for a given
> measurement.
>
> Figure 3.7 Graph of the Normal (Bell-Shaped) Distribution
>
> The curve in Figure 3.7 is symmetric on either side of a vertical line drawn through the mean, . The mean is
>
> the same as the median, which is the same as the mode, because the graph is symmetric about . As the
> notation indicates, the normal distribution depends only on the mean and the standard deviation. Because the
> area under the curve must equal 1, a change in the standard deviation, , causes a change in the shape of the
> normal curve; the curve becomes fatter and wider or skinnier and taller depending on . A change in  causes
> the graph to shift to the left or right. This means there are an infinite number of normal probability
> distributions.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-011-pool-002

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-004`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> This calculation requires n
> deviations
> . Because the sum of the deviations is zero, we can find the last deviation once we know the other
> n – 1 deviations. The other n – 1 deviations can change or vary freely. We call the number n – 1 the degrees of freedom
> (df).
>
> Properties of the Student's t-Distribution
>
> • The graph for the Student's t-distribution is similar to the standard normal curve.
> • The mean for the Student's t-distribution is zero and the distribution is symmetric about zero.
> • The Student's t-distribution has more probability in its tails than the standard normal distribution because the
> spread of the t-distribution is greater than the spread of the standard normal. So the graph of the Student's t-
> distribution will be thicker in the tails and shorter in the center than the graph of the standard normal distribution.
> • The exact shape of the Student's t-distribution depends on the degrees of freedom. As the degrees of freedom
> increases, the graph of Student's t-distribution becomes more like the graph of the standard normal distribution.
> • The underlying population of individual observations is assumed to be normally distributed with unknown
> population mean μ and unknown population standard deviation σ. The size of the underlying population is
> generally not relevant unless it is very small. If it is bell shaped (normal) then the assumption is met and doesn't
> need discussion. Random sampling is assumed, but that is a completely separate assumption from normality.
>
> Calculators and computers can easily calculate any Student's t-probabilities. The TI-83,83+, and 84+ have a tcdf function
> to find the probability for given values of t. The grammar for the tcdf command is tcdf(lower bound, upper bound,
> degrees of freedom).

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-011-pool-003

**Chunk:** `openstax_principles_ds:3.2:chunk-002`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.2: Measures of Variation
>
> Providing some measure of the spread, or variation, in a dataset is crucial to a comprehensive summary of the
> dataset. Two datasets may have the same mean but can exhibit very different spread, and so a measure of
> dispersion for a dataset is very important. While measures of central tendency (like mean, median, and mode)
> describe the center or average value of a distribution, measures of dispersion give insights into how much
> individual data points deviate from this central value.
>
> The following two datasets are the exam scores for a group of three students in a biology course and in a
> statistics course.
>
> Dataset A: Exam scores for students in a biology course: 40, 70, 100
> Dataset B: Exam scores for students in a statistics course: 69, 70, 71
>
> Notice that the mean score for both Dataset A and Dataset B is 70.
>
> However, the datasets are significantly different from one another:
>
> Dataset A has larger variability where one student scored 30 points below the mean and another student
> scored 30 points above the mean. Dataset B has smaller variability where the exam scores are much more tightly clustered around the mean of
> 70.
>
> This example illustrates that publishing the mean of a dataset is often inadequate to fully communicate the
> characteristics of the dataset. Instead, data scientists will typically include a measure of variation as well.
>
> The three primary measures of variability are range, variance, and standard deviation, and these are described
> next.
>
> Range
>
> Range is a measure of dispersion for a dataset that is calculated by subtracting the minimum from the
> maximum of the dataset:
>
> Range is a straightforward calculation but makes use of only two of the data values in a dataset. The range can
> also be affected by outliers.
>
> EXAMPLE 3.6
>
> Problem

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-011-pool-005

**Chunk:** `openstax_intro_stats_2e:6.1:chunk-005`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 6: The Normal Distribution
> Section 6.1: The Standard Normal Distribution
>
> The z-score for y = 4 is z = 2. This means that four is z = 2 standard deviations to the right of the mean. Therefore, x = 17
> and y = 4 are both two (of their own) standard deviations to the right of their respective means.
>
> The z-score allows us to compare data that are scaled differently. To understand the concept, suppose X ~ N(5, 6)
> represents weight gains for one group of people who are trying to gain weight in a six week period and Y ~ N(2, 1)
> measures the same weight gain for a second group of people. A negative weight gain would be a weight loss. Since x =
> 17 and y = 4 are each two standard deviations to the right of their means, they represent the same, standardized weight
> gain relative to their means.
>
> TRY IT 6.2
>
> Fill in the blanks.
>
> Jerome averages 16 points a game with a standard deviation of four points. X ~ N(16,4). Suppose Jerome scores ten
> points in a game. The z–score when x = 10 is –1.5. This score tells you that x = 10 is _____ standard deviations to the
> ______(right or left) of the mean______(What is the mean?).
>
> The Empirical Rule
> If X is a random variable and has a normal distribution with mean µ and standard deviation σ, then the Empirical Rule
> states the following:

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-011-pool-006

**Chunk:** `openstax_intro_stats_2e:6.2:chunk-005`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 6: The Normal Distribution
> Section 6.2: Using the Normal Distribution
>
> Solution
> c. Find the 90th percentile. For each problem or part of a problem, draw a new graph. Draw the x-axis. Shade the area
> that corresponds to the 90th percentile.
>
> Let k = the 90th percentile. The variable k is located on the x-axis. P(x < k) is the area to the left of k. The 90th percentile
> k separates the exam scores into those that are the same or lower than k and those that are the same or higher. Ninety
>
> percent of the test scores are the same or lower than k, and ten percent are the same or higher. The variable k is often
> called a critical value.
>
> k = 69.4
>
> Figure 6.6
>
> The 90th percentile is 69.4. This means that 90% of the test scores fall at or below 69.4 and 10% fall at or above. To get
> this answer on the calculator, follow this step:
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> invNorm in 2nd DISTR. invNorm(area to the left, mean, standard deviation)
>
> For this problem, invNorm(0.90,63,5) = 69.4
>
> Problem
> d. Find the 70th percentile (that is, find the score k such that 70% of scores are below k and 30% of the scores are above
> k).
>
> Solution
> d. Find the 70th percentile.
>
> Draw a new graph and label it appropriately. k = 65.6
>
> The 70th percentile is 65.6. This means that 70% of the test scores fall at or below 65.5 and 30% fall at or above.
>
> invNorm(0.70,63,5) = 65.6
>
> TRY IT 6.8
>
> The golf scores for a school team were normally distributed with a mean of 68 and a standard deviation of three.
>
> Find the probability that a randomly selected golfer scored less than 65.
>
> EXAMPLE 6.9

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-011-pool-007

**Chunk:** `openstax_principles_ds:4.2:chunk-015`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> For this procedure, the test statistic will be a t-score and the standardized test statistic is calculated as follows:
>
> Where:
>
> is the sample mean.
>  is the hypothesized value of the population mean, which comes from the null hypothesis.
>  is the sample standard deviation.
>
> is the sample size.
>
> Example 4.14 provides a step-by-step example to illustrate this process.
>
> EXAMPLE 4.14
>
> Problem
>
> A smartphone manufacturer claims that the mean battery life of its latest smartphone model is 25 hours. A
> consumer group decides to test this hypothesis and collects a sample of 50 smartphones and determines
> that the mean battery life of the sample is 24.1 hours with a sample standard deviation of 4.1 hours. Use
> this sample data to test the claim made by the smartphone manufacturer. Use a level of significance of 0.10
> for this analysis.
>
> Solution
>
> The first step in the hypothesis testing procedure is to write the null and alternative hypotheses based on
> the claim. Notice that the claim involves the phrase “is 25 hours,” where “is” will translate to an equals
> symbol. An equals symbol must be used in the null hypothesis. The complement of an “equals” symbol is a
> “not equals” symbol, which will be used in the alternative hypothesis. The claim refers to the population
> mean battery life of smartphones, so the symbol  will be used. The claim corresponds to the null
> hypothesis. Notice that this setup will correspond to Setup A from Table 4.6. Thus the setup of the null and
>
> alternative hypotheses will be as follows:
>
> Since the population standard deviation is unknown in this example, the t-distribution will be used to
> conduct the hypothesis test.
>
> Next, calculate the standardized test statistic as follows:

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-011-pool-008

**Chunk:** `openstax_intro_stats_2e:6.2:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 6: The Normal Distribution
> Section 6.2: Using the Normal Distribution
>
> TRY IT 6.7
>
> If the area to the left of x is 0.012, then what is the area to the right?
>
> EXAMPLE 6.8
>
> The final exam scores in a statistics class were normally distributed with a mean of 63 and a standard deviation of five.
>
> Problem
> a. Find the probability that a randomly selected student scored more than 65 on the exam.
>
> Solution
> a. Let X = a score on the final exam. X ~ N(63, 5), where μ = 63 and σ = 5.
>
> Draw a graph.
>
> Then, find P(x > 65).
>
> P(x > 65) = 0.3446
>
> Figure 6.5
>
> The probability that any student selected at random scores more than 65 is 0.3446.
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> Go into 2nd DISTR.
>
> After pressing 2nd DISTR, press 2:normalcdf.
>
> The syntax for the instructions are as follows:
>
> normalcdf(lower value, upper value, mean, standard deviation) For this problem: normalcdf(65,1E99,63,5) = 0.3446. You get 1E99 (= 1099) by pressing 1, the EE key (a 2nd key) and then 99. Or, you can enter 10^99 instead. The number
>
> 1099 is way out in the right tail of the normal curve. We are calculating the area between 65 and 1099. In some
>
> instances, the lower number of the area might be –1E99 (= –1099). The number –1099 is way out in the left tail of the
> normal curve.
>
> Historical Note
>
> The TI probability program calculates a z-score and then the probability from the z-score. Before technology, the
> z-score was looked up in a standard normal probability table (because the math involved is too cumbersome) to find
> the probability. In this example, a standard normal table with area to the left of the z-score was used. You calculate
> the z-score and look up the area to the left.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-011-pool-009

**Chunk:** `openstax_intro_stats_2e:8.4:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.4: Confidence Interval (Home Costs)
>
> c. n = _____
>
> 2. In words, define the random variable
> . 3. State the estimated distribution to use. Use both words and symbols.
>
> Find the Confidence Interval
>
> 1. Calculate the confidence interval and the error bound.
> a. Confidence Interval: _____
> b. Error Bound: _____
>
> 2. How much area is in both tails (combined)? α = _____
> 3. How much area is in each tail?
>  = _____
>
> 4. Fill in the blanks on the graph with the area in each section. Then, fill in the number line with the upper and lower
> limits of the confidence interval and the sample mean.
>
> Figure 8.6
>
> 5. Some students think that a 90% confidence interval contains 90% of the data. Use the list of data on the first page
> and count how many of the data values lie within the confidence interval. What percent is this? Is this percent close
> to 90%? Explain why this percent should or should not be close to 90%.
>
> Describe the Confidence Interval
>
> 1. In two to three complete sentences, explain what a confidence interval means (in general), as if you were talking to
> someone who has not taken statistics. 2. In one to two complete sentences, explain what this confidence interval means for this particular study.
>
> Use the Data to Construct Confidence Intervals
>
> 1. Using the given information, construct a confidence interval for each confidence level given.
>
> Confidence level
> EBM/Error Bound
> Confidence Interval
>
> 50%
>
> 80%
>
> 95%
>
> 99%
>
> Table 8.6
>
> 2. What happens to the EBM as the confidence level increases? Does the width of the confidence interval increase or
> decrease? Explain why this happens.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-011-pool-010

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> He realized that he could not use a normal distribution for the calculation; he found that
>
> the actual distribution depends on the sample size. This problem led him to "discover" what is called the Student's t-
> distribution. The name comes from the fact that Gosset wrote under the pen name "Student."
>
> Up until the mid-1970s, some statisticians used the normal distribution approximation for large sample sizes and used
> the Student's t-distribution only for sample sizes of at most 30. With graphing calculators and computers, the practice
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
>
> Properties of the Student's t-Distribution

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-011-pool-011

**Chunk:** `openstax_principles_ds:3.2:chunk-001`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.2: Measures of Variation
>
> summarize data. Recall that the method describe() is defined for a DataFrame type object so should be
>
> called upon a DataFrame type variable (e.g. given a DataFrame d, use d.describe()).
>
> Figure 3.2 shows the output of DataFrame.describe() on the “Movie Profit” dataset we used in What Are
>
> Data and Data Science?, movie_profit.csv. The mean and 50% quartile show the average and median of each
> column. For example, the average worldwide gross earnings are $410.14 million, and the median earnings are
> $309.35 million. Note that average and/or median of some columns are not as meaningful as the others. The
> first column—Unnamed: 0—was simply used as an identifier of each item in the dataset, so the average and
> mean of this column is not quite useful. DataFrame.describe() still computes the values because it can (and
>
> it does not care which column is meaningful to do so or not).
>
> Figure 3.2 The Output of DataFrame.describe() with the Movie Profit Dataset
>
> EXPLORING FURTHER
>
> Working with Python
>
> See the Python website (https://openstax.org/r/python) for more details on using, installing, and working
> with Python. See this additional documentation, for more specific information on the statistics module
> (https://openstax.org/r/docspython).
>
> 3.2 Measures of Variation
>
> Learning Outcomes
> By the end of this section, you should be able to:
>
> • 3.2.1 Define and calculate the range, the variance, and the standard deviation for a dataset.
> • 3.2.2 Use Python to calculate measures of variation for a dataset.
>
> Providing some measure of the spread, or variation, in a dataset is crucial to a comprehensive summary of the
> dataset. Two datasets may have the same mean but can exhibit very different spread, and so a measure of
> dispersion for a dataset is very important.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-011-pool-012

**Chunk:** `openstax_principles_ds:3.1:chunk-003`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> The most widely used measures of the center of a dataset are the mean (average), the
> median, and the mode.
>
> Mean and Trimmed Mean
>
> The mean, or average, (sometimes referred to as the arithmetic mean) is the most commonly used measure of
> the center of a dataset. Sometimes the mean can be skewed by the presence of outliers, or data values that
> are significantly different as compared to the remainder of the dataset. In these instances, the trimmed mean
> is often used to provide a more representative measure of the center of the dataset, as we will discuss in the
> following section.
>
> Mean
>
> To calculate the mean, add the values of all the items in a dataset and divide by the number of items. For
> example, if the scores on your last three exams were 87, 92, and 73, then the mean score would be
>
> . If you had a large number of data values, you would proceed in the same way. For example, to
>
> calculate the mean value of 50 exam scores, add the 50 scores together and divide by 50. If the 50 scores add
>
> up to 4,050, for example, the mean score is
> , or 81.
>
> In data science applications, you will encounter two types of datasets: sample data and population data. Population data represents all the outcomes or measurements that are of interest. Sample data represents
> outcomes or measurements collected from a subset, or part, of the population of interest. Of course in many
> applications, collecting data from an entire population is not practical or feasible, and so we often rely on
> sample data.
>
> The notation  is used to indicate the sample mean, where the mean is calculated based on data taken from a
> sample.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-011-pool-013

**Chunk:** `openstax_principles_ds:3.1:chunk-004`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> Of course in many
> applications, collecting data from an entire population is not practical or feasible, and so we often rely on
> sample data.
>
> The notation  is used to indicate the sample mean, where the mean is calculated based on data taken from a
> sample. The notation
>  is used to denote the sum of the data values, and  is used to indicate the number
>
> of data values in the sample, also known as the sample size.
>
> The sample mean can be calculated using the following formula:
>
> The notation  is used to indicate the population mean, where the mean is calculated based on data taken
> from the entire population, and
>  is used to indicate the number of data values in the population, also known
> as the population size. The population mean can be calculated using the following formula:
>
> The mean can also be determined by its frequency distribution. For every unique data value in the dataset, the
> frequency distribution gives the number of times, or frequency, that this unique value appears in the
> dataset. In this type of situation, the mean can be calculated by multiplying each distinct value by its
> frequency, summing these values, and then dividing this sum by the total number of data values. Here is the
> corresponding formula for the sample mean using the frequency distribution:
>
> When all the values in the dataset are unique, this reduces to the previous formula given for the sample mean.
>
> EXAMPLE 3.1
>
> Problem
>
> During a clinical trial, a sample is taken of 10 patients and pulse rates are measured in beats per minute:
>
> 68, 92, 76, 51, 65, 83, 94, 72, 88, 59
>
> Calculate the mean pulse rate for this sample.
>
> Solution
>
> Add the 10 data values, and the sum is 748.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-011-pool-014

**Chunk:** `openstax_principles_ds:3.5:chunk-013`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.5: Discrete and Continuous Probability Distributions
>
> Many probability distributions apply to continuous random variables. These distributions rely on determining
> the probability that the random variable falls within a distinct range of values, which can be calculated using a
> probability density function (PDF). The probability density function (PDF) calculates the corresponding area
> under the probability density curve to determine the probability that the random variable will fall within this
> specific range of values. For example, to determine the probability that a salary falls between $50,000 and
> $70,000, we can calculate the area under the probability density function between these two salaries.
>
> Note that the total area under the probability density function will always equal 1. The probability that a
> continuous random variable takes on a specific value  is 0, so we will always calculate the probability for a
> random variable falling within some interval of values.
>
> In this section, we will examine an important continuous probability distribution that relies on the probability
> density function, namely the normal distribution. Many variables, such as heights, weights, salaries, and blood
> pressure measurements, follow a normal distribution, making it especially important in statistical analysis. In
> addition, the normal distribution forms the basis for more advanced statistical analysis such as confidence
> intervals and hypothesis testing, which are discussed in Inferential Statistics and Regression Analysis.
>
> The normal distribution is a continuous probability distribution that is symmetrical and bell-shaped. It is used
> when the frequency of data values decreases with data values above and below the mean. The normal
> distribution has applications in many fields including engineering, science, finance, medicine, marketing, and
> psychology.
>
> The normal distribution has two parameters: the mean, , and the standard deviation, . The mean represents
> the center of the distribution, and the standard deviation measures the spread, or dispersion, of the
> distribution.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-011-pool-015

**Chunk:** `openstax_principles_ds:3.2:chunk-005`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.2: Measures of Variation
>
> For example, if a researcher wanted to estimate the percentage of
> smokers for all adults in the United States, it would be impractical to collect data from every adult in the United
> States.
>
> Notice that the sample variance is a sum of squares. Its units of measurement are squares of the units of
> measurement of the original data. Since these square units are different than the units in the original data,
> this can be confusing. By contrast, standard deviation is measured in the same units as the original dataset,
> and thus the standard deviation is more commonly used to measure the spread of a dataset.
>
> Standard Deviation
>
> The standard deviation of a dataset provides a numerical measure of the overall amount of variation in a
> dataset in the same units as the data; it can be used to determine whether a particular data value is close to or
>
> far from the mean, relative to the typical distance from the mean.
>
> The standard deviation is always positive or zero. It is small when the data values are all concentrated close to
> the mean, exhibiting little variation, or spread. It is larger when the data values are spread out more from the
> mean, exhibiting more variation. A smaller standard deviation implies less variability in a dataset, and a larger
> standard deviation implies more variability in a dataset.
>
> Suppose that we are studying the variability of two companies (A and B) with respect to employee salaries. The
> average salary for both companies is $60,000. For Company A, the standard deviation of salaries is $8,000,
> whereas the standard deviation for salaries for Company B is $19,000. Because Company B has a higher
> standard deviation, we know that there is more variation in the employee salaries for Company B as compared
> to Company A.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-011-pool-016

**Chunk:** `openstax_principles_ds:4.2:chunk-013`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> Next, calculate the standardized test statistic:
>
> Notice that since the alternative hypothesis contains a “less than” symbol, the hypothesis test is called a
> “left tailed” test and the p-value will be calculated as the area to the left of the test statistic. The area under
> the standard normal curve to the left of a z-score of
>  is approximately 0.0324. Thus, the p-value for
> this hypothesis test is 0.0324.
>
> The area under the standard normal curve can be found using software such as Excel, Python, or R.
>
> For example, in Python, the area under the normal curve to the left of a z-score of
>  can be obtained
> using the function norm.cdf().
>
> The syntax for using this function is
>
> norm.cdf(x, mean, standard_deviation)
>
> Where:
> x is the measurement of interest—in this case, this will be the test statistic of
> .
>
> mean is the mean of the standard normal distribution, which is 0.
>
> standard_deviation is the standard deviation of the standard normal distribution, which is 1.
>
> Here is the Python code to calculate the p-value for this example:
>
> PYTHON CODE
>
> # from scipy.stats import norm
> from scipy.stats import norm
>
> # define parameters x, mean and standard_deviation:
> x = -1.846
> mean = 0
> standard_deviation = 1
> # use norm.cdf function to calculate normal probability - note this is the area
> to the left of the x-value
> # subtract this result from 1 to obtain area to the right of the x-value
> # use round function to round answer to 4 decimal places
> round (norm.cdf(x, mean, standard_deviation), 4)
>
> The resulting output will look like this:
>
> 0.0324
>
> The final step in the hypothesis testing procedure is to come to a final decision regarding the null
>
> hypothesis. This is accomplished by comparing the p-value with the level of significance.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-012

**Pregunta:** With confidence level and population variability held constant, how does a larger sample affect the error bound and the width of a confidence interval?

**Respondibilidad de referencia:** answerable

### q-v1-012-pool-002

**Chunk:** `openstax_intro_stats_2e:8.4:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.4: Confidence Interval (Home Costs)
>
> c. n = _____
>
> 2. In words, define the random variable
> . 3. State the estimated distribution to use. Use both words and symbols.
>
> Find the Confidence Interval
>
> 1. Calculate the confidence interval and the error bound.
> a. Confidence Interval: _____
> b. Error Bound: _____
>
> 2. How much area is in both tails (combined)? α = _____
> 3. How much area is in each tail?
>  = _____
>
> 4. Fill in the blanks on the graph with the area in each section. Then, fill in the number line with the upper and lower
> limits of the confidence interval and the sample mean.
>
> Figure 8.6
>
> 5. Some students think that a 90% confidence interval contains 90% of the data. Use the list of data on the first page
> and count how many of the data values lie within the confidence interval. What percent is this? Is this percent close
> to 90%? Explain why this percent should or should not be close to 90%.
>
> Describe the Confidence Interval
>
> 1. In two to three complete sentences, explain what a confidence interval means (in general), as if you were talking to
> someone who has not taken statistics. 2. In one to two complete sentences, explain what this confidence interval means for this particular study.
>
> Use the Data to Construct Confidence Intervals
>
> 1. Using the given information, construct a confidence interval for each confidence level given.
>
> Confidence level
> EBM/Error Bound
> Confidence Interval
>
> 50%
>
> 80%
>
> 95%
>
> 99%
>
> Table 8.6
>
> 2. What happens to the EBM as the confidence level increases? Does the width of the confidence interval increase or
> decrease? Explain why this happens.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-012-pool-003

**Chunk:** `openstax_principles_ds:4.1:chunk-010`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> The margin of error is calculated as follows:
>
> The 90% confidence interval is calculated as follows:
>
> Concluding statement:
>
> The college professor can forecast with 90% confident that the mean amount of time spent on homework
> assignments in a future semester is the interval from 11.03 to 13.97 hours per week.
>
> Calculation for 95% Confidence Interval
>
> For a 95% confidence interval, the corresponding critical value is
> .
>
> The margin of error is calculated as follows:
>
> The 95% confidence interval is calculated as follows:
>
> Concluding statement:
>
> The college professor can forecast with 95% confident that the mean amount of time spent on homework
> assignments in a future semester is the interval from 10.75 to 14.25 hours per week.
>
> Comparison of 90% and 95% confidence intervals:
>
> The 90% confidence interval extends from 11.03 to 13.97. The 95% confidence interval extends from 10.75 to 14.25.
>
> Notice that the 95% confidence interval is wider. If the confidence level is increased, with all other
>
> parameters held constant, we should expect that the confidence interval will become wider. Another way to
> consider this: the wider the confidence interval, the more likely the interval is to contain the true population
> mean. This makes intuitive sense in that if you want to be more certain that the true value of the parameter
> is within an interval, then the interval needs to be wider to account for a larger range of potential values. As
> an analogy, consider a person trying to catch a fish. The wider the net used, the higher the probability of
> catching a fish.
>
> You might notice that the sample size  is located in the denominator of the formula for margin of error. This indicates that as the sample size increases, the margin of error will decrease, which will then result in a
> narrower confidence interval.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-012-pool-004

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-010`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> = 68
>
> EBM =
>
> σ = 3; n = 36; The confidence level is 95% (CL = 0.95).
>
> CL = 0.95 so α = 1 – CL = 1 – 0.95 = 0.05
>
> The area to the right of z0.025 is 0.025 and the area to the left of z0.025 is 1 – 0.025 = 0.975.
>
> when using invnorm(0.975,0,1) on the TI-83, 83+, or 84+ calculators. (This can also be found using appropriate
> commands on other calculators, using a computer, or using a probability table for the standard normal distribution.)
>
> EBM = (1.96)
>  = 0.98
>
> – EBM = 68 – 0.98 = 67.02
>
> + EBM = 68 + 0.98 = 68.98
>
> Notice that the EBM is larger for a 95% confidence level in the original problem.
>
> We estimate with 95% confidence that the true population mean for all statistics exam scores is between 67.02 and
> 68.98.
>
> Explanation of 95% Confidence Level: Ninety-five percent of all confidence intervals constructed in this way contain the
> true value of the population mean statistics exam score.
>
> Comparing the results: The 90% confidence interval is (67.18, 68.82). The 95% confidence interval is (67.02, 68.98). The
> 95% confidence interval is wider. If you look at the graphs, because the area 0.95 is larger than the area 0.90, it makes
> sense that the 95% confidence interval is wider. To be more confident that the confidence interval actually does contain
> the true value of the population mean for all statistics exam scores, the confidence interval necessarily needs to be
> wider.
>
> Figure 8.5
>
> Summary: Effect of Changing the Confidence Level
>
> • Increasing the confidence level increases the error bound, making the confidence interval wider.
> • Decreasing the confidence level decreases the error bound, making the confidence interval narrower.
>
> TRY IT 8.4
>
> Refer back to the pizza-delivery Try It exercise.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-012-pool-006

**Chunk:** `openstax_principles_ds:4.1:chunk-004`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> An unbiased estimator is a statistic that provides an
> accurate estimate for the corresponding population parameter without overestimating or underestimating the
> parameter.
>
> In order to calculate a confidence interval, two quantities are needed:
>
> • The point estimate
> • The margin of error
>
> As noted, the point estimate is a single number that is used to estimate the population parameter. The margin
> of error (usually denoted by E) provides an indication of the maximum error of the estimate. The margin of
> error can be viewed as the maximum distance around the point estimate where the population parameter
> exists based on a specified confidence.
>
> Once the point estimate and margin of error are determined, the confidence interval is calculated as follows:
>
> The margin of error reflects the desired confidence level of the researcher. The confidence level is the
> probability that the interval estimate will contain the population parameter, given that the estimation process
> on the parameter is repeated over and over. Confidence levels typically range from 80% to 95% confidence.
>
> In addition to the confidence level, both the variability of the sample and the sample size will affect the margin
> of error.
>
> Once the confidence interval has been calculated, a concluding statement is made that reflects both the
> confidence level and the unknown population parameter. The concluding statement indicates that there is a
> certain level of confidence that the population parameter is contained within the bounds of the confidence
> interval.
>
> As an example, consider a data scientist who is interested in forecasting the median income for all residents of
> California. Income data is collected from a sample of 1,000 residents, and the median income level is $68,500. Also assume the margin of error for a 95% confidence interval is $4,500 (more details on the calculation of
> margin of error are provided next).

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-012-pool-007

**Chunk:** `openstax_principles_ds:4.1:chunk-017`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Too large of a sample size can result in wasted resources if a smaller sample
> size would be sufficient. Sampling is covered in some depth in Handling Large Datasets. Here, we review
> methods to determine minimum sample size requirements when constructing confidence intervals for means
> or proportions. Note that the desired margin of error plays a key role in this sample size determination.
>
> Sample Size for Confidence Interval for the Mean
>
> When determining a confidence interval for a mean, a researcher can use the margin of error formula for the
> mean; solving this formula algebraically for the sample size ( ), the following minimum sample size formula
> can be used to determine the minimum sample size needed to achieve a certain margin of error:
>
> Sample size formula for confidence interval for mean:
>
> Where:
>
> is the critical value of the normal distribution.
>  is the population standard deviation.
>
> is the desired margin of error.
>
> Note that for sample size calculations, sample size results are rounded up to the next higher whole number.
>
> For example, if the formula previously shown results in a sample size of 59.2, then the sample size will be
> rounded to 60.
>
> EXAMPLE 4.6
>
> Problem
>
> A benefits analyst is interested in a 90% confidence interval for the mean salary for chemical engineers. What sample size should the analyst use if a margin of error of $1,000 is desired? Assume a population
> standard deviation of $8,000.
>
> Solution
>
> For a 90% confidence interval, the corresponding critical value is
> . The population standard
> deviation is given as $8,000, and the margin of error is given as $1,000.
>
> Using the sample size formula:
>
> Round to the next higher whole number, so the desired sample size is 174.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-012-pool-008

**Chunk:** `openstax_intro_stats_2e:8.5:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.5: Confidence Interval (Place of Birth)
>
> 8.5 Confidence Interval (Place of Birth)
>
> Stats Lab
>
> Confidence Interval (Place of Birth)
> Class Time:
>
> Names:
>
> Student Learning Outcomes
>
> • The student will calculate the 90% confidence interval the proportion of students in this school who were born in
> this state.
> • The student will interpret confidence intervals.
> • The student will determine the effects of changing conditions on the confidence interval.
>
> Collect the Data
>
> 1. Survey the students in your class, asking them if they were born in this state. Let X = the number that were born in
> this state.
>
> a. n = ____________
> b. x = ____________
>
> 2. In words, define the random variable P′. 3. State the estimated distribution to use.
>
> Find the Confidence Interval and Error Bound
>
> 1. Calculate the confidence interval and the error bound.
> a. Confidence Interval: _____
> b. Error Bound: _____
>
> 2. How much area is in both tails (combined)? α = _____
> 3. How much area is in each tail?
>  = _____
>
> 4. Fill in the blanks on the graph with the area in each section. Then, fill in the number line with the upper and lower
> limits of the confidence interval and the sample proportion.
>
> Figure 8.7
>
> Describe the Confidence Interval
>
> 1. In two to three complete sentences, explain what a confidence interval means (in general), as though you were
> talking to someone who has not taken statistics. 2. In one to two complete sentences, explain what this confidence interval means for this particular study. 3. Construct a confidence interval for each confidence level given.
>
> Confidence level
> EBP/Error Bound
> Confidence Interval
>
> 50%
>
> 80%
>
> Table 8.7

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-012-pool-009

**Chunk:** `openstax_principles_ds:4.1:chunk-011`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> The wider the net used, the higher the probability of
> catching a fish.
>
> You might notice that the sample size  is located in the denominator of the formula for margin of error. This indicates that as the sample size increases, the margin of error will decrease, which will then result in a
> narrower confidence interval. On the other hand, as the sample size decreases, the margin of error
> increases and the confidence interval becomes wider.
>
> Confidence Interval for the Mean When the Population Standard Deviation Is
> Unknown
>
> A confidence interval can still be determined when the population standard deviation is unknown by
> calculating a sample standard deviation based on the sample data. This is actually the more common
> application of confidence intervals.
>
> Here are the conditions required to use this procedure:
>
> a. A random sample is selected from the population.
> b. The sample size is at least 30, or the underlying population is known to follow a normal distribution.
>
> c. The population standard deviation ( ) is unknown; the sample standard deviation
>  can be calculated.
>
> Once these requirements are met, the margin of error (E) is calculated according to the following formula:
>
> is called the critical value of the t-distribution. The t-distribution is a bell-shaped, symmetric distribution
> similar to the normal distribution, though the t-distribution has “thicker tails” as compared to the normal
> distribution. The comparison of the normal and t-distribution curves is shown in Figure 4.3.
>
> Figure 4.3 Comparison of t-Distribution and Normal Distribution Curves
>
> The t-distribution is actually a family of curves, determined by a parameter called degrees of freedom (df),
> where df is equal to
> . The critical value
>  is similar to a z-score and specifies the area under the t-
> distribution curve corresponding to the confidence level between
>  and
> .

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-012-pool-010

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> The margin of error (EBM) depends on the confidence level (abbreviated CL). The confidence level is often considered
> the probability that the calculated confidence interval estimate will contain the true population parameter. However, it is
> more accurate to state that the confidence level is the percent of confidence intervals that contain the true population
> parameter when repeated samples are taken. Most often, it is the choice of the person constructing the confidence
> interval to choose a confidence level of 90% or higher because that person wants to be reasonably certain of their
> conclusions.
>
> There is another probability called alpha (α). α is related to the confidence level, CL. α is the probability that the interval
> does not contain the unknown population parameter. Mathematically, α + CL = 1.
>
> EXAMPLE 8.1
>
> Suppose we have collected data from a sample. We know the sample mean but we do not know the mean for the entire
> population. The sample mean is seven, and the error bound for the mean is 2.5.
>
> = 7 and EBM = 2.5
>
> The confidence interval is (7 – 2.5, 7 + 2.5), and calculating the values gives (4.5, 9.5).
>
> If the confidence level (CL) is 95%, then we say that, "We estimate with 95% confidence that the true value of the
> population mean is between 4.5 and 9.5."
>
> TRY IT 8.1
>
> Suppose we have data from a sample. The sample mean is 15, and the error bound for the mean is 3.2.
>
> What is the confidence interval estimate for the population mean?
>
> A confidence interval for a population mean with a known standard deviation is based on the fact that the sample means
> follow an approximately normal distribution.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-012-pool-011

**Chunk:** `openstax_intro_stats_2e:8.3:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.3: A Population Proportion
>
> The random variable
>  (read "P prime")
>
> is that proportion,
>
> (Sometimes the random variable is denoted as
> , read "P hat".)
>
> When n is large and p is not close to zero or one, we can use the normal distribution to approximate the binomial.
>
> If we divide the random variable, the mean, and the standard deviation by n, we get a normal distribution of proportions
> with
> , called the estimated proportion, as the random variable. (Recall that a proportion as the number of successes
> divided by n.)
>
> Using algebra to simplify :
>
> follows a normal distribution for proportions:
>
> The confidence interval has the form (
>  – EBP,
>  + EBP). EBP is error bound for the proportion.
>
> =
>
> = the estimated proportion of successes (
>  is a point estimate for p, the true proportion.)
>
> x = the number of successes
>
> n = the size of the sample
>
> The error bound for a proportion is
>
> where
>  = 1 –
>
> This formula is similar to the error bound formula for a mean, except that the "appropriate standard deviation" is
> different. For a mean, when the population standard deviation is known, the appropriate standard deviation that we use
>
> is
> . For a proportion, the appropriate standard deviation is
> .
>
> However, in the error bound formula, we use
>  as the standard deviation, instead of
> .
>
> In the error bound formula, the sample proportions
>  and
>  are estimates of the unknown population proportions
> p and q. The estimated proportions
>  and
>  are used because p and q are not known. The sample proportions
>  and
>  are calculated from the data:
>  is the estimated proportion of successes, and
>  is the estimated proportion of
> failures.
>
> The confidence interval can be used only if the number of successes
>  and the number of failures
>  are both greater
> than five.
>
> NOTE

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-012-pool-012

**Chunk:** `openstax_intro_stats_2e:8.3:chunk-010`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.3: A Population Proportion
>
> Solution
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> Press STAT and arrow over to TESTS.
>
> Arrow down to A:1-PropZint. Press ENTER.
>
> Arrow down to x and enter 15. Arrow down to n and enter 54. Arrow down to C-Level and enter 0.90.
>
> Arrow down to Calculate and press ENTER.
>
> The confidence interval is (0.178, 0.378).
>
> TRY IT 8.13
>
> The survey referenced in Example 8.13 talked to adults aged 18–29 in smaller focus groups but also interviewed
> additional individuals over the phone. When the study was complete, 588 adults aged 18–29 had answered the
> question about their potential purchase of an electric vehicle with 159 saying that they would consider such a
> purchase. Use the “plus-four” method to find a 90% confidence interval for the true proportion of adults aged 18–29
> who would consider the purchase of an electric vehicle based on this larger sample. Compare the results to those in
> Example 8.13.
>
> Calculating the Sample Size n
>
> If researchers desire a specific margin of error, then they can use the error bound formula to calculate the required
> sample size.
>
> The error bound formula for a population proportion is
>
> •
>
> • Solving for n gives you an equation for the sample size.
>
> •
>
> EXAMPLE 8.14
>
> Problem
> Suppose a mobile phone company wants to determine the current percentage of customers aged 50+ who use text
> messaging on their cell phones. How many customers aged 50+ should the company survey in order to be 90%
> confident that the estimated (sample) proportion is within three percentage points of the true population proportion of
> customers aged 50+ who use text messaging on their cell phones.
>
> Solution
> From the problem, we know that EBP = 0.03 (3%=0.03) and
>  z0.05 = 1.645 because the confidence level is 90%.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-012-pool-013

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> Use n = 217: Always round the answer UP to the next higher integer to ensure that the sample size is large enough.
>
> Therefore, 217 Foothill College students should be surveyed in order to be 95% confident that we are within two years of
> the true population mean age of Foothill College students.
>
> TRY IT 8.7
>
> The population standard deviation for the height of high school basketball players is three inches. If we want to be
> 95% confident that the sample mean height is within one inch of the true population mean height, how many
> randomly selected students must be surveyed?
>
> 8.2 A Single Population Mean using the Student t Distribution
>
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

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-012-pool-014

**Chunk:** `openstax_intro_stats_2e:8.6:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.6: Confidence Interval (Women's Heights)
>
> Confidence level
> EBP/Error Bound
> Confidence Interval
>
> 95%
>
> 99%
>
> Table 8.7
>
> 4. What happens to the EBP as the confidence level increases? Does the width of the confidence interval increase or
> decrease? Explain why this happens.
>
> 8.6 Confidence Interval (Women's Heights)
>
> Stats Lab
>
> Confidence Interval (Women's Heights)
> Class Time:
>
> Names:
>
> Student Learning Outcomes
>
> • The student will calculate a 90% confidence interval using the given data.
> • The student will determine the relationship between the confidence level and the percentage of constructed
> intervals that contain the population mean.
>
> Given:
>
> 59.4
> 71.6
> 69.3
> 65.0
> 62.9
> 66.5
> 61.7
> 55.2
>
> 67.5
> 67.2
> 63.8
> 62.9
> 63.0
> 63.9
> 68.7
> 65.5
>
> 61.9
> 69.6
> 58.7
> 63.4
> 61.8
> 60.6
> 69.8
> 60.0
>
> 64.9
> 66.1
> 66.8
> 60.6
> 65.6
> 63.8
> 61.3
> 59.2
>
> 64.1
> 59.3
> 64.9
> 62.4
> 63.5
> 60.9
> 63.3
> 66.3
>
> 61.5
> 64.3
> 62.9
> 60.6
> 63.8
> 58.8
> 64.9
> 65.7
>
> 62.5
> 70.9
> 62.9
> 63.1
> 62.2
> 58.7
> 64.7
> 66.0
>
> 60.5
> 64.7
> 65.4
> 60.2
> 65.0
> 64.1
> 61.1
> 65.3
>
> 64.6
> 59.2
> 61.4
> 62.0
> 63.5
> 61.4
> 65.5
> 62.3
>
> 65.5
> 64.7
> 58.8
> 66.1
> 64.9
> 66.9
> 57.9
> 69.8
>
> 58.5
> 63.4
> 69.2
> 65.9
> 62.2
> 60.0
> 58.1
> 62.5
>
> Table 8.8 Heights of 100 Women (in Inches)
>
> 62.4
> 59.1
> 66.4
> 61.2
> 60.4
> 58.7
> 66.7
> 67.5
>
> 63.2
> 56.6
> 67.7
> 62.5
>
> Table 8.8 Heights of 100 Women (in Inches)
>
> 1. Table 8.8 lists the heights of 100 women. Use a random number generator to select ten data values randomly. 2. Calculate the sample mean and the sample standard deviation. Assume that the population standard deviation is
> known to be 3.3 inches. With these values, construct a 90% confidence interval for your sample of ten values. Write
> the confidence interval you obtained in the first space of Table 8.9. 3. Now write your confidence interval on the board. As others in the class write their confidence intervals on the board,
> copy them into Table 8.9.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-012-pool-015

**Chunk:** `openstax_principles_ds:4.1:chunk-018`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Assume a population
> standard deviation of $8,000.
>
> Solution
>
> For a 90% confidence interval, the corresponding critical value is
> . The population standard
> deviation is given as $8,000, and the margin of error is given as $1,000.
>
> Using the sample size formula:
>
> Round to the next higher whole number, so the desired sample size is 174.
>
> The analyst should target a sample size of 174 chemical engineers for a salary-related survey in order to
> them calculate a 90% confidence interval for the mean salary of chemical engineers.
>
> Sample Size for Confidence interval for a Proportion
>
> In Example 4.5, how would the researcher know the optimal sample size to use to collect sample data on the
> proportion of adults who are smokers? The margin of error formula can be used to derive the sample size for a
> proportion as follows:
>
> Where:
>
> is the critical value of the normal distribution.
>  is the sample proportion.
>
> is the desired margin of error.
>
> Notice in this formula, it’s assumed that some prior estimate for the sample proportion  is available, perhaps
> from historical data or previous studies. If a prior estimate for the sample proportion is not available, then use
> the value of 0.5 for .
>
> DETERMINING SAMPLE SIZE
>
> When determining sample size needed for a confidence interval for a proportion:
>
> If a prior estimate for the sample proportion is available, then that prior estimate should be utilized.
>
> • If a prior estimate for the sample proportion is not available, then use
> .
>
> EXAMPLE 4.7
>
> Problem
>
> Political candidate Smith is planning a survey to determine a 95% confidence interval for the proportion of
> voters who plan to vote for Smith. How many people should be surveyed? Assume a margin of error is 3%.
>
> a.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-012-pool-016

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> Calculate the Sample Mean:
> • If we know the error bound:  = 68.82 – 0.82 = 68
>
> • If we don't know the error bound:  =
>  = 68.
>
> TRY IT 8.6
>
> Suppose we know that a confidence interval is (42.12, 47.88). Find the error bound and the sample mean.
>
> Calculating the Sample Size n
>
> If researchers desire a specific margin of error, then they can use the error bound formula to calculate the required
> sample size.
>
> The error bound formula for a population mean when the population standard deviation is known is
>
> EBM =
> .
>
> The formula for sample size is n =
> , found by solving the error bound formula for n.
>
> In this formula, z is
> , corresponding to the desired confidence level. A researcher planning a study who wants a
>
> specified confidence level and error bound can use this formula to calculate the size of the sample needed for the study.
>
> EXAMPLE 8.7
>
> The population standard deviation for the age of Foothill College students is 15 years. If we want to be 95% confident
> that the sample mean age is within two years of the true population mean age of Foothill College students, how many
> randomly selected Foothill College students must be surveyed?
>
> From the problem, we know that σ = 15 and EBM = 2.
> z = z0.025 = 1.96, because the confidence level is 95%.
>
> n =
>  =
>  = 216.09 using the sample size equation.
>
> Use n = 217: Always round the answer UP to the next higher integer to ensure that the sample size is large enough.
>
> Therefore, 217 Foothill College students should be surveyed in order to be 95% confident that we are within two years of
> the true population mean age of Foothill College students.
>
> TRY IT 8.7

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-013

**Pregunta:** Which distribution should be used to construct a confidence interval for a population mean when the population standard deviation is known versus when it is estimated by the sample standard deviation, and how do degrees of freedom enter the Student t case?

**Respondibilidad de referencia:** answerable

### q-v1-013-pool-002

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-006`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> A Student's t table (See Appendix H Tables) gives t-scores given the degrees of freedom and the right-tailed probability. The table is very limited. Calculators and computers can easily calculate any Student's t-probabilities.
>
> The notation for the Student's t-distribution (using T as the random variable) is:
>
> • T ~ tdf where df = n – 1.
> • For example, if we have a sample of size n = 20 items, then we calculate the degrees of freedom as df = n - 1 = 20 - 1
> = 19 and we write the distribution as T ~ t19.
>
> If the population standard deviation is not known, the error bound for a population mean is:
>
> •
> ,
>
> •
>  is the t-score with area to the right equal to
> ,
>
> • use df = n – 1 degrees of freedom, and
>
> • s = sample standard deviation.
>
> The format for the confidence interval is:
>
> .
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> To calculate the confidence interval directly:
> Press STAT.
>
> Arrow over to TESTS.
>
> Arrow down to 8:TInterval and press ENTER (or just press 8).
>
> EXAMPLE 8.8
>
> Problem
> Suppose you do a study of acupuncture to determine how effective it is in relieving pain. You measure sensory rates for
> 15 subjects with the results given. Use the sample data to construct a 95% confidence interval for the mean sensory rate
> for the population (assumed normal) from which you took the data. The solution is shown step-by-step and by using the TI-83, 83+, or 84+ calculators.
>
> 8.6; 9.4; 7.9; 6.8; 8.3; 7.3; 9.2; 9.6; 8.7; 11.4; 10.3; 5.4; 8.1; 5.5; 6.9
> Solution
> • The first solution is step-by-step.
> • The second solution uses the TI-83+ and TI-84 calculators.
>
> To find the confidence interval, you need the sample mean, , and the EBM.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-013-pool-003

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-004`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> This calculation requires n
> deviations
> . Because the sum of the deviations is zero, we can find the last deviation once we know the other
> n – 1 deviations. The other n – 1 deviations can change or vary freely. We call the number n – 1 the degrees of freedom
> (df).
>
> Properties of the Student's t-Distribution
>
> • The graph for the Student's t-distribution is similar to the standard normal curve.
> • The mean for the Student's t-distribution is zero and the distribution is symmetric about zero.
> • The Student's t-distribution has more probability in its tails than the standard normal distribution because the
> spread of the t-distribution is greater than the spread of the standard normal. So the graph of the Student's t-
> distribution will be thicker in the tails and shorter in the center than the graph of the standard normal distribution.
> • The exact shape of the Student's t-distribution depends on the degrees of freedom. As the degrees of freedom
> increases, the graph of Student's t-distribution becomes more like the graph of the standard normal distribution.
> • The underlying population of individual observations is assumed to be normally distributed with unknown
> population mean μ and unknown population standard deviation σ. The size of the underlying population is
> generally not relevant unless it is very small. If it is bell shaped (normal) then the assumption is met and doesn't
> need discussion. Random sampling is assumed, but that is a completely separate assumption from normality.
>
> Calculators and computers can easily calculate any Student's t-probabilities. The TI-83,83+, and 84+ have a tcdf function
> to find the probability for given values of t. The grammar for the tcdf command is tcdf(lower bound, upper bound,
> degrees of freedom).

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-013-pool-004

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-008`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> NOTE
>
> When calculating the error bound, a probability table for the Student's t-distribution can also be used to find the value
> of t. The table gives t-scores that correspond to the confidence level (column) and degrees of freedom (row); the
> t-score is found where the row and column intersect in the table.
>
> TRY IT 8.8
>
> You do a study of hypnotherapy to determine how effective it is in increasing the number of hours of sleep subjects
> get each night. You measure hours of sleep for 12 subjects with the following results. Construct a 95% confidence
> interval for the mean number of hours slept for the population (assumed normal) from which you took the data.
>
> 8.2; 9.1; 7.7; 8.6; 6.9; 11.2; 10.1; 9.9; 8.9; 9.2; 7.5; 10.5
>
> EXAMPLE 8.9
>
> Problem
> The Human Toxome Project (HTP) is working to understand the scope of industrial pollution in the human body. Industrial chemicals may enter the body through pollution or as ingredients in consumer products. The scientists at HTP
> tested cord blood samples for 20 newborn infants in the United States. The cord blood of the "In utero/newborn" group
> was tested for 430 industrial compounds, pollutants, and other chemicals, including chemicals linked to brain and
> nervous system toxicity, immune system toxicity, and reproductive toxicity, and fertility problems. There are health
> concerns about the effects of some chemicals on the brain and nervous system. Table 8.3 shows how many of the
> targeted chemicals were found in each infant’s cord blood.
>
> 79
> 145
> 147
> 160
> 116
> 100
> 159
> 151
> 156
> 126
>
> 137
> 83
> 156
> 94
> 121
> 144
> 123
> 114
> 139
> 99
>
> Table 8.3
>
> Use this sample data to construct a 90% confidence interval for the mean number of targeted industrial chemicals to be
> found in an in infant’s blood.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-013-pool-005

**Chunk:** `openstax_principles_ds:4.1:chunk-011`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> The wider the net used, the higher the probability of
> catching a fish.
>
> You might notice that the sample size  is located in the denominator of the formula for margin of error. This indicates that as the sample size increases, the margin of error will decrease, which will then result in a
> narrower confidence interval. On the other hand, as the sample size decreases, the margin of error
> increases and the confidence interval becomes wider.
>
> Confidence Interval for the Mean When the Population Standard Deviation Is
> Unknown
>
> A confidence interval can still be determined when the population standard deviation is unknown by
> calculating a sample standard deviation based on the sample data. This is actually the more common
> application of confidence intervals.
>
> Here are the conditions required to use this procedure:
>
> a. A random sample is selected from the population.
> b. The sample size is at least 30, or the underlying population is known to follow a normal distribution.
>
> c. The population standard deviation ( ) is unknown; the sample standard deviation
>  can be calculated.
>
> Once these requirements are met, the margin of error (E) is calculated according to the following formula:
>
> is called the critical value of the t-distribution. The t-distribution is a bell-shaped, symmetric distribution
> similar to the normal distribution, though the t-distribution has “thicker tails” as compared to the normal
> distribution. The comparison of the normal and t-distribution curves is shown in Figure 4.3.
>
> Figure 4.3 Comparison of t-Distribution and Normal Distribution Curves
>
> The t-distribution is actually a family of curves, determined by a parameter called degrees of freedom (df),
> where df is equal to
> . The critical value
>  is similar to a z-score and specifies the area under the t-
> distribution curve corresponding to the confidence level between
>  and
> .

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-013-pool-006

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-007`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> The solution is shown step-by-step and by using the TI-83, 83+, or 84+ calculators.
>
> 8.6; 9.4; 7.9; 6.8; 8.3; 7.3; 9.2; 9.6; 8.7; 11.4; 10.3; 5.4; 8.1; 5.5; 6.9
> Solution
> • The first solution is step-by-step.
> • The second solution uses the TI-83+ and TI-84 calculators.
>
> To find the confidence interval, you need the sample mean, , and the EBM.
>
> = 8.2267 s = 1.6722 n = 15
>
> df = 15 – 1 = 14 CL so α = 1 – CL = 1 – 0.95 = 0.05
>
> = 0.025
>
> The area to the right of t0.025 is 0.025, and the area to the left of t0.025 is 1 – 0.025 = 0.975
>
> using invT(.975,14) on the TI-84+ calculator.
>
> – EBM = 8.2267 – 0.9240 = 7.3
>
> + EBM = 8.2267 + 0.9240 = 9.15
>
> The 95% confidence interval is (7.30, 9.15).
>
> We estimate with 95% confidence that the true population mean sensory rate is between 7.30 and 9.15.
>
> Solution
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> Press STAT and arrow over to TESTS.
>
> Arrow down to 8:TInterval and press ENTER (or you can just press 8).
>
> Arrow to Data and press ENTER.
>
> Arrow down to List and enter the list name where you put the data.
>
> There should be a 1 after Freq.
>
> Arrow down to C-level and enter 0.95
>
> Arrow down to Calculate and press ENTER.
>
> The 95% confidence interval is (7.3006, 9.1527)
>
> NOTE
>
> When calculating the error bound, a probability table for the Student's t-distribution can also be used to find the value
> of t. The table gives t-scores that correspond to the confidence level (column) and degrees of freedom (row); the
> t-score is found where the row and column intersect in the table.
>
> TRY IT 8.8

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-013-pool-007

**Chunk:** `openstax_principles_ds:4.1:chunk-012`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Figure 4.3 Comparison of t-Distribution and Normal Distribution Curves
>
> The t-distribution is actually a family of curves, determined by a parameter called degrees of freedom (df),
> where df is equal to
> . The critical value
>  is similar to a z-score and specifies the area under the t-
> distribution curve corresponding to the confidence level between
>  and
> . Values of
>  can be obtained
> using either a look-up table or technology.
>
> For example, for a 95% confidence interval and sample size of 30, the corresponding critical value is
> since an area of 0.95 under the t-distribution curve is contained between the t-scores of
>  and
> .
>
> is the sample standard deviation.
>
> is the sample size.
>
> df is degrees of freedom, where
> .
>
> Typical values of
>  for various confidence levels and degrees of freedom are shown in Table 4.3.
>
> Confidence Level
>
> 90% Confidence
> 95% Confidence
> 99% Confidence
>
> Degrees of
> Freedom (df)
>
> 1
> 6.314
> 12.706
> 63.657
>
> 2
> 2.920
> 4.203
> 9.925
>
> 3
> 2.353
> 3.182
> 5.841
>
> 4
> 2.132
> 2.776
> 4.604
>
> 5
> 2.015
> 2.571
> 4.032
>
> 10
> 1.812
> 2.228
> 3.169
>
> 15
> 1.753
> 2.131
> 2.947
>
> 20
> 1.725
> 2.086
> 2.845
>
> 25
> 1.708
> 2.060
> 2.787
>
> 30
> 1.697
> 2.042
> 2.750
>
> Table 4.3 Typical Values of
>  for Various Confidence Levels and Degrees of Freedom
>
> Note that Python can be used to calculate these critical values. Python provides a function called t.ppf() that
>
> generates the value of the t-distribution corresponding to a specified area under the t-distribution curve and
> specified degrees of freedom. This function is part of the scipy.stats library (https://openstax.org/r/stats).
>
> The syntax for the function is:
> t.ppf(area to left, degrees of freedom)
>
> For example, for a 95% confidence interval, there is an area of 0.95 centered under the t-distribution curve,
> which leaves a remaining area of 0.05 for the two tails of the distribution, which implies an area of 0.025 in
> each tail.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-013-pool-008

**Chunk:** `openstax_principles_ds:4.1:chunk-025`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> #print the confidence interval
> print(conf_interval.confidence_interval)
>
> The resulting output will look like this:
>
> ConfidenceInterval(low=22.45, high=26.7)
>
> Using 50,000 bootstrapped samples, a 95% confidence interval is generated as (22.45, 26.7).
>
> EXPLORING FURTHER
>
> Simulating Confidence Intervals
>
> A number of websites and resources, such as the online textbook Online Statistics Education: A Multimedia
> Course of Study (https://openstax.org/r/estimation) (http://onlinestatbook.com/) (project leader: David M. Lane, Rice University), allow the user to simulate confidence intervals for means or proportions using
> simulated sample data. It is useful to observe how many intervals contain an assumed value for the
> population mean or population proportion. The Stapplet (https://openstax.org/r/stapplet) website provides
> a similar tool.
>
> Using Python to Calculate Confidence Intervals
>
> When calculating confidence intervals, data scientists typically make use of technology to help streamline and
> automate the analysis. Python provides built-in functions for confidence interval calculations, and several
> examples are shown in Table 4.5. Students are encouraged to try examples themselves and experiment to use
> Python to assist with these calculations.
>
> Table 4.5 provides a summary of various functions available within the SciPy library (https://openstax.org/
>
> r/spy) for confidence interval calculations:
>
> Usage
> Python Function Name
> Syntax
>
> norm.interval()
> norm.interval(conf_level,
> sample_mean,standard_dev/
> sqrt
>
> (n))
>
> Calculate confidence interval for
> the mean when population
> standard deviation is known,
> given sample mean, population
> standard deviation, and sample
> size (uses normal distribution).
>
> t.interval()
> t.interval(conf_level,
> degrees_freedom,
> sample_mean,standard_dev/
> sqrt
>
> (n))
>
> Calculate confidence interval for
> the mean when population
> standard deviation is unknown,
> given sample mean, sample
> standard deviation, and sample
> size (uses t-distribution).
>
> Calculate confidence interval for
> a proportion (uses normal
> distribution).
>
> proportion_confint()
> proportion_confint(success,
> sample_size,
> 1 – confidence_level)
>
> Table 4.5 Python Functions for Confidence Intervals
>
> EXAMPLE 4.9
>
> Problem
>
> Repeat Example 4.3 to calculate a 90% confidence interval, but use Python functions to calculate the
> confidence interval.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-013-pool-010

**Chunk:** `openstax_intro_stats_2e:9.4:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.4: Rare Events, the Sample, Decision and Conclusion
>
> Assumptions
>
> When you perform a hypothesis test of a single population mean μ using a normal distribution (often called a z-test), you
> take a simple random sample from the population. The population you are testing is normally distributed, or your
> sample size is sufficiently large. You know the value of the population standard deviation, which, in reality, is rarely
> known.
>
> When you perform a hypothesis test of a single population mean μ using a Student's t-distribution (often called a
> t-test), there are fundamental assumptions that need to be met in order for the test to work properly. Your data should
> be a simple random sample that comes from a population that is approximately normally distributed. You use the
> sample standard deviation to approximate the population standard deviation. (Note that if the sample size is sufficiently
> large, a t-test will work even if the population is not approximately normally distributed).
>
> When you perform a hypothesis test of a single population proportion p, you take a simple random sample from the
> population. You must meet the conditions for a binomial distribution: there are a certain number n of independent
> trials, the outcomes of any trial are success or failure, and each trial has the same probability of a success p. The shape
> of the binomial distribution needs to be similar to the shape of the normal distribution. To ensure this, the quantities np
> and nq must both be greater than five (
>  and
> ). Then the binomial distribution of a sample (estimated)
>
> proportion can be approximated by the normal distribution with
>  and
> . Remember that
> .
>
> 9.4 Rare Events, the Sample, Decision and Conclusion
>
> Establishing the type of distribution, sample size, and known or unknown standard deviation can help you figure out
> how to go about a hypothesis test.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-013-pool-011

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-005`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> Random sampling is assumed, but that is a completely separate assumption from normality.
>
> Calculators and computers can easily calculate any Student's t-probabilities. The TI-83,83+, and 84+ have a tcdf function
> to find the probability for given values of t. The grammar for the tcdf command is tcdf(lower bound, upper bound,
> degrees of freedom). However for confidence intervals, we need to use inverse probability to find the value of t when we
> know the probability.
>
> For the TI-84+ you can use the invT command on the DISTRibution menu. The invT command works similarly to the
> invnorm. The invT command requires two inputs: invT(area to the left, degrees of freedom) The output is the t-score
> that corresponds to the area we specified.
>
> The TI-83 and 83+ do not have the invT command. (The TI-89 has an inverse T command.)
>
> A probability table for the Student's t-distribution can also be used. The table gives t-scores that correspond to the
> confidence level (column) and degrees of freedom (row). (The TI-86 does not have an invT program or command, so if
> you are using that calculator, you need to use a probability table for the Student's t-Distribution.) When using a t-table,
> note that some tables are formatted to show the confidence level in the column headings, while the column headings in
> some tables may show only corresponding area in one or both tails.
>
> A Student's t table (See Appendix H Tables) gives t-scores given the degrees of freedom and the right-tailed probability. The table is very limited. Calculators and computers can easily calculate any Student's t-probabilities.
>
> The notation for the Student's t-distribution (using T as the random variable) is:

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-013-pool-012

**Chunk:** `openstax_principles_ds:4.2:chunk-011`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> Row 3
> Fail to reject the null
> hypothesis
>
> Claim is the null
> hypothesis
>
> There is not enough
> evidence to reject the
> claim.
>
> Row 4
> Fail to reject the null
> hypothesis
>
> Claim is the alternative
> hypothesis
>
> There is not enough
> evidence to support the
> claim.
>
> Table 4.8 How to Establish a Conclusion from a Hypothesis Test
>
> Testing Claims for the Mean When the Population Standard Deviation Is Known
>
> Recall that in the discussion for confidence intervals we examined the confidence interval for the population
> mean when the population standard deviation is known (normal distribution is used) or when the population
> standard deviation is unknown (t-distribution is used). We follow the same procedure when conducting
> hypothesis tests.
>
> In this section, we discuss hypothesis testing for the mean when the population standard deviation is known. Although the population standard deviation is typically unknown, in some cases a reasonable estimate for the
> population standard deviation can be obtained from past studies or historical data.
>
> Here are the requirements to use this procedure:
>
> a. A random sample is selected from the population.
> b. The sample size is at least 30, or the underlying population is known to follow a normal distribution.
>
> c. The population standard deviation ( ) is known.
>
> When these requirements are met, the normal distribution is used as the basis for conducting the hypothesis
> test.
>
> For this procedure, the test statistic will be a z-score and the standardized test statistic is calculated as follows:
>
> Where:
>
> is the sample mean.
>  is the hypothesized value of the population mean, which comes from the null hypothesis.
>  is the population standard deviation.
>  is the sample size.
>
> Example 4.13 provides a step-by-step example to illustrate the hypothesis testing process.
>
> EXAMPLE 4.13
>
> Problem

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-013-pool-013

**Chunk:** `openstax_intro_stats_2e:8.intro:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.intro: Introduction
>
> We use sample data to make generalizations about an unknown population. This part of statistics is called inferential
> statistics. The sample data help us to make an estimate of a population parameter. We realize that the point
> estimate is most likely not the exact value of the population parameter, but close to it. After calculating point estimates,
> we construct interval estimates, called confidence intervals.
>
> In this chapter, you will learn to construct and interpret confidence intervals. You will also learn a new distribution, the
> Student's-t, and how it is used with these intervals. Throughout the chapter, it is important to keep in mind that the
>
> confidence interval is a random variable. It is the population parameter that is fixed.
>
> If you worked in the marketing department of an entertainment company, you might be interested in the mean number
> of songs a consumer downloads a month from Apple Music. If so, you could conduct a survey and calculate the sample
> mean, , and the sample standard deviation, s. You would use  to estimate the population mean and s to estimate the
> population standard deviation. The sample mean, , is the point estimate for the population mean, μ. The sample
> standard deviation, s, is the point estimate for the population standard deviation, σ.
>
> Each of  and s is called a statistic.
>
> A confidence interval is another type of estimate but, instead of being just one number, it is an interval of numbers. It
> provides a range of reasonable values in which we expect the population parameter to fall. There is no guarantee that a
> given confidence interval does capture the parameter, but there is a predictable probability of success.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-013-pool-014

**Chunk:** `openstax_principles_ds:4.1:chunk-026`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Calculate confidence interval for
> a proportion (uses normal
> distribution).
>
> proportion_confint()
> proportion_confint(success,
> sample_size,
> 1 – confidence_level)
>
> Table 4.5 Python Functions for Confidence Intervals
>
> EXAMPLE 4.9
>
> Problem
>
> Repeat Example 4.3 to calculate a 90% confidence interval, but use Python functions to calculate the
> confidence interval.
>
> Recall from Example 4.3, the sample mean is 12.5 hours with a population standard deviation of 6.3 hours. The sample size is 50 students, and we are interested in calculating a 90% confidence interval.
>
> Solution
>
> Use the Python function norm.interval() as shown:
>
> PYTHON CODE
>
> import scipy.stats as stats
> import numpy as np
> import math
>
> # Enter sample mean, population standard deviation and sample size
> sample_mean = 12.5
> population_standard_deviation = 6.3
> sample_size = 50
>
> # Confidence level
> confidence_level = 0.90
>
> # standard error
> standard_error = population_standard_deviation / math.sqrt(sample_size)
>
> # Calculate confidence interval using norm.interval function
> stats.norm.interval(confidence_level, sample_mean, standard_error)
>
> The resulting output will look like this:
>
> (11.03451018636739, 13.965489813632608)
>
> EXAMPLE 4.10
>
> Problem
>
> Repeat Example 4.4 to calculate a 99% confidence interval, but use Python functions to calculate the
> confidence interval.
>
> Recall from Example 4.4, the sample mean is 15.8 miles with a standard deviation of 3.2 miles. The sample
> size is 26 employees, and we are interested in calculating a 99% confidence interval.
>
> Solution
>
> Use the Python function t.interval() as shown:
>
> PYTHON CODE
>
> # Enter sample mean, sample standard deviation, and sample size
> sample_mean = 15.8
> sample_standard_deviation = 3.2
> sample_size = 26
>
> # Degrees of freedom (sample size - 1)
> degrees_of_freedom = sample_size - 1
>
> # Confidence level
> confidence_level = 0.99
>
> # standard error
> standard_error = sample_standard_deviation / math.sqrt(sample_size)

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-014

**Pregunta:** What sequence should be followed to flag unusually low or high observations using the middle 50% of an ordered dataset?

**Respondibilidad de referencia:** answerable

### q-v1-014-pool-001

**Chunk:** `openstax_principles_ds:3.1:chunk-010`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> For example, assume that the
> weekly closing stock price for a technology stock, in dollars, is recorded for 20 consecutive weeks as follows:
>
> 50, 53, 59, 59, 63, 63, 72, 72, 72, 72, 72, 76, 78, 81, 83, 84, 84, 84, 90, 93
>
> To find the mode, determine the most frequent score, which is 72, which occurs five times. Thus, the mode of
> this dataset is 72.
>
> The mode can also be applied to non-numeric (qualitative) data, whereas the mean and the median can only
> be applied for numeric (quantitative) data. For example, a restaurant manager might want to determine the
> mode for responses to customer surveys on the quality of the service of a restaurant, as shown in Table 3.1.
>
> Customer
>
> Service
>
> Number of
> Respondents
>
> Rating
>
> Excellent
> 267
>
> Very Good
> 410
>
> Good
> 392
>
> Fair
> 107
>
> Poor
> 18
>
> Table 3.1 Customer Survey Results for
> Customer Survey Rating
>
> Based on the survey responses, the mode is the Customer Service Rating of “Very Good,” since this is the data
> value with the greatest frequency.
>
> Influence of Outliers on Measures of Center
>
> As mentioned earlier, when outliers are present in a dataset, the mean may not represent the center of the
> dataset, and the median will provide a better measure of center. The reason is that the median focuses on the
> middle value of the ordered dataset. Thus, any outliers at the lower end of the dataset or any outliers at the
> upper end of the dataset will not affect the median. Note: A formal method for identifying outliers is presented
> in Measures of Position when measures of position are discussed. The following example illustrates the point
> that the median is a better measure of central tendency when potential outliers are present.
>
> EXAMPLE 3.5
>
> Problem

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-014-pool-003

**Chunk:** `openstax_principles_ds:3.1:chunk-008`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> Since the median
> focuses on the middle value of the ordered dataset, the median is preferred when outliers are present because
> the median is not affected by the numerical values of the outliers.
>
> To determine the median of a dataset, first order the data from smallest to largest, and then find the middle
> value in the ordered dataset. For example, to find the median value of 50 exam scores, find the score that
> splits the data into two equal parts. The exam scores for 25 students will be below the median, and 25
> students will have exam scores above the median.
>
> If there is an odd number of data values in the dataset, then there will be one data value that represents the
> middle value, and this is the median. If there is an even number of data values in the dataset, then to find the
> median, add the two middle values together and divide by 2 (this is essentially finding the mean of the two
> middle values in the dataset).
>
> EXAMPLE 3.4
>
> Problem
>
> The same dataset of pulse rates from Example 3.1 is:
>
> 68, 92, 76, 51, 65, 83, 94, 72, 88, 59
>
> Calculate the median pulse rate for this sample.
>
> Solution
>
> First, order the 10 data values from smallest to largest. Divide this sum by the number of data values, which
> is 10. The result is:
>
> 51, 59, 65, 68, 72, 76, 83, 88, 92, 94
>
> Since there is an even number of data values, add the two middle values together and divide by 2. The two middle values are 72 and 76.
>
> You can also quickly find the sample median of a dataset as follows.
>
> Let  represent the number of data values in the sample.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-014-pool-005

**Chunk:** `openstax_principles_ds:3.1:chunk-009`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> 51, 59, 65, 68, 72, 76, 83, 88, 92, 94
>
> Since there is an even number of data values, add the two middle values together and divide by 2. The two middle values are 72 and 76.
>
> You can also quickly find the sample median of a dataset as follows.
>
> Let  represent the number of data values in the sample.
>
> • If  is odd, then the median is the data value in position
> .
>
> • If  is even, the median is the mean of the observations in position
>  and position
> .
>
> For example, let’s say a dataset has 25 data values. Since  is odd, to identify the position of the median,
>
> calculate
> , which is
> , or 13. This indicates that the median is located in the 13th data position.
>
> As another example, let’s say a dataset has 100 data values. Since  is even, to identify the position of the
>
> median, calculate
> , which is
> , which is 50, and also calculate
> , which is
> , which is 51. This
>
> indicates that the median is calculated as the mean of the 50th and 51st data values.
>
> Mode
>
> Another measure of center is the mode. The mode is the data value that occurs with the greatest frequency. If
> there are no repeating data values in a dataset, then there is no mode. If two data values occur with same
> greatest frequency, then there are two modes, and we say the data is bimodal. For example, assume that the
> weekly closing stock price for a technology stock, in dollars, is recorded for 20 consecutive weeks as follows:
>
> 50, 53, 59, 59, 63, 63, 72, 72, 72, 72, 72, 76, 78, 81, 83, 84, 84, 84, 90, 93

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-014-pool-006

**Chunk:** `openstax_principles_ds:3.3:chunk-003`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.3: Measures of Position
>
> Determine the percentile for the employee who scored 88 on the aptitude test.
>
> Solution
>
> There are 15 data values in total, and there are 10 data values below 88.
>
> Quartiles
>
> While percentiles separate data into 100 equal parts, quartiles separate data into quarters, or four equal
> parts. To find the quartiles, first find the median, or second quartile. The first quartile,
> , is the middle value,
> or median, of the lower half of the data, and the third quartile,
> , is the middle value of the upper half of the
> data.
>
> Note the following correspondence between quartiles and percentiles:
>
> • The first quartile corresponds to the 25th percentile.
> • The second quartile (which is the median) corresponds to the 50th percentile.
> • The third quartile corresponds to the 75th percentile.
>
> EXAMPLE 3.11
>
> Problem
>
> Consider the following ordered dataset, which represents the time in seconds for an athlete to complete a
> 40-yard run:
>
> 5.4, 6.0, 6.3, 6.8, 7.1, 7.2, 7.4, 7.5, 7.9, 8.2, 8.7
>
> Solution
>
> The median, or second quartile, is the middle value in this dataset, which is 7.2. Notice that 50% of the data
> values are below the median, and 50% of the data values are above the median. The lower half of the data
> values are 5.4, 6.0, 6.3, 6.8, 7.1. Note that these are the data values below the median. The upper half of the
> data values are 7.4, 7.5, 7.9, 8.2, 8.7, which are the data values above the median.
>
> To find the first quartile,
> , locate the middle value of the lower half of the data (5.4, 6.0, 6.3, 6.8, 7.1). The
> middle value of the lower half of the dataset is 6.3.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-014-pool-007

**Chunk:** `openstax_principles_ds:3.1:chunk-011`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> Note: A formal method for identifying outliers is presented
> in Measures of Position when measures of position are discussed. The following example illustrates the point
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
>
> Using Python for Measures of Center
>
> We learned in What Are Data and Data Science? how the DataFrame.describe() method is used to

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-014-pool-008

**Chunk:** `openstax_principles_ds:4.1:chunk-020`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Bootstrapping Methods
>
> In the earlier discussion of confidence intervals, certain requirements needed to be met in order to use the
> estimation methods. For example, when calculating the confidence interval for a mean, this requirement was
> indicated:
>
> • The sample size is at least 30, or the underlying population is known to follow a normal distribution.
>
> When calculating the confidence interval for a proportion, this requirement was noted:
>
> • Verify that the normal approximation to the binomial distribution is appropriate by ensuring that both
> and
>  are at least 5.
>
> What should a researcher do when these requirements are not met? Fortunately, there is another option called
> “bootstrapping” that can be used to find confidence intervals when the underlying distribution is unknown or if
> one of the conditions is not met. This bootstrapping method involves repeatedly taking samples with
> replacement.
>
> Sampling with replacement means that when a sample is selected, the sample is replaced back in the dataset
> before selecting the next sample. For example, a casino dealer plans to take a sample of two cards from a
> standard 52-card deck. If the sampling is to be done with replacement, then after selecting the sample of the
> first card, this card is then returned to the deck before the second card is selected. This implies that the same
> data value can appear multiple times in a given sample since once a data value is selected for the sample, it is
>
> replaced back in the dataset and is eligible to be selected again for the sample.
>
> For example, a researcher who has collected 100 samples to use for inference may want to estimate a
> confidence interval for the population mean. The researcher can then resample, with replacement, from this
> limited set of 100 observations.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-014-pool-009

**Chunk:** `openstax_principles_ds:4.1:chunk-024`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> To find the 5th percentile (P5), multiply the percentile (5%) times the number of data values, which is 20. The
> result is 1, so to find the 5th percentile, add the first and second data values together and divide by 2. For
> this example, add 21.9 to 22.2 and divide by 2. The result is 22.05.
>
> To find the 95th percentile (P95), multiply the percentile (95%) times the number of data values, which is 20. The result is 19, so to find the 95th percentile, add the 19th and 20th data values together and divide by 2. For this example, add 28.5 to 28.6 and divide by 2. The result is 28.6.
>
> Based on the bootstrapping method, the 90% confidence interval is (22.05, 28.6).
>
> Python provides a function called bootstrap() as part of the scipy.stats library to automate this
>
> bootstrapping process.
>
> Within the bootstrap()function, the user can specify the number of resamples to be performed as part of
>
> the bootstrapping process. In this example, we will use 50,000 samples by way of the _resample
> parameter.
>
> PYTHON CODE
>
> from scipy.stats import bootstrap
> import numpy as np
>
> #define random sample of ages
> ages = [22, 23, 25, 31, 24, 21, 28, 23, 21, 20, 22, 19, 34, 19, 37, 26, 29, 21,
> 24, 20]
>
> #convert ages to sequence
> ages = (ages,)
>
> #use bootstrap function for confidence interval for the mean
> conf_interval = bootstrap(ages, np.mean, confidence_level=0.95,
>                          random_state=1, n_resamples = 50000,
> method='percentile')
>
> #print the confidence interval
> print(conf_interval.confidence_interval)
>
> The resulting output will look like this:
>
> ConfidenceInterval(low=22.45, high=26.7)
>
> Using 50,000 bootstrapped samples, a 95% confidence interval is generated as (22.45, 26.7).
>
> EXPLORING FURTHER
>
> Simulating Confidence Intervals
>
> A number of websites and resources, such as the online textbook Online Statistics Education: A Multimedia
> Course of Study (https://openstax.org/r/estimation) (http://onlinestatbook.com/) (project leader: David M.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-014-pool-010

**Chunk:** `openstax_principles_ds:3.1:chunk-003`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> The most widely used measures of the center of a dataset are the mean (average), the
> median, and the mode.
>
> Mean and Trimmed Mean
>
> The mean, or average, (sometimes referred to as the arithmetic mean) is the most commonly used measure of
> the center of a dataset. Sometimes the mean can be skewed by the presence of outliers, or data values that
> are significantly different as compared to the remainder of the dataset. In these instances, the trimmed mean
> is often used to provide a more representative measure of the center of the dataset, as we will discuss in the
> following section.
>
> Mean
>
> To calculate the mean, add the values of all the items in a dataset and divide by the number of items. For
> example, if the scores on your last three exams were 87, 92, and 73, then the mean score would be
>
> . If you had a large number of data values, you would proceed in the same way. For example, to
>
> calculate the mean value of 50 exam scores, add the 50 scores together and divide by 50. If the 50 scores add
>
> up to 4,050, for example, the mean score is
> , or 81.
>
> In data science applications, you will encounter two types of datasets: sample data and population data. Population data represents all the outcomes or measurements that are of interest. Sample data represents
> outcomes or measurements collected from a subset, or part, of the population of interest. Of course in many
> applications, collecting data from an entire population is not practical or feasible, and so we often rely on
> sample data.
>
> The notation  is used to indicate the sample mean, where the mean is calculated based on data taken from a
> sample.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-014-pool-011

**Chunk:** `openstax_principles_ds:3.1:chunk-007`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> For the mean, add the 15 data values, and the sum is 10,777,090. Divide this sum by the number of
> data values, which is 15. The result is:
>
> 2. For the trimmed mean, first order the data from smallest to largest. The sorted dataset is:
>
> 385000, 397900, 403890, 452600, 488300, 499000, 507400, 525000, 573200, 599000, 612300, 623400,
> 675000, 1689300, 2345800
>
> Twenty percent of 15 data values is 3, and this indicates that 3 data values are to be deleted from each
> of the lower end and upper end of the dataset. The resulting 9 undeleted data values are:
>
> 452600, 488300, 499000, 507400, 525000, 573200, 599000, 612300, 623400
>
> Then find the mean for the remaining data values. The sum of these 9 data values is 4,880,200. Divide
> this sum by the number of data values (9). The result is:
>
> Notice how the mean calculated in Part (a) is significantly larger as compared to the trimmed mean
> calculated in Part (b). The reason is the presence of several large outlier home prices. Once these outlier
> data values are removed by the trimmed mean calculation, the resulting trimmed mean is more
> representative of the typical home price in this neighborhood as compared to the mean.
>
> Median
>
> The median provides another measure of central tendency for a dataset. The median is generally a better
> measure of the central tendency when there are outliers (extreme values) in the dataset. Since the median
> focuses on the middle value of the ordered dataset, the median is preferred when outliers are present because
> the median is not affected by the numerical values of the outliers.
>
> To determine the median of a dataset, first order the data from smallest to largest, and then find the middle
> value in the ordered dataset.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-014-pool-012

**Chunk:** `openstax_intro_stats_2e:7.intro:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 7: The Central Limit Theorem
> Section 7.intro: Introduction
>
> The second alternative says that if we again
> collect samples of size n that are "large enough," calculate the sum of each sample and create a histogram, then the
> resulting histogram will again tend to have a normal bell-shape.
>
> The size of the sample, n, that is required in order to be "large enough" depends on the original population from which
> the samples are drawn (the sample size should be at least 30 or the data should come from a normal distribution). If the
> original population is far from normal, then more observations are needed for the sample means or sums to be normal. Sampling is done with replacement.
>
> It would be difficult to overstate the importance of the central limit theorem in statistical theory. Knowing that data, even
> if its distribution is not normal, behaves in a predictable way is a powerful tool.
>
> COLLABORATIVE EXERCISE
>
> Suppose eight of you roll one fair die ten times, seven of you roll two fair dice ten times, nine of you roll five fair dice
> ten times, and 11 of you roll ten fair dice ten times.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-014-pool-013

**Chunk:** `openstax_intro_stats_2e:9.5:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.5: Additional Information and Full Hypothesis Test Examples
>
> Conclusion: After you make your decision, write a thoughtful conclusion about the hypotheses in terms of the given
> problem.
>
> EXAMPLE 9.10
>
> When using the p-value to evaluate a hypothesis test, it is sometimes useful to use the following memory device
>
> If the p-value is low, the null must go.
>
> If the p-value is high, the null must fly.
>
> This memory aid relates a p-value less than the established alpha (the p is low) as rejecting the null hypothesis and,
> likewise, relates a p-value higher than the established alpha (the p is high) as not rejecting the null hypothesis.
>
> Problem
> Fill in the blanks.
>
> Reject the null hypothesis when ______________________________________.
>
> The results of the sample data _____________________________________.
>
> Do not reject the null when hypothesis when __________________________________________.
>
> The results of the sample data ____________________________________________.
>
> Solution
> Reject the null hypothesis when the p-value is less than the established alpha value. The results of the sample data
> support the alternative hypothesis.
>
> Do not reject the null hypothesis when the p-value is greater than the established alpha value. The results of the
> sample data do not support the alternative hypothesis.
>
> TRY IT 9.10
>
> It’s a Boy Genetics Labs claim their procedures improve the chances of a boy being born. The results for a test of a
> single population proportion are as follows:
>
> H0: p = 0.50, Ha: p > 0.50
>
> α = 0.01
>
> p-value = 0.025
>
> Interpret the results and state a conclusion in simple, non-technical terms.
>
> 9.5 Additional Information and Full Hypothesis Test Examples

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-014-pool-014

**Chunk:** `openstax_principles_ds:3.1:chunk-005`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> EXAMPLE 3.1
>
> Problem
>
> During a clinical trial, a sample is taken of 10 patients and pulse rates are measured in beats per minute:
>
> 68, 92, 76, 51, 65, 83, 94, 72, 88, 59
>
> Calculate the mean pulse rate for this sample.
>
> Solution
>
> Add the 10 data values, and the sum is 748. Divide this sum by the number of data values, which is 10. The
> result is:
>
> EXAMPLE 3.2
>
> Problem
>
> A college professor records the ages of 25 students in a data science class as shown:
>
> Student Age
> Number of
>
> Students
> (Frequency)
>
> 19
> 3
>
> 20
> 4
>
> 21
> 8
>
> 22
> 6
>
> 23
> 2
>
> 27
> 1
>
> 31
> 1
>
> Total
> 25
>
> Calculate the mean age for this sample of students.
>
> Solution
>
> Substitute the values from the table in the following formula:
>
> Trimmed Mean
>
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

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-015

**Pregunta:** How do the ordinary mean, a trimmed mean, and the median respond differently to extreme observations?

**Respondibilidad de referencia:** answerable

### q-v1-015-pool-001

**Chunk:** `openstax_intro_stats_2e:9.4:chunk-004`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.4: Rare Events, the Sample, Decision and Conclusion
>
> To persuade his customers that he is right, the baker decides to do a hypothesis test. He bakes 10 loaves of bread. The mean height of the sample loaves is 17 cm. The baker knows from baking hundreds of loaves of bread that the
> standard deviation for the height is 0.5 cm. and the distribution of heights is normal.
>
> The null hypothesis could be H0: μ ≤ 15 The alternate hypothesis is Ha: μ > 15
>
> The words "is more than" translates as a ">" so "μ > 15" goes into the alternate hypothesis. The null hypothesis must
> contradict the alternate hypothesis.
>
> By the Central Limit Theorem, the distribution of sample means, for samples of 10 loaves, will be normal with mean μ =
> 15 and standard deviation
> .
>
> Suppose the null hypothesis is true (the mean height of the loaves is no more than 15 cm). Then is the mean height (17
> cm) calculated from the sample unexpectedly large? The hypothesis test works by asking the question how unlikely the
> sample mean would be if the null hypothesis were true. The graph shows how far out the sample mean is on the normal
> curve. The p-value is the probability that, if we were to take other samples, any other sample mean would fall at least as
> far out as 17 cm.
>
> The p-value, then, is the probability that a sample mean is the same or greater than 17 cm. when the population
> mean is, in fact, 15 cm. We can calculate this probability using the normal distribution for means.
>
> Figure 9.2
>
> p-value= P( > 17) which is approximately zero.
>
> A p-value of approximately zero tells us that it is highly unlikely that a loaf of bread rises no more than 15 cm, on
> average.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-015-pool-002

**Chunk:** `openstax_principles_ds:3.1:chunk-007`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> For the mean, add the 15 data values, and the sum is 10,777,090. Divide this sum by the number of
> data values, which is 15. The result is:
>
> 2. For the trimmed mean, first order the data from smallest to largest. The sorted dataset is:
>
> 385000, 397900, 403890, 452600, 488300, 499000, 507400, 525000, 573200, 599000, 612300, 623400,
> 675000, 1689300, 2345800
>
> Twenty percent of 15 data values is 3, and this indicates that 3 data values are to be deleted from each
> of the lower end and upper end of the dataset. The resulting 9 undeleted data values are:
>
> 452600, 488300, 499000, 507400, 525000, 573200, 599000, 612300, 623400
>
> Then find the mean for the remaining data values. The sum of these 9 data values is 4,880,200. Divide
> this sum by the number of data values (9). The result is:
>
> Notice how the mean calculated in Part (a) is significantly larger as compared to the trimmed mean
> calculated in Part (b). The reason is the presence of several large outlier home prices. Once these outlier
> data values are removed by the trimmed mean calculation, the resulting trimmed mean is more
> representative of the typical home price in this neighborhood as compared to the mean.
>
> Median
>
> The median provides another measure of central tendency for a dataset. The median is generally a better
> measure of the central tendency when there are outliers (extreme values) in the dataset. Since the median
> focuses on the middle value of the ordered dataset, the median is preferred when outliers are present because
> the median is not affected by the numerical values of the outliers.
>
> To determine the median of a dataset, first order the data from smallest to largest, and then find the middle
> value in the ordered dataset.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-015-pool-003

**Chunk:** `openstax_principles_ds:3.1:chunk-002`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> Probability theory helps
> us deal with quantifying uncertainty, which is always inherent in real-world data. We will see that in real-world
> datasets we often have to deal with noise and randomness that will be analyzed using statistical analyses.
>
> Probability analysis provides the tools to model, understand, and quantify uncertainties, allowing data
> scientists to make informed decisions from data. Probability theory also forms the basis for different types of
> analyses, such as confidence intervals and hypothesis testing, which will be discussed further in Inferential
> Statistics and Regression Analysis. Such methods rely on probability models to make predictions and detect
> patterns. In addition, machine learning (discussed in Time Series and Forecasting) uses probabilistic models to
> help represent uncertainty and make predictions based on the collected data. Probability analysis helps data
> scientists to select data models, interpret the results, and assess the reliability of these conclusions. For a more
> detailed review of statistical concepts, please refer to Introductory Statistics 2e (https://openstax.org/books/
> introductory-statistics-2e/pages/1-introduction).
>
> 3.1 Measures of Center
>
> Learning Outcomes
> By the end of this section, you should be able to:
>
> • 3.1.1 Define and calculate mean, trimmed mean, median, and mode for a dataset.
> • 3.1.2 Determine the effect of outliers on the mean and the median.
> • 3.1.3 Use Python to calculate measures of center for a dataset.
>
> Measures of center are statistical measurements that provide a central, or typical, representation of a dataset. These measures can help indicate where the bulk of the data is concentrated and are often called the data’s
> central tendency. The most widely used measures of the center of a dataset are the mean (average), the
> median, and the mode.
>
> Mean and Trimmed Mean
>
> The mean, or average, (sometimes referred to as the arithmetic mean) is the most commonly used measure of
> the center of a dataset.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-015-pool-004

**Chunk:** `openstax_principles_ds:3.1:chunk-006`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> To calculate the trimmed mean for a dataset, first sort the data in ascending order (from smallest to largest). Then decide on a certain percentage of data values to be deleted from the lower and upper ends of the
> dataset. This might represent the extent of outliers in the dataset; trimmed mean percentages of 10% and 20%
> are common. Then delete the specified percentage of data values from both the lower end and upper end of
> the dataset. Then find the mean for the remaining undeleted data values.
>
> As an example, to calculate a 10% trimmed mean, first sort the data values from smallest to largest. Then
> delete the lower 10% of the data values and delete the upper 10% of the data values. Then calculate the mean
> for the resulting dataset. Any outliers would tend to be deleted as part of the trimmed mean calculation, and
> thus the trimmed mean would then be a more representative measure of the center of the data for datasets
> containing outliers.
>
> EXAMPLE 3.3
>
> Problem
>
> A real estate agent collects data on a sample of recently sold homes in a certain neighborhood, and the
> data are shown in the following dataset:
>
> 397900, 452600, 507400, 488300, 623400, 573200, 1689300, 403890, 612300, 599000, 2345800, 499000,
> 525000, 675000, 385000
>
> 1. Calculate the mean of the dataset. 2. Calculate a 20% trimmed mean rate for the dataset.
>
> Solution
>
> 1. For the mean, add the 15 data values, and the sum is 10,777,090. Divide this sum by the number of
> data values, which is 15. The result is:
>
> 2. For the trimmed mean, first order the data from smallest to largest. The sorted dataset is:
>
> 385000, 397900, 403890, 452600, 488300, 499000, 507400, 525000, 573200, 599000, 612300, 623400,
> 675000, 1689300, 2345800

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-015-pool-005

**Chunk:** `openstax_principles_ds:4.2:chunk-008`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> In hypothesis testing, the maximum allowed probability of making a Type I error is called the level of
> significance, denoted by the Greek letter alpha, . From a practical standpoint, the level of significance is the
> probability value used to determine when the sample data indicates significant evidence against the null
> hypothesis. This level of significance is typically set to a small value, which indicates that the researcher wants
> the probability of rejecting a true null hypothesis to be small. Typical values of the level of significance used in
> hypothesis testing are as follows:
> ,
> , or
> .
>
> Once the null and alternative hypotheses are written and a level of significance is selected, the next step is for
> the researcher to collect relevant sample data from the population under study. It’s important that a
> representative random sample is selected, as discussed in Handling Large Datasets. After the sample data is
> collected, two calculations are performed: test statistic and p-value.
>
> The test statistic is a numerical value used to assess the strength of evidence against a null hypothesis and is
> calculated from sample data that is used in hypothesis testing. As noted in Estimating Parameters with
> Confidence Intervals, a sample statistic is a numerical value calculated from a sample of observations drawn
> from a larger population such as a sample mean or sample proportion. The sample statistic is converted to a
> standardized test statistic such as a z-score or t-score based on the assumption that the null hypothesis is
>
> true.
>
> Once the test statistic has been determined, a probability, or p-value, is created. A p-value is the probability of
> obtaining a sample statistic with a value as extreme as (or more extreme than) the value determined by the
> sample data under the assumption that the null hypothesis is true.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-015-pool-006

**Chunk:** `openstax_principles_ds:3.1:chunk-003`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> The most widely used measures of the center of a dataset are the mean (average), the
> median, and the mode.
>
> Mean and Trimmed Mean
>
> The mean, or average, (sometimes referred to as the arithmetic mean) is the most commonly used measure of
> the center of a dataset. Sometimes the mean can be skewed by the presence of outliers, or data values that
> are significantly different as compared to the remainder of the dataset. In these instances, the trimmed mean
> is often used to provide a more representative measure of the center of the dataset, as we will discuss in the
> following section.
>
> Mean
>
> To calculate the mean, add the values of all the items in a dataset and divide by the number of items. For
> example, if the scores on your last three exams were 87, 92, and 73, then the mean score would be
>
> . If you had a large number of data values, you would proceed in the same way. For example, to
>
> calculate the mean value of 50 exam scores, add the 50 scores together and divide by 50. If the 50 scores add
>
> up to 4,050, for example, the mean score is
> , or 81.
>
> In data science applications, you will encounter two types of datasets: sample data and population data. Population data represents all the outcomes or measurements that are of interest. Sample data represents
> outcomes or measurements collected from a subset, or part, of the population of interest. Of course in many
> applications, collecting data from an entire population is not practical or feasible, and so we often rely on
> sample data.
>
> The notation  is used to indicate the sample mean, where the mean is calculated based on data taken from a
> sample.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-015-pool-007

**Chunk:** `openstax_intro_stats_2e:9.4:chunk-005`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.4: Rare Events, the Sample, Decision and Conclusion
>
> We can calculate this probability using the normal distribution for means.
>
> Figure 9.2
>
> p-value= P( > 17) which is approximately zero.
>
> A p-value of approximately zero tells us that it is highly unlikely that a loaf of bread rises no more than 15 cm, on
> average. That is, almost 0% of all loaves of bread would be at least as high as 17 cm. purely by CHANCE had the
> population mean height really been 15 cm. Because the outcome of 17 cm. is so unlikely (meaning it is happening
> NOT by chance alone), we conclude that the evidence is strongly against the null hypothesis (the mean height is at most
> 15 cm.). There is sufficient evidence that the true mean height for the population of the baker's loaves of bread is greater
> than 15 cm.
>
> TRY IT 9.9
>
> A normal distribution has a standard deviation of 1. We want to verify a claim that the mean is greater than 12. A
> sample of 36 is taken with a sample mean of 12.5.
>
> H0: μ ≤ 12
> Ha: μ > 12
> The p-value is 0.0013
> Draw a graph that shows the p-value.
>
> Decision and Conclusion
>
> A systematic way to make a decision of whether to reject or not reject the null hypothesis is to compare the p-value and
> a preset or preconceived α (also called a "significance level"). A preset α is the probability of a Type I error (rejecting
> the null hypothesis when the null hypothesis is true). It may or may not be given to you at the beginning of the problem.
>
> When you make a decision to reject or not reject H0, do as follows:
>
> • If α > p-value, reject H0. The results of the sample data are significant.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-015-pool-008

**Chunk:** `openstax_principles_ds:3.1:chunk-009`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> 51, 59, 65, 68, 72, 76, 83, 88, 92, 94
>
> Since there is an even number of data values, add the two middle values together and divide by 2. The two middle values are 72 and 76.
>
> You can also quickly find the sample median of a dataset as follows.
>
> Let  represent the number of data values in the sample.
>
> • If  is odd, then the median is the data value in position
> .
>
> • If  is even, the median is the mean of the observations in position
>  and position
> .
>
> For example, let’s say a dataset has 25 data values. Since  is odd, to identify the position of the median,
>
> calculate
> , which is
> , or 13. This indicates that the median is located in the 13th data position.
>
> As another example, let’s say a dataset has 100 data values. Since  is even, to identify the position of the
>
> median, calculate
> , which is
> , which is 50, and also calculate
> , which is
> , which is 51. This
>
> indicates that the median is calculated as the mean of the 50th and 51st data values.
>
> Mode
>
> Another measure of center is the mode. The mode is the data value that occurs with the greatest frequency. If
> there are no repeating data values in a dataset, then there is no mode. If two data values occur with same
> greatest frequency, then there are two modes, and we say the data is bimodal. For example, assume that the
> weekly closing stock price for a technology stock, in dollars, is recorded for 20 consecutive weeks as follows:
>
> 50, 53, 59, 59, 63, 63, 72, 72, 72, 72, 72, 76, 78, 81, 83, 84, 84, 84, 90, 93

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-015-pool-009

**Chunk:** `openstax_principles_ds:3.1:chunk-010`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> For example, assume that the
> weekly closing stock price for a technology stock, in dollars, is recorded for 20 consecutive weeks as follows:
>
> 50, 53, 59, 59, 63, 63, 72, 72, 72, 72, 72, 76, 78, 81, 83, 84, 84, 84, 90, 93
>
> To find the mode, determine the most frequent score, which is 72, which occurs five times. Thus, the mode of
> this dataset is 72.
>
> The mode can also be applied to non-numeric (qualitative) data, whereas the mean and the median can only
> be applied for numeric (quantitative) data. For example, a restaurant manager might want to determine the
> mode for responses to customer surveys on the quality of the service of a restaurant, as shown in Table 3.1.
>
> Customer
>
> Service
>
> Number of
> Respondents
>
> Rating
>
> Excellent
> 267
>
> Very Good
> 410
>
> Good
> 392
>
> Fair
> 107
>
> Poor
> 18
>
> Table 3.1 Customer Survey Results for
> Customer Survey Rating
>
> Based on the survey responses, the mode is the Customer Service Rating of “Very Good,” since this is the data
> value with the greatest frequency.
>
> Influence of Outliers on Measures of Center
>
> As mentioned earlier, when outliers are present in a dataset, the mean may not represent the center of the
> dataset, and the median will provide a better measure of center. The reason is that the median focuses on the
> middle value of the ordered dataset. Thus, any outliers at the lower end of the dataset or any outliers at the
> upper end of the dataset will not affect the median. Note: A formal method for identifying outliers is presented
> in Measures of Position when measures of position are discussed. The following example illustrates the point
> that the median is a better measure of central tendency when potential outliers are present.
>
> EXAMPLE 3.5
>
> Problem

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-015-pool-010

**Chunk:** `openstax_intro_stats_2e:9.4:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.4: Rare Events, the Sample, Decision and Conclusion
>
> Didi is the first person to reach into the basket and pull
> out a bubble. Her bubble contains a $100 bill. The probability of this happening is
>  = 0.005. Because this is so unlikely,
>
> Ali is hoping that what the two of them were told is wrong and there are more $100 bills in the basket. A "rare event" has
> occurred (Didi getting the $100 bill) so Ali doubts the assumption about only one $100 bill being in the basket.
>
> Using the Sample to Test the Null Hypothesis
>
> Use the sample data to calculate the actual probability of getting the test result, called the p-value. The p-value is the
> probability that, if the null hypothesis is true, the results from another randomly selected sample will be as
> extreme or more extreme as the results obtained from the given sample.
>
> A large p-value calculated from the data indicates that we should not reject the null hypothesis. The smaller the p-value,
> the more unlikely the outcome, and the stronger the evidence is against the null hypothesis. We would reject the null
> hypothesis if the evidence is strongly against it.
>
> Draw a graph that shows the p-value. The hypothesis test is easier to perform if you use a graph because you see
> the problem more clearly.
>
> EXAMPLE 9.9
>
> Suppose a baker claims that his bread height is more than 15 cm, on average. Several of his customers do not believe
> him. To persuade his customers that he is right, the baker decides to do a hypothesis test. He bakes 10 loaves of bread. The mean height of the sample loaves is 17 cm. The baker knows from baking hundreds of loaves of bread that the
> standard deviation for the height is 0.5 cm. and the distribution of heights is normal.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-015-pool-013

**Chunk:** `openstax_intro_stats_2e:6.4:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 6: The Normal Distribution
> Section 6.4: Normal Distribution (Pinkie Length)
>
> does it have a hump in the middle or at either end, and so on?)
>
> Analyze the Distribution
> Using your sample mean, sample standard deviation, and histogram to help, what is the approximate theoretical
> distribution of the data?
>
> • X ~ _____(_____,_____)
> • How does the histogram help you arrive at the approximate distribution?
>
> Describe the Data
> Use the data you collected to complete the following statements.
>
> • The IQR goes from __________ to __________.
> • IQR = __________. (IQR = Q3 – Q1)
> • The 15th percentile is _______.
> • The 85th percentile is _______.
> • The median is _______.
> • The empirical probability that a randomly chosen lap time is more than 130 seconds is _______.
> • Explain the meaning of the 85th percentile of this data.
>
> Theoretical Distribution
> Using the theoretical distribution, complete the following statements. You should use a normal approximation based on
> your sample data.
>
> • The IQR goes from __________ to __________.
> • IQR = _______.
> • The 15th percentile is _______.
> • The 85th percentile is _______.
> • The median is _______.
> • The probability that a randomly chosen lap time is more than 130 seconds is _______.
> • Explain the meaning of the 85th percentile of this distribution.
>
> Discussion Questions
> Do the data from the section titled Collect the Data give a close approximation to the theoretical distribution in the
> section titled Analyze the Distribution? In complete sentences and comparing the result in the sections titled Describe
> the Data and Theoretical Distribution, explain why or why not.
>
> 6.4 Normal Distribution (Pinkie Length)
>
> Stats Lab
>
> Normal Distribution (Pinkie Length)
> Class Time:
>
> Names:
>
> Student Learning Outcomes
>
> • The student will compare empirical data and a theoretical distribution to determine if data from the experiment
> follow a continuous distribution.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-016

**Pregunta:** How do count-based outcomes differ from measurement-based outcomes in the kinds of numerical values they can take?

**Respondibilidad de referencia:** answerable

### q-v1-016-pool-002

**Chunk:** `openstax_principles_ds:3.5:chunk-009`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.5: Discrete and Continuous Probability Distributions
>
> The PMF is given by the
> formula:
>
> Where:
>
> is the probability that the random variable
>  takes on the value of exactly  successes
>  is the number of trials in the experiment
>  is the probability of success
>
> is the number of successes in the experiment
>
> refers to the number of ways to choose  successes from
>
> Note: The notation
>  is read as  factorial and is a mathematical notation used to express the multiplication of
>
> . For example,
> .
>
> EXAMPLE 3.25
>
> Problem
>
> For the binomial experiment discussed in Example 3.24, calculate the probability that 18 out of the 20
> patients will respond to indicate that the surgery was successful. Also, show a graph of the binomial
> distribution to show the probability distribution for all values of the random variable .
>
> Solution
>
> In Example 3.24, the parameters of the binomial experiment are:
>
> Substituting these values into the binomial probability formula, the probability for 18 successes can be
> calculated as follows:
>
> Based on this result, the probability that 18 out of the 20 patients will respond to indicate that the surgery
> was successful is 0.271, or approximately 27%.
>
> Figure 3.5 illustrates this binomial distribution, where the horizontal axis shows the values of the random
> variable , and the vertical axis shows the binomial probability for each value of . Note that values of  less
> than 14 are not shown on the graph since these corresponding probabilities are very close to zero.
>
> Figure 3.5 Graph of the Binomial Distribution for
>  and
>
> Since these computations tend to be complicated and time-consuming, most data scientists will use
> technology (such as Python, R, Excel, or others) to calculate binomial probabilities.
>
> Poisson Distribution
>
> The goal of a binomial experiment is to calculate the probability of a certain number of successes in a specific
> number of trials.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-016-pool-004

**Chunk:** `openstax_principles_ds:3.5:chunk-006`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.5: Discrete and Continuous Probability Distributions
>
> Note that the word “success” here does not necessarily imply a good outcome. For example, if
> a survey was conducted of adults and each adult was asked if they smoke, we can consider the answer “yes” to
> be a success and the answer “no” to be a failure. This means that the researcher can define success and failure
> in any way; however, the binomial distribution is applicable when there are only two outcomes in each trial of
> an experiment.
>
> The requirements to identify a binomial experiment and apply the binomial distribution include:
>
> • The experiment of interest is repeated for a fixed number of trials, and each trial is independent of other
> trials. For example, a market researcher might select a sample of 20 people to be surveyed where each
> respondent will reply with a “yes” or “no” answer. This experiment consists of 20 trials, and each person’s
> response to the survey question can be considered as independent of another person’s response.
> • There are only two possible outcomes for each trial, which can be labeled as “success” or “failure.”
> • The probability of success remains the same for each trial of the experiment. For example, from past data
> we know that 35% of people prefer vanilla as their favorite ice cream flavor. If a group of 15 individuals are
> surveyed to ask if vanilla is their favorite ice cream flavor, the probability of success for each trial will be
> 0.35.
> • The random variable  will count the number of successes in the experiment. Notice that since  will count
>
> the number of successes, this implies that  will be a discrete random variable.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-016-pool-005

**Chunk:** `openstax_principles_ds:3.5:chunk-005`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.5: Discrete and Continuous Probability Distributions
>
> 5. The number of inches of rain in Detroit, Michigan, in a certain month can take on any value, such as
> 2.0563, so this represents a continuous random variable.
>
> Discrete Probability Distributions: Binomial and Poisson
>
> Discrete random variables are of interest in many data science applications, and there are several probability
> distributions that apply to discrete random variables. In this chapter, we present the binomial distribution and
> the Poisson distribution, which are two commonly used probability distributions used to model discrete
> random variables for different types of events.
>
> Binomial Distribution
>
> The binomial distribution is used in applications where there are two possible outcomes for each trial in an
> experiment and the two possible outcomes can be considered as success or failure. For example, when a
> baseball player is at-bat, the player either gets a hit or does not get a hit. There are many applications of
> binomial experiments that occur in medicine, psychology, engineering, science, marketing, and other fields.
>
> There are many statistical experiments where the results of each trial can be considered as either a success or
> a failure. For example, when flipping a coin, the two outcomes are heads or tails. When rolling a die, the two
> outcomes can be considered to be an even number appears on the face of the die or an odd number appears
> on the face of the die. When conducting a marketing study, a customer can be asked if they like or dislike a
> certain product. Note that the word “success” here does not necessarily imply a good outcome. For example, if
> a survey was conducted of adults and each adult was asked if they smoke, we can consider the answer “yes” to
> be a success and the answer “no” to be a failure.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-016-pool-006

**Chunk:** `openstax_principles_ds:3.5:chunk-008`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.5: Discrete and Continuous Probability Distributions
>
> From past data, the
> researcher knows that the probability of success for this type of surgery is 92%.
>
> 1. Does this experiment meet the requirements for a binomial experiment? 2. If so, identify the values of , , and  in the experiment.
>
> Solution
>
> 1. This experiment does meet the requirements for a binomial experiment since the experiment will be
> repeated for 20 trials, and each response from a patient will be independent of other responses. Each
> reply from a patient will be one of two responses—the surgery was successful or the surgery was not
> successful. The probability of success remains the same for each trial at 92%. The random variable
> can be used to count the number of patients who respond that the surgery was successful. 2. The number of trials is 20 since 20 patients are being surveyed, so
> . The probability of success for each surgery is 92%, so
> . The number of successes of interest is 18 since the researcher wants to determine the probability that
> 18 of the 20 patients had a successful result from the surgery, so
> .
>
> When calculating the probability for  successes in a binomial experiment, a binomial probability formula can
> be used, but in many cases technology is used instead to streamline the calculations.
>
> The probability mass function (PMF) for the binomial distribution describes the probability of getting exactly
>
> successes in  independent Bernoulli trials, each with a probability  of success. The PMF is given by the
> formula:
>
> Where:
>
> is the probability that the random variable
>  takes on the value of exactly  successes
>  is the number of trials in the experiment
>  is the probability of success
>
> is the number of successes in the experiment
>
> refers to the number of ways to choose  successes from

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-016-pool-007

**Chunk:** `openstax_intro_stats_2e:8.6:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.6: Confidence Interval (Women's Heights)
>
> 5. When we construct a 90% confidence interval, we say that we are 90% confident that the true population mean
> lies within the confidence interval. Using complete sentences, explain what we mean by this phrase. 6. Some students think that a 90% confidence interval contains 90% of the data. Use the list of data given (the heights
> of women) and count how many of the data values lie within the confidence interval that you generated based on
> that data. How many of the 100 data values lie within your confidence interval? What percent is this? Is this percent
> close to 90%? 7. Explain why it does not make sense to count data values that lie in a confidence interval. Think about the random
> variable that is being used in the problem. 8. Suppose you obtained the heights of ten women and calculated a confidence interval from this information. Without knowing the population mean μ, would you have any way of knowing for certain if your interval actually
> contained the value of μ? Explain.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-016-pool-008

**Chunk:** `openstax_intro_stats_2e:7.intro:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 7: The Central Limit Theorem
> Section 7.intro: Introduction
>
> The second alternative says that if we again
> collect samples of size n that are "large enough," calculate the sum of each sample and create a histogram, then the
> resulting histogram will again tend to have a normal bell-shape.
>
> The size of the sample, n, that is required in order to be "large enough" depends on the original population from which
> the samples are drawn (the sample size should be at least 30 or the data should come from a normal distribution). If the
> original population is far from normal, then more observations are needed for the sample means or sums to be normal. Sampling is done with replacement.
>
> It would be difficult to overstate the importance of the central limit theorem in statistical theory. Knowing that data, even
> if its distribution is not normal, behaves in a predictable way is a powerful tool.
>
> COLLABORATIVE EXERCISE
>
> Suppose eight of you roll one fair die ten times, seven of you roll two fair dice ten times, nine of you roll five fair dice
> ten times, and 11 of you roll ten fair dice ten times.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-016-pool-009

**Chunk:** `openstax_principles_ds:3.3:chunk-002`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.3: Measures of Position
>
> To calculate percentiles, the data must be ordered from smallest to largest and then the ordered data divided
> into hundredths. If you score in the 80th percentile on an aptitude test, that does not necessarily mean that
> you scored 80% on the test. It means that 80% of the test scores are the same as or less than your score and
> the remaining 20% of the scores are the same as or greater than your score.
>
> Percentiles are useful for comparing many types of values. For example, a stock market mutual fund might
> report that the performance for the fund over the past year was in the 80th percentile of all mutual funds in
> the peer group. This indicates that the fund performed better than 80% of all other funds in the peer group. This also indicates that 20% of the funds performed better than this particular fund.
>
> To calculate percentiles for a specific data value in a dataset, first order the dataset from smallest to largest
> and count the number of data values in the dataset. Locate the measurement of interest and count how many
> data values fall below the measurement. Then the percentile for the measurement is calculated as follows:
>
> EXAMPLE 3.10
>
> Problem
>
> The following ordered dataset represents the scores of 15 employees on an aptitude test:
>
> 51, 63, 65, 68, 71, 75, 75, 77, 79, 82, 88, 89, 89, 92, 95
>
> Determine the percentile for the employee who scored 88 on the aptitude test.
>
> Solution
>
> There are 15 data values in total, and there are 10 data values below 88.
>
> Quartiles
>
> While percentiles separate data into 100 equal parts, quartiles separate data into quarters, or four equal
> parts. To find the quartiles, first find the median, or second quartile.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-016-pool-010

**Chunk:** `openstax_principles_ds:3.5:chunk-018`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.5: Discrete and Continuous Probability Distributions
>
> • norm()—calculate probabilities associated with the normal distribution
>
> To import these probability density functions within Python, use the import command. For example, to import
> the binom() function use the following command:
>
> from scipy.stats import binom
>
> Using Python with the Binomial Distribution
>
> The binom() function in Python allows calculations of binomial probabilities. The probability mass function for
>
> the binomial distribution within Python is referred to as binom.pmf().
>
> The syntax for using this function is binom.pmf(x, n, p)
>
> Where:
>
> is the number of trials in the experiment
>  is the probability of success
>
> is the number of successes in the experiment
>
> Consider the previous Example 3.24 worked out using the Python binom.pmf() function. A medical
>
> researcher is conducting a study related to a certain type of shoulder surgery. A sample of 20 patients who
> have recently undergone the surgery is selected, and the researcher wants to determine the probability that
> 18 of the 20 patients had a successful result from the surgery. From past data, the researcher knows that the
> probability of success for this type of surgery is 92%. Round your answer to 3 decimal places.
>
> In this example:
>
> is the number of trials in the experiment
>  is the probability of success
>
> is the number of successes in the experiment
>
> The corresponding function in Python is written as:
>
> binom.pmf (18, 20, 0.92)
>
> The round() function is then used to round the probability result to 3 decimal places.
>
> Here is the input and output of this Python program:
>
> PYTHON CODE
>
> # import the binom function from the scipy.stats library
>
> from scipy.stats import binom
>
> # define parameters x, n, and p:
> x = 18
> n = 20
> p = 0.92
>
> # use binom.pmf() function to calculate binomial probability
> # use round() function to round answer to 3 decimal places
> round (binom.pmf(x, n, p), 3)

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-016-pool-011

**Chunk:** `openstax_intro_stats_2e:9.2:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.2: Outcomes and the Type I and Type II Errors
>
> COLLABORATIVE EXERCISE
>
> Bring to class a newspaper, some news magazines, and some Internet articles . In groups, find articles from which
> your group can write null and alternative hypotheses. Discuss your hypotheses with the rest of the class.
>
> 9.2 Outcomes and the Type I and Type II Errors
>
> When you perform a hypothesis test, there are four possible outcomes depending on the actual truth (or falseness) of
> the null hypothesis H0 and the decision to reject or not. The outcomes are summarized in the following table:
>
> ACTION
> H0 IS ACTUALLY
> ...
>
> True
> False
>
> Do not reject H0
> Correct Outcome
> Type II error
>
> Reject H0
> Type I Error
> Correct Outcome
>
> Table 9.2
>
> The four possible outcomes in the table are:
>
> 1. The decision is not to reject H0 when H0 is true (correct decision). 2. The decision is to reject H0 when H0 is true (incorrect decision known as aType I error). 3. The decision is not to reject H0 when, in fact, H0 is false (incorrect decision known as a Type II error). 4. The decision is to reject H0 when H0 is false (correct decision whose probability is called the Power of the Test).
>
> Each of the errors occurs with a particular probability. The Greek letters α and β represent the probabilities.
>
> α = probability of a Type I error = P(Type I error) = probability of rejecting the null hypothesis when the null hypothesis is
> true.
>
> β = probability of a Type II error = P(Type II error) = probability of not rejecting the null hypothesis when the null
> hypothesis is false.
>
> α and β should be as small as possible because they are probabilities of errors. They are rarely zero.
>
> The Power of the Test is 1 – β.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-016-pool-012

**Chunk:** `openstax_principles_ds:3.5:chunk-007`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.5: Discrete and Continuous Probability Distributions
>
> If a group of 15 individuals are
> surveyed to ask if vanilla is their favorite ice cream flavor, the probability of success for each trial will be
> 0.35.
> • The random variable  will count the number of successes in the experiment. Notice that since  will count
>
> the number of successes, this implies that  will be a discrete random variable. For example, if the
> researcher is counting the number of people in the group of 15 that respond to say vanilla is their favorite
> ice cream flavor, then  can take on values such as 3 or 7 or 12, but  could not equal 5.28 since  is
> counting the number of people.
>
> When working with a binomial experiment, it is useful to identify two specific parameters in a binomial
> experiment:
>
> 1. The number of trials in the experiment. Label this as . 2. The probability of success for each trial (which is a constant value). Label this as .
>
> We then count the number of successes of interest as the value of the discrete random variable. Label this as .
>
> EXAMPLE 3.24
>
> Problem
>
> A medical researcher is conducting a study related to a certain type of shoulder surgery. A sample of 20
> patients who have recently undergone the surgery is selected, and the researcher wants to determine the
> probability that 18 of the 20 patients had a successful result from the surgery. From past data, the
> researcher knows that the probability of success for this type of surgery is 92%.
>
> 1. Does this experiment meet the requirements for a binomial experiment? 2. If so, identify the values of , , and  in the experiment.
>
> Solution
>
> 1.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-016-pool-013

**Chunk:** `openstax_principles_ds:3.4:chunk-001`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.4: Probability Theory
>
> EXAMPLE 3.13
>
> Problem
>
> For the home example in Example 3.12, the  value is the home price of $270,000, the mean  is $350,000,
> and the standard deviation  is $40,000. Calculate the -score.
>
> Solution
>
> The -score can be calculated as follows:
>
> This -score of −2 indicates that the selling price for this home is 2 standard deviations below the mean,
> which represents a data value that is significantly below the mean.
>
> Using Python to Calculate Measures of Position for a Dataset
>
> DataFrame.describe() computes different measures of position as well on each column of a dataset. See
>
> min, 25%, 50%, 75%, and max in Figure 3.4.
>
> Figure 3.4 The Output of DataFrame.describe() with the Movie Profit Dataset
>
> 3.4 Probability Theory
>
> Learning Outcomes
> By the end of this section, you should be able to:
>
> • 3.4.1 Describe the basic concepts of probability and apply these concepts to real-world applications
> in data science.
> • 3.4.2 Apply conditional probability and Bayes’ Theorem.
>
> Probability is a numerical measure that assesses the likelihood of occurrence of an event. Probability
> applications are ubiquitous in data science since many decisions in business, science, and engineering are
> based on probability considerations. We all use probability calculations every day as we decide, for instance,
> whether to take an umbrella to work, the optimal route for a morning commute, or the choice of a college
> major.
>
> Basic Concepts of Probability
>
> We have all used probability in one way or another on a day-to-day basis. Before leaving the house, you might
>
> want to know the probability of rain. The probability of obtaining heads on one flip of a coin is one-half, or 0.5.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-016-pool-014

**Chunk:** `openstax_principles_ds:3.4:chunk-003`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.4: Probability Theory
>
> A data scientist conducts or observes a
> procedure and determines the number of times a certain Event
>  occurs. The probability of Event
> , denoted
> as
> , is then calculated based on data that has been collected from the experiment, as follows:
>
> EXAMPLE 3.14
>
> Problem
>
> A polling organization asks a sample of 400 people if they are in favor of increased funding for local schools;
> 312 of the respondents indicate they are in favor of increased funding. Calculate the probability that a
> randomly selected person will be in favor of increased funding for local schools.
>
> Solution
>
> Using the data collected from this polling, a total of 400 people were asked the question, and 312 people
> were in favor of increased school funding. The probability for a randomly selected person being in favor of
> increased funding can then be calculated as follows (notice that Event
>  in this example corresponds to the
> event that a person is in favor of the increased funding):
>
> EXAMPLE 3.15
>
> Problem
>
> A medical patient is told they need knee surgery, and they ask the doctor for an estimate of the probability
> of success for the surgical procedure. The doctor reviews data from the past two years and determines
> there were 200 such knee surgeries performed and 188 of them were successful. Based on this past data,
> the doctor calculates the probability of success for the knee surgery (notice that Event
>  in this example
> corresponds to the event that a patient has a successful knee surgery result).
>
> Solution
>
> Using the data collected from the past two years, there were 200 surgeries performed, with 188 successes. The probability can then be calculated as:
>
> The doctor informs the patient that there is a 94% chance of success for the pending knee surgery.
>
> Theoretical Probability

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-016-pool-015

**Chunk:** `openstax_principles_ds:3.4:chunk-002`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.4: Probability Theory
>
> Basic Concepts of Probability
>
> We have all used probability in one way or another on a day-to-day basis. Before leaving the house, you might
>
> want to know the probability of rain. The probability of obtaining heads on one flip of a coin is one-half, or 0.5.
>
> A data scientist is in interested in expressing probability as a number between 0 and 1 (inclusive), where 0
> indicates impossibility (the event will not occur) and 1 indicates certainty (the event will occur). The probability
> of an event falling between 0 and 1 reflects the degree of uncertainty associated with the event.
>
> Here is some terminology we will be using in probability-related analysis:
>
> • An outcome is the result of a single trial in a probability experiment.
> • The sample space is the set of all possible outcomes in a probability experiment.
> • An event is some subset of the sample space. For example, an event could be rolling an even number on a
> six-sided die. This event corresponds to three outcomes, namely rolling a 2, 4, or 6 on the die.
>
> To calculate probabilities, we can use several approaches, including relative frequency probability, which is
> based on actual data, and theoretical probability, which is based on theoretical conditions.
>
> Relative Frequency Probability
>
> Relative frequency probability is a method of determining the likelihood of an event occurring based on the
> observed frequency of its occurrence in a given sample or population. A data scientist conducts or observes a
> procedure and determines the number of times a certain Event
>  occurs. The probability of Event
> , denoted
> as
> , is then calculated based on data that has been collected from the experiment, as follows:
>
> EXAMPLE 3.14
>
> Problem

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-016-pool-016

**Chunk:** `openstax_principles_ds:3.1:chunk-003`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> The most widely used measures of the center of a dataset are the mean (average), the
> median, and the mode.
>
> Mean and Trimmed Mean
>
> The mean, or average, (sometimes referred to as the arithmetic mean) is the most commonly used measure of
> the center of a dataset. Sometimes the mean can be skewed by the presence of outliers, or data values that
> are significantly different as compared to the remainder of the dataset. In these instances, the trimmed mean
> is often used to provide a more representative measure of the center of the dataset, as we will discuss in the
> following section.
>
> Mean
>
> To calculate the mean, add the values of all the items in a dataset and divide by the number of items. For
> example, if the scores on your last three exams were 87, 92, and 73, then the mean score would be
>
> . If you had a large number of data values, you would proceed in the same way. For example, to
>
> calculate the mean value of 50 exam scores, add the 50 scores together and divide by 50. If the 50 scores add
>
> up to 4,050, for example, the mean score is
> , or 81.
>
> In data science applications, you will encounter two types of datasets: sample data and population data. Population data represents all the outcomes or measurements that are of interest. Sample data represents
> outcomes or measurements collected from a subset, or part, of the population of interest. Of course in many
> applications, collecting data from an entire population is not practical or feasible, and so we often rely on
> sample data.
>
> The notation  is used to indicate the sample mean, where the mean is calculated based on data taken from a
> sample.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-016-pool-017

**Chunk:** `openstax_principles_ds:3.1:chunk-004`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.1: Measures of Center
>
> Of course in many
> applications, collecting data from an entire population is not practical or feasible, and so we often rely on
> sample data.
>
> The notation  is used to indicate the sample mean, where the mean is calculated based on data taken from a
> sample. The notation
>  is used to denote the sum of the data values, and  is used to indicate the number
>
> of data values in the sample, also known as the sample size.
>
> The sample mean can be calculated using the following formula:
>
> The notation  is used to indicate the population mean, where the mean is calculated based on data taken
> from the entire population, and
>  is used to indicate the number of data values in the population, also known
> as the population size. The population mean can be calculated using the following formula:
>
> The mean can also be determined by its frequency distribution. For every unique data value in the dataset, the
> frequency distribution gives the number of times, or frequency, that this unique value appears in the
> dataset. In this type of situation, the mean can be calculated by multiplying each distinct value by its
> frequency, summing these values, and then dividing this sum by the total number of data values. Here is the
> corresponding formula for the sample mean using the frequency distribution:
>
> When all the values in the dataset are unique, this reduces to the previous formula given for the sample mean.
>
> EXAMPLE 3.1
>
> Problem
>
> During a clinical trial, a sample is taken of 10 patients and pulse rates are measured in beats per minute:
>
> 68, 92, 76, 51, 65, 83, 94, 72, 88, 59
>
> Calculate the mean pulse rate for this sample.
>
> Solution
>
> Add the 10 data values, and the sum is 748.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-017

**Pregunta:** When is one-way ANOVA an appropriate choice, and how are its null and alternative hypotheses framed?

**Respondibilidad de referencia:** answerable

### q-v1-017-pool-001

**Chunk:** `openstax_intro_stats_2e:9.1:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.1: Null and Alternative Hypotheses
>
> 5. Make a decision and write a meaningful conclusion.
>
> NOTE
>
> To do the hypothesis test homework problems for this chapter and later chapters, make copies of the appropriate
> special solution sheets. See Appendix E.
>
> 9.1 Null and Alternative Hypotheses
>
> The actual test begins by considering two hypotheses. They are called the null hypothesis and the alternative
> hypothesis. These hypotheses contain opposing viewpoints.
>
> H0: The null hypothesis: It is a statement of no difference between the variables—they are not related. This can often be
> considered the status quo and as a result if you cannot accept the null it requires some action.
>
> Ha: The alternative hypothesis: It is a claim about the population that is contradictory to H0 and what we conclude
> when we reject H0. This is usually what the researcher is trying to prove.
>
> Since the null and alternative hypotheses are contradictory, you must examine evidence to decide if you have enough
> evidence to reject the null hypothesis or not. The evidence is in the form of sample data.
>
> After you have determined which hypothesis the sample supports, you make a decision. There are two options for a
> decision. They are "reject H0" if the sample information favors the alternative hypothesis or "do not reject H0" or "decline
> to reject H0" if the sample information is insufficient to reject the null hypothesis.
>
> Mathematical Symbols Used in H0 and Ha:
>
> H0
> Ha
>
> equal (=)
> not equal (≠) or greater than (>) or less than (<)
>
> greater than or equal to (≥)
> less than (<)
>
> less than or equal to (≤)
> more than (>)
>
> Table 9.1
>
> NOTE
>
> H0 always has a symbol with an equal in it. Ha never has a symbol with an equal in it. The choice of symbol depends
> on the wording of the hypothesis test.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-017-pool-003

**Chunk:** `openstax_intro_stats_2e:9.1:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.1: Null and Alternative Hypotheses
>
> greater than or equal to (≥)
> less than (<)
>
> less than or equal to (≤)
> more than (>)
>
> Table 9.1
>
> NOTE
>
> H0 always has a symbol with an equal in it. Ha never has a symbol with an equal in it. The choice of symbol depends
> on the wording of the hypothesis test. However, be aware that many researchers (including one of the co-authors in
> research work) use = in the null hypothesis, even with > or < as the symbol in the alternative hypothesis. This practice
> is acceptable because we only make the decision to reject or not reject the null hypothesis.
>
> EXAMPLE 9.1
>
> H0: No more than 30% of the registered voters in Santa Clara County voted in the primary election. p ≤ .30
> Ha: More than 30% of the registered voters in Santa Clara County voted in the primary election. p > 30
>
> TRY IT 9.1
>
> A medical trial is conducted to test whether or not a new medicine reduces cholesterol by 25%. State the null and
> alternative hypotheses.
>
> EXAMPLE 9.2
>
> We want to test whether the mean GPA of students in American colleges is different from 2.0 (out of 4.0). The null and
> alternative hypotheses are:
> H0: μ = 2.0
> Ha: μ ≠ 2.0
>
> TRY IT 9.2
>
> We want to test whether the mean height of eighth graders is 66 inches. State the null and alternative hypotheses. Fill
> in the correct symbol (=, ≠, ≥, <, ≤, >) for the null and alternative hypotheses.
>
> a. H0: μ __ 66
> b. Ha: μ __ 66
>
> EXAMPLE 9.3
>
> We want to test if college students take less than five years to graduate from college, on the average. The null and
> alternative hypotheses are:
> H0: μ ≥ 5
> Ha: μ < 5
>
> TRY IT 9.3

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-017-pool-005

**Chunk:** `openstax_principles_ds:4.4:chunk-007`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.4: Analysis of Variance (ANOVA)
>
> The following Python program generates the corresponding F test statistic and p-value for this ANOVA
> analysis:
>
> PYTHON CODE
>
> # import libraries
> import numpy as np
> from scipy.stats  import f_oneway
>  
> # enter airline arrival data
>
> AirlineA = np.array([8, 12, 7, 9, 11, 4])
> AirlineB = np.array([13, 0, 2, 7, 6, 5])
> AirlineC = np.array([11, 15, 9, 11, 12])
>
> #f_oneway function returns both the test statistic and p-value
> f_oneway(AirlineA, AirlineB, AirlineC)
>
> The resulting output will look like this:
>
> F_onewayResult(statistic=4.388264306955828, pvalue=0.03314999857295516)
>
> From this Python output, the test statistic is
>  and the p-value is 0.033.
>
> The final step in the hypothesis testing procedure is to come to a final decision regarding the null
> hypothesis. This is accomplished by comparing the p-value with the level of significance. In this example,
> the p-value is 0.033 and the level of significance is 0.05: since the p-value  level of significance, the
> decision is to “reject the null hypothesis.”
>
> Conclusion: The decision is to reject the null hypothesis. The claim corresponds to the null hypothesis. This
> scenario corresponds to the first row in Table 4.18 and thus the conclusion is: There is enough evidence to
> reject the claim that the average arrival delays are the same for three airlines. This implies that at least one
> of the means is different from the others.
>
> Note: The ANOVA test method does not specify which mean is different from the others. Further statistical
> analysis is needed to make this determination.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-017-pool-006

**Chunk:** `openstax_principles_ds:4.2:chunk-004`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> For this example, the null hypothesis would be
> written as:
>
> Where the notation  refers to the population mean time to complete an exam. The null hypothesis will always contain one of the following three symbols:
> .
>
> The alternative hypothesis is labeled as
>  and will be the complement of the null hypothesis. For example, if
> the null hypothesis contains an equals symbol, then the alternative hypothesis will contain a not equals
> symbol.
>
> If the null hypothesis contains a  symbol, then the alternative hypothesis will contain a  symbol. If the null hypothesis contains a  symbol, then the alternative hypothesis will contain a  symbol.
>
> Note that the alternative hypothesis will always contain one of the following three symbols:
> .
>
> To write the null and alternative hypotheses, start off by translating the claim into a mathematical statement
>
> involving the unknown population parameter. Depending on the wording, the claim can be placed in either the
> null or the alternative hypothesis. Then write the complement of this statement as the other hypothesis (see
> Table 4.6).
>
> When translating claims about a population mean, use the symbol  as part of the null and alternative
> hypotheses. When translating claims about a population proportion, use the symbol p as part of the null and
> alternative hypotheses.
>
> Table 4.6 provides the three possible setups for the null and alternative hypotheses when conducting a one-
> sample hypothesis test for a population mean. Notice that for each setup, the null and alternative hypotheses
> are complements of one another. Note that the value of “ ” will be replaced by some numerical constant taken
> from the stated claim.
>
> Setup A
> Setup B
> Setup C
>
> Table 4.6 Possible Setups for the Null and
> Alternative Hypotheses for a Population Mean (One
> Sample)

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-017-pool-007

**Chunk:** `openstax_intro_stats_2e:9.4:chunk-006`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.4: Rare Events, the Sample, Decision and Conclusion
>
> It may or may not be given to you at the beginning of the problem.
>
> When you make a decision to reject or not reject H0, do as follows:
>
> • If α > p-value, reject H0. The results of the sample data are significant. There is sufficient evidence to conclude that
> H0 is an incorrect belief and that the alternative hypothesis, Ha, may be correct.
> • If α ≤ p-value, do not reject H0. The results of the sample data are not significant.There is not sufficient evidence to
> conclude that the alternative hypothesis,Ha, may be correct.
> • When you "do not reject H0", it does not mean that you should believe that H0 is true. It simply means that the
> sample data have failed to provide sufficient evidence to cast serious doubt about the truthfulness of Ho.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-017-pool-008

**Chunk:** `openstax_principles_ds:4.4:chunk-006`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.4: Analysis of Variance (ANOVA)
>
> The details of this Python function are shown in Example 4.25.
>
> Here is a step-by-step example to illustrate this ANOVA hypothesis testing process.
>
> EXAMPLE 4.25
>
> Problem
>
> An airline manager claims that the average arrival delays for flights from Boston to Dallas are the same for
> three airlines: Airlines A, B, and C. The following arrival delay data (in minutes) is collected on samples of
> flights for the three airlines (Table 4.18):
>
> Airline
>
> Airline
>
> Airline C
>
> A
>
> B
>
> 8
> 13
> 11
>
> 12
> 0
> 15
>
> 7
> 2
> 9
>
> 9
> 7
> 11
>
> 11
> 6
> 12
>
> 4
> 5
> N/A
>
> Table 4.18 Arrival Delay Data (in Minutes)
> for Three Airlines
>
> Use this sample data to test the claim that the average arrival delays are the same for three airlines: Airlines
> A, B, and C. Use a level of significance of 0.05 for this analysis. Assume the samples are independent and
> taken from approximately normal distributions and each population has approximately the same variance.
>
> Solution
>
> The first step in the hypothesis testing procedure is to write the null and alternative hypothesis based on
> the claim.
>
> For an ANOVA hypothesis test, the setup of the null and alternative hypotheses is shown here. Notice that
> the claim mentions “the average arrival delays are the same for three airlines,” which corresponds to the
> null hypothesis.
>
> : All three population means are equal:
>  [Claim]
>
> : At least one population mean is different from the others.
>
> The following Python program generates the corresponding F test statistic and p-value for this ANOVA
> analysis:
>
> PYTHON CODE
>
> # import libraries
> import numpy as np
> from scipy.stats  import f_oneway
>  
> # enter airline arrival data
>
> AirlineA = np.array([8, 12, 7, 9, 11, 4])
> AirlineB = np.array([13, 0, 2, 7, 6, 5])
> AirlineC = np.array([11, 15, 9, 11, 12])

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-017-pool-009

**Chunk:** `openstax_principles_ds:4.2:chunk-024`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> As a reminder, the general hypothesis testing method introduced in the previous section includes the following
> steps:
>
> 1. Set up a null and an alternative hypothesis based on the claim. 2. Collect relevant sample data to investigate the claim. 3. Determine the correct distribution to be used to analyze the hypothesis test (e.g., normal distribution or t-
> distribution). 4. Analyze the sample data to determine if the sample data is consistent with the null hypothesis. This will
> involve statistical calculations involving a test statistic and a p-value, which are discussed next. 5. If the sample data is inconsistent with the null hypothesis, then the decision is to “reject the null
> hypothesis.” If the sample data is consistent with the null hypothesis, then the decision is to “fail to reject
> the null hypothesis.”
>
> As discussed for one-sample hypothesis testing, when writing the null and alternative hypotheses, start off by
> translating the claim into a mathematical statement involving the unknown population parameters. The claim
> could correspond to either the null or the alternative hypothesis. Then write the complement of this statement
> in order to write the other hypothesis. The difference now as compared to the previous section is that the
> hypotheses will be comparing two means or two proportions instead of just one mean or one proportion.
>
> When translating claims about a population mean, use the symbols
>  and
>  as part of the null and
> alternative hypotheses to represent the two unknown population means. When translating claims about a
> population proportions, use the symbols p1 and p2 as part of the null and alternative hypotheses to represent
> the two unknown population proportions. Refer to Table 4.9 and Table 4.10 for the various setups to construct
>
> the null and alternative hypotheses for two-sample hypothesis testing.
>
> Setup A
> Setup B
> Setup C

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-017-pool-010

**Chunk:** `openstax_principles_ds:4.2:chunk-033`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> Thus the setup
>
> of the null and alternative hypotheses will be as follows:
>
> The mean of the differences is average of the differences column shown in Table 4.13. The mean of the
> differences column is 13.9, and the standard deviation of the differences column is 12.414.
>
> Next, calculate the standardized test statistic as follows:
>
> Notice that since the alternative hypothesis contains a “greater than” symbol, the hypothesis test is called a
> “right tailed” test and the p-value will be calculated as the area under the t-distribution curve to the right of
> the test statistic. The area under the t-distribution curve to the right of a t-score of 3.541 (using degrees of
> freedom
> ) is approximately 0.003. Thus the p-value for this hypothesis test is 0.003.
>
> The final step in the hypothesis testing procedure is to come to a final decision regarding the null
> hypothesis. This is accomplished by comparing the p-value with the level of significance. In this example,
> the p-value is 0.003 and the level of significance is 0.05: since the p-value  level of significance, then the
> decision is to “reject the null hypothesis.”
>
> Conclusion: The decision is to reject the null hypothesis; the claim corresponds to the alternative
> hypothesis. This scenario corresponds to Row 2 in Table 4.8, and “there is enough evidence to support the
> claim that the medication helps to lower cholesterol levels.”
>
> Testing Claims for Two Proportions
>
> Data scientists and researchers are often interested in comparing two proportions. For example, a medical
> researcher might be interested in comparing the percentage of people contracting a respiratory virus for
> those taking a vaccine versus not taking a vaccine.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-017-pool-011

**Chunk:** `openstax_principles_ds:4.4:chunk-005`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.4: Analysis of Variance (ANOVA)
>
> For degrees of freedom for the denominator, this is calculated as the total of the sample sizes minus the
> number of groups. 6. Calculate the quantity called “mean square between (MSB)” according to the following formula:
>
> 7. Calculate the quantity called “mean square within (MSW)” according to the following formula:
>
> 8. Calculate the test statistic (
> ), according to the following formula:
>
> Once the test statistic is obtained, the p-value is calculated as the area to the right of the test statistic under
> the
> -distribution curve (note that the ANOVA hypothesis test is always considered a “right-tail” test).
>
> Usually, the results of these computations are organized in an ANOVA summary table like Table 4.17.
>
> Degrees
>
> p-value
>
> Variation
> Sum of
> Squares
>
> Mean
> Squares
>
> Test Statistic
>
> of
> Freedom
>
> Between
> SSB
> MSB
> Area to the right of the F test statistic
>
> Within
> SSW
> MSW
> N/A
>
> Table 4.17 ANOVA Summary Table
>
> Using Python for One-Way ANOVA
>
> As mentioned earlier, due to the complexity of these calculations, technology is typically used to calculate the
> test statistic and p-value.
>
> Using Python, the f_oneway() function is provided as part of the scipy library, and this function provides
>
> both the test statistic and p-value for a one-way ANOVA hypothesis test.
>
> The syntax is to call the function with the data arrays as arguments, as in:
>
> f_oneway(Array1, Array2, Array3, …)
>
> The function returns both the F test statistic and the p-value for the one-way ANOVA hypothesis test.
>
> The details of this Python function are shown in Example 4.25.
>
> Here is a step-by-step example to illustrate this ANOVA hypothesis testing process.
>
> EXAMPLE 4.25
>
> Problem
>
> An airline manager claims that the average arrival delays for flights from Boston to Dallas are the same for
> three airlines: Airlines A, B, and C.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-017-pool-012

**Chunk:** `openstax_principles_ds:4.2:chunk-025`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> When translating claims about a
> population proportions, use the symbols p1 and p2 as part of the null and alternative hypotheses to represent
> the two unknown population proportions. Refer to Table 4.9 and Table 4.10 for the various setups to construct
>
> the null and alternative hypotheses for two-sample hypothesis testing.
>
> Setup A
> Setup B
> Setup C
>
> Table 4.9 Three Possible Setups for the Null and Alternative Hypotheses
> for a Population Mean (Two Samples)
>
> Setup D
> Setup E
> Setup F
>
> Table 4.10 Three Possible Setups for the Null and Alternative
> Hypotheses for a Population Proportion (Two Samples)
>
> Comparing Two Means
>
> In this section, we discuss two-sample hypothesis testing for the mean when the population standard
> deviations are unknown. Typically, in real-world applications, population standard deviations are unknown, so
> this method has considerable practical appeal.
>
> One other consideration when conducting hypothesis testing for two samples is to determine if the two
> samples are dependent or independent. Two samples are considered to be independent samples when the
> sample values from one population are not related to the sample values taken from the second population. In
> other words, there is not an inherent paired or matched relationship between the two samples. Two samples
> are considered to be dependent samples if the samples from one population can be paired or matched to the
> samples taken from the second population. Dependent samples are sometimes also called paired samples.
>
> For example, if a researcher were to collect data for the ages for a random sample of 15 men and a random
> sample of 15 women, there would be no inherent relationship between these two samples, and so these
> samples are considered independent samples.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-017-pool-013

**Chunk:** `openstax_principles_ds:4.2:chunk-003`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> The steps for hypothesis testing are as follows:
>
> 1. Set up a null and alternative hypothesis based on the claim. Identify whether the null or the alternative
> hypothesis represents the claim. 2. Collect relevant sample data to investigate the claim. 3. Determine the correct distribution to be used to analyze the hypothesis test (e.g., normal distribution or t-
> distribution). 4. Analyze the sample data to determine if the sample data is consistent with the null hypothesis. This will
> involve statistical calculations involving what is called a test statistic and a p-value (discussed in the next
> section). 5. If the sample data is inconsistent with the null hypothesis, then the decision is to “reject the null
> hypothesis.” If the sample data is consistent with the null hypothesis, then the decision is to “fail to reject
> the null hypothesis.”
>
> The first step in the hypothesis testing process is to write what is a called a “null” hypothesis and an
> “alternative” hypothesis. These hypotheses will be statements regarding an unknown population parameter,
> such as a population mean or a population proportion. These two hypotheses are based on the claim under
> study and will be written as complementary statements to each other. When one of the hypotheses is true, the
> other hypothesis must be false (since they are complements of one another). Note that either the null or
> alternative hypothesis can represent the claim.
>
> The null hypothesis is labeled as
>  and is a statement of equality—for example, the null hypothesis might
> state that the mean time to complete an exam is 42 minutes. For this example, the null hypothesis would be
> written as:
>
> Where the notation  refers to the population mean time to complete an exam. The null hypothesis will always contain one of the following three symbols:
> .

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-017-pool-014

**Chunk:** `openstax_principles_ds:4.2:chunk-022`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> Notice that this setup will correspond to Setup B from Table 4.6. Thus the setup of the null and alternative hypotheses will be as follows:
>
> Since the population standard deviation is unknown in this example, the t-distribution will be used to
> conduct the hypothesis test.
>
> To use the ttest_1samp() function in Python, the syntax is as follows:
>
> Ttest_1samp(data_array, null_hypothesis_mean)
>
> The function will then return the value of the test statistic and the two-tailed p-value.
>
> In this example we are interested in the right tailed p-value, so the Python program will calculate one-half
> of the p-value returned by the function.
>
> Here is the Python code for this example:
>
> PYTHON CODE
>
> import scipy.stats as stats
> import numpy as np
>
> # Enter data array
> oxygen_level = np.array([76, 75, 74, 81, 76, 77, 71, 74, 73, 79])
>
> # Hypothesized population mean
> null_hypothesis_mean = 75
>
> # Perform one-sample t-test
> test_stat, two_tailed_p_value = stats.ttest_1samp(oxygen_level,
> null_hypothesis_mean)
>
> # Obtain the one tailed p-value
> one_tailed_p_value = two_tailed_p_value / 2
>
> # print out test statistic and p-value and round to 3 decimal places
> print("Test Statistic = ", test_stat)
> print("p-value = ", one_tailed_p_value)
>
> The resulting output will look like this:
>
> Test Statistic = 0.6512171447631733
> p-value = 0.2655900985964262
>
> The final step in the hypothesis testing procedure is to come to a final decision regarding the null
> hypothesis. This is accomplished by comparing the p-value with the level of significance. In this example,
> the p-value is 0.266 and the level of significance is 0.05: since the p-value  level of significance, the
> decision is to “fail to reject the null hypothesis.”
>
> Conclusion: The decision is to fail to reject the null hypothesis; the claim corresponds to the alternative
> hypothesis.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-018

**Pregunta:** What is the quartile-normalized z-score, and how does it combine the interquartile range with the standard deviation?

**Respondibilidad de referencia:** unanswerable

### q-v1-018-pool-001

**Chunk:** `openstax_intro_stats_2e:6.2:chunk-004`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 6: The Normal Distribution
> Section 6.2: Using the Normal Distribution
>
> Before technology, the
> z-score was looked up in a standard normal probability table (because the math involved is too cumbersome) to find
> the probability. In this example, a standard normal table with area to the left of the z-score was used. You calculate
> the z-score and look up the area to the left. The probability is the area to the right.
>
> z =
>  = 0.4
>
> Area to the left is 0.6554.
>
> P(x > 65) = P(z > 0.4) = 1 – 0.6554 = 0.3446
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> Find the percentile for a student scoring 65:
>
> *Press 2nd Distr
>
> *Press 2:normalcdf(
>
> *Enter lower bound, upper bound, mean, standard deviation followed by )
> *Press ENTER.
>
> For this Example, the steps are
> 2nd Distr
>
> 2:normalcdf(65,1,2nd EE,99,63,5) ENTER
>
> The probability that a selected student scored more than 65 is 0.3446. To find the probability that a selected student scored more than 65, subtract the percentile from 1.
>
> Problem
> b. Find the probability that a randomly selected student scored less than 85.
>
> Solution
> b. Draw a graph.
>
> Then find P(x < 85), and shade the graph.
>
> Using a computer or calculator, find P(x < 85) = 1.
>
> normalcdf(0,85,63,5) = 1 (rounds to one)
>
> The probability that one student scores less than 85 is approximately one (or 100%).
>
> Problem
> c. Find the 90th percentile (that is, find the score k that has 90% of the scores below k and 10% of the scores above k).
>
> Solution
> c. Find the 90th percentile. For each problem or part of a problem, draw a new graph. Draw the x-axis. Shade the area
> that corresponds to the 90th percentile.
>
> Let k = the 90th percentile. The variable k is located on the x-axis. P(x < k) is the area to the left of k.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-018-pool-002

**Chunk:** `openstax_principles_ds:3.3:chunk-006`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.3: Measures of Position
>
> Order the data from smallest to largest.
>
> 114950, 158000, 230500, 387000, 389950, 479000, 488800, 529000, 575000, 639000, 659000, 1095000,
> 5500000
>
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
> 1,159,375. Therefore, the home price of $5,500,000 is a potential outlier. This is important because the
> presence of outliers could potentially indicate data errors or some other anomalies in the dataset that
> should be investigated. For example, there may have been a data entry error and a home price of $550,000
> was erroneously entered as $5,500,000.
>
> -scores
>
> The -score is a measure of the position of an entry in a dataset that makes use of the mean and standard
> deviation of the data. It represents the number of standard deviations by which a data value differs from the
> mean.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-018-pool-003

**Chunk:** `openstax_intro_stats_2e:6.2:chunk-008`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 6: The Normal Distribution
> Section 6.2: Using the Normal Distribution
>
> TRY IT 6.10
>
> Use the information in Example 6.10 to answer the following questions.
>
> a. Find the 30th percentile, and interpret it in a complete sentence.
> b. What is the probability that the age of a randomly selected smartphone user in the range 13 to 55+ is less than
>
> 27 years old.
>
> EXAMPLE 6.11
>
> In the United States the ages 13 to 55+ of smartphone users approximately follow a normal distribution with
> approximate mean and standard deviation of 36.9 years and 13.9 years respectively. Using this information, answer the
> following questions (round answers to one decimal place).
>
> Problem
> a. Calculate the interquartile range (IQR).
>
> b. Forty percent of the smartphone users from 13 to 55+ are at least what age?
>
> Solution
> a.
>
> IQR = Q3 – Q1
> Calculate Q3 = 75th percentile and Q1 = 25th percentile.
> invNorm(0.75,36.9,13.9) = Q3 = 46.2754
> invNorm(0.25,36.9,13.9) = Q1 = 27.5246
> IQR = Q3 – Q1 = 18.8
>
> b.
>
> Find k where P(x ≥ k) = 0.40 ("At least" translates to "greater than or equal to.")
> 0.40 = the area to the right. Area to the left = 1 – 0.40 = 0.60. The area to the left of k = 0.60.
>
> invNorm(0.60,36.9,13.9) = 40.4215.
> k = 40.4. Forty percent of the smartphone users from 13 to 55+ are at least 40.4 years.
>
> TRY IT 6.11
>
> Two thousand students took an exam. The scores on the exam have an approximate normal distribution with a mean
> μ = 81 points and standard deviation σ = 15 points.
>
> a. Calculate the first- and third-quartile scores for this exam.
> b. The middle 50% of the exam scores are between what two values?
>
> EXAMPLE 6.12

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-018-pool-004

**Chunk:** `openstax_intro_stats_2e:6.1:chunk-005`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 6: The Normal Distribution
> Section 6.1: The Standard Normal Distribution
>
> The z-score for y = 4 is z = 2. This means that four is z = 2 standard deviations to the right of the mean. Therefore, x = 17
> and y = 4 are both two (of their own) standard deviations to the right of their respective means.
>
> The z-score allows us to compare data that are scaled differently. To understand the concept, suppose X ~ N(5, 6)
> represents weight gains for one group of people who are trying to gain weight in a six week period and Y ~ N(2, 1)
> measures the same weight gain for a second group of people. A negative weight gain would be a weight loss. Since x =
> 17 and y = 4 are each two standard deviations to the right of their means, they represent the same, standardized weight
> gain relative to their means.
>
> TRY IT 6.2
>
> Fill in the blanks.
>
> Jerome averages 16 points a game with a standard deviation of four points. X ~ N(16,4). Suppose Jerome scores ten
> points in a game. The z–score when x = 10 is –1.5. This score tells you that x = 10 is _____ standard deviations to the
> ______(right or left) of the mean______(What is the mean?).
>
> The Empirical Rule
> If X is a random variable and has a normal distribution with mean µ and standard deviation σ, then the Empirical Rule
> states the following:

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-018-pool-005

**Chunk:** `openstax_intro_stats_2e:6.2:chunk-007`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 6: The Normal Distribution
> Section 6.2: Using the Normal Distribution
>
> Find the maximum number of hours per day that the bottom quartile of households uses a personal computer for
> entertainment.
>
> Solution
> b. To find the maximum number of hours per day that the bottom quartile of households uses a personal computer for
> entertainment, find the 25th percentile, k, where P(x < k) = 0.25.
>
> Figure 6.8
>
> invNorm(0.25,2,0.5) = 1.66
>
> The maximum number of hours per day that the bottom quartile of households uses a personal computer for
> entertainment is 1.66 hours.
>
> TRY IT 6.9
>
> The golf scores for a school team were normally distributed with a mean of 68 and a standard deviation of three. Find
> the probability that a golfer scored between 66 and 70.
>
> EXAMPLE 6.10
>
> In the United States the ages 13 to 55+ of smartphone users approximately follow a normal distribution with
>
> approximate mean and standard deviation of 36.9 years and 13.9 years, respectively.
>
> Problem
> a. Determine the probability that a random smartphone user in the age range 13 to 55+ is between 23 and 64.7 years
> old.
>
> b. Determine the probability that a randomly selected smartphone user in the age range 13 to 55+ is at most 50.8 years
> old.
>
> c. Find the 80th percentile of this distribution, and interpret it in a complete sentence.
>
> Solution
> a. normalcdf(23,64.7,36.9,13.9) = 0.8186
>
> b. normalcdf(–1099,50.8,36.9,13.9) = 0.8413
>
> c.
>
> invNorm(0.80,36.9,13.9) = 48.6
> The 80th percentile is 48.6 years. 80% of the smartphone users in the age range 13 – 55+ are 48.6 years old or less.
>
> TRY IT 6.10
>
> Use the information in Example 6.10 to answer the following questions.
>
> a. Find the 30th percentile, and interpret it in a complete sentence.
> b. What is the probability that the age of a randomly selected smartphone user in the range 13 to 55+ is less than
>
> 27 years old.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-018-pool-006

**Chunk:** `openstax_intro_stats_2e:6.2:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 6: The Normal Distribution
> Section 6.2: Using the Normal Distribution
>
> TRY IT 6.7
>
> If the area to the left of x is 0.012, then what is the area to the right?
>
> EXAMPLE 6.8
>
> The final exam scores in a statistics class were normally distributed with a mean of 63 and a standard deviation of five.
>
> Problem
> a. Find the probability that a randomly selected student scored more than 65 on the exam.
>
> Solution
> a. Let X = a score on the final exam. X ~ N(63, 5), where μ = 63 and σ = 5.
>
> Draw a graph.
>
> Then, find P(x > 65).
>
> P(x > 65) = 0.3446
>
> Figure 6.5
>
> The probability that any student selected at random scores more than 65 is 0.3446.
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> Go into 2nd DISTR.
>
> After pressing 2nd DISTR, press 2:normalcdf.
>
> The syntax for the instructions are as follows:
>
> normalcdf(lower value, upper value, mean, standard deviation) For this problem: normalcdf(65,1E99,63,5) = 0.3446. You get 1E99 (= 1099) by pressing 1, the EE key (a 2nd key) and then 99. Or, you can enter 10^99 instead. The number
>
> 1099 is way out in the right tail of the normal curve. We are calculating the area between 65 and 1099. In some
>
> instances, the lower number of the area might be –1E99 (= –1099). The number –1099 is way out in the left tail of the
> normal curve.
>
> Historical Note
>
> The TI probability program calculates a z-score and then the probability from the z-score. Before technology, the
> z-score was looked up in a standard normal probability table (because the math involved is too cumbersome) to find
> the probability. In this example, a standard normal table with area to the left of the z-score was used. You calculate
> the z-score and look up the area to the left.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-018-pool-007

**Chunk:** `openstax_principles_ds:3.3:chunk-004`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.3: Measures of Position
>
> The upper half of the
> data values are 7.4, 7.5, 7.9, 8.2, 8.7, which are the data values above the median.
>
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
> Quartiles and the IQR can be used to flag possible outliers in a dataset. For example, if most employees at a
> company earn about $50,000 and the CEO of the company earns $2.5 million, then we consider the CEO’s
> salary to be an outlier data value because this salary is significantly different from all the other salaries in the
> dataset.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-018-pool-008

**Chunk:** `openstax_intro_stats_2e:6.1:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 6: The Normal Distribution
> Section 6.1: The Standard Normal Distribution
>
> Calculate the
>
> mean for each data set. Write the means on the x-axis of the appropriate graph below the peak. Shade the
> approximate area that represents the probability that one randomly chosen male is taller than 72 inches. Shade the
> approximate area that represents the probability that one randomly chosen female is shorter than 60 inches. If the
> total area under each curve is one, does either probability appear to be more than 0.5?
>
> 6.1 The Standard Normal Distribution
>
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
>
> EXAMPLE 6.1
>
> Suppose X ~ N(5, 6).

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-018-pool-009

**Chunk:** `openstax_intro_stats_2e:6.1:chunk-008`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 6: The Normal Distribution
> Section 6.1: The Standard Normal Distribution
>
> What is
>
> the male’s height? The z-score (z = –2) tells you that the male’s height is ________ standard deviations to the
> __________ (right or left) of the mean.
>
> EXAMPLE 6.4
>
> Problem
> From 1984 to 1985, the mean height of 15 to 18-year-old males from Chile was 172.36 cm, and the standard deviation
> was 6.34 cm. Let Y = the height of 15 to 18-year-old males from 1984 to 1985. Then Y ~ N(172.36, 6.34).
>
> The mean height of 15 to 18-year-old males from Chile from 2009 to 2010 was 170 cm with a standard deviation of 6.28
> cm. Male heights are known to follow a normal distribution. Let X = the height of a 15 to 18-year-old male from Chile in
> 2009 to 2010. Then X ~ N(170, 6.28).
>
> Find the z-scores for x = 160.58 cm and y = 162.85 cm. Interpret each z-score. What can you say about x = 160.58 cm and
> y = 162.85 cm as they compare to their respective means and standard deviations?
>
> Solution
> The z-score for x = -160.58 is z = –1.5. The z-score for y = 162.85 is z = –1.5. Both x = 160.58 and y = 162.85 deviate the same number of standard deviations from their respective means and in the
> same direction.
>
> TRY IT 6.4
>
> In 2012, 1,664,479 students took the SAT exam. The distribution of scores in the verbal section of the SAT had a mean
> µ = 496 and a standard deviation σ = 114. Let X = a SAT exam verbal section score in 2012. Then X ~ N(496, 114).
>
> Find the z-scores for x1 = 325 and x2 = 366.21. Interpret each z-score.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-018-pool-010

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-005`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> CL = 1 – α, so α is the area that is
> split equally between the two tails. Each of the tails contains an area equal to
> .
>
> The z-score that has an area to the right of
>  is denoted by
> .
>
> For example, when CL = 0.95, α = 0.05 and
>  = 0.025; we write
>  = z0.025.
>
> The area to the right of z0.025 is 0.025 and the area to the left of z0.025 is 1 – 0.025 = 0.975.
>
> , using a calculator, computer or a standard normal probability table.
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> invNorm(0.975, 0, 1) = 1.96
>
> NOTE
>
> Remember to use the area to the LEFT of
> ; in this chapter the last two inputs in the invNorm command are 0, 1,
>
> because you are using a standard normal distribution Z ~ N(0, 1).
>
> Writing the Interpretation
> The interpretation should clearly state the confidence level (CL), explain what population parameter is being estimated
> (here, a population mean), and state the confidence interval (both endpoints). "We estimate with ___% confidence that
> the true population mean (include the context of the problem) is between ___ and ___ (include appropriate units)."
>
> EXAMPLE 8.2
>
> Suppose scores on exams in statistics are normally distributed with an unknown population mean and a population
> standard deviation of three points. A random sample of 36 scores is taken and gives a sample mean (sample mean score)
> of 68. Find a confidence interval estimate for the population mean exam score (the mean score on all exams).
>
> Problem
> Find a 90% confidence interval for the true (population) mean of statistics exam scores.
>
> Solution
> • You can use technology to calculate the confidence interval directly.
> • The first solution is shown step-by-step.
> • The second solution uses the TI-83, 83+, and 84+ calculators.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-018-pool-011

**Chunk:** `openstax_intro_stats_2e:6.1:chunk-007`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 6: The Normal Distribution
> Section 6.1: The Standard Normal Distribution
>
> Male heights are known to follow a normal distribution. Let X = the height of a 15 to 18-year-old male from Chile in
> 2009 to 2010. Then X ~ N(170, 6.28).
>
> Problem
> a. Suppose a 15 to 18-year-old male from Chile was 168 cm tall from 2009 to 2010. The z-score when x = 168 cm is z =
> _______. This z-score tells you that x = 168 is ________ standard deviations to the ________ (right or left) of the mean _____
> (What is the mean?).
>
> b. Suppose that the height of a 15 to 18-year-old male from Chile from 2009 to 2010 has a z-score of z = 1.27. What is the
> male’s height? The z-score (z = 1.27) tells you that the male’s height is ________ standard deviations to the __________ (right
> or left) of the mean.
>
> Solution
> a. –0.32, 0.32, left, 170
>
> b. 177.98 cm, 1.27, right
>
> TRY IT 6.3
>
> Use the information in Example 6.3 to answer the following questions.
>
> a. Suppose a 15 to 18-year-old male from Chile was 176 cm tall from 2009 to 2010. The z-score when x = 176 cm is z
>
> = _______. This z-score tells you that x = 176 cm is ________ standard deviations to the ________ (right or left) of the
> mean _____ (What is the mean?).
> b. Suppose that the height of a 15 to 18-year-old male from Chile from 2009 to 2010 has a z-score of z = –2. What is
>
> the male’s height? The z-score (z = –2) tells you that the male’s height is ________ standard deviations to the
> __________ (right or left) of the mean.
>
> EXAMPLE 6.4
>
> Problem
> From 1984 to 1985, the mean height of 15 to 18-year-old males from Chile was 172.36 cm, and the standard deviation
> was 6.34 cm.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-018-pool-012

**Chunk:** `openstax_intro_stats_2e:6.1:chunk-009`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 6: The Normal Distribution
> Section 6.1: The Standard Normal Distribution
>
> The distribution of scores in the verbal section of the SAT had a mean
> µ = 496 and a standard deviation σ = 114. Let X = a SAT exam verbal section score in 2012. Then X ~ N(496, 114).
>
> Find the z-scores for x1 = 325 and x2 = 366.21. Interpret each z-score. What can you say about x1 = 325 and x2 = 366.21
> as they compare to their respective means and standard deviations?
>
> EXAMPLE 6.5
>
> Suppose x has a normal distribution with mean 50 and standard deviation 6.
>
> • About 68% of the x values lie within one standard deviation of the mean. Therefore, about 68% of the x values lie
> between –1σ = (–1)(6) = –6 and 1σ = (1)(6) = 6 of the mean 50. The values 50 – 6 = 44 and 50 + 6 = 56 are within one
> standard deviation from the mean 50. The z-scores are –1 and +1 for 44 and 56, respectively.
> • About 95% of the x values lie within two standard deviations of the mean. Therefore, about 95% of the x values lie
> between –2σ = (–2)(6) = –12 and 2σ = (2)(6) = 12. The values 50 – 12 = 38 and 50 + 12 = 62 are within two standard
> deviations from the mean 50. The z-scores are –2 and +2 for 38 and 62, respectively.
> • About 99.7% of the x values lie within three standard deviations of the mean. Therefore, about 99.7% of the x values
> lie between –3σ = (–3)(6) = –18 and 3σ = (3)(6) = 18 from the mean 50. The values 50 – 18 = 32 and 50 + 18 = 68 are
> within three standard deviations of the mean 50. The z-scores are –3 and +3 for 32 and 68, respectively.
>
> TRY IT 6.5
>
> Suppose X has a normal distribution with mean 25 and standard deviation five. Between what values of x do 68% of

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-018-pool-013

**Chunk:** `openstax_principles_ds:3.2:chunk-001`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.2: Measures of Variation
>
> summarize data. Recall that the method describe() is defined for a DataFrame type object so should be
>
> called upon a DataFrame type variable (e.g. given a DataFrame d, use d.describe()).
>
> Figure 3.2 shows the output of DataFrame.describe() on the “Movie Profit” dataset we used in What Are
>
> Data and Data Science?, movie_profit.csv. The mean and 50% quartile show the average and median of each
> column. For example, the average worldwide gross earnings are $410.14 million, and the median earnings are
> $309.35 million. Note that average and/or median of some columns are not as meaningful as the others. The
> first column—Unnamed: 0—was simply used as an identifier of each item in the dataset, so the average and
> mean of this column is not quite useful. DataFrame.describe() still computes the values because it can (and
>
> it does not care which column is meaningful to do so or not).
>
> Figure 3.2 The Output of DataFrame.describe() with the Movie Profit Dataset
>
> EXPLORING FURTHER
>
> Working with Python
>
> See the Python website (https://openstax.org/r/python) for more details on using, installing, and working
> with Python. See this additional documentation, for more specific information on the statistics module
> (https://openstax.org/r/docspython).
>
> 3.2 Measures of Variation
>
> Learning Outcomes
> By the end of this section, you should be able to:
>
> • 3.2.1 Define and calculate the range, the variance, and the standard deviation for a dataset.
> • 3.2.2 Use Python to calculate measures of variation for a dataset.
>
> Providing some measure of the spread, or variation, in a dataset is crucial to a comprehensive summary of the
> dataset. Two datasets may have the same mean but can exhibit very different spread, and so a measure of
> dispersion for a dataset is very important.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-018-pool-014

**Chunk:** `openstax_principles_ds:4.2:chunk-013`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> Next, calculate the standardized test statistic:
>
> Notice that since the alternative hypothesis contains a “less than” symbol, the hypothesis test is called a
> “left tailed” test and the p-value will be calculated as the area to the left of the test statistic. The area under
> the standard normal curve to the left of a z-score of
>  is approximately 0.0324. Thus, the p-value for
> this hypothesis test is 0.0324.
>
> The area under the standard normal curve can be found using software such as Excel, Python, or R.
>
> For example, in Python, the area under the normal curve to the left of a z-score of
>  can be obtained
> using the function norm.cdf().
>
> The syntax for using this function is
>
> norm.cdf(x, mean, standard_deviation)
>
> Where:
> x is the measurement of interest—in this case, this will be the test statistic of
> .
>
> mean is the mean of the standard normal distribution, which is 0.
>
> standard_deviation is the standard deviation of the standard normal distribution, which is 1.
>
> Here is the Python code to calculate the p-value for this example:
>
> PYTHON CODE
>
> # from scipy.stats import norm
> from scipy.stats import norm
>
> # define parameters x, mean and standard_deviation:
> x = -1.846
> mean = 0
> standard_deviation = 1
> # use norm.cdf function to calculate normal probability - note this is the area
> to the left of the x-value
> # subtract this result from 1 to obtain area to the right of the x-value
> # use round function to round answer to 4 decimal places
> round (norm.cdf(x, mean, standard_deviation), 4)
>
> The resulting output will look like this:
>
> 0.0324
>
> The final step in the hypothesis testing procedure is to come to a final decision regarding the null
>
> hypothesis. This is accomplished by comparing the p-value with the level of significance.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-018-pool-015

**Chunk:** `openstax_intro_stats_2e:7.3:chunk-008`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 7: The Central Limit Theorem
> Section 7.3: Using the Central Limit Theorem
>
> Suppose the
> standard deviation is 0.5 minutes and the sample size is 100.
>
> Problem
> a. Find the median, the first quartile, and the third quartile for the sample mean time of robberies in the United States.
> b. Find the median, the first quartile, and the third quartile for the sum of sample times of robberies in the United
>
> States.
> c. Find the probability that a robbery occurs on the average between 1.75 and 1.85 minutes.
> d. Find the value that is two standard deviations above the sample mean.
> e. Find the IQR for the sum of the sample times.
>
> Solution
>
> a. We have, μx = μ = 2 and σx =
>  =
>  = 0.05. Therefore:
>
> 1. 50th percentile = μx = μ = 2
> 2. 25th percentile = invNorm(0.25,2,0.05) = 1.97
> 3. 75th percentile = invNorm(0.75,2,0.05) = 2.03
>
> b. We have μΣx = n(μx) = 100(2) = 200 and σμx =
> (σx) = 10(0.5) = 5. Therefore
>
> 1. 50th percentile = μΣx = n(μx) = 100(2) = 200
> 2. 25th percentile = invNorm(0.25,200,5) = 196.63
> 3. 75th percentile = invNorm(0.75,200,5) = 203.37
>
> c. P(1.75 <  < 1.85) = normalcdf(1.75,1.85,2,0.05) = 0.0013
>
> d. Using the z-score equation,
> , and solving for x, we have x = 2(0.05) + 2 = 2.1
>
> e. The IQR is 75th percentile – 25th percentile = 203.37 – 196.63 = 6.74
>
> TRY IT 7.10
>
> Based on data from the National Health Survey, females between the ages of 18 and 24 have an average systolic
> blood pressures (in mm Hg) of 114.8 with a standard deviation of 13.1. Systolic blood pressure for females between
> the ages of 18 to 24 follow a normal distribution.
>
> a. If one female from this population is randomly selected, find the probability that their systolic blood pressure is
>
> greater than 120.
> b.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-019

**Pregunta:** According to the selected sources, what is the Shapiro-Wilk p-value for the women's heights dataset?

**Respondibilidad de referencia:** unanswerable

### q-v1-019-pool-001

**Chunk:** `openstax_intro_stats_2e:8.6:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.6: Confidence Interval (Women's Heights)
>
> Confidence level
> EBP/Error Bound
> Confidence Interval
>
> 95%
>
> 99%
>
> Table 8.7
>
> 4. What happens to the EBP as the confidence level increases? Does the width of the confidence interval increase or
> decrease? Explain why this happens.
>
> 8.6 Confidence Interval (Women's Heights)
>
> Stats Lab
>
> Confidence Interval (Women's Heights)
> Class Time:
>
> Names:
>
> Student Learning Outcomes
>
> • The student will calculate a 90% confidence interval using the given data.
> • The student will determine the relationship between the confidence level and the percentage of constructed
> intervals that contain the population mean.
>
> Given:
>
> 59.4
> 71.6
> 69.3
> 65.0
> 62.9
> 66.5
> 61.7
> 55.2
>
> 67.5
> 67.2
> 63.8
> 62.9
> 63.0
> 63.9
> 68.7
> 65.5
>
> 61.9
> 69.6
> 58.7
> 63.4
> 61.8
> 60.6
> 69.8
> 60.0
>
> 64.9
> 66.1
> 66.8
> 60.6
> 65.6
> 63.8
> 61.3
> 59.2
>
> 64.1
> 59.3
> 64.9
> 62.4
> 63.5
> 60.9
> 63.3
> 66.3
>
> 61.5
> 64.3
> 62.9
> 60.6
> 63.8
> 58.8
> 64.9
> 65.7
>
> 62.5
> 70.9
> 62.9
> 63.1
> 62.2
> 58.7
> 64.7
> 66.0
>
> 60.5
> 64.7
> 65.4
> 60.2
> 65.0
> 64.1
> 61.1
> 65.3
>
> 64.6
> 59.2
> 61.4
> 62.0
> 63.5
> 61.4
> 65.5
> 62.3
>
> 65.5
> 64.7
> 58.8
> 66.1
> 64.9
> 66.9
> 57.9
> 69.8
>
> 58.5
> 63.4
> 69.2
> 65.9
> 62.2
> 60.0
> 58.1
> 62.5
>
> Table 8.8 Heights of 100 Women (in Inches)
>
> 62.4
> 59.1
> 66.4
> 61.2
> 60.4
> 58.7
> 66.7
> 67.5
>
> 63.2
> 56.6
> 67.7
> 62.5
>
> Table 8.8 Heights of 100 Women (in Inches)
>
> 1. Table 8.8 lists the heights of 100 women. Use a random number generator to select ten data values randomly. 2. Calculate the sample mean and the sample standard deviation. Assume that the population standard deviation is
> known to be 3.3 inches. With these values, construct a 90% confidence interval for your sample of ten values. Write
> the confidence interval you obtained in the first space of Table 8.9. 3. Now write your confidence interval on the board. As others in the class write their confidence intervals on the board,
> copy them into Table 8.9.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-019-pool-002

**Chunk:** `openstax_intro_stats_2e:8.6:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.6: Confidence Interval (Women's Heights)
>
> 5. When we construct a 90% confidence interval, we say that we are 90% confident that the true population mean
> lies within the confidence interval. Using complete sentences, explain what we mean by this phrase. 6. Some students think that a 90% confidence interval contains 90% of the data. Use the list of data given (the heights
> of women) and count how many of the data values lie within the confidence interval that you generated based on
> that data. How many of the 100 data values lie within your confidence interval? What percent is this? Is this percent
> close to 90%? 7. Explain why it does not make sense to count data values that lie in a confidence interval. Think about the random
> variable that is being used in the problem. 8. Suppose you obtained the heights of ten women and calculated a confidence interval from this information. Without knowing the population mean μ, would you have any way of knowing for certain if your interval actually
> contained the value of μ? Explain.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-019-pool-003

**Chunk:** `openstax_principles_ds:3.5:chunk-017`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.5: Discrete and Continuous Probability Distributions
>
> Assume the heights of adults follow a normal distribution with mean of 68 inches and
> standard deviation of 3 inches. For what range of heights should the designer model the car seats to
> accommodate 95% of drivers?
>
> Solution
>
> According to the empirical rule, the area under the normal curve within two standard deviations of the
> mean is 95%. Thus, the designer should design the seats to accommodate heights that are two standard
> deviations away from the mean. The lower bound of heights would be
>  inches, and the upper
> bound of heights would be
>  inches. Thus, the car seats should be designed to accommodate driver
> heights between 62 and 74 inches.
>
> EXPLORING FURTHER
>
> Statistical Applets to Explore Statistical Concepts
>
> Applets are very useful tools to help visualize statistical concepts in action. Many applets can simulate
> statistical concepts such as probabilities for the normal distribution, use of the empirical rule, creating box
> plots, etc.
>
> Visit the Utah State University applet website (https://openstax.org/r/usu) and experiment with various
> statistical tools.
>
> Using Python with Probability Distributions
>
> Python provides a number of built-in functions for calculating probabilities associated with both discrete and
> continuous probability distributions such as binomial distribution and the normal distribution. These functions
> are part of a library called scipy.stats (https://openstax.org/r/scipy).
>
> Here are a few of these probability density functions available within Python:
>
> • binom()—calculate probabilities associated with the binomial distribution
>
> • poisson()—calculate probabilities associated with the Poisson distribution
>
> • expon()—calculate probabilities associated with the exponential distribution
>
> • norm()—calculate probabilities associated with the normal distribution
>
> To import these probability density functions within Python, use the import command. For example, to import
> the binom() function use the following command:
>
> from scipy.stats import binom
>
> Using Python with the Binomial Distribution
>
> The binom() function in Python allows calculations of binomial probabilities. The probability mass function for

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-019-pool-004

**Chunk:** `openstax_intro_stats_2e:8.6:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.6: Confidence Interval (Women's Heights)
>
> With these values, construct a 90% confidence interval for your sample of ten values. Write
> the confidence interval you obtained in the first space of Table 8.9. 3. Now write your confidence interval on the board. As others in the class write their confidence intervals on the board,
> copy them into Table 8.9.
>
> __________
> __________
> __________
> __________
> __________
>
> __________
> __________
> __________
> __________
> __________
>
> __________
> __________
> __________
> __________
> __________
>
> __________
> __________
> __________
> __________
> __________
>
> __________
> __________
> __________
> __________
> __________
>
> __________
> __________
> __________
> __________
> __________
>
> __________
> __________
> __________
> __________
> __________
>
> __________
> __________
> __________
> __________
> __________
>
> Table 8.9 90% Confidence Intervals
>
> Discussion Questions
>
> 1. The actual population mean for the 100 heights given Table 8.8 is μ = 63.4. Using the class listing of confidence
> intervals, count how many of them contain the population mean μ; i.e., for how many intervals does the value of μ
> lie between the endpoints of the confidence interval? 2. Divide this number by the total number of confidence intervals generated by the class to determine the percent of
>
> confidence intervals that contains the mean μ. Write this percent here: _____________. 3. Is the percent of confidence intervals that contain the population mean μ close to 90%? 4. Suppose we had generated 100 confidence intervals. What do you think would happen to the percent of confidence
> intervals that contained the population mean? 5. When we construct a 90% confidence interval, we say that we are 90% confident that the true population mean
> lies within the confidence interval. Using complete sentences, explain what we mean by this phrase. 6. Some students think that a 90% confidence interval contains 90% of the data.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-019-pool-005

**Chunk:** `openstax_intro_stats_2e:9.4:chunk-005`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.4: Rare Events, the Sample, Decision and Conclusion
>
> We can calculate this probability using the normal distribution for means.
>
> Figure 9.2
>
> p-value= P( > 17) which is approximately zero.
>
> A p-value of approximately zero tells us that it is highly unlikely that a loaf of bread rises no more than 15 cm, on
> average. That is, almost 0% of all loaves of bread would be at least as high as 17 cm. purely by CHANCE had the
> population mean height really been 15 cm. Because the outcome of 17 cm. is so unlikely (meaning it is happening
> NOT by chance alone), we conclude that the evidence is strongly against the null hypothesis (the mean height is at most
> 15 cm.). There is sufficient evidence that the true mean height for the population of the baker's loaves of bread is greater
> than 15 cm.
>
> TRY IT 9.9
>
> A normal distribution has a standard deviation of 1. We want to verify a claim that the mean is greater than 12. A
> sample of 36 is taken with a sample mean of 12.5.
>
> H0: μ ≤ 12
> Ha: μ > 12
> The p-value is 0.0013
> Draw a graph that shows the p-value.
>
> Decision and Conclusion
>
> A systematic way to make a decision of whether to reject or not reject the null hypothesis is to compare the p-value and
> a preset or preconceived α (also called a "significance level"). A preset α is the probability of a Type I error (rejecting
> the null hypothesis when the null hypothesis is true). It may or may not be given to you at the beginning of the problem.
>
> When you make a decision to reject or not reject H0, do as follows:
>
> • If α > p-value, reject H0. The results of the sample data are significant.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-019-pool-006

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> Use n = 217: Always round the answer UP to the next higher integer to ensure that the sample size is large enough.
>
> Therefore, 217 Foothill College students should be surveyed in order to be 95% confident that we are within two years of
> the true population mean age of Foothill College students.
>
> TRY IT 8.7
>
> The population standard deviation for the height of high school basketball players is three inches. If we want to be
> 95% confident that the sample mean height is within one inch of the true population mean height, how many
> randomly selected students must be surveyed?
>
> 8.2 A Single Population Mean using the Student t Distribution
>
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

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-019-pool-007

**Chunk:** `openstax_principles_ds:3.5:chunk-016`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.5: Discrete and Continuous Probability Distributions
>
> See Using Python with Probability
> Distributions for the specific Python program and results. The resulting probability is calculated as 0.143.
>
> Thus, there is a probability of about 14% that a random employee has a salary greater than $75,000.
>
> The empirical rule is a method for determining approximate areas under the normal curve for measurements
> that fall within one, two, and three standard deviations from the mean for the normal (bell-shaped)
> distribution. (See Figure 3.9).
>
> Figure 3.9 Normal Distribution Showing Mean and Increments of Standard Deviation
>
> If  is a continuous random variable and has a normal distribution with mean  and standard deviation , then
> the empirical rule states that:
>
> • About 68% of the -values lie between
>  and
>  units from the mean  (within one standard deviation
> of the mean).
>
> • About 95% of the -values lie between
>  and
>  units from the mean  (within two standard
> deviations of the mean).
> • About 99.7% of the -values lie between
>  and
>  units from the mean  (within three standard
> deviations of the mean). Notice that almost all the x-values lie within three standard deviations of the
> mean.
> • The -scores for
>  and
>  are
>  and
> , respectively.
> • The -scores for
>  and
>  are
>  and
> , respectively.
> • The -scores for
>  and
>  are
>  and
> , respectively.
>
> EXAMPLE 3.28
>
> Problem
>
> An automotive designer is interested in designing automotive seats to accommodate the heights for about
> 95% of customers. Assume the heights of adults follow a normal distribution with mean of 68 inches and
> standard deviation of 3 inches. For what range of heights should the designer model the car seats to
> accommodate 95% of drivers?
>
> Solution
>
> According to the empirical rule, the area under the normal curve within two standard deviations of the
> mean is 95%.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-019-pool-008

**Chunk:** `openstax_principles_ds:4.2:chunk-029`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> The area under the t-distribution curve to the left of a t-score of
>  (using degrees of
> freedom
> ) is approximately 0.025. Thus, the p-value for this hypothesis test is 0.025.
>
> The final step in the hypothesis testing procedure is to come to a final decision regarding the null
> hypothesis. This is accomplished by comparing the p-value with the level of significance. In this example,
> the p-value is 0.025 and the level of significance is 0.04: since the p-value  level of significance, then the
> decision is to “reject the null hypothesis.”
>
> Conclusion: The decision is to reject the null hypothesis; the claim corresponds to the alternative
> hypothesis. This scenario corresponds to Row 2 in Table 4.8, and thus “there is enough evidence to support
> the claim” that the average salary of women engineers is less than that of men engineers.
>
> This problem can also be solved using the Python function called ttest_ind_from_stats().
>
> There is also a Python function to perform a two-sample t-test given raw data for the two groups, and this
> Python function is ttest_ind().
>
> For the function ttest_ind_from_stats(), the syntax is as follows:
>
> PYTHON CODE
>
> stats.ttest_ind_from_stats(sample_mean1, sample_standard_deviation1,
> sample_size1, sample_mean2, sample_standard_deviation2, sample_size2)
>
> Here is the Python code that can be used to solve Example 4.19. Note that this function returns the two-
> tailed p-value. Since Example 4.19 involves a left-tailed test, the desired p-value is one-half of the two-tailed
> p-value.
>
> PYTHON CODE
>
> import scipy.stats as stats
> import numpy as np
>  
> #Example 4.19 - Two Sample t-test given sample means, sample standard deviations
>
> sample_mean1 = 72700
> sample_standard_deviation1 = 9800
> sample_size1 = 45
>
> sample_mean2 = 76900
> sample_standard_deviation2 = 10700
> sample_size2 = 50
>
> test_statistic, two_tailed_p_value = stats.ttest_ind_from_stats(sample_mean1,
> sample_standard_deviation1, sample_size1, sample_mean2,
> sample_standard_deviation2, sample_size2)
>
> left_tailed_p_value = two_tailed_p_value / 2
>
> print("test statistic = ", "%.3f" % test_statistic)
> print("p-value = ", "%.3f" % left_tailed_p_value)

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-019-pool-009

**Chunk:** `openstax_intro_stats_2e:9.4:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.4: Rare Events, the Sample, Decision and Conclusion
>
> Didi is the first person to reach into the basket and pull
> out a bubble. Her bubble contains a $100 bill. The probability of this happening is
>  = 0.005. Because this is so unlikely,
>
> Ali is hoping that what the two of them were told is wrong and there are more $100 bills in the basket. A "rare event" has
> occurred (Didi getting the $100 bill) so Ali doubts the assumption about only one $100 bill being in the basket.
>
> Using the Sample to Test the Null Hypothesis
>
> Use the sample data to calculate the actual probability of getting the test result, called the p-value. The p-value is the
> probability that, if the null hypothesis is true, the results from another randomly selected sample will be as
> extreme or more extreme as the results obtained from the given sample.
>
> A large p-value calculated from the data indicates that we should not reject the null hypothesis. The smaller the p-value,
> the more unlikely the outcome, and the stronger the evidence is against the null hypothesis. We would reject the null
> hypothesis if the evidence is strongly against it.
>
> Draw a graph that shows the p-value. The hypothesis test is easier to perform if you use a graph because you see
> the problem more clearly.
>
> EXAMPLE 9.9
>
> Suppose a baker claims that his bread height is more than 15 cm, on average. Several of his customers do not believe
> him. To persuade his customers that he is right, the baker decides to do a hypothesis test. He bakes 10 loaves of bread. The mean height of the sample loaves is 17 cm. The baker knows from baking hundreds of loaves of bread that the
> standard deviation for the height is 0.5 cm. and the distribution of heights is normal.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-019-pool-010

**Chunk:** `openstax_principles_ds:4.2:chunk-008`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> In hypothesis testing, the maximum allowed probability of making a Type I error is called the level of
> significance, denoted by the Greek letter alpha, . From a practical standpoint, the level of significance is the
> probability value used to determine when the sample data indicates significant evidence against the null
> hypothesis. This level of significance is typically set to a small value, which indicates that the researcher wants
> the probability of rejecting a true null hypothesis to be small. Typical values of the level of significance used in
> hypothesis testing are as follows:
> ,
> , or
> .
>
> Once the null and alternative hypotheses are written and a level of significance is selected, the next step is for
> the researcher to collect relevant sample data from the population under study. It’s important that a
> representative random sample is selected, as discussed in Handling Large Datasets. After the sample data is
> collected, two calculations are performed: test statistic and p-value.
>
> The test statistic is a numerical value used to assess the strength of evidence against a null hypothesis and is
> calculated from sample data that is used in hypothesis testing. As noted in Estimating Parameters with
> Confidence Intervals, a sample statistic is a numerical value calculated from a sample of observations drawn
> from a larger population such as a sample mean or sample proportion. The sample statistic is converted to a
> standardized test statistic such as a z-score or t-score based on the assumption that the null hypothesis is
>
> true.
>
> Once the test statistic has been determined, a probability, or p-value, is created. A p-value is the probability of
> obtaining a sample statistic with a value as extreme as (or more extreme than) the value determined by the
> sample data under the assumption that the null hypothesis is true.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-019-pool-011

**Chunk:** `openstax_principles_ds:4.1:chunk-020`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Bootstrapping Methods
>
> In the earlier discussion of confidence intervals, certain requirements needed to be met in order to use the
> estimation methods. For example, when calculating the confidence interval for a mean, this requirement was
> indicated:
>
> • The sample size is at least 30, or the underlying population is known to follow a normal distribution.
>
> When calculating the confidence interval for a proportion, this requirement was noted:
>
> • Verify that the normal approximation to the binomial distribution is appropriate by ensuring that both
> and
>  are at least 5.
>
> What should a researcher do when these requirements are not met? Fortunately, there is another option called
> “bootstrapping” that can be used to find confidence intervals when the underlying distribution is unknown or if
> one of the conditions is not met. This bootstrapping method involves repeatedly taking samples with
> replacement.
>
> Sampling with replacement means that when a sample is selected, the sample is replaced back in the dataset
> before selecting the next sample. For example, a casino dealer plans to take a sample of two cards from a
> standard 52-card deck. If the sampling is to be done with replacement, then after selecting the sample of the
> first card, this card is then returned to the deck before the second card is selected. This implies that the same
> data value can appear multiple times in a given sample since once a data value is selected for the sample, it is
>
> replaced back in the dataset and is eligible to be selected again for the sample.
>
> For example, a researcher who has collected 100 samples to use for inference may want to estimate a
> confidence interval for the population mean. The researcher can then resample, with replacement, from this
> limited set of 100 observations.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-019-pool-012

**Chunk:** `openstax_principles_ds:4.2:chunk-017`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> df is the degrees of freedom.
>
> Here is the Python code to calculate the p-value for this example:
>
> PYTHON CODE
>
> # from scipy.stats import t
> from scipy.stats import t
>
> # define parameters test_statistic and degrees of freedom df
> x = -1.552
> df = 49
>
> # use t.cdf function to calculate area under t-distribution curve - note this is
> the area to the left of the x-value
> # subtract this result from 1 to obtain area to the right of the x-value
> # use round function to round answer to 4 decimal places
> round (t.cdf(x, df=49), 4)
>
> The resulting output will look like this:
>
> 0.0635
>
> The final step in the hypothesis testing procedure is to come to a final decision regarding the null
> hypothesis. This is accomplished by comparing the p-value with the level of significance. In this example,
> the p-value is 0.127 and the level of significance is 0.10: since the p-value  level of significance, then the
> decision is to “fail to reject the null hypothesis.”
>
> Conclusion: The decision is to fail to reject the null hypothesis; the claim corresponds to the null hypothesis. This scenario corresponds to Row 3 in Table 4.8, which means “there is not enough evidence to reject the
> claim” that the mean battery life of its latest smartphone model is 25 hours.
>
> Testing Claims for the Proportion
>
> In this section, we discuss one sample hypothesis testing for proportions. Recall that a sample proportion is
> measuring “how many out of the total.” For example, a medical researcher might be interested in testing a
> claim that the proportion of patients experiencing side effects from a new blood pressure–lowering medication
> is less than 4%.
>
> Here are the requirements to use this procedure:
>
> a. A random sample is selected from the population.
> b.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-019-pool-013

**Chunk:** `openstax_intro_stats_2e:6.1:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 6: The Normal Distribution
> Section 6.1: The Standard Normal Distribution
>
> f(x) =
>
> The cumulative distribution function is P(X < x). It is calculated either by a calculator or a computer, or it is looked up in a
> table. Technology has made the tables virtually obsolete. For that reason, as well as the fact that there are various table
> formats, we are not including table instructions.
>
> The curve is symmetric about a vertical line drawn through the mean, μ. In theory, the mean is the same as the median,
> because the graph is symmetric about μ. As the notation indicates, the normal distribution depends only on the mean
> and the standard deviation. Since the area under the curve must equal one, a change in the standard deviation, σ,
> causes a change in the shape of the curve; the curve becomes fatter or skinnier depending on σ. A change in μ causes
> the graph to shift to the left or right. This means there are an infinite number of normal probability distributions. One of
> special interest is called the standard normal distribution.
>
> COLLABORATIVE EXERCISE
>
> Your instructor will record the heights of both men and women in your class, separately. Draw histograms of your
> data. Then draw a smooth curve through each histogram. Is each curve somewhat bell-shaped? Do you think that if
> you had recorded 200 data values for men and 200 for women that the curves would look bell-shaped? Calculate the
>
> mean for each data set. Write the means on the x-axis of the appropriate graph below the peak. Shade the
> approximate area that represents the probability that one randomly chosen male is taller than 72 inches. Shade the
> approximate area that represents the probability that one randomly chosen female is shorter than 60 inches.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-019-pool-014

**Chunk:** `openstax_principles_ds:4.2:chunk-025`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> When translating claims about a
> population proportions, use the symbols p1 and p2 as part of the null and alternative hypotheses to represent
> the two unknown population proportions. Refer to Table 4.9 and Table 4.10 for the various setups to construct
>
> the null and alternative hypotheses for two-sample hypothesis testing.
>
> Setup A
> Setup B
> Setup C
>
> Table 4.9 Three Possible Setups for the Null and Alternative Hypotheses
> for a Population Mean (Two Samples)
>
> Setup D
> Setup E
> Setup F
>
> Table 4.10 Three Possible Setups for the Null and Alternative
> Hypotheses for a Population Proportion (Two Samples)
>
> Comparing Two Means
>
> In this section, we discuss two-sample hypothesis testing for the mean when the population standard
> deviations are unknown. Typically, in real-world applications, population standard deviations are unknown, so
> this method has considerable practical appeal.
>
> One other consideration when conducting hypothesis testing for two samples is to determine if the two
> samples are dependent or independent. Two samples are considered to be independent samples when the
> sample values from one population are not related to the sample values taken from the second population. In
> other words, there is not an inherent paired or matched relationship between the two samples. Two samples
> are considered to be dependent samples if the samples from one population can be paired or matched to the
> samples taken from the second population. Dependent samples are sometimes also called paired samples.
>
> For example, if a researcher were to collect data for the ages for a random sample of 15 men and a random
> sample of 15 women, there would be no inherent relationship between these two samples, and so these
> samples are considered independent samples.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-019-pool-015

**Chunk:** `openstax_principles_ds:4.2:chunk-028`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> Women Engineers
> Men Engineers
>
> Sample Mean
>
> Sample Standard
> Deviation
>
> Sample Size
>
> Table 4.11 Sample Data for Women and Men Engineers
>
> Use this sample data to test the claim made by the software engineer. Use a level of significance of 0.05 for
> this analysis.
>
> Solution
>
> The first step in the hypothesis testing procedure is to write the null and alternative hypotheses based on
> the claim. Notice that the claim mentions “average salary of women engineers is less than that of men
> engineers, where “less than” will translate to a less than symbol. A less than symbol must be used in the
> alternative hypothesis. The complement of a “less than” symbol is a “greater than or equals” symbol, which
> will be used in the null hypothesis. Let
>  represent the population mean salary for women engineers and
> let
>  represent the population mean salary for men engineers. The null hypothesis can be considered to
> represent that we expect there to be “no difference” between the salaries of women and men engineers. Note that this setup will correspond to Setup C from Table 4.9. The claim corresponds to the alternative
> hypothesis. Thus, the setup of the null and alternative hypotheses will be as follows:
>
> Since the population standard deviations are unknown in this example, the t-distribution will be used to
> conduct the hypothesis test.
>
> Next, calculate the standardized test statistic as follows:
>
> Notice that since the alternative hypothesis contains a “less than” symbol, the hypothesis test is called a
> “left tailed” test and the p-value will be calculated as the area under the t-distribution curve to the left of the
> test statistic. The area under the t-distribution curve to the left of a t-score of
>  (using degrees of
> freedom
> ) is approximately 0.025. Thus, the p-value for this hypothesis test is 0.025.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-019-pool-016

**Chunk:** `openstax_principles_ds:4.4:chunk-007`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.4: Analysis of Variance (ANOVA)
>
> The following Python program generates the corresponding F test statistic and p-value for this ANOVA
> analysis:
>
> PYTHON CODE
>
> # import libraries
> import numpy as np
> from scipy.stats  import f_oneway
>  
> # enter airline arrival data
>
> AirlineA = np.array([8, 12, 7, 9, 11, 4])
> AirlineB = np.array([13, 0, 2, 7, 6, 5])
> AirlineC = np.array([11, 15, 9, 11, 12])
>
> #f_oneway function returns both the test statistic and p-value
> f_oneway(AirlineA, AirlineB, AirlineC)
>
> The resulting output will look like this:
>
> F_onewayResult(statistic=4.388264306955828, pvalue=0.03314999857295516)
>
> From this Python output, the test statistic is
>  and the p-value is 0.033.
>
> The final step in the hypothesis testing procedure is to come to a final decision regarding the null
> hypothesis. This is accomplished by comparing the p-value with the level of significance. In this example,
> the p-value is 0.033 and the level of significance is 0.05: since the p-value  level of significance, the
> decision is to “reject the null hypothesis.”
>
> Conclusion: The decision is to reject the null hypothesis. The claim corresponds to the null hypothesis. This
> scenario corresponds to the first row in Table 4.18 and thus the conclusion is: There is enough evidence to
> reject the claim that the average arrival delays are the same for three airlines. This implies that at least one
> of the means is different from the others.
>
> Note: The ANOVA test method does not specify which mean is different from the others. Further statistical
> analysis is needed to make this determination.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-019-pool-017

**Chunk:** `openstax_intro_stats_2e:7.3:chunk-010`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 7: The Central Limit Theorem
> Section 7.3: Using the Central Limit Theorem
>
> Interpret the results.
>
> Solution
> a. P( < 35) = normalcdf(-E99,35,30.9,1.8) = 0.9886
> b. P( > 50) = normalcdf(50, E99,30.9,1.8) ≈ 0. For this sample group, it is almost impossible for the group’s average
>
> age to be more than 50. However, it is still possible for an individual in this group to have an age greater than 50.
> c. P(Σx ≥ 1,600) = normalcdf(1600,E99,1514.10,63) = 0.0864
> d. P(Σx ≤ 1,595) = normalcdf(-E99,1595,1514.10,63) = 0.9005. This means that there is a 90% chance that the sum of
>
> the ages for the sample group n = 49 is at most 1595.
> e. The 95th percentile = invNorm(0.95,30.9,1.1) = 32.7. This indicates that 95% of the attendees in the sample of 65 are
>
> younger than 32.7 years, on average.
> f. The 90th percentile = invNorm(0.90,2008.5,72.56) = 2101.5. This indicates that 90% of the attendees in the sample of
>
> 65 have a sum of ages less than 2,101.5 years.
>
> TRY IT 7.11
>
> According to Boeing data, the 757 airliner carries 200 passengers and has doors with a height of 72 inches. Assume
> for a certain population of men we have a mean height of 69.0 inches and a standard deviation of 2.8 inches.
>
> a. What doorway height would allow 95% of men to enter the aircraft without bending?
> b. Assume that half of the 200 passengers are men. What mean doorway height satisfies the condition that there is
>
> a 0.95 probability that this height is greater than the mean height of 100 men?
> c. For engineers designing the 757, which result is more relevant: the height from part a or part b? Why?
>
> HISTORICAL NOTE
>
> Normal Approximation to the Binomial
>
> Historically, being able to compute binomial probabilities was one of the most important applications of the central
> limit theorem.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-020

**Pregunta:** Why does increasing the confidence level make the confidence interval narrower when all other inputs are fixed?

**Respondibilidad de referencia:** unanswerable

### q-v1-020-pool-001

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-010`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> = 68
>
> EBM =
>
> σ = 3; n = 36; The confidence level is 95% (CL = 0.95).
>
> CL = 0.95 so α = 1 – CL = 1 – 0.95 = 0.05
>
> The area to the right of z0.025 is 0.025 and the area to the left of z0.025 is 1 – 0.025 = 0.975.
>
> when using invnorm(0.975,0,1) on the TI-83, 83+, or 84+ calculators. (This can also be found using appropriate
> commands on other calculators, using a computer, or using a probability table for the standard normal distribution.)
>
> EBM = (1.96)
>  = 0.98
>
> – EBM = 68 – 0.98 = 67.02
>
> + EBM = 68 + 0.98 = 68.98
>
> Notice that the EBM is larger for a 95% confidence level in the original problem.
>
> We estimate with 95% confidence that the true population mean for all statistics exam scores is between 67.02 and
> 68.98.
>
> Explanation of 95% Confidence Level: Ninety-five percent of all confidence intervals constructed in this way contain the
> true value of the population mean statistics exam score.
>
> Comparing the results: The 90% confidence interval is (67.18, 68.82). The 95% confidence interval is (67.02, 68.98). The
> 95% confidence interval is wider. If you look at the graphs, because the area 0.95 is larger than the area 0.90, it makes
> sense that the 95% confidence interval is wider. To be more confident that the confidence interval actually does contain
> the true value of the population mean for all statistics exam scores, the confidence interval necessarily needs to be
> wider.
>
> Figure 8.5
>
> Summary: Effect of Changing the Confidence Level
>
> • Increasing the confidence level increases the error bound, making the confidence interval wider.
> • Decreasing the confidence level decreases the error bound, making the confidence interval narrower.
>
> TRY IT 8.4
>
> Refer back to the pizza-delivery Try It exercise.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-020-pool-002

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-011`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> Figure 8.5
>
> Summary: Effect of Changing the Confidence Level
>
> • Increasing the confidence level increases the error bound, making the confidence interval wider.
> • Decreasing the confidence level decreases the error bound, making the confidence interval narrower.
>
> TRY IT 8.4
>
> Refer back to the pizza-delivery Try It exercise. The population standard deviation is six minutes and the sample mean
> deliver time is 36 minutes. Use a sample size of 20. Find a 95% confidence interval estimate for the true mean pizza
> delivery time.
>
> EXAMPLE 8.5
>
> Suppose we change the original problem in Example 8.2 to see what happens to the error bound if the sample size is
> changed.
>
> Problem
> Leave everything the same except the sample size. Use the original 90% confidence level. What happens to the error
> bound and the confidence interval if we increase the sample size and use n = 100 instead of n = 36? What happens if we
>
> decrease the sample size to n = 25 instead of n = 36?
>
> •
>  = 68
>
> • EBM =
>
> • σ = 3; The confidence level is 90% (CL=0.90);
>  = z0.05 = 1.645.
>
> Solution
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
>
> TRY IT 8.5
>
> Refer back to the pizza-delivery Try It exercise.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-020-pool-003

**Chunk:** `openstax_principles_ds:4.1:chunk-010`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> The margin of error is calculated as follows:
>
> The 90% confidence interval is calculated as follows:
>
> Concluding statement:
>
> The college professor can forecast with 90% confident that the mean amount of time spent on homework
> assignments in a future semester is the interval from 11.03 to 13.97 hours per week.
>
> Calculation for 95% Confidence Interval
>
> For a 95% confidence interval, the corresponding critical value is
> .
>
> The margin of error is calculated as follows:
>
> The 95% confidence interval is calculated as follows:
>
> Concluding statement:
>
> The college professor can forecast with 95% confident that the mean amount of time spent on homework
> assignments in a future semester is the interval from 10.75 to 14.25 hours per week.
>
> Comparison of 90% and 95% confidence intervals:
>
> The 90% confidence interval extends from 11.03 to 13.97. The 95% confidence interval extends from 10.75 to 14.25.
>
> Notice that the 95% confidence interval is wider. If the confidence level is increased, with all other
>
> parameters held constant, we should expect that the confidence interval will become wider. Another way to
> consider this: the wider the confidence interval, the more likely the interval is to contain the true population
> mean. This makes intuitive sense in that if you want to be more certain that the true value of the parameter
> is within an interval, then the interval needs to be wider to account for a larger range of potential values. As
> an analogy, consider a person trying to catch a fish. The wider the net used, the higher the probability of
> catching a fish.
>
> You might notice that the sample size  is located in the denominator of the formula for margin of error. This indicates that as the sample size increases, the margin of error will decrease, which will then result in a
> narrower confidence interval.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-020-pool-004

**Chunk:** `openstax_intro_stats_2e:8.6:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.6: Confidence Interval (Women's Heights)
>
> 5. When we construct a 90% confidence interval, we say that we are 90% confident that the true population mean
> lies within the confidence interval. Using complete sentences, explain what we mean by this phrase. 6. Some students think that a 90% confidence interval contains 90% of the data. Use the list of data given (the heights
> of women) and count how many of the data values lie within the confidence interval that you generated based on
> that data. How many of the 100 data values lie within your confidence interval? What percent is this? Is this percent
> close to 90%? 7. Explain why it does not make sense to count data values that lie in a confidence interval. Think about the random
> variable that is being used in the problem. 8. Suppose you obtained the heights of ten women and calculated a confidence interval from this information. Without knowing the population mean μ, would you have any way of knowing for certain if your interval actually
> contained the value of μ? Explain.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-020-pool-005

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-012`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> When n = 25: EBM =
>  = (1.645)
>  = 0.987.
>
> Summary: Effect of Changing the Sample Size
>
> • Increasing the sample size causes the error bound to decrease, making the confidence interval narrower.
> • Decreasing the sample size causes the error bound to increase, making the confidence interval wider.
>
> TRY IT 8.5
>
> Refer back to the pizza-delivery Try It exercise. The mean delivery time is 36 minutes and the population standard
> deviation is six minutes. Assume the sample size is changed to 50 restaurants with the same sample mean. Find a
> 90% confidence interval estimate for the population mean delivery time.
>
> Working Backwards to Find the Error Bound or Sample Mean
>
> When we calculate a confidence interval, we find the sample mean, calculate the error bound, and use them to calculate
> the confidence interval. However, sometimes when we read statistical studies, the study may state the confidence
> interval only. If we know the confidence interval, we can work backwards to find both the error bound and the sample
> mean.
>
> Finding the Error Bound
>
> • From the upper value for the interval, subtract the sample mean,
> • OR, from the upper value for the interval, subtract the lower value. Then divide the difference by two.
>
> Finding the Sample Mean
>
> • Subtract the error bound from the upper value of the confidence interval,
> • OR, average the upper and lower endpoints of the confidence interval.
>
> Notice that there are two methods to perform each calculation. You can choose the method that is easier to use with the
> information you know.
>
> EXAMPLE 8.6
>
> Suppose we know that a confidence interval is (67.18, 68.82) and we want to find the error bound.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-020-pool-006

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> The margin of error (EBM) depends on the confidence level (abbreviated CL). The confidence level is often considered
> the probability that the calculated confidence interval estimate will contain the true population parameter. However, it is
> more accurate to state that the confidence level is the percent of confidence intervals that contain the true population
> parameter when repeated samples are taken. Most often, it is the choice of the person constructing the confidence
> interval to choose a confidence level of 90% or higher because that person wants to be reasonably certain of their
> conclusions.
>
> There is another probability called alpha (α). α is related to the confidence level, CL. α is the probability that the interval
> does not contain the unknown population parameter. Mathematically, α + CL = 1.
>
> EXAMPLE 8.1
>
> Suppose we have collected data from a sample. We know the sample mean but we do not know the mean for the entire
> population. The sample mean is seven, and the error bound for the mean is 2.5.
>
> = 7 and EBM = 2.5
>
> The confidence interval is (7 – 2.5, 7 + 2.5), and calculating the values gives (4.5, 9.5).
>
> If the confidence level (CL) is 95%, then we say that, "We estimate with 95% confidence that the true value of the
> population mean is between 4.5 and 9.5."
>
> TRY IT 8.1
>
> Suppose we have data from a sample. The sample mean is 15, and the error bound for the mean is 3.2.
>
> What is the confidence interval estimate for the population mean?
>
> A confidence interval for a population mean with a known standard deviation is based on the fact that the sample means
> follow an approximately normal distribution.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-020-pool-007

**Chunk:** `openstax_intro_stats_2e:8.intro:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.intro: Introduction
>
> We use sample data to make generalizations about an unknown population. This part of statistics is called inferential
> statistics. The sample data help us to make an estimate of a population parameter. We realize that the point
> estimate is most likely not the exact value of the population parameter, but close to it. After calculating point estimates,
> we construct interval estimates, called confidence intervals.
>
> In this chapter, you will learn to construct and interpret confidence intervals. You will also learn a new distribution, the
> Student's-t, and how it is used with these intervals. Throughout the chapter, it is important to keep in mind that the
>
> confidence interval is a random variable. It is the population parameter that is fixed.
>
> If you worked in the marketing department of an entertainment company, you might be interested in the mean number
> of songs a consumer downloads a month from Apple Music. If so, you could conduct a survey and calculate the sample
> mean, , and the sample standard deviation, s. You would use  to estimate the population mean and s to estimate the
> population standard deviation. The sample mean, , is the point estimate for the population mean, μ. The sample
> standard deviation, s, is the point estimate for the population standard deviation, σ.
>
> Each of  and s is called a statistic.
>
> A confidence interval is another type of estimate but, instead of being just one number, it is an interval of numbers. It
> provides a range of reasonable values in which we expect the population parameter to fall. There is no guarantee that a
> given confidence interval does capture the parameter, but there is a predictable probability of success.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-020-pool-008

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-009`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> 79
> 145
> 147
> 160
> 116
> 100
> 159
> 151
> 156
> 126
>
> 137
> 83
> 156
> 94
> 121
> 144
> 123
> 114
> 139
> 99
>
> Table 8.3
>
> Use this sample data to construct a 90% confidence interval for the mean number of targeted industrial chemicals to be
> found in an in infant’s blood.
>
> Solution
> From the sample, you can calculate  = 127.45 and s = 25.965. There are 20 infants in the sample, so n = 20, and df = 20 –
> 1 = 19.
>
> You are asked to calculate a 90% confidence interval: CL = 0.90, so α = 1 – CL = 1 – 0.90 = 0.10
>
> By definition, the area to the right of t0.05 is 0.05 and so the area to the left of t0.05 is 1 – 0.05 = 0.95.
>
> Use a table, calculator, or computer to find that t0.05 = 1.729.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-020-pool-009

**Chunk:** `openstax_intro_stats_2e:8.4:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.4: Confidence Interval (Home Costs)
>
> c. n = _____
>
> 2. In words, define the random variable
> . 3. State the estimated distribution to use. Use both words and symbols.
>
> Find the Confidence Interval
>
> 1. Calculate the confidence interval and the error bound.
> a. Confidence Interval: _____
> b. Error Bound: _____
>
> 2. How much area is in both tails (combined)? α = _____
> 3. How much area is in each tail?
>  = _____
>
> 4. Fill in the blanks on the graph with the area in each section. Then, fill in the number line with the upper and lower
> limits of the confidence interval and the sample mean.
>
> Figure 8.6
>
> 5. Some students think that a 90% confidence interval contains 90% of the data. Use the list of data on the first page
> and count how many of the data values lie within the confidence interval. What percent is this? Is this percent close
> to 90%? Explain why this percent should or should not be close to 90%.
>
> Describe the Confidence Interval
>
> 1. In two to three complete sentences, explain what a confidence interval means (in general), as if you were talking to
> someone who has not taken statistics. 2. In one to two complete sentences, explain what this confidence interval means for this particular study.
>
> Use the Data to Construct Confidence Intervals
>
> 1. Using the given information, construct a confidence interval for each confidence level given.
>
> Confidence level
> EBM/Error Bound
> Confidence Interval
>
> 50%
>
> 80%
>
> 95%
>
> 99%
>
> Table 8.6
>
> 2. What happens to the EBM as the confidence level increases? Does the width of the confidence interval increase or
> decrease? Explain why this happens.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-020-pool-010

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-005`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> Random sampling is assumed, but that is a completely separate assumption from normality.
>
> Calculators and computers can easily calculate any Student's t-probabilities. The TI-83,83+, and 84+ have a tcdf function
> to find the probability for given values of t. The grammar for the tcdf command is tcdf(lower bound, upper bound,
> degrees of freedom). However for confidence intervals, we need to use inverse probability to find the value of t when we
> know the probability.
>
> For the TI-84+ you can use the invT command on the DISTRibution menu. The invT command works similarly to the
> invnorm. The invT command requires two inputs: invT(area to the left, degrees of freedom) The output is the t-score
> that corresponds to the area we specified.
>
> The TI-83 and 83+ do not have the invT command. (The TI-89 has an inverse T command.)
>
> A probability table for the Student's t-distribution can also be used. The table gives t-scores that correspond to the
> confidence level (column) and degrees of freedom (row). (The TI-86 does not have an invT program or command, so if
> you are using that calculator, you need to use a probability table for the Student's t-Distribution.) When using a t-table,
> note that some tables are formatted to show the confidence level in the column headings, while the column headings in
> some tables may show only corresponding area in one or both tails.
>
> A Student's t table (See Appendix H Tables) gives t-scores given the degrees of freedom and the right-tailed probability. The table is very limited. Calculators and computers can easily calculate any Student's t-probabilities.
>
> The notation for the Student's t-distribution (using T as the random variable) is:

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-020-pool-011

**Chunk:** `openstax_intro_stats_2e:8.1:chunk-005`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.1: A Single Population Mean using the Normal Distribution
>
> CL = 1 – α, so α is the area that is
> split equally between the two tails. Each of the tails contains an area equal to
> .
>
> The z-score that has an area to the right of
>  is denoted by
> .
>
> For example, when CL = 0.95, α = 0.05 and
>  = 0.025; we write
>  = z0.025.
>
> The area to the right of z0.025 is 0.025 and the area to the left of z0.025 is 1 – 0.025 = 0.975.
>
> , using a calculator, computer or a standard normal probability table.
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> invNorm(0.975, 0, 1) = 1.96
>
> NOTE
>
> Remember to use the area to the LEFT of
> ; in this chapter the last two inputs in the invNorm command are 0, 1,
>
> because you are using a standard normal distribution Z ~ N(0, 1).
>
> Writing the Interpretation
> The interpretation should clearly state the confidence level (CL), explain what population parameter is being estimated
> (here, a population mean), and state the confidence interval (both endpoints). "We estimate with ___% confidence that
> the true population mean (include the context of the problem) is between ___ and ___ (include appropriate units)."
>
> EXAMPLE 8.2
>
> Suppose scores on exams in statistics are normally distributed with an unknown population mean and a population
> standard deviation of three points. A random sample of 36 scores is taken and gives a sample mean (sample mean score)
> of 68. Find a confidence interval estimate for the population mean exam score (the mean score on all exams).
>
> Problem
> Find a 90% confidence interval for the true (population) mean of statistics exam scores.
>
> Solution
> • You can use technology to calculate the confidence interval directly.
> • The first solution is shown step-by-step.
> • The second solution uses the TI-83, 83+, and 84+ calculators.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-020-pool-012

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-008`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> NOTE
>
> When calculating the error bound, a probability table for the Student's t-distribution can also be used to find the value
> of t. The table gives t-scores that correspond to the confidence level (column) and degrees of freedom (row); the
> t-score is found where the row and column intersect in the table.
>
> TRY IT 8.8
>
> You do a study of hypnotherapy to determine how effective it is in increasing the number of hours of sleep subjects
> get each night. You measure hours of sleep for 12 subjects with the following results. Construct a 95% confidence
> interval for the mean number of hours slept for the population (assumed normal) from which you took the data.
>
> 8.2; 9.1; 7.7; 8.6; 6.9; 11.2; 10.1; 9.9; 8.9; 9.2; 7.5; 10.5
>
> EXAMPLE 8.9
>
> Problem
> The Human Toxome Project (HTP) is working to understand the scope of industrial pollution in the human body. Industrial chemicals may enter the body through pollution or as ingredients in consumer products. The scientists at HTP
> tested cord blood samples for 20 newborn infants in the United States. The cord blood of the "In utero/newborn" group
> was tested for 430 industrial compounds, pollutants, and other chemicals, including chemicals linked to brain and
> nervous system toxicity, immune system toxicity, and reproductive toxicity, and fertility problems. There are health
> concerns about the effects of some chemicals on the brain and nervous system. Table 8.3 shows how many of the
> targeted chemicals were found in each infant’s cord blood.
>
> 79
> 145
> 147
> 160
> 116
> 100
> 159
> 151
> 156
> 126
>
> 137
> 83
> 156
> 94
> 121
> 144
> 123
> 114
> 139
> 99
>
> Table 8.3
>
> Use this sample data to construct a 90% confidence interval for the mean number of targeted industrial chemicals to be
> found in an in infant’s blood.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-020-pool-013

**Chunk:** `openstax_principles_ds:4.1:chunk-011`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> The wider the net used, the higher the probability of
> catching a fish.
>
> You might notice that the sample size  is located in the denominator of the formula for margin of error. This indicates that as the sample size increases, the margin of error will decrease, which will then result in a
> narrower confidence interval. On the other hand, as the sample size decreases, the margin of error
> increases and the confidence interval becomes wider.
>
> Confidence Interval for the Mean When the Population Standard Deviation Is
> Unknown
>
> A confidence interval can still be determined when the population standard deviation is unknown by
> calculating a sample standard deviation based on the sample data. This is actually the more common
> application of confidence intervals.
>
> Here are the conditions required to use this procedure:
>
> a. A random sample is selected from the population.
> b. The sample size is at least 30, or the underlying population is known to follow a normal distribution.
>
> c. The population standard deviation ( ) is unknown; the sample standard deviation
>  can be calculated.
>
> Once these requirements are met, the margin of error (E) is calculated according to the following formula:
>
> is called the critical value of the t-distribution. The t-distribution is a bell-shaped, symmetric distribution
> similar to the normal distribution, though the t-distribution has “thicker tails” as compared to the normal
> distribution. The comparison of the normal and t-distribution curves is shown in Figure 4.3.
>
> Figure 4.3 Comparison of t-Distribution and Normal Distribution Curves
>
> The t-distribution is actually a family of curves, determined by a parameter called degrees of freedom (df),
> where df is equal to
> . The critical value
>  is similar to a z-score and specifies the area under the t-
> distribution curve corresponding to the confidence level between
>  and
> .

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-020-pool-014

**Chunk:** `openstax_principles_ds:4.1:chunk-020`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Bootstrapping Methods
>
> In the earlier discussion of confidence intervals, certain requirements needed to be met in order to use the
> estimation methods. For example, when calculating the confidence interval for a mean, this requirement was
> indicated:
>
> • The sample size is at least 30, or the underlying population is known to follow a normal distribution.
>
> When calculating the confidence interval for a proportion, this requirement was noted:
>
> • Verify that the normal approximation to the binomial distribution is appropriate by ensuring that both
> and
>  are at least 5.
>
> What should a researcher do when these requirements are not met? Fortunately, there is another option called
> “bootstrapping” that can be used to find confidence intervals when the underlying distribution is unknown or if
> one of the conditions is not met. This bootstrapping method involves repeatedly taking samples with
> replacement.
>
> Sampling with replacement means that when a sample is selected, the sample is replaced back in the dataset
> before selecting the next sample. For example, a casino dealer plans to take a sample of two cards from a
> standard 52-card deck. If the sampling is to be done with replacement, then after selecting the sample of the
> first card, this card is then returned to the deck before the second card is selected. This implies that the same
> data value can appear multiple times in a given sample since once a data value is selected for the sample, it is
>
> replaced back in the dataset and is eligible to be selected again for the sample.
>
> For example, a researcher who has collected 100 samples to use for inference may want to estimate a
> confidence interval for the population mean. The researcher can then resample, with replacement, from this
> limited set of 100 observations.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-020-pool-015

**Chunk:** `openstax_intro_stats_2e:8.3:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.3: A Population Proportion
>
> – EBM = 127.45 – 10.038 = 117.412
>
> + EBM = 127.45 + 10.038 = 137.488
>
> We estimate with 90% confidence that the mean number of all targeted industrial chemicals found in cord blood in the
> United States is between 117.412 and 137.488.
>
> Solution
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> Enter the data as a list. Press STAT and arrow over to TESTS.
>
> Arrow down to 8:TInterval and press ENTER (or you can just press 8). Arrow to Data and press ENTER.
>
> Arrow down to List and enter the list name where you put the data.
>
> Arrow down to Freq and enter 1.
>
> Arrow down to C-level and enter 0.90
>
> Arrow down to Calculate and press ENTER.
>
> The 90% confidence interval is (117.41, 137.49).
>
> TRY IT 8.9
>
> A random sample of statistics students were asked to estimate the total number of hours they spend watching
> television in an average week. The responses are recorded in Table 8.4. Use this sample data to construct a 98%
> confidence interval for the mean number of hours statistics students will spend watching television in one week.
>
> 0
> 3
> 1
> 20
> 9
>
> 5
> 10
> 1
> 10
> 4
>
> 14
> 2
> 4
> 4
> 5
>
> Table 8.4
>
> 8.3 A Population Proportion
>
> During an election year, we see articles in the newspaper that state confidence intervals in terms of proportions or
> percentages. For example, a poll for a particular candidate running for president might show that the candidate has 40%
> of the vote within three percentage points (if the sample is large enough). Often, election polls are calculated with 95%
> confidence, so, the pollsters would be 95% confident that the true proportion of voters who favored the candidate would
> be between 0.37 and 0.43: (0.40 – 0.03,0.40 + 0.03).

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-020-pool-016

**Chunk:** `openstax_principles_ds:4.1:chunk-025`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> #print the confidence interval
> print(conf_interval.confidence_interval)
>
> The resulting output will look like this:
>
> ConfidenceInterval(low=22.45, high=26.7)
>
> Using 50,000 bootstrapped samples, a 95% confidence interval is generated as (22.45, 26.7).
>
> EXPLORING FURTHER
>
> Simulating Confidence Intervals
>
> A number of websites and resources, such as the online textbook Online Statistics Education: A Multimedia
> Course of Study (https://openstax.org/r/estimation) (http://onlinestatbook.com/) (project leader: David M. Lane, Rice University), allow the user to simulate confidence intervals for means or proportions using
> simulated sample data. It is useful to observe how many intervals contain an assumed value for the
> population mean or population proportion. The Stapplet (https://openstax.org/r/stapplet) website provides
> a similar tool.
>
> Using Python to Calculate Confidence Intervals
>
> When calculating confidence intervals, data scientists typically make use of technology to help streamline and
> automate the analysis. Python provides built-in functions for confidence interval calculations, and several
> examples are shown in Table 4.5. Students are encouraged to try examples themselves and experiment to use
> Python to assist with these calculations.
>
> Table 4.5 provides a summary of various functions available within the SciPy library (https://openstax.org/
>
> r/spy) for confidence interval calculations:
>
> Usage
> Python Function Name
> Syntax
>
> norm.interval()
> norm.interval(conf_level,
> sample_mean,standard_dev/
> sqrt
>
> (n))
>
> Calculate confidence interval for
> the mean when population
> standard deviation is known,
> given sample mean, population
> standard deviation, and sample
> size (uses normal distribution).
>
> t.interval()
> t.interval(conf_level,
> degrees_freedom,
> sample_mean,standard_dev/
> sqrt
>
> (n))
>
> Calculate confidence interval for
> the mean when population
> standard deviation is unknown,
> given sample mean, sample
> standard deviation, and sample
> size (uses t-distribution).
>
> Calculate confidence interval for
> a proportion (uses normal
> distribution).
>
> proportion_confint()
> proportion_confint(success,
> sample_size,
> 1 – confidence_level)
>
> Table 4.5 Python Functions for Confidence Intervals
>
> EXAMPLE 4.9
>
> Problem
>
> Repeat Example 4.3 to calculate a 90% confidence interval, but use Python functions to calculate the
> confidence interval.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-021

**Pregunta:** How do one-way ANOVA and the Kruskal-Wallis test differ in their distributional assumptions and interpretation?

**Respondibilidad de referencia:** unanswerable

### q-v1-021-pool-001

**Chunk:** `openstax_principles_ds:4.4:chunk-002`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.4: Analysis of Variance (ANOVA)
>
> In this case, we should not assign any interpretation to the
> y-intercept.
>
> In the previous example, the range of data collected for the -variable was from $49,000 to $153,000 spent per
> month on advertising. Since this interval does not include an x-value of zero, we would not provide any
> interpretation for the intercept.
>
> 4.4 Analysis of Variance (ANOVA)
>
> Learning Outcomes
> By the end of this section, you should be able to:
>
> • 4.4.1 Set up and apply one-way analysis of variance hypothesis test.
> • 4.4.2 Use Python to conduct one-way analysis of variance.
>
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

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-021-pool-002

**Chunk:** `openstax_principles_ds:4.4:chunk-003`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.4: Analysis of Variance (ANOVA)
>
> To compare three or more means, the sample sizes for each group can be different sample sizes (samples
> sizes do not need to be identical). For one-way ANOVA hypothesis testing, we will follow the same general
>
> outline of steps for hypothesis testing that was discussed in Hypothesis Testing.
>
> The first step will be to write the null and alternative hypotheses. For one-way ANOVA, the null and alternative
> hypotheses are always stated as the following:
>
> : All population means are equal:
>
> : At least one population mean is different from the others.
>
> Here are the requirements to use this procedure:
>
> a. The samples are random and selected from approximately normal distributions.
> b. The samples are independent of one another.
>
> c. The population variances are approximately equal.
>
> In this discussion, we assume that the population variances are not equal.
>
> When these requirements are met, the F-distribution is used as the basis for conducting the hypothesis test.
>
> The F-distribution is a skewed distribution (skewed to the right), and the shape of the distribution depends on
> two different degrees of freedom, referred to as degrees of freedom for the numerator and degrees of
> freedom for the denominator.
>
> Figure 4.10 shows the typical shape of the F-distribution:
>
> Figure 4.10 Shape of the F-Distribution
>
> The test statistic for this hypothesis test will be the ratio of two variances, namely the ratio of the variance
> between samples to the ratio of the variances within the samples.
>
> The numerator of the test statistic (variance between samples) is sometimes referred to as variation due to
> treatment or explained variation.
>
> The denominator of the test statistic (variance within samples) is sometimes referred to as variation due to
> error, or unexplained variation.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-021-pool-003

**Chunk:** `openstax_principles_ds:4.4:chunk-005`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.4: Analysis of Variance (ANOVA)
>
> For degrees of freedom for the denominator, this is calculated as the total of the sample sizes minus the
> number of groups. 6. Calculate the quantity called “mean square between (MSB)” according to the following formula:
>
> 7. Calculate the quantity called “mean square within (MSW)” according to the following formula:
>
> 8. Calculate the test statistic (
> ), according to the following formula:
>
> Once the test statistic is obtained, the p-value is calculated as the area to the right of the test statistic under
> the
> -distribution curve (note that the ANOVA hypothesis test is always considered a “right-tail” test).
>
> Usually, the results of these computations are organized in an ANOVA summary table like Table 4.17.
>
> Degrees
>
> p-value
>
> Variation
> Sum of
> Squares
>
> Mean
> Squares
>
> Test Statistic
>
> of
> Freedom
>
> Between
> SSB
> MSB
> Area to the right of the F test statistic
>
> Within
> SSW
> MSW
> N/A
>
> Table 4.17 ANOVA Summary Table
>
> Using Python for One-Way ANOVA
>
> As mentioned earlier, due to the complexity of these calculations, technology is typically used to calculate the
> test statistic and p-value.
>
> Using Python, the f_oneway() function is provided as part of the scipy library, and this function provides
>
> both the test statistic and p-value for a one-way ANOVA hypothesis test.
>
> The syntax is to call the function with the data arrays as arguments, as in:
>
> f_oneway(Array1, Array2, Array3, …)
>
> The function returns both the F test statistic and the p-value for the one-way ANOVA hypothesis test.
>
> The details of this Python function are shown in Example 4.25.
>
> Here is a step-by-step example to illustrate this ANOVA hypothesis testing process.
>
> EXAMPLE 4.25
>
> Problem
>
> An airline manager claims that the average arrival delays for flights from Boston to Dallas are the same for
> three airlines: Airlines A, B, and C.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-021-pool-004

**Chunk:** `openstax_principles_ds:4.4:chunk-007`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.4: Analysis of Variance (ANOVA)
>
> The following Python program generates the corresponding F test statistic and p-value for this ANOVA
> analysis:
>
> PYTHON CODE
>
> # import libraries
> import numpy as np
> from scipy.stats  import f_oneway
>  
> # enter airline arrival data
>
> AirlineA = np.array([8, 12, 7, 9, 11, 4])
> AirlineB = np.array([13, 0, 2, 7, 6, 5])
> AirlineC = np.array([11, 15, 9, 11, 12])
>
> #f_oneway function returns both the test statistic and p-value
> f_oneway(AirlineA, AirlineB, AirlineC)
>
> The resulting output will look like this:
>
> F_onewayResult(statistic=4.388264306955828, pvalue=0.03314999857295516)
>
> From this Python output, the test statistic is
>  and the p-value is 0.033.
>
> The final step in the hypothesis testing procedure is to come to a final decision regarding the null
> hypothesis. This is accomplished by comparing the p-value with the level of significance. In this example,
> the p-value is 0.033 and the level of significance is 0.05: since the p-value  level of significance, the
> decision is to “reject the null hypothesis.”
>
> Conclusion: The decision is to reject the null hypothesis. The claim corresponds to the null hypothesis. This
> scenario corresponds to the first row in Table 4.18 and thus the conclusion is: There is enough evidence to
> reject the claim that the average arrival delays are the same for three airlines. This implies that at least one
> of the means is different from the others.
>
> Note: The ANOVA test method does not specify which mean is different from the others. Further statistical
> analysis is needed to make this determination.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-021-pool-005

**Chunk:** `openstax_principles_ds:4.4:chunk-001`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.4: Analysis of Variance (ANOVA)
>
> Interpret and Apply the Slope and y-Intercept
>
> The slope of the line, , describes how changes in the variables are related. It is important to interpret the
> slope of the line in the context of the situation represented by the data. You should be able to write a sentence
> interpreting the slope in plain English.
>
> Interpretation of the Slope
>
> The slope of the best-fit line tells us how the dependent variable ( ) changes for every one-unit increase in the
> independent ( ) variable, on average.
>
> In the previous example, the linear regression model for the monthly amount spent on advertising and the
> monthly revenue for a company for 12 months was generated as follows:
>
> Since the slope was determined to be 61.8, the company can interpret this to mean that for every $1,000 spent
> on advertising, on average, this will result in an increase in revenues of $61,800.
>
> The intercept of the regression equation is the corresponding y-value when
> .
>
> Interpretation of the Intercept
>
> The intercept of the best-fit line tells us the expected mean value of  in the case where the -variable is equal
> to zero.
>
> However, in many scenarios it may not make sense to have the -variable equal zero, and in these cases, the
> intercept does not have any meaning in the context of the problem. In other examples, the x-value of zero is
> outside the range of the -data that was collected. In this case, we should not assign any interpretation to the
> y-intercept.
>
> In the previous example, the range of data collected for the -variable was from $49,000 to $153,000 spent per
> month on advertising. Since this interval does not include an x-value of zero, we would not provide any
> interpretation for the intercept.
>
> 4.4 Analysis of Variance (ANOVA)

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-021-pool-006

**Chunk:** `openstax_intro_stats_2e:9.4:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.4: Rare Events, the Sample, Decision and Conclusion
>
> Assumptions
>
> When you perform a hypothesis test of a single population mean μ using a normal distribution (often called a z-test), you
> take a simple random sample from the population. The population you are testing is normally distributed, or your
> sample size is sufficiently large. You know the value of the population standard deviation, which, in reality, is rarely
> known.
>
> When you perform a hypothesis test of a single population mean μ using a Student's t-distribution (often called a
> t-test), there are fundamental assumptions that need to be met in order for the test to work properly. Your data should
> be a simple random sample that comes from a population that is approximately normally distributed. You use the
> sample standard deviation to approximate the population standard deviation. (Note that if the sample size is sufficiently
> large, a t-test will work even if the population is not approximately normally distributed).
>
> When you perform a hypothesis test of a single population proportion p, you take a simple random sample from the
> population. You must meet the conditions for a binomial distribution: there are a certain number n of independent
> trials, the outcomes of any trial are success or failure, and each trial has the same probability of a success p. The shape
> of the binomial distribution needs to be similar to the shape of the normal distribution. To ensure this, the quantities np
> and nq must both be greater than five (
>  and
> ). Then the binomial distribution of a sample (estimated)
>
> proportion can be approximated by the normal distribution with
>  and
> . Remember that
> .
>
> 9.4 Rare Events, the Sample, Decision and Conclusion
>
> Establishing the type of distribution, sample size, and known or unknown standard deviation can help you figure out
> how to go about a hypothesis test.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-021-pool-007

**Chunk:** `openstax_intro_stats_2e:9.5:chunk-015`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.5: Additional Information and Full Hypothesis Test Examples
>
> Arrow down to
>
> Prop and arrow to not equals p0. Press ENTER. Arrow down to Calculate and press ENTER. The calculator
>
> calculates the p-value (p = 0.5485) and the test statistic (z-score). Prop not equals .5 is the alternate hypothesis. Do
>
> this set of instructions again except arrow to Draw (instead of Calculate). Press ENTER. A shaded graph appears with
>
> z = 0.6 (test statistic) and p = 0.5485 (p-value). Make sure when you use Draw that no other equations are highlighted
>
> in Y = and the plots are turned off.
>
> The Type I and Type II errors are as follows:
>
> The Type I error is to conclude that the proportion of first-time brides who are younger than their grooms is different
> from 50% when, in fact, the proportion is actually 50%. (Reject the null hypothesis when the null hypothesis is true).
>
> The Type II error is there is not enough evidence to conclude that the proportion of first time brides who are younger
> than their grooms differs from 50% when, in fact, the proportion does differ from 50%. (Do not reject the null hypothesis
> when the null hypothesis is false.)
>
> TRY IT 9.17
>
> A teacher believes that 85% of students in the class will want to go on a field trip to the local zoo. The teacher
> performs a hypothesis test to determine if the percentage is the same or different from 85%. The teacher samples 50
> students and 39 reply that they would want to go to the zoo. For the hypothesis test, use a 1% level of significance.
>
> First, determine what type of test this is, set up the hypothesis test, find the p-value, sketch the graph, and state your
> conclusion.
>
> EXAMPLE 9.18

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-021-pool-008

**Chunk:** `openstax_intro_stats_2e:9.4:chunk-005`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.4: Rare Events, the Sample, Decision and Conclusion
>
> We can calculate this probability using the normal distribution for means.
>
> Figure 9.2
>
> p-value= P( > 17) which is approximately zero.
>
> A p-value of approximately zero tells us that it is highly unlikely that a loaf of bread rises no more than 15 cm, on
> average. That is, almost 0% of all loaves of bread would be at least as high as 17 cm. purely by CHANCE had the
> population mean height really been 15 cm. Because the outcome of 17 cm. is so unlikely (meaning it is happening
> NOT by chance alone), we conclude that the evidence is strongly against the null hypothesis (the mean height is at most
> 15 cm.). There is sufficient evidence that the true mean height for the population of the baker's loaves of bread is greater
> than 15 cm.
>
> TRY IT 9.9
>
> A normal distribution has a standard deviation of 1. We want to verify a claim that the mean is greater than 12. A
> sample of 36 is taken with a sample mean of 12.5.
>
> H0: μ ≤ 12
> Ha: μ > 12
> The p-value is 0.0013
> Draw a graph that shows the p-value.
>
> Decision and Conclusion
>
> A systematic way to make a decision of whether to reject or not reject the null hypothesis is to compare the p-value and
> a preset or preconceived α (also called a "significance level"). A preset α is the probability of a Type I error (rejecting
> the null hypothesis when the null hypothesis is true). It may or may not be given to you at the beginning of the problem.
>
> When you make a decision to reject or not reject H0, do as follows:
>
> • If α > p-value, reject H0. The results of the sample data are significant.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-021-pool-009

**Chunk:** `openstax_principles_ds:4.3:chunk-017`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> Assumptions for Linear Regression
>
> Testing the significance of the correlation coefficient requires that certain assumptions about the data are
> satisfied. The premise of this test is that the data are a sample of observed points taken from a larger
> population. We have not examined the entire population because it is not possible or feasible to do so. We are
> examining the sample to draw a conclusion about whether the linear relationship that we see between  and
> data in the sample data provides strong enough evidence that we can conclude that there actually is a linear
> relationship between  and  data in the population.
>
> The regression line equation that we calculate from the sample data gives the best-fit line for our particular
> sample. We want to use this best-fit line for the sample as an estimate of the best-fit line for the population
> (Figure 4.8). Examining the scatterplot and testing the significance of the correlation coefficient helps us
> determine if it is appropriate to do this.
>
> These are the assumptions underlying the test of significance:
>
> 1. There is a linear relationship in the population that models the average value of  for varying values of . In other words, the expected value of  for each particular value lies on a straight line in the population.
> (We do not know the equation for the line for the population. Our regression line from the sample is our
> best estimate of this line in the population.)
> 2. The y-values for any particular x-value are normally distributed about the line. This implies that there are
> more y-values scattered closer to the line than are scattered farther away. Assumption (1) implies that
> these normal distributions are centered on the line: the means of these normal distributions of y-values lie
> on the line. 3.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-021-pool-010

**Chunk:** `openstax_principles_ds:4.4:chunk-006`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.4: Analysis of Variance (ANOVA)
>
> The details of this Python function are shown in Example 4.25.
>
> Here is a step-by-step example to illustrate this ANOVA hypothesis testing process.
>
> EXAMPLE 4.25
>
> Problem
>
> An airline manager claims that the average arrival delays for flights from Boston to Dallas are the same for
> three airlines: Airlines A, B, and C. The following arrival delay data (in minutes) is collected on samples of
> flights for the three airlines (Table 4.18):
>
> Airline
>
> Airline
>
> Airline C
>
> A
>
> B
>
> 8
> 13
> 11
>
> 12
> 0
> 15
>
> 7
> 2
> 9
>
> 9
> 7
> 11
>
> 11
> 6
> 12
>
> 4
> 5
> N/A
>
> Table 4.18 Arrival Delay Data (in Minutes)
> for Three Airlines
>
> Use this sample data to test the claim that the average arrival delays are the same for three airlines: Airlines
> A, B, and C. Use a level of significance of 0.05 for this analysis. Assume the samples are independent and
> taken from approximately normal distributions and each population has approximately the same variance.
>
> Solution
>
> The first step in the hypothesis testing procedure is to write the null and alternative hypothesis based on
> the claim.
>
> For an ANOVA hypothesis test, the setup of the null and alternative hypotheses is shown here. Notice that
> the claim mentions “the average arrival delays are the same for three airlines,” which corresponds to the
> null hypothesis.
>
> : All three population means are equal:
>  [Claim]
>
> : At least one population mean is different from the others.
>
> The following Python program generates the corresponding F test statistic and p-value for this ANOVA
> analysis:
>
> PYTHON CODE
>
> # import libraries
> import numpy as np
> from scipy.stats  import f_oneway
>  
> # enter airline arrival data
>
> AirlineA = np.array([8, 12, 7, 9, 11, 4])
> AirlineB = np.array([13, 0, 2, 7, 6, 5])
> AirlineC = np.array([11, 15, 9, 11, 12])

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-021-pool-011

**Chunk:** `openstax_intro_stats_2e:9.4:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.4: Rare Events, the Sample, Decision and Conclusion
>
> Then the binomial distribution of a sample (estimated)
>
> proportion can be approximated by the normal distribution with
>  and
> . Remember that
> .
>
> 9.4 Rare Events, the Sample, Decision and Conclusion
>
> Establishing the type of distribution, sample size, and known or unknown standard deviation can help you figure out
> how to go about a hypothesis test. However, there are several other factors you should consider when working out a
> hypothesis test.
>
> Rare Events
>
> Suppose you make an assumption about a property of the population (this assumption is the null hypothesis). Then you
> gather sample data randomly. If the sample has properties that would be very unlikely to occur if the assumption is
> true, then you would conclude that your assumption about the population is probably incorrect. (Remember that your
> assumption is just an assumption—it is not a fact and it may or may not be true. But your sample data are real and the
> data are showing you a fact that seems to contradict your assumption.)
>
> For example, Didi and Ali are at a birthday party of a very wealthy friend. They hurry to be first in line to grab a prize from
> a tall basket that they cannot see inside because they will be blindfolded. There are 200 plastic bubbles in the basket and
> Didi and Ali have been told that there is only one with a $100 bill. Didi is the first person to reach into the basket and pull
> out a bubble. Her bubble contains a $100 bill. The probability of this happening is
>  = 0.005. Because this is so unlikely,
>
> Ali is hoping that what the two of them were told is wrong and there are more $100 bills in the basket.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-021-pool-012

**Chunk:** `openstax_intro_stats_2e:9.5:chunk-014`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.5: Additional Information and Full Hypothesis Test Examples
>
> The information is given in terms of
> percentages. Use the distribution for P′, the estimated proportion.
>
> Therefore,
>
> where p = 0.50, q = 1−p = 0.50, and n = 100
>
> Calculate the p-value using the normal distribution for proportions:
>
> p-value = P (p′ < 0.47 or p′ > 0.53) = 0.5485
>
> where x = 53, p′ =
>  = 0.53.
>
> Interpretation of the p-value: If the null hypothesis is true, there is 0.5485 probability (54.85%) that the sample
> (estimated) proportion  is 0.53 or more OR 0.47 or less (see the graph in Figure 9.10).
>
> Figure 9.10
>
> μ = p = 0.50 comes from H0, the null hypothesis.
>
> p′ = 0.53. Since the curve is symmetrical and the test is two-tailed, the p′ for the left tail is equal to 0.50 – 0.03 = 0.47
> where μ = p = 0.50. (0.03 is the difference between 0.53 and 0.50.)
>
> Compare α and the p-value:
>
> Since α = 0.01 and p-value = 0.5485. α < p-value.
>
> Make a decision: Since α < p-value, you cannot reject H0.
>
> Conclusion: At the 1% level of significance, the sample data do not show sufficient evidence that the percentage of first-
> time brides who are younger than their grooms is different from 50%.
>
> USING THE TI-83, 83+, 84, 84+ CALCULATOR
>
> Press STAT and arrow over to TESTS. Press 5:1-PropZTest. Enter .5 for p0, 53 for x and 100 for n. Arrow down to
>
> Prop and arrow to not equals p0. Press ENTER. Arrow down to Calculate and press ENTER. The calculator
>
> calculates the p-value (p = 0.5485) and the test statistic (z-score). Prop not equals .5 is the alternate hypothesis. Do
>
> this set of instructions again except arrow to Draw (instead of Calculate). Press ENTER. A shaded graph appears with

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-021-pool-013

**Chunk:** `openstax_intro_stats_2e:9.4:chunk-004`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.4: Rare Events, the Sample, Decision and Conclusion
>
> To persuade his customers that he is right, the baker decides to do a hypothesis test. He bakes 10 loaves of bread. The mean height of the sample loaves is 17 cm. The baker knows from baking hundreds of loaves of bread that the
> standard deviation for the height is 0.5 cm. and the distribution of heights is normal.
>
> The null hypothesis could be H0: μ ≤ 15 The alternate hypothesis is Ha: μ > 15
>
> The words "is more than" translates as a ">" so "μ > 15" goes into the alternate hypothesis. The null hypothesis must
> contradict the alternate hypothesis.
>
> By the Central Limit Theorem, the distribution of sample means, for samples of 10 loaves, will be normal with mean μ =
> 15 and standard deviation
> .
>
> Suppose the null hypothesis is true (the mean height of the loaves is no more than 15 cm). Then is the mean height (17
> cm) calculated from the sample unexpectedly large? The hypothesis test works by asking the question how unlikely the
> sample mean would be if the null hypothesis were true. The graph shows how far out the sample mean is on the normal
> curve. The p-value is the probability that, if we were to take other samples, any other sample mean would fall at least as
> far out as 17 cm.
>
> The p-value, then, is the probability that a sample mean is the same or greater than 17 cm. when the population
> mean is, in fact, 15 cm. We can calculate this probability using the normal distribution for means.
>
> Figure 9.2
>
> p-value= P( > 17) which is approximately zero.
>
> A p-value of approximately zero tells us that it is highly unlikely that a loaf of bread rises no more than 15 cm, on
> average.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-021-pool-014

**Chunk:** `openstax_intro_stats_2e:9.4:chunk-003`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.4: Rare Events, the Sample, Decision and Conclusion
>
> Didi is the first person to reach into the basket and pull
> out a bubble. Her bubble contains a $100 bill. The probability of this happening is
>  = 0.005. Because this is so unlikely,
>
> Ali is hoping that what the two of them were told is wrong and there are more $100 bills in the basket. A "rare event" has
> occurred (Didi getting the $100 bill) so Ali doubts the assumption about only one $100 bill being in the basket.
>
> Using the Sample to Test the Null Hypothesis
>
> Use the sample data to calculate the actual probability of getting the test result, called the p-value. The p-value is the
> probability that, if the null hypothesis is true, the results from another randomly selected sample will be as
> extreme or more extreme as the results obtained from the given sample.
>
> A large p-value calculated from the data indicates that we should not reject the null hypothesis. The smaller the p-value,
> the more unlikely the outcome, and the stronger the evidence is against the null hypothesis. We would reject the null
> hypothesis if the evidence is strongly against it.
>
> Draw a graph that shows the p-value. The hypothesis test is easier to perform if you use a graph because you see
> the problem more clearly.
>
> EXAMPLE 9.9
>
> Suppose a baker claims that his bread height is more than 15 cm, on average. Several of his customers do not believe
> him. To persuade his customers that he is right, the baker decides to do a hypothesis test. He bakes 10 loaves of bread. The mean height of the sample loaves is 17 cm. The baker knows from baking hundreds of loaves of bread that the
> standard deviation for the height is 0.5 cm. and the distribution of heights is normal.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---

## q-v1-022

**Pregunta:** How should a chi-square test of independence be conducted for a contingency table?

**Respondibilidad de referencia:** unanswerable

### q-v1-022-pool-001

**Chunk:** `openstax_principles_ds:4.2:chunk-025`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> When translating claims about a
> population proportions, use the symbols p1 and p2 as part of the null and alternative hypotheses to represent
> the two unknown population proportions. Refer to Table 4.9 and Table 4.10 for the various setups to construct
>
> the null and alternative hypotheses for two-sample hypothesis testing.
>
> Setup A
> Setup B
> Setup C
>
> Table 4.9 Three Possible Setups for the Null and Alternative Hypotheses
> for a Population Mean (Two Samples)
>
> Setup D
> Setup E
> Setup F
>
> Table 4.10 Three Possible Setups for the Null and Alternative
> Hypotheses for a Population Proportion (Two Samples)
>
> Comparing Two Means
>
> In this section, we discuss two-sample hypothesis testing for the mean when the population standard
> deviations are unknown. Typically, in real-world applications, population standard deviations are unknown, so
> this method has considerable practical appeal.
>
> One other consideration when conducting hypothesis testing for two samples is to determine if the two
> samples are dependent or independent. Two samples are considered to be independent samples when the
> sample values from one population are not related to the sample values taken from the second population. In
> other words, there is not an inherent paired or matched relationship between the two samples. Two samples
> are considered to be dependent samples if the samples from one population can be paired or matched to the
> samples taken from the second population. Dependent samples are sometimes also called paired samples.
>
> For example, if a researcher were to collect data for the ages for a random sample of 15 men and a random
> sample of 15 women, there would be no inherent relationship between these two samples, and so these
> samples are considered independent samples.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-002

**Chunk:** `openstax_principles_ds:4.4:chunk-005`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.4: Analysis of Variance (ANOVA)
>
> For degrees of freedom for the denominator, this is calculated as the total of the sample sizes minus the
> number of groups. 6. Calculate the quantity called “mean square between (MSB)” according to the following formula:
>
> 7. Calculate the quantity called “mean square within (MSW)” according to the following formula:
>
> 8. Calculate the test statistic (
> ), according to the following formula:
>
> Once the test statistic is obtained, the p-value is calculated as the area to the right of the test statistic under
> the
> -distribution curve (note that the ANOVA hypothesis test is always considered a “right-tail” test).
>
> Usually, the results of these computations are organized in an ANOVA summary table like Table 4.17.
>
> Degrees
>
> p-value
>
> Variation
> Sum of
> Squares
>
> Mean
> Squares
>
> Test Statistic
>
> of
> Freedom
>
> Between
> SSB
> MSB
> Area to the right of the F test statistic
>
> Within
> SSW
> MSW
> N/A
>
> Table 4.17 ANOVA Summary Table
>
> Using Python for One-Way ANOVA
>
> As mentioned earlier, due to the complexity of these calculations, technology is typically used to calculate the
> test statistic and p-value.
>
> Using Python, the f_oneway() function is provided as part of the scipy library, and this function provides
>
> both the test statistic and p-value for a one-way ANOVA hypothesis test.
>
> The syntax is to call the function with the data arrays as arguments, as in:
>
> f_oneway(Array1, Array2, Array3, …)
>
> The function returns both the F test statistic and the p-value for the one-way ANOVA hypothesis test.
>
> The details of this Python function are shown in Example 4.25.
>
> Here is a step-by-step example to illustrate this ANOVA hypothesis testing process.
>
> EXAMPLE 4.25
>
> Problem
>
> An airline manager claims that the average arrival delays for flights from Boston to Dallas are the same for
> three airlines: Airlines A, B, and C.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-003

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-008`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> NOTE
>
> When calculating the error bound, a probability table for the Student's t-distribution can also be used to find the value
> of t. The table gives t-scores that correspond to the confidence level (column) and degrees of freedom (row); the
> t-score is found where the row and column intersect in the table.
>
> TRY IT 8.8
>
> You do a study of hypnotherapy to determine how effective it is in increasing the number of hours of sleep subjects
> get each night. You measure hours of sleep for 12 subjects with the following results. Construct a 95% confidence
> interval for the mean number of hours slept for the population (assumed normal) from which you took the data.
>
> 8.2; 9.1; 7.7; 8.6; 6.9; 11.2; 10.1; 9.9; 8.9; 9.2; 7.5; 10.5
>
> EXAMPLE 8.9
>
> Problem
> The Human Toxome Project (HTP) is working to understand the scope of industrial pollution in the human body. Industrial chemicals may enter the body through pollution or as ingredients in consumer products. The scientists at HTP
> tested cord blood samples for 20 newborn infants in the United States. The cord blood of the "In utero/newborn" group
> was tested for 430 industrial compounds, pollutants, and other chemicals, including chemicals linked to brain and
> nervous system toxicity, immune system toxicity, and reproductive toxicity, and fertility problems. There are health
> concerns about the effects of some chemicals on the brain and nervous system. Table 8.3 shows how many of the
> targeted chemicals were found in each infant’s cord blood.
>
> 79
> 145
> 147
> 160
> 116
> 100
> 159
> 151
> 156
> 126
>
> 137
> 83
> 156
> 94
> 121
> 144
> 123
> 114
> 139
> 99
>
> Table 8.3
>
> Use this sample data to construct a 90% confidence interval for the mean number of targeted industrial chemicals to be
> found in an in infant’s blood.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-004

**Chunk:** `openstax_principles_ds:4.3:chunk-006`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> A more precise assessment of the correlation between the two quantities can be obtained by
> calculating the numeric correlation coefficient (referred to using the symbol ).
>
> The correlation coefficient is a measure of the strength and direction of the correlation between the
> independent variable  and the dependent variable .
>
> The formula for  is shown; however, software is typically used to calculate the correlation coefficient.
>
> where  refers to the number of data pairs and the symbol
>  indicates to sum the x-values.
>
> Note that this value of “ ” is sometimes referred to as the “Pearson correlation coefficient.”
>
> Table 4.15 provides a step-by-step procedure on how to calculate the correlation coefficient .
>
> Step
> Representation in Symbols
>
> 1. Calculate the sum of the x-values.
>
> 2. Calculate the sum of the y-values.
>
> 3. Multiply each x-value by the corresponding
> y-value and calculate the sum of these
>  products.
>
> 4. Square each x-value and then calculate the sum
> of these squared values.
>
> 5. Square each y-value and then calculate the sum
> of these squared values.
>
> n
>
> 6. Determine the value of , which is the number of
> data pairs.
>
> 7. Use these results to then substitute into the
> formula for the correlation coefficient.
>
> Table 4.15 Steps for Calculating the Correlation Coefficient
>
> Note that since  is calculated using sample data,  is considered a sample statistic and is used to measure the
> strength of the correlation for the two population variables. Recall that sample data indicates data based on a
> subset of the entire population.
>
> As mentioned, given the complexity of this calculation, software is typically used to calculate the correlation
> coefficient. There are several options for calculating the correlation coefficient in Python. The example shown
> uses the scipy.stats library in Python which includes the function pearsonr() for calculating the Pearson
>
> correlation coefficient ( ).

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-005

**Chunk:** `openstax_principles_ds:4.2:chunk-010`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> The smaller the p-value, the more the sample data deviates from the null hypothesis, and this is more evidence
> to indicate that the null hypothesis should be rejected.
>
> The final step in the hypothesis testing procedure is to come to a final decision regarding the null hypothesis. This is accomplished by comparing the p-value with the level of significance and applying the following rule:
>
> • If the p-value  level of significance, then the decision is to “reject the null hypothesis.”
> • If the p-value  level of significance, then the decision is to “fail to reject the null hypothesis.”
>
> Recall that these are the only two possible decisions that a researcher can deduce when conducting a
> hypothesis test.
>
> Often, we would like to translate these decisions into a conclusion that is easier to interpret for someone
> without a statistical background. For example, a decision to “fail to reject the null hypothesis” might be difficult
> to interpret for those not familiar with the terminology of hypothesis testing. These decisions can be
> translated into concluding statements such as those shown in Table 4.8.
>
> Is the claim in the null or
>
> Select the decision
> from the hypothesis
>
> the alternative
>
> Then, use this
> concluding statement:
>
> test:
>
> hypothesis?
>
> Row 1
> Reject the null
> hypothesis
>
> Claim is the null
> hypothesis
>
> There is enough
> evidence to reject the
> claim.
>
> Row 2
> Reject the null
> hypothesis
>
> Claim is the alternative
> hypothesis
>
> There is enough
> evidence to support the
> claim.
>
> Row 3
> Fail to reject the null
> hypothesis
>
> Claim is the null
> hypothesis
>
> There is not enough
> evidence to reject the
> claim.
>
> Row 4
> Fail to reject the null
> hypothesis
>
> Claim is the alternative
> hypothesis
>
> There is not enough
> evidence to support the
> claim.
>
> Table 4.8 How to Establish a Conclusion from a Hypothesis Test

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-006

**Chunk:** `openstax_principles_ds:4.2:chunk-033`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> Thus the setup
>
> of the null and alternative hypotheses will be as follows:
>
> The mean of the differences is average of the differences column shown in Table 4.13. The mean of the
> differences column is 13.9, and the standard deviation of the differences column is 12.414.
>
> Next, calculate the standardized test statistic as follows:
>
> Notice that since the alternative hypothesis contains a “greater than” symbol, the hypothesis test is called a
> “right tailed” test and the p-value will be calculated as the area under the t-distribution curve to the right of
> the test statistic. The area under the t-distribution curve to the right of a t-score of 3.541 (using degrees of
> freedom
> ) is approximately 0.003. Thus the p-value for this hypothesis test is 0.003.
>
> The final step in the hypothesis testing procedure is to come to a final decision regarding the null
> hypothesis. This is accomplished by comparing the p-value with the level of significance. In this example,
> the p-value is 0.003 and the level of significance is 0.05: since the p-value  level of significance, then the
> decision is to “reject the null hypothesis.”
>
> Conclusion: The decision is to reject the null hypothesis; the claim corresponds to the alternative
> hypothesis. This scenario corresponds to Row 2 in Table 4.8, and “there is enough evidence to support the
> claim that the medication helps to lower cholesterol levels.”
>
> Testing Claims for Two Proportions
>
> Data scientists and researchers are often interested in comparing two proportions. For example, a medical
> researcher might be interested in comparing the percentage of people contracting a respiratory virus for
> those taking a vaccine versus not taking a vaccine.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-007

**Chunk:** `openstax_intro_stats_2e:8.4:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.4: Confidence Interval (Home Costs)
>
> gives
>
> Round the answer to the next higher value. The sample size should be 752 cell phone customers aged 50+ in order to be
> 90% confident that the estimated (sample) proportion is within three percentage points of the true population
> proportion of all customers aged 50+ who use text messaging on their cell phones.
>
> TRY IT 8.14
>
> Suppose an internet marketing company wants to determine the current percentage of customers who click on ads
> on their smartphones. How many customers should the company survey in order to be 90% confident that the
> estimated proportion is within five percentage points of the true population proportion of customers who click on ads
> on their smartphones?
>
> 8.4 Confidence Interval (Home Costs)
>
> Stats Lab
>
> Confidence Interval (Home Costs)
> Class Time:
>
> Names:
>
> Student Learning Outcomes
>
> • The student will calculate the 90% confidence interval for the mean cost of a home in the area in which this school is
> located.
> • The student will interpret confidence intervals.
> • The student will determine the effects of changing conditions on the confidence interval.
>
> Collect the Data
> Check the Real Estate section in your local newspaper. Record the sale prices for 35 randomly selected homes recently
> listed in the county.
>
> NOTE
>
> Many newspapers list them only one day per week. Also, we will assume that homes come up for sale randomly.
>
> 1. Complete the table:
>
> Table 8.5
>
> Describe the Data
>
> 1. Compute the following:
> a.
>  = _____
> b.
>  = _____
>
> c. n = _____
>
> 2. In words, define the random variable
> . 3. State the estimated distribution to use. Use both words and symbols.
>
> Find the Confidence Interval
>
> 1. Calculate the confidence interval and the error bound.
> a. Confidence Interval: _____
> b. Error Bound: _____
>
> 2. How much area is in both tails (combined)? α = _____
> 3.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-008

**Chunk:** `openstax_principles_ds:4.2:chunk-005`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> Notice that for each setup, the null and alternative hypotheses
> are complements of one another. Note that the value of “ ” will be replaced by some numerical constant taken
> from the stated claim.
>
> Setup A
> Setup B
> Setup C
>
> Table 4.6 Possible Setups for the Null and
> Alternative Hypotheses for a Population Mean (One
> Sample)
>
> Table 4.7 provides the three possible setups for the null and alternative hypotheses when conducting a one-
> sample hypothesis test for a population proportion. Note that the value of “ ” will be replaced by some
> numerical constant taken from the stated claim.
>
> Setup D
> Setup E
> Setup F
>
> Table 4.7 Possible Setups for the Null and
> Alternative Hypotheses for a Population Proportion
> (One Sample)
>
> Follow these steps to determine which of these setups to use for a given hypothesis test:
>
> 1. Determine if the hypothesis test involves a claim for a population mean or population proportion. If the
> hypothesis test involves a population mean, use either Setup A, B, or C. 2. If the hypothesis test involves a population proportion, use either Setup D, E, or F. 3. Translate a phrase from the claim into a mathematical symbol and then match this mathematical symbol
> with one of the setups in Table 4.6 and Table 4.7.
>
> For example, if a claim for a hypothesis test for a mean references the phrase “at least,” note that the phrase
> “at least” corresponds to a greater than or equals symbol. A greater than or equals symbol appears in Setup C
> in Table 4.6, so that would be the correct setup to use.
>
> If a claim for a hypothesis test for a proportion references the phrase “different than,” note that the phrase
> “different than” corresponds to a not equals symbol.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-009

**Chunk:** `openstax_intro_stats_2e:9.1:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.1: Null and Alternative Hypotheses
>
> greater than or equal to (≥)
> less than (<)
>
> less than or equal to (≤)
> more than (>)
>
> Table 9.1
>
> NOTE
>
> H0 always has a symbol with an equal in it. Ha never has a symbol with an equal in it. The choice of symbol depends
> on the wording of the hypothesis test. However, be aware that many researchers (including one of the co-authors in
> research work) use = in the null hypothesis, even with > or < as the symbol in the alternative hypothesis. This practice
> is acceptable because we only make the decision to reject or not reject the null hypothesis.
>
> EXAMPLE 9.1
>
> H0: No more than 30% of the registered voters in Santa Clara County voted in the primary election. p ≤ .30
> Ha: More than 30% of the registered voters in Santa Clara County voted in the primary election. p > 30
>
> TRY IT 9.1
>
> A medical trial is conducted to test whether or not a new medicine reduces cholesterol by 25%. State the null and
> alternative hypotheses.
>
> EXAMPLE 9.2
>
> We want to test whether the mean GPA of students in American colleges is different from 2.0 (out of 4.0). The null and
> alternative hypotheses are:
> H0: μ = 2.0
> Ha: μ ≠ 2.0
>
> TRY IT 9.2
>
> We want to test whether the mean height of eighth graders is 66 inches. State the null and alternative hypotheses. Fill
> in the correct symbol (=, ≠, ≥, <, ≤, >) for the null and alternative hypotheses.
>
> a. H0: μ __ 66
> b. Ha: μ __ 66
>
> EXAMPLE 9.3
>
> We want to test if college students take less than five years to graduate from college, on the average. The null and
> alternative hypotheses are:
> H0: μ ≥ 5
> Ha: μ < 5
>
> TRY IT 9.3

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-010

**Chunk:** `openstax_principles_ds:4.2:chunk-017`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> df is the degrees of freedom.
>
> Here is the Python code to calculate the p-value for this example:
>
> PYTHON CODE
>
> # from scipy.stats import t
> from scipy.stats import t
>
> # define parameters test_statistic and degrees of freedom df
> x = -1.552
> df = 49
>
> # use t.cdf function to calculate area under t-distribution curve - note this is
> the area to the left of the x-value
> # subtract this result from 1 to obtain area to the right of the x-value
> # use round function to round answer to 4 decimal places
> round (t.cdf(x, df=49), 4)
>
> The resulting output will look like this:
>
> 0.0635
>
> The final step in the hypothesis testing procedure is to come to a final decision regarding the null
> hypothesis. This is accomplished by comparing the p-value with the level of significance. In this example,
> the p-value is 0.127 and the level of significance is 0.10: since the p-value  level of significance, then the
> decision is to “fail to reject the null hypothesis.”
>
> Conclusion: The decision is to fail to reject the null hypothesis; the claim corresponds to the null hypothesis. This scenario corresponds to Row 3 in Table 4.8, which means “there is not enough evidence to reject the
> claim” that the mean battery life of its latest smartphone model is 25 hours.
>
> Testing Claims for the Proportion
>
> In this section, we discuss one sample hypothesis testing for proportions. Recall that a sample proportion is
> measuring “how many out of the total.” For example, a medical researcher might be interested in testing a
> claim that the proportion of patients experiencing side effects from a new blood pressure–lowering medication
> is less than 4%.
>
> Here are the requirements to use this procedure:
>
> a. A random sample is selected from the population.
> b.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-011

**Chunk:** `openstax_intro_stats_2e:8.2:chunk-005`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.2: A Single Population Mean using the Student t Distribution
>
> Random sampling is assumed, but that is a completely separate assumption from normality.
>
> Calculators and computers can easily calculate any Student's t-probabilities. The TI-83,83+, and 84+ have a tcdf function
> to find the probability for given values of t. The grammar for the tcdf command is tcdf(lower bound, upper bound,
> degrees of freedom). However for confidence intervals, we need to use inverse probability to find the value of t when we
> know the probability.
>
> For the TI-84+ you can use the invT command on the DISTRibution menu. The invT command works similarly to the
> invnorm. The invT command requires two inputs: invT(area to the left, degrees of freedom) The output is the t-score
> that corresponds to the area we specified.
>
> The TI-83 and 83+ do not have the invT command. (The TI-89 has an inverse T command.)
>
> A probability table for the Student's t-distribution can also be used. The table gives t-scores that correspond to the
> confidence level (column) and degrees of freedom (row). (The TI-86 does not have an invT program or command, so if
> you are using that calculator, you need to use a probability table for the Student's t-Distribution.) When using a t-table,
> note that some tables are formatted to show the confidence level in the column headings, while the column headings in
> some tables may show only corresponding area in one or both tails.
>
> A Student's t table (See Appendix H Tables) gives t-scores given the degrees of freedom and the right-tailed probability. The table is very limited. Calculators and computers can easily calculate any Student's t-probabilities.
>
> The notation for the Student's t-distribution (using T as the random variable) is:

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-012

**Chunk:** `openstax_intro_stats_2e:8.4:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 8: Confidence Intervals
> Section 8.4: Confidence Interval (Home Costs)
>
> c. n = _____
>
> 2. In words, define the random variable
> . 3. State the estimated distribution to use. Use both words and symbols.
>
> Find the Confidence Interval
>
> 1. Calculate the confidence interval and the error bound.
> a. Confidence Interval: _____
> b. Error Bound: _____
>
> 2. How much area is in both tails (combined)? α = _____
> 3. How much area is in each tail?
>  = _____
>
> 4. Fill in the blanks on the graph with the area in each section. Then, fill in the number line with the upper and lower
> limits of the confidence interval and the sample mean.
>
> Figure 8.6
>
> 5. Some students think that a 90% confidence interval contains 90% of the data. Use the list of data on the first page
> and count how many of the data values lie within the confidence interval. What percent is this? Is this percent close
> to 90%? Explain why this percent should or should not be close to 90%.
>
> Describe the Confidence Interval
>
> 1. In two to three complete sentences, explain what a confidence interval means (in general), as if you were talking to
> someone who has not taken statistics. 2. In one to two complete sentences, explain what this confidence interval means for this particular study.
>
> Use the Data to Construct Confidence Intervals
>
> 1. Using the given information, construct a confidence interval for each confidence level given.
>
> Confidence level
> EBM/Error Bound
> Confidence Interval
>
> 50%
>
> 80%
>
> 95%
>
> 99%
>
> Table 8.6
>
> 2. What happens to the EBM as the confidence level increases? Does the width of the confidence interval increase or
> decrease? Explain why this happens.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-013

**Chunk:** `openstax_intro_stats_2e:9.4:chunk-001`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.4: Rare Events, the Sample, Decision and Conclusion
>
> Assumptions
>
> When you perform a hypothesis test of a single population mean μ using a normal distribution (often called a z-test), you
> take a simple random sample from the population. The population you are testing is normally distributed, or your
> sample size is sufficiently large. You know the value of the population standard deviation, which, in reality, is rarely
> known.
>
> When you perform a hypothesis test of a single population mean μ using a Student's t-distribution (often called a
> t-test), there are fundamental assumptions that need to be met in order for the test to work properly. Your data should
> be a simple random sample that comes from a population that is approximately normally distributed. You use the
> sample standard deviation to approximate the population standard deviation. (Note that if the sample size is sufficiently
> large, a t-test will work even if the population is not approximately normally distributed).
>
> When you perform a hypothesis test of a single population proportion p, you take a simple random sample from the
> population. You must meet the conditions for a binomial distribution: there are a certain number n of independent
> trials, the outcomes of any trial are success or failure, and each trial has the same probability of a success p. The shape
> of the binomial distribution needs to be similar to the shape of the normal distribution. To ensure this, the quantities np
> and nq must both be greater than five (
>  and
> ). Then the binomial distribution of a sample (estimated)
>
> proportion can be approximated by the normal distribution with
>  and
> . Remember that
> .
>
> 9.4 Rare Events, the Sample, Decision and Conclusion
>
> Establishing the type of distribution, sample size, and known or unknown standard deviation can help you figure out
> how to go about a hypothesis test.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-014

**Chunk:** `openstax_principles_ds:4.2:chunk-024`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> As a reminder, the general hypothesis testing method introduced in the previous section includes the following
> steps:
>
> 1. Set up a null and an alternative hypothesis based on the claim. 2. Collect relevant sample data to investigate the claim. 3. Determine the correct distribution to be used to analyze the hypothesis test (e.g., normal distribution or t-
> distribution). 4. Analyze the sample data to determine if the sample data is consistent with the null hypothesis. This will
> involve statistical calculations involving a test statistic and a p-value, which are discussed next. 5. If the sample data is inconsistent with the null hypothesis, then the decision is to “reject the null
> hypothesis.” If the sample data is consistent with the null hypothesis, then the decision is to “fail to reject
> the null hypothesis.”
>
> As discussed for one-sample hypothesis testing, when writing the null and alternative hypotheses, start off by
> translating the claim into a mathematical statement involving the unknown population parameters. The claim
> could correspond to either the null or the alternative hypothesis. Then write the complement of this statement
> in order to write the other hypothesis. The difference now as compared to the previous section is that the
> hypotheses will be comparing two means or two proportions instead of just one mean or one proportion.
>
> When translating claims about a population mean, use the symbols
>  and
>  as part of the null and
> alternative hypotheses to represent the two unknown population means. When translating claims about a
> population proportions, use the symbols p1 and p2 as part of the null and alternative hypotheses to represent
> the two unknown population proportions. Refer to Table 4.9 and Table 4.10 for the various setups to construct
>
> the null and alternative hypotheses for two-sample hypothesis testing.
>
> Setup A
> Setup B
> Setup C

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-015

**Chunk:** `openstax_principles_ds:4.1:chunk-018`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.1: Statistical Inference and Confidence Intervals
>
> Assume a population
> standard deviation of $8,000.
>
> Solution
>
> For a 90% confidence interval, the corresponding critical value is
> . The population standard
> deviation is given as $8,000, and the margin of error is given as $1,000.
>
> Using the sample size formula:
>
> Round to the next higher whole number, so the desired sample size is 174.
>
> The analyst should target a sample size of 174 chemical engineers for a salary-related survey in order to
> them calculate a 90% confidence interval for the mean salary of chemical engineers.
>
> Sample Size for Confidence interval for a Proportion
>
> In Example 4.5, how would the researcher know the optimal sample size to use to collect sample data on the
> proportion of adults who are smokers? The margin of error formula can be used to derive the sample size for a
> proportion as follows:
>
> Where:
>
> is the critical value of the normal distribution.
>  is the sample proportion.
>
> is the desired margin of error.
>
> Notice in this formula, it’s assumed that some prior estimate for the sample proportion  is available, perhaps
> from historical data or previous studies. If a prior estimate for the sample proportion is not available, then use
> the value of 0.5 for .
>
> DETERMINING SAMPLE SIZE
>
> When determining sample size needed for a confidence interval for a proportion:
>
> If a prior estimate for the sample proportion is available, then that prior estimate should be utilized.
>
> • If a prior estimate for the sample proportion is not available, then use
> .
>
> EXAMPLE 4.7
>
> Problem
>
> Political candidate Smith is planning a survey to determine a 95% confidence interval for the proportion of
> voters who plan to vote for Smith. How many people should be surveyed? Assume a margin of error is 3%.
>
> a.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-016

**Chunk:** `openstax_principles_ds:4.3:chunk-017`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.3: Correlation and Linear Regression Analysis
>
> Assumptions for Linear Regression
>
> Testing the significance of the correlation coefficient requires that certain assumptions about the data are
> satisfied. The premise of this test is that the data are a sample of observed points taken from a larger
> population. We have not examined the entire population because it is not possible or feasible to do so. We are
> examining the sample to draw a conclusion about whether the linear relationship that we see between  and
> data in the sample data provides strong enough evidence that we can conclude that there actually is a linear
> relationship between  and  data in the population.
>
> The regression line equation that we calculate from the sample data gives the best-fit line for our particular
> sample. We want to use this best-fit line for the sample as an estimate of the best-fit line for the population
> (Figure 4.8). Examining the scatterplot and testing the significance of the correlation coefficient helps us
> determine if it is appropriate to do this.
>
> These are the assumptions underlying the test of significance:
>
> 1. There is a linear relationship in the population that models the average value of  for varying values of . In other words, the expected value of  for each particular value lies on a straight line in the population.
> (We do not know the equation for the line for the population. Our regression line from the sample is our
> best estimate of this line in the population.)
> 2. The y-values for any particular x-value are normally distributed about the line. This implies that there are
> more y-values scattered closer to the line than are scattered farther away. Assumption (1) implies that
> these normal distributions are centered on the line: the means of these normal distributions of y-values lie
> on the line. 3.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-017

**Chunk:** `openstax_principles_ds:3.2:chunk-006`

**Texto:**

> Source: Principles of Data Science
> Chapter 3: Descriptive Statistics: Statistical Measurements and Probability Distributions
> Section 3.2: Measures of Variation
>
> The
> average salary for both companies is $60,000. For Company A, the standard deviation of salaries is $8,000,
> whereas the standard deviation for salaries for Company B is $19,000. Because Company B has a higher
> standard deviation, we know that there is more variation in the employee salaries for Company B as compared
> to Company A.
>
> There are two different formulas for calculating standard deviation. Which formula to use depends on whether
> the data represents a sample or a population. The notation  is used to represent the sample standard
> deviation, and the notation  is used to represent the population standard deviation. In the formulas shown,
> is the sample mean,  is the population mean,  is the sample size, and
>  is the population size.
>
> Formula for the sample standard deviation:
>
> Formula for the population standard deviation:
>
> Notice that the sample standard deviation is calculated as the square root of the variance. This means that
> once the sample variance has been calculated, the sample standard deviation can then be easily calculated as
> the square root of the sample variance, as in Example 3.7.
>
> EXAMPLE 3.7
>
> Problem
>
> A biologist calculates that the sample variance for the amount of plant growth for a sample of plants is 8.7
> cm2. Calculate the sample standard deviation.
>
> Solution
>
> The sample standard deviation ( ) is calculated as the square root of the variance.
>
> EXAMPLE 3.8
>
> Problem
>
> Assume the sample variance (
> ) for a dataset is calculated as 42.2. Based on this, calculate the sample
> standard deviation.
>
> Solution
>
> The sample standard deviation ( ) is calculated as the square root of the variance.
>
> This result indicates that the standard deviation is about 6.5 years.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-018

**Chunk:** `openstax_principles_ds:4.2:chunk-029`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> The area under the t-distribution curve to the left of a t-score of
>  (using degrees of
> freedom
> ) is approximately 0.025. Thus, the p-value for this hypothesis test is 0.025.
>
> The final step in the hypothesis testing procedure is to come to a final decision regarding the null
> hypothesis. This is accomplished by comparing the p-value with the level of significance. In this example,
> the p-value is 0.025 and the level of significance is 0.04: since the p-value  level of significance, then the
> decision is to “reject the null hypothesis.”
>
> Conclusion: The decision is to reject the null hypothesis; the claim corresponds to the alternative
> hypothesis. This scenario corresponds to Row 2 in Table 4.8, and thus “there is enough evidence to support
> the claim” that the average salary of women engineers is less than that of men engineers.
>
> This problem can also be solved using the Python function called ttest_ind_from_stats().
>
> There is also a Python function to perform a two-sample t-test given raw data for the two groups, and this
> Python function is ttest_ind().
>
> For the function ttest_ind_from_stats(), the syntax is as follows:
>
> PYTHON CODE
>
> stats.ttest_ind_from_stats(sample_mean1, sample_standard_deviation1,
> sample_size1, sample_mean2, sample_standard_deviation2, sample_size2)
>
> Here is the Python code that can be used to solve Example 4.19. Note that this function returns the two-
> tailed p-value. Since Example 4.19 involves a left-tailed test, the desired p-value is one-half of the two-tailed
> p-value.
>
> PYTHON CODE
>
> import scipy.stats as stats
> import numpy as np
>  
> #Example 4.19 - Two Sample t-test given sample means, sample standard deviations
>
> sample_mean1 = 72700
> sample_standard_deviation1 = 9800
> sample_size1 = 45
>
> sample_mean2 = 76900
> sample_standard_deviation2 = 10700
> sample_size2 = 50
>
> test_statistic, two_tailed_p_value = stats.ttest_ind_from_stats(sample_mean1,
> sample_standard_deviation1, sample_size1, sample_mean2,
> sample_standard_deviation2, sample_size2)
>
> left_tailed_p_value = two_tailed_p_value / 2
>
> print("test statistic = ", "%.3f" % test_statistic)
> print("p-value = ", "%.3f" % left_tailed_p_value)

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-019

**Chunk:** `openstax_intro_stats_2e:9.4:chunk-002`

**Texto:**

> Source: Introductory Statistics 2e
> Chapter 9: Hypothesis Testing with One Sample
> Section 9.4: Rare Events, the Sample, Decision and Conclusion
>
> Then the binomial distribution of a sample (estimated)
>
> proportion can be approximated by the normal distribution with
>  and
> . Remember that
> .
>
> 9.4 Rare Events, the Sample, Decision and Conclusion
>
> Establishing the type of distribution, sample size, and known or unknown standard deviation can help you figure out
> how to go about a hypothesis test. However, there are several other factors you should consider when working out a
> hypothesis test.
>
> Rare Events
>
> Suppose you make an assumption about a property of the population (this assumption is the null hypothesis). Then you
> gather sample data randomly. If the sample has properties that would be very unlikely to occur if the assumption is
> true, then you would conclude that your assumption about the population is probably incorrect. (Remember that your
> assumption is just an assumption—it is not a fact and it may or may not be true. But your sample data are real and the
> data are showing you a fact that seems to contradict your assumption.)
>
> For example, Didi and Ali are at a birthday party of a very wealthy friend. They hurry to be first in line to grab a prize from
> a tall basket that they cannot see inside because they will be blindfolded. There are 200 plastic bubbles in the basket and
> Didi and Ali have been told that there is only one with a $100 bill. Didi is the first person to reach into the basket and pull
> out a bubble. Her bubble contains a $100 bill. The probability of this happening is
>  = 0.005. Because this is so unlikely,
>
> Ali is hoping that what the two of them were told is wrong and there are more $100 bills in the basket.

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

### q-v1-022-pool-020

**Chunk:** `openstax_principles_ds:4.2:chunk-007`

**Texto:**

> Source: Principles of Data Science
> Chapter 4: Inferential Statistics and Regression Analysis
> Section 4.2: Hypothesis Testing
>
> A less
> than or equals symbol must be used in the null hypothesis. The complement of less than or equals is a
> greater than symbol, which will be used in the alternative hypothesis. The claim refers to the population
> proportion of smokers, so the symbol  will be used. Notice that this setup will correspond to Setup E from
> Table 4.7. Thus, the setup of the null and alternative hypotheses will be as follows:
>
> The basis of the hypothesis test procedure is to assume that the null hypothesis is true to begin with and then
> examine the sample data to determine if the sample data is consistent with the null hypothesis. Based on this
> analysis, you will decide to either reject the null hypothesis or fail to reject the null hypothesis.
>
> It is important to note that these are the only two possible decisions for any hypothesis test, namely:
>
> • Reject the null hypothesis, or
> • Fail to reject the null hypothesis.
>
> Keep in mind that this decision will be based on statistical analysis of sample data, so there is a small chance of
> coming to a wrong decision. The only way to be absolutely certain of your decision is to test the entire
> population, which is typically not feasible. Since the hypothesis test decision is based on a sample, there are
> two possible errors that can be made by the researcher:
>
> • The researcher rejects the null hypothesis when in fact the null hypothesis is actually true, or a Type I
> error.
> • A researcher fails to reject the null hypothesis when the null hypothesis is actually false, or a Type II error.
>
> In hypothesis testing, the maximum allowed probability of making a Type I error is called the level of
> significance, denoted by the Greek letter alpha, .

**Revisión humana:**

- Grado: `__`
- Canónico: `sí / no / pendiente`
- Nota:

---
