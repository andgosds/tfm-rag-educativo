"""Rutas y ejecución de los análisis offline de los cuadernos."""
from pathlib import Path
import json
import re
import subprocess
import sys
from uuid import uuid4

OFFLINE_SCRIPTS = {
    'scripts/validate_final_results.py', 'docs/validar_apendices.py',
    'scripts/evaluate_retrieval_v3.py', 'scripts/paired_explicitness_v3.py',
    'scripts/analysis_capacity_v3.py', 'scripts/analyze_final_experiment.py',
    'scripts/reproduce_offline.py', 'scripts/reproduce_figures.py',
}


def read_jsonl(path):
    """Lee los registros de un JSONL sin modificar el archivo de origen."""
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def find_root(start=None):
    """Localiza la raíz técnica a partir del directorio de trabajo."""
    start = Path(start or Path.cwd()).resolve()
    for candidate in (start, *start.parents):
        if (candidate / 'config/inputs_v2.json').is_file() and (candidate / 'scripts/reproduce_offline.py').is_file():
            return candidate
    raise FileNotFoundError('Abra los notebooks desde reproduccion/ o uno de sus subdirectorios.')


def new_run(label, root=None):
    """Crea un destino exclusivo sin reemplazar ejecuciones anteriores."""
    if not re.fullmatch(r'[A-Za-z0-9_-]+', label):
        raise ValueError('La etiqueta solo admite letras, números, guion y guion bajo.')
    root = Path(root) if root is not None else find_root()
    output = root / 'outputs/local_runs/final_experiment_20260930' / f'REPLAY_notebook_{label}_{uuid4().hex[:12]}'
    output.mkdir(parents=True, exist_ok=False)
    return output


def run_script(script, *arguments, log_dir, root=None):
    """Ejecuta un análisis offline con el Python del kernel y conserva su log."""
    if script not in OFFLINE_SCRIPTS:
        raise ValueError('Este auxiliar solo ejecuta los análisis offline de la entrega.')
    root = Path(root) if root is not None else find_root()
    # El mismo intérprete evita depender de otro entorno o kernelspec local.
    result = subprocess.run([sys.executable, str(root / script), *map(str, arguments)],
                            cwd=root, capture_output=True, text=True)
    log = Path(log_dir) / (Path(script).stem + '.log')
    log.write_text(result.stdout + '\n' + result.stderr)
    if result.returncode:
        raise RuntimeError(f'{script} terminó con error. Log: {log}\n{result.stderr}')
    return result.stdout


def compare_csv(generated, reference):
    """Compara el conjunto de CSV y sus bytes con las referencias congeladas."""
    generated, reference = Path(generated), Path(reference)
    names = {p.name for p in reference.glob('*.csv')}
    assert names, f'No hay CSV de referencia en {reference}'
    assert names == {p.name for p in generated.glob('*.csv')}, 'El conjunto de CSV difiere.'
    checked = []
    for name in sorted(names):
        assert (generated / name).read_bytes() == (reference / name).read_bytes(), name
        checked.append({'archivo': name, 'identico': True})
    return checked
