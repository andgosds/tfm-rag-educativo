from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import statistics
import sys
import time
from collections import defaultdict
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from run_bm25 import _load_jsonl, _load_qrels_tsv, _write_csv, evaluate_ranking


DEFAULT_MODEL_ID = "cross-encoder/ms-marco-MiniLM-L6-v2"
DEFAULT_MODEL_REVISION = "233902d25c440f23af6f7d6e94d2946bac0bee0a"


def rerank_candidates(
    question: str,
    candidates: Sequence[Mapping[str, object]],
    *,
    score_pairs: Callable[[list[list[str]]], Sequence[float]],
) -> list[tuple[str, float]]:
    """Reordena candidatos con puntuaciones pregunta-pasaje y desempate por identificador."""
    pairs = [[question, str(candidate["retrieval_text"])] for candidate in candidates]
    scores = score_pairs(pairs)
    if len(scores) != len(candidates):
        raise ValueError("score count does not match candidate count")
    ranking = [
        (str(candidate["chunk_id"]), float(score))
        for candidate, score in zip(candidates, scores)
    ]
    return sorted(ranking, key=lambda item: (-item[1], item[0]))


def _sha256(path: Path) -> str:
    """Calcula la huella SHA-256 de un archivo mediante lectura por bloques."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _load_hybrid_run(path: Path) -> tuple[str, dict[str, list[dict[str, Any]]]]:
    """Carga la run híbrida y valida unicidad, continuidad de rangos y profundidad común."""
    rows = _load_jsonl(path)
    if not rows:
        raise ValueError(f"Run is empty: {path}")
    run_ids = {str(row["run_id"]) for row in rows}
    if len(run_ids) != 1:
        raise ValueError(f"Expected one run_id in {path}, found {sorted(run_ids)}")
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["qid"])].append(row)
    depths = set()
    for qid, qid_rows in grouped.items():
        qid_rows.sort(key=lambda row: int(row["rank"]))
        ranks = [int(row["rank"]) for row in qid_rows]
        if ranks != list(range(1, len(ranks) + 1)):
            raise ValueError(f"Non-contiguous ranks for {qid} in {path}")
        chunk_ids = [str(row["chunk_id"]) for row in qid_rows]
        if len(chunk_ids) != len(set(chunk_ids)):
            raise ValueError(f"Duplicate chunk_id for {qid} in {path}")
        depths.add(len(qid_rows))
    if len(depths) != 1:
        raise ValueError(f"Inconsistent candidate depth in {path}: {sorted(depths)}")
    return run_ids.pop(), dict(grouped)


def _single_latency(rows: Sequence[Mapping[str, Any]], field: str) -> float:
    """Obtiene una latencia fuente comprobando que sea común a todas las filas."""
    values = {float(row[field]) for row in rows}
    if len(values) != 1:
        raise ValueError(f"All source rows must share {field}")
    return values.pop()


def run_experiment(
    *,
    run_id: str,
    hybrid_run_path: Path,
    chunks_path: Path,
    golden_path: Path,
    qrels_path: Path,
    output_root: Path,
    score_pairs: Callable[[list[list[str]]], Sequence[float]],
    count_pair_tokens: Callable[[list[list[str]]], Sequence[int]],
    model_id: str,
    model_revision: str,
    max_seq_length: int,
    batch_size: int,
    device: str,
    model_load_latency_ms: float,
    cutoffs: Sequence[int] = (5, 10),
    package_versions: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Reordena la run híbrida y exporta métricas, latencias y diagnósticos de truncamiento."""
    from output_safety import guard_run_outputs
    guard_run_outputs(output_root, run_id)
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", run_id):
        raise ValueError("run_id must contain only letters, digits, dot, underscore or hyphen")
    chunks = _load_jsonl(chunks_path)
    chunk_by_id = {str(chunk["chunk_id"]): chunk for chunk in chunks}
    if len(chunk_by_id) != len(chunks):
        raise ValueError("Duplicate chunk_id in corpus")
    records = _load_jsonl(golden_path)
    qrels = _load_qrels_tsv(qrels_path)
    source_run_id, source = _load_hybrid_run(hybrid_run_path)
    record_qids = [str(record["qid"]) for record in records]
    if set(source) != set(record_qids):
        raise ValueError("Hybrid run qids do not match golden set")
    candidate_depth = len(next(iter(source.values())))

    run_rows: list[dict[str, Any]] = []
    per_query_rows: list[dict[str, Any]] = []
    audit_queries: list[dict[str, Any]] = []
    metrics_by_query: dict[str, dict[int, dict[str, float | None]]] = {}
    rerank_latencies: list[float] = []
    serial_latencies: list[float] = []
    parallel_latencies: list[float] = []
    token_lengths: list[int] = []

    for record in records:
        qid = str(record["qid"])
        source_rows = source[qid]
        if source_rows[0]["question"] != record["question"]:
            raise ValueError(f"Question mismatch for {qid}")
        if source_rows[0]["answerability"] != record["answerability"]:
            raise ValueError(f"Answerability mismatch for {qid}")
        candidates = []
        source_by_chunk: dict[str, dict[str, Any]] = {}
        for row in source_rows:
            chunk_id = str(row["chunk_id"])
            if chunk_id not in chunk_by_id:
                raise ValueError(f"Unknown chunk_id in source run: {chunk_id}")
            source_by_chunk[chunk_id] = row
            candidates.append(
                {
                    "chunk_id": chunk_id,
                    "retrieval_text": chunk_by_id[chunk_id]["retrieval_text"],
                }
            )
        pairs = [
            [str(record["question"]), str(candidate["retrieval_text"])]
            for candidate in candidates
        ]
        lengths = [int(length) for length in count_pair_tokens(pairs)]
        if len(lengths) != len(pairs):
            raise ValueError("token length count does not match candidate count")
        token_lengths.extend(lengths)
        started = time.perf_counter()
        ranking = rerank_candidates(
            str(record["question"]), candidates, score_pairs=score_pairs
        )
        rerank_latency_ms = (time.perf_counter() - started) * 1000
        source_serial_ms = _single_latency(
            source_rows, "query_latency_serial_estimate_ms"
        )
        source_parallel_ms = _single_latency(
            source_rows, "query_latency_parallel_estimate_ms"
        )
        serial_latency_ms = source_serial_ms + rerank_latency_ms
        parallel_latency_ms = source_parallel_ms + rerank_latency_ms
        rerank_latencies.append(rerank_latency_ms)
        serial_latencies.append(serial_latency_ms)
        parallel_latencies.append(parallel_latency_ms)

        ranked_ids = [chunk_id for chunk_id, _ in ranking]
        # Mantener los candidatos aísla el efecto del nuevo orden frente a la recuperación.
        if set(ranked_ids) != set(source_by_chunk):
            raise ValueError(f"Reranker changed candidate set for {qid}")
        query_qrels = qrels.get(qid, {})
        metrics_by_query[qid] = {
            cutoff: evaluate_ranking(ranked_ids, query_qrels, k=cutoff)
            for cutoff in cutoffs
        }
        for rank, (chunk_id, rerank_score) in enumerate(ranking, start=1):
            source_row = source_by_chunk[chunk_id]
            run_rows.append(
                {
                    "run_id": run_id,
                    "qid": qid,
                    "question": record["question"],
                    "answerability": record["answerability"],
                    "chunk_id": chunk_id,
                    "rank": rank,
                    "score": rerank_score,
                    "rerank_score": rerank_score,
                    "source_rank": int(source_row["rank"]),
                    "source_score": float(source_row["score"]),
                    "bm25_rank": source_row.get("bm25_rank"),
                    "dense_rank": source_row.get("dense_rank"),
                    "relevant_grade": query_qrels.get(chunk_id, 0),
                    "is_relevant": query_qrels.get(chunk_id) == 2,
                    "rerank_latency_ms": rerank_latency_ms,
                    "query_latency_ms": serial_latency_ms,
                    "query_latency_serial_estimate_ms": serial_latency_ms,
                    "query_latency_parallel_estimate_ms": parallel_latency_ms,
                }
            )
        first_relevant_rank = next(
            (
                rank
                for rank, chunk_id in enumerate(ranked_ids, start=1)
                if query_qrels.get(chunk_id) == 2
            ),
            None,
        )
        per_query: dict[str, Any] = {
            "qid": qid,
            "question_type": record.get("question_type", ""),
            "answerability": record["answerability"],
            "relevant_count": sum(grade == 2 for grade in query_qrels.values()),
            "first_relevant_rank": first_relevant_rank,
            "top_score": ranking[0][1],
            "score_margin": ranking[0][1] - ranking[1][1]
            if len(ranking) > 1
            else None,
            "rerank_latency_ms": rerank_latency_ms,
            "query_latency_serial_estimate_ms": serial_latency_ms,
            "query_latency_parallel_estimate_ms": parallel_latency_ms,
        }
        for cutoff in cutoffs:
            for metric, value in metrics_by_query[qid][cutoff].items():
                per_query[f"{metric}_at_{cutoff}"] = value
        per_query_rows.append(per_query)
        audit_queries.append(
            {
                "qid": qid,
                "answerability": record["answerability"],
                "candidate_set_preserved": set(ranked_ids) == set(source_by_chunk),
                "qrel_ranks": [
                    {
                        "chunk_id": chunk_id,
                        "relevance_grade": grade,
                        "source_rank": source_by_chunk.get(chunk_id, {}).get("rank"),
                        "reranked_rank": ranked_ids.index(chunk_id) + 1
                        if chunk_id in ranked_ids
                        else None,
                    }
                    for chunk_id, grade in sorted(query_qrels.items())
                ],
            }
        )

    runs_path = output_root / "runs" / f"{run_id}.jsonl"
    metrics_dir = output_root / "metrics"
    metadata_dir = output_root / "rerankers"
    runs_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)
    runs_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in run_rows),
        encoding="utf-8",
    )

    metric_names = ("precision", "recall", "mrr", "ndcg")
    metric_qids = [
        str(record["qid"])
        for record in records
        if record["answerability"] == "answerable"
        and any(grade == 2 for grade in qrels.get(str(record["qid"]), {}).values())
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
                    "value": statistics.fmean(
                        value for value in values if value is not None
                    ),
                    "query_count": len(metric_qids),
                }
            )
    metrics_path = metrics_dir / f"{run_id}_metrics.csv"
    _write_csv(
        metrics_path,
        aggregate_rows,
        ["run_id", "query_scope", "metric", "k", "value", "query_count"],
    )
    metric_fields = [
        f"{metric}_at_{cutoff}"
        for cutoff in cutoffs
        for metric in metric_names
    ]
    per_query_path = metrics_dir / f"{run_id}_per_query.csv"
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
            "rerank_latency_ms",
            "query_latency_serial_estimate_ms",
            "query_latency_parallel_estimate_ms",
            *metric_fields,
        ],
    )
    audit_path = metrics_dir / f"{run_id}_audit.json"
    audit_path.write_text(
        json.dumps(
            {
                "run_id": run_id,
                "source_run_id": source_run_id,
                "binary_relevance_grade": 2,
                "ndcg_relevance_grades": [0, 1, 2],
                "queries": audit_queries,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    summary: dict[str, Any] = {
        "run_id": run_id,
        "method": "hybrid_cross_encoder_reranking",
        "source_run_id": source_run_id,
        "source_run_path": str(hybrid_run_path),
        "source_run_sha256": _sha256(hybrid_run_path),
        "model_id": model_id,
        "model_revision": model_revision,
        "model_license": "apache-2.0",
        "model_language": "en",
        "model_training_dataset": "sentence-transformers/msmarco",
        "max_seq_length": max_seq_length,
        "batch_size": batch_size,
        "device": device,
        "candidate_depth": candidate_depth,
        "tie_break": "descending_rerank_score_then_ascending_chunk_id",
        "document_count": len(chunks),
        "query_count": len(records),
        "metric_query_count": len(metric_qids),
        "unanswerable_query_count": sum(
            record["answerability"] == "unanswerable" for record in records
        ),
        "cutoffs": list(cutoffs),
        "binary_relevance_grade": 2,
        "ndcg_relevance_grades": [0, 1, 2],
        "chunks_path": str(chunks_path),
        "chunks_sha256": _sha256(chunks_path),
        "golden_set_path": str(golden_path),
        "golden_set_sha256": _sha256(golden_path),
        "qrels_source_path": str(qrels_path),
        "qrels_sha256": _sha256(qrels_path),
        "pair_count": len(token_lengths),
        "truncated_pair_count": sum(
            length > max_seq_length for length in token_lengths
        ),
        "max_observed_pair_tokens": max(token_lengths),
        "model_load_latency_ms": model_load_latency_ms,
        "total_rerank_latency_ms": sum(rerank_latencies),
        "mean_rerank_latency_ms": statistics.fmean(rerank_latencies),
        "mean_query_latency_serial_estimate_ms": statistics.fmean(serial_latencies),
        "mean_query_latency_parallel_estimate_ms": statistics.fmean(
            parallel_latencies
        ),
        "latency_interpretation": "measured_cross_encoder_reranking_plus_source_retrieval_estimates",
        "python_version": platform.python_version(),
        "package_versions": dict(package_versions or {}),
    }
    summary_path = metrics_dir / f"{run_id}_summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    metadata_path = metadata_dir / f"{run_id}_metadata.json"
    metadata_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def build_parser(root: Path) -> argparse.ArgumentParser:
    """Define las fuentes y la configuración del cross-encoder de reordenación."""
    parser = argparse.ArgumentParser(
        description="Rerank the frozen hybrid RRF top-10 with a cross-encoder"
    )
    parser.add_argument(
        "--hybrid-run",
        type=Path,
        default=root / "outputs/runs/hybrid_rrf_k60_pooled_v1_22q.jsonl",
    )
    parser.add_argument(
        "--chunks",
        type=Path,
        default=root / "data/processed/chunks_v1.jsonl",
    )
    parser.add_argument(
        "--golden",
        type=Path,
        default=root / "data/golden/golden_set_pilot_v1.jsonl",
    )
    parser.add_argument(
        "--qrels",
        type=Path,
        default=root / "data/golden/qrels_golden_set_pooled_v1_22q.tsv",
    )
    parser.add_argument("--output-root", type=Path, default=root / "outputs")
    parser.add_argument(
        "--run-id", default="hybrid_rrf_k60_minilm_l6_rerank_pooled_v1_22q"
    )
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID)
    parser.add_argument("--model-revision", default=DEFAULT_MODEL_REVISION)
    parser.add_argument("--max-seq-length", type=int, default=512)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--device", default="cuda")
    return parser


def main() -> int:
    """Carga el cross-encoder y ejecuta la reordenación con destinos protegidos."""
    root = Path(__file__).resolve().parents[1]
    args = build_parser(root).parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="run_reranker")
    import numpy
    import sentence_transformers
    import torch
    from sentence_transformers import CrossEncoder

    load_started = time.perf_counter()
    model = CrossEncoder(
        args.model_id,
        revision=args.model_revision,
        device=args.device,
        max_length=args.max_seq_length,
    )
    model_load_latency_ms = (time.perf_counter() - load_started) * 1000

    def score_pairs(pairs: list[list[str]]) -> Sequence[float]:
        """Puntúa por lotes los pares pregunta-pasaje con el modelo cargado."""
        return model.predict(
            pairs,
            batch_size=args.batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
        )

    def count_pair_tokens(pairs: list[list[str]]) -> Sequence[int]:
        """Cuenta los tokens de cada par sin truncar para diagnosticar pérdidas de contexto."""
        return [
            len(
                model.tokenizer(
                    pair[0],
                    pair[1],
                    add_special_tokens=True,
                    truncation=False,
                )["input_ids"]
            )
            for pair in pairs
        ]

    summary = run_experiment(
        run_id=args.run_id,
        hybrid_run_path=args.hybrid_run,
        chunks_path=args.chunks,
        golden_path=args.golden,
        qrels_path=args.qrels,
        output_root=args.output_root,
        score_pairs=score_pairs,
        count_pair_tokens=count_pair_tokens,
        model_id=args.model_id,
        model_revision=args.model_revision,
        max_seq_length=args.max_seq_length,
        batch_size=args.batch_size,
        device=args.device,
        model_load_latency_ms=model_load_latency_ms,
        cutoffs=(5, 10),
        package_versions={
            "numpy": numpy.__version__,
            "sentence_transformers": sentence_transformers.__version__,
            "torch": torch.__version__,
        },
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
