"""Read-only validation for the independent technical appendix.

Run from reproduccion/: uv run --no-sync python docs/validar_apendices.py
No inference, historical writes, main-manuscript edits or editorial comparisons.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import hashlib
import importlib
import re
import subprocess
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
closure = importlib.import_module('validate_tfm_closure')


def validate_data(root: Path) -> dict:
    """Comprueba cobertura, intentos y fuentes congeladas del experimento final."""
    report, _ = closure.build_report(root, check_tables=False)
    campaign = root / 'outputs/local_runs/generation_scaling_v3'
    accepted, failed = [], []
    for slug in closure.V3_MODELS.values():
        for condition in closure.V3_CONDITIONS:
            path = campaign / f'rag_{condition}_top5_{slug}.jsonl'
            accepted.extend(json.loads(line) for line in path.read_text().splitlines() if line.strip())
            failures = path.with_name(path.stem + '_failures.jsonl')
            if failures.exists():
                failed.extend(json.loads(line) for line in failures.read_text().splitlines() if line.strip())
    attempts = {
        'accepted': sum(row['generation_attempts'] for row in accepted),
        'failed': sum(row['generation_attempts'] for row in failed),
    }
    assert attempts == {'accepted': 614, 'failed': 60}, attempts
    golden = [json.loads(line) for line in (root / 'data/golden/variants/generation_golden_v3.jsonl').read_text().splitlines() if line.strip()]
    bases = {}
    for row in golden:
        assert row['base_qid'] not in bases or bases[row['base_qid']] == row['expected_behavior']
        bases[row['base_qid']] = row['expected_behavior']
    assert len(golden) == 52 and len(bases) == 26
    assert Counter(row['base_qid'] for row in golden) == Counter({base: 2 for base in bases})
    behavior = dict(Counter(bases.values()))
    assert behavior == {'answer': 17, 'grounded_correction': 5, 'abstain': 4}
    analysis = root / 'outputs/local_runs/final_experiment_20260930/analysis'
    operation_counts = {}
    for name, expected in [('operational.csv', 12), ('operational_summary.csv', 24), ('operational_cells.csv', 624), ('paired_contrasts.csv', 72)]:
        with (analysis / name).open() as stream:
            operation_counts[name] = len(list(csv.DictReader(stream)))
        assert operation_counts[name] == expected, (name, operation_counts[name])
    return {
        'scope': 'technical_appendix_only',
        'experiment': report['academic_campaigns']['v3'],
        'attempts': attempts,
        'base_behavior': behavior,
        'operational_files': operation_counts,
        'frozen_artifact_integrity': report['academic_inputs_unchanged'] and report['academic_campaigns']['corrections']['artifact_hashes_verified'],
        'document_checked': False,
        'new_inference': False,
        'full_experimental_test_suite': False,
    }


def validate_document(root: Path, source_text: str | None = None) -> dict:
    """Contrasta tablas y recetas del apéndice con su PDF y los artefactos."""
    pymupdf = importlib.import_module('pymupdf')

    source = root / 'tfm_v2_4_apendices_tecnicos.qmd'
    # El PDF de lectura está separado de la fuente QMD y del paquete técnico.
    pdf = root.parent / 'documentos' / 'tfm_apendices_tecnicos_AndresGonzalezSanchez.pdf'
    text = source.read_text() if source_text is None else source_text
    norm = lambda value: re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', value)).strip()
    with pymupdf.open(pdf) as document:
        pages = [norm(page.get_text()) for page in document]
    combined = ' '.join(pages)
    assert '??' not in combined, 'Unresolved PDF reference'
    table_ids = ['tbl-apendice-config-retrieval', 'tbl-apendice-contrato-generacion']
    first = closure._document_table(text, table_ids[0])
    second = closure._document_table(text, table_ids[1])
    assert len(first) == 4
    assert [row[0] for row in first] == ['BM25', 'Dense', 'RRF', 'RRF + reranking']
    cfg = json.loads((root / 'outputs/local_runs/explicitness_v3/configuration.json').read_text())
    assert cfg['bm25_k1'] == 1.5 and cfg['bm25_b'] == 0.75
    assert cfg['top_k'] == cfg['fusion_depth'] == 10 and cfg['k0'] == 60
    assert cfg['dense_model'] in first[1][1] and cfg['reranker_model'] in first[3][1]
    assert '$k_1=1,5$' in first[0][1] and '$b=0,75$' in first[0][1]
    assert '$k_0=60$' in first[2][1]
    assert all('10' in row[2] or 'diez' in row[2] for row in first)
    fields = {row[0]: row[1] for row in second}
    required_fields = {
        'Preguntas': ('26 preguntas base', '52 formulaciones', '17 preguntas base', 'cinco', 'cuatro'),
        'Generadores': tuple(closure.V3_MODELS),
        'Decodificación': ('Temperatura 0', '20260902', '300', '8192', 'adaptador'),
        'Prompt generativo': ('rag_answer_prompt_v1', 'cinco fragmentos', 'tres intentos totales'),
        'Evaluación válida': ('ragas_rubric_v3.2', 'instrumento ordinal propio', 'dos jueces'),
        'Jueces': ('gpt-6-sol', 'openai-codex', 'mimo-v2.6-pro', 'opencode-go'),
        'Arbitraje y cierre': ('gpt-6-astra', 'validación humana'),
        'Agregación': ('pregunta base', 'soporte común'),
        'Incertidumbre': ('5.000', '20260928', 'IC puntuales'),
        'Fuentes de respuestas': ('Doce archivos', 'generation_scaling_v3'),
    }
    assert len(second) == len(required_fields)
    assert set(fields) == set(required_fields)
    for label, fragments in required_fields.items():
        assert all(fragment in fields[label] for fragment in fragments), (label, 'configuration changed')
    for caption in re.findall(r'(?m)^: \*(.*?)\* \{#tbl-[\w-]+\}', text):
        assert norm(caption) in combined, (caption, 'absent from PDF')
    assert re.findall(r'(?m)^## ([CDE])\. ', text) == ['C', 'D', 'E']
    anchors = re.findall(r'\{#((?:tbl|fig|sec)-[\w-]+)\}', text)
    assert len(anchors) == len(set(anchors)) == 2
    refs = set(re.findall(r'@((?:tbl|fig|sec)-[\w-]+)', text))
    unresolved = sorted(refs - set(anchors))
    assert not unresolved
    blocks = re.findall(r'(?ms)^```bash\n(.*?)^```', text)
    assert len(blocks) == 7
    for block in blocks:
        result = subprocess.run(['bash', '-n'], input=block, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        assert max(map(len, block.splitlines())) <= 64, 'Shell line too long for the PDF'
        assert any(norm(block) in page for page in pages), 'Shell block wraps a token or splits across PDF pages'
    notebook_names = (
        '00_entorno_corpus_y_dataset.ipynb',
        '01_preguntas_evidencias_y_qrels.ipynb',
        '02_recuperacion_y_explicitud.ipynb',
        '03_respuestas_evaluacion_y_decisiones.ipynb',
        '04_comparaciones_finales_y_verificacion.ipynb',
    )
    assert {path.name for path in (root / 'notebooks').glob('*.ipynb')} == set(notebook_names)
    for name in notebook_names:
        assert name in text and name in combined, (name, 'Notebook absent from source or PDF')
    assert '### E.2. Reproducción mediante notebooks' in text
    for command in (
        'cd reproduccion', 'uv sync --locked --group dev',
        'uv run --no-sync jupyter lab notebooks',
        'uv run --no-sync python notebooks/verify_notebooks.py',
        'scripts/reproduce_offline.py', 'scripts/reproduce_figures.py',
    ):
        assert command in text and command in combined, command
    assert '35 CSV' in norm(text.replace('**', '')) and '35 CSV' in combined
    assert 'verification/notebooks_validation.json' in text
    assert 'docs/validar_apendices.py' in text
    assert 'python docs/validate_tfm_v2_4_editorial.py' not in text
    assert 'python scripts/validate_tfm_closure.py' not in text
    assert 'quarto render tfm_v2_4.qmd' not in text
    assert 'quarto render tfm_v2_4_sponsor.qmd' not in text
    for phrase in ('614 intentos', 'sesenta', '624 registros individuales', '158 celdas y 233 criterios', '446 casos de consenso'):
        assert phrase in norm(text.replace('**', '')) and phrase in combined, phrase
    return {
        'source': source.name, 'pdf': pdf.name, 'pdf_pages': len(pages),
        'tables_checked': 2, 'shell_blocks_checked': len(blocks),
        'notebooks_checked': len(notebook_names),
        'reproduction_entrypoint': 'notebooks',
        'shell_blocks_whole_and_copyable': True,
        'unresolved_references': unresolved,
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'pdf_sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
    }


def main() -> None:
    """Ejecuta la comprobación técnica e imprime el informe JSON."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-only', action='store_true', help='Check frozen data without requiring the appendix PDF.')
    args = parser.parse_args()
    report = validate_data(ROOT)
    if not args.data_only:
        report['document'] = validate_document(ROOT)
        report['document_checked'] = True
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
