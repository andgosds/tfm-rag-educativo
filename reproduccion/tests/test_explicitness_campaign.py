import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

class CampaignTests(unittest.TestCase):
    def test_formulations_preserve_text_without_inheriting_adjudication(self):
        spec = importlib.util.find_spec('explicitness_campaign')
        self.assertIsNotNone(spec, 'retrieval-only adapter is missing')
        from explicitness_campaign import formulations
        pair = dict(pair_id='p', base_qid='q', explicit_question='Explicit?', implicit_question='Implicit?', ready_for_candidate_retrieval=True)
        rows = formulations([pair])
        self.assertEqual([r['question'] for r in rows], ['Explicit?', 'Implicit?'])
        self.assertEqual({r['qid'] for r in rows}, {'q__explicit', 'q__implicit'})
        self.assertTrue(all(r['annotation_status'] == 'pending_evidence_review' for r in rows))
        self.assertTrue(all(r['base_qid'] == 'q' for r in rows))

    def test_pool_separates_seen_unjudged_zero_and_pending_reuse(self):
        import explicitness_campaign as c
        self.assertTrue(hasattr(c, 'build_pool'), 'pool builder missing')
        queries = c.formulations([dict(pair_id='p', base_qid='q', explicit_question='E', implicit_question='I', ready_for_candidate_retrieval=True)])
        runs = {'bm25': [dict(qid=q['qid'], chunk_id=cid, rank=i+1, score=1.0) for q in queries for i,cid in enumerate(['seen','zero','new','positive'])]}
        prior = {('q','seen'), ('q','zero'), ('q','positive')}
        decisions = {('q','zero'): [{'grade':0,'source':'human'}], ('q','positive'): [{'grade':2,'source':'original'}]}
        chunks = {cid: {'retrieval_text':cid} for cid in ['seen','zero','new','positive']}
        pool, blind, reuse = c.build_pool(queries, runs, prior, decisions, chunks)
        self.assertEqual(len(pool),8)
        self.assertEqual(len(blind),4)
        self.assertEqual(len(reuse),4)
        self.assertEqual({r['chunk_id'] for r in blind}, {'seen','new'})
        self.assertTrue(all(r['human_decision'] is None and r['reviews'] == [] for r in blind))
        self.assertTrue(all('provenance' not in r and 'historical_decisions' not in r for r in blind))
        self.assertTrue(all(r['reuse_status']=='pending_equivalence_confirmation' for r in reuse))
        self.assertEqual(sum(not r['previously_seen'] for r in pool),2)

    def test_runner_rejects_outputs_outside_v2_before_execution(self):
        import explicitness_campaign as c
        self.assertTrue(hasattr(c, 'execute'), 'execution adapter missing')
        with self.assertRaises(ValueError):
            c.execute(ROOT.parent / 'v1/outputs/forbidden')
        with self.assertRaises(ValueError):
            c.execute(ROOT / '../outputs/forbidden')

if __name__ == '__main__':
    unittest.main()
