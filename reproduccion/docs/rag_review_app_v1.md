> **Recetas desde la raíz del paquete v2.** Los resultados descritos son históricos. Para operaciones de escritura usar destinos nuevos bajo `outputs/local_runs/`; los defaults congelados se rechazan. Recetas vigentes seguras: `standalone_operations.md`. No ejecutar inferencia mientras siga abierta la adjudicación.

# Aplicación local de auditoría humana de respuestas RAG

## Finalidad

La aplicación permite adjudicar la cola de riesgo generada al comparar **Gemma 3 4B** y **GLM 5.3 Flash (low)**. Presenta una pregunta por pantalla y, cuando existen ambas, coloca las respuestas de **RRF** y **RRF + reranking** en paralelo.

La decisión humana se guarda como una capa independiente en `human_adjudication`. Las respuestas, los contextos, las citas y las puntuaciones automáticas no se modifican.

## Ejecución

Desde la raíz del TFM:

```bash
uv run python scripts/rag_review_app.py
```

La aplicación escucha únicamente en `http://127.0.0.1:8766` y abre el navegador por defecto. Para no abrirlo automáticamente:

```bash
uv run python scripts/rag_review_app.py --no-browser
```

El archivo de trabajo predeterminado es:

```text
outputs/rag_eval/rag_judge_sensitivity_gemma3_4b_vs_glm53flash_low_human_risk_queue_v1_22q.jsonl
```

La ruta puede cambiarse con `--input`. El identificador del revisor se establece con `--reviewer-id` y su valor predeterminado es `andres`.

## Unidad de revisión

La pantalla agrupa la cola por `qid`. Cada condición presente conserva su propia adjudicación, porque RRF y reranking pueden producir respuestas distintas. Al guardar, todas las condiciones visibles del qid se validan primero y se escriben juntas mediante sustitución atómica del JSONL.

La aplicación reanuda el trabajo desde los casos cuyo estado sigue siendo `pending`. El filtro permite mostrar pendientes, revisados o todos los casos.

## Decisiones humanas

### Faithfulness

- `supported`: las afirmaciones verificables están respaldadas por los contextos recuperados.
- `partially_supported`: existe una combinación relevante de afirmaciones respaldadas y no respaldadas.
- `unsupported`: la respuesta introduce afirmaciones centrales sin apoyo en los contextos.
- `not_applicable`: no hay afirmaciones factuales que evaluar, como puede ocurrir en una abstención breve.

### Factual Correctness

- `correct`: la respuesta coincide sustancialmente con la referencia o con la corrección fundamentada esperada.
- `partially_correct`: contiene información correcta, pero omite o distorsiona un elemento relevante.
- `incorrect`: la conclusión central es errónea.
- `not_applicable`: no procede evaluar corrección factual, normalmente por tratarse de una abstención sin respuesta sustantiva.

### Conducta

- `0`: conducta incorrecta respecto al comportamiento esperado.
- `1`: cumplimiento parcial.
- `2`: cumplimiento pleno.

Las notas son opcionales, pero deben justificar desacuerdos con los jueces, valoraciones parciales y decisiones metodológicamente sensibles.

## Guardado y recuperación

Cuando las tres decisiones están completas en todas las condiciones visibles, el autosave se activa después de 700 ms sin avanzar de pregunta. **Guardar qid y siguiente** realiza la misma escritura y avanza al siguiente caso.

El servidor:

1. comprueba que el qid existe;
2. exige exactamente las condiciones presentes en la cola;
3. valida las etiquetas y la puntuación de conducta;
4. incorpora `reviewer_id` y `reviewed_at`;
5. escribe un archivo temporal y lo sustituye atómicamente.

**Deshacer** restaura el último estado guardado durante la sesión del navegador. **Dejar qid pendiente** borra únicamente la adjudicación humana del qid. **Exportar JSONL** descarga el archivo de trabajo actual.

## Atajos

| Atajo | Acción |
|---|---|
| `0`, `1`, `2` | Asignar conducta a la condición activa |
| `N` | Enfocar las notas de la condición activa |
| `Enter` | Guardar el qid y avanzar |
| `←`, `→` | Navegar entre qids visibles |
| `U` | Deshacer el último guardado de la sesión |
| `Esc` | Salir del control activo |

La condición activa es la última tarjeta sobre la que se hizo clic.

## Verificación

Pruebas específicas:

```bash
uv run pytest -q tests/test_rag_review_app.py
```

Suite completa:

```bash
uv run pytest -q tests
```

Para probar escrituras sin alterar la cola canónica, debe pasarse una copia del JSONL mediante `--input`.
