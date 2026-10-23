> **Recetas desde la raíz del paquete v2.** Los resultados descritos son históricos. Para operaciones de escritura usar destinos nuevos bajo `outputs/local_runs/`; los defaults congelados se rechazan. Recetas vigentes seguras: `standalone_operations.md`. No ejecutar inferencia mientras siga abierta la adjudicación.

# Protocolo de anotación del golden set piloto v1

## Propósito y alcance

El golden set permite evaluar si cada técnica de recuperación encuentra la evidencia necesaria y si esa evidencia sustenta una respuesta correcta. El piloto servirá para validar el procedimiento antes de ampliar el conjunto definitivo.

Las anotaciones están vinculadas a:

- corpus: `corpus_v1`;
- colección: `data/processed/chunks_v1.jsonl`;
- chunking: `section_paragraphs_300w_overlap60_v1`;
- esquema: `config/golden_set_schema_v1.json`.

Si cambia la segmentación, los identificadores y los juicios de relevancia dejan de ser directamente reutilizables.

## Unidad de anotación

Cada línea de `golden_set_pilot_v1.jsonl` representa una pregunta. La pregunta se vincula con uno o más chunks positivos y conserva una respuesta breve, citas textuales y notas de decisión.

El tipo de pregunta y su respondibilidad son dimensiones independientes. Una pregunta factual puede ser no respondible con este corpus y debe conservar el tipo `factual` junto con `answerability = unanswerable`.

## Tipos de pregunta

| Tipo | Criterio | Ejemplo de operación cognitiva |
|---|---|---|
| `factual` | Solicita un dato, propiedad o definición explícita | Identificar el valor de un parámetro |
| `explanatory` | Exige explicar una relación, causa o interpretación | Explicar por qué cambia una distribución |
| `comparative` | Contrasta al menos dos conceptos o métodos | Comparar dos procedimientos |
| `procedural` | Solicita una secuencia o criterio de aplicación | Describir cómo estandarizar una variable |

Las preguntas deben poder comprenderse sin conocer el índice del libro. Se evitarán formulaciones como «según el párrafo anterior» y pistas textuales artificiales copiadas del encabezado.

## Respondibilidad

### Pregunta respondible

Una pregunta es `answerable` cuando el corpus contiene evidencia suficiente para construir la respuesta sin recurrir a conocimiento externo. Requiere:

- una respuesta de referencia breve;
- `evidence_sufficient = true`;
- al menos un chunk con grado 2;
- al menos un chunk canónico.

### Pregunta no respondible

Una pregunta es `unanswerable` cuando el corpus no contiene evidencia suficiente, aunque el tema pueda parecer relacionado. Requiere:

- `gold_answer = null`;
- `answer_language = null`;
- `evidence_sufficient = false`;
- ausencia de evidencia directa o canónica;
- una nota que explique el límite del corpus.

Las preguntas no respondibles forman parte obligatoria del piloto porque el diseño evalúa abstención y resistencia a responder sin evidencia. Su inclusión debe mantener plausibilidad temática y no limitarse a preguntas absurdas o claramente ajenas al corpus.

Cada pregunta no respondible se clasificará en una de estas categorías:

| Categoría | Criterio |
|---|---|
| `out_of_scope` | El tema queda fuera del dominio delimitado por el corpus |
| `nonexistent_entity_or_concept` | La consulta introduce una entidad o concepto inexistente |
| `false_premise` | La pregunta presupone como cierto algo incompatible con el corpus |
| `missing_evidence` | El tema es pertinente, pero la evidencia necesaria no aparece |
| `insufficient_evidence` | Existe información relacionada, pero no basta para responder con rigor |

## Escala de relevancia

| Grado | Definición operacional | Uso |
|---:|---|---|
| 2 | El chunk contiene evidencia directamente útil y suficiente, por sí solo o junto con otros chunks de grado 2 | Qrel positivo fuerte |
| 1 | El chunk aporta contexto relacionado, pero no permite responder de forma suficiente | Qrel positivo débil |
| 0 | El chunk no contribuye a responder la pregunta | Juicio negativo durante pooling o auditoría |

El archivo principal conserva únicamente evidencias de grado 1 y 2. Los grados 0 se incorporarán al evaluar candidatos recuperados o construir un pool de juicios; no se almacenan como evidencia positiva.

Para las métricas binarias de recuperación se adopta un criterio estricto: Recall@k y MRR@k consideran relevante únicamente un chunk de grado 2. Los chunks de grado 1 aportan contexto relacionado, pero no cuentan como recuperación de evidencia suficiente. nDCG@k mantiene la escala graduada completa 0/1/2 para valorar tanto la utilidad parcial como la evidencia directa.

## Evidencia canónica y redundancia

`is_canonical = true` identifica el conjunto mínimo preferido de chunks con el que puede elaborarse la respuesta de referencia. Toda evidencia canónica debe tener grado 2.

Una pregunta simple puede tener un único chunk canónico. Una pregunta comparativa o una explicación distribuida puede necesitar varios. Otros chunks solapados pueden tener grado 2 sin ser canónicos cuando repiten la misma evidencia y no son necesarios para el conjunto mínimo.

Cada evidencia debe contener:

- `chunk_id`: identificador exacto de `chunks_v1.jsonl`;
- `quote`: cita literal incluida en el campo `text` del chunk;
- `supports`: explicación breve de qué parte de la respuesta respalda;
- grado e indicación de canonicidad;
- información sobre verificación de la fuente cuando proceda.

## Respuesta de referencia

La respuesta debe ser breve, autosuficiente y proporcional a la pregunta. Se redactará solo con afirmaciones respaldadas por la evidencia canónica. No debe copiar innecesariamente un párrafo completo ni introducir explicaciones externas para hacerla más elegante.

El piloto se redactará íntegramente en inglés. Tanto `question_language` como `answer_language` serán `en` en las preguntas respondibles. Este control evita introducir todavía el multilingüismo como factor de confusión.

## Fórmulas y extracción degradada

Los chunks con `formula_risk = true` no se excluyen automáticamente, pero requieren comprobación en el PDF o en la versión web oficial. En ese caso:

- `source_verified = true`;
- `verification_note` registra la fuente y página consultada;
- la fórmula no se reconstruye a partir de una conjetura;
- si la comprobación no resuelve la ambigüedad, la pregunta no se incorpora.

Para chunks sin riesgo detectado, `source_verified` puede mantenerse en `false` y `verification_note` vacío.

## Procedencia y revisión

`question_origin` distingue:

- `human`: pregunta redactada directamente por una persona;
- `llm_assisted`: propuesta o reformulación producida con apoyo de un LLM.

Toda pregunta asistida por LLM requiere revisión humana de redacción, respuesta y evidencia. La procedencia no modifica el grado de relevancia, pero permite documentar posibles sesgos de generación.

Las revisiones automáticas se almacenan en `reviews`. Cada modelo lingüístico usado como juez registra identificador del revisor, modelo y versión, configuración de inferencia cuando sea relevante, versión del prompt, fecha de ejecución, decisión sobre respondibilidad, suficiencia de la evidencia, calidad de la respuesta de referencia, justificación y confianza declarada. En la primera revisión, `model_version` conserva `openai-codex/gpt-5.6-sol; reasoning_effort=high`, de modo que el esfuerzo de razonamiento no se confunda con el identificador base del modelo. Los modelos actúan como revisores auxiliares: no modifican directamente la etiqueta oro. El prompt reproducible se conserva en `config/golden_set_review_prompt_v1.md`.

La decisión final se conserva en `human_adjudication`. Andrés actúa como revisor y adjudicador humano, examina los desacuerdos entre modelos y acepta, revisa o excluye el registro. Los juicios de los LLM se analizan como apoyo y señal de dificultad, no como acuerdo interanotador humano.

Estados del registro:

1. `draft`: primera anotación, todavía sin decisión final.
2. `reviewed`: al menos un LLM-as-judge y una revisión humana.
3. `adjudicated`: al menos dos LLM-as-judge y decisión humana final.

No se informará acuerdo interanotador humano porque solo habrá un adjudicador humano. Podrá calcularse concordancia entre jueces automáticos como diagnóstico, indicando con claridad su naturaleza y sus limitaciones.

## Flujo de anotación

1. Seleccionar una sección y revisar sus chunks dentro del documento fuente.
2. Formular una pregunta natural sin copiar una frase completa de la evidencia.
3. Clasificar su tipo y declarar el idioma.
4. Redactar la respuesta utilizando únicamente evidencia verificable.
5. Identificar todos los chunks de grado 2 y los chunks de grado 1 conocidos.
6. Marcar el conjunto canónico mínimo.
7. Copiar citas literales y explicar qué respalda cada una.
8. Comprobar fórmulas contra la fuente cuando exista riesgo.
9. Ejecutar el validador.
10. Revisar la anotación sin consultar el ranking de un recuperador concreto.

La anotación inicial se realiza antes de ejecutar BM25, dense retrieval, híbrido o reranking. Así se reduce el riesgo de favorecer a una técnica concreta. Después podrán ampliarse los juicios mediante pooling de resultados, conservando la procedencia de las nuevas decisiones.

## Criterios de exclusión

Se excluirá una pregunta cuando:

- dependa de una fórmula que no pueda verificarse;
- sea ambigua incluso después de revisar el contexto;
- necesite conocimiento externo no declarado;
- replique otra pregunta sin aportar una operación distinta;
- solo pueda responderse gracias a una pista literal artificial;
- mezcle varias preguntas independientes;
- su respuesta requiera un cálculo complejo ajeno al objetivo de retrieval.

## Control de calidad del piloto

Antes de ampliar el conjunto se comprobará:

- validez estructural y existencia de todos los chunk_id;
- unicidad de qid y de chunks dentro de cada evidencia;
- citas literales presentes en el texto de origen;
- respuesta completamente respaldada por el conjunto canónico;
- equilibrio razonable por tipo, fuente y capítulo;
- ausencia de dependencia inadvertida de chunks con fórmulas degradadas;
- distribución de preguntas sin predominio de coincidencias léxicas triviales;
- revisión de todos los registros antes de calcular métricas definitivas.

## Validación

Desde la raíz del proyecto:

```bash
uv run python scripts/validate_golden_set.py \
  data/golden/golden_set_pilot_v1.jsonl \
  --chunks data/processed/chunks_v1.jsonl
```

El comando devuelve código 0 solo si todos los registros cumplen las reglas y todas las evidencias apuntan a chunks existentes.
