"""Local RAGAS campaign; incremental scores, explicit partial availability."""
import asyncio
import hashlib
import itertools
import json
import math
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from evaluate_rag import run_evaluation, read_jsonl, METRIC_NAMES, ensure_usable_evaluation

async def main():
    for repeat in (1, 2):
        row = read_jsonl(OUT / f'smoke_{repeat}_scores.jsonl')[0]
        assert not row['evaluation_errors']
        assert row['faithfulness'] == row['factual_correctness'] == 1
    config = json.loads((OUT / 'evaluation_config.json').read_text())
    source = OUT / 'campaign_input_interleaved.jsonl'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == config['input_sha256']
    summary = await run_evaluation(input_paths=[source], output_path=OUT / 'scores.jsonl', summary_path=OUT / 'summary.json', risk_path=OUT / 'risk_queue.jsonl', judge_model='gemma3:4b')
    expected = read_jsonl(source)
    rows = read_jsonl(OUT / 'scores.jsonl')
    key = lambda x: (x['retrieval_condition'], x['qid'])
    assert len(rows) == 55 and len(set(map(key, rows))) == 55
    assert set(map(key, rows)) == set(map(key, expected))
    def valid(v):
        return isinstance(v, (int, float)) and math.isfinite(v)
    conditions = sorted({x['retrieval_condition'] for x in rows})
    lookup = {key(x): x for x in rows}
    comparisons = []
    for baseline, contender in itertools.combinations(conditions, 2):
        for metric in METRIC_NAMES:
            common = sorted({x['qid'] for x in rows if (baseline, x['qid']) in lookup and (contender, x['qid']) in lookup})
            scored = [q for q in common if valid(lookup[baseline, q].get(metric)) and valid(lookup[contender, q].get(metric))]
            deltas = [lookup[contender, q][metric] - lookup[baseline, q][metric] for q in scored]
            comparisons.append({'baseline': baseline, 'contender': contender, 'metric': metric, 'common_generated_n': len(common), 'paired_scored_n': len(deltas), 'wins': sum(d > 0 for d in deltas), 'ties': sum(d == 0 for d in deltas), 'losses': sum(d < 0 for d in deltas), 'mean_delta': statistics.fmean(deltas) if deltas else None, 'qids': scored})
    explicitness = []
    for condition in conditions:
        for metric in METRIC_NAMES:
            deltas = []
            for base in sorted({x['qid'].split('__')[0] for x in rows}):
                e, i = lookup.get((condition, base + '__explicit'), {}), lookup.get((condition, base + '__implicit'), {})
                if valid(e.get(metric)) and valid(i.get(metric)):
                    deltas.append({'base_qid': base, 'delta': i[metric] - e[metric]})
            explicitness.append({'condition': condition, 'metric': metric, 'n_base_pairs': len(deltas), 'mean_implicit_minus_explicit': statistics.fmean(x['delta'] for x in deltas) if deltas else None, 'pairs': deltas})
    errors = {condition: dict(Counter(e.split(':', 1)[0] for x in rows if x['retrieval_condition'] == condition for e in x['evaluation_errors'])) for condition in conditions}
    risk = read_jsonl(OUT / 'risk_queue.jsonl')
    risk_keys = set(map(key, risk))
    for row in rows:
        reasons = []
        if row['evaluation_errors']: reasons.append('evaluation_errors')
        if row['reported_behavior'] == 'abstain': reasons.append('generated_abstention_requires_audit')
        if row.get('generation_attempts', 1) != 1: reasons.append('generation_retry')
        if reasons and key(row) not in risk_keys:
            risk.append({**row, 'risk_reasons': reasons})
    (OUT / 'risk_queue_augmented.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in risk))
    audit = {'status': 'automatic_evaluation_executed_not_human_validation', 'accepted_evaluated': len(rows), 'generation_failed_not_scored': 1, 'expected_behavior_counts': dict(Counter(x['expected_behavior'] for x in rows)), 'reported_behavior_counts': dict(Counter(x['reported_behavior'] for x in rows)), 'metric_error_counts': errors, 'conditions': summary['conditions'], 'paired_condition_comparisons': comparisons, 'paired_explicitness': explicitness, 'risk_pairs': len(risk), 'limits': config['limitations']}
    (OUT / 'evaluation_audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    manifest = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file() and p.name != 'hash_manifest.json'}
    (OUT / 'hash_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(audit), flush=True)
    ensure_usable_evaluation(summary)

asyncio.run(main())
