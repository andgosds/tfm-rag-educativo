> **Recetas desde la raíz del paquete v2.** Los resultados descritos son históricos. Para operaciones de escritura usar destinos nuevos bajo `outputs/local_runs/`; los defaults congelados se rechazan. Recetas vigentes seguras: `standalone_operations.md`. No ejecutar inferencia mientras siga abierta la adjudicación.

# Ejecución retrieval-only de explicitness v2

## Resultado verificado

Se ejecutaron realmente BM25, dense E5, RRF y cross-encoder sobre las catorce formulaciones de siete preguntas base y los 288 chunks intactos. Cada estrategia produjo 140 filas. La segunda ejecución independiente reprodujo exactamente scores, ranks y demás campos no temporales; los tres archivos del pool y los embeddings fueron byte-idénticos. No se calcularon métricas de calidad ni se generaron respuestas, juicios o qrels nuevos.

La configuración congelada está en `outputs/explicitness_v2/configuration.json`. BM25 mantiene k1=1.5, b=0.75 y tokenización `[a-z0-9]+`; E5 usa `intfloat/e5-base-v2` revisión `f52bf8ec8c7124536f0efb74aca902b2995e5bcd`, prefijos passage/query y vectores normalizados con búsqueda exhaustiva por producto escalar. RRF conserva k0=60, profundidad de cada fuente=10 y salida=10. MiniLM usa `cross-encoder/ms-marco-MiniLM-L6-v2` revisión `233902d25c440f23af6f7d6e94d2946bac0bee0a` sobre exactamente los diez candidatos RRF. Ambos modelos usan float32, CUDA, batch 16 y límite 512. Empates: score descendente, chunk_id ascendente.

Ejecución local offline en NVIDIA GeForce RTX 2060 SUPER; Python 3.12.13, NumPy 2.5.2, PyTorch 2.13.0+cu130 y Sentence Transformers 5.7.0. Se reencodificó el corpus, no se simularon scores. Los modelos estaban en caché y no hicieron llamadas de pago. Se observaron 15 pasajes E5 truncados, cero queries truncadas y 3 pares del reranker truncados entre 140. Los avisos del tokenizer proceden del recuento deliberadamente sin truncar; la inferencia mantuvo límite 512.

## Adaptación mínima y estado epistemológico

Los CLI v1 mezclan recuperación, exigencia de adjudicación y evaluación. No se les pasaron falsos registros adjudicados ni qrels vacíos como artificio. El nuevo adaptador importa sus kernels de ranking sin modificar los scripts históricos. Los identificadores de ejecución son `base_qid__explicit` y `base_qid__implicit`; cada fila conserva base_qid, pair_id, explicitness y texto literal. Todas las formulaciones permanecen `pending_evidence_review` y ningún run contiene relevancia inventada.

Las latencias guardadas son medidas por etapa, sincronizadas con CUDA, en una pasada. Las sumas de etapas no son un benchmark end-to-end repetido ni una medición paralela. No se hacen recomendaciones operativas a partir de esos tiempos.

## Pool y cola de evidencia

| Unidad | Conteo |
|---|---:|
| Pool técnico histórico completo base–chunk | 340 |
| Unión actual base–chunk | 156 |
| Base–chunk nuevos respecto al pool histórico | 45 |
| Base–chunk ya vistos | 111 |
| Pool actual formulación–chunk | 220 |
| Formulación–chunk ya vistas | 175 |
| Cola ciega sin juicio | 122 |
| Nuevas y sin juicio | 44 |
| Ya vistas pero sin juicio | 78 |
| Reutilizaciones históricas pendientes | 98 |
| Reutilizaciones que incluyen grado 0 | 7 |

La novedad se calcula contra `pool_bm25_dense_v1_22q.jsonl`, no contra qrels positivos. Se consultaron el golden adjudicado y la cola final de tres jueces para recuperar decisiones históricas; se comprobó que ninguna adjudicación de la cola humana anterior quedaba fuera de la cola final. Se preservan los modos de adjudicación, en particular `assistant_on_behalf_of_andres`, sin presentarlos como decisiones humanas independientes.

Un candidato nuevo respecto al pool, `q-v1-014 / openstax_principles_ds:3.3:chunk-006`, ya era evidencia original adjudicada: pertenece a reutilización pendiente, no a la cola sin juicio. Por ello novedad y estado de revisión son dimensiones independientes. Las 98 decisiones previas están pendientes de equivalencia incluso cuando la formulación conserva el original; esta política conservadora no produce qrels v2 automáticos.

`pools/technical_pool.jsonl` conserva métodos, ranks, scores y procedencia histórica. `pools/blind_review_queue.jsonl` omite esas señales y contiene pregunta, texto del chunk, reviews vacías y decisión humana nula. `pools/pending_judgment_reuse.jsonl` conserva las decisiones previas como propuestas de reutilización pendientes. Cada formulación–chunk se revisa separadamente: no se presupone equivalencia entre formulaciones.

## Comandos reproducibles

Desde la raíz TFM:

```bash
# Comando realmente ejecutado; rechaza sobrescribir un directorio existente.
PYTHONDONTWRITEBYTECODE=1 uv run --project environments/dense --no-sync python scripts/explicitness_campaign.py --output outputs/explicitness_v2

# Segunda ejecución real realizada y comparada.
PYTHONDONTWRITEBYTECODE=1 uv run --project environments/dense --no-sync python scripts/explicitness_campaign.py --output outputs/explicitness_v2_reproduction

# Para una nueva réplica: elegir un nombre aún inexistente dentro de v2.
PYTHONDONTWRITEBYTECODE=1 uv run --project environments/dense --no-sync python scripts/explicitness_campaign.py --output outputs/explicitness_v2_replica_nueva

# Suite completa y aceptación read-only de artefactos congelados.
PYTHONDONTWRITEBYTECODE=1 uv run --no-sync python -m pytest -p no:cacheprovider tests -q
```

Resultado final: **116 tests passed**. Se verifican claves exactas, qids, rangos 1–10, unicidad, scores finitos, orden, RRF recalculado, igualdad exacta de conjuntos RRF/reranker, source_rank/source_score, partición de cola, cegamiento, hashes y réplica real. Los tres comportamientos nuevos del adaptador se desarrollaron con tests fallidos antes de implementación. Inicialmente se lanzó la suite completa en el entorno ML: 108 pasaron y 7 tests de extracción fallaron por ausencia de PyMuPDF. La suite completa posterior usa el entorno raíz correcto, sin instalar ni modificar dependencias históricas.

`protected_v1_before.json` y la verificación posterior cubren 277 archivos históricos: cero cambios. Excluyen entornos virtuales y cachés de Python/pytest, no datos ni resultados. Los hashes de entradas, scripts compartidos, adaptador y lockfiles constan en la configuración; `artifact_sha256.json` sella los resultados de cada ejecución. No hubo commits.

## Pendiente

Adjudicar las 122 unidades ciegas y confirmar o rechazar las 98 reutilizaciones; solo después construir qrels v2 y evaluar. No se ejecutaron generación, jueces automáticos, métricas finales, expansión del golden ni benchmark repetido de latencia.
