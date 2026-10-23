"""The technical package locates the delivered PDFs outside its work root."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_final_validation_from_unrelated_cwd_uses_delivered_pdfs(tmp_path):
    assert ROOT.name == 'reproduccion'
    documents = ROOT.parent / 'documentos'
    for name in ('tfm_AndresGonzalezSanchez.pdf',
                 'tfm_sponsor_AndresGonzalezSanchez.pdf',
                 'tfm_apendices_tecnicos_AndresGonzalezSanchez.pdf'):
        assert (documents / name).is_file()
        assert not (ROOT / name).exists()
    result = subprocess.run(
        [sys.executable, str(ROOT / 'scripts/validate_final_results.py')],
        cwd=tmp_path, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report['table_count'] == 11
    assert report['numeric_cells'] == 389
    assert report['pdf']['main_pages'] == 57
    assert report['pdf']['sponsor_pages'] == 9
    assert report['pdf']['appendix_pages'] == 9
