"""Targeted tests for the technical appendix, not the experimental suite.

uv run --no-sync python -m pytest -q docs/test_validar_apendices.py
"""
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

pytest = importlib.import_module('pytest')

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / 'docs/validar_apendices.py'
SPEC = importlib.util.spec_from_file_location('appendix_validator', VALIDATOR)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def test_frozen_data_validation_succeeds_without_manuscript_comparison():
    result = subprocess.run([sys.executable, str(VALIDATOR), '--data-only'], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report['scope'] == 'technical_appendix_only'
    assert report['experiment']['accepted'] == 604
    assert report['experiment']['failed'] == 20
    assert report['attempts'] == {'accepted': 614, 'failed': 60}
    assert report['base_behavior'] == {'answer': 17, 'grounded_correction': 5, 'abstain': 4}
    assert report['frozen_artifact_integrity'] is True
    assert report['document_checked'] is False
    assert report['new_inference'] is False


def test_reproduction_is_led_by_the_five_current_notebooks():
    """Exige el recorrido actual y su comprobación en la fuente y el PDF."""
    report = validator.validate_document(ROOT)
    assert report['notebooks_checked'] == 5
    assert report['reproduction_entrypoint'] == 'notebooks'


def test_default_command_checks_the_independent_appendix():
    result = subprocess.run([sys.executable, str(VALIDATOR)], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report['document_checked'] is True
    assert report['document']['source'] == 'tfm_v2_4_apendices_tecnicos.qmd'
    assert report['document']['pdf'] == 'tfm_apendices_tecnicos_AndresGonzalezSanchez.pdf'
    assert report['document']['tables_checked'] == 2
    assert report['document']['shell_blocks_checked'] == 7
    assert report['document']['unresolved_references'] == []


@pytest.mark.parametrize('old,new', [
    ('$k_1=1,5$', '$k_1=1,6$'),
    ('26 preguntas base y 52 formulaciones:', '27 preguntas base y 52 formulaciones:'),
    ('614 intentos', '615 intentos'),
    ('docs/validar_apendices.py', 'docs/inexistente.py'),
    ('notebooks/verify_notebooks.py', 'notebooks/\nverify_notebooks.py'),
])
def test_document_rejects_changed_values_or_broken_recipes(old, new):
    text = (ROOT / 'tfm_v2_4_apendices_tecnicos.qmd').read_text()
    assert old in text
    with pytest.raises(AssertionError):
        validator.validate_document(ROOT, source_text=text.replace(old, new))


def test_default_validation_preserves_protected_documents():
    protected = [ROOT / name for name in ('tfm_v2_4.qmd', 'tfm_v2_4_sponsor.qmd', 'tfm_v2_4_apendices_tecnicos.qmd')]
    pdfs = [ROOT.parent / 'documentos' / name for name in ('tfm_AndresGonzalezSanchez.pdf', 'tfm_sponsor_AndresGonzalezSanchez.pdf', 'tfm_apendices_tecnicos_AndresGonzalezSanchez.pdf')]
    assert all(p.is_file() for p in pdfs)
    protected += pdfs
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    result = subprocess.run([sys.executable, str(VALIDATOR)], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert before == {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
