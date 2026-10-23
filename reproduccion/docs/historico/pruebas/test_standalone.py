"""Standalone contract: no sibling repository is required."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class StandaloneTests(unittest.TestCase):
    def test_local_kernel_and_corpus_are_available(self):
        self.assertTrue((ROOT / 'scripts/run_bm25.py').is_file(), 'local ranking kernel missing')
        self.assertTrue((ROOT / 'data/processed/chunks_v1.jsonl').is_file(), 'local corpus missing')
        spec = importlib.util.spec_from_file_location('campaign_probe', ROOT/'scripts/explicitness_campaign.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.ROOT, ROOT)

    def test_inherited_frozen_bytes_match_manifest(self):
        import hashlib
        manifest = json.loads((ROOT/'config/standalone_migration_manifest.json').read_text())
        for item in manifest['files']:
            if not item['adapted']:
                self.assertEqual(hashlib.sha256((ROOT/item['target']).read_bytes()).hexdigest(), item['source_sha256'], item['target'])

    def test_explicitness_notebook_reads_closed_reuse_including_adjustments(self):
        notebook = json.loads((ROOT/'notebooks/09_explicitud_y_pendientes.ipynb').read_text())
        cells = [c for c in notebook['cells'] if c['cell_type'] == 'code']
        book = json.loads((ROOT/'data/golden/variants/explicitness_reuse_adjudications_v1.jsonl').read_text())
        env = {
            'pairs': [json.loads(s) for s in (ROOT/'data/golden/variants/explicitness_pairs_v1_consolidated.jsonl').read_text().splitlines() if s.strip()],
            'reuse': book['adjudications'] + book['grade_1_2_proposals'],
            'blind': [json.loads(s) for s in (ROOT/'outputs/explicitness_v2/pools/blind_review_queue.jsonl').read_text().splitlines() if s.strip()],
        }
        exec(''.join(cells[2]['source']), env)
        self.assertEqual(len(env['confirmed']), 98)
        self.assertEqual(len(env['pending']), 0)
        self.assertEqual(sum(r['reuse_status'] == 'confirmed_with_adjustment' for r in env['confirmed']), 2)

    def test_registered_inputs_resolve_locally(self):
        config = json.loads((ROOT/'config/inputs_v2.json').read_text())
        self.assertEqual(config['path_base'], 'v2_root')
        for path in config['shared_inputs']:
            target = (ROOT/path).resolve()
            self.assertTrue(target.is_relative_to(ROOT))
            self.assertTrue(target.is_file(), path)

if __name__ == '__main__':
    unittest.main()
