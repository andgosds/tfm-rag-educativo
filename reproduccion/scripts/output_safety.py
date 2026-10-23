"""Fail closed before expensive work; never replace an existing run artifact."""
from pathlib import Path
import re


def guard_run_outputs(output_root, run_id, *extra_paths):
    """Valida el identificador y rechaza destinos que ya contienen artefactos de la run."""
    if not re.fullmatch(r'[A-Za-z0-9_.-]+', run_id) or run_id in ('.', '..'):
        raise ValueError('run_id must contain only letters, digits, dot, underscore or hyphen; not dot components')
    root = Path(output_root)
    paths = list(extra_paths)
    for folder in ('runs', 'metrics', 'embeddings', 'rerankers', 'latency'):
        directory = root / folder
        if directory.exists():
            paths.extend(p for p in directory.iterdir()
                         if p.name == run_id + '.jsonl' or p.name.startswith(run_id + '_'))
    for path in paths:
        if path is not None and (Path(path).exists() or Path(path).is_symlink()):
            raise FileExistsError(f'destination already exists: {path}')


def guard_cli_outputs(args, *, root=None, script=''):
    """CLI writes are confined to outputs/local_runs; no force override.

    Existing files are only allowed for explicit resumable generation/evaluation
    and review copies in that working area, never frozen study artifacts.
    """
    root = Path(root or Path(__file__).resolve().parents[1]).resolve()
    allowed = root / 'outputs/local_runs'
    fields = {'output', 'output_root', 'summary', 'risk_queue', 'metadata',
              'provenance', 'report', 'processed_dir'}
    values = vars(args)
    destinations = [(key, value) for key, value in values.items()
                    if key in fields and value is not None]
    if script in ('run_bm25', 'run_dense') and not values.get('qrels_input'):
        destinations.append(('qrels', values['qrels']))
    if script == 'extract_openstax_chapters':
        destinations.append(('interim_dir', values.get('interim_dir') or root/'data/interim'))
    if script == 'pool_review_app':
        destinations.append(('priority', values['priority']))
    if script == 'rag_review_app':
        destinations.append(('input', values['input']))
    for key, value in destinations:
        path = Path(value).resolve()
        if not path.is_relative_to(allowed) or path == allowed:
            raise ValueError(f'protected destination: {key}={value}; choose outputs/local_runs/NEW_RUN/...')
        resumable = script in ('run_rag_generation', 'evaluate_rag', 'pool_review_app', 'rag_review_app')
        if path.exists() and not resumable:
            raise FileExistsError(f'protected destination already exists: {path}')
    for key in ('run_id', 'benchmark_id', 'experiment_id'):
        if key in values and (not re.fullmatch(r'[A-Za-z0-9_.-]+', values[key]) or values[key] in ('.', '..')):
            raise ValueError(f'unsafe {key}')
