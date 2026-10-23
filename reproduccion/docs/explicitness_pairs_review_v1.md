# Revisión delegada de parejas de explicitud

Esta revisión complementa y actualiza las propuestas del borrador; no sustituye el golden set original. Las decisiones del asistente no se registran como adjudicaciones humanas. La revisión de qrels y candidatos nuevos sigue pendiente.

| Pregunta | Decisión | Motivo |
|---|---|---|
| q-v1-001 | retain_human_accepted | Se conserva la aceptación humana de la formulación ajustada. |
| q-v1-002 | accept_assistant | Misma distinción entre verdad y decisión; no exigir los nombres de los errores como condición adicional. |
| q-v1-003 | accept_adjusted_assistant | Se elimina decidir si rechazar la afirmación genérica; se pide el procedimiento para evaluar evidencia contra una afirmación poblacional. |
| q-v1-004 | exclude_assistant | La descripción revela el mecanismo de robustez solicitado y simplifica el caso par. |
| q-v1-005 | exclude_assistant | Medida numérica de asociación no identifica de forma suficiente el coeficiente buscado. |
| q-v1-006 | accept_assistant | Conserva nivel, porcentajes y condiciones; no revela dirección del cambio. Explicitud relativa a confidence interval. |
| q-v1-011 | exclude_assistant | La definición sustitutiva entrega parte sustancial de la interpretación solicitada. |
| q-v1-012 | accept_assistant | Conserva condiciones y efectos solicitados; no revela dirección del cambio. |
| q-v1-013 | needs_user_decision | El original ya proporciona Student t como parte de la respuesta pedida. Retirarlo mezcla explicitud y eliminación de una pista de respuesta. |
| q-v1-014 | accept_assistant | Conserva procedimiento y objeto; ninguna versión proporciona factor 1.5 ni límites. |
| q-v1-015 | exclude_assistant | Las descripciones entregan mecanismos de robustez y alteran mucho longitud y carga informativa. |
| q-v1-016 | accept_assistant | Conserva conteo/medición y valores posibles; explicita nombres sin proporcionar la respuesta sobre el conjunto de valores. |
| q-v1-017 | exclude_assistant | Describir el contraste por su uso responde parcialmente a cuándo procede y no identifica ANOVA de forma única. |

## Formulación ajustada de q-v1-003

What sequence of steps should be followed to determine whether sample data provide sufficient evidence against a claim about a population?

Se conserva la petición de un procedimiento general. La referencia sigue siendo candidata compatible según revisión del asistente; no se afirma validación independiente.

## Pendiente de decisión: q-v1-013

Recomendación: excluir del contraste principal de explicitud. El original menciona Student t mientras pide identificar la distribución, de modo que la alternativa retira una pista de respuesta. Si se conserva, presentarla como diagnóstico separado de sensibilidad a pistas, no mezclarla silenciosamente con pares sin filtración.

## Estado de ejecución

No se han ejecutado recuperación ni generación. La aceptación de formulación no autoriza reutilizar automáticamente qrels ni heredar adjudicaciones. Antes de ejecutar, congelar parejas, revisar evidencia y cerrar el protocolo.
