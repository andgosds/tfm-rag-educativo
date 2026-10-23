"""Acceptance of the submitted package, not historical manuscript revisions."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


def test_final_table_contracts_and_delivered_pdf_are_verified():
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/validate_final_results.py')], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report['table_count'] == 11
    assert report['numeric_cells'] == 389
    assert report['experiment']['accepted'] == 604
    assert report['experiment']['failed'] == 20
    assert report['new_inference'] is False
    assert report['pdf']['main_pages'] == 57
    assert report['pdf']['sponsor_pages'] == 9
    assert report['pdf']['appendix_pages'] == 9


def test_replay_runner_rejects_unsafe_and_existing_destinations(tmp_path):
    import importlib
    import importlib.util
    pytest = importlib.import_module('pytest')
    path = ROOT / 'scripts/reproduce_offline.py'
    assert path.is_file(), 'Missing reproducibility runner'
    spec = importlib.util.spec_from_file_location('delivery_replay', path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for value in ('../escape', '/absolute', '.', '..', 'bad/name'):
        with pytest.raises(ValueError):
            module.destination(tmp_path, value)
    good = module.destination(tmp_path, 'tribunal_01')
    assert good.is_relative_to(tmp_path)
    assert not good.exists()
    good.mkdir(parents=True)
    with pytest.raises(FileExistsError):
        module.destination(tmp_path, 'tribunal_01')


def test_figure_runner_extracts_literal_r_code_from_final_sources():
    import importlib.util
    path = ROOT / 'scripts/reproduce_figures.py'
    assert path.is_file(), 'Missing figure reproduction runner'
    spec = importlib.util.spec_from_file_location('delivery_figures', path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    main = module.r_chunks((ROOT / 'tfm_v2_4.qmd').read_text())
    sponsor = module.r_chunks((ROOT / 'tfm_v2_4_sponsor.qmd').read_text())
    assert len(main) == 9 and len(sponsor) == 2
    assert sum(row['label'] is not None for row in main + sponsor) == 10
    assert main[0]['label'] == 'fig-chunks-capitulo'
    assert 'library(dplyr)' in main[0]['code']
