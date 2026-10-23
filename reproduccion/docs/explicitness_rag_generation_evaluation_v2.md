> **Recetas desde la raíz del paquete v2.** Las salidas de esta fase viven en `outputs/local_runs/`; no se sobrescriben artefactos históricos ni se toca `v1/`. Este documento registra una ejecución real, no un plan.

# Cierre de fase: generación y evaluación RAG de explicitness v2

## Resultado verificado

Se generaron y evaluaron respuestas para las catorce formulaciones de las siete preguntas base bajo las cuatro condiciones de recuperación (BM25, dense E5, RRF, RRF+reranking), con top-5 de contexto. **55 unidades aceptadas y 1 fallida = 56 cubiertas.** La unidad fallida, `rerank / q-v1-006__explicit`, queda separada, documentada y **no se puntúa**.

La evaluación automática puntuó las 55 respuestas aceptadas. Una **cola de riesgo de 16 pares** fue revisada y confirmada por el usuario el 2026-09-21; las 39 restantes conservan al juez principal. Los campos automáticos quedan intactos y los finales se derivan solo sobre las claves revisadas.

## Configuración congelada

**Generador:** `qwen3.5:9b` por Ollama local (sin API de pago), temperatura 0, semilla 20260902, `top_k=5`, prompt `rag_answer_prompt_v1`, máximo 3 intentos correctivos por unidad con validación estricta de citas contra los contextos suministrados.

**Juez:** `gemma3:4b` (digest `a2af6cc3eb7f…`), distinto del generador, mediante RAGAS 0.4.3. `ragas_max_tokens=1024`, `behavior_max_tokens=250`, rúbrica `rag_behavior_rubric_v1`. Dos repeticiones de humo idénticas antes del lote: Faithfulness 1.0, Corrección factual 1.0, Conducta 2, sin errores en ambas.

**Orden:** por `qid` y luego condición; entrada intercalada en `campaign_input_interleaved.jsonl` (sha256 `cf4436fded5d…`). Generación en ejecución secuencial con reanudación.

## Generación

| Condición | Aceptadas | Fallidas |
|---|---:|---:|
| BM25 | 14 | 0 |
| Dense E5 | 14 | 0 |
| RRF | 14 | 0 |
| RRF + reranking | 13 | 1 |

Se conservaron byte a byte las 48 respuestas preexistentes y se generaron las siete posteriores pendientes. La reanudación se verificó con un generador que falla si es invocado: cero llamadas en las cuatro condiciones sobre lo ya completado.

**La unidad fallida.** `rerank / q-v1-006__explicit` incumplió el contrato de citas en tres intentos: el modelo emitió `[openstax_principles_ds:4.1:chunk-010]` con corchetes sobre un identificador que sí estaba en el top-5. Es un incumplimiento literal de formato, **no una cita a un chunk inventado**. No se normalizó la cita ni se cambiaron prompt, semilla, modelo, top-k ni límite de intentos. Los raw de los seis intentos históricos no son recuperables y se registran como `null`, sin reconstruir.

## Evaluación automática y adjudicación humana

La cola de riesgo se construyó por cuatro motivos: etiqueta de conducta desalineada, reintento de generación, error de métrica y puntuación baja. Los 16 pares se revisaron con texto completo (pregunta, referencia, respuesta, citas, contexto, puntuaciones y rationale del juez) y se confirmaron cuatro decisiones:

| Decisión | Casos | Efecto |
|---|---:|---|
| Reclasificar conducta `grounded_correction` → `answer` | 10 | Solo etiqueta; puntuaciones intactas |
| Confirmar fallo por abstención no justificada | 1 | Conducta 0, se mantiene |
| Aceptar respuesta tras reintento correctivo | 2 | Ninguno |
| Registrar Faithfulness como no disponible | 7 de 55 | Sin sustituir por 0 |

Las **diez reclasificaciones** son un artefacto del juez de conducta: etiquetó `grounded_correction` contestaciones directas y correctas, sin corrección de presupuesto alguno, mientras su propio rationale las calificaba de «substantively correct answer consistent with the reference».

El **único fallo genuino** es `dense / q-v1-016__implicit`: la respuesta se abstuvo («I cannot answer from the supplied contexts») pese a que RRF y reranking contestan la misma pregunta con el mismo corpus y el mismo top-5. Se verificó el contexto suministrado: los cuatro chunks pertenecen a la sección 3.5 sobre distribuciones discretas y continuas y contienen la distinción pedida. La abstención no está justificada y las puntuaciones 0/0/0 se confirman. Matiz de trazabilidad: el rationale del juez describe «información de fondo extensa» que no aparece en la respuesta final, señal de que se redactó sobre un intento previo; la puntuación sí corresponde a la respuesta final.

**Faithfulness quedó sin calcular en 7 de 55 filas** por error de la métrica de RAGAS; solo 48 tienen valor numérico. Se registran como métrica ausente con su error asociado, nunca como 0. Cuatro de esas siete entraron en la cola por `reported_behavior_mismatch` y no por `evaluation_errors`, por lo que el recuento se deriva de los scores y no de los motivos de riesgo.

### Resultados consolidados (campos finales)

| Condición | Faithfulness | Corrección factual | Conducta | Citas válidas |
|---|---:|---:|---:|---:|
| BM25 | 1.000 (n=12) | 0.927 | 2.00 | 1.00 |
| Dense E5 | 0.923 (n=13) | 0.859 | 1.86 | 0.93 |
| RRF | 0.972 (n=12) | 0.936 | 2.00 | 1.00 |
| RRF + reranking | 0.985 (n=11) | 0.953 | 2.00 | 1.00 |

Diferencias emparejadas implícita − explícita sobre conducta final: BM25 0.000, RRF 0.000, reranking 0.000 y **dense −0.286** (n=6–7 parejas por condición).

## Estado epistemológico y límites

- El juez local es **diagnóstico, no verdad humana**: un modelo pequeño de 4B. Los valores sirven para trazar comparaciones entre condiciones, no como magnitudes absolutas defendibles. La auditoría de riesgo aporta valor humano solo sobre las 16 claves revisadas.
- La cola de riesgo es una **muestreo dirigido por riesgo**; el estado del artefacto es `human_adjudicated_not_population_estimate`. El acuerdo sobre esos 16 pares **no es una estimación de precisión poblacional**.
- `faithfulness` con n=5–7 por celda: las diferencias pequeñas en esa métrica no son interpretables como efecto.
- Citas válidas comprueban **perteneția al top-5**, no soporte semántico de la afirmación.
- La generación se ejecutó de forma secuencial con reanudación; el orden temporal y el digest actual del modelo no acreditan retrospectivamente el digest de la generación histórica.
- La campaña no incluye abstención justificada ni corrección de falso presupuesto como conductas esperadas: todas las preguntas eran respondibles (`expected_behavior=answer`).
- Coste: modelo local, sin cargo de API; se conservan tokens y latencias, no euros.

## Comandos reproducibles

Desde la raíz `v2`:

```bash
# Generación (idempotente: reanuda sin repetir completados ni reintentar fallos).
../.venv/bin/python scripts/run_rag_generation.py --experiment-id rag_explicitness_v2_bm25_top5 --retrieval-condition bm25

# Evaluación RAGAS local con juez gemma3:4b (tras humo doble).
environments/rag/.venv/bin/python outputs/local_runs/rag_explicitness_eval_gemma3_v2/run_campaign.py

# Consolidación de la adjudicación humana (determinista).
../.venv/bin/python scripts/consolidate_rag_adjudication.py \
  --scores outputs/local_runs/rag_explicitness_eval_gemma3_v2/scores.jsonl \
  --adjudications outputs/local_runs/rag_explicitness_eval_gemma3_v2/adjudication/rag_adjudications_v2.jsonl \
  --summary outputs/local_runs/rag_explicitness_eval_gemma3_v2/adjudication/rag_adjudication_summary.json

# Verificación read-only de reanudación y suite completa.
.venv/bin/python outputs/local_runs/rag_explicitness_v2/verify_resume.py   # desde TFM
../.venv/bin/python -m pytest tests -q
```

Resultado de la suite: **163 tests passed**. Incluye 7 pruebas del consolidador, con verificación de regeneración determinista (dos ejecuciones producen bytes idénticos).

## Artefactos y hashes

| Artefacto | sha256 (abreviado) |
|---|---|
| `rag_explicitness_v2/completion_audit.json` | `29d07dc3c68c55c0` |
| `rag_explicitness_eval_gemma3_v2/evaluation_config.json` | `80289758ca44d560` |
| `rag_explicitness_eval_gemma3_v2/adjudication/rag_adjudications_v2.jsonl` | `b2772387d9a78263` |
| `rag_explicitness_eval_gemma3_v2/adjudication/rag_adjudication_summary.json` | `8ee871bce710456b` |

Los hashes completos de la evaluación están en `rag_explicitness_eval_gemma3_v2/hash_manifest.json`. Qrels v2 con procedencia corregida en `outputs/local_runs/explicitness_qrels_v2_evalprovenance/` (TSV idéntico byte a byte al histórico; 107 filas de asistente bajo delegación explícita, 91 de confirmación humana).

No se hicieron commits ni llamadas de pago. No se modificó `v1/`.

## Pendiente

Integrar en la memoria los resultados de recuperación emparejada y de generación/evaluación en los capítulos de resultados y discusión, con estos límites declarados. Queda fuera de esta fase la validación con juez externo o humano completo de las 55 respuestas, y el benchmark repetido end-to-end de latencia.
