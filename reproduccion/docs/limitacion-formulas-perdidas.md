# Fórmulas perdidas en la extracción del corpus

**Fecha:** 2026-09-23
**Estado:** limitación conocida y cuantificada. No se corrige; se declara.

## Qué ocurre

La conversión de los manuales de OpenStax a texto plano **pierde en ocasiones el contenido
matemático**, dejando el rastro de la fórmula sin la fórmula. Los síntomas característicos son
líneas que terminan en un signo igual sin nada a continuación, o enunciados del tipo
`f(x) =` seguidos de blanco.

Afecta por igual a los dos manuales del corpus. No es un error del *chunking*: la fórmula ya
había desaparecido antes de segmentar, en el paso de extracción. La normalización de MathML
del *pipeline* preserva lo que recibe; lo que se pierde es lo que nunca llega a ella.

## Cuantificación

| Magnitud | Valor |
|---|---|
| Chunks del corpus | 288 |
| **Chunks con señal de fórmula perdida** | **20 — 6,9 %** |
| Unidades de qrels tocadas | 50 / 578 — 8,7 % |
| De ellas, de grado 2 | 14 |
| Preguntas con evidencia de grado 2 afectada | 10 |

El sesgo **no es simétrico**: las unidades sobre chunks marcados tienen un 28 % de grado 2,
frente al 19 % del resto. Los fragmentos que perdieron fórmulas son los que contenían más
evidencia relevante, porque la matemática es donde suele estar la respuesta.

Preguntas con evidencia de grado 2 tocada: `q-v1-001`, `q-v1-003`, `q-v1-006`, `q-v1-011`,
`q-v1-012`, `q-v1-013`, `q-v1-020`, `q-v3-001`, `q-v3-002`, `q-v3-005`.

## Por qué no se corrige

Re-extraer con conservación de fórmulas arreglaría la causa, pero **invalidaría el *chunking*
y todo lo que cuelga de él**: los 578 pares gradados, el *pool* de relevancia, los qrels y las
métricas. La corrección de una pérdida de precisión absoluta pondría en riesgo el cierre de la
memoria sin alterar las conclusiones del trabajo.

## Efecto sobre la validez

**La comparación entre técnicas de IR no se ve afectada.** Las cuatro estrategias se enfrentan
al mismo corpus, con los mismos huecos: si un método falla en un fragmento sin fórmula, fallan
todos. Lo que se distorsiona es el **valor absoluto** de las métricas, no el **ranking** de
estrategias, y el ranking es lo que responde a la pregunta de investigación.

Conviene por tanto:

- reportar las métricas de recuperación como **estimaciones por defecto** del rendimiento real;
- no comparar estos valores absolutos con los de otros trabajos sobre corpus sin degradar;
- declarar el efecto en *amenazas a la validez*, con la cuantificación de esta nota.

## Rastro

- Detección: `scripts/` — barrido por patrón sobre `data/processed/chunks_v1.jsonl`.
- Casos que lo hicieron visible en la gradación: unidades de `q-v1-008`, `q-v1-012` y `q-v1-014`,
  donde los jueces señalaron literalmente «la fórmula ausente» en su razonamiento.
- Decisión de no corregir: usuario, 2026-09-23.
