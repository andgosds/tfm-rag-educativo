# Evaluación de generación invalidada — solo ids en el contexto

**Fecha de invalidación:** 2026-09-27. **Alcance:** todo el pase de evaluación de
`generation_scaling_v3` con jueces A (`gpt-6-sol`) y B (`mimo-v2.6-pro`), 604 celdas cada uno.

**Causa raíz:** los lotes mandaban el contexto recuperado como `contexto recuperado:
[openstax_intro_stats_2e:8.2:chunk-001]` —solo el id, sin el texto del fragmento. El juez A
se negó a puntuar sin evidencia y el juez B puntuó contra la referencia, no contra el
contexto. Los cuatro criterios quedan descalificados, `behavior_ok` incluido: se salvaba por
no necesitar contexto, pero procede del mismo pase.

**Por qué se archiva en vez de sobrescribir:** el evaluador es reanudable por la clave
generador + estrategia + qid. Si los veredictos inválidos siguieran en su ruta, la reanudación
los daría por hechos y no se evaluaría nada.

Contenido:

- `eval_verdicts_v3.jsonl`, `eval_verdicts_v3_juezB.jsonl`: 604 veredictos inválidos por juez.
- `contraste_jueces_v3.jsonl`: contraste A−B calculado sobre datos inválidos.
- `eval_batches/`, `eval_juezB_lote10/`: lotes sin texto de contexto.
- `log_evaluacion_*`, `log_supervisor_*`: trazas de aquella ejecución.

Los artefactos de generación NO están aquí: las 604 respuestas son válidas y solo se
reevalúan. Repetición con `ragas_rubric_v3.1` (contexto con texto completo) en los mismos
paths de siempre.
