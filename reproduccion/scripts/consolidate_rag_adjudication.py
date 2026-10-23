#!/usr/bin/env python3
"""Consolida la adjudicación humana de la cola de riesgo RAG sobre los scores automáticos.

Conserva intactos los campos ``automatic_*`` del juez y añade ``final_*`` derivados de la
decisión humana, tal y como exige el protocolo de revisión de respuestas RAG: la
adjudicación humana solo prevalece sobre las claves revisadas; el resto conserva al juez
principal. Regenera resúmenes por condición y comparaciones emparejadas a partir de los
campos finales y verifica la regeneración determinista.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REVIEWER = "andres"
REVIEWER_ROLE = "human"
ADJUDICATION_MODE = "human_confirmation"
PROPOSAL_SOURCE = "assistant_proposal_user_confirmed"

# Decisiones confirmadas por el usuario (2026-09-21), agrupadas como en la hoja de revisión.
RECLASSIFY_LABEL = [
    "dense q-v1-001__explicit",
    "rerank q-v1-001__implicit",
    "bm25 q-v1-012__explicit",
    "dense q-v1-014__explicit",
    "rrf q-v1-014__explicit",
    "dense q-v1-014__implicit",
    "rerank q-v1-014__implicit",
    "rrf q-v1-014__implicit",
    "rerank q-v1-016__implicit",
    "rrf q-v1-016__implicit",
]
CONFIRM_FAILURE = ["dense q-v1-016__implicit"]
ACCEPT_AFTER_RETRY = ["rerank q-v1-002__explicit", "dense q-v1-003__explicit"]
FAITHFULNESS_UNAVAILABLE_FLAGGED = [
    "bm25 q-v1-006__explicit",
    "bm25 q-v1-014__explicit",
    "rerank q-v1-014__explicit",
]


def _key(row: dict) -> str:
    """Forma la clave de revisión con la estrategia y el identificador de pregunta."""
    return f"{row['retrieval_condition']} {row['qid']}"


def _explicitness(qid: str) -> str:
    """Extrae la variante de explicitud del sufijo del identificador."""
    return qid.rsplit("__", 1)[1]


def _base_qid(qid: str) -> str:
    """Recupera el identificador base eliminando el sufijo de explicitud."""
    return qid.rsplit("__", 1)[0]


def decision_for(key: str) -> tuple[str, str, str]:
    """Devuelve (decision_group, decision, nota) para una clave revisada.

    Para claves no revisadas devuelve ``auto`` y conserva al juez principal.
    """
    if key in CONFIRM_FAILURE:
        return (
            "A2",
            "confirm_unsupported_abstention",
            "El contexto era suficiente (sección 3.5 de distribuciones discretas y continuas) "
            "y otras técnicas contestan la misma pregunta; la abstención no está justificada. "
            "Conducta 0 confirmada. El rationale del juez describe un intento previo, no la respuesta final.",
        )
    if key in RECLASSIFY_LABEL:
        return (
            "A1",
            "reclassify_behavior_label",
            "Respuesta directa y correcta sin corrección de presupuesto alguno; el rationale "
            "califica el contenido de correcto y la conducta puntúa 2. La etiqueta "
            "grounded_correction es un artefacto del juez de conducta. Se reclasifica a answer "
            "conservando las puntuaciones.",
        )
    if key in ACCEPT_AFTER_RETRY:
        return (
            "B",
            "accept_after_retry",
            "Primera generación incumplió el formato de citas y hubo reintento correctivo; la "
            "respuesta final cumple el contrato y puntúa 1.0/1.0/2. Evento de contrato, no defecto de calidad.",
        )
    if key in FAITHFULNESS_UNAVAILABLE_FLAGGED:
        extra = (
            " Además requirió reintento de generación."
            if key == "bm25 q-v1-014__explicit"
            else ""
        )
        return (
            "C",
            "record_faithfulness_unavailable",
            "El cálculo de faithfulness de RAGAS falló; el contenido está completo y correcto. "
            "Se registra la métrica como no disponible, nunca como 0." + extra,
        )
    return ("auto", "primary_judge_retained", "Clave no seleccionada en la cola de riesgo; prevalece el juez principal.")


def build_adjudications(scores: list[dict], adjudicated_at: str) -> list[dict]:
    """Aplica las decisiones humanas confirmadas conservando las puntuaciones automáticas originales."""
    out = []
    for row in scores:
        key = _key(row)
        group, decision, note = decision_for(key)
        reviewed = group != "auto"
        faith = row.get("faithfulness")
        faith_status = "scored" if isinstance(faith, (int, float)) else "unavailable"

        auto_label = row.get("reported_behavior")
        auto_score = row.get("behavior_judge_score")

        if group == "A2":
            final_label, final_score = "abstain", 0
        elif group == "A1":
            final_label, final_score = "answer", auto_score
        else:
            final_label, final_score = auto_label, auto_score

        rec = {
            "retrieval_condition": row["retrieval_condition"],
            "qid": row["qid"],
            "base_qid": _base_qid(row["qid"]),
            "explicitness": _explicitness(row["qid"]),
            "expected_behavior": row.get("expected_behavior"),
            # Campos automáticos intactos, sin reescribir.
            "automatic_behavior_label": auto_label,
            "automatic_behavior_score": auto_score,
            "automatic_faithfulness": faith,
            "automatic_factual_correctness": row.get("factual_correctness"),
            "automatic_citation_validity": row.get("citation_validity"),
            "automatic_citation_presence": row.get("citation_presence"),
            # Campos derivados de la adjudicación.
            "final_behavior_label": final_label,
            "final_behavior_score": final_score,
            "final_behavior_source": "human_adjudication" if reviewed else "primary_judge",
            "faithfulness": faith,
            "faithfulness_status": faith_status,
            "factual_correctness": row.get("factual_correctness"),
            "citation_validity": row.get("citation_validity"),
            "citation_presence": row.get("citation_presence"),
            "decision_group": group,
            "decision": decision,
            "notes": note,
            "risk_reasons": row.get("risk_reasons", []),
            "evaluation_errors": row.get("evaluation_errors", []),
            "reviewer": REVIEWER if reviewed else "gemma3:4b (primary judge)",
            "reviewer_role": REVIEWER_ROLE if reviewed else "model",
            "adjudication_mode": ADJUDICATION_MODE if reviewed else "automatic_primary_judge",
            "proposal_source": PROPOSAL_SOURCE if reviewed else None,
            "adjudicated_at": adjudicated_at if reviewed else None,
        }
        out.append(rec)
    return out


def summarize(adjs: list[dict]) -> dict:
    """Resume las adjudicaciones por estrategia y contrasta las variantes de explicitud emparejadas."""
    def mean(vals):
        """Devuelve el número de valores numéricos y su media redondeada."""
        vals = [v for v in vals if isinstance(v, (int, float))]
        return {"n": len(vals), "mean": round(sum(vals) / len(vals), 4) if vals else None}

    cond = defaultdict(lambda: defaultdict(list))
    for a in adjs:
        for m in ("faithfulness", "factual_correctness", "final_behavior_score",
                  "citation_validity", "citation_presence"):
            cond[a["retrieval_condition"]][m].append(a[m])

    conditions = {
        c: {m: mean(v) for m, v in metrics.items()} for c, metrics in sorted(cond.items())
    }

    # Deltas emparejados (implícita - explícita) por condición y métrica.
    per = defaultdict(dict)
    for a in adjs:
        per[(a["retrieval_condition"], a["base_qid"])][a["explicitness"]] = a
    paired = []
    for cond_name in sorted({a["retrieval_condition"] for a in adjs}):
        for m in ("faithfulness", "factual_correctness", "final_behavior_score"):
            deltas = []
            for (c, _b), sides in per.items():
                if c != cond_name or "explicit" not in sides or "implicit" not in sides:
                    continue
                x, y = sides["explicit"][m], sides["implicit"][m]
                if isinstance(x, (int, float)) and isinstance(y, (int, float)):
                    deltas.append(round(y - x, 4))
            paired.append({
                "retrieval_condition": cond_name,
                "metric": m,
                "n_base_pairs": len(deltas),
                "mean_implicit_minus_explicit": round(sum(deltas) / len(deltas), 4) if deltas else None,
            })

    return {
        "counts": {
            "total_rows": len(adjs),
            "reviewed_human": sum(1 for a in adjs if a["adjudication_mode"] == ADJUDICATION_MODE),
            "primary_judge_retained": sum(1 for a in adjs if a["adjudication_mode"] == "automatic_primary_judge"),
            "by_decision_group": dict(Counter(a["decision_group"] for a in adjs)),
            "faithfulness_scored": sum(1 for a in adjs if a["faithfulness_status"] == "scored"),
            "faithfulness_unavailable": sum(1 for a in adjs if a["faithfulness_status"] == "unavailable"),
            "behavior_reclassified": sum(1 for a in adjs if a["decision"] == "reclassify_behavior_label"),
            "behavior_score_overridden": sum(
                1 for a in adjs
                if a["automatic_behavior_score"] != a["final_behavior_score"]
            ),
        },
        "conditions": conditions,
        "paired_explicitness": paired,
    }


def _dump(rows: list[dict]) -> str:
    """Serializa las adjudicaciones en JSONL con claves ordenadas."""
    return "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)


def main() -> None:
    """Guarda las adjudicaciones y su resumen con fecha y hashes de procedencia."""
    ap = argparse.ArgumentParser()
    root = Path(__file__).resolve().parent.parent
    ap.add_argument("--scores", type=Path, required=True)
    ap.add_argument("--adjudications", type=Path, required=True)
    ap.add_argument("--summary", type=Path, required=True)
    ap.add_argument("--adjudicated-at", default=None)
    args = ap.parse_args()

    stamp = args.adjudicated_at or datetime.now(timezone.utc).isoformat()
    scores = [
        json.loads(line)
        for line in args.scores.read_text().splitlines()
        if line.strip()
    ]
    adjs = build_adjudications(scores, stamp)
    summary = summarize(adjs)

    args.adjudications.parent.mkdir(parents=True, exist_ok=True)
    args.adjudications.write_text(_dump(adjs))
    payload = dict(summary)
    payload["inputs"] = {
        "scores_name": args.scores.name,
        "scores_sha256": hashlib.sha256(args.scores.read_bytes()).hexdigest(),
    }
    payload["adjudications_name"] = args.adjudications.name
    payload["adjudications_sha256"] = hashlib.sha256(args.adjudications.read_bytes()).hexdigest()
    payload["adjudicated_at"] = stamp
    payload["status"] = "human_adjudicated_not_population_estimate"
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(summary["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
