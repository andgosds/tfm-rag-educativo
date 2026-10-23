"""Read-only acceptance tests for the frozen, actually executed campaign."""
import hashlib
import json
import math
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'outputs/explicitness_v2'
sys.dont_write_bytecode = True
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(ROOT/'scripts'))
def rows(path):
    return [json.loads(s) for s in path.read_text().splitlines()]

class Artifacts(unittest.TestCase):
    def test_exact_keys_ranks_scores_and_provenance(self):
        from run_hybrid_rrf import reciprocal_rank_fusion
        qs=rows(OUT/'formulations.jsonl')
        runs={m:rows(OUT/f'runs/explicitness_v2_{m}.jsonl') for m in ['bm25','dense','rrf','rerank']}
        common={'qid','base_qid','pair_id','explicitness','question','annotation_status','run_id','method','chunk_id','rank','score','stage_latency_ms'}
        for m,rs in runs.items():
            self.assertEqual(len(rs),140)
            self.assertEqual({r['qid'] for r in rs},{q['qid'] for q in qs})
            expected=common | ({'bm25_rank','dense_rank'} if m in ('rrf','rerank') else set()) | ({'source_rank','source_score'} if m=='rerank' else set())
            for r in rs:
                self.assertEqual(set(r),expected)
                self.assertTrue(math.isfinite(r['score']))
                self.assertEqual(r['annotation_status'],'pending_evidence_review')
            for q in qs:
                ranked=[r for r in rs if r['qid']==q['qid']]
                self.assertEqual([r['rank'] for r in ranked],list(range(1,11)))
                self.assertEqual(len({r['chunk_id'] for r in ranked}),10)
                self.assertEqual(ranked,sorted(ranked,key=lambda r:(-r['score'],r['chunk_id'])))
                self.assertTrue(all(r['question']==q['question'] for r in ranked))
        for q in qs:
            grouped={m:[r for r in rs if r['qid']==q['qid']] for m,rs in runs.items()}
            fused=reciprocal_rank_fusion([[r['chunk_id'] for r in grouped[m]] for m in ['bm25','dense']],k0=60,top_k=10)
            self.assertEqual(fused,[(r['chunk_id'],r['score']) for r in grouped['rrf']])
            self.assertEqual({r['chunk_id'] for r in grouped['rrf']},{r['chunk_id'] for r in grouped['rerank']})
            source={r['chunk_id']:r for r in grouped['rrf']}
            for r in grouped['rerank']:
                self.assertEqual((r['source_rank'],r['source_score']),(source[r['chunk_id']]['rank'],source[r['chunk_id']]['score']))

    def test_pool_partition_blinding_and_historical_preservation(self):
        tech=rows(OUT/'pools/technical_pool.jsonl')
        blind=rows(OUT/'pools/blind_review_queue.jsonl')
        reuse=rows(OUT/'pools/pending_judgment_reuse.jsonl')
        key=lambda r:(r['qid'],r['chunk_id'])
        self.assertEqual({key(r) for r in tech},{key(r) for r in blind}|{key(r) for r in reuse})
        self.assertFalse({key(r) for r in blind}&{key(r) for r in reuse})
        all_runs=[r for p in (OUT/'runs').glob('*.jsonl') for r in rows(p)]
        self.assertEqual({key(r) for r in tech},{key(r) for r in all_runs})
        prior={(r['qid'],r['chunk_id']) for r in rows(ROOT/'data/golden/pool_bm25_dense_v1_22q.jsonl')}
        for r in tech:
            self.assertEqual(r['previously_seen'],(r['base_qid'],r['chunk_id']) in prior)
            self.assertIsNone(r['current_grade'])
        for r in blind:
            self.assertEqual(set(r),{'pool_id','qid','base_qid','explicitness','question','chunk_id','retrieval_text','reviews','human_decision','annotation_status'})
            self.assertEqual(r['reviews'],[])
            self.assertIsNone(r['human_decision'])
        for r in reuse:
            self.assertIsNone(r['human_decision'])
            self.assertEqual(r['reuse_status'],'pending_equivalence_confirmation')
        # protected_v1_before.json is a historical observation, not a live dependency.
        for manifest,base in [('artifact_sha256.json',OUT)]:
            for p,h in json.loads((OUT/manifest).read_text()).items():
                self.assertEqual(hashlib.sha256((base/p).read_bytes()).hexdigest(),h,p)

    def test_real_second_execution_reproduces_scores_and_pools(self):
        other=ROOT/'outputs/explicitness_v2_reproduction'
        for p in (OUT/'runs').glob('*.jsonl'):
            strip=lambda rs:[{k:v for k,v in r.items() if k!='stage_latency_ms'} for r in rs]
            self.assertEqual(strip(rows(p)),strip(rows(other/'runs'/p.name)))
        for p in (OUT/'pools').glob('*.jsonl'):
            self.assertEqual(p.read_bytes(),(other/'pools'/p.name).read_bytes())
        self.assertEqual((OUT/'embeddings/documents.npy').read_bytes(),(other/'embeddings/documents.npy').read_bytes())

if __name__=='__main__':
    unittest.main()
