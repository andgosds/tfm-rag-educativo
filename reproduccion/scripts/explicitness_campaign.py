"""Retrieval-only adapter: local inherited ranking kernels, no evaluation runners."""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


def formulations(pairs):
    """Desdobla cada pareja lista en sus formulaciones explícita e implícita."""
    rows = []
    for pair in pairs:
        if not pair['ready_for_candidate_retrieval']:
            raise ValueError('pair not ready for candidate retrieval')
        for kind in ('explicit', 'implicit'):
            rows.append(dict(qid=pair['base_qid'] + '__' + kind,
                             base_qid=pair['base_qid'], pair_id=pair['pair_id'],
                             explicitness=kind, question=pair[kind + '_question'],
                             annotation_status='pending_evidence_review'))
    if len({r['qid'] for r in rows}) != len(rows):
        raise ValueError('duplicate formulation qid')
    return rows


def build_pool(queries, runs, prior, decisions, chunks):
    """Une candidatos y separa la revisión ciega de la reutilización pendiente de juicios."""
    by_qid = {q['qid']: q for q in queries}
    union = {}
    for method, rows in runs.items():
        for row in rows:
            key = (row['qid'], row['chunk_id'])
            union.setdefault(key, []).append(dict(method=method, rank=row['rank'], score=row['score']))
    technical, blind, reuse = [], [], []
    # Un juicio histórico exige confirmar equivalencia antes de reutilizarlo.
    for (qid, cid), provenance in sorted(union.items()):
        q = by_qid[qid]
        base_key = (q['base_qid'], cid)
        historical = decisions.get(base_key, [])
        unit = dict(pool_id=qid+'::'+cid, qid=qid, base_qid=q['base_qid'],
                    explicitness=q['explicitness'], question=q['question'], chunk_id=cid)
        technical.append(dict(**unit, provenance=provenance, previously_seen=base_key in prior,
                              historical_decisions=historical, historically_adjudicated=bool(historical),
                              current_grade=None, current_status='pending_equivalence_confirmation' if historical else 'unjudged'))
        if historical:
            reuse.append(dict(**unit, historical_decisions=historical,
                              reuse_status='pending_equivalence_confirmation', human_decision=None))
        else:
            blind.append(dict(**unit, retrieval_text=chunks[cid]['retrieval_text'],
                              reviews=[], human_decision=None, annotation_status='pending'))
    return technical, blind, reuse


def execute(output):
    """Ejecuta la recuperación v2 y guarda rankings, colas y comprobaciones de integridad."""
    import json, hashlib, os, time, platform
    from collections import Counter
    output = Path(output).resolve()
    if not output.is_relative_to(ROOT):
        raise ValueError('outputs must be inside v2')
    if output.exists():
        raise FileExistsError('refusing to overwrite campaign; select a fresh v2 output directory')
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['TRANSFORMERS_OFFLINE'] = '1'
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    def load(path):
        """Carga un archivo JSONL relativo a la raíz de reproducción."""
        return [json.loads(s) for s in (ROOT/path).read_text().splitlines() if s.strip()]
    def sha(path):
        """Calcula la huella SHA-256 de una entrada o un artefacto."""
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    def write(name, obj):
        """Guarda un objeto JSON dentro del directorio de la campaña."""
        p = output/name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')
    def jsonl(name, rows):
        """Guarda los registros de la campaña en formato JSONL."""
        p = output/name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in rows))
    protected = {str(p.relative_to(ROOT)): sha(p) for p in (ROOT/'data').rglob('*')
                 if p.is_file() and not any(x in p.parts for x in ('.venv','__pycache__','.pytest_cache'))}
    paths = dict(pairs='data/golden/variants/explicitness_pairs_v1_consolidated.jsonl',
                 chunks='data/processed/chunks_v1.jsonl',
                 prior='data/golden/pool_bm25_dense_v1_22q.jsonl',
                 golden='data/golden/golden_set_pilot_v1.jsonl',
                 human='data/golden/pool_human_priority_three_judge_v1_22q.jsonl')
    registered = json.loads((ROOT/'config/inputs_v2.json').read_text())
    for p, expected in registered['shared_inputs'].items():
        if sha(ROOT/p) != expected:
            raise ValueError('registered historical hash mismatch: '+p)
    queries = formulations(load(paths['pairs']))
    assert len(queries)==14 and len({q['base_qid'] for q in queries})==7
    chunks = load(paths['chunks'])
    ids = [c['chunk_id'] for c in chunks]
    assert len(ids)==len(set(ids))
    chunkmap = {c['chunk_id']:c for c in chunks}
    config = dict(campaign='explicitness_v2', mode='retrieval_only', paths=paths,
                  input_sha256={p:sha(ROOT/p) for p in paths.values()},
                  top_k=10, fusion_depth=10, k0=60, bm25_k1=1.5, bm25_b=.75,
                  dense_model='intfloat/e5-base-v2', dense_revision='f52bf8ec8c7124536f0efb74aca902b2995e5bcd',
                  reranker_model='cross-encoder/ms-marco-MiniLM-L6-v2', reranker_revision='233902d25c440f23af6f7d6e94d2946bac0bee0a',
                  device='cuda', batch_size=16, max_seq_length=512, dtype='float32',
                  document_prefix='passage: ', query_prefix='query: ', normalize_embeddings=True,
                  search='exact_numpy_dot_product', indexed_field='retrieval_text',
                  tie_break='score_descending_then_chunk_id_ascending', seed=0,
                  generation=False, paid_api_calls=False, metrics=False, final_qrels_ready=False,
                  historical_reuse='pending_equivalence_confirmation_for_every_formulation',
                  model_access='local_files_only_offline',
                  command='PYTHONDONTWRITEBYTECODE=1 uv run --project environments/dense --no-sync python scripts/explicitness_campaign.py --output '+str(output.relative_to(ROOT)),
                  implementation_sha256={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__), *(ROOT/'scripts'/n for n in ('run_bm25.py','run_dense.py','run_hybrid_rrf.py','run_reranker.py'))]},
                  environment_sha256={str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'environments/dense').glob('*') if p.is_file()})
    write('configuration.json',config)
    write('protected_v1_before.json',protected)
    jsonl('formulations.jsonl',queries)
    import numpy as np
    import torch, sentence_transformers
    from sentence_transformers import SentenceTransformer, CrossEncoder
    from run_bm25 import BM25Index
    from run_dense import _encode, rank_embeddings, _count_truncated_inputs
    from run_hybrid_rrf import reciprocal_rank_fusion
    from run_reranker import rerank_candidates
    if not torch.cuda.is_available():
        raise RuntimeError('Frozen CUDA device unavailable; no silent device change')
    torch.manual_seed(0)
    np.random.seed(0)
    def sync():
        """Espera a que terminen las operaciones CUDA antes de medir tiempos."""
        torch.cuda.synchronize()
    def timed(fn):
        """Mide una etapa con sincronización CUDA y devuelve resultado y milisegundos."""
        sync(); start=time.perf_counter(); result=fn(); sync()
        return result,(time.perf_counter()-start)*1000
    metadata = dict(python=platform.python_version(), numpy=np.__version__, torch=torch.__version__,
                    sentence_transformers=sentence_transformers.__version__, gpu=torch.cuda.get_device_name(),
                    timing='single-pass synchronized stages; not warmed repeated operational benchmark')
    bm25, metadata['bm25_build_ms'] = timed(lambda: BM25Index({c['chunk_id']:c['retrieval_text'] for c in chunks},k1=1.5,b=.75))
    dense, metadata['dense_model_load_ms'] = timed(lambda: SentenceTransformer(config['dense_model'],revision=config['dense_revision'],device='cuda',trust_remote_code=False,local_files_only=True))
    dense.max_seq_length=512
    passages=['passage: '+c['retrieval_text'] for c in chunks]
    query_texts=['query: '+q['question'] for q in queries]
    for kind,texts in [('passage',passages),('query',query_texts)]:
        metadata['truncated_'+kind+'_count']=_count_truncated_inputs(dense.tokenizer,texts,max_seq_length=512,batch_size=16)
    embeddings, metadata['corpus_encode_ms']=timed(lambda: _encode(dense,passages,batch_size=16))
    metadata['embedding_dimension']=embeddings.shape[1]
    metadata['dense_parameter_dtype']=str(next(dense.parameters()).dtype)
    (output/'embeddings').mkdir()
    np.save(output/'embeddings/documents.npy',embeddings)
    write('embeddings/document_ids.json',ids)
    cross, metadata['reranker_model_load_ms']=timed(lambda: CrossEncoder(config['reranker_model'],revision=config['reranker_revision'],device='cuda',max_length=512,local_files_only=True))
    metadata['reranker_parameter_dtype']=str(next(cross.model.parameters()).dtype)
    runs={m:[] for m in ('bm25','dense','rrf','rerank')}
    diagnostics=[]
    for q in queries:
        sparse, sparse_ms=timed(lambda: bm25.rank(q['question'],top_k=10))
        def dense_search():
            """Codifica la formulación actual y recupera sus diez fragmentos más cercanos."""
            vector=_encode(dense,['query: '+q['question']],batch_size=16)[0]
            return rank_embeddings(vector,embeddings,ids,top_k=10)
        dr,dense_ms=timed(dense_search)
        fused,fusion_ms=timed(lambda: reciprocal_rank_fusion([[x[0] for x in sparse],[x[0] for x in dr]],k0=60,top_k=10))
        candidates=[chunkmap[cid] for cid,_ in fused]
        lengths=[len(cross.tokenizer(q['question'],c['retrieval_text'],truncation=False)['input_ids']) for c in candidates]
        reranked,rerank_ms=timed(lambda: rerank_candidates(q['question'],candidates,score_pairs=lambda pairs:cross.predict(pairs,batch_size=16,show_progress_bar=False,convert_to_numpy=True)))
        assert {x[0] for x in fused}=={x[0] for x in reranked}
        ranks={m:{cid:i for i,(cid,_) in enumerate(r,1)} for m,r in [('bm25',sparse),('dense',dr),('rrf',fused)]}
        for method,ranking,latency in [('bm25',sparse,sparse_ms),('dense',dr,dense_ms),('rrf',fused,fusion_ms),('rerank',reranked,rerank_ms)]:
            for rank,(cid,score) in enumerate(ranking,1):
                row=dict(**q,run_id='explicitness_v2_'+method,method=method,chunk_id=cid,rank=rank,score=float(score),stage_latency_ms=latency)
                if method in ('rrf','rerank'):
                    row.update(bm25_rank=ranks['bm25'].get(cid),dense_rank=ranks['dense'].get(cid))
                if method=='rerank':
                    row.update(source_rank=ranks['rrf'][cid],source_score=dict(fused)[cid])
                runs[method].append(row)
        diagnostics.append(dict(qid=q['qid'],bm25_ms=sparse_ms,dense_ms=dense_ms,fusion_ms=fusion_ms,rerank_ms=rerank_ms,
                                reranker_pair_tokens=lengths,truncated_pair_count=sum(n>512 for n in lengths),
                                serial_rrf_stage_sum_ms=sparse_ms+dense_ms+fusion_ms,
                                serial_rerank_stage_sum_ms=sparse_ms+dense_ms+fusion_ms+rerank_ms))
        for method,rows in runs.items():
            jsonl('runs/explicitness_v2_'+method+'.jsonl',rows)
    metadata['truncated_pair_count']=sum(d['truncated_pair_count'] for d in diagnostics)
    metadata['reranker_pair_count']=sum(len(d['reranker_pair_tokens']) for d in diagnostics)
    write('execution_metadata.json',metadata)
    jsonl('query_diagnostics.jsonl',diagnostics)
    prior={(r['qid'],r['chunk_id']) for r in load(paths['prior'])}
    decisions={}
    for r in load(paths['golden']):
        if r['annotation_status']=='adjudicated':
            for e in r['evidence']:
                decisions.setdefault((r['qid'],e['chunk_id']),[]).append(dict(grade=e['relevance_grade'],source=paths['golden'],human_adjudication=r['human_adjudication'],canonical=e['is_canonical']))
    for r in load(paths['human']):
        if r.get('human_status')=='adjudicated' and r.get('human_grade') in (0,1,2):
            decisions.setdefault((r['qid'],r['chunk_id']),[]).append(dict(grade=r['human_grade'],source=paths['human'],pool_id=r['pool_id'],reviewer=r.get('human_reviewer_id'),adjudication_mode=r.get('adjudication_mode'),reviewed_at=r.get('human_reviewed_at')))
    pool,blind,reuse=build_pool(queries,runs,prior,decisions,chunkmap)
    jsonl('pools/technical_pool.jsonl',pool)
    jsonl('pools/blind_review_queue.jsonl',blind)
    jsonl('pools/pending_judgment_reuse.jsonl',reuse)
    base={(r['base_qid'],r['chunk_id']) for r in pool}
    report=dict(base_questions=len({q['base_qid'] for q in queries}),formulations=len(queries),chunks=len(chunks),
                rankings={m:len(r) for m,r in runs.items()},technical_formulation_chunk_pairs=len(pool),base_chunk_union=len(base),
                historical_technical_pool_pairs=len(prior),new_base_chunk_pairs=len(base-prior),seen_base_chunk_pairs=len(base&prior),
                new_formulation_chunk_pairs=sum(not r['previously_seen'] for r in pool),
                seen_formulation_chunk_pairs=sum(r['previously_seen'] for r in pool),
                blind_review_units=len(blind),pending_reuse_units=len(reuse),
                unjudged_seen_review_units=sum(r['previously_seen'] and not r['historically_adjudicated'] for r in pool),
                historical_grade_zero_reuse_units=sum(any(d['grade']==0 for d in r['historical_decisions']) for r in reuse),
                historical_decision_modes=dict(Counter(d.get('adjudication_mode') or 'original_or_direct_human' for r in reuse for d in r['historical_decisions'])),
                final_qrels_ready=False,quality_metrics_computed=False,generation_executed=False,
                candidate_set_equality=True)
    for method,rows in runs.items():
        assert {r['qid'] for r in rows}=={q['qid'] for q in queries}
        for q in queries:
            subset=[r for r in rows if r['qid']==q['qid']]
            assert [r['rank'] for r in subset]==list(range(1,11))
            assert len({r['chunk_id'] for r in subset})==10
            assert all(np.isfinite(r['score']) and r['chunk_id'] in chunkmap for r in subset)
    assert len(blind)+len(reuse)==len(pool)
    assert all(r['human_decision'] is None and r['reviews']==[] for r in blind)
    changed=[p for p,h in protected.items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
    report.update(protected_v1_files=len(protected),changed_v1_files=changed,verified=not changed)
    write('verification.json',report)
    assert not changed, changed
    write('artifact_sha256.json',{str(p.relative_to(output)):sha(p) for p in output.rglob('*') if p.is_file()})
    print(json.dumps(report,indent=2))
    return report


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True,help='fresh directory within v2; existing directories refused')
    execute(parser.parse_args().output)
