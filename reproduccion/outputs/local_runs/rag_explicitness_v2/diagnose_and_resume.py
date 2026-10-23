"""One diagnostic call only; historical failure stays failed. Then resume seven units."""
import sys
import json
import urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
import run_rag_generation as rag
OUT = Path(__file__).resolve().parent
qid = 'q-v1-006__explicit'
run = ROOT / 'outputs/explicitness_v2/runs/explicitness_v2_rerank.jsonl'
chunks_path = ROOT / 'data/processed/chunks_v1.jsonl'
golden_path = OUT / 'golden_variants_14q.jsonl'
resolutions_path = ROOT / 'data/golden/answerability_resolutions_v1_22q.json'
chunks = {r['chunk_id']: r['text'] for r in rag.read_jsonl(chunks_path)}
golden = next(r for r in rag.read_jsonl(golden_path) if r['qid'] == qid)
selected = sorted([r for r in rag.read_jsonl(run) if r['qid'] == qid], key=lambda r:(r['rank'],r['chunk_id']))[:5]
ids = [r['chunk_id'] for r in selected]
contexts = [{'chunk_id': c, 'text': chunks[c]} for c in ids]
output = OUT / 'rag_rerank_top5_qwen35_9b_v2_14q.jsonl'
failure_path = output.with_name(output.stem + '_failures.jsonl')
if not failure_path.exists():
    failure = dict(experiment_id='rag_explicitness_v2_rerank_top5', retrieval_condition='rerank', qid=qid,
        status='failed', error='citation outside retrieved contexts', question=golden['question'],
        retrieved_chunk_ids=ids, retrieved_contexts=[chunks[c] for c in ids], generator_model='qwen3.5:9b',
        prompt_version='rag_answer_prompt_v1', top_k=5, provenance='historical_terminal_failure_import',
        generation_attempts=3, historical_batch_executions=2, historical_total_attempts=6,
        raw_generation_attempts=None, prompt_tokens=None, completion_tokens=None, generation_latency_ms=None,
        audit_note='Two historical terminal runs documented by logs and operator context. Raw attempts/usage were lost by old runner; no invented reconstruction. Qid inferred from six accepted prefix rows and frozen golden order.',
        source_logs={n:rag.sha256_file(OUT/n) for n in ['gen_rerank.log','gen_rerank_retry.log']})
    failure_path.write_text(json.dumps(failure,ensure_ascii=False)+'\n')
# Never use diagnostic replay as a replacement accepted answer.
diag_path = OUT / 'citation_diagnostic_single_attempt.json'
if not diag_path.exists():
    generator = rag.ollama_generator('qwen3.5:9b')
    messages = rag.build_messages(golden['question'], contexts)
    parsed, usage = generator(messages)
    try:
        rag.validate_generation_result(parsed, ids)
        error = None
    except ValueError as exc:
        error = str(exc)
    diag = dict(qid=qid, purpose='single diagnostic replay excluded from campaign acceptance; not retry-until-success',
        messages=messages, parsed=parsed, allowed_ids=ids, outside_ids=[c for c in parsed['citations'] if c not in ids],
        validation_error=error, usage=usage, seed=20260902, temperature=0, num_predict=300,
        model='qwen3.5:9b', original_raw_recovered=False)
    diag_path.write_text(json.dumps(diag,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(diag,ensure_ascii=False),flush=True)
metadata = rag.run_experiment(experiment_id='rag_explicitness_v2_rerank_top5', retrieval_condition='rerank',
    retrieval_run_path=run, chunks_path=chunks_path, golden_path=golden_path, resolutions_path=resolutions_path,
    output_path=output, top_k=5, generator=rag.ollama_generator('qwen3.5:9b'), generator_model='qwen3.5:9b',
    prompt_version='rag_answer_prompt_v1')
(OUT / 'rag_rerank_top5_qwen35_9b_v2_14q_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(json.dumps(metadata,indent=2),flush=True)
