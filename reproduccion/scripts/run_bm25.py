from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import statistics
import time
from collections import Counter
from collections.abc import Mapping
from pathlib import Path
from typing import Any


TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    """Extrae términos alfanuméricos en minúsculas con el patrón fijado para BM25."""
    return TOKEN_PATTERN.findall(text.lower())


def _dcg(grades: list[int]) -> float:
    """Calcula la ganancia graduada acumulada con descuento logarítmico."""
    return sum(
        (2**grade - 1) / math.log2(rank + 1)
        for rank, grade in enumerate(grades, start=1)
    )


def evaluate_ranking(
    ranking: list[str], qrels: Mapping[str, int], *, k: int
) -> dict[str, float | None]:
    """Evalúa el top-k con relevancia estricta de grado 2 y nDCG graduado."""
    if not qrels:
        return {"precision": None, "recall": None, "mrr": None, "ndcg": None}
    retrieved = ranking[:k]
    strict_relevant = {
        document_id for document_id, grade in qrels.items() if grade == 2
    }
    retrieved_relevant = [
        document_id for document_id in retrieved if document_id in strict_relevant
    ]
    first_relevant_rank = next(
        (
            rank
            for rank, document_id in enumerate(retrieved, start=1)
            if document_id in strict_relevant
        ),
        None,
    )
    grades = [qrels.get(document_id, 0) for document_id in retrieved]
    ideal_grades = sorted(qrels.values(), reverse=True)[:k]
    ideal_dcg = _dcg(ideal_grades)
    return {
        "precision": len(retrieved_relevant) / k,
        "recall": (
            None
            if not strict_relevant
            else len(retrieved_relevant) / len(strict_relevant)
        ),
        "mrr": 0.0 if first_relevant_rank is None else 1 / first_relevant_rank,
        "ndcg": 0.0 if ideal_dcg == 0 else _dcg(grades) / ideal_dcg,
    }


class BM25Index:
    def __init__(
        self,
        documents: Mapping[str, str],
        *,
        k1: float = 1.5,
        b: float = 0.75,
    ) -> None:
        """Construye las frecuencias y longitudes del índice BM25 con sus parámetros."""
        if not documents:
            raise ValueError("BM25 requires at least one document")
        self.k1 = k1
        self.b = b
        self.document_ids = sorted(documents)
        self.term_frequencies = {
            document_id: Counter(tokenize(documents[document_id]))
            for document_id in self.document_ids
        }
        self.document_lengths = {
            document_id: sum(frequencies.values())
            for document_id, frequencies in self.term_frequencies.items()
        }
        self.average_document_length = sum(self.document_lengths.values()) / len(
            self.document_ids
        )
        document_frequencies: Counter[str] = Counter()
        for frequencies in self.term_frequencies.values():
            document_frequencies.update(frequencies.keys())
        document_count = len(self.document_ids)
        self.idf = {
            term: math.log(
                1
                + (document_count - frequency + 0.5)
                / (frequency + 0.5)
            )
            for term, frequency in document_frequencies.items()
        }

    def score(self, query: str, document_id: str) -> float:
        """Calcula BM25 para un documento con saturación y normalización de longitud."""
        query_frequencies = Counter(tokenize(query))
        frequencies = self.term_frequencies[document_id]
        document_length = self.document_lengths[document_id]
        score = 0.0
        for term, query_frequency in query_frequencies.items():
            term_frequency = frequencies.get(term, 0)
            if term_frequency == 0:
                continue
            length_normalization = self.k1 * (
                1
                - self.b
                + self.b * document_length / self.average_document_length
            )
            score += (
                query_frequency
                * self.idf[term]
                * term_frequency
                * (self.k1 + 1)
                / (term_frequency + length_normalization)
            )
        return score

    def rank(self, query: str, *, top_k: int) -> list[tuple[str, float]]:
        """Ordena los documentos por BM25 y desempata por identificador ascendente."""
        ranking = [
            (document_id, self.score(query, document_id))
            for document_id in self.document_ids
        ]
        ranking.sort(key=lambda item: (-item[1], item[0]))
        return ranking[:top_k]


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Carga los registros JSONL omitiendo líneas vacías."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _build_qrels(records: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    """Deriva qrels positivos del golden set conservando el mayor grado por fragmento."""
    qrels: dict[str, dict[str, int]] = {}
    for record in records:
        qid = record["qid"]
        qrels[qid] = {}
        for evidence in record["evidence"]:
            grade = int(evidence["relevance_grade"])
            if grade > 0:
                chunk_id = evidence["chunk_id"]
                qrels[qid][chunk_id] = max(qrels[qid].get(chunk_id, 0), grade)
    return qrels


def _load_qrels_tsv(path: Path) -> dict[str, dict[str, int]]:
    """Lee qrels TSV con grados 1 o 2 y rechaza claves duplicadas."""
    qrels: dict[str, dict[str, int]] = {}
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        fields = line.split("\t")
        if len(fields) != 4 or fields[1] != "0":
            raise ValueError(f"invalid qrel at line {line_number}")
        qid, _, chunk_id, raw_grade = fields
        grade = int(raw_grade)
        if grade not in (1, 2):
            raise ValueError(f"qrel grade must be 1 or 2 at line {line_number}")
        if chunk_id in qrels.setdefault(qid, {}):
            raise ValueError(f"duplicate qrel at line {line_number}: {qid}/{chunk_id}")
        qrels[qid][chunk_id] = grade
    return qrels


def _sha256(path: Path) -> str:
    """Calcula la huella SHA-256 del archivo de qrels utilizado."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    """Escribe las filas CSV con las columnas indicadas y saltos de línea uniformes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def run_experiment(
    *,
    run_id: str,
    chunks_path: Path,
    golden_path: Path,
    output_root: Path,
    qrels_path: Path,
    k1: float,
    b: float,
    top_k: int,
    cutoffs: tuple[int, ...],
    qrels_input_path: Path | None = None,
) -> dict[str, Any]:
    """Ejecuta BM25 y exporta rankings, métricas y trazabilidad de los qrels."""
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", run_id):
        raise ValueError("run_id must contain only letters, digits, dot, underscore or hyphen")
    from output_safety import guard_run_outputs
    guard_run_outputs(output_root, run_id, qrels_path if qrels_input_path is None else None)
    if top_k < 1 or any(cutoff < 1 or cutoff > top_k for cutoff in cutoffs):
        raise ValueError("cutoffs must be between 1 and top_k")
    chunks = _load_jsonl(chunks_path)
    records = _load_jsonl(golden_path)
    if any(record["annotation_status"] != "adjudicated" for record in records):
        raise ValueError("BM25 requires adjudicated golden-set records")
    documents = {chunk["chunk_id"]: chunk["retrieval_text"] for chunk in chunks}
    if len(documents) != len(chunks):
        raise ValueError("duplicate chunk_id in corpus")

    build_started = time.perf_counter()
    index = BM25Index(documents, k1=k1, b=b)
    build_latency_ms = (time.perf_counter() - build_started) * 1000
    record_qids = {record["qid"] for record in records}
    if qrels_input_path is None:
        qrels = _build_qrels(records)
        qrels_path.parent.mkdir(parents=True, exist_ok=True)
        qrels_lines = [
            f"{qid}\t0\t{chunk_id}\t{grade}\n"
            for qid in sorted(qrels)
            for chunk_id, grade in sorted(qrels[qid].items())
        ]
        qrels_path.write_text("".join(qrels_lines), encoding="utf-8")
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
            if chunk_id not in documents
        }
        if unknown_chunks:
            raise ValueError(f"qrels contain unknown chunks: {sorted(unknown_chunks)}")
        qrels_source = "external_tsv"
        resolved_qrels_path = qrels_input_path
    for qid in record_qids:
        qrels.setdefault(qid, {})

    run_rows: list[dict[str, Any]] = []
    per_query_rows: list[dict[str, Any]] = []
    metrics_by_query: dict[str, dict[int, dict[str, float | None]]] = {}
    query_latencies: list[float] = []

    for record in records:
        qid = record["qid"]
        query_started = time.perf_counter()
        ranking = index.rank(record["question"], top_k=top_k)
        query_latency_ms = (time.perf_counter() - query_started) * 1000
        query_latencies.append(query_latency_ms)
        ranked_ids = [chunk_id for chunk_id, _ in ranking]
        metrics_by_query[qid] = {
            cutoff: evaluate_ranking(ranked_ids, qrels[qid], k=cutoff)
            for cutoff in cutoffs
        }
        first_relevant_rank = next(
            (
                rank
                for rank, chunk_id in enumerate(ranked_ids, start=1)
                if qrels[qid].get(chunk_id) == 2
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
            "relevant_count": sum(grade == 2 for grade in qrels[qid].values()),
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
    # La media incluye solo preguntas respondibles con evidencia conocida de grado 2.
    metric_qids = [
        record["qid"]
        for record in records
        if record["answerability"] == "answerable"
        and any(grade == 2 for grade in qrels[record["qid"]].values())
    ]
    aggregate_rows: list[dict[str, Any]] = []
    for cutoff in cutoffs:
        for metric in metric_names:
            values = [
                metrics_by_query[qid][cutoff][metric]
                for qid in metric_qids
            ]
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
        "tokenizer": TOKEN_PATTERN.pattern,
        "k1": k1,
        "b": b,
        "top_k": top_k,
        "cutoffs": list(cutoffs),
        "binary_relevance_grade": 2,
        "ndcg_relevance_grades": [0, 1, 2],
        "index_build_latency_ms": build_latency_ms,
        "total_query_latency_ms": sum(query_latencies),
        "mean_query_latency_ms": statistics.fmean(query_latencies),
        "vocabulary_size": len(index.idf),
        "corpus_token_count": sum(index.document_lengths.values()),
    }
    summary_path = output_root / "metrics" / f"{run_id}_summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def build_parser(root: Path) -> argparse.ArgumentParser:
    """Define las entradas, salidas y parámetros de la línea base BM25."""
    parser = argparse.ArgumentParser(description="Run the reproducible BM25 v1 baseline")
    parser.add_argument(
        "--chunks", type=Path, default=root / "data/processed/chunks_v1.jsonl"
    )
    parser.add_argument(
        "--golden", type=Path, default=root / "data/golden/golden_set_pilot_v1.jsonl"
    )
    parser.add_argument("--output-root", type=Path, default=root / "outputs")
    parser.add_argument("--run-id", default="bm25_v1_22q")
    parser.add_argument(
        "--qrels", type=Path, default=root / "data/golden/qrels_bm25_v1_22q.tsv"
    )
    parser.add_argument(
        "--qrels-input",
        type=Path,
        default=None,
        help="Read method-independent qrels from this TSV instead of rebuilding them",
    )
    parser.add_argument("--k1", type=float, default=1.5)
    parser.add_argument("--b", type=float, default=0.75)
    parser.add_argument("--top-k", type=int, default=10)
    return parser


def main() -> int:
    """Ejecuta la línea base BM25 con los argumentos y destinos validados."""
    root = Path(__file__).resolve().parents[1]
    parser = build_parser(root)
    args = parser.parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="run_bm25")
    summary = run_experiment(
        run_id=args.run_id,
        chunks_path=args.chunks,
        golden_path=args.golden,
        output_root=args.output_root,
        qrels_path=args.qrels,
        k1=args.k1,
        b=args.b,
        top_k=args.top_k,
        cutoffs=(5, 10),
        qrels_input_path=args.qrels_input,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
