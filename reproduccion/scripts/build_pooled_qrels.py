from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Carga los registros JSONL no vacíos de una fuente de anotaciones."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _load_answerability_resolutions(
    path: Path | None,
) -> dict[str, dict[str, Any]]:
    """Valida e indexa las resoluciones de premisas refutadas por pregunta."""
    if path is None:
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    resolutions: dict[str, dict[str, Any]] = {}
    for row in payload.get("resolutions", []):
        qid = row["qid"]
        if qid in resolutions:
            raise ValueError(f"duplicate answerability resolution: {qid}")
        if row.get("decision") != "keep_unanswerable_with_contradiction_evidence":
            raise ValueError(f"unsupported answerability decision: {qid}")
        if row.get("expected_response_behavior") != "grounded_correction":
            raise ValueError(f"invalid expected response behavior: {qid}")
        if row.get("evidence_role") != "contradiction":
            raise ValueError(f"invalid evidence role: {qid}")
        if not row.get("evidence_chunk_ids"):
            raise ValueError(f"answerability resolution without evidence: {qid}")
        resolutions[qid] = row
    return resolutions


def _sha256(path: Path) -> str:
    """Calcula el SHA-256 del archivo para el informe de procedencia."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _atomic_write(path: Path, content: str) -> None:
    """Guarda el contenido mediante un temporal sincronizado y un reemplazo atómico."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def _load_qrels(path: Path) -> dict[tuple[str, str], int]:
    """Lee los qrels positivos y rechaza grados, formatos o pares duplicados inválidos."""
    qrels: dict[tuple[str, str], int] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        fields = line.split("\t")
        if len(fields) != 4 or fields[1] != "0":
            raise ValueError(f"invalid qrel at line {line_number}")
        qid, _, chunk_id, raw_grade = fields
        grade = int(raw_grade)
        if grade not in (1, 2):
            raise ValueError(f"invalid positive qrel grade at line {line_number}")
        key = (qid, chunk_id)
        if key in qrels:
            raise ValueError(f"duplicate original qrel: {qid}/{chunk_id}")
        qrels[key] = grade
    return qrels


def build_pooled_qrels(
    *,
    original_qrels_path: Path,
    adjudication_path: Path,
    golden_path: Path,
    answerability_resolution_path: Path | None = None,
    output_qrels_path: Path,
    provenance_path: Path,
    report_path: Path,
) -> dict[str, Any]:
    """Amplía los qrels originales con adjudicaciones y audita los conflictos de respondibilidad."""
    original = _load_qrels(original_qrels_path)
    adjudications = _load_jsonl(adjudication_path)
    golden = _load_jsonl(golden_path)
    answerability = {record["qid"]: record["answerability"] for record in golden}
    if len(answerability) != len(golden):
        raise ValueError("duplicate qid in golden set")
    golden_canonical = {
        (record["qid"], evidence["chunk_id"]): bool(evidence["is_canonical"])
        for record in golden
        for evidence in record.get("evidence", [])
    }
    resolutions = _load_answerability_resolutions(answerability_resolution_path)
    for qid, resolution in resolutions.items():
        if qid not in answerability:
            raise ValueError(f"unknown qid in answerability resolution: {qid}")
        if answerability[qid] != "unanswerable":
            raise ValueError(f"answerability resolution requires unanswerable qid: {qid}")
        resolution["evidence_chunk_ids"] = set(resolution["evidence_chunk_ids"])

    def evidence_role(key: tuple[str, str], grade: int) -> str:
        """Clasifica la evidencia como contexto, respuesta, contradicción o conflicto pendiente."""
        qid, chunk_id = key
        if grade == 1:
            return "context"
        if answerability[qid] == "answerable":
            return "answer_support"
        resolution = resolutions.get(qid)
        if resolution and chunk_id in resolution["evidence_chunk_ids"]:
            return "contradiction"
        return "unresolved_answerability_conflict"

    def resolution_id(key: tuple[str, str]) -> str | None:
        """Obtiene la resolución que autoriza un fragmento como evidencia de contradicción."""
        qid, chunk_id = key
        resolution = resolutions.get(qid)
        if resolution and chunk_id in resolution["evidence_chunk_ids"]:
            return resolution["resolution_id"]
        return None

    final = dict(original)
    provenance: dict[tuple[str, str], dict[str, Any]] = {
        key: {
            "qid": key[0],
            "chunk_id": key[1],
            "grade": grade,
            "canonical": golden_canonical.get(key),
            "source": "original_qrel",
            "pool_id": None,
            "human_reviewer_id": None,
            "adjudication_mode": None,
            "evidence_role": evidence_role(key, grade),
            "answerability_resolution_id": resolution_id(key),
        }
        for key, grade in original.items()
    }
    audited_grade_0 = 0
    added_keys: set[tuple[str, str]] = set()
    conflicts: list[dict[str, Any]] = []
    resolved_conflicts: list[dict[str, Any]] = []
    for key, grade in original.items():
        qid, chunk_id = key
        if grade == 2 and answerability[qid] == "unanswerable":
            if provenance[key]["evidence_role"] == "contradiction":
                resolved_conflicts.append(
                    {
                        "qid": qid,
                        "chunk_id": chunk_id,
                        "grade": grade,
                        "evidence_role": "contradiction",
                        "resolution_id": provenance[key]["answerability_resolution_id"],
                    }
                )
            else:
                conflicts.append({"qid": qid, "chunk_id": chunk_id, "grade": grade})
    seen_pool_ids: set[str] = set()

    for row in adjudications:
        pool_id = row["pool_id"]
        if pool_id in seen_pool_ids:
            raise ValueError(f"duplicate pool_id: {pool_id}")
        seen_pool_ids.add(pool_id)
        qid = row["qid"]
        if qid not in answerability:
            raise ValueError(f"unknown qid in adjudication: {qid}")
        grade = row.get("human_grade")
        if grade not in (0, 1, 2):
            raise ValueError(f"pending adjudication: {pool_id}")
        canonical = bool(row.get("human_canonical"))
        if canonical and grade != 2:
            raise ValueError(f"canonical evidence must have grade 2: {pool_id}")
        if grade == 0:
            audited_grade_0 += 1
            continue

        key = (qid, row["chunk_id"])
        previous_grade = final.get(key)
        # La ampliación conserva el mayor grado entre el qrel histórico y la adjudicación.
        final[key] = max(previous_grade or 0, grade)
        if previous_grade is None:
            added_keys.add(key)
            source = "pool_adjudication"
        else:
            source = "original_qrel_and_pool_adjudication"
        provenance[key] = {
            "qid": qid,
            "chunk_id": row["chunk_id"],
            "grade": final[key],
            "canonical": canonical or bool(golden_canonical.get(key)),
            "source": source,
            "pool_id": pool_id,
            "human_reviewer_id": row.get("human_reviewer_id"),
            "adjudication_mode": row.get("adjudication_mode", "direct_user_review"),
            "evidence_role": evidence_role(key, final[key]),
            "answerability_resolution_id": resolution_id(key),
        }
        if (
            grade == 2
            and answerability[qid] == "unanswerable"
            and previous_grade != 2
        ):
            if provenance[key]["evidence_role"] == "contradiction":
                resolved_conflicts.append(
                    {
                        "qid": qid,
                        "chunk_id": row["chunk_id"],
                        "grade": grade,
                        "evidence_role": "contradiction",
                        "resolution_id": provenance[key]["answerability_resolution_id"],
                    }
                )
            else:
                conflicts.append({"qid": qid, "chunk_id": row["chunk_id"], "grade": grade})

    ordered = sorted(final.items())
    qrels_text = "".join(
        f"{qid}\t0\t{chunk_id}\t{grade}\n"
        for (qid, chunk_id), grade in ordered
    )
    provenance_text = "".join(
        json.dumps(provenance[key], ensure_ascii=False, sort_keys=True) + "\n"
        for key, _ in ordered
    )
    _atomic_write(output_qrels_path, qrels_text)
    _atomic_write(provenance_path, provenance_text)

    grade_counts = Counter(final.values())
    qid_counts: Counter[str] = Counter(qid for qid, _ in final)
    report: dict[str, Any] = {
        "protocol_id": "pooled_qrels_from_three_judge_risk_adjudication_v1",
        "original_qrel_count": len(original),
        "added_qrel_count": len(added_keys),
        "audited_grade_0_count": audited_grade_0,
        "final_qrel_count": len(final),
        "final_grade_counts": {str(grade): grade_counts.get(grade, 0) for grade in (1, 2)},
        "qids_with_positive_qrels": len(qid_counts),
        "qrel_count_by_qid": dict(sorted(qid_counts.items())),
        "answerability_conflicts": sorted(conflicts, key=lambda item: (item["qid"], item["chunk_id"])),
        "resolved_answerability_conflicts": sorted(
            resolved_conflicts, key=lambda item: (item["qid"], item["chunk_id"])
        ),
        "binary_relevance_grade": 2,
        "ndcg_relevance_grades": [0, 1, 2],
        "input_paths": {
            "original_qrels": str(original_qrels_path),
            "adjudication": str(adjudication_path),
            "golden_set": str(golden_path),
            "answerability_resolutions": (
                str(answerability_resolution_path)
                if answerability_resolution_path is not None
                else None
            ),
        },
        "input_sha256": {
            "original_qrels": _sha256(original_qrels_path),
            "adjudication": _sha256(adjudication_path),
            "golden_set": _sha256(golden_path),
            "answerability_resolutions": (
                _sha256(answerability_resolution_path)
                if answerability_resolution_path is not None
                else None
            ),
        },
        "output_qrels_path": str(output_qrels_path),
        "provenance_path": str(provenance_path),
        "output_sha256": _sha256(output_qrels_path),
        "provenance_sha256": _sha256(provenance_path),
    }
    _atomic_write(report_path, json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return report


def build_parser(root: Path) -> argparse.ArgumentParser:
    """Define las fuentes y salidas de la ampliación de qrels por adjudicación."""
    parser = argparse.ArgumentParser(description="Build pooled qrels from final risk-directed adjudication")
    parser.add_argument("--original-qrels", type=Path, default=root / "data/golden/qrels_golden_set_v1_22q.tsv")
    parser.add_argument("--adjudication", type=Path, default=root / "data/golden/pool_human_priority_three_judge_v1_22q.jsonl")
    parser.add_argument("--golden", type=Path, default=root / "data/golden/golden_set_pilot_v1.jsonl")
    parser.add_argument(
        "--answerability-resolutions",
        type=Path,
        default=root / "data/golden/answerability_resolutions_v1_22q.json",
    )
    parser.add_argument("--output", type=Path, default=root / "data/golden/qrels_golden_set_pooled_v1_22q.tsv")
    parser.add_argument("--provenance", type=Path, default=root / "data/golden/qrels_golden_set_pooled_v1_22q_provenance.jsonl")
    parser.add_argument("--report", type=Path, default=root / "data/golden/qrels_golden_set_pooled_v1_22q_report.json")
    return parser


def main() -> int:
    """Construye los qrels ampliados y muestra su informe de procedencia."""
    root = Path(__file__).resolve().parents[1]
    args = build_parser(root).parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="build_pooled_qrels")
    report = build_pooled_qrels(
        original_qrels_path=args.original_qrels,
        adjudication_path=args.adjudication,
        golden_path=args.golden,
        answerability_resolution_path=args.answerability_resolutions,
        output_qrels_path=args.output,
        provenance_path=args.provenance,
        report_path=args.report,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
