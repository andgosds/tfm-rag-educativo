from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from run_bm25 import (
    _build_qrels,
    _load_jsonl,
    _load_qrels_tsv,
    _write_csv,
    evaluate_ranking,
)

MODEL_ID = "intfloat/e5-base-v2"
MODEL_REVISION = "f52bf8ec8c7124536f0efb74aca902b2995e5bcd"
DEFAULT_MAX_SEQ_LENGTH = 512


def build_query_input(question: str) -> str:
    """Añade el prefijo de consulta requerido por E5."""
    return f"query: {question}"


def build_passage_input(text: str) -> str:
    """Añade el prefijo de pasaje requerido por E5."""
    return f"passage: {text}"


def rank_embeddings(
    query_embedding: np.ndarray,
    document_embeddings: np.ndarray,
    document_ids: list[str],
    *,
    top_k: int,
) -> list[tuple[str, float]]:
    """Ordena por producto escalar y resuelve empates por identificador del documento."""
    if document_embeddings.ndim != 2:
        raise ValueError("document_embeddings must be a two-dimensional matrix")
    if query_embedding.ndim != 1:
        raise ValueError("query_embedding must be a one-dimensional vector")
    if document_embeddings.shape[1] != query_embedding.shape[0]:
        raise ValueError("query and document embedding dimensions must match")
    if len(document_ids) != document_embeddings.shape[0]:
        raise ValueError("document_ids and document_embeddings must have the same length")
    if top_k < 1:
        raise ValueError("top_k must be positive")

    scores = document_embeddings @ query_embedding
    # Con vectores normalizados, el producto escalar equivale a la similitud coseno.
    ranking = [
        (document_id, float(score))
        for document_id, score in zip(document_ids, scores, strict=True)
    ]
    ranking.sort(key=lambda item: (-item[1], item[0]))
    return ranking[:top_k]


def _sha256(path: Path) -> str:
    """Calcula la huella SHA-256 de una entrada para registrar su procedencia."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _resolve_device(requested: str) -> str:
    """Respeta el dispositivo solicitado o elige CUDA si está disponible en modo auto."""
    if requested != "auto":
        return requested
    import torch

    return "cuda" if torch.cuda.is_available() else "cpu"


def _count_truncated_inputs(
    tokenizer: Any,
    texts: list[str],
    *,
    max_seq_length: int,
    batch_size: int,
) -> int:
    """Cuenta los textos que exceden el límite de tokens antes de aplicar truncamiento."""
    truncated = 0
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        encoded = tokenizer(
            batch,
            padding=False,
            truncation=False,
            add_special_tokens=True,
        )
        truncated += sum(len(input_ids) > max_seq_length for input_ids in encoded["input_ids"])
    return truncated


def _encode(
    model: SentenceTransformer,
    texts: list[str],
    *,
    batch_size: int,
) -> np.ndarray:
    """Codifica textos como vectores normalizados de precisión float32."""
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    return np.asarray(embeddings, dtype=np.float32)


def run_experiment(
    *,
    run_id: str,
    chunks_path: Path,
    golden_path: Path,
    output_root: Path,
    qrels_path: Path,
    model_id: str = MODEL_ID,
    model_revision: str = MODEL_REVISION,
    device: str = "auto",
    batch_size: int = 16,
    max_seq_length: int = DEFAULT_MAX_SEQ_LENGTH,
    top_k: int = 10,
    cutoffs: tuple[int, ...] = (5, 10),
    qrels_input_path: Path | None = None,
) -> dict[str, Any]:
    """Ejecuta recuperación E5 y guarda embeddings, rankings, métricas y diagnósticos."""
    from output_safety import guard_run_outputs
    guard_run_outputs(output_root, run_id, qrels_path if qrels_input_path is None else None)
    if not run_id.replace("_", "").replace("-", "").replace(".", "").isalnum():
        raise ValueError("run_id must contain only letters, digits, dot, underscore or hyphen")
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    if top_k < 1 or any(cutoff < 1 or cutoff > top_k for cutoff in cutoffs):
        raise ValueError("cutoffs must be between 1 and top_k")

    chunks = _load_jsonl(chunks_path)
    records = _load_jsonl(golden_path)
    if any(record["annotation_status"] != "adjudicated" for record in records):
        raise ValueError("dense retrieval requires adjudicated golden-set records")

    document_ids = [chunk["chunk_id"] for chunk in chunks]
    if len(set(document_ids)) != len(document_ids):
        raise ValueError("duplicate chunk_id in corpus")
    passages = [build_passage_input(chunk["retrieval_text"]) for chunk in chunks]
    queries = [build_query_input(record["question"]) for record in records]
    record_qids = {record["qid"] for record in records}
    if qrels_input_path is None:
        qrels = _build_qrels(records)
        qrels_source = "golden_set_evidence"
        resolved_qrels_path = qrels_path
    else:
        qrels = _load_qrels_tsv(qrels_input_path)
        unknown_qids = set(qrels) - record_qids
        if unknown_qids:
            raise ValueError(f"qrels contain unknown qids: {sorted(unknown_qids)}")
        unknown_chunks = {
            chunk_id
            for qid_qrels in qrels.values()
            for chunk_id in qid_qrels
            if chunk_id not in document_ids
        }
        if unknown_chunks:
            raise ValueError(f"qrels contain unknown chunks: {sorted(unknown_chunks)}")
        qrels_source = "external_tsv"
        resolved_qrels_path = qrels_input_path
    for qid in record_qids:
        qrels.setdefault(qid, {})
    resolved_device = _resolve_device(device)

    model_started = time.perf_counter()
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(
        model_id,
        revision=model_revision,
        device=resolved_device,
        trust_remote_code=False,
    )
    model.max_seq_length = max_seq_length
    model_load_latency_ms = (time.perf_counter() - model_started) * 1000

    truncated_passages = _count_truncated_inputs(
        model.tokenizer,
        passages,
        max_seq_length=max_seq_length,
        batch_size=batch_size,
    )
    truncated_queries = _count_truncated_inputs(
        model.tokenizer,
        queries,
        max_seq_length=max_seq_length,
        batch_size=batch_size,
    )

    corpus_started = time.perf_counter()
    document_embeddings = _encode(model, passages, batch_size=batch_size)
    corpus_embedding_latency_ms = (time.perf_counter() - corpus_started) * 1000
    embedding_dimension = int(document_embeddings.shape[1])

    embeddings_dir = output_root / "embeddings"
    embeddings_dir.mkdir(parents=True, exist_ok=True)
    embeddings_path = embeddings_dir / f"{run_id}_documents.npy"
    np.save(embeddings_path, document_embeddings)
    metadata_path = embeddings_dir / f"{run_id}_metadata.json"
    metadata = {
        "run_id": run_id,
        "model_id": model_id,
        "model_revision": model_revision,
        "embedding_dimension": embedding_dimension,
        "document_prefix": "passage: ",
        "query_prefix": "query: ",
        "normalize_embeddings": True,
        "max_seq_length": max_seq_length,
        "batch_size": batch_size,
        "device": resolved_device,
        "document_count": len(chunks),
        "truncated_passage_count": truncated_passages,
        "truncated_query_count": truncated_queries,
        "corpus_path": str(chunks_path),
        "corpus_sha256": _sha256(chunks_path),
        "golden_path": str(golden_path),
        "golden_sha256": _sha256(golden_path),
    }
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if qrels_input_path is None:
        qrels_path.parent.mkdir(parents=True, exist_ok=True)
        qrels_path.write_text(
            "".join(
                f"{qid}\t0\t{chunk_id}\t{grade}\n"
                for qid in sorted(qrels)
                for chunk_id, grade in sorted(qrels[qid].items())
            ),
            encoding="utf-8",
        )

    query_latencies: list[float] = []
    run_rows: list[dict[str, Any]] = []
    per_query_rows: list[dict[str, Any]] = []
    metrics_by_query: dict[str, dict[int, dict[str, float | None]]] = {}

    if queries:
        # Una consulta de calentamiento queda fuera de las latencias registradas.
        _encode(model, [queries[0]], batch_size=1)

    for record, query_text in zip(records, queries, strict=True):
        query_started = time.perf_counter()
        query_embedding = _encode(model, [query_text], batch_size=1)[0]
        ranking = rank_embeddings(
            query_embedding,
            document_embeddings,
            document_ids,
            top_k=top_k,
        )
        query_latency_ms = (time.perf_counter() - query_started) * 1000
        query_latencies.append(query_latency_ms)
        ranked_ids = [chunk_id for chunk_id, _ in ranking]
        qid = record["qid"]
        metrics_by_query[qid] = {
            cutoff: evaluate_ranking(ranked_ids, qrels[qid], k=cutoff)
            for cutoff in cutoffs
        }
        strict_relevant = {
            chunk_id for chunk_id, grade in qrels[qid].items() if grade == 2
        }
        first_relevant_rank = next(
            (
                rank
                for rank, chunk_id in enumerate(ranked_ids, start=1)
                if chunk_id in strict_relevant
            ),
            None,
        )
        for rank, (chunk_id, score) in enumerate(ranking, start=1):
            run_rows.append(
                {
                    "run_id": run_id,
                    "qid": qid,
                    "question": record["question"],
                    "answerability": record["answerability"],
                    "chunk_id": chunk_id,
                    "rank": rank,
                    "score": score,
                    "relevant_grade": qrels[qid].get(chunk_id, 0),
                    "is_relevant": qrels[qid].get(chunk_id) == 2,
                    "query_latency_ms": query_latency_ms,
                }
            )
        per_query = {
            "qid": qid,
            "question_type": record.get("question_type", ""),
            "answerability": record["answerability"],
            "relevant_count": len(strict_relevant),
            "first_relevant_rank": first_relevant_rank,
            "top_score": ranking[0][1],
            "score_margin": ranking[0][1] - ranking[1][1] if len(ranking) > 1 else None,
            "query_latency_ms": query_latency_ms,
        }
        for cutoff in cutoffs:
            for metric, value in metrics_by_query[qid][cutoff].items():
                per_query[f"{metric}_at_{cutoff}"] = value
        per_query_rows.append(per_query)

    runs_path = output_root / "runs" / f"{run_id}.jsonl"
    runs_path.parent.mkdir(parents=True, exist_ok=True)
    runs_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in run_rows),
        encoding="utf-8",
    )

    metric_names = ("precision", "recall", "mrr", "ndcg")
    metric_qids = [
        record["qid"]
        for record in records
        if record["answerability"] == "answerable"
        and any(grade == 2 for grade in qrels[record["qid"]].values())
    ]
    aggregate_rows: list[dict[str, Any]] = []
    for cutoff in cutoffs:
        for metric in metric_names:
            values = [metrics_by_query[qid][cutoff][metric] for qid in metric_qids]
            aggregate_rows.append(
                {
                    "run_id": run_id,
                    "query_scope": "answerable_with_grade2_qrels",
                    "metric": metric,
                    "k": cutoff,
                    "value": statistics.fmean(value for value in values if value is not None),
                    "query_count": len(metric_qids),
                }
            )

    metrics_path = output_root / "metrics" / f"{run_id}_metrics.csv"
    _write_csv(
        metrics_path,
        aggregate_rows,
        ["run_id", "query_scope", "metric", "k", "value", "query_count"],
    )
    per_query_path = output_root / "metrics" / f"{run_id}_per_query.csv"
    metric_fields = [
        f"{metric}_at_{cutoff}"
        for cutoff in cutoffs
        for metric in metric_names
    ]
    _write_csv(
        per_query_path,
        per_query_rows,
        [
            "qid",
            "question_type",
            "answerability",
            "relevant_count",
            "first_relevant_rank",
            "top_score",
            "score_margin",
            "query_latency_ms",
            *metric_fields,
        ],
    )

    summary = {
        "run_id": run_id,
        "model_id": model_id,
        "model_revision": model_revision,
        "device": resolved_device,
        "embedding_dimension": embedding_dimension,
        "document_count": len(chunks),
        "query_count": len(records),
        "metric_query_count": len(metric_qids),
        "unanswerable_query_count": sum(
            record["answerability"] == "unanswerable" for record in records
        ),
        "answerable_without_grade2_qrels_count": sum(
            record["answerability"] == "answerable"
            and not any(grade == 2 for grade in qrels[record["qid"]].values())
            for record in records
        ),
        "qrels_source": qrels_source,
        "qrels_source_path": str(resolved_qrels_path),
        "qrels_sha256": _sha256(resolved_qrels_path),
        "retrieval_text_field": "retrieval_text",
        "document_prefix": "passage: ",
        "query_prefix": "query: ",
        "normalize_embeddings": True,
        "max_seq_length": max_seq_length,
        "batch_size": batch_size,
        "truncated_passage_count": truncated_passages,
        "truncated_query_count": truncated_queries,
        "top_k": top_k,
        "cutoffs": list(cutoffs),
        "binary_relevance_grade": 2,
        "ndcg_relevance_grades": [0, 1, 2],
        "model_load_latency_ms": model_load_latency_ms,
        "corpus_embedding_latency_ms": corpus_embedding_latency_ms,
        "total_query_latency_ms": sum(query_latencies),
        "mean_query_latency_ms": statistics.fmean(query_latencies),
    }
    summary_path = output_root / "metrics" / f"{run_id}_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def build_parser(root: Path) -> argparse.ArgumentParser:
    """Define las rutas y los parámetros del modelo para la recuperación densa."""
    parser = argparse.ArgumentParser(description="Run dense E5 retrieval for the TFM")
    parser.add_argument("--chunks", type=Path, default=root / "data/processed/chunks_v1.jsonl")
    parser.add_argument("--golden", type=Path, default=root / "data/golden/golden_set_pilot_v1.jsonl")
    parser.add_argument("--output-root", type=Path, default=root / "outputs")
    parser.add_argument("--run-id", default="dense_e5_base_v2_22q")
    parser.add_argument("--qrels", type=Path, default=root / "data/golden/qrels_golden_set_v1_22q.tsv")
    parser.add_argument(
        "--qrels-input",
        type=Path,
        default=None,
        help="Read method-independent qrels from this TSV instead of rebuilding them",
    )
    parser.add_argument("--model-id", default=MODEL_ID)
    parser.add_argument("--model-revision", default=MODEL_REVISION)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--max-seq-length", type=int, default=DEFAULT_MAX_SEQ_LENGTH)
    parser.add_argument("--top-k", type=int, default=10)
    return parser


def main() -> int:
    """Lanza la recuperación densa con protección de los destinos de salida."""
    root = Path(__file__).resolve().parents[1]
    args = build_parser(root).parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="run_dense")
    summary = run_experiment(
        run_id=args.run_id,
        chunks_path=args.chunks,
        golden_path=args.golden,
        output_root=args.output_root,
        qrels_path=args.qrels,
        model_id=args.model_id,
        model_revision=args.model_revision,
        device=args.device,
        batch_size=args.batch_size,
        max_seq_length=args.max_seq_length,
        top_k=args.top_k,
        cutoffs=(5, 10),
        qrels_input_path=args.qrels_input,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
