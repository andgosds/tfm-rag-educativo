"""Pruebas de la consolidación de adjudicación humana RAG."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from consolidate_rag_adjudication import (  # noqa: E402
    build_adjudications,
    summarize,
)

ROOT = Path(__file__).resolve().parent.parent


def _scores():
    return [
        json.loads(line)
        for line in (ROOT / "outputs/local_runs/rag_explicitness_eval_gemma3_v2/scores.jsonl")
        .read_text().splitlines()
        if line.strip()
    ]


def test_automatic_fields_preserved_and_final_reclassified():
    adjs = {f"{a['retrieval_condition']} {a['qid']}": a for a in build_adjudications(_scores(), "T")}
    a = adjs["dense q-v1-001__explicit"]
    assert a["automatic_behavior_label"] == "grounded_correction"
    assert a["automatic_behavior_score"] == 2
    assert a["final_behavior_label"] == "answer"
    assert a["final_behavior_score"] == 2
    assert a["final_behavior_source"] == "human_adjudication"
    assert a["decision"] == "reclassify_behavior_label"


def test_confirmed_failure_keeps_zero_score():
    adjs = {f"{a['retrieval_condition']} {a['qid']}": a for a in build_adjudications(_scores(), "T")}
    a = adjs["dense q-v1-016__implicit"]
    assert a["decision"] == "confirm_unsupported_abstention"
    assert a["automatic_behavior_score"] == 0
    assert a["final_behavior_score"] == 0
    assert a["final_behavior_label"] == "abstain"


def test_faithfulness_unavailable_on_seven_rows():
    adjs = build_adjudications(_scores(), "T")
    un = [a for a in adjs if a["faithfulness_status"] == "unavailable"]
    assert len(un) == 7
    assert all(a["faithfulness"] is None for a in un)


def test_behavior_score_overridden_exactly_once():
    adjs = build_adjudications(_scores(), "T")
    changed = [a for a in adjs if a["automatic_behavior_score"] != a["final_behavior_score"]]
    # Solo el fallo confirmado cambia de puntuación; ya era 0, luego ninguna cambia.
    assert changed == []


def test_unreviewed_rows_keep_primary_judge():
    adjs = build_adjudications(_scores(), "T")
    auto = [a for a in adjs if a["decision_group"] == "auto"]
    assert auto, "debe haber claves no revisadas"
    for a in auto:
        assert a["final_behavior_source"] == "primary_judge"
        assert a["final_behavior_score"] == a["automatic_behavior_score"]


def test_summary_counts():
    s = summarize(build_adjudications(_scores(), "T"))
    assert s["counts"]["total_rows"] == 55
    assert s["counts"]["behavior_reclassified"] == 10
    assert s["counts"]["faithfulness_unavailable"] == 7
    assert s["counts"]["faithfulness_scored"] == 48


def test_deterministic_regeneration(tmp_path):
    scores = ROOT / "outputs/local_runs/rag_explicitness_eval_gemma3_v2/scores.jsonl"
    script = ROOT / "scripts/consolidate_rag_adjudication.py"
    outs = []
    for i in range(2):
        sub = tmp_path / f"run{i}"
        sub.mkdir()
        adj = sub / "adjudications.jsonl"
        summ = sub / "summary.json"
        subprocess.run(
            [sys.executable, str(script), "--scores", str(scores),
             "--adjudications", str(adj), "--summary", str(summ),
             "--adjudicated-at", "2026-09-21T00:00:00+00:00"],
            check=True, capture_output=True,
        )
        outs.append((adj.read_bytes(), summ.read_bytes()))
    assert outs[0][0] == outs[1][0], "adjudicaciones no deterministas"
    assert outs[0][1] == outs[1][1], "resumen no determinista"
