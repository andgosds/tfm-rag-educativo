> **Recetas desde la raíz del paquete v2.** Los resultados descritos son históricos. Para operaciones de escritura usar destinos nuevos bajo `outputs/local_runs/`; los defaults congelados se rechazan. Recetas vigentes seguras: `standalone_operations.md`. No ejecutar inferencia mientras siga abierta la adjudicación.

# Aplicación local para adjudicar el pool

La aplicación permite revisar 109 candidatos seleccionados mediante un protocolo dirigido por riesgo a partir de tres jueces automáticos, sin mostrar la procedencia de los recuperadores. No modifica los qrels: guarda las decisiones humanas únicamente en `pool_human_priority_three_judge_v1_22q.jsonl`.

La selección incluye cualquier candidato con algún grado 2, los 13 desacuerdos completos 0/1/2, los conflictos de respondibilidad, diez consensos 0/0/0 y diez consensos 1/1/1 elegidos mediante muestreo determinista. También conserva las decisiones realizadas antes de adoptar el protocolo reducido.

La adjudicación quedó completa el 2026-08-24: 109 de 109 candidatos revisados, con 14 grados 0, 45 grados 1, 50 grados 2 y 16 evidencias canónicas. La procedencia distingue 23 decisiones directas del usuario, 70 delegadas al asistente y 16 discrepancias fuertes confirmadas por el usuario.

## Inicio

Desde la raíz del TFM:

```bash
uv run python scripts/pool_review_app.py
```

La aplicación escucha exclusivamente en `127.0.0.1:8765` y abre el navegador predeterminado. Para iniciarla sin abrir el navegador:

```bash
uv run python scripts/pool_review_app.py --no-browser
```

## Flujo de revisión

1. Leer la pregunta, la respuesta de referencia o la abstención esperada y el chunk.
2. Asignar un grado:
   - **0**: no relevante;
   - **1**: relacionado o útil, pero insuficiente;
   - **2**: evidencia directa y suficiente.
3. Marcar **Evidencia canónica** solo cuando el grado sea 2 y el chunk sea la evidencia principal preferida.
4. Añadir una nota únicamente cuando la decisión necesite justificación.
5. Pulsar **Guardar y siguiente**.

Las opiniones de GPT-5.6-sol, GLM-5.3 y Kimi k3 permanecen cerradas por defecto. Deben consultarse solo cuando ayuden a resolver una duda; no sustituyen la decisión humana.

## Atajos

| Tecla | Acción |
|---|---|
| `0`, `1`, `2` | Seleccionar grado |
| `C` | Cambiar canonicidad cuando el grado es 2 |
| `N` | Enfocar la nota |
| `Enter` | Guardar y avanzar |
| `←`, `→` | Navegar |
| `U` | Deshacer la última decisión de la sesión |
| `Escape` | Salir de un campo de edición |

## Seguridad y trazabilidad

Cada guardado sustituye el JSONL de forma atómica y registra:

- `human_grade`;
- `human_canonical`;
- `human_note`;
- `human_reviewer_id = "andres"`;
- `human_reviewed_at`;
- `human_status = "adjudicated"`.

**Dejar pendiente** elimina la decisión del candidato y restaura su estado `pending`. **Exportar** descarga una copia del JSONL actual.

La aplicación muestra un aviso cuando `formula_risk = true`. Esos fragmentos requieren comprobación documental antes de aceptarlos como evidencia matemática.

## Validación

```bash
uv run pytest -q tests/test_pool_review_app.py
```

Las 109 decisiones se validaron antes de generar los qrels pooled. Los consensos automáticos no auditados no se incorporaron. `build_pooled_qrels.py` conserva los qrels originales y produce un archivo nuevo con 119 juicios positivos y procedencia trazable.
