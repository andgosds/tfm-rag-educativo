# Lote 3 — q-v1-016 (5 unidades, formulación alternativa)

**Formulación explícita (original):** How do discrete random variables associated with counting differ from continuous random variables associated with measurement in the kinds of numerical values they can take?
**Formulación implícita (a validar):** How do count-based outcomes differ from measurement-based outcomes in the kinds of numerical values they can take?
**Respondible, comparativa.** Respuesta de referencia: una variable aleatoria discreta toma un conjunto finito o numerable de valores distintos (típicamente de contar); una continua puede tomar cualquier valor de un intervalo (típicamente de medir).

**Lectura de equivalencia:** la implícita sustituye la terminología técnica ("discrete/continuous random variables") por "count-based / measurement-based outcomes". **Es la paráfrasis más fuerte del lote**: elimina el término técnico que el corpus usa constantemente. La pregunta conserva el contenido (qué valores pueden tomar), pero lexicalmente se aleja del corpus. Eso hace *más* interesante evaluarla, no menos válida: los chunks que definen la distinción siguen siendo los mismos.

| # | chunk_id | Grado hist. | Contenido | Propuesta |
|---|---|---|---|---|
| 1 | openstax_principles_ds:3.5:chunk-002 | **2** | Define variable aleatoria; ejemplos con valores asignados a resultados. Base de la taxonomía. | Reutilizar 2 |
| 2 | openstax_principles_ds:3.5:chunk-003 | **2** | Resumen literal: discretas = finito/numerable de valores distintos; continuas = cualquier valor de un intervalo; medición → continua. | Reutilizar 2 |
| 3 | openstax_principles_ds:3.5:chunk-005 | **2** | Ejemplo de lluvia como continua; distribución binomial/Poisson para discretas. | Reutilizar 2 |
| 4 | openstax_principles_ds:3.5:chunk-006 | **2** | Requisitos del experimento binomial; conteo de éxitos. Es contexto de "counting" pero no contrasta con medición. | Reutilizar 2 (la más discutible: ya era generosa) |
| 5 | openstax_principles_ds:3.5:chunk-007 | **2** | "X cuenta el número de éxitos… no puede ser 5.28 porque cuenta personas": ilustra por qué contar → valores discretos. | Reutilizar 2 |

**Propuesta: reutilizar las 5 con sus grados históricos.** La unidad 4 (binomial, requisitos) era ya la más contextual; conservarla mantiene la paridad con la adjudicación original. Degradarla a 1 sería defendible pero cambiaría el criterio a mitad de campaña.

**Nota metodológica para la memoria:** esta pregunta es el caso donde la formulación implícita más se aleja léxicamente del corpus; conviene señalarlo al interpretar la caída esperada de BM25 frente a dense en la comparación emparejada.
