from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import statistics
import sys
import time
from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from run_bm25 import _load_jsonl, _load_qrels_tsv, _write_csv, evaluate_ranking


def reciprocal_rank_fusion(
    rankings: Sequence[Sequence[str]], *, k0: int = 60, top_k: int = 10
) -> list[tuple[str, float]]:
    """Fusiona rankings sumando rangos recíprocos sin repetir documentos dentro de cada lista."""
    if k0 <= 0:
        raise ValueError("k0 must be positive")
    if top_k <= 0:
        raise ValueError("top_k must be positive")
    scores: dict[str, float] = {}
    for ranking in rankings:
        seen: set[str] = set()
        for rank, chunk_id in enumerate(ranking[:top_k], start=1):
            if chunk_id in seen:
                continue
            seen.add(chunk_id)
            scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (k0 + rank)
    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))[:top_k]


def _sha256(path: Path) -> str:
    """Calcula la huella SHA-256 leyendo el archivo por bloques."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _load_run(path: Path) -> tuple[str, dict[str, list[dict[str, Any]]]]:
    """Carga una run y valida rangos contiguos e identificadores únicos por pregunta."""
    rows = _load_jsonl(path)
    if not rows:
        raise ValueError(f"Run is empty: {path}")
    run_ids = {str(row["run_id"]) for row in rows}
    if len(run_ids) != 1:
        raise ValueError(f"Expected one run_id in {path}, found {sorted(run_ids)}")
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["qid"])].append(row)
    for qid, qid_rows in grouped.items():
        qid_rows.sort(key=lambda row: int(row["rank"]))
        ranks = [int(row["rank"]) for row in qid_rows]
        if ranks != list(range(1, len(ranks) + 1)):
            raise ValueError(f"Non-contiguous ranks for {qid} in {path}")
        chunk_ids = [str(row["chunk_id"]) for row in qid_rows]
        if len(chunk_ids) != len(set(chunk_ids)):
            raise ValueError(f"Duplicate chunk_id for {qid} in {path}")
    return run_ids.pop(), dict(grouped)


def _source_latency(rows: Sequence[Mapping[str, Any]]) -> float:
    """Obtiene la latencia común de las filas de una consulta fuente."""
    values = {float(row["query_latency_ms"]) for row in rows}
    if len(values) != 1:
        raise ValueError("All rows for a source query must share query_latency_ms")
    return values.pop()


def build_incremental_pool(
    *,
    run_path: Path,
    qrels_path: Path,
    prior_pool_path: Path,
    pool_path: Path,
    report_path: Path,
) -> dict[str, Any]:
    """Extrae candidatos ausentes del pool previo y documenta sus fuentes."""
    rows = _load_jsonl(run_path)
    prior_pool = _load_jsonl(prior_pool_path)
    prior_pairs = {
        (str(row["qid"]), str(row["chunk_id"])) for row in prior_pool
    }
    new_rows = [
        {
            "pool_status": "unjudged",
            "source_run_id": row["run_id"],
            "qid": row["qid"],
            "question": row["question"],
            "answerability": row["answerability"],
            "chunk_id": row["chunk_id"],
            "hybrid_rank": row["rank"],
            "hybrid_score": row["score"],
            "bm25_rank": row.get("bm25_rank"),
            "dense_rank": row.get("dense_rank"),
        }
        for row in rows
        if (str(row["qid"]), str(row["chunk_id"])) not in prior_pairs
    ]
    pool_path.parent.mkdir(parents=True, exist_ok=True)
    pool_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in new_rows),
        encoding="utf-8",
    )
    report = {
        "source_run_path": str(run_path),
        "source_run_sha256": _sha256(run_path),
        "qrels_path": str(qrels_path),
        "qrels_sha256": _sha256(qrels_path),
        "prior_pool_path": str(prior_pool_path),
        "prior_pool_sha256": _sha256(prior_pool_path),
        "prior_pool_candidate_count": len(prior_pairs),
        "candidate_count": len(rows),
        "existing_prior_pool_count": len(rows) - len(new_rows),
        "new_candidate_count": len(new_rows),
        "new_candidate_qid_count": len({str(row["qid"]) for row in new_rows}),
        "criterion": "(qid, chunk_id) absent from prior technical pool",
        "pool_path": str(pool_path),
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


def run_experiment(
    *,
    run_id: str,
    bm25_run_path: Path,
    dense_run_path: Path,
    golden_path: Path,
    qrels_path: Path,
    output_root: Path,
    k0: int = 60,
    top_k: int = 10,
    cutoffs: Sequence[int] = (5, 10),
    chunks_path: Path | None = None,
) -> dict[str, Any]:
    """Fusiona las runs BM25 y densa y exporta métricas y auditoría de posiciones."""
    from output_safety import guard_run_outputs
    guard_run_outputs(output_root, run_id)
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", run_id):
        raise ValueError("run_id must contain only letters, digits, dot, underscore or hyphen")
    records = _load_jsonl(golden_path)
    qrels = _load_qrels_tsv(qrels_path)
    bm25_run_id, bm25 = _load_run(bm25_run_path)
    dense_run_id, dense = _load_run(dense_run_path)
    record_qids = [str(record["qid"]) for record in records]
    expected_qids = set(record_qids)
    for method, source in (("bm25", bm25), ("dense", dense)):
        if set(source) != expected_qids:
            missing = sorted(expected_qids - set(source))
            extra = sorted(set(source) - expected_qids)
            raise ValueError(f"{method} qid mismatch: missing={missing}, extra={extra}")

    run_rows: list[dict[str, Any]] = []
    per_query_rows: list[dict[str, Any]] = []
    audit_queries: list[dict[str, Any]] = []
    metrics_by_query: dict[str, dict[int, dict[str, float | None]]] = {}
    fusion_latencies: list[float] = []
    serial_latencies: list[float] = []
    parallel_latencies: list[float] = []

    for record in records:
        qid = str(record["qid"])
        bm25_rows = bm25[qid]
        dense_rows = dense[qid]
        for source_row in (bm25_rows[0], dense_rows[0]):
            if source_row["question"] != record["question"]:
                raise ValueError(f"Question mismatch for {qid}")
            if source_row["answerability"] != record["answerability"]:
                raise ValueError(f"Answerability mismatch for {qid}")
        bm25_ids = [str(row["chunk_id"]) for row in bm25_rows]
        dense_ids = [str(row["chunk_id"]) for row in dense_rows]
        fusion_started = time.perf_counter()
        ranking = reciprocal_rank_fusion(
            [bm25_ids, dense_ids], k0=k0, top_k=top_k
        )
        fusion_latency_ms = (time.perf_counter() - fusion_started) * 1000
        bm25_latency_ms = _source_latency(bm25_rows)
        dense_latency_ms = _source_latency(dense_rows)
        serial_latency_ms = bm25_latency_ms + dense_latency_ms + fusion_latency_ms
        # Son estimaciones a partir de latencias fuente, no ejecuciones paralelas medidas.
        parallel_latency_ms = max(bm25_latency_ms, dense_latency_ms) + fusion_latency_ms
        fusion_latencies.append(fusion_latency_ms)
        serial_latencies.append(serial_latency_ms)
        parallel_latencies.append(parallel_latency_ms)

        ranked_ids = [chunk_id for chunk_id, _ in ranking]
        query_qrels = qrels.get(qid, {})
        metrics_by_query[qid] = {
            cutoff: evaluate_ranking(ranked_ids, query_qrels, k=cutoff)
            for cutoff in cutoffs
        }
        source_ranks = {
            "bm25": {str(row["chunk_id"]): int(row["rank"]) for row in bm25_rows},
            "dense": {str(row["chunk_id"]): int(row["rank"]) for row in dense_rows},
        }
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
                    "bm25_rank": source_ranks["bm25"].get(chunk_id),
                    "dense_rank": source_ranks["dense"].get(chunk_id),
                    "relevant_grade": query_qrels.get(chunk_id, 0),
                    "is_relevant": query_qrels.get(chunk_id) == 2,
                    "fusion_latency_ms": fusion_latency_ms,
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
            "fusion_latency_ms": fusion_latency_ms,
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
                "qrel_ranks": [
                    {
                        "chunk_id": chunk_id,
                        "relevance_grade": grade,
                        "hybrid_rank": ranked_ids.index(chunk_id) + 1
                        if chunk_id in ranked_ids
                        else None,
                        "bm25_rank": source_ranks["bm25"].get(chunk_id),
                        "dense_rank": source_ranks["dense"].get(chunk_id),
                    }
                    for chunk_id, grade in sorted(query_qrels.items())
                ],
            }
        )

    runs_path = output_root / "runs" / f"{run_id}.jsonl"
    metrics_dir = output_root / "metrics"
    runs_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_dir.mkdir(parents=True, exist_ok=True)
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
            "fusion_latency_ms",
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

    source_candidate_ids = {
        str(row["chunk_id"])
        for source in (bm25, dense)
        for rows in source.values()
        for row in rows
    }
    summary: dict[str, Any] = {
        "run_id": run_id,
        "method": "hybrid_rrf",
        "source_run_ids": [bm25_run_id, dense_run_id],
        "source_run_paths": [str(bm25_run_path), str(dense_run_path)],
        "source_run_sha256": {
            "bm25": _sha256(bm25_run_path),
            "dense": _sha256(dense_run_path),
        },
        "golden_set_path": str(golden_path),
        "golden_set_sha256": _sha256(golden_path),
        "qrels_source_path": str(qrels_path),
        "qrels_sha256": _sha256(qrels_path),
        "query_count": len(records),
        "metric_query_count": len(metric_qids),
        "unanswerable_query_count": sum(
            record["answerability"] == "unanswerable" for record in records
        ),
        "source_candidate_count": len(source_candidate_ids),
        "k0": k0,
        "fusion_depth": top_k,
        "cutoffs": list(cutoffs),
        "binary_relevance_grade": 2,
        "ndcg_relevance_grades": [0, 1, 2],
        "tie_break": "descending_rrf_score_then_ascending_chunk_id",
        "latency_interpretation": "estimated_from_recorded_source_query_latencies_plus_measured_fusion",
        "total_fusion_latency_ms": sum(fusion_latencies),
        "mean_fusion_latency_ms": statistics.fmean(fusion_latencies),
        "mean_query_latency_serial_estimate_ms": statistics.fmean(serial_latencies),
        "mean_query_latency_parallel_estimate_ms": statistics.fmean(parallel_latencies),
    }
    if chunks_path is not None:
        chunks = _load_jsonl(chunks_path)
        summary["document_count"] = len(chunks)
        summary["chunks_path"] = str(chunks_path)
        summary["chunks_sha256"] = _sha256(chunks_path)
    summary_path = metrics_dir / f"{run_id}_summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def build_parser(root: Path) -> argparse.ArgumentParser:
    """Define las runs fuente, los qrels y los parámetros de fusión RRF."""
    parser = argparse.ArgumentParser(
        description="Fuse BM25 and dense rankings with Reciprocal Rank Fusion"
    )
    parser.add_argument(
        "--bm25-run",
        type=Path,
        default=root / "outputs/runs/bm25_pooled_v1_22q.jsonl",
    )
    parser.add_argument(
        "--dense-run",
        type=Path,
        default=root / "outputs/runs/dense_e5_base_v2_pooled_v1_22q.jsonl",
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
    parser.add_argument(
        "--chunks",
        type=Path,
        default=root / "data/processed/chunks_v1.jsonl",
    )
    parser.add_argument("--output-root", type=Path, default=root / "outputs")
    parser.add_argument("--run-id", default="hybrid_rrf_k60_pooled_v1_22q")
    parser.add_argument("--k0", type=int, default=60)
    parser.add_argument("--top-k", type=int, default=10)
    return parser


def main() -> int:
    """Ejecuta la fusión híbrida y muestra el resumen de la nueva run."""
    root = Path(__file__).resolve().parents[1]
    args = build_parser(root).parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="run_hybrid_rrf")
    summary = run_experiment(
        run_id=args.run_id,
        bm25_run_path=args.bm25_run,
        dense_run_path=args.dense_run,
        golden_path=args.golden,
        qrels_path=args.qrels,
        chunks_path=args.chunks,
        output_root=args.output_root,
        k0=args.k0,
        top_k=args.top_k,
        cutoffs=(5, 10),
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
