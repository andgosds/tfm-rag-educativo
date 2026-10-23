"""Recompute the final numerical results from included frozen evidence.

No retrieval/generation models or external judges are invoked. The submitted
PDFs and frozen artifacts are read only. Every invocation needs a fresh run ID.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def destination(root: Path, run_id: str) -> Path:
    """Valida el identificador y devuelve una ruta de salida todavía inexistente."""
    if not re.fullmatch(r'[A-Za-z0-9_.-]+', run_id) or run_id in ('.', '..'):
        raise ValueError('run-id must contain only letters, digits, dot, underscore or hyphen')
    allowed = (root / 'outputs/local_runs/final_experiment_20260930').resolve()
    target = (allowed / ('REPLAY_' + run_id)).resolve()
    if not target.is_relative_to(allowed) or target == allowed:
        raise ValueError('destination escapes the permitted output directory')
    if target.exists():
        raise FileExistsError(f'destination already exists: {target}')
    return target


def main() -> None:
    """Recalcula los resultados sin inferencia y compara los CSV con las referencias congeladas."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id', required=True)
    args = parser.parse_args()
    try:
        output = destination(ROOT, args.run_id)
    except (ValueError, FileExistsError) as error:
        parser.error(str(error))
    output.mkdir(parents=True, exist_ok=False)
    ir = ROOT / 'outputs/local_runs/explicitness_v3'
    commands = [
        ('validation', ['scripts/validate_final_results.py']),
        ('retrieval', ['scripts/evaluate_retrieval_v3.py', '--run-dir', str(ir),
                       '--qrels', str(ir / 'qrels_final_v3.jsonl'),
                       '--methods', 'bm25,dense,rrf,rerank',
                       '--output-dir', str(output / 'retrieval')]),
        ('paired', ['scripts/paired_explicitness_v3.py',
                    '--metrics-dir', str(output / 'retrieval'),
                    '--historical-metrics-dir', str(ir / 'retrieval_metrics_v3'),
                    '--output-dir', str(output / 'paired')]),
        ('capacity', ['scripts/analysis_capacity_v3.py',
                      '--output-dir', str(output / 'capacity')]),
        ('final', ['scripts/analyze_final_experiment.py',
                   '--output-dir', str(output / 'final')]),
    ]
    for label, arguments in commands:
        result = subprocess.run([sys.executable, *arguments], cwd=ROOT, capture_output=True, text=True)
        (output / (label + '.log')).write_text(result.stdout + '\n' + result.stderr)
        if result.returncode:
            raise RuntimeError(f'{label} failed; see {output / (label + ".log")}')
        if label == 'validation':
            (output / 'validation.json').write_text(result.stdout)
        print(label + ': OK', file=sys.stderr)
    corrected = ROOT / 'outputs/local_runs/academic_corrections_20260930'
    references = {
        'retrieval': corrected / 'retrieval/evaluation',
        'paired': corrected / 'retrieval/paired',
        'capacity': corrected / 'capacity/release_run1',
        'final': ROOT / 'outputs/local_runs/final_experiment_20260930/analysis',
    }
    compared = {}
    for label, reference in references.items():
        files = sorted(reference.glob('*.csv'))
        assert files, ('empty reference', reference)
        compared[label] = {}
        for source in files:
            generated = output / label / source.name
            # La igualdad de bytes comprueba tanto los valores como el formato del CSV.
            assert source.read_bytes() == generated.read_bytes(), (label, source.name, 'different results')
            compared[label][source.name] = hashlib.sha256(generated.read_bytes()).hexdigest()
    report = {
        'run_id': args.run_id,
        'new_inference': False,
        'documents_rendered': False,
        'frozen_sources_overwritten': False,
        'compared_csv_count': sum(map(len, compared.values())),
        'csv_sha256_equal_to_frozen': compared,
        'output': str(output.relative_to(ROOT)),
    }
    (output / 'reproduction_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
