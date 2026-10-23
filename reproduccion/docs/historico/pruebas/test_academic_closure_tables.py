"""Regression: the current manuscript must verify applicable metrics."""
import hashlib
import importlib.util
import json

import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def closure():
    spec = importlib.util.spec_from_file_location(
        "closure_academic", ROOT / "scripts/validate_tfm_closure.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_build_report_audits_v3_sources_without_manuscript_tables():
    report, _ = closure().build_report(ROOT, check_tables=False)
    v3 = report["academic_campaigns"]["v3"]
    assert v3["accepted"] == v3["evaluated"] == v3["judge_a"] == v3["judge_b"] == 604
    assert v3["planned"] == 624 and v3["failed"] == 20
    assert v3["human_cells"] == 158 and v3["human_criteria"] == 233
    assert v3["acta_records"] == 159 and v3["convention_records"] == 1
    assert v3["consensus_cells"] == 446
    assert v3["criterion_denominators"] == {
        "faithfulness": 604, "factual_correctness": 600,
        "behavior_ok": 604, "citations_ok": 604,
    }
    assert v3["scales"] == {
        "faithfulness": [0, 2], "factual_correctness": [0, 2],
        "behavior_ok": [0, 2], "citations_ok": [0, 1],
    }
    assert report["academic_input_sha256_before"] == report["academic_input_sha256_after"]
    assert report["academic_inputs_unchanged"]
    assert report["academic_tables_status"] == "not_checked"


def test_explicitness_v2_has_independent_coverage_and_denominators():
    report, _ = closure().build_report(ROOT, check_tables=False)
    v2 = report["academic_campaigns"]["explicitness_v2"]
    assert v2["planned"] == 56 and v2["accepted"] == 55 and v2["failed"] == 1
    assert v2["complete_pairs"] == 27 and v2["unpaired_accepted"] == 1
    assert v2["reviewed_human"] == 16 and v2["primary_judge_retained"] == 39
    assert v2["faithfulness_denominator"] == 48 and v2["faithfulness_unavailable"] == 7
    assert v2["retrieval_base_questions"] == 7


def test_fresh_corrections_are_audited_not_historical_summaries():
    report, _ = closure().build_report(ROOT, check_tables=False)
    corrections = report["academic_campaigns"]["corrections"]
    assert corrections["retrieval_per_query"] == 416
    assert corrections["retrieval_per_base"] == 208
    assert corrections["retrieval_aggregates"] == 16
    assert corrections["paired_tests"] == corrections["eligible_paired_tests"] == 32
    assert corrections["capacity_cells"] == 604 and corrections["capacity_failures"] == 20
    assert corrections["retrieval_cohort_denominators"] == {"all_pairs": 26, "grade2_eligible": 20}
    assert corrections["capacity_primary_cells"] == 509
    assert corrections["paths"]["capacity"].endswith("capacity/release_run1")
    assert corrections["artifact_hashes_verified"]


def test_table_interface_checks_caption_scoped_rows_and_denominators():
    text = """| Modelo | Valor |
|---|---|
| Igual | 9,999 (10) |

: histórica {#tbl-old}

| Modelo | Valor |
|---|---|
| Igual | **0,179** (154) |

: corregida {#tbl-new}
"""
    expected = {"tbl-new": [["Igual", "0,179 (154)"]]}
    checks = closure().validate_document_tables(text, expected, expected_numeric_cells={"tbl-new": 2})
    assert checks == [{"table": "tbl-new", "numeric_cells": 2, "expected_numeric_cells": 2}]
    with pytest.raises(AssertionError):
        closure().validate_document_tables(text.replace("(154)", "(153)"), expected, expected_numeric_cells={"tbl-new": 2})
    with pytest.raises(AssertionError):
        closure().validate_document_tables(text, {}, expected_numeric_cells={})
    with pytest.raises(AssertionError):
        closure().validate_document_tables(text, expected, expected_numeric_cells={"tbl-new": 3})


PRINCIPAL_CORRECTED = {
    "tbl-expl-v3-recuperacion": 32, "tbl-expl-v3-pareado": 48,
    "tbl-capacidad-niveles": 12, "tbl-capacidad-separacion": 36,
    "tbl-capacidad-explicitud": 36, "tbl-capacidad-interaccion": 24,
}
EXPLORATORY = {"tbl-expl-generacion": 64, "tbl-expl-generacion-pareada": 32}
FINAL = {"tbl-final-recuperadores": 96, "tbl-final-operacion": 60}


def test_corrected_contract_preserves_six_principal_anchors():
    expected, counts = closure().academic_table_contract(ROOT)
    assert counts == PRINCIPAL_CORRECTED
    assert set(expected) == set(counts)
    assert sum(counts.values()) == 188


def test_exploratory_contract_belongs_only_to_supplement():
    expected, counts = closure().academic_table_contract(ROOT, scope="supplement")
    assert counts == EXPLORATORY
    assert set(expected) == set(counts)
    assert sum(counts.values()) == 96


def test_current_documents_check_each_scope_independently():
    report, _ = closure().build_report(ROOT)
    assert report["academic_tables_status"] == "verified"
    documents = report["document_tables"]
    principal = documents["tfm.qmd"]
    supplement = documents["antecedentes_experimentales.qmd"]
    assert principal["expected_numeric_cells"] == principal["verified_numeric_cells"] == 344
    assert principal["expected_tables"] == principal["verified_tables"] == 8
    assert {r["table"]: r["numeric_cells"] for r in principal["tables"]} == PRINCIPAL_CORRECTED | FINAL
    assert supplement["expected_numeric_cells"] == supplement["verified_numeric_cells"] == 314
    assert supplement["expected_tables"] == supplement["verified_tables"] == 15
    assert supplement["scopes"]["historical"]["verified_numeric_cells"] == 218
    assert supplement["scopes"]["historical"]["verified_tables"] == 13
    assert supplement["scopes"]["exploratory"]["verified_numeric_cells"] == 96
    assert report["verified_numeric_table_cells"] == 218
    assert report["academic_verified_numeric_table_cells"] == 188
    assert report["raw_inputs_unchanged"]


def table_document(expected):
    """Temporary documents from real artifact values, not mocked analyses."""
    blocks = []
    for name, rows in expected.items():
        header = "| " + " | ".join(["Etiqueta"] + ["Valor"] * (len(rows[0]) - 1)) + " |"
        separator = "|" + "|".join(["---"] * len(rows[0])) + "|"
        blocks.append("\n".join([header, separator] + ["| " + " | ".join(r) + " |" for r in rows]) + f"\n\n: Artefactos reales {{#{name}}}\n")
    return "\n".join(blocks)


def linked_root(tmp_path):
    for child in ROOT.iterdir():
        if child.name not in ("tfm.qmd", "antecedentes_experimentales.qmd"):
            (tmp_path / child.name).symlink_to(child, target_is_directory=child.is_dir())
    return tmp_path


def test_principal_scope_does_not_require_pilot_tables(tmp_path):
    module = closure()
    expected, counts = module.academic_table_contract(ROOT)
    (tmp_path / "tfm.qmd").write_text(table_document(expected))
    checks = module.validate_document_scope(tmp_path, "tfm.qmd", expected, counts)
    assert len(checks) == 6 and sum(r["numeric_cells"] for r in checks) == 188


@pytest.mark.parametrize("missing_table", list(EXPLORATORY))
def test_supplement_missing_required_exploratory_table_fails(tmp_path, missing_table):
    module = closure()
    expected, counts = module.academic_table_contract(ROOT, scope="supplement")
    (tmp_path / "antecedentes_experimentales.qmd").write_text(table_document({k: v for k, v in expected.items() if k != missing_table}))
    with pytest.raises(AssertionError, match=missing_table):
        module.validate_document_scope(tmp_path, "antecedentes_experimentales.qmd", expected, counts)


def test_supplement_is_required_even_if_principal_contains_history(tmp_path):
    root = linked_root(tmp_path)
    (root / "tfm.qmd").write_text((ROOT / "tfm.qmd").read_text())
    with pytest.raises(AssertionError, match="antecedentes_experimentales.qmd.*required document"):
        closure().build_report(root)


def test_document_scope_rejects_empty_contract(tmp_path):
    (tmp_path / "antecedentes_experimentales.qmd").write_text("No tables")
    with pytest.raises(AssertionError, match="non-empty exact table contract"):
        closure().validate_document_scope(tmp_path, "antecedentes_experimentales.qmd", {}, {})


def test_exploratory_adulterated_number_fails(tmp_path):
    module = closure()
    expected, counts = module.academic_table_contract(ROOT, scope="supplement")
    text = table_document(expected)
    number = expected["tbl-expl-generacion"][0][1].split(" → ")[0]
    (tmp_path / "antecedentes_experimentales.qmd").write_text(text.replace(number, "9,999", 1))
    with pytest.raises(AssertionError, match="tbl-expl-generacion"):
        module.validate_document_scope(tmp_path, "antecedentes_experimentales.qmd", expected, counts)


def test_frozen_sources_survive_report_without_table_checks():
    protected = [ROOT / "data", ROOT / "outputs/local_runs/generation_scaling_v3",
                 ROOT / "outputs/local_runs/rag_explicitness_eval_gemma3_v2/adjudication",
                 ROOT / "outputs/local_runs/academic_corrections_20260930"]
    paths = [p for directory in protected for p in directory.rglob("*") if p.is_file()]
    before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    closure().build_report(ROOT, check_tables=False)
    assert before == {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def historical_document_source():
    source = ROOT / "antecedentes_experimentales.qmd"
    return (source if source.is_file() else ROOT / "tfm.qmd").read_text()


def test_real_supplement_validates_13_historical_tables_independently():
    module = closure()
    _, products = module.build_report(ROOT, check_tables=False)
    checks = module.validate_historical_tables(ROOT, products)
    assert {r["table"]: r["numeric_cells"] for r in checks} == module.HISTORICAL_COUNTS
    assert len(checks) == 13 and sum(r["numeric_cells"] for r in checks) == 218
    assert all(r["document"] == "antecedentes_experimentales.qmd" for r in checks)


def test_historical_contract_matches_frozen_closure_reference():
    reference = ROOT / "outputs/local_runs/academic_corrections_20260930/final_validation/closure_release/tfm_closure_validation_v1_22q.json"
    recorded = json.loads(reference.read_text())
    assert closure().HISTORICAL_COUNTS == {r["table"]: r["numeric_cells"] for r in recorded["qmd_tables"]}
    assert len(closure().HISTORICAL_COUNTS) == 13
    assert sum(closure().HISTORICAL_COUNTS.values()) == recorded["verified_numeric_table_cells"] == 218


@pytest.mark.parametrize("missing_table", [
    "tbl-calidad-rag", "tbl-rag-aplicable", "tbl-eficiencia-rag",
    "tbl-apendice-rag-pareado", "tbl-apendice-rag-conducta",
    "tbl-bm25-original", "tbl-bm25-dense-original", "tbl-bm25-dense-pooled",
    "tbl-resultados-rrf", "tbl-retrieval-piloto-top5", "tbl-retrieval-piloto-top10",
    "tbl-latencia-retrieval", "tbl-alineacion-jueces",
])
def test_supplement_missing_required_historical_table_fails(tmp_path, missing_table):
    root = linked_root(tmp_path)
    expected, _ = closure().academic_table_contract(ROOT)
    (root / "tfm.qmd").write_text(table_document(expected))
    text = historical_document_source().replace("{#" + missing_table + "}", "{#removed-table}")
    (root / "antecedentes_experimentales.qmd").write_text(text)
    with pytest.raises(AssertionError, match=missing_table):
        closure().build_report(root)


@pytest.mark.parametrize("replacement", ["9,9999", "BM26"])
def test_historical_number_or_method_tampering_fails(tmp_path, replacement):
    module = closure()
    root = linked_root(tmp_path)
    expected, _ = module.academic_table_contract(ROOT)
    (root / "tfm.qmd").write_text(table_document(expected))
    text = historical_document_source()
    if replacement == "BM26":
        text = text.replace("| BM25 →", "| BM26 →")
    else:
        value = module._document_table(text, "tbl-calidad-rag")[0][1]
        text = text.replace(value, replacement)
    (root / "antecedentes_experimentales.qmd").write_text(text)
    with pytest.raises(AssertionError):
        module.build_report(root)


def test_unchecked_documents_have_no_fabricated_verified_totals():
    report, _ = closure().build_report(ROOT, check_tables=False)
    assert report["verified_numeric_table_cells"] is None
    for document, expected in (("tfm.qmd", (8, 344)), ("antecedentes_experimentales.qmd", (15, 314))):
        result = report["document_tables"][document]
        assert (result["expected_tables"], result["expected_numeric_cells"]) == expected
        assert result["status"] == "not_checked"
        assert result["verified_tables"] is result["verified_numeric_cells"] is None
        assert result["tables"] == []
        for scope in result["scopes"].values():
            assert scope["verified_tables"] is scope["verified_numeric_cells"] is None


def test_final_contract_matches_real_proposed_tables():
    module = closure()
    expected, counts = module.final_table_contract(ROOT)
    assert counts == FINAL
    assert set(expected) == set(FINAL)
    labels = [(model, method) for model in ("Gemma", "Qwen4", "Qwen9")
              for method in ("bm25", "dense", "rrf", "rerank")]
    for rows in expected.values():
        assert len(rows) == 12
        assert [tuple(row[:2]) for row in rows] == labels
    assert expected["tbl-final-recuperadores"][0] == [
        "Gemma", "bm25", "1,806 (34)", "1,500 (33)", "1,568 (41)", "0,955 (41)",
    ]
    assert expected["tbl-final-operacion"][0] == [
        "Gemma", "bm25", "2,810", "2405,9", "126,3", "48", "4",
    ]
    text = (ROOT / module.FINAL_ANALYSIS / "results_proposed.md").read_text()
    checks = module.validate_document_tables(text, expected, expected_numeric_cells=counts)
    assert {row["table"]: row["numeric_cells"] for row in checks} == FINAL
    assert sum(row["numeric_cells"] for row in checks) == 156


def final_artifact_copy(tmp_path):
    """Copy only the two real CSVs; mutations must never touch the campaign."""
    import shutil
    module = closure()
    directory = tmp_path / module.FINAL_ANALYSIS
    directory.mkdir(parents=True)
    for name in ("per_retriever.csv", "operational.csv"):
        shutil.copyfile(ROOT / module.FINAL_ANALYSIS / name, directory / name)
    return directory


@pytest.mark.parametrize("filename", ["per_retriever.csv", "operational.csv"])
def test_final_contract_rejects_duplicate_keys(tmp_path, filename):
    directory = final_artifact_copy(tmp_path)
    path = directory / filename
    lines = path.read_text().splitlines()
    path.write_text("\n".join(lines + [lines[1]]) + "\n")
    with pytest.raises(AssertionError, match="unique rows"):
        closure().final_table_contract(tmp_path)


def rewrite_final_csv(path, transform):
    import csv
    with path.open() as stream:
        reader = csv.DictReader(stream)
        fields, rows = reader.fieldnames, list(reader)
    assert fields
    fields, rows = transform(fields, rows)
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


@pytest.mark.parametrize("filename", ["per_retriever.csv", "operational.csv"])
@pytest.mark.parametrize("field,replacement", [
    ("generator_model", "unknown:model"), ("model", "Inventado"),
    ("retrieval_condition", "BM25"), ("retrieval_condition", "bm26"),
])
def test_final_contract_rejects_unknown_identities(tmp_path, filename, field, replacement):
    directory = final_artifact_copy(tmp_path)
    def replace(fields, rows):
        rows[0][field] = replacement
        return fields, rows
    rewrite_final_csv(directory / filename, replace)
    with pytest.raises(AssertionError, match="identity"):
        closure().final_table_contract(tmp_path)


def test_missing_final_artifacts_are_explicitly_pending(tmp_path):
    with pytest.raises(AssertionError, match="final validation pending.*per_retriever.csv.*operational.csv"):
        closure().final_table_contract(tmp_path)


@pytest.mark.parametrize("filename,field", [
    ("per_retriever.csv", "faithfulness_mean"),
    ("per_retriever.csv", "faithfulness_n_base"),
    ("operational.csv", "latency_s_mean"),
])
@pytest.mark.parametrize("replacement", ["nan", "-1", ""])
def test_final_contract_rejects_invalid_numeric_source(tmp_path, filename, field, replacement):
    directory = final_artifact_copy(tmp_path)
    def replace(fields, rows):
        rows[0][field] = replacement
        return fields, rows
    rewrite_final_csv(directory / filename, replace)
    with pytest.raises(AssertionError, match="numeric source"):
        closure().final_table_contract(tmp_path)


def test_numeric_count_excludes_digits_embedded_in_method_names():
    text = "| Métrica | Contraste |\n|---|---|\n| Citas | bm25−rerank: 0,028 [−0,056; 0,111] |\n\n: x {#tbl-test}\n"
    expected = {"tbl-test": [["Citas", "bm25−rerank: 0,028 [−0,056; 0,111]"]]}
    result = closure().validate_document_tables(text, expected, expected_numeric_cells={"tbl-test": 3})
    assert result[0]["numeric_cells"] == 3


def test_method_identifiers_keep_their_digits_in_table_checks():
    text = "| Métrica | Contraste |\n|---|---|\n| Citas | bm26−rerank: 0,028 [−0,056; 0,111] |\n\n: x {#tbl-test}\n"
    expected = {"tbl-test": [["Citas", "bm25−rerank: 0,028 [−0,056; 0,111]"]]}
    with pytest.raises(AssertionError, match="cell labels"):
        closure().validate_document_tables(text, expected, expected_numeric_cells={"tbl-test": 3})
