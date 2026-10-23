"""Ejecuta los cinco cuadernos de la entrega en kernels independientes."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
import re
import sys
import time

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

from notebook_support import new_run

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED = [
    '00_entorno_corpus_y_dataset.ipynb', '01_preguntas_evidencias_y_qrels.ipynb',
    '02_recuperacion_y_explicitud.ipynb', '03_respuestas_evaluacion_y_decisiones.ipynb',
    '04_comparaciones_finales_y_verificacion.ipynb',
]


def snapshot(root):
    """Calcula huellas en memoria, excluyendo cachés y salidas de ejecución."""
    result = {}
    for path in root.rglob('*'):
        relative = path.relative_to(root)
        if any(part in ('.venv', '__pycache__', '.pytest_cache', '.ipynb_checkpoints', '.git')
               or part.startswith('REPLAY_') for part in relative.parts):
            continue
        if path.is_file():
            result[str(relative)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def execute_notebook(source, output, timeout=900, figures=False):
    """Ejecuta un cuaderno con este intérprete y guarda la copia, incluso si falla."""
    notebook = nbformat.read(source, as_version=4)
    nbformat.validate(notebook)
    if figures and source.name == EXPECTED[-1]:
        for cell in notebook.cells:
            if cell.cell_type == 'code' and 'REGENERAR_FIGURAS = False' in cell.source:
                cell.source = cell.source.replace('REGENERAR_FIGURAS = False', 'REGENERAR_FIGURAS = True')
    manager = KernelManager(kernel_name='python3')
    assert manager.kernel_spec is not None
    # El kernel usa el Python del verificador, aunque python3 esté registrado fuera del proyecto.
    manager.kernel_spec.argv = [os.path.abspath(sys.executable), '-m', 'ipykernel_launcher', '-f', '{connection_file}']
    start = time.monotonic()
    record = {'notebook': source.name, 'status': 'failed'}
    try:
        NotebookClient(notebook, km=manager, timeout=timeout, allow_errors=False,
                       resources={'metadata': {'path': str(HERE)}}).execute()
        cells = [cell for cell in notebook.cells if cell.cell_type == 'code']
        assert cells and all(cell.execution_count is not None for cell in cells)
        assert not any(o.output_type == 'error' for cell in cells for o in cell.outputs)
        saved = json.dumps([cell.outputs for cell in cells], ensure_ascii=False)
        assert not re.search(r'sk-[A-Za-z0-9]{20,}|Bearer [A-Za-z0-9._-]{20,}', saved)
        record.update(status='passed', code_cells=len(cells),
                      executed_cells=sum(cell.execution_count is not None for cell in cells))
    except Exception as error:
        record.update(error_type=type(error).__name__, error=str(error))
    finally:
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)
        nbformat.write(notebook, output)
    record['duration_s'] = round(time.monotonic() - start, 3)
    return record


def main():
    """Ejecuta la colección completa y comprueba resultados y archivos protegidos."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--figures', action='store_true', help='Ejecutar también la etapa R opcional del cuaderno final.')
    parser.add_argument('--timeout', type=int, default=900, help='Tiempo máximo por celda, en segundos.')
    args = parser.parse_args()
    names = sorted(path.name for path in HERE.glob('*.ipynb'))
    assert names == EXPECTED, (names, EXPECTED)
    before = snapshot(ROOT.parent)
    replay_root = ROOT / 'outputs/local_runs/final_experiment_20260930'
    prior_reports = set(replay_root.glob('REPLAY_*/reproduction_report.json'))
    prior_figures = set(replay_root.glob('REPLAY_*/figures_report.json'))
    output = new_run('ejecucion', root=ROOT)
    executed = output / 'executed'
    executed.mkdir()
    records = []
    for name in names:
        record = execute_notebook(HERE / name, executed / name, timeout=args.timeout, figures=args.figures)
        records.append(record)
        print(f'{name}: {record["status"]} ({record["duration_s"]} s)', flush=True)
    new_reports = sorted(set(replay_root.glob('REPLAY_*/reproduction_report.json')) - prior_reports)
    reports = [json.loads(path.read_text()) for path in new_reports]
    after = snapshot(ROOT.parent)
    changed = sorted(path for path in before.keys() | after.keys() if before.get(path) != after.get(path))
    new_figures = sorted(set(replay_root.glob('REPLAY_*/figures_report.json')) - prior_figures)
    figure_reports = [json.loads(path.read_text()) for path in new_figures]
    report = {
        'execution_date': datetime.now(timezone.utc).isoformat(),
        'requested_notebooks': len(names), 'attempted_notebooks': len(records),
        'passed_notebooks': sum(row['status'] == 'passed' for row in records),
        'executed_code_cells': sum(row.get('executed_cells', 0) for row in records),
        'notebooks': records, 'protected_files_checked': len(before),
        'protected_files_unchanged': not changed, 'changed_protected_files': changed,
        'reproduction_reports': reports, 'figures_requested': args.figures,
        'figure_reports': figure_reports, 'new_inference': False, 'documents_rendered': False,
        'output': str(output.relative_to(ROOT)),
    }
    (output / 'notebooks_validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    assert not changed, changed
    assert report['passed_notebooks'] == len(names), 'Hay cuadernos con errores; consulte las copias ejecutadas.'
    assert len(reports) == 1 and reports[0]['compared_csv_count'] == 35
    if args.figures:
        assert len(figure_reports) == 1 and figure_reports[0]['svg_count'] == 10
    print('Informe:', report['output'] + '/notebooks_validation.json', flush=True)


if __name__ == '__main__':
    main()
