from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import random
import re
import statistics
import sys
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from run_bm25 import BM25Index, _load_jsonl
from run_hybrid_rrf import reciprocal_rank_fusion


DENSE_MODEL_ID = "intfloat/e5-base-v2"
DENSE_MODEL_REVISION = "f52bf8ec8c7124536f0efb74aca902b2995e5bcd"
RERANKER_MODEL_ID = "cross-encoder/ms-marco-MiniLM-L6-v2"
RERANKER_MODEL_REVISION = "233902d25c440f23af6f7d6e94d2946bac0bee0a"


def _percentile(values: Sequence[float], probability: float) -> float:
    """Calcula un percentil de latencia mediante interpolación lineal entre muestras ordenadas."""
    if not values:
        raise ValueError("latency samples cannot be empty")
    ordered = sorted(float(value) for value in values)
    position = (len(ordered) - 1) * probability
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def summarize_latencies(values: Sequence[float]) -> dict[str, float | int]:
    """Resume la distribución de latencias con media, percentiles y dispersión muestral."""
    if not values:
        raise ValueError("latency samples cannot be empty")
    samples = [float(value) for value in values]
    return {
        "sample_count": len(samples),
        "mean_ms": statistics.fmean(samples),
        "median_ms": statistics.median(samples),
        "p95_ms": _percentile(samples, 0.95),
        "std_ms": statistics.stdev(samples) if len(samples) > 1 else 0.0,
        "min_ms": min(samples),
        "max_ms": max(samples),
    }


def build_condition_samples(
    stage_rows: Sequence[Mapping[str, float]],
) -> dict[str, list[float]]:
    """Compone las latencias de cada condición sumando sus etapas en ejecución serial."""
    required = ("bm25_ms", "dense_ms", "fusion_ms", "rerank_ms")
    samples = {
        "bm25": [],
        "dense": [],
        "hybrid_rrf_serial": [],
        "hybrid_rrf_rerank_serial": [],
    }
    for row in stage_rows:
        missing = [field for field in required if field not in row]
        if missing:
            raise ValueError(f"missing latency stage: {', '.join(missing)}")
        bm25 = float(row["bm25_ms"])
        dense = float(row["dense_ms"])
        fusion = float(row["fusion_ms"])
        rerank = float(row["rerank_ms"])
        hybrid = bm25 + dense + fusion
        samples["bm25"].append(bm25)
        samples["dense"].append(dense)
        samples["hybrid_rrf_serial"].append(hybrid)
        samples["hybrid_rrf_rerank_serial"].append(hybrid + rerank)
    return samples


def _sha256(path: Path) -> str:
    """Calcula el SHA-256 de un archivo leyendo bloques de un megabyte."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> None:
    """Guarda las muestras o sus resúmenes en un CSV con columnas explícitas."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run_benchmark(
    *,
    benchmark_id: str,
    chunks_path: Path,
    golden_path: Path,
    document_embeddings_path: Path,
    output_root: Path,
    warmup_rounds: int,
    repetitions: int,
    seed: int,
    top_k: int,
    dense_batch_size: int,
    reranker_batch_size: int,
    device: str,
) -> dict[str, Any]:
    """Mide las etapas de recuperación tras el calentamiento y exporta muestras y metadatos."""
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", benchmark_id):
        raise ValueError(
            "benchmark_id must contain only letters, digits, dot, underscore or hyphen"
        )
    if warmup_rounds < 1 or repetitions < 1:
        raise ValueError("warmup_rounds and repetitions must be positive")
    if top_k < 1:
        raise ValueError("top_k must be positive")

    import numpy as np
    import sentence_transformers
    import torch
    from sentence_transformers import CrossEncoder, SentenceTransformer

    chunks = _load_jsonl(chunks_path)
    records = _load_jsonl(golden_path)
    if not chunks or not records:
        raise ValueError("benchmark requires non-empty chunks and questions")
    if len({str(chunk["chunk_id"]) for chunk in chunks}) != len(chunks):
        raise ValueError("duplicate chunk_id in corpus")
    if len({str(record["qid"]) for record in records}) != len(records):
        raise ValueError("duplicate qid in golden set")

    documents = {str(chunk["chunk_id"]): str(chunk["retrieval_text"]) for chunk in chunks}
    document_ids = [str(chunk["chunk_id"]) for chunk in chunks]
    document_texts = {str(chunk["chunk_id"]): str(chunk["retrieval_text"]) for chunk in chunks}
    bm25 = BM25Index(documents)
    document_embeddings = np.load(document_embeddings_path)
    if document_embeddings.ndim != 2 or document_embeddings.shape[0] != len(document_ids):
        raise ValueError("document embeddings do not match corpus")

    resolved_device = device
    if device == "auto":
        resolved_device = "cuda" if torch.cuda.is_available() else "cpu"
    if resolved_device == "cuda" and not torch.cuda.is_available():
        raise ValueError("CUDA requested but unavailable")

    dense_model = SentenceTransformer(
        DENSE_MODEL_ID,
        revision=DENSE_MODEL_REVISION,
        device=resolved_device,
        trust_remote_code=False,
    )
    dense_model.max_seq_length = 512
    reranker = CrossEncoder(
        RERANKER_MODEL_ID,
        revision=RERANKER_MODEL_REVISION,
        max_length=512,
        device=resolved_device,
        trust_remote_code=False,
    )

    def synchronize() -> None:
        """Espera a que terminen las operaciones CUDA antes de delimitar cada medición."""
        if resolved_device == "cuda":
            torch.cuda.synchronize()

    def dense_rank(question: str) -> list[tuple[str, float]]:
        """Ordena los fragmentos por similitud densa con desempate por identificador."""
        query_embedding = dense_model.encode(
            [f"query: {question}"],
            batch_size=dense_batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )[0]
        scores = document_embeddings @ np.asarray(query_embedding, dtype=np.float32)
        ranking = [
            (document_id, float(score))
            for document_id, score in zip(document_ids, scores, strict=True)
        ]
        ranking.sort(key=lambda item: (-item[1], item[0]))
        return ranking[:top_k]

    def execute(question: str) -> dict[str, float]:
        """Cronometra BM25, búsqueda densa, fusión y reranking para una pregunta."""
        started = time.perf_counter_ns()
        bm25_ranking = bm25.rank(question, top_k=top_k)
        bm25_ms = (time.perf_counter_ns() - started) / 1_000_000

        synchronize()
        started = time.perf_counter_ns()
        dense_ranking = dense_rank(question)
        synchronize()
        dense_ms = (time.perf_counter_ns() - started) / 1_000_000

        started = time.perf_counter_ns()
        hybrid_ranking = reciprocal_rank_fusion(
            [
                [chunk_id for chunk_id, _ in bm25_ranking],
                [chunk_id for chunk_id, _ in dense_ranking],
            ],
            k0=60,
            top_k=top_k,
        )
        fusion_ms = (time.perf_counter_ns() - started) / 1_000_000

        pairs = [
            [question, document_texts[chunk_id]]
            for chunk_id, _ in hybrid_ranking
        ]
        synchronize()
        started = time.perf_counter_ns()
        reranker.predict(
            pairs,
            batch_size=reranker_batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
        )
        synchronize()
        rerank_ms = (time.perf_counter_ns() - started) / 1_000_000
        return {
            "bm25_ms": bm25_ms,
            "dense_ms": dense_ms,
            "fusion_ms": fusion_ms,
            "rerank_ms": rerank_ms,
        }

    # El calentamiento usa las mismas etapas, pero sus tiempos no entran en las muestras.
    rng = random.Random(seed)
    for _ in range(warmup_rounds):
        warmup_records = list(records)
        rng.shuffle(warmup_records)
        for record in warmup_records:
            execute(str(record["question"]))

    stage_rows: list[dict[str, Any]] = []
    for repetition in range(1, repetitions + 1):
        repetition_records = list(records)
        rng.shuffle(repetition_records)
        for order, record in enumerate(repetition_records, start=1):
            stages = execute(str(record["question"]))
            hybrid_ms = stages["bm25_ms"] + stages["dense_ms"] + stages["fusion_ms"]
            stage_rows.append(
                {
                    "benchmark_id": benchmark_id,
                    "repetition": repetition,
                    "query_order": order,
                    "qid": str(record["qid"]),
                    **stages,
                    "hybrid_rrf_serial_ms": hybrid_ms,
                    "hybrid_rrf_rerank_serial_ms": hybrid_ms + stages["rerank_ms"],
                }
            )

    condition_samples = build_condition_samples(stage_rows)
    condition_rows = [
        {"benchmark_id": benchmark_id, "condition": condition, **summarize_latencies(values)}
        for condition, values in condition_samples.items()
    ]
    latency_dir = output_root / "latency"
    raw_path = latency_dir / f"{benchmark_id}_raw.csv"
    summary_csv_path = latency_dir / f"{benchmark_id}_summary.csv"
    summary_json_path = latency_dir / f"{benchmark_id}_summary.json"
    _write_csv(
        raw_path,
        stage_rows,
        (
            "benchmark_id",
            "repetition",
            "query_order",
            "qid",
            "bm25_ms",
            "dense_ms",
            "fusion_ms",
            "rerank_ms",
            "hybrid_rrf_serial_ms",
            "hybrid_rrf_rerank_serial_ms",
        ),
    )
    _write_csv(
        summary_csv_path,
        condition_rows,
        (
            "benchmark_id",
            "condition",
            "sample_count",
            "mean_ms",
            "median_ms",
            "p95_ms",
            "std_ms",
            "min_ms",
            "max_ms",
        ),
    )
    summary: dict[str, Any] = {
        "benchmark_id": benchmark_id,
        "protocol": "integrated_serial_query_latency_v1",
        "warmup_rounds": warmup_rounds,
        "repetitions": repetitions,
        "seed": seed,
        "query_count": len(records),
        "sample_count_per_condition": len(records) * repetitions,
        "top_k": top_k,
        "fusion": {"method": "rrf", "k0": 60},
        "timing": {
            "clock": "time.perf_counter_ns",
            "cuda_synchronization": resolved_device == "cuda",
            "models_and_indices_preloaded": True,
            "condition_execution": "serial",
        },
        "hardware": {
            "platform": platform.platform(),
            "device": resolved_device,
            "gpu": torch.cuda.get_device_name(0) if resolved_device == "cuda" else None,
        },
        "models": {
            "dense": {
                "model_id": DENSE_MODEL_ID,
                "revision": DENSE_MODEL_REVISION,
                "batch_size": dense_batch_size,
                "max_seq_length": 512,
            },
            "reranker": {
                "model_id": RERANKER_MODEL_ID,
                "revision": RERANKER_MODEL_REVISION,
                "batch_size": reranker_batch_size,
                "max_seq_length": 512,
            },
        },
        "versions": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "torch": torch.__version__,
            "sentence_transformers": sentence_transformers.__version__,
        },
        "inputs": {
            "chunks_path": str(chunks_path),
            "chunks_sha256": _sha256(chunks_path),
            "golden_path": str(golden_path),
            "golden_sha256": _sha256(golden_path),
            "document_embeddings_path": str(document_embeddings_path),
            "document_embeddings_sha256": _sha256(document_embeddings_path),
        },
        "conditions": {row["condition"]: {k: v for k, v in row.items() if k not in {"benchmark_id", "condition"}} for row in condition_rows},
        "raw_output_path": str(raw_path),
        "summary_csv_path": str(summary_csv_path),
    }
    summary_json_path.parent.mkdir(parents=True, exist_ok=True)
    summary_json_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def build_parser(root: Path) -> argparse.ArgumentParser:
    """Define las rutas y los parámetros del protocolo de latencia controlada."""
    parser = argparse.ArgumentParser(description="Benchmark controlled retrieval latency")
    parser.add_argument("--benchmark-id", default="retrieval_latency_controlled_v1_22q")
    parser.add_argument("--chunks", type=Path, default=root / "data/processed/chunks_v1.jsonl")
    parser.add_argument("--golden", type=Path, default=root / "data/golden/golden_set_pilot_v1.jsonl")
    parser.add_argument(
        "--document-embeddings",
        type=Path,
        default=root / "outputs/embeddings/dense_e5_base_v2_pooled_v1_22q_documents.npy",
    )
    parser.add_argument("--output-root", type=Path, default=root / "outputs")
    parser.add_argument("--warmup-rounds", type=int, default=5)
    parser.add_argument("--repetitions", type=int, default=30)
    parser.add_argument("--seed", type=int, default=20260831)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--dense-batch-size", type=int, default=1)
    parser.add_argument("--reranker-batch-size", type=int, default=16)
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    return parser


def main() -> int:
    """Ejecuta el benchmark de recuperación con las salidas protegidas."""
    root = Path(__file__).resolve().parents[1]
    args = build_parser(root).parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="benchmark_retrieval_latency")
    summary = run_benchmark(
        benchmark_id=args.benchmark_id,
        chunks_path=args.chunks,
        golden_path=args.golden,
        document_embeddings_path=args.document_embeddings,
        output_root=args.output_root,
        warmup_rounds=args.warmup_rounds,
        repetitions=args.repetitions,
        seed=args.seed,
        top_k=args.top_k,
        dense_batch_size=args.dense_batch_size,
        reranker_batch_size=args.reranker_batch_size,
        device=args.device,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
