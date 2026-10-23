"""Analyse frozen FINAL generation/evaluation only; no inference or historical writes.

Within each generator/criterion intersect the four retrieval strategies on exact
formulations BEFORE averaging formulations within each independent base question.
No generator-capacity axis, pilot recommendation, score imputation or pooling.
"""
from __future__ import annotations

from collections import defaultdict
from statistics import mean, median, pstdev
import math
from itertools import combinations

import argparse
import hashlib
import json
from pathlib import Path
import platform
from typing import Any

from analysis_capacity_v3 import (BASE, RUN, CRIT, CONDS, N_BOOT, SEED, cargar,
                                  macro_base, bootstrap_ci, contrast_trace,
                                  coverage_report, write_csv)

MODELS = ('gemma4:e4b', 'qwen3.5:4b', 'qwen3.5:9b')
LABELS = dict(zip(MODELS, ('Gemma', 'Qwen4', 'Qwen9')))


def analyze_quality(rows):
    """Criterion-specific four-strategy common support, then base macro."""
    seen, behaviors = set(), {}
    for r in rows:
        key = (r['generator_model'],r['retrieval_condition'],r['qid'])
        if key in seen:
            raise ValueError(f'duplicate quality cell: {key}')
        seen.add(key)
        if r['generator_model'] not in MODELS or r['retrieval_condition'] not in CONDS:
            raise ValueError('unknown final generator/retrieval condition')
        if r['qid'] not in (r['base_qid']+'__explicit',r['base_qid']+'__implicit'):
            raise ValueError('formulation/base identity mismatch')
        behavior = r['expected_behavior']
        if behavior not in ('answer','grounded_correction','abstain'):
            raise ValueError('invalid expected behavior')
        if r['qid'] in behaviors and behaviors[r['qid']] != behavior:
            raise ValueError('expected behavior differs across strategies/generators')
        behaviors[r['qid']] = behavior
        for cr in CRIT:
            v = r.get(cr)
            if v is None or v == 'na':
                continue
            if type(v) not in (int,float) or not math.isfinite(v) or not 0 <= v <= (1 if cr=='citations_ok' else 2):
                raise ValueError(f'invalid {cr} score: {v}')
    levels, contrasts, availability = [], [], []
    for g in MODELS:
        for cr in CRIT:
            eligible = [r for r in rows if r['generator_model'] == g and
                        (cr not in ('faithfulness', 'factual_correctness') or
                         r['expected_behavior'] in ('answer', 'grounded_correction'))]
            cells = {c: {r['qid']: r for r in eligible if r['retrieval_condition'] == c
                         and type(r.get(cr)) in (int, float)} for c in CONDS}
            support = sorted(set.intersection(*(set(d) for d in cells.values())))
            for c in CONDS:
                accepted = [r for r in rows if r['generator_model']==g and r['retrieval_condition']==c]
                in_scope = [r for r in eligible if r['retrieval_condition']==c]
                unavailable = sorted(r['qid'] for r in in_scope if type(r.get(cr)) not in (int,float))
                excluded = sorted(set(cells[c]) - set(support))
                availability.append(dict(generator_model=g, model=LABELS[g], retrieval_condition=c,
                                         criterion=cr, n_accepted=len(accepted), n_in_scope=len(in_scope),
                                         n_outside_scope=len(accepted)-len(in_scope), n_numeric=len(cells[c]),
                                         n_unavailable=len(unavailable), n_common=len(support),
                                         n_numeric_excluded=len(excluded), unavailable_qids=unavailable,
                                         numeric_excluded_qids=excluded))
                selected = [cells[c][qid] for qid in support]
                bases = defaultdict(list)
                for r in selected:
                    bases[r['base_qid']].append(r[cr])
                levels.append(dict(generator_model=g, model=LABELS[g], retrieval_condition=c,
                                   criterion=cr, mean=macro_base(selected, cr),
                                   n_cells=len(support), n_base=len(bases), support=support,
                                   base_means={b: mean(bases[b]) for b in sorted(bases)}))
            for a, b in combinations(CONDS, 2):
                per_base = defaultdict(list)
                trace = []
                for qid in support:
                    base = cells[a][qid]['base_qid']
                    delta = cells[b][qid][cr] - cells[a][qid][cr]
                    per_base[base].append(delta)
                    trace.append(dict(qid=qid, base_qid=base, delta=delta))
                point, lo, hi = bootstrap_ci([mean(per_base[k]) for k in sorted(per_base)])
                contrasts.append(dict(generator_model=g, model=LABELS[g], criterion=cr,
                                      from_condition=a, to_condition=b, diff=point,
                                      ic95_lo=lo, ic95_hi=hi, n_cells=len(support),
                                      n_base=len(per_base), support=support,
                                      interval_scope='pointwise post-hoc descriptive; unadjusted',
                                      **contrast_trace(per_base, trace)))
    return dict(levels=levels, contrasts=contrasts, availability=availability)


def analyze_operations(generations, failures):
    """Recorded cumulative usage, one observation per unit; failed units separate.

    Top-level usage was accumulated by run_rag_generation.generate_validated.
    It is never added to the attempt ledger again. Missing values are recovered
    only when EVERY declared attempt provides that field, not from partial sums.
    """
    cells = []
    for status, rows in (('accepted', generations), ('failed', failures)):
        for r in rows:
            attempts = r.get('generation_attempts')
            raw = r.get('raw_generation_attempts')
            if attempts is not None and (type(attempts) is not int or attempts < 1):
                raise ValueError('invalid attempt count')
            if isinstance(raw, list) and attempts is not None and len(raw) != attempts:
                raise ValueError('raw/declared attempt count mismatch')
            ledger = r.get('attempt_usage', [])
            complete = attempts is not None and len(ledger) == attempts
            out: dict[str, Any] = dict(qid=r['qid'], base_qid=r['base_qid'], generator_model=r['generator_model'],
                       model=LABELS[r['generator_model']], retrieval_condition=r['retrieval_condition'],
                       expected_behavior=r['expected_behavior'], status=status,
                       source=r['generation_source'] if status=='accepted' else r['failure_source'],
                       generation_attempts=attempts, raw_attempts_count=len(raw) if isinstance(raw,list) else None,
                       attempt_usage_count=len(ledger), attempt_usage_complete=complete,
                       usage_basis='recorded_cumulative', error=r.get('error'))
            for field in ('generation_latency_ms', 'prompt_tokens', 'completion_tokens'):
                numeric = lambda v: type(v) in (int,float) and math.isfinite(v) and v >= 0
                value = r.get(field)
                if value is not None and not numeric(value):
                    raise ValueError(f'invalid operational {field}: {value}')
                full = complete and all(numeric(a.get(field)) for a in ledger)
                total = sum(a[field] for a in ledger) if full else None
                if full and value is not None and not math.isclose(value,total,rel_tol=1e-9,abs_tol=1e-6):
                    raise ValueError(f'cumulative {field} disagrees with complete attempt ledger')
                out[field] = value if value is not None else total
                out[field+'_basis'] = ('recorded_cumulative' if value is not None else
                                        'complete_attempt_sum' if full else 'unavailable')
            out['latency_s'] = out['generation_latency_ms']/1000 if out['generation_latency_ms'] is not None else None
            cells.append(out)
    summary = []
    for g in MODELS:
        for c in CONDS:
            for status in ('accepted','failed'):
                sub = [r for r in cells if (r['generator_model'],r['retrieval_condition'],r['status'])==(g,c,status)]
                attempts = [r['generation_attempts'] for r in sub if r['generation_attempts'] is not None]
                out: dict[str, Any] = dict(generator_model=g,model=LABELS[g],retrieval_condition=c,status=status,
                           n_cells=len(sub), n_base=len({r['base_qid'] for r in sub}),
                           n_attempts=sum(attempts), n_attempt_count_unavailable=len(sub)-len(attempts),
                           n_retried_units=sum(n>1 for n in attempts),
                           n_complete_attempt_ledgers=sum(r['attempt_usage_complete'] for r in sub),
                           aggregation='arithmetic over recorded units; not base macro')
                for field in ('latency_s','prompt_tokens','completion_tokens'):
                    values = sorted(r[field] for r in sub if r[field] is not None)
                    out.update({field+'_n_numeric':len(values),field+'_n_unavailable':len(sub)-len(values),
                                field+'_mean':mean(values) if values else None,
                                field+'_median':median(values) if values else None,
                                field+'_p95':values[math.ceil(.95*len(values))-1] if values else None,
                                field+'_min':min(values) if values else None,
                                field+'_max':max(values) if values else None,
                                field+'_sd_population':pstdev(values) if values else None,
                                field+'_total':sum(values) if values else None})
                summary.append(out)
    return dict(cells=cells,summary=summary)


def make_memoria_tables(quality, operations):
    """Full precision CSV sources; fixed generator × strategy ordering."""
    levels = {(r['generator_model'],r['retrieval_condition'],r['criterion']):r for r in quality['levels']}
    ops = {(r['generator_model'],r['retrieval_condition'],r['status']):r for r in operations['summary']}
    main, operational = [], []
    for g in MODELS:
        for c in CONDS:
            r = dict(generator_model=g, model=LABELS[g], retrieval_condition=c)
            for cr in CRIT:
                level = levels[g,c,cr]
                r.update({cr+'_mean':level['mean'], cr+'_n_cells':level['n_cells'], cr+'_n_base':level['n_base']})
            main.append(r)
            a, f = ops[g,c,'accepted'], ops[g,c,'failed']
            operational.append(dict(generator_model=g,model=LABELS[g],retrieval_condition=c,
                                    latency_s_mean=a['latency_s_mean'],prompt_tokens_mean=a['prompt_tokens_mean'],
                                    completion_tokens_mean=a['completion_tokens_mean'],accepted=a['n_cells'],
                                    failed=f['n_cells'],latency_s_n_numeric=a['latency_s_n_numeric'],
                                    prompt_tokens_n_numeric=a['prompt_tokens_n_numeric'],
                                    completion_tokens_n_numeric=a['completion_tokens_n_numeric']))
    return main, operational


def fmt(value, decimals=3):
    """Round once, directly from full precision; Spanish decimal comma."""
    return '—' if value is None else f'{value:.{decimals}f}'.replace('.',',')


def proposed_results(data, main, operational):
    """Suggested memoria prose and two fixed tables, generated from this analysis."""
    cov = data['coverage_summary']
    lines = ['## Comparación final de recuperadores dentro de cada generador', '',
             'La campaña final es la evidencia empírica principal. Se comparan bm25, dense, rrf y rerank '
             'dentro de cada generador; no se combinan sus puntuaciones ni se toma el piloto como ancla de la recomendación. '
             'El piloto y la exploración quedan como material suplementario separado.', '',
             f"Se cerraron {cov['n_planned']} unidades previstas: {cov['n_accepted']} respuestas aceptadas y "
             f"{cov['n_failed']} fallos de contrato. La evaluación final cubre todas las aceptadas. "
             'Las puntuaciones consolidadas combinan consenso entre jueces y decisiones humanas sobre las discrepancias, '
             'no una revisión humana exhaustiva ni métricas RAGAS estándar. Los fallos no se convierten en ceros de calidad.', '',
             'Para cada generador y criterio se intersectan las formulaciones disponibles y numéricas de las cuatro '
             'estrategias antes de agregar. Cada pregunta base aporta la media de sus formulaciones retenidas; '
             'la media final asigna el mismo peso a cada base. Puede quedar una sola formulación de una base. '
             'Fundamentación y corrección incluyen solo tareas esperadas answer o grounded_correction; '
             'conducta y citas incluyen todas las tareas. Los soportes son específicos del generador y criterio, '
             'por lo que los niveles no establecen una comparación directa entre generadores.', '',
             '| Modelo | Método | Fundamentación | Corrección | Conducta | Citas |',
             '|---|---|---:|---:|---:|---:|']
    for r in main:
        values = [f"{fmt(r[cr+'_mean'])} ({r[cr+'_n_cells']})" for cr in CRIT]
        lines.append('| '+' | '.join([r['model'],r['retrieval_condition'],*values])+' |')
    lines += ['', ': Calidad final sobre soporte común de las cuatro estrategias: media macro por pregunta base (n_cells por estrategia). {#tbl-final-recuperadores}', '',
              'Nota: fundamentación, corrección y conducta tienen escala 0–2; citas, 0–1. '
              'Los paréntesis cuentan formulaciones por estrategia, no unidades independientes. '
              'Los denominadores por criterio (n_cells / n_base) son:']
    for g in MODELS:
        r = next(r for r in main if r['generator_model']==g)
        lines.append('- '+LABELS[g]+': '+ '; '.join(f"{name} {r[cr+'_n_cells']} / {r[cr+'_n_base']}" for cr,name in
                   zip(CRIT,('fundamentación','corrección','conducta','citas')))+'.')
    lines += ['', '### Lectura descriptiva y recomendación condicionada', '']
    for g in MODELS:
        sub = [r for r in main if r['generator_model']==g]
        findings = []
        for cr,name in zip(CRIT,('fundamentación','corrección','conducta','citas')):
            valid = [r for r in sub if r[cr+'_mean'] is not None]
            if valid:
                best = max(r[cr+'_mean'] for r in valid)
                winners = [r['retrieval_condition'] for r in valid if r[cr+'_mean']==best]
                findings.append(name+': '+', '.join(winners)+' ('+fmt(best)+')')
        lines.append('- '+LABELS[g]+', máximos observados: '+'; '.join(findings)+'.')
    lines += ['', 'Con Gemma, dense ofrece el máximo descriptivo de corrección, mientras rerank lo ofrece en '
              'fundamentación y rrf en citas: no se optimizan a la vez. Con Qwen4, rerank es una opción si la '
              'prioridad es el contenido (fundamentación y corrección), pero rrf conserva el mayor nivel de '
              'conducta. Con Qwen9, rrf es una opción si se prioriza fundamentación y citas; rerank si se '
              'prioriza corrección y conducta, con una menor puntuación de citas. Estas son recomendaciones '
              'condicionadas al experimento final, no al piloto, y no una demostración de superioridad.', '',
              'Estos máximos son descriptivos, no pruebas de superioridad estadística. '
              'La recomendación debe condicionarse al generador y al criterio prioritario, sin construir un índice '
              'compuesto ni decidir pesos después de observar los resultados. No hay base para declarar un ganador '
              'universal a partir de un único máximo. Los seis contrastes por generador y criterio se publican sin '
              'seleccionar extremos: diferencia destino − origen, primero por formulación y después por base. '
              f'Los IC percentiles del 95 % usan {N_BOOT} réplicas y semilla {SEED}; son intervalos puntuales '
              'post-hoc/descriptivos, no ajustados por multiplicidad. No acreditan superioridad familiar y '
              'un intervalo que contiene cero no demuestra equivalencia.', '',
              '### Tiempo y tokens registrados en la generación final', '',
              '| Modelo | Método | Latencia (s) | Prompt (tokens) | Completion (tokens) | Aceptadas | Fallidas |',
              '|---|---|---:|---:|---:|---:|---:|']
    for r in operational:
        lines.append('| '+' | '.join([r['model'],r['retrieval_condition'],fmt(r['latency_s_mean']),
                     fmt(r['prompt_tokens_mean'],1),fmt(r['completion_tokens_mean'],1),str(r['accepted']),str(r['failed'])])+' |')
    lines += ['', ': Descriptivos operacionales de generación final: medias aritméticas de unidades aceptadas y cobertura de fallos separada. {#tbl-final-operacion}', '',
              'Nota: los denominadores de las tres medias son las aceptadas de cada fila; '
              'su disponibilidad se conserva en el CSV. Son observaciones de la campaña, no un benchmark controlado '
              'ni mediciones de latencia end-to-end del RAG. Proceden de generation_latency_ms / 1000, '
              'prompt_tokens y completion_tokens de los doce JSONL finales. Son totales registrados acumulados '
              'sobre los intentos de la unidad, no solo el último intento. Los costes de recuperación, evaluación, '
              'energía y amortización no están medidos; no se estima coste monetario. Las diferencias pueden '
              'reflejar longitud de respuesta, contexto, reintentos, carga y orden de ejecución, además del generador. '
              'Los fallos, sus tiempos y tokens se publican por separado en operational_summary.csv. '
              'Las aceptadas no conservan un desglose numérico por intento, de modo que sus acumulados no pueden '
              'reconstruirse de forma independiente a partir del texto bruto. Los fallos sí conservan attempt_usage; '
              'solo se recuperan totales ausentes si ese ledger está completo.', '',
              'El estudio evalúa fiabilidad informacional bajo este corpus, conjunto de preguntas y contrato, '
              'no efectividad pedagógica. El replay offline reproduce el análisis, no otra campaña de inferencia.']
    return '\n'.join(lines)+'\n'


def reproducible_report(data, proposed):
    """Audit, operational availability and EVERY paired comparison, not selected examples."""
    lines = ['# Informe reproducible — experimento FINAL', '',
             '## Reproducción offline', '', 'Desde la raíz v2, con uv y el entorno ya sincronizado:', '',
             '```sh', 'uv run --no-sync python scripts/analyze_final_experiment.py --output-dir outputs/local_runs/final_experiment_20260930/analysis',
             'uv run --no-sync python scripts/analyze_final_experiment.py --output-dir outputs/local_runs/final_experiment_20260930/verificationsecond',
             'uv run --no-sync pytest tests/test_final_experiment.py -q', '```', '',
             'Cada destino debe ser nuevo. No se permiten destinos externos, históricos ni sobrescrituras. '
             'La segunda ejecución conserva nombres y hashes sin rutas absolutas, reloj o metadatos volátiles. '
             'hash_manifest.json contiene hashes SHA-256 de cada fuente y de cada salida excepto sí mismo. '
             'La comparación byte-exacta cubre también el manifiesto.', '',
             f"Python registrado: {data['python']}. Bootstrap: {N_BOOT} réplicas; random.Random({SEED}) "
             'reiniciado por contraste, IC percentil en índices floor(0,025B), floor(0,975B), diferencias de medias '
             'por base. Semilla y algoritmo reutilizados sin modificar analysis_capacity_v3.py.', '',
             'Fuentes activas: solo doce archivos rag_<estrategia>_top5_<generador>.jsonl de los tres generadores '
             'elegibles, sus ledgers de fallos y eval_final_v3.jsonl. Se excluyen modelos no elegibles, evaluaciones '
             'invalidada/diagnóstica, piloto y exploración. El pre-registro, las decisiones y las fuentes permanecen congelados.', '',
             proposed, '', '## Auditoría de cobertura y disponibilidad', '',
             '| Modelo | Método | Previstas | Aceptadas | Fallidas | Faith num. | Factual num. | Conducta num. | Citas num. |',
             '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in data['tables']['operational']:
        sub = [x for x in data['joined_cells'] if x['generator_model']==r['generator_model'] and x['retrieval_condition']==r['retrieval_condition']]
        n = [sum(type(x.get(cr)) in (int,float) for x in sub) for cr in CRIT]
        lines.append('| '+' | '.join([r['model'],r['retrieval_condition'],str(r['accepted']+r['failed']),str(r['accepted']),str(r['failed']),*map(str,n)])+' |')
    lines += ['', 'Disponibilidad anterior calculada sobre todas las aceptadas; no confundir con aplicabilidad ni soporte '
              'común. availability.csv informa por generador, estrategia y criterio: aceptadas, dentro/fuera del ámbito, '
              'numéricas, no disponibles, comunes y numéricas excluidas, con qids. analysis.json y support_cells.csv '
              'permiten reconstruir las medias y sus denominadores. Los fallos no reciben puntuación.', '',
              '### Intentos y disponibilidad operacional', '',
              '| Modelo | Método | Estado | Unidades | Intentos | Reintentadas | Ledger completo | Latencia n | Prompt n | Completion n |',
              '|---|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in data['operations']['summary']:
        lines.append('| '+' | '.join([r['model'],r['retrieval_condition'],r['status'],str(r['n_cells']),str(r['n_attempts']),
                     str(r['n_retried_units']),str(r['n_complete_attempt_ledgers']),str(r['latency_s_n_numeric']),
                     str(r['prompt_tokens_n_numeric']),str(r['completion_tokens_n_numeric'])])+' |')
    lines += ['', 'Los acumulados se leen una sola vez: nunca se añade el total de attempt_usage al total ya '
              'registrado. Los 20 ledgers fallidos permiten comprobar las sumas de cada intento. '
              'Los descriptivos completos incluyen media, mediana, p95 por nearest-rank (ceil(0,95n)), mínimo, máximo, '
              'desviación poblacional, suma y disponibilidad; son aritméticos por unidad, no macro por base.', '',
              '## Los seis contrastes no seleccionados por generador y criterio', '',
              'Signo: destino − origen. Pos/neg/empates se cuentan sobre preguntas base tras promediar '
              'las diferencias de sus formulaciones comunes a las CUATRO estrategias. No se interpreta la exclusión '
              'del cero como superioridad ajustada. No hay corrección por multiplicidad ni conclusión de equivalencia.', '']
    for g in MODELS:
        lines += ['### '+LABELS[g], '', '| Criterio | Origen → destino | Delta | IC95 puntual | n_cells | n_base | Pos | Neg | Empates |',
                  '|---|---|---:|---|---:|---:|---:|---:|---:|']
        for r in data['quality']['contrasts']:
            if r['generator_model']==g:
                lines.append('| '+' | '.join([r['criterion'],r['from_condition']+' → '+r['to_condition'],fmt(r['diff']),
                             '['+fmt(r['ic95_lo'])+'; '+fmt(r['ic95_hi'])+']',str(r['n_cells']),str(r['n_base']),
                             str(r['positive']),str(r['negative']),str(r['ties'])])+' |')
        lines.append('')
    lines += ['## Artefactos y contrato', '',
              '- main_table.csv: 12 filas, medias a precisión completa y n_cells/n_base por criterio; fuente de tbl-final-recuperadores (96 cifras visibles).',
              '- operational_table.csv: 12 filas; medias de aceptadas y conteos de aceptadas/fallidas; fuente de tbl-final-operacion (60 cifras visibles).',
              '- per_retriever.csv y operational.csv: copias de los dos CSV anteriores para integración con el contrato documental.',
              '- quality_levels.csv (48) y paired_contrasts.csv (72): niveles y todos los contrastes; trazas completas en analysis.json.',
              '- coverage.csv, availability.csv, failures.csv y joined_cells.csv: cobertura, disponibilidad, fallos y puntuaciones consolidadas.',
              '- support_cells.csv: cada celda de soporte y puntuación que contribuye a cada nivel.',
              '- operational_cells.csv (624) y operational_summary.csv (24): procedencia fila/archivo y descriptivos separados por estado.',
              '- results_proposed.md: propuesta generada para integrar en memoria; no modifica tfm.qmd.',
              '- analysis.json y hash_manifest.json: parámetros, resultados, trazas y hashes; no se usa un eje externo de capacidad.', '',
              'La calidad es condicional a respuestas aceptadas y a soporte común. Fallos asimétricos pueden producir '
              'sesgo de supervivencia; no se eliminan de la auditoría ni se imputan. Las variantes no son réplicas '
              'independientes. Los IC puntuales no proporcionan control de error familiar. El corpus y golden set '
              'limitan la generalización. El replay determinista no verifica disponibilidad actual de modelos/API '
              'y no añade datos ni reevalúa decisiones humanas.']
    return '\n'.join(lines)+'\n'


def main(argv=None):
    """Exporta el análisis offline de calidad y operación de la campaña final."""
    parser = argparse.ArgumentParser(description='Offline FINAL-only retriever comparison; fresh artifacts.')
    parser.add_argument('--output-dir',required=True,type=Path)
    args = parser.parse_args(argv)
    output = args.output_dir.resolve()
    allowed = (BASE/'outputs/local_runs/final_experiment_20260930').resolve()
    if not output.is_relative_to(allowed) or output == allowed:
        parser.error('output-dir must be a new directory under outputs/local_runs/final_experiment_20260930')
    if output.exists():
        parser.error('output-dir exists; refusing to overwrite')
    rows, failures, sources = cargar()
    if (len(rows),len(failures)) != (604,20):
        raise ValueError('FINAL must cover exactly 604 accepted + 20 failed')
    quality = analyze_quality(rows)
    # Recover only generation fields from the exact traced row (not from evaluation).
    by_path = {}
    generations = []
    for r in rows:
        src = r['generation_source']
        if src['path'] not in by_path:
            by_path[src['path']] = [json.loads(line) for line in (BASE/src['path']).read_text(encoding='utf-8').splitlines() if line.strip()]
        gen = by_path[src['path']][src['row']-1]
        if (gen['qid'],gen['generator_model'],gen['retrieval_condition']) != (r['qid'],r['generator_model'],r['retrieval_condition']):
            raise ValueError('generation provenance row mismatch')
        generations.append(dict(gen,base_qid=r['base_qid'],generation_source=src))
    operations = analyze_operations(generations,failures)
    main_table, ops_table = make_memoria_tables(quality,operations)
    coverage = coverage_report(rows,failures)
    data = dict(quality=quality,operations=operations,joined_cells=rows,
                tables=dict(main=main_table,operational=ops_table),coverage=coverage,python=platform.python_version(),
                scopes={cr:['answer','grounded_correction'] if cr in ('faithfulness','factual_correctness') else
                        ['answer','grounded_correction','abstain'] for cr in CRIT},
                bootstrap=dict(replicates=N_BOOT,seed=SEED,unit='base question',interval='pointwise post-hoc descriptive; unadjusted'),
                coverage_summary=dict(n_planned=len(rows)+len(failures),n_accepted=len(rows),n_failed=len(failures),
                                      n_formulations=len({r['qid'] for r in rows}),n_base=len({r['base_qid'] for r in rows}),
                                      unavailable_by_criterion={cr:sum(type(r.get(cr)) not in (int,float) for r in rows) for cr in CRIT}),
                quality_unit='four-strategy intersection on formulation; mean within base, then equal-weight bases',
                no_model_calls=True,no_historical_writes=True,
                limits=['conditional accepted-output quality; asymmetric failures',
                        'post-hoc pointwise intervals do not control multiplicity; no equivalence',
                        'recorded generation descriptives only; not controlled end-to-end timing or monetary cost'])
    proposed = proposed_results(data,main_table,ops_table)
    report = reproducible_report(data,proposed)
    for script in ('analyze_final_experiment.py','analysis_capacity_v3.py','run_rag_generation.py'):
        rel = 'scripts/'+script
        sources[rel] = dict(sha256=hashlib.sha256((BASE/rel).read_bytes()).hexdigest())
    # Check sources did not change while reading. No allocation until all analysis is valid.
    for rel,info in sources.items():
        if hashlib.sha256((BASE/rel).read_bytes()).hexdigest() != info['sha256']:
            raise ValueError('source changed during analysis: '+rel)
    output.mkdir(parents=True,exist_ok=False)
    (output/'analysis.json').write_text(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n',encoding='utf-8')
    for name,records in [('main_table',main_table),('operational_table',ops_table),('quality_levels',quality['levels']),
                         ('per_retriever',main_table),('operational',ops_table),
                         ('paired_contrasts',quality['contrasts']),('availability',quality['availability']),('coverage',coverage),
                         ('joined_cells',rows),('operational_cells',operations['cells']),('operational_summary',operations['summary'])]:
        write_csv(output/(name+'.csv'),records,compact=name=='paired_contrasts')
    write_csv(output/'failures.csv',[{k:r.get(k) for k in ('qid','base_qid','generator_model','retrieval_condition','expected_behavior','error','failure_source')} for r in failures])
    index = {(r['generator_model'],r['retrieval_condition'],r['qid']):r for r in rows}
    support = [dict(generator_model=r['generator_model'],retrieval_condition=r['retrieval_condition'],criterion=r['criterion'],
                    qid=qid,base_qid=index[r['generator_model'],r['retrieval_condition'],qid]['base_qid'],
                    value=index[r['generator_model'],r['retrieval_condition'],qid][r['criterion']])
               for r in quality['levels'] for qid in r['support']]
    write_csv(output/'support_cells.csv',support)
    (output/'results_proposed.md').write_text(proposed,encoding='utf-8')
    (output/'report.md').write_text(report,encoding='utf-8')
    outputs = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.iterdir())}
    manifest = dict(sources=sources,outputs=outputs,python=platform.python_version(),no_model_calls=True,no_historical_writes=True,
                    command='uv run --no-sync python scripts/analyze_final_experiment.py --output-dir <fresh-directory-under-outputs/local_runs/final_experiment_20260930>')
    (output/'hash_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(data['coverage_summary'],ensure_ascii=False,sort_keys=True))
    return data


if __name__ == '__main__':
    main()
