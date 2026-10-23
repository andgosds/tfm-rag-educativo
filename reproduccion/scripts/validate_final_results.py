"""Validate final results and frozen delivery PDFs without rendering them.

This delivery-only adapter reuses the artifact-derived numerical contracts.
It does not compare manuscript prose to historical versions.
"""
from collections import Counter
from pathlib import Path
import csv
import importlib
import json
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'docs'))
closure = importlib.import_module('validate_tfm_closure')
appendix = importlib.import_module('validar_apendices')
academic_table_contract = closure.academic_table_contract
final_table_contract = closure.final_table_contract
validate_document_tables = closure.validate_document_tables


def validate_tables(target):
    """Contrasta las tablas de la entrega con valores derivados de los artefactos congelados."""
    expected, counts = academic_table_contract(ROOT)
    # Presentation-only adaptations of the external contract to v2_3/v2_4.
    matrix = expected["tbl-expl-v3-recuperacion"]
    metrics = ("Recall", "Precision", "MRR", "nDCG")
    expected["tbl-expl-v3-recuperacion"] = [
        [f"{metric}\\@{k}"] + [row[1 + offset] for row in matrix]
        for offset, (k, metric) in enumerate((k, metric) for k in (5, 10) for metric in metrics)
    ]
    paired = expected["tbl-expl-v3-pareado"]
    expected["tbl-expl-v3-pareado"] = [
        [label, row[0], row[start], row[start + 1], *row[start + 2].split(" / ")]
        for label, start in (("Recall\\@10", 1), ("nDCG\\@10", 4))
        for row in paired
    ]
    extremes = expected["tbl-capacidad-separacion"]
    model_names = ("gemma4:e4b", "qwen3.5:4b", "qwen3.5:9b")
    expected["tbl-capacidad-separacion"] = [
        [model, row[0], *row[column].split(": ", 1)]
        for column, model in enumerate(model_names, 1)
        for row in extremes
    ]
    final_expected, final_counts = final_table_contract(ROOT)
    expected.update(final_expected)
    counts.update(final_counts)

    profile_path = ROOT / "outputs/local_runs/final_experiment_20260930/analysis/joined_cells.csv"
    with profile_path.open() as stream:
        cells = list(csv.DictReader(stream))
    content = [r for r in cells if r["expected_behavior"] in ("answer", "grounded_correction")]
    assert len(cells) == 604 and len(content) == 509
    def numeric(value):
        """Distingue puntuaciones disponibles de los marcadores de ausencia del CSV."""
        return value not in ("", "NA", "na", "None")
    complete = [r for r in content if numeric(r["faithfulness"]) and numeric(r["factual_correctness"])]
    assert len(content) - len(complete) == 4
    profile_rows = []
    for model, label in zip(model_names, ("Gemma E4B", "Qwen 4B", "Qwen 9B")):
        subset = [r for r in complete if r["generator_model"] == model]
        profile = Counter((float(r["faithfulness"]) == 2, float(r["factual_correctness"]) == 2) for r in subset)
        profile_rows.append([label] + [str(profile[key]) for key in ((True, True), (True, False), (False, True), (False, False))] + [str(len(subset))])
    expected["tbl-perfiles-contenido"] = profile_rows
    counts["tbl-perfiles-contenido"] = 15

    def jsonl(path):
        """Carga registros JSONL de una ruta relativa a la reproducción."""
        return [json.loads(line) for line in (ROOT / path).read_text().splitlines() if line.strip()]

    golden = jsonl("data/golden/variants/generation_golden_v3.jsonl")
    assert len(golden) == 52 and len({row["qid"] for row in golden}) == 52
    bases = {}
    for row in golden:
        base = row["base_qid"]
        assert base not in bases or bases[base] == row["expected_behavior"]
        bases[base] = row["expected_behavior"]
    assert len(bases) == 26
    assert Counter(row["base_qid"] for row in golden) == Counter({base: 2 for base in bases})
    types = {
        row["qid"]: row.get("question_type") or row.get("semantic_type")
        for path in ("data/golden/golden_set_pilot_v1.jsonl", "data/golden/expansion_v3/question_design_v3.jsonl")
        for row in jsonl(path)
    }
    labels = {"factual": "Factual", "explanatory": "Explicativa", "comparative": "Comparativa", "procedural": "Procedimental", "procedimental": "Procedimental"}
    distribution = Counter((labels[types[base]], behavior) for base, behavior in bases.items())
    behaviors = ("answer", "grounded_correction", "abstain")
    question_rows = []
    for label in ("Factual", "Explicativa", "Comparativa", "Procedimental"):
        values = [distribution[label, behavior] for behavior in behaviors]
        question_rows.append([label, *map(str, values), str(sum(values))])
    totals = [sum(distribution[label, behavior] for label in set(labels.values())) for behavior in behaviors]
    assert totals == [17, 5, 4]
    question_rows.append(["Total", *map(str, totals), str(len(bases))])
    expected["tbl-preguntas-tipo-conducta"] = question_rows
    counts["tbl-preguntas-tipo-conducta"] = 20

    qrels = jsonl("outputs/local_runs/explicitness_v3/qrels_final_v3.jsonl")
    assert len(qrels) == len({row["unit_id"] for row in qrels}) == 578
    assert {row["base_qid"] for row in qrels} == set(bases)
    assert len({row["chunk_id"] for row in qrels}) == 223
    passes = Counter(row["pass_tag"] for row in qrels)
    assert passes == {"main": 458, "premise": 120}
    flagged = {row["base_qid"] for row in jsonl("data/golden/variants/question_premise_audit_v3.jsonl")}
    assert len(flagged) == 5
    assert all((row["base_qid"] in flagged) == (row["pass_tag"] == "premise") for row in qrels)
    grades = Counter(row["grade"] for row in qrels)
    sources = Counter(row["grade_source"] for row in qrels)
    assert set(grades) == {0, 1, 2} and set(sources) == {"judge_consensus", "arbitration", "human_validation"}
    expected["tbl-pool-final"] = [
        ["Relevancia", f"Grado {grade}", str(grades[grade])] for grade in (0, 1, 2)
    ] + [
        ["Procedencia", label, str(sources[key])]
        for key, label in (("judge_consensus", "Consenso de los dos jueces"), ("arbitration", "Arbitraje"), ("human_validation", "Decisión humana"))
    ] + [["Conjunto", "Total de pares únicos", str(len(qrels))]]
    counts["tbl-pool-final"] = 10
    checks = validate_document_tables(target, expected, expected_numeric_cells=counts)
    assert len(checks) == 11 and sum(r["numeric_cells"] for r in checks) == 389

    return checks


def main():
    """Valida datos, tablas y referencias de los PDF finales sin volver a renderizarlos."""
    audit = appendix.validate_data(ROOT)
    tech = appendix.validate_document(ROOT)
    target = (ROOT / 'tfm_v2_4.qmd').read_text()
    checks = validate_tables(target)
    pymupdf = importlib.import_module('pymupdf')
    pdf_info = {}
    main_text = ''
    for label, name in (
        ('main', 'tfm_AndresGonzalezSanchez.pdf'),
        ('sponsor', 'tfm_sponsor_AndresGonzalezSanchez.pdf'),
        ('appendix', 'tfm_apendices_tecnicos_AndresGonzalezSanchez.pdf'),
    ):
        with pymupdf.open(ROOT.parent / 'documentos' / name) as doc:
            text = '\n'.join(page.get_text() for page in doc)
            pdf_info[label + '_pages'] = len(doc)
        assert '??' not in text, name
        if label == 'main':
            main_text = text
    table_numbers = re.findall(r'Tabla\s+(\d+)\s*:', main_text)
    figure_numbers = re.findall(r'Figura\s+(\d+)\s*:', main_text)
    captions = re.findall(r'(?m)^: \*(.*?)\* \{#tbl-[\w-]+\}', target)
    assert len(captions) == 24
    assert table_numbers == [str(n) for n in range(1, len(captions) + 1)], table_numbers
    assert figure_numbers == [str(n) for n in range(1, 10)], figure_numbers
    pdf_info['main_table_captions'] = len(captions)
    norm = lambda value: re.sub(r'\W+', ' ', unicodedata.normalize('NFKC', value).casefold()).strip()
    for caption in re.findall(r'(?m)^: \*(.*?)\* \{#tbl-[\w-]+\}', target):
        assert norm(caption.replace('\\', '')) in norm(main_text), caption
    print(json.dumps({
        'scope': 'final_delivery_artifact_contracts',
        'table_count': len(checks),
        'numeric_cells': sum(row['numeric_cells'] for row in checks),
        'tables': checks,
        'experiment': audit['experiment'],
        'attempts': audit['attempts'],
        'pdf': pdf_info,
        'appendix': tech,
        'new_inference': False,
        'documents_rendered': False,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
