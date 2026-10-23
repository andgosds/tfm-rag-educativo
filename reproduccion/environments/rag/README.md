# Entorno RAG y RAGAS

Este entorno se conserva para las campañas anteriores que utilizaron RAGAS. No es necesario para reproducir el experimento final desde los notebooks: esa fase analiza puntuaciones congeladas de un instrumento ordinal propio.

## Versiones fijadas

- Python 3.12.
- RAGAS 0.4.3.
- LangChain Community 0.3.31. RAGAS 0.4.3 todavía importa un módulo retirado en LangChain Community 0.4, por lo que esta versión queda fijada.
- LangChain Ollama 1.x.
- Ollama como servidor local.

## Modelos

```bash
ollama pull qwen3.5:9b
ollama pull gemma3:4b
```

Qwen 3.5 9B genera las respuestas. Gemma 3 4B calcula las métricas RAGAS y la rúbrica auxiliar de comportamiento. Los modelos se mantienen separados para reducir la autoevaluación con la misma familia, aunque la evaluación sigue siendo automática y requiere auditoría humana.

## Instalación

Desde reproduccion/. Los comandos de esta página preparan o ejecutan inferencia; no forman parte del reanálisis offline:

```bash
uv sync --project environments/rag --locked --python 3.12
uv run --project environments/rag --no-sync python environments/rag/smoke_test.py
```

El smoke test debe devolver Faithfulness y Factual Correctness para un caso mínimo.

## Evaluación

```bash
uv run --project environments/rag --no-sync python scripts/evaluate_rag.py \
  --input outputs/rag/rag_rrf_top5_qwen35_9b_v1_22q.jsonl \
  --input outputs/rag/rag_rrf_rerank_top5_qwen35_9b_v1_22q.jsonl \
  --output outputs/local_runs/NUEVA_EVALUACION/rag_rrf_vs_rerank_top5_qwen35_9b_gemma3_4b_scores_v1_22q.jsonl \
  --summary outputs/local_runs/NUEVA_EVALUACION/rag_rrf_vs_rerank_top5_qwen35_9b_gemma3_4b_summary_v1_22q.json \
  --risk-queue outputs/local_runs/NUEVA_EVALUACION/rag_rrf_vs_rerank_top5_qwen35_9b_gemma3_4b_risk_queue_v1_22q.jsonl \
  --judge-model gemma3:4b
```

El evaluador escribe cada caso inmediatamente y reanuda por el par condición–pregunta. Una ejecución interrumpida no repite los casos ya guardados.
