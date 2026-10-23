# Reproducción documental: correcciones R18, R20 y R21

**Fecha:** 2026-09-30. **Raíz operativa:** la carpeta v2 que contiene `pyproject.toml`, `tfm.qmd` y `TASK_QUEUE.md`. Este informe complementa `docs/standalone_operations.md`: no modifica el pre-registro, los juicios, el acta ni los resultados congelados. No se han ejecutado modelos, llamadas a API ni adjudicaciones. Las salidas auxiliares offline nuevas están en `outputs/local_runs/reproduction_documental_20260930/`.

## 1. Niveles de reproducción y evidencia obtenida

| Nivel | Operación real | Evidencia en esta revisión |
|---|---|---|
| Observación del entorno | R y cuatro paquetes; Quarto; Typst incluido en Quarto | Versiones y sesión R capturadas en `docs/render_environment_20260930.json`; no instalación limpia ni render |
| Replay offline de recuperación | `evaluate_retrieval_v3.py` sobre rankings y qrels ya existentes | Ejecución exitosa; 52 formulaciones, 26 bases; IDCG global sobre qrels; salida `retrieval/` |
| Reanálisis emparejado offline | `paired_explicitness_v3.py` sobre las métricas recién reconstruidas | Ejecución exitosa; 32 contrastes y 32 de sensibilidad; 20 bases con grado 2; salida `paired/` |
| Reanálisis de capacidad offline | `analysis_capacity_v3.py --output-dir` corregido | Ayuda y ejecución exitosa; 624 previstas, 604 aceptadas, 20 fallidas; salida `capacity/` con CSV/JSON y hashes |
| Preparación offline de evaluación | `evaluate_rag_remote_v3.py --only-batches` | Ejecución exitosa; corpus 288, 604 inputs, 61 lotes; salida `judge_inputs/batches/`; no invocación de juez |
| Auditoría offline de consolidación | Comparación de A/B, acta y valores finales por clave completa y criterio | Cobertura exacta y valores/procedencia reconstruidos iguales a los congelados; sin escritura de decisiones |
| Inferencia local o remota | Recuperación neuronal, generación, evaluación y arbitraje | Solo `--help` donde existe parser; no pruebas de modelos ni validación de disponibilidad actual de proveedores |
| Adjudicación humana | Confirmaciones del usuario sobre las hojas históricas | Fuente existente conservada; no se ha adjudicado nada en esta revisión |

La ayuda se verificó para `evaluate_retrieval_v3`, `paired_explicitness_v3`, `explicitness_campaign_v3`, `run_rag_generation`, `evaluate_rag_remote_v3`, `arbitrate_rag_discrepancies_v3`, `build_qrels_final_v3`, `build_generation_golden_v3`, `build_chunks`, `extract_openstax_chapters`, `run_bm25` y `validate_tfm_closure`. Se evitó `contraste_jueces_v3.py --help`: no tiene parser y escribe al ejecutarse. No se asume que cualquier script admita ayuda inocua.

## 2. Receta offline ejercitada desde v2

```sh
set -eu
DEST=outputs/local_runs/reproduction_documental_NUEVA
test ! -e "$DEST"
PYTHONDONTWRITEBYTECODE=1 uv run --no-sync python scripts/evaluate_retrieval_v3.py \
  --run-dir outputs/local_runs/explicitness_v3 \
  --qrels outputs/local_runs/explicitness_v3/qrels_final_v3.jsonl \
  --methods bm25,dense,rrf,rerank --output-dir "$DEST/retrieval"
PYTHONDONTWRITEBYTECODE=1 uv run --no-sync python scripts/paired_explicitness_v3.py \
  --metrics-dir "$DEST/retrieval" \
  --historical-metrics-dir outputs/local_runs/explicitness_v3/retrieval_metrics_v3 \
  --output-dir "$DEST/paired"
PYTHONDONTWRITEBYTECODE=1 uv run --no-sync python scripts/analysis_capacity_v3.py \
  --output-dir "$DEST/capacity"
PYTHONDONTWRITEBYTECODE=1 uv run --no-sync python scripts/evaluate_rag_remote_v3.py \
  --inputs outputs/local_runs/generation_scaling_v3/rag_*_top5_qwen35_4b.jsonl \
    outputs/local_runs/generation_scaling_v3/rag_*_top5_gemma4_e4b.jsonl \
    outputs/local_runs/generation_scaling_v3/rag_*_top5_qwen35_9b.jsonl \
  --batches-dir "$DEST/judge_inputs" --output "$DEST/unused_verdicts.jsonl" \
  --batch-size 10 --only-batches
```

La prueba usó `DEST=outputs/local_runs/reproduction_documental_20260930`, que no existía. Los glob incluyen únicamente los doce archivos de respuestas aceptadas de los tres generadores del análisis; **no** incluyen fallos, el modelo excluido Gemma 3 ni archivos de diagnósticos. La reconstrucción de lotes por código incluye el texto del corpus por id. La salida exitosa del preparador acredita preparación y recuento, no calidad de un juez.

`retrieval/retrieval_correction_report.json` y `paired/paired_correction_report.json` guardan contratos y hashes de sus fuentes. Las filas originales no se sobrescriben. La protección de salidas del evaluador y del análisis pareado no implica protección equivalente en todos los demás scripts v3. Para scripts sin guard, comprobar previamente que todo destino sea nuevo dentro de `outputs/local_runs/`.

El CLI de capacidad incorporado durante las correcciones también se leyó y ejercitó: exige `--output-dir` nuevo y crea CSV/JSON sin modelos ni figuras Python. Confirmó 604 aceptadas + 20 fallidas de 624 previstas en los tres modelos incluidos, 389 `answer`, 120 `grounded_correction`, 95 `abstain`, cuatro factual no disponibles. `capacity/hash_manifest.json` registra el hash del script ejecutado (`699a2dccd5256132b3da02cb309826e0d3998cc2e473272f962cade2fdf19da5`), las fuentes de generación/fallos y cada salida; el alcance primario de contenido se separa de todas las celdas y de abstenciones diagnósticas. El archivo `joined_cells.csv` conserva la unión por clave completa; no edita el consolidado congelado. La procedencia AA sigue siendo aportación del usuario, no verificación externa.

## 3. Cadena de fuentes de la campaña v3

1. **Corpus:** `data/processed/chunks_v1.jsonl`; se conservan los 288 fragmentos extraídos, incluso sus limitaciones matemáticas. No reextraer para corregir silenciosamente las evidencias usadas por jueces.
2. **Parejas admitidas:** `data/golden/variants/explicitness_pairs_v3_all26.jsonl` y `outputs/local_runs/explicitness_v3/formulations.jsonl` (26 bases / 52 formulaciones). El pre-registro planteó 30 bases; no todas se admitieron como parejas.
3. **Recuperación:** `outputs/local_runs/explicitness_v3/configuration.json`, `execution_metadata.json` y cuatro archivos `runs/explicitness_v3_{bm25,dense,rrf,rerank}.jsonl`. CUDA, revisiones inmutables de E5 y cross-encoder, fusión y desempate están en la configuración real, no se infieren del nombre del archivo.
4. **Relevancia:** `qrels_final_v3.jsonl` contiene fuentes por unidad. El constructor existente `build_qrels_final_v3.py --run-dir ...` escribe dentro de ese directorio: para repetirlo habría que copiar antes las entradas `judging/` y `judging_premise/` a un destino nuevo, nunca señalar al congelado. Usa la marca de premisa de `question_premise_audit_v3.jsonl`. Su política permite `single_judge` como último recurso: que exista el constructor no demuestra revisión humana exhaustiva.
5. **Golden de generación:** `data/golden/variants/generation_golden_v3.jsonl`; constructor `build_generation_golden_v3.py`, que admite entradas explícitas. Fuentes: formulaciones, `data/golden/expansion_v3/question_design_v3.jsonl`, `golden_set_v3_draft.jsonl`, piloto local `data/golden/golden_set_pilot_v1.jsonl` y marca humana de premisa. Esas rutas con v1 en el nombre siguen estando dentro de v2.
6. **Generación:** doce archivos `rag_{condicion}_top5_{generador}.jsonl` de Qwen 4B, Gemma 4 E4B y Qwen 9B; sus `*_metadata.json` registran hashes de rankings, corpus, golden y `data/golden/answerability_resolutions_v1_22q.json`. Los ledgers `*_failures.jsonl` siguen separados; no se convierten en puntuaciones 0 ni en respuestas aceptadas.
7. **Jueces válidos:** `eval_verdicts_v3.jsonl` y `eval_verdicts_v3_juezB.jsonl`, con `prompt_version: ragas_rubric_v3.2`. Son rúbricas discretas vía Hermes, **no métricas RAGAS ejecutadas**, pese al nombre histórico del prompt.
8. **Desacuerdos y arbitraje:** `contraste_jueces_v3.jsonl` y `arbitraje_discrepancias_v3/arbitraje_v3.jsonl`; propuesta delegada con sus `raw/`, no adjudicación humana por sí misma.
9. **Acta humana:** `arbitraje_discrepancias_v3/validacion_humana_v3.jsonl`, hojas `validacion_lote_01.md`…`validacion_lote_16.md`. El JSONL contiene 158 decisiones celulares **y una fila adicional de convención metodológica**: no contar líneas como casos.
10. **Consolidación:** `eval_final_v3.jsonl` y `eval_final_v3_summary.json`, con procedencia por criterio. Hay 604 celdas, 446 de consenso en todos los criterios y 158 con validación humana en al menos un criterio; no son 604 revisiones humanas.
11. **Análisis corregidos:** las nuevas métricas y análisis deben leerse de destinos propios de corrección académica, no confundirse con `retrieval_metrics_v3/` ni con `generation_scaling_v3/capacidad/` históricos. Este informe no certifica por anticipado artefactos que otros procesos estén construyendo.

La reproducción propia de capacidad aquí certificada es `outputs/local_runs/reproduction_documental_20260930/capacity/`; los destinos paralelos `academic_corrections_20260930` deben verificarse con sus propios informes al cerrar esa fase. El éxito de este replay no constituye una nueva campaña ni nuevo juicio.

### Identidades registradas, no marcas inferidas

Se inspeccionaron los campos de las 604 filas de cada juez: A registra `judge_model=gpt-6-sol`, `judge_provider=openai-codex`; B registra `judge_model=mimo-v2.6-pro`, `judge_provider=opencode-go`; todos declaran `ragas_rubric_v3.2`. Se informa **identidad registrada de ejecución**, no una comprobación actual del catálogo ni independencia de familias demostrada. El protocolo declara el solape de B con el diseño de preguntas y el posible sesgo de familia entre A y el árbitro. Los datos históricos del piloto con identidad no acreditada no se elevan aquí a identidades verificadas.

La reconstrucción por `(qid, generator_model, retrieval_condition)` confirmó cobertura idéntica en generación, A, B y final; el acta cubre exactamente los **233 pares celda–criterio discrepantes** de 158 celdas. En los consensos se conserva A=B; en discrepancias se toma `decisions[criterio].final`; `final_provenance` coincide con esta regla en todos los criterios. `label_ok` es idéntico en A, B y final. `expected_behavior` aparece nulo en el consolidado: cualquier desglose por conducta debe recuperarlo de la generación mediante la clave completa, nunca adivinarlo desde qid.

No se localizó una CLI dedicada para construir el consolidado RAG v3 en el árbol inspeccionado. La consolidación histórica tuvo una fase manual/asistida; los constructores del piloto no sustituyen ese contrato. Aquí se verificó su resultado **en lectura** mediante la regla anterior. Para obtener un nuevo archivo se requiere implementar y probar un constructor por separado, o documentar explícitamente la operación manual, sin inventar un comando que no existe.

## 4. Inferencia: recetas de interfaz, no ejecutadas

Recuperación neuronal local (cache offline no significa ausencia de inferencia):

```sh
uv run --project environments/dense --no-sync python scripts/explicitness_campaign_v3.py \
  --output outputs/local_runs/NUEVO_IR_V3 --top-k 10
```

Generación de una condición y un modelo, conservando corpus, golden y referencias v3:

```sh
uv run --project environments/rag --no-sync python scripts/run_rag_generation.py \
  --experiment-id gen_replay_v3_bm25_qwen35_4b --retrieval-condition bm25 \
  --retrieval-run outputs/local_runs/explicitness_v3/runs/explicitness_v3_bm25.jsonl \
  --chunks data/processed/chunks_v1.jsonl \
  --golden data/golden/variants/generation_golden_v3.jsonl \
  --resolutions data/golden/answerability_resolutions_v1_22q.json \
  --model qwen3.5:4b --top-k 5 --prompt-version rag_answer_prompt_v1 \
  --output outputs/local_runs/NUEVA_GENERACION/rag_bm25_top5_qwen35_4b.jsonl \
  --metadata outputs/local_runs/NUEVA_GENERACION/rag_bm25_top5_qwen35_4b_metadata.json
```

Es una receta de una celda de diseño, **no un runner factorial intercalado**. Repetir por condiciones/modelos debe preservar y registrar el orden real. Los parámetros del cliente Ollama no son flags de esta CLI: en la fuente se fijan temperatura 0, seed 20260902, `num_predict=300`, `num_ctx=8192`, `think=false`, endpoint local y hasta tres intentos trazables. No añadir flags imaginarios. Un nombre de modelo Ollama es una etiqueta, no garantía de reproducir sus pesos: antes de otra campaña registrar su identidad/digest y entorno; esa comprobación no se realizó aquí.

La receta de juicio remoto es la preparación offline anterior sin `--only-batches`, con salida y lotes separados por juez y pares explícitos A `--model gpt-6-sol --provider openai-codex --reasoning high`, B `--model mimo-v2.6-pro --provider opencode-go --reasoning ''`. La cadena vacía evita trasladar el default `high` de A a B. Esta variante **no se ejecutó** y requiere autorización/acceso al proveedor. No representa nueva validación del juez. El arbitraje existente lee inputs históricos fijados en código; la revisión humana y el cierre del acta siguen siendo pasos explícitos manuales.

## 5. Pre-registro frente a ejecución y correcciones posteriores

El documento `docs/explicitness_v3_preregistration.md` se conserva como fuente histórica. Contiene diez enmiendas, con la 7 situada antes de la 6; sus bloques originales todavía incluyen cifras/modelos superados (416 celdas, Qwen 3.8 27B, Gemma 3 como juez y cuatro generadores). No interpretar todo el cuerpo como configuración efectiva uniforme ni reescribirlo retroactivamente.

| Plan o decisión registrada | Ejecución/estado que se debe distinguir |
|---|---|
| 30 bases y parejas sujetas a R1/R2/R3 | 26 parejas admitidas; 52 formulaciones; no sumar formulaciones como unidades independientes |
| Escala con tres tamaños de Qwen | Las exclusiones de viabilidad dejan dos tamaños Qwen y un contraste Gemma; no una curva causal de tres tamaños de una familia |
| Gemma 3 incorporado al diseño | Enmienda 4 declara que omitió la sonda antes de generar; se excluye de calidad, no se oculta el fallo de procedimiento |
| Contrato estricto original | Enmienda 6 amplía el parser tras observar datos; archivos de fallos estrictos y fallos finales no son intercambiables |
| Orden intercalado de factores | La CLI es por condición; no tiene runner de intercalado factorial. Conservar el orden realmente ejecutado como limitación temporal, no afirmar cumplimiento por existencia del plan |
| Un juez/RAGAS en bloques iniciales | Enmienda 7 fija dos jueces remotos y rúbrica discreta; son 604 respuestas válidas por juez, no 416 |
| Primer pase de evaluación | Enmienda 8 invalida todo `eval_invalida_solo_ids_20260927/` (contextos solo ids), incluso conducta; prohibido usarlo como entrada analítica |
| Parcial v3.1 | Enmienda 9 archiva 310 A y 40 B en `eval_diagnostico_v3.1_parcial/`; conducta cambia de igualdad de etiquetas a escala real 0–2, `label_ok` queda aparte |
| Auditoría humana directa | Enmienda 10 incorpora arbitraje delegado seguido de validación humana; preservar ambos, sin llamar humano al arbitraje pendiente |
| Bootstrap 2.000 réplicas previsto | Análisis histórico de capacidad usa 5.000 y seed 20260928; cambio analítico documentado, no nueva generación |
| Informe descriptivo con IC, sin pruebas de superioridad | Test de signos ejecutado y Holm de las correcciones son post-hoc; dos familias de 16 contrastes por cohorte; no redefinen H1–H6 ni prueban equivalencia |
| nDCG graduado pre-registrado | Corrección R01 repara IDCG del código con todos los qrels; no cambio de la definición declarada, pero sí cambio de cifras históricas |
| AA Intelligence Index | Valores aportados por el usuario (Gemma=9, Qwen4B=13, Qwen9B=14), no contrastados con fuente externa; eje descriptivo con familia/capacidad confundidas |

La dirección del análisis pareado CLI es **explícita − implícita**; el pre-registro describe **implícita − explícita**. Ambos son legítimos si se conservan los signos y las etiquetas; no copiar deltas sin invertirlos cuando cambie la convención. Los intervalos que incluyen cero no establecen equivalencia ni robustez.

## 6. Entorno de render observado

- R 4.6.1 (2026-06-24).
- dplyr 1.2.1; ggplot2 4.0.3; jsonlite 2.0.0; knitr 1.51.
- Quarto 1.8.25; Typst incluido 0.13.0 (`8dce676d`).
- No hay `typst` independiente en PATH; usar `quarto typst --version`.

Comprobaciones repetibles desde v2:

```sh
Rscript -e 'cat(R.version.string,"\n"); for(p in c("dplyr","ggplot2","jsonlite","knitr")) cat(p,as.character(packageVersion(p)),"\n")'
quarto --version
quarto typst --version
```

`render_environment_20260930.json` preserva comandos, resultados y `sessionInfo()`. Es una fotografía del entorno instalado, no un lock ni prueba de instalación nueva. Para producir PDF ejecutar `quarto render tfm.qmd --to typst --output reproduced-tfm.pdf` desde una **copia desechable** del paquete: Quarto también crea auxiliares y figuras. Esta revisión no ha renderizado ni modificado `tfm.qmd`/PDF.

## 7. SHA-256 de fuentes reales

Calculados sobre los bytes actuales de cada archivo indicado, no copiados del nombre ni reconstruidos. Los doce archivos de generación aceptada se enumeran para evitar glob ambiguo. Los metadatos históricos de generación también registran hashes coincidentes del corpus, golden, resoluciones y ranking de su condición. No se presentan como validación externa de modelos ni del índice AA.

- `data/processed/chunks_v1.jsonl`
  - `19a5d50c97d501f021f4c461f2bbbed5b47b89cbc0486bbadf53087b5e05ac4a`
- `data/golden/variants/explicitness_pairs_v3_all26.jsonl`
  - `e8a32a6a598ad5ff98b6b764a1ede2b2c3c22d62a9dc99c724dfd721340e8f17`
- `data/golden/variants/generation_golden_v3.jsonl`
  - `866b75af5de3258c9affc53b1188313d79b3c24fc0a19d1a804c440cd40d49e0`
- `data/golden/variants/question_premise_audit_v3.jsonl`
  - `7ccf27ce259d011b6ee50badadba43ab1cfebef3e98e9c81b2449a4396b36d38`
- `data/golden/answerability_resolutions_v1_22q.json`
  - `cd70b77fa7a410aca84c5737ef4cc0588217df736039c9244bc3067658a5d190`
- `docs/explicitness_v3_preregistration.md`
  - `eeb8f49f64cf2036de357c99dc965d369eb803b8687a6d59c9f83f4b19181869`
- `outputs/local_runs/explicitness_v3/configuration.json`
  - `1fd30dade199e60ce45a2b07bcc3b9794196c169b07b01300799f55b62b47a91`
- `outputs/local_runs/explicitness_v3/formulations.jsonl`
  - `7520db83e458e96a0c3f7500b11fbfcbe8ec0ae912b09e63ff4b685954984e7b`
- `outputs/local_runs/explicitness_v3/qrels_final_v3.jsonl`
  - `18ce8d47fefaec3524e863f263cfa19d4b87f896931c90b1bc14aaecec6d7e18`
- `outputs/local_runs/generation_scaling_v3/rag_bm25_top5_qwen35_4b.jsonl`
  - `447ed24e2cd72850c0ccfce566f1fa5876a9622cf46684593c80af45bb5513e4`
- `outputs/local_runs/generation_scaling_v3/rag_dense_top5_qwen35_4b.jsonl`
  - `14e8c6d113e066923fac51d147f834f1c73ca5eb3f307f5f99c4f076e9b85e20`
- `outputs/local_runs/generation_scaling_v3/rag_rrf_top5_qwen35_4b.jsonl`
  - `4b6df2552f6a2fe177c9b359c041cbfc6fbb041dafffd51d4b802697d41473f2`
- `outputs/local_runs/generation_scaling_v3/rag_rerank_top5_qwen35_4b.jsonl`
  - `a554d38aff369b8f9a084dc3f26f5331d8ae4558e11ac8b114ae3bfb79d2b8a7`
- `outputs/local_runs/generation_scaling_v3/rag_bm25_top5_gemma4_e4b.jsonl`
  - `d905587a119bab301c3e0cdbfc34e593dbab6fa98aa5f428addb057eec052afb`
- `outputs/local_runs/generation_scaling_v3/rag_dense_top5_gemma4_e4b.jsonl`
  - `41ea6c1adb9b553db106fe21d5ea711c2ed900f9c93fcd798c24c5414687a9e8`
- `outputs/local_runs/generation_scaling_v3/rag_rrf_top5_gemma4_e4b.jsonl`
  - `ef235a125b845b8205736d252ec80f8a42a2d01eaa24ed68602e305adb5f73ff`
- `outputs/local_runs/generation_scaling_v3/rag_rerank_top5_gemma4_e4b.jsonl`
  - `ab4cc3dea0795e2cc629dba60679e91c0fc9962ff9673d055deb6621e69f2217`
- `outputs/local_runs/generation_scaling_v3/rag_bm25_top5_qwen35_9b.jsonl`
  - `481fb7d3663d74a09b3240023b9c3d024a6734353f4bbb504c0fe6b813d69d96`
- `outputs/local_runs/generation_scaling_v3/rag_dense_top5_qwen35_9b.jsonl`
  - `d3ea2a4931a0e64f3c8f326e1cc1d6a027adf2a303f2a547aa54404a73014e8b`
- `outputs/local_runs/generation_scaling_v3/rag_rrf_top5_qwen35_9b.jsonl`
  - `e7061b2f300963904ae793ea63dd9636effa6b0db537d69c4f07c9da9e6667e0`
- `outputs/local_runs/generation_scaling_v3/rag_rerank_top5_qwen35_9b.jsonl`
  - `6eec7c8d539582afc4423cb2bce1e3792f2b4ff3d0ae0c6726e4efb50b07bc1e`
- `outputs/local_runs/generation_scaling_v3/eval_verdicts_v3.jsonl`
  - `18163d09918805f530d2122b29b1aa809182b27a481a8a7d2733f0e8f02da907`
- `outputs/local_runs/generation_scaling_v3/eval_verdicts_v3_juezB.jsonl`
  - `f0fa618bfba4f87e495cb59d9733fb0e28b496646f09baeecb35d3f22f20612c`
- `outputs/local_runs/generation_scaling_v3/contraste_jueces_v3.jsonl`
  - `ccfd894a9ca4f61f45c997a04b3ba988ef61fe5d46c3f6d33fb74f4dfc37b069`
- `outputs/local_runs/generation_scaling_v3/arbitraje_discrepancias_v3/arbitraje_v3.jsonl`
  - `905fd98c1f74dc5e727e9f08cb55e2a431d2c8f318616d4e70465db195a38eed`
- `outputs/local_runs/generation_scaling_v3/arbitraje_discrepancias_v3/validacion_humana_v3.jsonl`
  - `295d56cb18c7d7b94499aff5c6cf61f461e5afcb83da35dde1f6f9b81256ffae`
- `outputs/local_runs/generation_scaling_v3/eval_final_v3.jsonl`
  - `c017ee322141bce3f88a68dfe2457e991f90bf54f6f136fad80fed8c771bf071`
- `outputs/local_runs/generation_scaling_v3/eval_final_v3_summary.json`
  - `64679b406431c45fc0f8b88bfb98376803cb26277b1f745c2d827c98efb3e7e3`
- `outputs/local_runs/generation_scaling_v3/eval_invalida_solo_ids_20260927/LEEME.md`
  - `945270892a447d6e8f9cb41cb398391453cf412d8303fb6fe16acce5db785d83`
- `outputs/local_runs/generation_scaling_v3/eval_diagnostico_v3.1_parcial/LEEME.md`
  - `cbf7c4b50f0baed9803fc2f971b004b7141c4e063b489c7624a48b445d78acb9`
- `outputs/local_runs/explicitness_v3/runs/explicitness_v3_bm25.jsonl`
  - `89c9bd8d45ff092cfdb37365868c3ff44efebe1483132e4a1c35f0937d16408b`
- `outputs/local_runs/explicitness_v3/runs/explicitness_v3_dense.jsonl`
  - `8146050a86e13299d1d317fadb9d9ca71678ac1810d60029b55f95df2c8dc0ba`
- `outputs/local_runs/explicitness_v3/runs/explicitness_v3_rrf.jsonl`
  - `6ff7b67b4c094b7ebb8027695340e76d8b6b1f84ca011e679eb9fb4887b9c3a9`
- `outputs/local_runs/explicitness_v3/runs/explicitness_v3_rerank.jsonl`
  - `7bdb6fdf82b8a06c8135378559f1e88329ed2897169ca6fdf594b07465a5d9b6`
