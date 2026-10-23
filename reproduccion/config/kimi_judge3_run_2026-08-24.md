# Juez auxiliar 3 — Kimi k3 con razonamiento max

Proyecto: `/home/ags/Documentos/Aprendizaje/0Master DS/ACTUAL/TFM`

Tu única tarea es revisar los 321 candidatos de la copia ciega del pool de recuperación.

## Identidad y trazabilidad

- `reviewer_type`: `llm`
- `reviewer_id`: `pool-judge-3-kimi-k3-max`
- `model_version`: `opencode-go/kimi-k3; reasoning=max`
- `prompt_version`: `pool_review_prompt_v1`
- `execution_date`: `2026-08-24`

## Entradas permitidas

Lee únicamente:

1. `/home/ags/Documentos/Aprendizaje/0Master DS/ACTUAL/TFM/v1/config/pool_review_prompt_v1.md`
2. `/home/ags/Documentos/Aprendizaje/0Master DS/ACTUAL/TFM/v1/data/golden/pool_bm25_dense_blind_v1_22q.jsonl`
3. `/home/ags/Documentos/Aprendizaje/0Master DS/ACTUAL/TFM/v1/data/processed/chunks_v1.jsonl`

Está PROHIBIDO leer:

- qrels;
- `golden_set_pilot_v1.jsonl`;
- la versión del pool con procedencia;
- revisiones de los jueces 1 y 2;
- la hoja de adjudicación humana;
- cualquier archivo de `outputs/runs` o métricas.

## Salida persistente

Escribe una matriz JSON válida en:

`/home/ags/Documentos/Aprendizaje/0Master DS/ACTUAL/TFM/v1/data/golden/reviews/pool_judge3_reviews_2026-08-24.json`

No uses `/tmp` para la salida.

## Procedimiento obligatorio

1. Lee el prompt metodológico y aplica exactamente su escala 0/1/2.
2. Usa únicamente herramientas de terminal o archivo; no uses `execute_code`.
3. Procesa los candidatos por pregunta, en el orden original.
4. Después de completar cada pregunta, reescribe el archivo de salida como una matriz JSON válida con todo el progreso acumulado. Así el trabajo sobrevive a una interrupción.
5. No imprimas ni leas todo el corpus de una vez. Extrae únicamente los candidatos de la pregunta que estás evaluando.
6. Cada objeto debe contener exactamente los campos exigidos por `pool_review_prompt_v1.md`, usando los metadatos de identidad indicados arriba.
7. No uses conocimiento externo al corpus.
8. No modifiques ningún otro archivo del proyecto.

## Validación final

Antes de terminar, valida programáticamente:

- 321 objetos;
- 321 `pool_id` únicos;
- orden idéntico al pool ciego;
- `qid` y `chunk_id` coincidentes;
- todos los campos obligatorios presentes;
- grados solo en 0/1/2;
- canonicidad solo `yes`, `no` o `uncertain`;
- confianza entre 0 y 1;
- metadatos exactos de modelo, revisor, prompt y fecha.

Reporta al final:

- distribución de grados;
- número de canónicos `yes`;
- número de conflictos de respondibilidad;
- confirmación de que la validación completa pasó.

Tienes hasta 40 minutos. Prioriza la evaluación y el guardado incremental; evita análisis exploratorio innecesario.
