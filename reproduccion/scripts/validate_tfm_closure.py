"""Offline closure audit. No inference, no adjudication changes, no network.

Run from the repository root with uv run python scripts/validate_tfm_closure.py.
Use --write-analysis to regenerate only derived JSON analyses after comparison.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_rag_results import analyze, analyze_applicable_content, read_jsonl
from analyze_rag_human_adjudication import analyze_judges, JUDGES
from compare_rag_judges import compare_judges
from consolidate_rag_behavior import consolidate_behavior

PREFIX = "rag_four_retrievers_"
GLM = PREFIX + "top5_qwen35_9b_glm53flash_low_rubricv2_max4096_retry3_seed20260902_scores_v1_22q.jsonl"
GEMMA = PREFIX + "top5_qwen35_9b_gemma3_4b_seed20260902_scores_v1_22q.jsonl"
AUDIT = PREFIX + "gemma3_4b_vs_glm53flash_low_rubricv2_max4096_retry3_seed20260902_risk_queue_v1_22q.jsonl"
CONDITIONS = ["bm25", "dense", "rrf", "rrf_rerank"]


V3_CONDITIONS = ("bm25", "dense", "rrf", "rerank")
V3_MODELS = {"gemma4:e4b": "gemma4_e4b", "qwen3.5:4b": "qwen35_4b", "qwen3.5:9b": "qwen35_9b"}
SCALES = {"faithfulness": [0, 2], "factual_correctness": [0, 2], "behavior_ok": [0, 2], "citations_ok": [0, 1]}
ACADEMIC_CORRECTIONS = Path("outputs/local_runs/academic_corrections_20260930")


def _cell_key(row):
    """Identifica una celda por pregunta, modelo generador y condición de recuperación."""
    return row["qid"], row["generator_model"], row["retrieval_condition"]


def _unique(rows, key, expected, label):
    """Indexa las filas y exige el número esperado de claves únicas."""
    index = {key(row): row for row in rows}
    assert len(rows) == len(index) == expected, (label, len(rows), len(index), expected)
    return index


def _academic_sources(root):
    """Read-only campaign audit; planned keys come from the frozen golden set."""
    hashes = {}

    def read(relative, kind="jsonl"):
        """Lee una fuente de la campaña y registra la huella de sus bytes originales."""
        path = root / relative
        raw = path.read_bytes()
        hashes[str(relative)] = hashlib.sha256(raw).hexdigest()
        if kind == "json":
            return json.loads(raw)
        if kind == "csv":
            return list(csv.DictReader(raw.decode().splitlines()))
        return [json.loads(line) for line in raw.decode().splitlines() if line.strip()]

    base = Path("outputs/local_runs/generation_scaling_v3")
    golden = read(Path("data/golden/variants/generation_golden_v3.jsonl"))
    golden_index = _unique(golden, lambda r: r["qid"], 52, "v3 golden")
    assert len({r["base_qid"] for r in golden}) == 26
    planned = {(qid, model, condition) for qid in golden_index for model in V3_MODELS for condition in V3_CONDITIONS}
    assert len(planned) == 624
    generations, failures = [], []
    for model, slug in V3_MODELS.items():
        for condition in V3_CONDITIONS:
            path = base / f"rag_{condition}_top5_{slug}.jsonl"
            rows = read(path)
            assert all(r["generator_model"] == model and r["retrieval_condition"] == condition for r in rows)
            generations.extend(rows)
            fp = path.with_name(path.stem + "_failures.jsonl")
            if (root / fp).exists():
                rows = read(fp)
                assert all(r["generator_model"] == model and r["retrieval_condition"] == condition and r["status"] == "failed" for r in rows)
                failures.extend(rows)
    generated = _unique(generations, _cell_key, 604, "v3 generation")
    failed = _unique(failures, _cell_key, 20, "v3 failures")
    assert not generated.keys() & failed.keys()
    # Aceptaciones y fallos deben cubrir todo el diseño sin solaparse.
    assert generated.keys() | failed.keys() == planned, "v3 planned coverage"
    final = _unique(read(base / "eval_final_v3.jsonl"), _cell_key, 604, "v3 final")
    a = _unique(read(base / "eval_verdicts_v3.jsonl"), _cell_key, 604, "v3 judge A")
    b = _unique(read(base / "eval_verdicts_v3_juezB.jsonl"), _cell_key, 604, "v3 judge B")
    assert final.keys() == a.keys() == b.keys() == generated.keys(), "v3 full key coverage"
    acta = read(base / "arbitraje_discrepancias_v3/validacion_humana_v3.jsonl")
    conventions = [r for r in acta if r.get("tipo") == "convencion_familia_pregunta"]
    decisions = [r for r in acta if "decisions" in r]
    assert len(acta) == 159 and len(conventions) == 1
    assert "q-v3-007" in conventions[0]["ambito"] and conventions[0]["fijada_por"] == "andres"
    assert "behavior_ok=0" in conventions[0]["regla"]
    human = _unique(decisions, _cell_key, 158, "v3 acta")
    assert sum(len(r["decisions"]) for r in decisions) == 233
    discrepancies = {k: {cr for cr in SCALES if a[k][cr] != b[k][cr]} for k in final}
    assert {k for k, cr in discrepancies.items() if cr} == human.keys(), "v3 disputed coverage"
    provenance = Counter()
    denominators = Counter()
    for key, row in final.items():
        gold = golden_index[row["qid"]]
        generation = generated[key]
        assert row["base_qid"] == gold["base_qid"]
        assert row["qid"] in (row["base_qid"] + "__explicit", row["base_qid"] + "__implicit")
        assert generation["expected_behavior"] == gold["expected_behavior"]
        assert row.get("expected_behavior") in (None, generation["expected_behavior"])
        assert row["label_ok"] == a[key]["label_ok"] == b[key]["label_ok"]
        assert row["label_ok"] in (0, 1)
        assert row["human_validated_cell"] == (key in human)
        if key in human:
            review = human[key]
            assert review["status"] == "adjudicated" and review["reviewer"] == "andres"
            assert set(review["decisions"]) == set(review["disputed_criteria"]) == discrepancies[key]
        for criterion, (_, maximum) in SCALES.items():
            value = row[criterion]
            assert value == "na" or (type(value) in (int, float) and math.isfinite(value) and 0 <= value <= maximum), (key, criterion, value)
            denominators[criterion] += value != "na"
            if criterion in discrepancies[key]:
                assert value == human[key]["decisions"][criterion]["final"], (key, criterion, "human decision")
                source = "validacion_humana"
            else:
                assert value == a[key][criterion] == b[key][criterion], (key, criterion, "consensus")
                source = "consenso_jueces"
            assert row["final_provenance"][criterion] == source, (key, criterion, "provenance")
            provenance[source] += 1
        if row["base_qid"] == "q-v3-007" and "behavior_ok" in discrepancies[key]:
            assert row["behavior_ok"] == 0, "q-v3-007 human convention"
    expected_denominators = {"faithfulness": 604, "factual_correctness": 600, "behavior_ok": 604, "citations_ok": 604}
    assert dict(denominators) == expected_denominators
    summary = read(base / "eval_final_v3_summary.json", "json")
    assert summary["n_cells"] == 604 and summary["human_validated_cells"] == 158
    for group, rows in ((model, [r for r in final.values() if r["generator_model"] == model]) for model in V3_MODELS):
        stats = summary["by_generator"][group]
        assert stats["n"] == len(rows)
        for criterion in SCALES:
            values = [r[criterion] for r in rows if r[criterion] != "na"]
            assert stats[criterion + "_n"] == len(values)
            assert stats[criterion] == round(statistics.fmean(values), 3)
    report = {"v3": {"accepted": 604, "evaluated": 604, "judge_a": 604, "judge_b": 604,
                     "planned": 624, "failed": 20, "human_cells": 158, "human_criteria": 233,
                     "acta_records": 159, "convention_records": 1, "consensus_cells": 446,
                     "scales": SCALES, "criterion_denominators": dict(denominators),
                     "criterion_provenance": dict(provenance), "full_cell_key_checked": True}}
    gen_base = Path("outputs/local_runs/rag_explicitness_v2")
    eval_base = Path("outputs/local_runs/rag_explicitness_eval_gemma3_v2")
    golden_v2 = _unique(read(gen_base / "golden_variants_14q.jsonl"), lambda r: r["qid"], 14, "v2 golden")
    v2_key = lambda r: (r["qid"], r["retrieval_condition"])
    v2_generated = []
    v2_failures = []
    for condition in V3_CONDITIONS:
        path = gen_base / f"rag_{condition}_top5_qwen35_9b_v2_14q.jsonl"
        rows = read(path)
        assert all(r["retrieval_condition"] == condition and r["generator_model"] == "qwen3.5:9b" for r in rows)
        v2_generated.extend(rows)
        fp = path.with_name(path.stem + "_failures.jsonl")
        if (root / fp).exists():
            v2_failures.extend(read(fp))
    v2_generated = _unique(v2_generated, v2_key, 55, "v2 generation")
    v2_failures = _unique(v2_failures, v2_key, 1, "v2 failures")
    assert set(v2_failures) == {("q-v1-006__explicit", "rerank")}
    assert v2_failures[("q-v1-006__explicit", "rerank")]["status"] == "failed"
    v2_planned = {(qid, c) for qid in golden_v2 for c in V3_CONDITIONS}
    assert len(v2_planned) == 56 and v2_generated.keys() | v2_failures.keys() == v2_planned
    assert not v2_generated.keys() & v2_failures.keys()
    scores = _unique(read(eval_base / "scores.jsonl"), v2_key, 55, "v2 scores")
    adjudications = _unique(read(eval_base / "adjudication/rag_adjudications_v2.jsonl"), v2_key, 55, "v2 consolidation")
    assert scores.keys() == adjudications.keys() == v2_generated.keys()
    for key, row in scores.items():
        assert row["generator_model"] == "qwen3.5:9b"
        for field in ("question", "expected_behavior", "reference", "response", "retrieved_chunk_ids", "retrieved_contexts", "citations"):
            assert row[field] == v2_generated[key][field], (key, field)
        rec = adjudications[key]
        for automatic, original in (("behavior_label", "reported_behavior"), ("behavior_score", "behavior_judge_score"),
                                    ("faithfulness", "faithfulness"), ("factual_correctness", "factual_correctness"),
                                    ("citation_validity", "citation_validity"), ("citation_presence", "citation_presence")):
            assert rec["automatic_" + automatic] == row[original], (key, automatic)
        if rec["final_behavior_source"] == "primary_judge":
            assert rec["final_behavior_score"] == row["behavior_judge_score"]
    assert Counter(r["final_behavior_source"] for r in adjudications.values()) == {"human_adjudication": 16, "primary_judge": 39}
    faith_n = sum(type(r["faithfulness"]) in (int, float) for r in adjudications.values())
    assert faith_n == 48
    pairs = Counter((qid.rsplit("__", 1)[0], c) for qid, c in v2_generated)
    assert sum(n == 2 for n in pairs.values()) == 27 and sum(n == 1 for n in pairs.values()) == 1
    v2_summary = read(eval_base / "adjudication/rag_adjudication_summary.json", "json")
    assert v2_summary["counts"]["total_rows"] == 55 and v2_summary["counts"]["faithfulness_scored"] == 48
    assert v2_summary["counts"]["faithfulness_unavailable"] == 7
    retrieval_v2 = read(Path("outputs/local_runs/explicitness_paired_metrics/paired_metrics_full.json"), "json")
    assert len({r["base_qid"] for r in golden_v2.values()}) == 7
    assert len(retrieval_v2["means"]) == 24
    report["explicitness_v2"] = {"planned": 56, "accepted": 55, "failed": 1, "complete_pairs": 27,
                                "unpaired_accepted": 1, "reviewed_human": 16, "primary_judge_retained": 39,
                                "faithfulness_denominator": faith_n, "faithfulness_unavailable": 55 - faith_n,
                                "retrieval_base_questions": 7}
    metric_base = ACADEMIC_CORRECTIONS / "retrieval/evaluation"
    paired_base = ACADEMIC_CORRECTIONS / "retrieval/paired"
    capacity_base = ACADEMIC_CORRECTIONS / "capacity/release_run1"

    def verify_outputs(directory, manifest):
        """Comprueba las huellas de los artefactos declarados en un manifiesto no vacío."""
        assert manifest, "empty artifact manifest"
        for name, digest in manifest.items():
            assert Path(name).name == name, "manifest output must be a filename"
            path = directory / name
            raw = (root / path).read_bytes()
            hashes[str(path)] = hashlib.sha256(raw).hexdigest()
            assert hashes[str(path)] == digest, (path, "artifact hash")

    retrieval_report = read(metric_base / "retrieval_correction_report.json", "json")
    paired_report = read(paired_base / "paired_correction_report.json", "json")
    verify_outputs(metric_base, retrieval_report["outputs"])
    verify_outputs(paired_base, paired_report["outputs"])
    queries = read(metric_base / "per_query.csv", "csv")
    bases = read(metric_base / "per_base.csv", "csv")
    aggregates = read(metric_base / "aggregate_metrics.csv", "csv")
    qindex = _unique(queries, lambda r: (r["method"], r["qid"], int(r["k"])), 416, "corrected per-query")
    _unique(bases, lambda r: (r["method"], r["base_qid"], int(r["k"])), 208, "corrected per-base")
    _unique(aggregates, lambda r: (r["cohort"], r["method"], int(r["k"])), 16, "corrected aggregate")
    assert set(qindex) == {(m, q, k) for m in V3_CONDITIONS for q in golden_index for k in (5, 10)}
    from evaluate_retrieval_v3 import metrics_for, METRICS
    from paired_explicitness_v3 import compute_contrasts
    qrel_path = Path("outputs/local_runs/explicitness_v3/qrels_final_v3.jsonl")
    qrel_rows = read(qrel_path)
    qrels = _unique(qrel_rows, lambda r: (r["base_qid"], r["chunk_id"]), 578, "v3 qrels")
    assert hashes[str(qrel_path)] == retrieval_report["inputs"]["qrels"]["sha256"]
    for method in V3_CONDITIONS:
        path = Path(f"outputs/local_runs/explicitness_v3/runs/explicitness_v3_{method}.jsonl")
        run = read(path)
        assert len(run) == 520 and hashes[str(path)] == retrieval_report["inputs"][method]["sha256"]
        for qid, gold in golden_index.items():
            ranking = sorted((r for r in run if r["qid"] == qid), key=lambda r: r["rank"])
            assert len(ranking) == len({r["chunk_id"] for r in ranking}) == 10
            assert [r["rank"] for r in ranking] == list(range(1, 11))
            grades = [r["grade"] for r in qrel_rows if r["base_qid"] == gold["base_qid"]]
            n_rel = grades.count(2)
            retrieved = [qrels.get((gold["base_qid"], r["chunk_id"]), {}).get("grade", 0) for r in ranking]
            for k in (5, 10):
                row = qindex[method, qid, k]
                assert row["base_qid"] == gold["base_qid"] and int(row["n_relevant"]) == n_rel
                values = metrics_for(retrieved, k, n_rel, qrel_grades=grades)
                for metric in METRICS:
                    assert math.isclose(float(row[metric]), values[metric], abs_tol=1e-12), (method, qid, k, metric)
    for row in bases:
        values = [qindex[row["method"], row["base_qid"] + "__" + side, int(row["k"])] for side in ("explicit", "implicit")]
        assert int(row["n_formulaciones"]) == 2
        for metric in METRICS:
            assert math.isclose(float(row[metric]), statistics.fmean(float(v[metric]) for v in values), abs_tol=1e-12)
    cohort_sizes = {"all_pairs": 26, "grade2_eligible": 20}
    for cohort, expected_n in cohort_sizes.items():
        selected_bases = {r["base_qid"] for r in bases if cohort == "all_pairs" or int(r["n_relevant"]) > 0}
        assert len(selected_bases) == expected_n
        assert retrieval_report["cohorts"][cohort]["base_qids"] == sorted(selected_bases)
        for row in aggregates:
            if row["cohort"] != cohort:
                continue
            assert int(row["n_base"]) == expected_n
            subset = [r for r in bases if r["base_qid"] in selected_bases and r["method"] == row["method"] and r["k"] == row["k"]]
            assert len(subset) == expected_n
            for metric in METRICS:
                assert math.isclose(float(row[metric]), statistics.fmean(float(r[metric]) for r in subset), abs_tol=1e-12)
        numeric_queries = [{**r, "k": int(r["k"]), "n_relevant": int(r["n_relevant"]), **{m: float(r[m]) for m in METRICS}} for r in queries]
        recomputed, _ = compute_contrasts(numeric_queries, sorted(selected_bases))
        path = paired_base / ("paired_explicitness_v3.csv" if cohort == "all_pairs" else "paired_grade2_eligible.csv")
        pairs = read(path, "csv")
        pindex = _unique(pairs, lambda r: (r["method"], int(r["k"]), r["metric"]), 32, "paired tests")
        for row in recomputed:
            actual = pindex[row["method"], row["k"], row["metric"]]
            assert int(actual["n_pairs"]) == expected_n
            for field in ("mean_diff", "p_sign", "p_holm", "pos", "neg", "ties", "n_effective", "family_size"):
                assert math.isclose(float(actual[field]), row[field], abs_tol=1e-12), (path, field)
            assert int(actual["pos"]) + int(actual["neg"]) + int(actual["ties"]) == expected_n
    capacity_manifest = read(capacity_base / "hash_manifest.json", "json")
    verify_outputs(capacity_base, capacity_manifest["outputs"])
    for path, metadata in capacity_manifest["sources"].items():
        # The script hash is reproducibility metadata; all campaign inputs must match.
        raw = (root / path).read_bytes()
        hashes[path] = hashlib.sha256(raw).hexdigest()
        if path.startswith("scripts/"):
            continue  # recorded implementation hash, not a frozen campaign input
        assert hashes[path] == metadata["sha256"], (path, "capacity source hash")
    capacity = read(capacity_base / "tables.json", "json")
    assert capacity["scales"] == SCALES and capacity["n_cells"] == 604
    assert capacity["coverage_summary"]["n_planned"] == 624
    assert capacity["coverage_summary"]["n_accepted"] == 604 and capacity["coverage_summary"]["n_failed"] == 20
    assert capacity["primary_content"]["n_cells"] == 509 and capacity["primary_content"]["n_base"] == 22
    joined = read(capacity_base / "joined_cells.csv", "csv")
    jindex = _unique(joined, _cell_key, 604, "capacity joined cells")
    assert jindex.keys() == generated.keys()
    for key, row in jindex.items():
        assert row["expected_behavior"] == generated[key]["expected_behavior"]
        for criterion in SCALES:
            expected = final[key][criterion]
            assert row[criterion] == str(expected), (key, criterion, "capacity score")
    cf = read(capacity_base / "failures.csv", "csv")
    assert _unique(cf, _cell_key, 20, "capacity failures").keys() == failed.keys()
    from analysis_capacity_v3 import coverage_report
    enriched = [{**r, "expected_behavior": generated[k]["expected_behavior"]} for k, r in final.items()]
    enriched_failures = [{**r, "base_qid": r["qid"].rsplit("__", 1)[0], "expected_behavior": golden_index[r["qid"]]["expected_behavior"]} for r in failed.values()]
    assert capacity["coverage"] == coverage_report(enriched, enriched_failures)
    assert capacity["coverage_summary"]["by_expected_behavior"] == dict(Counter(r["expected_behavior"] for r in enriched))
    assert capacity["coverage_summary"]["unavailable_by_criterion"] == {cr: 604 - denominators[cr] for cr in SCALES}
    report["corrections"] = {"retrieval_per_query": 416, "retrieval_per_base": 208, "retrieval_aggregates": 16,
                             "paired_tests": 32, "eligible_paired_tests": 32, "capacity_cells": 604,
                             "capacity_failures": 20, "capacity_primary_cells": 509,
                             "retrieval_cohort_denominators": cohort_sizes, "artifact_hashes_verified": True,
                             "paths": {"retrieval": str(metric_base), "paired": str(paired_base), "capacity": str(capacity_base)}}
    after = {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in hashes}
    assert hashes == after, "academic sources changed during validation"
    return report, hashes, after


def _document_table(text, table_id):
    """Find one Pandoc pipe table by its caption; blank lines are not rows."""
    anchors = list(re.finditer(r"(?m)^\s*:\s*[^\n]*\{#" + re.escape(table_id) + r"\}", text))
    assert len(anchors) == 1, (table_id, "missing or duplicate caption", len(anchors))
    lines = text[:anchors[0].start()].rstrip().splitlines()
    selected = []
    for line in reversed(lines):
        if not line.strip().startswith("|"):
            break
        selected.append([c.strip().replace("**", "") for c in line.strip().strip("|").split("|")])
    rows = list(reversed(selected))
    assert len(rows) >= 3 and all(re.fullmatch(r":?-+:?", c.replace(" ", "")) for c in rows[1]), (table_id, "empty/non-table block")
    return rows[2:]


def validate_document_tables(text, expected, *, expected_numeric_cells):
    """Compare an artifact-derived contract, never a denominator inferred from QMD.

    ``expected`` maps table IDs to full rows of display strings (including labels).
    ``expected_numeric_cells`` is an independent fixed count per required table.
    Use this API for a changed layout before wiring its contract into build_report.
    """
    from decimal import Decimal
    assert expected and set(expected) == set(expected_numeric_cells), "non-empty exact table contract required"
    number = re.compile(r"(?<!\w)[-+]?\d+(?:[.,]\d+)?(?!\w)")
    checks = []
    def clean(cell):
        """Normaliza el marcado y los espacios de una celda para compararla."""
        return re.sub(r"\s+", " ", cell.replace("**", "").replace("`", "").replace("*", "").replace("−", "-")).strip()
    def tokens(cell):
        """Extrae los valores decimales de una celda normalizando su separador."""
        return [Decimal(n.replace(",", ".")) for n in number.findall(clean(cell))]
    for table_id, rows in expected.items():
        assert rows and expected_numeric_cells[table_id] > 0, (table_id, "empty contract")
        actual = _document_table(text, table_id)
        assert len(actual) == len(rows), (table_id, "row count", len(actual), len(rows))
        checked = 0
        for observed, values in zip(actual, rows):
            assert len(observed) == len(values), (table_id, "column count", observed, values)
            assert clean(observed[0]) == clean(values[0]), (table_id, "row label", observed[0], values[0])
            for cell, value in zip(observed[1:], values[1:]):
                wanted = tokens(value)
                assert tokens(cell) == wanted, (table_id, cell, value)
                # Preserve method identities/extrema and other nonnumeric labels.
                words = lambda s: re.sub(r"\W+", "", number.sub("", clean(s).lower()))
                assert words(cell) == words(value), (table_id, "cell labels", cell, value)
                checked += len(wanted)
        assert checked == expected_numeric_cells[table_id], (table_id, "numeric count", checked, expected_numeric_cells[table_id])
        checks.append({"table": table_id, "numeric_cells": checked, "expected_numeric_cells": expected_numeric_cells[table_id]})
    return checks


def academic_table_contract(root: Path, *, scope="principal"):
    """Derive corrected or exploratory display values, never from either QMD."""
    assert scope in ("principal", "supplement"), (scope, "unknown academic scope")
    base = root / ACADEMIC_CORRECTIONS
    def csv_rows(path):
        """Carga las filas CSV de una tabla de correcciones académicas."""
        with (base / path).open() as stream:
            return list(csv.DictReader(stream))
    def fmt(value, signed=False):
        """Formatea un valor con tres decimales y coma decimal, con signo opcional."""
        return format(float(value), "+.3f" if signed else ".3f").replace(".", ",")
    def interval(row, field, signed=False):
        """Presenta una estimación y los límites de su intervalo al 95 por ciento."""
        return f"{fmt(row[field], signed)} [{fmt(row['ic95_lo'])}; {fmt(row['ic95_hi'])}]"
    methods = [("bm25", "BM25"), ("dense", "Dense"), ("rrf", "RRF"), ("rerank", "RRF + reranking")]
    models = ["gemma4:e4b", "qwen3.5:4b", "qwen3.5:9b"]
    criteria = [("faithfulness", "Fundamentación"), ("factual_correctness", "Corrección"),
                ("behavior_ok", "Conducta"), ("citations_ok", "Citas")]
    expected = {}
    aggregates = {(r["method"], int(r["k"])): r for r in csv_rows("retrieval/evaluation/aggregate_metrics.csv") if r["cohort"] == "all_pairs"}
    expected["tbl-expl-v3-recuperacion"] = [
        [label] + [fmt(aggregates[method, k][cr]) for k in (5, 10) for cr in ("recall", "precision", "mrr", "ndcg")]
        for method, label in methods]
    pairs = {(r["method"], r["metric"]): r for r in csv_rows("retrieval/paired/paired_explicitness_v3.csv") if r["k"] == "10"}
    rows = []
    for method, label in methods:
        row = [label]
        for cr in ("recall", "ndcg"):
            p = pairs[method, cr]
            assert int(p["n_pairs"]) == 26 and int(p["family_size"]) == 16
            row.extend([fmt(p["mean_diff"], True), f"{p['pos']}/{p['neg']}/{p['ties']}", f"{fmt(p['p_sign'])} / {fmt(p['p_holm'])}"])
        rows.append(row)
    expected["tbl-expl-v3-pareado"] = rows
    capacity_dir = "capacity/release_run1/"
    def primary(name):
        """Selecciona las filas del análisis de contenido principal en una tabla de capacidad."""
        return [r for r in csv_rows(capacity_dir + name) if r["scope"] == "primary_content"]
    levels = {r["generator_model"]: r for r in primary("h6_niveles_common.csv")}
    for row in levels.values():
        for cr, _ in criteria:
            assert int(row[cr + "_n_cells"]) == (154 if cr == "factual_correctness" else 157)
            assert int(row[cr + "_n_base"]) == 22
    expected["tbl-capacidad-niveles"] = [[model] + [fmt(levels[model][cr]) for cr, _ in criteria] for model in models]
    extremes = {(r["generator_model"], r["criterion"]): r for r in primary("h5_separacion_common.csv")}
    rows = []
    for cr, label in criteria:
        row = [label]
        for model in models:
            e = extremes[model, cr]
            assert e["mejor"] != e["peor"] and int(e["n_base"]) == 18
            assert int(e["n_cells"]) == (33 if cr == "factual_correctness" else 34)
            row.append(f"{e['mejor']}−{e['peor']}: " + interval(e, "ventaja"))
        rows.append(row)
    expected["tbl-capacidad-separacion"] = rows
    effects = {(r["generator_model"], r["criterion"]): r for r in primary("h6_explicitud_common.csv")}
    for (model, cr), row in effects.items():
        assert int(row["n_base"]) == 22 and int(row["n_cells"]) == (71 if cr == "factual_correctness" else 74)
    expected["tbl-capacidad-explicitud"] = [
        [model] + [interval(effects[model, cr], "diff_implicit_minus_explicit", True) for cr, _ in criteria] for model in models]
    interactions = {(r["from_model"], r["to_model"], r["criterion"]): r for r in primary("h6_interaccion.csv")}
    comparisons = [(models[0], models[1], "Gemma → Qwen 4B", (74, 71)),
                   (models[0], models[2], "Gemma → Qwen 9B", (74, 72)),
                   (models[1], models[2], "Qwen 4B → Qwen 9B", (88, 86))]
    rows = []
    for origin, destination, label, sizes in comparisons:
        pair = [interactions[origin, destination, cr] for cr in ("faithfulness", "factual_correctness")]
        assert tuple(int(r["n_cells"]) for r in pair) == sizes and all(int(r["n_base"]) == 22 for r in pair)
        rows.append([label] + [interval(r, "diff_of_diffs", True) for r in pair] + [f"{sizes[0]}/{sizes[1]}"])
    expected["tbl-capacidad-interaccion"] = rows
    source = root / "outputs/local_runs/rag_explicitness_eval_gemma3_v2/adjudication/rag_adjudications_v2.jsonl"
    records = [json.loads(line) for line in source.read_text().splitlines() if line.strip()]
    marginal, paired = [], []
    for method, label in methods:
        subsets = [{r["base_qid"]: r for r in records if r["retrieval_condition"] == method and r["explicitness"] == side}
                   for side in ("explicit", "implicit")]
        means, diffs = [label], [label]
        for field in ("faithfulness", "factual_correctness", "final_behavior_score", "citation_validity"):
            available = [[r[field] for r in subset.values() if r[field] is not None] for subset in subsets]
            means.append(f"{fmt(statistics.fmean(available[0]))} → {fmt(statistics.fmean(available[1]))} ({len(available[0])}/{len(available[1])})")
            common = [qid for qid in subsets[0].keys() & subsets[1].keys() if all(subset[qid][field] is not None for subset in subsets)]
            diff = statistics.fmean(subsets[1][qid][field] - subsets[0][qid][field] for qid in common)
            diffs.append(f"{fmt(diff, True)} ({len(common)})")
        marginal.append(means)
        paired.append(diffs)
    expected["tbl-expl-generacion"] = marginal
    expected["tbl-expl-generacion-pareada"] = paired
    counts = {"tbl-expl-v3-recuperacion": 32, "tbl-expl-v3-pareado": 48,
              "tbl-capacidad-niveles": 12, "tbl-capacidad-separacion": 36,
              "tbl-capacidad-explicitud": 36, "tbl-capacidad-interaccion": 24,
              "tbl-expl-generacion": 64, "tbl-expl-generacion-pareada": 32}
    selected = {name for name in counts if (name in ("tbl-expl-generacion", "tbl-expl-generacion-pareada")) == (scope == "supplement")}
    return {name: rows for name, rows in expected.items() if name in selected}, {name: n for name, n in counts.items() if name in selected}


HISTORICAL_COUNTS = {
    "tbl-calidad-rag": 24, "tbl-rag-aplicable": 8, "tbl-eficiencia-rag": 20,
    "tbl-apendice-rag-pareado": 18, "tbl-apendice-rag-conducta": 18,
    "tbl-bm25-original": 8, "tbl-bm25-dense-original": 16,
    "tbl-bm25-dense-pooled": 16, "tbl-resultados-rrf": 24,
    "tbl-retrieval-piloto-top5": 16, "tbl-retrieval-piloto-top10": 16,
    "tbl-latencia-retrieval": 16, "tbl-alineacion-jueces": 18,
}
FINAL_COUNTS = {"tbl-final-recuperadores": 96, "tbl-final-operacion": 60}
FINAL_ANALYSIS = Path("outputs/local_runs/final_experiment_20260930/analysis")
PRINCIPAL_DOCUMENT = "tfm.qmd"
SUPPLEMENT_DOCUMENT = "antecedentes_experimentales.qmd"


def validate_document_scope(root, document, expected, counts):
    """A missing document or empty source contract never constitutes a pass."""
    path = root / document
    assert path.is_file(), (document, "required document missing")
    checks = validate_document_tables(path.read_text(), expected, expected_numeric_cells=counts)
    return [{**row, "document": document} for row in checks]


def final_table_contract(root) -> tuple[dict, dict]:
    """Derive final display rows from CSVs, independently of the manuscript."""
    paths = [root / FINAL_ANALYSIS / name for name in ("per_retriever.csv", "operational.csv")]
    missing = [str(path.relative_to(root)) for path in paths if not path.is_file()]
    assert not missing, "final validation pending: missing artifacts " + ", ".join(missing)
    models = {"gemma4:e4b": "Gemma", "qwen3.5:4b": "Qwen4", "qwen3.5:9b": "Qwen9"}
    keys = [(model, method) for model in models for method in V3_CONDITIONS]
    indexes = []
    for path in paths:
        with path.open() as stream:
            rows = list(csv.DictReader(stream))
        index = {(r["generator_model"], r["retrieval_condition"]): r for r in rows}
        assert len(rows) == len(index) == 12, (path.name, "expected 12 unique rows", len(rows), len(index))
        assert set(index) == set(keys), (path.name, "model/method identity coverage")
        assert all(r["model"] == models[r["generator_model"]] for r in rows), (path.name, "model label identity")
        for row in rows:
            fields = ([criterion + suffix for criterion in SCALES
                       for suffix in ("_mean", "_n_cells", "_n_base")]
                      if path.name == "per_retriever.csv" else
                      ["latency_s_mean", "prompt_tokens_mean", "completion_tokens_mean",
                       "accepted", "failed", "latency_s_n_numeric",
                       "prompt_tokens_n_numeric", "completion_tokens_n_numeric"])
            for field in fields:
                try:
                    value = float(row[field])
                except (KeyError, TypeError, ValueError):
                    raise AssertionError((path.name, field, "invalid numeric source")) from None
                assert math.isfinite(value) and value >= 0, (path.name, field, "invalid numeric source")
                if not field.endswith("_mean"):
                    assert value.is_integer(), (path.name, field, "noninteger numeric source")
                if path.name == "per_retriever.csv" and field.endswith("_mean"):
                    criterion = field[:-5]
                    assert value <= SCALES[criterion][1], (path.name, field, "out-of-scale numeric source")
        indexes.append(index)
    def fmt(value, digits=3):
        """Formatea un valor numérico con coma decimal y la precisión solicitada."""
        return f"{float(value):.{digits}f}".replace(".", ",")
    quality, operational = [], []
    for model, method in keys:
        row = indexes[0][model, method]
        quality.append([models[model], method] + [
            f"{fmt(row[criterion + '_mean'])} ({row[criterion + '_n_cells']})" for criterion in SCALES])
        row = indexes[1][model, method]
        operational.append([models[model], method, fmt(row["latency_s_mean"]),
                            fmt(row["prompt_tokens_mean"], 1), fmt(row["completion_tokens_mean"], 1),
                            row["accepted"], row["failed"]])
    return {"tbl-final-recuperadores": quality, "tbl-final-operacion": operational}, dict(FINAL_COUNTS)


def _scope_summary(checks, counts, *, status="verified"):
    """Resume las tablas verificadas frente al contrato de recuentos del ámbito."""
    assert counts, "non-empty exact table contract required"
    expected_tables, expected_cells = len(counts), sum(counts.values())
    if status == "verified":
        assert {r["table"]: r["numeric_cells"] for r in checks} == counts
    return {"status": status, "expected_tables": expected_tables,
            "expected_numeric_cells": expected_cells,
            "verified_tables": len(checks) if status == "verified" else None,
            "verified_numeric_cells": sum(r["numeric_cells"] for r in checks) if status == "verified" else None,
            "tables": checks}


def validate_historical_tables(root, products):
    """Validate the frozen pilot only in its mandatory historical supplement."""
    assert (root / SUPPLEMENT_DOCUMENT).is_file(), (SUPPLEMENT_DOCUMENT, "required document missing")
    automatic = products[PREFIX + "glm53flash_analysis_v1_22q.json"]
    consolidated = products[PREFIX + "behavior_human_glm53flash_consolidated_v1_22q.json"]
    applicable = products[PREFIX + "glm53flash_applicable_analysis_v1_22q.json"]
    alignment = products[PREFIX + "judge_human_alignment_v1_22q.json"]
    config = json.loads((root / "config/rag_four_retrievers_experiment_v1.json").read_text())
    with (root / "outputs/latency/retrieval_latency_controlled_v1_22q_summary.csv").open() as stream:
        latency = list(csv.DictReader(stream))
    table_checks = []
    text = (root / SUPPLEMENT_DOCUMENT).read_text()
    def table(table_id):
        """Extrae del suplemento histórico las filas de la tabla indicada."""
        return _document_table(text, table_id)
    def check(table_id, expected, digits=4):
        """Contrasta etiquetas, recuentos y valores de una tabla histórica con su referencia."""
        actual = table(table_id)
        assert len(actual) == len(expected), (table_id, len(actual), len(expected))
        assert [r[0] for r in actual] == historical_labels[table_id], (table_id, "row labels")
        checked = sum(len(r) for r in expected)
        assert checked == HISTORICAL_COUNTS[table_id], (table_id, "numeric contract count", checked)
        for row, values in zip(actual, expected):
            observed = [float(x.replace("−", "-").replace(",", ".")) for x in row[1:]]
            assert observed == [float(f"{v:.{digits}f}") for v in values], (table_id, row, values)
        table_checks.append({"table": table_id, "numeric_cells": checked,
                             "expected_numeric_cells": HISTORICAL_COUNTS[table_id], "document": SUPPLEMENT_DOCUMENT})
    metrics_labels = ["Precision", "Recall", "MRR", "nDCG"]
    pair_labels = ["BM25 → dense", "BM25 → RRF", "BM25 → RRF + reranking",
                   "Dense → RRF", "Dense → RRF + reranking", "RRF → RRF + reranking"]
    historical_labels = {
        "tbl-calidad-rag": ["Factual Correctness automática, 15 casos", "Coincidencia de conducta declarada",
                            "Conducta automática GLM, escala 0--2", "Conducta consolidada, escala 0--2",
                            "Validez formal de citas", "Presencia o ausencia correcta de citas"],
        "tbl-rag-aplicable": ["Faithfulness", "Factual Correctness"],
        "tbl-eficiencia-rag": ["Latencia media de generación (ms)", "Latencia p95 de generación (ms)",
                              "Tokens medios de entrada", "Tokens medios de salida", "Respuestas con regeneración correctiva"],
        "tbl-apendice-rag-pareado": pair_labels, "tbl-apendice-rag-conducta": pair_labels,
        **{name: metrics_labels for name in ("tbl-bm25-original", "tbl-bm25-dense-original", "tbl-bm25-dense-pooled",
                                           "tbl-resultados-rrf", "tbl-retrieval-piloto-top5", "tbl-retrieval-piloto-top10")},
        "tbl-latencia-retrieval": ["BM25", "Dense", "RRF", "RRF + reranker"],
    }
    overall = automatic["overall"]
    quality_fields = ["factual_correctness_mean", "reported_behavior_match_mean", "behavior_judge_score_mean", "final_mean", "citation_validity_mean", "citation_presence_mean"]
    check("tbl-calidad-rag", [[(consolidated["by_retrieval_condition"][c][field] if field == "final_mean" else overall[c][field]) for c in CONDITIONS] for field in quality_fields])
    check("tbl-rag-aplicable", [[applicable["overall"][c][field] for c in CONDITIONS] for field in ["faithfulness_mean", "factual_correctness_mean"]])
    check("tbl-eficiencia-rag", [[overall[c][field] for c in CONDITIONS] for field in ["generation_latency_ms_mean", "generation_latency_ms_p95", "prompt_tokens_mean", "completion_tokens_mean", "responses_requiring_retry"]], digits=2)
    pairs = list(consolidated["all_pairwise"])
    check("tbl-apendice-rag-pareado", [[automatic["all_pairwise"][p][m]["mean_delta_contender_minus_baseline"] for m in ["faithfulness", "factual_correctness"]] + [consolidated["all_pairwise"][p]["mean_delta_contender_minus_baseline"]] for p in pairs])
    check("tbl-apendice-rag-conducta", [[consolidated["all_pairwise"][p][m] for m in ["contender_wins", "ties", "baseline_wins"]] for p in pairs], digits=0)
    metrics = {}
    run_ids = ["bm25_v1_22q", "dense_e5_base_v2_22q"] + [Path(item["retrieval_run"]).stem for item in config["conditions"]]
    for run_id in run_ids:
        metrics[run_id] = {(r["metric"], int(r["k"])): float(r["value"]) for r in csv.DictReader((root / f"outputs/metrics/{run_id}_metrics.csv").open())}
    pooled = run_ids[2:]
    tables = {"tbl-bm25-original": [(run_ids[0], 5), (run_ids[0], 10)], "tbl-bm25-dense-original": [(r, k) for k in [5, 10] for r in run_ids[:2]], "tbl-bm25-dense-pooled": [(r, k) for k in [5, 10] for r in pooled[:2]], "tbl-resultados-rrf": [(r, k) for k in [5, 10] for r in pooled[:3]], "tbl-retrieval-piloto-top5": [(r, 5) for r in pooled], "tbl-retrieval-piloto-top10": [(r, 10) for r in pooled]}
    for name, columns in tables.items():
        check(name, [[metrics[r][m, k] for r, k in columns] for m in ["precision", "recall", "mrr", "ndcg"]])
    check("tbl-latencia-retrieval", [[float(r[f]) for f in ["mean_ms", "median_ms", "p95_ms", "std_ms"]] for r in latency], digits=2)
    # Alignment table includes fractions and percentages; verify exact rendered cells.
    def fmt(value, places=4):
        """Formatea los valores de alineación con coma decimal y precisión fija."""
        return f"{value:.{places}f}".replace(".", ",")
    expected_columns = []
    for key in JUDGES:
        judge = alignment["judges"][key]
        behavior = judge["behavior"]
        frac = lambda b: f"{b['exact_agreement_n']}/{b['human_applicable_n']} ({fmt(b['exact_agreement_rate'] * 100, 1)} %)"
        faith = judge["faithfulness"]
        expected_columns.append([str(judge["evaluation_error_case_count"]), frac(behavior), fmt(behavior["mae_on_applicable"]), *[frac(behavior["by_expected_behavior"][b]) for b in ["answer", "abstain", "grounded_correction"]], f"{faith['judge_available_on_applicable_n']}/{faith['human_applicable_n']}", fmt(faith["mae_on_applicable"]), fmt(judge["factual_correctness"]["mae_on_applicable"])])
    actual = table("tbl-alineacion-jueces")
    alignment_labels = ["Errores explícitos de evaluación", "Acuerdo exacto en conducta", "MAE de conducta",
                        "Acuerdo en respuestas ordinarias", "Acuerdo en abstenciones", "Acuerdo en correcciones fundamentadas",
                        "Faithfulness aplicable disponible", "MAE de Faithfulness aplicable", "MAE de Factual Correctness aplicable"]
    assert [r[0] for r in actual] == alignment_labels, ("tbl-alineacion-jueces", "row labels")
    assert [r[1:] for r in actual] == [list(x) for x in zip(*expected_columns)]
    # Legacy closure counts 18 displayed data cells, including compound fractions.
    # Every numerator, denominator and percentage is nevertheless checked above.
    assert len(expected_columns) * len(alignment_labels) == HISTORICAL_COUNTS["tbl-alineacion-jueces"]
    table_checks.append({"table": "tbl-alineacion-jueces", "numeric_cells": 18,
                         "expected_numeric_cells": 18, "document": SUPPLEMENT_DOCUMENT})
    _scope_summary(table_checks, HISTORICAL_COUNTS)
    return table_checks


def build_report(root: Path, *, check_tables: bool = True) -> tuple[dict, dict]:
    """Reconstruye los análisis congelados y audita su cobertura, procedencia y tablas."""
    directory = root / "outputs/rag_eval"
    config = json.loads((root / "config/rag_four_retrievers_experiment_v1.json").read_text())
    raw_paths = [directory / name for name in [GLM, GEMMA, AUDIT]]
    raw_paths += [root / item["rag_output"] for item in config["conditions"]]
    raw_paths += [root / item["retrieval_run"] for item in config["conditions"]]
    raw_paths += [root / "data/processed/chunks_v1.jsonl", root / "data/golden/golden_set_pilot_v1.jsonl", root / "data/golden/qrels_golden_set_pooled_v1_22q.tsv"]
    hashes = {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest() for path in raw_paths}
    glm, gemma, audit = [read_jsonl(directory / name) for name in [GLM, GEMMA, AUDIT]]
    products = {
        PREFIX + "glm53flash_analysis_v1_22q.json": analyze(glm),
        PREFIX + "judge_human_alignment_v1_22q.json": analyze_judges(audit, JUDGES),
        PREFIX + "behavior_human_glm53flash_consolidated_v1_22q.json": consolidate_behavior(glm, audit, primary_judge="glm53flash_low"),
        PREFIX + "gemma3_4b_vs_glm53flash_comparison_v1_22q.json": compare_judges(gemma, glm, baseline_name="gemma3_4b", alternative_name="glm53flash_low"),
        PREFIX + "glm53flash_applicable_analysis_v1_22q.json": analyze_applicable_content(glm),
    }
    def equivalent(left, right):
        """Compara estructuras anidadas con tolerancia numérica para valores flotantes."""
        if isinstance(left, float) and isinstance(right, (int, float)):
            return math.isclose(left, right, rel_tol=1e-12, abs_tol=1e-12)
        if isinstance(left, dict) and isinstance(right, dict):
            return left.keys() == right.keys() and all(equivalent(left[k], right[k]) for k in left)
        if isinstance(left, list) and isinstance(right, list):
            return len(left) == len(right) and all(equivalent(a, b) for a, b in zip(left, right))
        return left == right
    equality = {name: equivalent(json.loads((directory / name).read_text()), value) for name, value in products.items() if (directory / name).exists()}
    assert all(equality.values()), equality
    automatic = products[PREFIX + "glm53flash_analysis_v1_22q.json"]
    consolidated = products[PREFIX + "behavior_human_glm53flash_consolidated_v1_22q.json"]
    applicable = products[PREFIX + "glm53flash_applicable_analysis_v1_22q.json"]
    alignment = products[PREFIX + "judge_human_alignment_v1_22q.json"]
    keys = lambda rows: {(r["retrieval_condition"], r["qid"]) for r in rows}
    assert len(glm) == len(gemma) == len(keys(glm)) == 88
    assert keys(glm) == keys(gemma)
    assert len(audit) == len(keys(audit)) == 61
    assert len({r["qid"] for r in audit}) == 21
    assert all(r["human_adjudication"]["status"] == "adjudicated" for r in audit)
    assert consolidated["source_counts"] == {"human_adjudication": 61, "glm53flash_low": 27}
    assert Counter(r["expected_behavior"] for r in audit) == {"abstain": 28, "answer": 25, "grounded_correction": 8}
    audit_index = {(r["retrieval_condition"], r["qid"]): r for r in audit}
    # Validate complete frozen review units and both judges, not only qid keys.
    content_fields = ["question", "expected_behavior", "reference", "response", "retrieved_chunk_ids", "retrieved_contexts"]
    for rows in [glm, gemma]:
        for row in rows:
            if (row["retrieval_condition"], row["qid"]) in audit_index:
                reviewed = audit_index[(row["retrieval_condition"], row["qid"])]
                for field in content_fields:
                    assert row[field] == reviewed[field], (row["qid"], field)
    for row in audit:
        if row["expected_behavior"] == "abstain":
            assert row["human_adjudication"]["faithfulness_assessment"] == "not_applicable"
            assert row["human_adjudication"]["factual_correctness_assessment"] == "not_applicable"
    assert applicable["row_count"] == 60
    runs = {}
    generation_count = 0
    for item in config["conditions"]:
        condition = item["id"]
        generated = read_jsonl(root / item["rag_output"])
        assert len(generated) == 22
        generation_count += len(generated)
        indexed = {(r["retrieval_condition"], r["qid"]): r for r in glm}
        for row in generated:
            other = indexed[(condition, row["qid"])]
            for field in content_fields + ["citations", "generation_latency_ms", "prompt_tokens", "completion_tokens"]:
                assert row[field] == other[field], (condition, row["qid"], field)
            assert set(row["citations"]).issubset(row["retrieved_chunk_ids"])
        runs[condition] = read_jsonl(root / item["retrieval_run"])
        assert len(runs[condition]) == 220
        assert Counter(r["qid"] for r in runs[condition]) == {r["qid"]: 10 for r in generated}
        for row in generated:
            top5 = [r["chunk_id"] for r in sorted(runs[condition], key=lambda r: r["rank"]) if r["qid"] == row["qid"]][:5]
            assert row["retrieved_chunk_ids"] == top5
    changed_top5 = 0
    for qid in {r["qid"] for r in runs["rrf"]}:
        left = [r for r in runs["rrf"] if r["qid"] == qid]
        right = [r for r in runs["rrf_rerank"] if r["qid"] == qid]
        assert {r["chunk_id"] for r in left} == {r["chunk_id"] for r in right}
        changed_top5 += {r["chunk_id"] for r in left if r["rank"] <= 5} != {r["chunk_id"] for r in right if r["rank"] <= 5}
    golden = read_jsonl(root / "data/golden/golden_set_pilot_v1.jsonl")
    assert len(golden) == 22
    assert Counter(r["answerability"] for r in golden) == {"answerable": 13, "unanswerable": 9}
    chunks = read_jsonl(root / "data/processed/chunks_v1.jsonl")
    assert len(chunks) == 288
    qrels = list(csv.reader((root / "data/golden/qrels_golden_set_pooled_v1_22q.tsv").open(), delimiter="\t"))
    assert len(qrels) == 119 and Counter(r[-1] for r in qrels) == {"1": 47, "2": 72}
    dense_bad = next(r for r in glm if r["retrieval_condition"] == "dense" and r["qid"] == "q-v1-016")
    assert dense_bad["reported_behavior"] == "abstain" and dense_bad["citations"] == []
    assert dense_bad["citation_validity"] == dense_bad["citation_presence"] == 0
    latency_dir = root / "outputs/latency"
    latency_raw = list(csv.DictReader((latency_dir / "retrieval_latency_controlled_v1_22q_raw.csv").open()))
    latency = list(csv.DictReader((latency_dir / "retrieval_latency_controlled_v1_22q_summary.csv").open()))
    assert len(latency_raw) == 660
    for row in latency:
        values = sorted(float(r[row["condition"] + "_ms"]) for r in latency_raw)
        position = 0.95 * (len(values) - 1)
        p95 = values[math.floor(position)] + (position % 1) * (values[math.ceil(position)] - values[math.floor(position)])
        for field, value in {"mean_ms": statistics.fmean(values), "median_ms": statistics.median(values), "p95_ms": p95, "std_ms": statistics.stdev(values)}.items():
            assert math.isclose(float(row[field]), value, rel_tol=1e-10), (field, row["condition"])
    table_checks = []
    if check_tables:
        for document in (PRINCIPAL_DOCUMENT, SUPPLEMENT_DOCUMENT):
            assert (root / document).is_file(), (document, "required document missing")
        table_checks = validate_historical_tables(root, products)
    unchanged = all(hashlib.sha256((root / name).read_bytes()).hexdigest() == value for name, value in hashes.items())
    assert unchanged
    report = {
        "scope": "offline deterministic analysis of frozen responses; no new inference",
        "counts": {"chunks": len(chunks), "questions": len(golden), "qrels": len(qrels), "responses": generation_count, "adjudicated_pairs": len(audit), "audit_qids": len({r['qid'] for r in audit}), "pending_adjudications": 0, "condition_pairs": len(consolidated["all_pairwise"]), "applicable_content_cases": applicable["row_count"], "retrieval_samples_per_condition": len(latency_raw)},
        "source_counts": consolidated["source_counts"],
        "reranker_top10_set_equality_qids": 22,
        "reranker_changed_top5_set_qids": changed_top5,
        "frozen_citation_out_of_context_count": sum(not set(r["citations"]).issubset(r["retrieved_chunk_ids"]) for r in glm),
        "regenerated_equal_to_existing": all(equality.values()),
        "existing_product_checks": equality,
        "raw_inputs_unchanged": unchanged,
        "input_sha256": hashes,
        "qmd_tables": table_checks,
        "verified_numeric_table_cells": sum(t["numeric_cells"] for t in table_checks) if check_tables else None,
        "latency_summary_recomputed_from_raw": True,
    }
    campaigns, academic_before, academic_after = _academic_sources(root)
    report.update(academic_campaigns=campaigns, academic_input_sha256_before=academic_before,
                  academic_input_sha256_after=academic_after, academic_inputs_unchanged=True,
                  academic_tables_status="not_checked")
    expected, counts = academic_table_contract(root)
    exploratory, exploratory_counts = academic_table_contract(root, scope="supplement")
    if check_tables:
        academic_checks = validate_document_scope(root, PRINCIPAL_DOCUMENT, expected, counts)
        exploratory_checks = validate_document_scope(root, SUPPLEMENT_DOCUMENT, exploratory, exploratory_counts)
        final_expected, final_counts = final_table_contract(root)
        assert final_counts == FINAL_COUNTS, "exact non-empty final table contract required"
        final_checks = validate_document_scope(root, PRINCIPAL_DOCUMENT, final_expected, final_counts)
        report.update(academic_tables_status="verified", academic_qmd_tables=academic_checks,
                      academic_verified_numeric_table_cells=sum(r["numeric_cells"] for r in academic_checks))
    else:
        academic_checks, exploratory_checks, final_checks = [], [], []
    status = "verified" if check_tables else "not_checked"
    principal_checks = academic_checks + final_checks
    supplement_checks = table_checks + exploratory_checks
    report["document_tables"] = {
        PRINCIPAL_DOCUMENT: {
            **_scope_summary(principal_checks, counts | FINAL_COUNTS, status=status),
            "scopes": {"corrected": _scope_summary(academic_checks, counts, status=status),
                       "final": _scope_summary(final_checks, FINAL_COUNTS, status=status)}},
        SUPPLEMENT_DOCUMENT: {
            **_scope_summary(supplement_checks, HISTORICAL_COUNTS | exploratory_counts, status=status),
            "scopes": {"historical": _scope_summary(table_checks, HISTORICAL_COUNTS, status=status),
                       "exploratory": _scope_summary(exploratory_checks, exploratory_counts, status=status)}}}
    return report, products


def main():
    """Ejecuta la auditoría de cierre y guarda derivados solo en un destino nuevo."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-analysis", action="store_true")
    parser.add_argument("--output", type=Path, help="Fresh directory under outputs/local_runs; otherwise read-only")
    args = parser.parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="validate_tfm_closure")
    if args.write_analysis and args.output is None:
        parser.error("--write-analysis requires --output; frozen products are never replaced")
    root = Path(__file__).resolve().parents[1]
    report, products = build_report(root)
    if args.output is not None:
        args.output.mkdir(parents=True, exist_ok=False)
        if args.write_analysis:
            for name, value in products.items():
                (args.output / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
        (args.output / "tfm_closure_validation_v1_22q.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key != "input_sha256"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
