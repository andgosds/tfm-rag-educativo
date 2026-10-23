# Lote 3 — Reutilizaciones en formulación alternativa (39 unidades)

> Revisión guiada por pregunta base. Cada unidad muestra el fragmento, el grado histórico (adjudicado por Andrés para la formulación original) y la propuesta del asistente para la formulación alternativa. **Nada se convierte en qrels v2 sin tu confirmación.**

## Cómo revisar

Para cada unidad confirma una de estas decisiones:

- **Reutilizar** el grado histórico (el fragmento sigue siendo relevante para la formulación implícita).
- **Cambiar grado** (indica 0/1/2).
- **No reutilizar** (el juicio histórico no se traslada; la unidad pasará a revisión en su formulación alternativa).

Propongo avanzar **por pregunta base completa**: confirmas las 9 de q-v1-002 como grupo y seguimos con la siguiente.

---

## q-v1-002 — 9 unidades

**Formulación explícita (original):** How do Type I and Type II errors differ in terms of the truth of the null hypothesis and the decision made?
**Formulación implícita (a validar):** In hypothesis testing, what are the two ways a decision about the null hypothesis can be wrong, considering whether that hypothesis is actually true or false?
**Respondible, comparativa.** Respuesta de referencia: A Type I error occurs when a true null hypothesis is rejected. A Type II error occurs when a false null hypothesis is not rejected.

| # | chunk_id | Grado hist. | Fragmento (síntesis) | Propuesta |
|---|---|---|---|---|
| 1 | openstax_intro_stats_2e:9.2:chunk-001 | **2** (canónico) | Tabla de los cuatro resultados: decisiones frente a verdad de H0, define Type I y Type II error. | Reutilizar 2 |
| 2 | openstax_intro_stats_2e:9.2:chunk-002 | **2** | Define α y β como probabilidades de los errores Tipo I y II; ejemplos. | Reutilizar 2 |
| 3 | openstax_intro_stats_2e:9.2:chunk-003 | **2** | Ejemplos 9.6/9.8 con definiciones explícitas de Type I y Type II en contexto. | Reutilizar 2 |
| 4 | openstax_intro_stats_2e:9.5:chunk-005 | **2** | Ejemplo de decisión con p-value; contexto de rechazo de H0, error enmarcado. | Reutilizar 2 |
| 5 | openstax_intro_stats_2e:9.1:chunk-001 | **1** | Define H0 y Ha; sin mención a errores Tipo I/II. Contexto previo necesario. | Reutilizar 1 |
| 6 | openstax_intro_stats_2e:9.3:chunk-001 | **1** | Ejemplo 9.8 (cura ≥75%): describe ambos errores en contexto. | Reutilizar 1 |
| 7 | openstax_intro_stats_2e:9.5:chunk-015 | **1** | Ejemplo con calculadora; enuncia Type I y Type II para proporción de bodas. | Reutilizar 1 |
| 8 | openstax_intro_stats_2e:9.4:chunk-006 | **1** | Reglas de decisión α vs p-value; sin nombrar errores Tipo I/II. | **Revisar** — aporta decisión, no la taxonomía de los dos errores; relevancia se degrada a 1 contextual o 0 |
| 9 | openstax_principles_ds:4.2:chunk-007 | **1** | Plantea H0/Ha y las dos únicas decisiones posibles; menciona posibilidad de decisión errónea sin nombrar los errores. | **Revisar** — hablaba del marco de decisión; para "dos formas de equivocarse" es contexto débil; propone 1 |

**Mi lectura global de la pregunta:** la formulación implícita ("las dos formas en que una decisión puede ser errónea") **preserva el contenido de la pregunta original**: los dos errores son Type I y Type II, y los chunks canónicos 9.2 los definen directamente. Las seis unidades con mención explícita de Type I/II se reutilizan sin riesgo. Las unidades 8 y 9 son las únicas con equivalencia dudosa: siguen siendo contexto relacionado (decisión sobre H0), pero no aportan la distinción que pregunta la versión implícita. **Propuesta: reutilizar las 7 primeras con su grado, y degradar 9.4:chunk-006 a grado 1 (se mantiene como contexto, no como pieza de respuesta) y 4.2:chunk-007 a grado 1.** Si prefieres conservar los grados históricos tal cual para no alterar la comparación emparejada, también es defendible: el efecto en métricas sería mínimo y queda documentado.

---

### Pendientes después de q-v1-002

q-v1-001 (8), q-v1-012 (5), q-v1-016 (5), q-v1-003 (4), q-v1-006 (4), q-v1-014 (4).
