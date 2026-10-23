"""Offline integrity/resume verification; local backend metadata only, no inference."""
import json
import sys
import hashlib
import urllib.request
from pathlib import Path
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
import run_rag_generation as rag

def digest(data):
    return hashlib.sha256(data).hexdigest()

golden_path = OUT / 'golden_variants_14q.jsonl'
chunks_path = ROOT / 'data/processed/chunks_v1.jsonl'
res_path = ROOT / 'data/golden/answerability_resolutions_v1_22q.json'
golden = {r['qid']: r for r in rag.read_jsonl(golden_path)}
chunks = {r['chunk_id']: r['text'] for r in rag.read_jsonl(chunks_path)}
baseline = json.loads((OUT / 'resume_baseline_manifest.json').read_text())
preserved = {}
for relative, info in baseline.items():
    path = ROOT.parent / relative
    data = path.read_bytes()
    prefix = data[:info['size']]
    assert digest(prefix) == info['sha256'], path
    if 'rag_rerank_top5' not in path.name:
        assert len(data) == info['size'], path
    preserved[path.name] = {'original_bytes': info['size'], 'prefix_sha256': digest(prefix), 'byte_identical': len(data) == info['size']}

def forbid_generation(messages):
    raise AssertionError('Resume must not call inference for accepted or failed units')

counts = {}
coverage = []
input_paths = [golden_path, chunks_path, res_path]
for condition in ('bm25', 'dense', 'rrf', 'rerank'):
    output = OUT / f'rag_{condition}_top5_qwen35_9b_v2_14q.jsonl'
    failures_path = output.with_name(output.stem + '_failures.jsonl')
    run_path = ROOT / f'outputs/explicitness_v2/runs/explicitness_v2_{condition}.jsonl'
    input_paths.append(run_path)
    rankings = rag.read_jsonl(run_path)
    accepted = rag.read_jsonl(output)
    failed = rag.read_jsonl(failures_path) if failures_path.exists() else []
    assert len({r['qid'] for r in accepted + failed}) == len(accepted + failed) == len(golden)
    assert {r['qid'] for r in accepted + failed} == set(golden)
    for row in accepted + failed:
        qid = row['qid']
        expected = sorted([r for r in rankings if r['qid'] == qid], key=lambda r:(r['rank'],r['chunk_id']))[:5]
        ids = [r['chunk_id'] for r in expected]
        assert row['retrieved_chunk_ids'] == ids
        assert row['retrieved_contexts'] == [chunks[c] for c in ids]
        assert row['question'] == golden[qid]['question']
        assert row['generator_model'] == 'qwen3.5:9b'
        assert row['prompt_version'] == 'rag_answer_prompt_v1'
        assert row['top_k'] == 5
        assert row['retrieval_condition'] == condition
        assert row['experiment_id'] == f'rag_explicitness_v2_{condition}_top5'
        if row in accepted:
            parsed = rag.parse_text_contract(row['raw_generation_text'])
            rag.validate_generation_result(parsed, ids)
            assert parsed['answer'] == row['response']
            assert parsed['citations'] == row['citations']
            assert parsed['behavior'] == row['reported_behavior']
        coverage.append({'condition':condition,'qid':qid,'status':'accepted' if row in accepted else 'failed'})
    metadata = json.loads(output.with_name(output.stem + '_metadata.json').read_text())
    for key, path in [('retrieval_run',run_path),('chunks',chunks_path),('golden',golden_path),('resolutions',res_path)]:
        assert metadata['input_sha256'][key] == rag.sha256_file(path)
    before = rag.sha256_file(output)
    failure_before = rag.sha256_file(failures_path) if failures_path.exists() else None
    resumed = rag.run_experiment(experiment_id=f'rag_explicitness_v2_{condition}_top5', retrieval_condition=condition,
        retrieval_run_path=run_path, chunks_path=chunks_path, golden_path=golden_path, resolutions_path=res_path,
        output_path=output, top_k=5, generator=forbid_generation, generator_model='qwen3.5:9b', prompt_version='rag_answer_prompt_v1')
    assert resumed['rows_written'] == 0
    assert rag.sha256_file(output) == before
    assert (rag.sha256_file(failures_path) if failures_path.exists() else None) == failure_before
    counts[condition] = {'accepted':len(accepted),'failed':len(failed),'total':len(accepted)+len(failed),'resume_inference_calls':0}

diag = json.loads((OUT / 'citation_diagnostic_single_attempt.json').read_text())
assert diag['validation_error'] == 'citation outside retrieved contexts'
assert diag['outside_ids'] == ['[openstax_principles_ds:4.1:chunk-010]']
assert 'openstax_principles_ds:4.1:chunk-010' in diag['allowed_ids']
# Exact-token violation: bracket decoration, not evidence of an invented underlying chunk.
tests = (OUT / 'test_suite.log').read_text()
assert '155 passed' in tests and 'failed' not in tests
local_backend = {}
for name, endpoint in [('version','version'),('models','tags')]:
    with urllib.request.urlopen('http://127.0.0.1:11434/api/' + endpoint) as response:
        local_backend[name] = json.load(response)
local_backend['models'] = [m for m in local_backend['models']['models'] if m['name'] == 'qwen3.5:9b']
paths = sorted(set(input_paths + [p for p in OUT.iterdir() if p.is_file() and p.name not in ('completion_audit.json','completion_audit.md')] + [ROOT/'scripts/run_rag_generation.py', ROOT/'tests/test_run_rag_generation.py']))
report = {
    'verified_at_utc':datetime.now(timezone.utc).isoformat(), 'scope':'generation only; not completed RAG evaluation',
    'counts':counts,'accepted_total':sum(v['accepted'] for v in counts.values()),'failed_total':sum(v['failed'] for v in counts.values()),
    'coverage_total':len(coverage),'coverage':coverage,'preservation':preserved,
    'checks':{'exact_unique_56_units':len(coverage)==56,'context_text_and_top5_order':True,'accepted_exact_citations_and_raw_parse':True,
        'metadata_input_hashes':True,'resume_no_inference_all_conditions':True,'existing_accepted_bytes_preserved':True},
    'diagnosis':{'historical_failed_qid':'q-v1-006__explicit','historical_failed_batches':2,'attempts_per_historical_batch':3,
        'historical_raw_usage_latency':'unavailable; lost by old runner; not reconstructed',
        'diagnostic_calls':1,'diagnostic_campaign_acceptance':False,'diagnostic_usage':diag['usage'],
        'observed_cause':'Model emits brackets around one otherwise supplied chunk ID; strict validator correctly rejects the non-exact token. No stripping/remapping applied.',
        'historical_causality_limit':'Single replay reproduces same validation error; original six raw attempts are unavailable, so their exact token defects cannot be asserted.'},
    'contract':{'model':'qwen3.5:9b','prompt':'rag_answer_prompt_v1','temperature':0,'seed':20260902,'top_k':5,'num_predict':300,'max_attempts':3},
    'local_backend_at_verification':local_backend,
    'tests':{'command':'.venv/bin/python -m pytest v2/tests -q','exit_code':0,'result':tests.strip(),'tdd':'Four red-green checks observed: terminal usage, continuation/resume, malformed output retention, wrong-condition resume guard.'},
    'limits':['No judges or paid APIs called; generation acceptance does not establish correctness or faithfulness.',
        'Historical failed usage/latency are unknown: no complete campaign cost/latency aggregate is defensible.',
        'Sequential and resumed execution batches, plus residual backend nondeterminism, remain validity threats.',
        'Backend digest was captured now, not pinned/recorded at the original three completed conditions.',
        'Historical reviewer attribution requires a separate audit: blind assistant decisions were labelled andres; claimed gpt5.6/glm5.3 subagent reviews lack verified model selection. Source adjudications not altered here.',
        'v1 already had unrelated working-tree changes at task entry; this task did not modify v1.',
        'Runner persists terminal model-contract failures; transport/programming errors still abort rather than being mislabelled model failures.'],
    'sha256':{str(p):rag.sha256_file(p) for p in paths}}
assert report['accepted_total'] == 55 and report['failed_total'] == 1
(OUT/'completion_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
md = '''# Cierre auditable de generación RAG explicitness v2

**55 accepted + 1 failed = 56/56 unidades cubiertas. No es cierre de evaluación RAG.**

| Condición | Accepted | Failed |
|---|---:|---:|
'''
for condition, count in counts.items():
    md += f"| {condition} | {count['accepted']} | {count['failed']} |\n"
md += '''
Se generaron realmente las siete unidades restantes de rerank. Se preservaron las 48 respuestas preexistentes byte a byte (prefijo rerank y tres archivos completos). Reanudación verificada con un generador que falla si es invocado: cero llamadas en las cuatro condiciones. Se comprobaron claves únicas, cobertura exacta, textos y orden top-5 contra corpus/rankings, citas y respuesta contra raw aceptado, y hashes de entradas contra metadata.

## Fallo y diagnóstico

`rerank / q-v1-006__explicit` permanece **failed**, importado de las dos ejecuciones históricas fallidas, tres intentos por ejecución según contrato y contexto operacional. Los logs solo conservan el traceback: raw, tokens y latencia originales no son recuperables y se registran como null, no cero.

Una única llamada diagnóstica separada (no tres nuevos intentos; no aceptación de campaña) reprodujo el error. El modelo emitió `[openstax_principles_ds:4.1:chunk-010]` en CITATIONS, mientras el ID permitido es `openstax_principles_ds:4.1:chunk-010`. Es incumplimiento literal por corchetes: **no demuestra invención del chunk subyacente**. El parser conserva el token y el validador estricto lo rechaza correctamente. No se normalizaron citas ni cambiaron prompt, seed, modelo, top-k o límite. Los seis raw históricos perdidos impiden afirmar que todos tuvieran este mismo defecto exacto.

`citation_diagnostic_single_attempt.json` conserva mensajes, raw, parseo, tokens y latencia medidos del diagnóstico, separados de los desconocidos históricos. El runner ahora preserva fallos terminales y sus intentos/uso/latencia en `_failures.jsonl`, continúa y salta esos fallos al reanudar. Conserva el esquema de respuestas aceptadas; errores de transporte/programación no se convierten en fallos del modelo.

## Pruebas y límites

- TDD: observados RED→GREEN para persistencia de uso/raw terminal, continuación y skip al reanudar, raw malformado, y rechazo de condición incorrecta.
- Suite completa, sin pipes: **155 passed** (`test_suite.log`).
- Ejecución local Ollama; ninguna evaluación por jueces, API de pago ni commit.
- No se dispone del coste/latencia total de campaña por los intentos históricos perdidos. No promediar únicamente éxitos como si fueran todas las unidades.
- Orden secuencial y reanudación temporal son amenazas; el digest de modelo actual no acredita retrospectivamente el digest histórico.
- **Auditoría de atribución pendiente:** decisiones ciegas del asistente etiquetadas `andres` y reviews atribuidas a `gpt5.6`/`glm5.3` sin selección de modelo acreditada. No se modificaron fuentes ajenas a esta tarea ni se ratifican esas atribuciones.
- Existían cambios ajenos en v1 al inicio; esta tarea no los modificó.

## Reproducción de la verificación

Desde TFM: `.venv/bin/python v2/outputs/local_runs/rag_explicitness_v2/verify_resume.py` (sin inferencia; consulta únicamente metadata local del backend). Inventario de hashes y cobertura por unidad en `completion_audit.json`. El script `diagnose_and_resume.py` registra primero el fallo histórico; su replay diagnóstico está acotado a una vez por artefacto y nunca sustituye el fallo por una respuesta aceptada.
'''
(OUT/'completion_audit.md').write_text(md)
print(json.dumps({'counts':counts,'accepted_total':report['accepted_total'],'failed_total':report['failed_total'],'coverage_total':report['coverage_total'],'report':str(OUT/'completion_audit.json')},indent=2))
