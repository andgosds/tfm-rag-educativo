# Parcial de diagnóstico — `ragas_rubric_v3.1` interrumpido

**Fecha:** 2026-09-27. **Motivo de la interrupción:** el análisis de los parciales detectó
que el criterio `behavior_ok` de la rúbrica `ragas_rubric_v3.1` no mide el comportamiento de
la respuesta, sino la **igualdad entre la etiqueta declarada por el generador y la esperada**:
en las 240 celdas evaluadas por el juez A, `behavior_ok` coincide **exactamente** con
`reported_behavior == expected_behavior`. Es una comparación de strings que no necesita juez,
y deja fuera el eje que la memoria necesita: si la respuesta contesta, corrige o se abstiene
como corresponde.

Diagnóstico adicional del parcial (no invalida los otros tres criterios; se conserva como
evidencia del hallazgo):

- Etiquetado del generador `qwen3.5:4b`: 118/208 mal etiquetadas (~56 %), casi todas
  `answer → grounded_correction` (94) y `abstain → grounded_correction` (18). Con la
  definición antigua, la métrica de conducta quedaba dominada por este artefacto.
- Acuerdo A−B provisional (30 celdas comunes): faithfulness 77 %, factual_correctness 73 %,
  behavior_ok 100 % (por ser comparación mecánica), citations_ok 77 %. Los desacuerdos son
  solo adyacentes (0↔1, 1↔2), sin celdas extremas 0↔2; A sistemáticamente más estricto que B.
- Abstenciones esperadas: 32/36 con faithfulness 2 y 34/36 con factual 2; ninguna abstención
  justificada penalizada con faithfulness 0. El tratamiento de abstención de la rúbrica
  funciona.
- Salud operativa: A 310 celdas en ~45 min, B 40; 0 lotes descartados y 0 reintentos fallidos
  (el pase invalidado anterior sí tenía descartes frecuentes).

Contenido: `eval_verdicts_v3.jsonl` (310), `eval_verdicts_v3_juezB.jsonl` (40) y los lotes y
logs correspondientes. **Ninguna cifra de este parcial entra en la memoria**; su valor es
documentar por qué se cambió la rúbrica antes de que el cambio pudiera parecer ajuste a los
resultados. Los otros tres criterios (faithfulness, factual_correctness, citations_ok) se
reevalúan igualmente, para que los cuatro procedan de un único `prompt_version`
(`ragas_rubric_v3.2`).
