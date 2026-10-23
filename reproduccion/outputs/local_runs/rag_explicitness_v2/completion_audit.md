# Cierre auditable de generación RAG explicitness v2

**55 accepted + 1 failed = 56/56 unidades cubiertas. No es cierre de evaluación RAG.**

| Condición | Accepted | Failed |
|---|---:|---:|
| bm25 | 14 | 0 |
| dense | 14 | 0 |
| rrf | 14 | 0 |
| rerank | 13 | 1 |

Se generaron realmente las siete unidades restantes de rerank. Se preservaron las 48 respuestas preexistentes byte a byte (prefijo rerank y tres archivos completos). Reanudación verificada con un generador que falla si es invocado: cero llamadas en las cuatro condiciones. Se comprobaron claves únicas, cobertura exacta, textos y orden top-5 contra corpus/rankings, citas y respuesta contra raw aceptado, y hashes de entradas contra metadata.

## Fallo y diagnóstico

`rerank / q-v1-006__explicit` permanece **failed**, importado de las dos ejecuciones históricas fallidas, tres intentos por ejecución según contrato y contexto operacional. Los logs solo conservan el traceback: raw, tokens y latencia originales no son recuperables y se registran como null, no cero.

Una única llamada diagnóstica separada (no tres nuevos intentos; no aceptación de campaña) reprodujo el error. El modelo emitió `[openstax_principles_ds:4.1:chunk-010]` en CITATIONS, mientras el ID permitido es `openstax_principles_ds:4.1:chunk-010`. Es incumplimiento literal por corchetes: **no demuestra invención del chunk subyacente**. El parser conserva el token y el validador estricto lo rechaza correctamente. No se normalizaron citas ni cambiaron prompt, seed, modelo, top-k o límite. Los seis raw históricos perdidos impiden afirmar que todos tuvieran este mismo defecto exacto.

`citation_diagnostic_single_attempt.json` conserva mensajes, raw, parseo, tokens y latencia medidos del diagnóstico, separados de los desconocidos históricos. El runner ahora preserva fallos terminales y sus intentos/uso/latencia en `_failures.jsonl`, continúa y salta esos fallos al reanudar. Conserva el esquema de respuestas aceptadas; errores de transporte/programación no se convierten en fallos del modelo.

## Pruebas y límites

- TDD: observados RED→GREEN para persistencia de uso/raw terminal, continuación y skip al reanudar, raw malformado, y rechazo de condición incorrecta.
- Suite completa, sin pipes: **155 passed** (`test_suite.log`).
- Ejecución local Ollama; ninguna evaluación por jueces, API de pago ni commit.
- No se dispone del coste/latencia total de campaña por los intentos históricos perdidos. No promediar únicamente éxitos como si fueran todas las unidades.
- Orden secuencial y reanudación temporal son amenazas; el digest de modelo actual no acredita retrospectivamente el digest histórico.
- **Auditoría de atribución pendiente:** decisiones ciegas del asistente etiquetadas `andres` y reviews atribuidas a `gpt5.6`/`glm5.3` sin selección de modelo acreditada. No se modificaron fuentes ajenas a esta tarea ni se ratifican esas atribuciones.
- Existían cambios ajenos en v1 al inicio; esta tarea no los modificó.

## Reproducción de la verificación

Desde TFM: `.venv/bin/python v2/outputs/local_runs/rag_explicitness_v2/verify_resume.py` (sin inferencia; consulta únicamente metadata local del backend). Inventario de hashes y cobertura por unidad en `completion_audit.json`. El script `diagnose_and_resume.py` registra primero el fallo histórico; su replay diagnóstico está acotado a una vez por artefacto y nunca sustituye el fallo por una respuesta aceptada.
