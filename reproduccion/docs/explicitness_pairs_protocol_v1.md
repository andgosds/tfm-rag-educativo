# Parejas de explicitud conceptual — borrador v1

## Estado y alcance

Se examinan las 13 preguntas respondibles del golden set. Cada pareja conserva literalmente la pregunta original y añade una formulación alternativa. No son nuevas preguntas base. Ninguna pareja está aprobada para ejecución: los candidatos requieren revisión humana de equivalencia y suficiencia. No se han ejecutado recuperadores ni generación.

La explicitud se define respecto a un concepto objetivo declarado. Una consulta implícita puede conservar otros términos técnicos. Este ajuste evita exigir la eliminación de todo el vocabulario disciplinar. No se añaden etiquetas de dificultad ni componentes de respuesta.

## Selección antes de ejecutar

Aceptar solo si ambas consultas piden la misma información, conservan condiciones y conducta, admiten la misma referencia, son claras y no proporcionan partes sustantivas de la respuesta mediante la descripción del concepto. Una paráfrasis no es un cambio puramente léxico: registrar diferencias de longitud y pistas como limitaciones. No seleccionar parejas en función del rendimiento obtenido.

Cribado del asistente: {'candidate': 7, 'needs_revision': 6}. candidate significa candidata a revisión, no equivalencia confirmada. needs_revision queda fuera de cualquier ejecución mientras no se revise o descarte.

## Parejas para revisión

### q-v1-001 — candidate

**Concepto objetivo:** sampling distribution of the sample mean

**Explícita:** How does increasing the sample size affect the sampling distribution of the sample mean?

**Implícita:** How does increasing the number of observations in each sample affect the distribution of the averages obtained by repeatedly drawing samples of that size?

**Referencia existente, pendiente de confirmar para la pareja:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.

**Cautela:** Conserva tamaño muestral y distribución de medias; la descripción operacional alarga la consulta.

### q-v1-002 — candidate

**Concepto objetivo:** Type I and Type II errors

**Explícita:** How do Type I and Type II errors differ in terms of the truth of the null hypothesis and the decision made?

**Implícita:** In hypothesis testing, what are the two ways a decision about the null hypothesis can be wrong, considering whether that hypothesis is actually true or false?

**Referencia existente, pendiente de confirmar para la pareja:** A Type I error occurs when a true null hypothesis is rejected. A Type II error occurs when a false null hypothesis is not rejected.

**Cautela:** Mantiene las dos decisiones erróneas sin proporcionar sus nombres.

### q-v1-003 — needs_revision

**Concepto objetivo:** hypothesis test

**Explícita:** What sequence of steps should be followed to conduct a hypothesis test?

**Implícita:** What sequence of steps should be followed to assess a claim about a population using sample data and decide whether to reject it?

**Referencia existente, pendiente de confirmar para la pareja:** Formulate null and alternative hypotheses from the claim, collect relevant sample data, select the appropriate sampling distribution, analyze the data using a test statistic and p-value, and then reject or fail to reject the null hypothesis according to whether the sample is inconsistent with it.

**Cautela:** Puede confundir la afirmación de interés con la hipótesis nula; no incluir sin resolver esa equivalencia.

### q-v1-004 — needs_revision

**Concepto objetivo:** median

**Explícita:** Why is the median a suitable measure of center when a dataset contains extreme outliers?

**Implícita:** Why is the central value of an ordered dataset a suitable measure of center when the dataset contains extreme outliers?

**Referencia existente, pendiente de confirmar para la pareja:** The median depends on the middle position of the ordered data and is not affected by the numerical magnitude of extreme values.

**Cautela:** La descripción proporciona parte de la explicación esperada y simplifica el caso de tamaño par.

### q-v1-005 — needs_revision

**Concepto objetivo:** correlation coefficient

**Explícita:** What two aspects of the relationship between an independent and a dependent variable are summarized by the correlation coefficient?

**Implícita:** What two aspects of the relationship between an independent and a dependent variable are summarized by a numerical measure of their association?

**Referencia existente, pendiente de confirmar para la pareja:** The correlation coefficient summarizes the strength and the direction of the correlation.

**Cautela:** Una medida de asociación puede referirse a otras medidas; ocultar el nombre pierde unicidad.

### q-v1-006 — candidate

**Concepto objetivo:** confidence interval

**Explícita:** If all other inputs remain unchanged, how does increasing the confidence level from 90% to 95% affect the width of the confidence interval, and why?

**Implícita:** If all other inputs remain unchanged, how does increasing the confidence level from 90% to 95% affect the width of the range estimated from sample data for a population parameter, and why?

**Referencia existente, pendiente de confirmar para la pareja:** The 95% confidence interval is wider than the 90% interval because greater confidence requires an interval that covers a larger range of plausible values for the population parameter.

**Cautela:** Se oculta confidence interval, no confidence level; explicitud relativa al concepto objetivo, no ausencia de todo tecnicismo.

### q-v1-011 — needs_revision

**Concepto objetivo:** standardized normal variable / standardized score

**Explícita:** For a standardized normal variable, what values define its center and spread, and how should the sign and magnitude of its standardized score be interpreted?

**Implícita:** For a normally distributed variable expressed as distances from its mean in units of its standard deviation, what values define its center and spread, and how should the sign and magnitude of those distances be interpreted?

**Referencia existente, pendiente de confirmar para la pareja:** The standard normal distribution has mean 0 and standard deviation 1. A z-score states how many standard deviations a value lies from the mean: a positive score is above the mean, a negative score is below it, and zero corresponds to the mean.

**Cautela:** La descripción revela la interpretación que se pide; riesgo de filtración de respuesta.

### q-v1-012 — candidate

**Concepto objetivo:** confidence interval

**Explícita:** With confidence level and population variability held constant, how does a larger sample affect the error bound and the width of a confidence interval?

**Implícita:** With confidence level and population variability held constant, how does a larger sample affect the error bound and the width of the range estimated from sample data for a population parameter?

**Referencia existente, pendiente de confirmar para la pareja:** A larger sample decreases the error bound and therefore makes the confidence interval narrower, provided that the confidence level and population variability remain fixed.

**Cautela:** Conserva condiciones y ambos efectos solicitados; solo se oculta confidence interval.

### q-v1-013 — candidate

**Concepto objetivo:** Student t distribution

**Explícita:** Which distribution should be used to construct a confidence interval for a population mean when the population standard deviation is known versus when it is estimated by the sample standard deviation, and how do degrees of freedom enter the Student t case?

**Implícita:** Which distribution should be used to construct a confidence interval for a population mean when the population standard deviation is known versus when it is estimated by the sample standard deviation, and how do degrees of freedom enter the latter case?

**Referencia existente, pendiente de confirmar para la pareja:** Use the normal distribution when the population standard deviation is known. When it is unknown and estimated by the sample standard deviation, use Student's t-distribution. For a simple random sample from an approximately normal population, the t-distribution has n − 1 degrees of freedom, which determine its exact shape.

**Cautela:** Retira la pista Student t; conserva ambas condiciones y la petición de grados de libertad.

### q-v1-014 — candidate

**Concepto objetivo:** interquartile range

**Explícita:** What sequence should be followed to flag unusually low or high observations using the interquartile range of an ordered dataset?

**Implícita:** What sequence should be followed to flag unusually low or high observations using the middle 50% of an ordered dataset?

**Referencia existente, pendiente de confirmar para la pareja:** Order the data and determine the first and third quartiles. Compute the interquartile range as the difference between the third and first quartiles, use the quartiles and a 1.5-IQR cutoff to define lower and upper bounds, and flag values below the lower bound or above the upper bound for further investigation.

**Cautela:** Original implícita; alternativa explícita. No introducir el factor 1.5 en ninguna consulta.

### q-v1-015 — needs_revision

**Concepto objetivo:** mean / trimmed mean / median

**Explícita:** How do the ordinary mean, a trimmed mean, and the median respond differently to extreme observations?

**Implícita:** How do the average of all observations, an average computed after removing a proportion of observations from each end of the ordered data, and the central value of the ordered data respond differently to extreme observations?

**Referencia existente, pendiente de confirmar para la pareja:** Extreme observations can disproportionately skew the ordinary mean. A trimmed mean reduces their influence by removing a selected percentage of values from both tails before averaging. The median depends on the middle position of the ordered data and is not affected by the numerical magnitude of the outliers.

**Cautela:** La descripción revela mecanismos de robustez y modifica mucho la longitud; no forzar su inclusión.

### q-v1-016 — candidate

**Concepto objetivo:** discrete / continuous random variables

**Explícita:** How do discrete random variables associated with counting differ from continuous random variables associated with measurement in the kinds of numerical values they can take?

**Implícita:** How do count-based outcomes differ from measurement-based outcomes in the kinds of numerical values they can take?

**Referencia existente, pendiente de confirmar para la pareja:** A discrete random variable takes a finite or countably infinite set of distinct values and typically results from counting. A continuous random variable can take any value within an interval and typically results from measurement.

**Cautela:** Original implícita; alternativa explícita conservando conteo y medición.

### q-v1-017 — needs_revision

**Concepto objetivo:** one-way ANOVA

**Explícita:** When is one-way ANOVA an appropriate choice, and how are its null and alternative hypotheses framed?

**Implícita:** When is a test that compares population means across groups defined by a single factor an appropriate choice, and how are its null and alternative hypotheses framed?

**Referencia existente, pendiente de confirmar para la pareja:** One-way ANOVA is appropriate for comparing three or more population means when there is one independent variable. Its null hypothesis states that all population means are equal, while its alternative states that at least one population mean differs from the others.

**Cautela:** La descripción aporta parte del criterio de uso; puede incluir alternativas a ANOVA. No incluir sin revisión.

## Preguntas no respondibles

No se incluyen en la primera tanda. 008 y 020 pueden estudiarse después conservando premisa falsa y corrección; 007 y 019 deben conservar el dato ausente y la población exacta; 009 y 021, ambos métodos y alcance comparativo; 010 y 022, el procedimiento fuera del corpus. 018 no se transforma en esta fase: retirar el nombre inventado puede cambiar su respondibilidad. Estos son criterios de cribado, no decisiones adjudicadas.

## Puerta de entrada al experimento

1. Revisión humana: aceptar, revisar o excluir cada pareja; registrar decisión explícita.
2. Confirmar equivalencia de referencia y evidencia. Las referencias copiadas son candidatas; no se heredan adjudicaciones de la pregunta original.
3. Revisiones auxiliares, si se realizan, aisladas y trazables; nunca sustituyen la decisión humana.
4. Congelar las parejas aceptadas y ejecutar las cuatro estrategias con ambas versiones. Construir el pool incremental sobre la unión de candidatos, revisar novedades y confirmar qrels antes de calcular métricas definitivas.
5. Fijar configuración y métricas antes de observar resultados. Propuesta: Recall@5 y nDCG@5 para el presupuesto top-5, cortes @10 secundarios; Faithfulness y Factual Correctness según aplicabilidad y conducta separada. Repeticiones, orden y presupuesto quedan pendientes de cerrar.
6. Generar ambas versiones bajo el mismo contrato y campaña, con orden equilibrado y persistencia. No comparar generaciones nuevas con originales históricos como contraste principal.

La unidad del análisis es la pregunta base. Mostrar diferencias implícita menos explícita por estrategia, tamaños y resultados por pregunta. Si la formulación cambia tanto en retrieval como en generación, el contraste end-to-end mide sensibilidad conjunta, no un efecto causal exclusivo del recuperador. No tratar las formulaciones como observaciones independientes.

## Archivos

- Datos: ../data/golden/variants/explicitness_pairs_v1_draft.jsonl
- Hoja de revisión: ../data/golden/variants/explicitness_pairs_v1_review.csv
- Trazabilidad: ../data/golden/variants/explicitness_pairs_v1_manifest.json
