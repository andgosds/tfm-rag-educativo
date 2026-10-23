"""Lightweight contracts; full kernel execution uses notebooks/verify_notebooks.py."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def support():
    path = ROOT / 'notebooks/notebook_support.py'
    assert path.is_file(), 'Missing support for the principal reproduction notebooks'
    spec = importlib.util.spec_from_file_location('delivery_notebook_support', path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_notebook_root_is_portable_from_nested_directory():
    module = support()
    assert module.find_root(ROOT / 'data/golden') == ROOT


def test_reanalysis_uses_fresh_outputs_and_rejects_model_calls(tmp_path):
    import pytest
    module = support()
    first = module.new_run('prueba', root=tmp_path)
    second = module.new_run('prueba', root=tmp_path)
    assert first != second and first.is_dir() and second.is_dir()
    assert first.is_relative_to(tmp_path / 'outputs/local_runs/final_experiment_20260930')
    assert first.name.startswith('REPLAY_')
    with pytest.raises(ValueError):
        module.new_run('../escape', root=tmp_path)
    with pytest.raises(ValueError):
        module.run_script('scripts/run_rag_generation.py', log_dir=first, root=tmp_path)


def test_csv_check_requires_exact_files_and_bytes(tmp_path):
    import pytest
    module = support()
    source, generated = tmp_path / 'source', tmp_path / 'generated'
    source.mkdir()
    generated.mkdir()
    (source / 'a.csv').write_text('x\n1\n')
    (generated / 'a.csv').write_text('x\n1\n')
    assert module.compare_csv(generated, source) == [{'archivo': 'a.csv', 'identico': True}]
    (generated / 'a.csv').write_text('x\n2\n')
    with pytest.raises(AssertionError):
        module.compare_csv(generated, source)
    (generated / 'a.csv').write_text('x\n1\n')
    (generated / 'extra.csv').write_text('x\n1\n')
    with pytest.raises(AssertionError):
        module.compare_csv(generated, source)


def test_five_notebooks_cover_the_final_experiment_with_executable_cells():
    import ast
    import nbformat
    files = sorted((ROOT / 'notebooks').glob('*.ipynb'))
    assert len(files) == 5
    required = ['00_entorno_corpus_y_dataset', '01_preguntas_evidencias_y_qrels',
                '02_recuperacion_y_explicitud', '03_respuestas_evaluacion_y_decisiones',
                '04_comparaciones_finales_y_verificacion']
    assert [p.stem for p in files] == required
    for path in files:
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        cells = [c for c in notebook.cells if c.cell_type == 'code']
        assert len(cells) >= 5
        for cell in cells:
            ast.parse(cell.source)
            assert '/home/' not in cell.source
    final = nbformat.read(files[-1], as_version=4)
    text = '\n'.join(cell.source for cell in final.cells)
    assert 'scripts/reproduce_offline.py' in text and 'compared_csv_count' in text
    retrieval = nbformat.read(files[2], as_version=4)
    text = '\n'.join(cell.source for cell in retrieval.cells)
    assert 'scripts/evaluate_retrieval_v3.py' in text
    assert 'scripts/paired_explicitness_v3.py' in text
