"""Final-only offline analysis: common formulations before base-question macro."""
import importlib
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
MODELS = ('gemma4:e4b', 'qwen3.5:4b', 'qwen3.5:9b')
CONDS = ('bm25', 'dense', 'rrf', 'rerank')
CRIT = ('faithfulness', 'factual_correctness', 'behavior_ok', 'citations_ok')


def row(c, value, base='a', form='explicit', g=MODELS[0], behavior='answer'):
    return dict(qid=base+'__'+form, base_qid=base, generator_model=g,
                retrieval_condition=c, expected_behavior=behavior,
                **{cr: min(value, 1) if cr == 'citations_ok' else value for cr in CRIT})


class FinalExperimentTests(unittest.TestCase):
    def module(self):
        self.assertTrue((ROOT/'scripts/analyze_final_experiment.py').exists(),
                        'Missing final-only analysis implementation')
        return importlib.import_module('analyze_final_experiment')

    def test_four_strategy_support_precedes_macro_and_is_generator_specific(self):
        m = self.module()
        rows = [row(c, v, base, form) for base, form, v in
                [('a','explicit',0), ('a','implicit',2), ('b','explicit',2)] for c in CONDS]
        # This unmatched high-score formulation must not alter any strategy's mean.
        rows += [row(c, 2, 'c') for c in CONDS[:3]]
        # Another generator has its own support, not an across-model intersection.
        rows += [row(c, 0, 'different', g=MODELS[1]) for c in CONDS]
        result = m.analyze_quality(rows)
        levels = [r for r in result['levels'] if r['generator_model']==MODELS[0]
                  and r['criterion']=='faithfulness']
        self.assertEqual(len(levels), 4)
        for r in levels:
            self.assertEqual(r['mean'], 1.5)  # base a=1, base b=2, not micro=4/3
            self.assertEqual((r['n_cells'], r['n_base']), (3, 2))
            self.assertEqual(r['support'], ['a__explicit','a__implicit','b__explicit'])
        other = next(r for r in result['levels'] if r['generator_model']==MODELS[1]
                     and r['criterion']=='faithfulness')
        self.assertEqual(other['support'], ['different__explicit'])
        self.assertEqual(other['mean'], 0)

    def test_all_six_unselected_contrasts_use_same_four_way_support_and_base_signs(self):
        m = self.module()
        rows = []
        for base, form, a, b in [('a','explicit',1,0), ('a','implicit',0,1),
                                 ('b','explicit',0,2), ('c','explicit',2,1)]:
            rows += [row(c, b if c == 'dense' else a, base, form) for c in CONDS]
        rows += [row(c, 2 if c == 'dense' else 0, 'unmatched') for c in CONDS[:3]]
        result = m.analyze_quality(rows)
        self.assertIn('contrasts', result)
        self.assertEqual(len(result['contrasts']), 72)
        pairs = [r for r in result['contrasts'] if r['generator_model']==MODELS[0]
                 and r['criterion']=='faithfulness']
        self.assertEqual(len(pairs), 6)
        self.assertTrue(all((r['n_cells'],r['n_base']) == (4,3) for r in pairs))
        contrast = next(r for r in pairs if r['from_condition']=='bm25' and r['to_condition']=='dense')
        self.assertAlmostEqual(contrast['diff'], 1/3)
        self.assertEqual(contrast['base_differences'], {'a':0,'b':2,'c':-1})
        self.assertEqual((contrast['positive'],contrast['negative'],contrast['ties']), (1,1,1))
        self.assertEqual(len(contrast['cell_differences']), 4)
        self.assertEqual((contrast['diff'], contrast['ic95_lo'], contrast['ic95_hi']),
                         m.bootstrap_ci([0,2,-1]))
        self.assertEqual(contrast['interval_scope'], 'pointwise post-hoc descriptive; unadjusted')

    def test_content_scope_na_availability_and_exclusions_are_criterion_specific(self):
        m = self.module()
        rows = [row(c, 2, base, behavior=behavior) for base, behavior in
                [('answer','answer'), ('correct','grounded_correction'), ('abstain','abstain')]
                for c in CONDS]
        rows[0]['factual_correctness'] = 'na'
        rows += [row(c, 1, 'unmatched') for c in CONDS[:3]]
        result = m.analyze_quality(rows)
        self.assertIn('availability', result)
        levels = {r['criterion']:r for r in result['levels']
                  if r['generator_model']==MODELS[0] and r['retrieval_condition']=='bm25'}
        self.assertEqual(levels['faithfulness']['support'], ['answer__explicit','correct__explicit'])
        self.assertEqual(levels['factual_correctness']['support'], ['correct__explicit'])
        self.assertEqual(levels['behavior_ok']['n_cells'], 3)
        self.assertEqual(levels['citations_ok']['n_cells'], 3)
        avail = next(r for r in result['availability'] if r['generator_model']==MODELS[0]
                     and r['retrieval_condition']=='bm25' and r['criterion']=='factual_correctness')
        self.assertEqual((avail['n_accepted'],avail['n_in_scope'],avail['n_numeric'],
                          avail['n_unavailable'],avail['n_common'],avail['n_numeric_excluded']),
                         (4,3,2,1,1,1))
        self.assertEqual(avail['unavailable_qids'], ['answer__explicit'])
        self.assertEqual(avail['numeric_excluded_qids'], ['unmatched__explicit'])

    def test_operational_descriptives_separate_failures_and_never_double_count_attempts(self):
        m = self.module()
        accepted = dict(row('bm25',2), generation_latency_ms=3000, prompt_tokens=30,
                        completion_tokens=6, generation_attempts=2, raw_generation_attempts=['one','two'],
                        generation_source={'path':'accepted.jsonl','row':1})
        usage = [dict(generation_latency_ms=1000,prompt_tokens=10,completion_tokens=2),
                 dict(generation_latency_ms=2000,prompt_tokens=20,completion_tokens=4)]
        failed = dict(row('bm25',0,'failed'),generation_attempts=2,raw_generation_attempts=['one','two'],
                      attempt_usage=usage, generation_latency_ms=3000,prompt_tokens=30,completion_tokens=6,
                      error='bad contract',failure_source={'path':'failed.jsonl','row':1})
        result = m.analyze_operations([accepted], [failed])
        self.assertEqual(len(result['cells']),2)
        self.assertEqual(len(result['summary']),24)
        a = next(r for r in result['summary'] if r['generator_model']==MODELS[0]
                 and r['retrieval_condition']=='bm25' and r['status']=='accepted')
        f = next(r for r in result['summary'] if r['generator_model']==MODELS[0]
                 and r['retrieval_condition']=='bm25' and r['status']=='failed')
        for s in (a,f):
            self.assertEqual(s['n_cells'],1)
            self.assertEqual(s['latency_s_mean'],3)
            self.assertEqual(s['prompt_tokens_mean'],30)
            self.assertEqual(s['completion_tokens_mean'],6)
            self.assertEqual(s['n_attempts'],2)
        self.assertEqual(result['cells'][0]['usage_basis'],'recorded_cumulative')
        self.assertFalse(result['cells'][0]['attempt_usage_complete'])
        self.assertTrue(result['cells'][1]['attempt_usage_complete'])
        # Missing total can be recovered only from a complete attempt ledger.
        partial = dict(failed, generation_latency_ms=None, attempt_usage=usage[:1])
        p = m.analyze_operations([], [partial])['cells'][0]
        self.assertIsNone(p['latency_s'])
        self.assertFalse(p['attempt_usage_complete'])
        recovered = m.analyze_operations([], [dict(failed,generation_latency_ms=None)])['cells'][0]
        self.assertEqual(recovered['latency_s'],3)
        self.assertEqual(recovered['generation_latency_ms_basis'],'complete_attempt_sum')
        with self.assertRaisesRegex(ValueError, 'cumulative'):
            m.analyze_operations([], [dict(failed,prompt_tokens=99)])
        with self.assertRaisesRegex(ValueError, 'attempt count'):
            m.analyze_operations([dict(accepted,generation_attempts=3)], [])

    def test_invalid_scores_duplicate_cells_and_inconsistent_base_identity_fail_closed(self):
        import math
        m = self.module()
        good = row('bm25',2)
        for cr,v in [('citations_ok',2),('behavior_ok',True),('faithfulness',math.nan),
                     ('factual_correctness','missing')]:
            with self.subTest(cr=cr), self.assertRaises(ValueError):
                m.analyze_quality([dict(good,**{cr:v})])
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            m.analyze_quality([good,good])
        with self.assertRaisesRegex(ValueError, 'base identity'):
            m.analyze_quality([dict(good,base_qid='different')])
        with self.assertRaisesRegex(ValueError, 'behavior'):
            m.analyze_quality([good,dict(row('dense',2),expected_behavior='abstain')])

    def test_real_cli_emits_final_only_tables_and_repeats_byte_exactly(self):
        import csv
        import hashlib
        import json
        import subprocess
        import tempfile
        m = self.module()
        self.assertTrue(callable(getattr(m,'main',None)), 'Missing final-only artifact CLI')
        protected = {str(p):hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in m.RUN.rglob('*') if p.is_file()}
        protected[str(ROOT/'scripts/analysis_capacity_v3.py')] = hashlib.sha256(
            (ROOT/'scripts/analysis_capacity_v3.py').read_bytes()).hexdigest()
        parent = ROOT/'outputs/local_runs/final_experiment_20260930'
        parent.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=parent) as tmp:
            outputs = [Path(tmp)/name for name in ('one','two')]
            for output in outputs:
                process = subprocess.run([sys.executable,str(ROOT/'scripts/analyze_final_experiment.py'),
                                          '--output-dir',str(output)],capture_output=True,text=True)
                self.assertEqual(process.returncode,0,process.stderr)
            names = sorted(p.name for p in outputs[0].iterdir())
            self.assertIn('report.md',names)
            self.assertIn('results_proposed.md',names)
            self.assertEqual(names,sorted(p.name for p in outputs[1].iterdir()))
            for name in names:
                self.assertEqual((outputs[0]/name).read_bytes(),(outputs[1]/name).read_bytes(),name)
            data = json.loads((outputs[0]/'analysis.json').read_text())
            self.assertEqual(data['coverage_summary']['n_planned'],624)
            self.assertEqual(data['coverage_summary']['n_accepted'],604)
            self.assertEqual(data['coverage_summary']['n_failed'],20)
            self.assertEqual(data['coverage_summary']['unavailable_by_criterion'],
                             {'faithfulness':0,'factual_correctness':4,'behavior_ok':0,'citations_ok':0})
            self.assertEqual(len(data['quality']['levels']),48)
            self.assertEqual(len(data['quality']['contrasts']),72)
            self.assertEqual(len(data['operations']['cells']),624)
            self.assertEqual(data['bootstrap']['replicates'],5000)
            self.assertEqual(data['bootstrap']['seed'],20260928)
            self.assertNotIn('capacity',data)
            self.assertEqual(data['scopes']['faithfulness'],['answer','grounded_correction'])
            for file in ('main_table.csv','operational_table.csv'):
                table = list(csv.DictReader((outputs[0]/file).open()))
                self.assertEqual(len(table),12)
                self.assertEqual([(r['model'],r['retrieval_condition']) for r in table],
                                 [(label,c) for label in ('Gemma','Qwen4','Qwen9') for c in CONDS])
            proposed = (outputs[0]/'results_proposed.md').read_text()
            self.assertIn('{#tbl-final-recuperadores}',proposed)
            self.assertIn('{#tbl-final-operacion}',proposed)
            for anchor,n_fields in [('tbl-final-recuperadores',8),('tbl-final-operacion',5)]:
                before = proposed.split('{#'+anchor+'}')[0].splitlines()
                body = []
                for line in reversed(before):
                    if line.startswith('| '):
                        body.append(line)
                    elif body:
                        break
                numeric = 0
                for line in body[:12]:
                    import re
                    # Labels/methods never contribute tokens (including bm25/Qwen4).
                    numeric += len(re.findall(r'(?<![A-Za-z0-9])\d+(?:[.,]\d+)?(?![A-Za-z0-9])',
                                              '|'.join(line.split('|')[3:-1])))
                self.assertEqual(numeric,12*n_fields)
            manifest = json.loads((outputs[0]/'hash_manifest.json').read_text())
            self.assertTrue(all('generation_scaling_v3' in path or path.startswith('scripts/')
                                for path in manifest['sources']))
            for name,digest in manifest['outputs'].items():
                self.assertEqual(hashlib.sha256((outputs[0]/name).read_bytes()).hexdigest(),digest)
        for path,digest in protected.items():
            self.assertEqual(hashlib.sha256(Path(path).read_bytes()).hexdigest(),digest,path)

    def test_cli_rejects_existing_outside_and_symlink_escape_without_writes(self):
        import subprocess
        import tempfile
        m = self.module()
        parent = ROOT/'outputs/local_runs/final_experiment_20260930'
        parent.mkdir(parents=True,exist_ok=True)
        command = [sys.executable,str(ROOT/'scripts/analyze_final_experiment.py')]
        with tempfile.TemporaryDirectory(dir=parent) as tmp:
            sentinel = Path(tmp)/'untouched'
            sentinel.write_bytes(b'protected')
            existing = subprocess.run(command+['--output-dir',tmp],capture_output=True,text=True)
            self.assertNotEqual(existing.returncode,0)
            self.assertIn('exists',existing.stderr)
            self.assertEqual(sentinel.read_bytes(),b'protected')
            escaped = Path(tmp)/'escape'
            escaped.symlink_to(ROOT/'docs',target_is_directory=True)
            outside_target = escaped/'forbidden_final_analysis'
            outside = subprocess.run(command+['--output-dir',str(outside_target)],capture_output=True,text=True)
            self.assertNotEqual(outside.returncode,0)
            self.assertFalse(outside_target.exists())
        missing = subprocess.run(command,capture_output=True,text=True)
        self.assertNotEqual(missing.returncode,0)
        self.assertIn('--output-dir',missing.stderr)
        historical = subprocess.run(command+['--output-dir',str(m.RUN/'forbidden_final_analysis')],capture_output=True,text=True)
        self.assertNotEqual(historical.returncode,0)
        self.assertFalse((m.RUN/'forbidden_final_analysis').exists())

    def test_real_scores_recompute_every_level_with_independent_stdlib_oracle(self):
        from statistics import mean
        from collections import defaultdict
        m = self.module()
        scores, failures, _ = m.cargar()
        data = m.analyze_quality(scores)
        self.assertEqual(data,m.analyze_quality(list(reversed(scores))))
        for level in data['levels']:
            g,c,cr = level['generator_model'],level['retrieval_condition'],level['criterion']
            by_condition = {}
            for condition in CONDS:
                by_condition[condition] = {r['qid']:r for r in scores
                    if r['generator_model']==g and r['retrieval_condition']==condition
                    and type(r[cr]) in (int,float)
                    and (cr in ('behavior_ok','citations_ok') or r['expected_behavior'] in ('answer','grounded_correction'))}
            shared = set.intersection(*(set(d) for d in by_condition.values()))
            bases = defaultdict(list)
            for qid in sorted(shared):
                r = by_condition[c][qid]
                bases[r['base_qid']].append(r[cr])
            expected = mean(mean(v) for v in bases.values())
            self.assertEqual(level['mean'],expected)
            self.assertEqual((level['n_cells'],level['n_base']),(len(shared),len(bases)))
        self.assertEqual((len(scores),len(failures)),(604,20))


if __name__ == '__main__':
    unittest.main()
