"""Offline regression tests; no models, no writes to historical artifacts."""
import importlib.util
from pathlib import Path
import unittest
import math
import inspect
import subprocess
import sys
import tempfile
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('capacity', ROOT / 'scripts/analysis_capacity_v3.py')
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


def row(g, c, value, formulation='explicit', base='b', behavior='answer'):
    return dict(qid=base+'__'+formulation, base_qid=base, generator_model=g,
                retrieval_condition=c, expected_behavior=behavior,
                **{k: min(value,1) if k=='citations_ok' else value for k in m.CRIT})


class CapacityCorrections(unittest.TestCase):
    def test_h5_common_capacity_table_has_same_formulations_across_models(self):
        self.assertIn('common',inspect.signature(m.h5).parameters)
        self.assertIn('common',inspect.signature(m.h5_comparaciones).parameters)
        rows = [row(g,c,0) for g in m.MODELOS for c in m.CONDS]
        rows += [row(g,c,int(c=='rerank'),base='b2') for g in m.MODELOS[1:] for c in m.CONDS]
        available = m.h5(rows)
        common = m.h5(rows,common=True)
        for r in common:
            self.assertEqual(r['n_cells'],1)
            self.assertEqual(r['ventaja'],0)
        q = next(r for r in available if r['generator_model']==m.MODELOS[1] and r['criterion']=='faithfulness')
        self.assertEqual(q['ventaja'],0.5)
        pairs = m.h5_comparaciones(rows,common=True)
        self.assertEqual(len(pairs),72)
        self.assertTrue(all(r['n_cells']==1 for r in pairs))

    def test_available_formulation_effects_are_not_silently_common_after_first_model(self):
        rows = [row(g,'bm25',0,form) for g in m.MODELOS for form in ('explicit','implicit')]
        rows += [row(g,'dense',int(form=='implicit'),form) for g in m.MODELOS[1:] for form in ('explicit','implicit')]
        available = m.h6_explicitud(rows)
        common = m.h6_explicitud(rows,common=True)
        for g in m.MODELOS[1:]:
            a = next(x for x in available if x['generator_model']==g and x['criterion']=='faithfulness')
            c = next(x for x in common if x['generator_model']==g and x['criterion']=='faithfulness')
            self.assertEqual(a['n_cells'],2)
            self.assertEqual(a['diff_implicit_minus_explicit'],0.5)
            self.assertEqual(c['n_cells'],1)
            self.assertEqual(c['diff_implicit_minus_explicit'],0)

    def test_real_cli_two_runs_are_byte_identical_traced_and_do_not_change_sources(self):
        capacity = ROOT/'outputs/local_runs/academic_corrections_20260930/capacity'
        capacity.mkdir(parents=True,exist_ok=True)
        protected = {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in m.RUN.rglob('*') if p.is_file()}
        with tempfile.TemporaryDirectory(dir=capacity) as tmp:
            outputs = [Path(tmp)/name for name in ('one','two')]
            for output in outputs:
                result = subprocess.run([sys.executable,str(ROOT/'scripts/analysis_capacity_v3.py'),'--output-dir',str(output)],capture_output=True,text=True)
                self.assertEqual(result.returncode,0,result.stderr)
            files = sorted(p.name for p in outputs[0].iterdir())
            self.assertEqual(files,sorted(p.name for p in outputs[1].iterdir()))
            for name in files:
                self.assertEqual((outputs[0]/name).read_bytes(),(outputs[1]/name).read_bytes(),name)
            tables = json.loads((outputs[0]/'tables.json').read_text())
            self.assertEqual(tables['n_cells'],604)
            self.assertEqual(tables['primary_content']['n_cells'],509)
            self.assertEqual(tables['sensitivity_abstain']['n_cells'],95)
            self.assertEqual(tables['coverage_summary']['n_planned'],624)
            self.assertEqual(tables['coverage_summary']['n_failed'],20)
            manifest = json.loads((outputs[0]/'hash_manifest.json').read_text())
            self.assertIn('scripts/analysis_capacity_v3.py',manifest['sources'])
            for name,digest in manifest['outputs'].items():
                self.assertEqual(hashlib.sha256((outputs[0]/name).read_bytes()).hexdigest(),digest)
        self.assertEqual(protected,{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in m.RUN.rglob('*') if p.is_file()})

    def test_cli_requires_new_output_dir_and_rejects_existing_before_analysis(self):
        self.assertIn('argv',inspect.signature(m.main).parameters)
        command = [sys.executable,str(ROOT/'scripts/analysis_capacity_v3.py')]
        missing = subprocess.run(command,capture_output=True,text=True)
        self.assertNotEqual(missing.returncode,0)
        self.assertIn('--output-dir',missing.stderr)
        capacity = ROOT/'outputs/local_runs/academic_corrections_20260930/capacity'
        capacity.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=capacity) as tmp:
            sentinel = Path(tmp)/'untouched'
            sentinel.write_bytes(b'protected')
            result = subprocess.run(command+['--output-dir',tmp],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('exists',result.stderr)
            self.assertEqual(sentinel.read_bytes(),b'protected')
        outside = subprocess.run(command+['--output-dir',str(ROOT/'capacity_forbidden')],capture_output=True,text=True)
        self.assertNotEqual(outside.returncode,0)
        self.assertFalse((ROOT/'capacity_forbidden').exists())

    def test_contrasts_trace_cells_then_base_means_and_sign_test_ties(self):
        a,b = m.MODELOS[:2]
        rows = [row(a,'bm25',0),row(b,'bm25',1),row(a,'dense',2),row(b,'dense',1),
                row(a,'bm25',0,base='b2'),row(b,'bm25',1,base='b2')]
        result = next(x for x in m.h6_pendientes(rows) if x['from_model']==a and x['to_model']==b and x['criterion']=='faithfulness')
        self.assertIn('base_differences',result)
        self.assertEqual(result['base_differences'],{'b':0,'b2':1})
        self.assertEqual(result['diff'],0.5)
        self.assertEqual((result['positive'],result['negative'],result['ties']),(1,0,1))
        self.assertEqual(result['sign_p_two_sided'],1)
        self.assertEqual(len(result['cell_differences']),3)

    def test_score_validation_rejects_wrong_scale_nonfinite_and_boolean(self):
        good = row(m.MODELOS[0],'bm25',2)
        for cr,value in [('citations_ok',2),('faithfulness',3),('behavior_ok',True),('factual_correctness',math.nan)]:
            with self.subTest(cr=cr), self.assertRaises(ValueError):
                m.enrich_evaluations([dict(good,**{cr:value})],[good])

    def test_factual_na_is_intersected_per_criterion_not_complete_case(self):
        a,b = m.MODELOS[:2]
        rows = [row(a,'bm25',0),row(b,'bm25',1),row(a,'dense',2),row(b,'dense',0)]
        rows[-1]['factual_correctness'] = 'na'
        results = {x['criterion']:x for x in m.h6_pendientes(rows) if x['from_model']==a and x['to_model']==b}
        self.assertEqual(results['factual_correctness']['diff'],1)
        self.assertEqual(results['factual_correctness']['n_cells'],1)
        self.assertEqual(results['faithfulness']['diff'],-0.5)
        self.assertEqual(results['faithfulness']['n_cells'],2)

    def test_primary_content_and_common_levels_preserve_na_and_abstention_sensitivity(self):
        self.assertTrue(callable(getattr(m,'build_tables',None)))
        rows = [row(g,'bm25',1) for g in m.MODELOS]
        rows += [row(g,'bm25',0,base='ab',behavior='abstain') for g in m.MODELOS]
        rows += [row(m.MODELOS[0],'dense',2)]
        rows[-1]['factual_correctness'] = 'na'
        tables = m.build_tables(rows)
        self.assertEqual(tables['scales']['citations_ok'],[0,1])
        self.assertEqual(tables['scales']['faithfulness'],[0,2])
        main = tables['primary_content']
        first = main['h6_niveles'][0]
        self.assertEqual(first['n_rows'],2)
        self.assertEqual(first['faithfulness'],1.5)
        self.assertEqual(first['factual_correctness'],1)
        self.assertEqual(first['factual_correctness_n_cells'],1)
        self.assertEqual(main['h6_niveles_common'][0]['faithfulness'],1)
        self.assertEqual(tables['sensitivity_all']['h6_niveles'][0]['n_rows'],3)
        self.assertEqual(tables['sensitivity_abstain']['h6_niveles'][0]['faithfulness'],0)

    def test_expected_behavior_join_uses_full_key_without_mutating_scores(self):
        self.assertTrue(callable(getattr(m,'enrich_evaluations',None)))
        a,b = m.MODELOS[:2]
        scores = [row(a,'bm25',1), row(b,'bm25',2)]
        generations = [dict(scores[0],expected_behavior='answer'), dict(scores[1],expected_behavior='abstain')]
        for r in scores:
            r['expected_behavior'] = None
        enriched = m.enrich_evaluations(scores,generations)
        self.assertEqual([r['expected_behavior'] for r in enriched],['answer','abstain'])
        self.assertEqual([r['faithfulness'] for r in enriched],[1,2])
        self.assertIsNone(scores[0]['expected_behavior'])
        with self.assertRaises(ValueError):
            m.enrich_evaluations(scores,generations[:1])
        with self.assertRaises(ValueError):
            m.enrich_evaluations(scores,generations+generations[:1])

    def test_interaction_is_difference_of_differences_on_four_common_cells(self):
        self.assertTrue(callable(getattr(m, 'h6_interaccion', None)))
        a,b = m.MODELOS[:2]
        rows = [row(a,'bm25',0), row(a,'bm25',0,'implicit'), row(a,'dense',2),
                row(b,'bm25',0), row(b,'bm25',1,'implicit'), row(b,'dense',2,'implicit')]
        result = next(x for x in m.h6_interaccion(rows) if x['from_model']==a and x['to_model']==b and x['criterion']=='faithfulness')
        self.assertEqual(result['diff_of_diffs'],1)
        self.assertEqual(result['n_cells'],1)
        self.assertEqual(result['effect_from'] ,0)
        self.assertEqual(result['effect_to'],1)
        self.assertEqual(result['ic95_lo'],1)
        self.assertEqual(result['ic95_hi'],1)

    def test_all_six_strategy_pairs_use_exact_formulation(self):
        self.assertTrue(callable(getattr(m, 'h5_comparaciones', None)))
        rows = [row(g,c,i/3) for g in m.MODELOS for i,c in enumerate(m.CONDS)]
        rows.append(row(m.MODELOS[0], 'bm25', 2, 'implicit'))
        results = m.h5_comparaciones(rows)
        self.assertEqual(len(results), 3*4*6)
        for result in results:
            self.assertNotEqual(result['from_condition'], result['to_condition'])
            self.assertEqual(result['n_cells'], 1)
            self.assertAlmostEqual(result['diff'], (m.CONDS.index(result['to_condition'])-m.CONDS.index(result['from_condition']))/3)

    def test_h5_ties_never_compare_strategy_to_itself(self):
        rows = [row(g,c,1) for g in m.MODELOS for c in m.CONDS]
        for result in m.h5(rows):
            self.assertNotEqual(result['mejor'], result['peor'])
            self.assertEqual(result['ventaja'], 0)
            self.assertEqual(result['n_cells'], 1)

    def test_formulation_pairs_same_strategy_before_macro(self):
        g = m.MODELOS[0]
        rows = [row(g, 'bm25', 0), row(g, 'dense', 2), row(g, 'bm25', 1, 'implicit')]
        result = next(x for x in m.h6_explicitud(rows) if x['generator_model']==g and x['criterion']=='faithfulness')
        self.assertEqual(result['diff_implicit_minus_explicit'], 1)
        self.assertEqual(result['n_cells'], 1)

    def test_generator_comparison_intersects_exact_cells_before_macro(self):
        a, b = m.MODELOS[:2]
        rows = [row(a, 'bm25', 0), row(a, 'dense', 2), row(b, 'bm25', 1)]
        result = next(x for x in m.h6_pendientes(rows) if x['criterion']=='faithfulness' and x['from_model']==a)
        self.assertEqual(result['diff'], 1)
        self.assertEqual(result['n_cells'], 1)
        self.assertEqual(result['n_base'], 1)


if __name__ == '__main__':
    unittest.main()
