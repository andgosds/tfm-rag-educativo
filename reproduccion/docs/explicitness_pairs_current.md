# Parejas de explicitud — conjunto vigente

## Fuente de trabajo

Usar `../data/golden/variants/explicitness_pairs_v1_consolidated.jsonl` y su CSV homónimo. Sustituyen a borradores y hojas anteriores para preparar la recuperación; estos se conservan como historial. El registro de procedencia y validación está en `explicitness_pairs_v1_validation.json`.

## Alcance de la validación

Siete preguntas base y catorce formulaciones. Revisión semántica y de evidencia realizada por el asistente bajo delegación del usuario, no validación independiente ni adjudicación humana. Se conserva la aceptación humana de 001. Se han comprobado las citas canónicas contra el texto real de los chunks.

El conjunto queda cerrado para obtener candidatos de recuperación. No está aprobado para calcular métricas finales con qrels heredados sin revisar: recuperar con ambas versiones, reunir candidatos de las cuatro estrategias, identificar novedades frente al pool técnico y revisar relevancia antes de cerrar evaluación. No se ha ejecutado recuperación ni generación.

## Revisión por pregunta

### q-v1-001

**Explícita:** How does increasing the sample size affect the sampling distribution of the sample mean?

**Implícita:** How does increasing the sample size affect the distribution of the averages obtained by repeatedly drawing samples of that size?

**Referencia:** As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal, retains the population mean, and has a smaller standard deviation equal to the population standard deviation divided by the square root of the sample size.

**Comprobación:** El chunk explica forma, centro y dispersión al aumentar n, y distingue tamaño muestral de número de repeticiones.

### q-v1-002

**Explícita:** How do Type I and Type II errors differ in terms of the truth of the null hypothesis and the decision made?

**Implícita:** In hypothesis testing, what are the two ways a decision about the null hypothesis can be wrong, considering whether that hypothesis is actually true or false?

**Referencia:** A Type I error occurs when a true null hypothesis is rejected. A Type II error occurs when a false null hypothesis is not rejected.

**Comprobación:** La tabla y el texto distinguen ambos errores por verdad de H0 y decisión. No exigir etiquetas técnicas como contenido adicional en la versión implícita.

### q-v1-003

**Explícita:** What sequence of steps should be followed to conduct a hypothesis test?

**Implícita:** What sequence of steps should be followed to evaluate a claim about a population using sample data?

**Referencia:** Formulate null and alternative hypotheses from the claim, collect relevant sample data, select the appropriate sampling distribution, analyze the data using a test statistic and p-value, and then reject or fail to reject the null hypothesis according to whether the sample is inconsistent with it.

**Comprobación:** El texto incluye cinco pasos y permite que la afirmación corresponda a H0 o H1. Se neutraliza evidence against a claim para no restringir ese alcance.

### q-v1-006

**Explícita:** If all other inputs remain unchanged, how does increasing the confidence level from 90% to 95% affect the width of the confidence interval, and why?

**Implícita:** If all other inputs remain unchanged, how does increasing the confidence level from 90% to 95% affect the width of the range estimated from sample data for a population parameter, and why?

**Referencia:** The 95% confidence interval is wider than the 90% interval because greater confidence requires an interval that covers a larger range of plausible values for the population parameter.

**Comprobación:** El ejemplo y explicación sostienen mayor anchura a mayor confianza, manteniendo constantes los demás parámetros.

### q-v1-012

**Explícita:** With confidence level and population variability held constant, how does a larger sample affect the error bound and the width of a confidence interval?

**Implícita:** With confidence level and population variability held constant, how does a larger sample affect the error bound and the width of the range estimated from sample data for a population parameter?

**Referencia:** A larger sample decreases the error bound and therefore makes the confidence interval narrower, provided that the confidence level and population variability remain fixed.

**Comprobación:** El resumen explicita menor margen y menor anchura al aumentar n bajo condiciones constantes.

### q-v1-014

**Explícita:** What sequence should be followed to flag unusually low or high observations using the interquartile range of an ordered dataset?

**Implícita:** What sequence should be followed to flag unusually low or high observations using the middle 50% of an ordered dataset?

**Referencia:** Order the data and determine the first and third quartiles. Compute the interquartile range as the difference between the third and first quartiles, use the quartiles and a 1.5-IQR cutoff to define lower and upper bounds, and flag values below the lower bound or above the upper bound for further investigation.

**Comprobación:** Los dos chunks sustentan cuartiles, IQR, límites, factor 1.5 e investigación de atípicos. Las fórmulas simbólicas no aparecen en el texto extraído: la referencia verbal se mantiene; no exigir fórmulas exactas como nueva obligación.

### q-v1-016

**Explícita:** How do discrete random variables associated with counting differ from continuous random variables associated with measurement in the kinds of numerical values they can take?

**Implícita:** How do count-based outcomes differ from measurement-based outcomes in the kinds of numerical values they can take?

**Referencia:** A discrete random variable takes a finite or countably infinite set of distinct values and typically results from counting. A continuous random variable can take any value within an interval and typically results from measurement.

**Comprobación:** El chunk contrasta valores contables con cualquier valor de un intervalo y describe conteo/medición como casos típicos, no equivalencias universales.

## Ajuste de 003

Se sustituye “determine whether sample data provide sufficient evidence against a claim” por “evaluate a claim ... using sample data”. La evidencia indica que la afirmación puede corresponder a la hipótesis nula o a la alternativa; pedir solo evidencia en contra restringía innecesariamente ese alcance.

## Revisión separada de 013

La redacción corregida conserva la misma referencia y evidencia según revisión del asistente. No se incluye en las parejas. La versión v1.1 mantiene el estado draft de este registro hasta cerrar la revalidación conforme al protocolo; no se atribuyen juicios antiguos a la nueva redacción.

## Límites

Explicitud relativa al concepto objetivo, no eliminación de todo vocabulario técnico. La descripción puede alterar longitud y carga lingüística; no interpretar el contraste como un cambio léxico puro. Las preguntas 006 y 012 pertenecen a un mismo ámbito y el tamaño del conjunto limita la generalización. En 014 hay fórmulas ausentes del texto extraído, por lo que se mantiene la referencia verbal sin añadir exigencias algebraicas. La unidad de comparación es la pregunta base.

## Próxima operación

Fijar configuración de ejecución y obtener rankings de ambas formulaciones bajo las cuatro estrategias; revisar el pool incremental antes de evaluar. Mantener generación y cualquier llamada de pago fuera de esta fase.
