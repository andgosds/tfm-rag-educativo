"""Curva de capacidad del generador (H5) y sensibilidad de las métricas (H6).

Pre-registro: docs/explicitness_v3_preregistration.md §3 (H5, H6) y §4
(unidad = pregunta base; diferencias emparejadas; medias macro).

Índice de capacidad: AA Intelligence Index v4.3.2, aportado por el usuario
(2026-09-28): gemma4:e4b = 9, qwen3.5:4b = 13, qwen3.5:9b = 14. El índice es
un eje x estrictamente descriptivo: con n = 3 modelos no se estima
correlación ni pendiente sobre él.

Entradas finales congeladas: eval_final_v3.jsonl, generación y fallos de
los tres modelos elegibles bajo outputs/local_runs/generation_scaling_v3/.
Conducta esperada unida por (qid, generator_model, retrieval_condition).

CLI obligatorio: --output-dir <directorio NUEVO bajo outputs/local_runs/>.
CSV/JSON sin matplotlib ni llamadas a modelos. Contenido answer/correction
principal; all/abstain diagnósticos. No sobrescribe histórico ni juicios.
Escalas: faith/factual/behavior 0–2; citations 0–1. Índice no verificado
externamente. Todas las diferencias intersectan celdas por criterio ANTES
de agregar por pregunta base; los niveles disponibles son condicionales.
"""

from __future__ import annotations

import csv
import argparse
import hashlib
import platform
from itertools import combinations
import json
import math
import random
from pathlib import Path
from statistics import mean
from typing import Any

BASE = Path(__file__).resolve().parent.parent
RUN = BASE / "outputs" / "local_runs" / "generation_scaling_v3"


CAPACITY = {"gemma4:e4b": 9, "qwen3.5:4b": 13, "qwen3.5:9b": 14}
CAPACITY_SOURCE = "AA Intelligence Index v4.3.2 (aportado por el usuario, 2026-09-28)"
MODELOS = sorted(CAPACITY, key=CAPACITY.get)  # de menor a mayor capacidad
CONDS = ["bm25", "dense", "rrf", "rerank"]
CRIT = ["faithfulness", "factual_correctness", "behavior_ok", "citations_ok"]
SCALES = {cr: [0, 1 if cr == 'citations_ok' else 2] for cr in CRIT}
N_BOOT = 5000
SEED = 20260928


def cell_key(row):
    """Identifica una celda por pregunta, generador y estrategia de recuperación."""
    return (row['qid'], row['generator_model'], row['retrieval_condition'])


def enrich_evaluations(scores, generations):
    """Recuperar conducta esperada de generación por clave completa, sin editar juicios."""
    index = {}
    for row in generations:
        key = cell_key(row)
        if key in index:
            raise ValueError(f'duplicate generation key: {key}')
        index[key] = row
    if len({cell_key(r) for r in scores}) != len(scores):
        raise ValueError('duplicate evaluation key')
    if set(index) != {cell_key(r) for r in scores}:
        raise ValueError('evaluation/generation coverage mismatch')
    result = []
    for row in scores:
        for cr in CRIT:
            v = row.get(cr)
            if v is None or v == 'na':
                continue
            if type(v) not in (int,float) or not math.isfinite(v) or not SCALES[cr][0] <= v <= SCALES[cr][1]:
                raise ValueError(f'invalid {cr} score: {v}')
        behavior = index[cell_key(row)].get('expected_behavior')
        if behavior not in ('answer','grounded_correction','abstain'):
            raise ValueError(f'missing expected behavior: {cell_key(row)}')
        if row.get('expected_behavior') not in (None,behavior):
            raise ValueError('conflicting expected behavior')
        joined = dict(row,expected_behavior=behavior)
        if 'generation_source' in index[cell_key(row)]:
            joined['generation_source'] = index[cell_key(row)]['generation_source']
        result.append(joined)
    return result


def cargar():
    """Leer sólo campaña final y tres generadores elegibles; exigir cierre exacto."""
    sources = {}
    def read(path):
        """Lee un JSONL y registra su hash y número de filas como procedencia."""
        rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
        sources[str(path.relative_to(BASE))] = dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(),n_rows=len(rows))
        return rows
    generations,failures = [],[]
    slugs = dict(zip(MODELOS,('gemma4_e4b','qwen35_4b','qwen35_9b')))
    for g in MODELOS:
        for c in CONDS:
            path = RUN/f'rag_{c}_top5_{slugs[g]}.jsonl'
            for number,row in enumerate(read(path),1):
                if row['generator_model'] != g or row['retrieval_condition'] != c:
                    raise ValueError('generation file identity mismatch')
                generations.append(dict(row,generation_source=dict(path=str(path.relative_to(BASE)),row=number)))
            fp = path.with_name(path.stem+'_failures.jsonl')
            if fp.exists():
                for number,row in enumerate(read(fp),1):
                    if row['generator_model'] != g or row['retrieval_condition'] != c or row.get('status') != 'failed':
                        raise ValueError('failure file identity mismatch')
                    failures.append(dict(row,failure_source=dict(path=str(fp.relative_to(BASE)),row=number)))
    filas = enrich_evaluations(read(RUN/'eval_final_v3.jsonl'),generations)
    behavior = {}
    for row in generations:
        key = (row['qid'],row['retrieval_condition'])
        if key in behavior and behavior[key] != row['expected_behavior']:
            raise ValueError('expected behavior varies by generator')
        behavior[key] = row['expected_behavior']
    qids = sorted({row['qid'] for row in generations})
    for row in filas:
        if row['qid'] != row['base_qid']+'__explicit' and row['qid'] != row['base_qid']+'__implicit':
            raise ValueError('formulation/base identity mismatch')
    planned = {(qid,g,c) for qid in qids for g in MODELOS for c in CONDS}
    accepted = {cell_key(row) for row in filas}
    failed = {cell_key(row) for row in failures}
    if len(failed)!=len(failures) or accepted & failed or accepted | failed != planned:
        raise ValueError('planned/accepted/failed campaign coverage mismatch')
    if len(qids)!=52 or len({q.rsplit('__',1)[0] for q in qids})!=26:
        raise ValueError('campaign formulation coverage mismatch (52 formulations/26 bases required)')
    for row in failures:
        row['expected_behavior'] = behavior[(row['qid'],row['retrieval_condition'])]
        row['base_qid'] = row['qid'].rsplit('__',1)[0]
    return filas,failures,sources


def macro_base(filas, valor):
    """Media macro sobre preguntas base: primero media por base_qid, luego entre base_qid."""
    por_base: dict[str, list[float]] = {}
    for f in filas:
        v = f.get(valor)
        if isinstance(v, (int, float)):
            por_base.setdefault(f["base_qid"], []).append(float(v))
    if not por_base:
        return None
    return mean(mean(vs) for vs in por_base.values())


def bootstrap_ci(valores_pareados):
    """IC percentil 95 % sobre medias macro de diferencias emparejadas por pregunta base."""
    rng = random.Random(SEED)
    n = len(valores_pareados)
    if n == 0:
        return (None, None, None)
    punto = mean(valores_pareados)
    boots = []
    for _ in range(N_BOOT):
        muestra = [valores_pareados[rng.randrange(n)] for _ in range(n)]
        boots.append(mean(muestra))
    boots.sort()
    return (punto, boots[int(0.025 * N_BOOT)], boots[int(0.975 * N_BOOT)])


def contrast_trace(per_base, records):
    """Soporte auditable y test de signos exacto bilateral (doblar cola menor)."""
    values = {b: mean(per_base[b]) for b in sorted(per_base)}
    pos = sum(v > 0 for v in values.values())
    neg = sum(v < 0 for v in values.values())
    n = pos + neg
    p = min(1.0, 2 * sum(math.comb(n,k) for k in range(min(pos,neg)+1)) / 2**n) if n else 1.0
    return dict(base_differences=values,cell_differences=records,
                positive=pos,negative=neg,ties=len(values)-n,sign_n=n,sign_p_two_sided=p)


def h5(filas, common=False):
    """Extremos descriptivos, seleccionados en soporte común de cuatro estrategias.

    Empates: orden CONDS; peor distinto del mejor. No inferencia postselección.
    """
    filas_h5 = []
    for g in MODELOS:
        for cr in CRIT:
            selected = common_rows(filas,cr) if common else filas
            cells = {c: {f['qid']: f for f in selected if f['generator_model']==g
                         and f['retrieval_condition']==c and isinstance(f.get(cr), (int, float))}
                     for c in CONDS}
            support = sorted(set.intersection(*(set(d) for d in cells.values())))
            if not support:
                continue
            medias = {c: macro_base([cells[c][k] for k in support], cr) for c in CONDS}
            mejor = max(CONDS, key=lambda c: medias[c])
            peor = min((c for c in CONDS if c != mejor), key=lambda c: medias[c])
            por_base = {}
            for key in support:
                por_base.setdefault(cells[mejor][key]['base_qid'], []).append(
                    cells[mejor][key][cr] - cells[peor][key][cr])
            diffs = [mean(por_base[b]) for b in sorted(por_base)]
            punto, lo, hi = bootstrap_ci(diffs)
            filas_h5.append({
                "generator_model": g, "capacity": CAPACITY[g], "criterion": cr,
                "mejor": mejor, "peor": peor,
                "media_mejor": medias[mejor],
                "media_peor": medias[peor],
                "ventaja": punto,
                "ic95_lo": lo,
                "ic95_hi": hi,
                "n_cells": len(support),
                "selection": "descriptive; four-strategy common support; CONDS tie order",
                **contrast_trace(por_base,[dict(key=[k],base_qid=cells[mejor][k]['base_qid'],
                                               delta=cells[mejor][k][cr]-cells[peor][k][cr]) for k in support]),
                "n_base": len(diffs),
            })
    return filas_h5


def h5_comparaciones(filas, common=False):
    """Los seis pares de estrategias, sin selección; signo = destino − origen."""
    out = []
    for g in MODELOS:
        for cr in CRIT:
            for a, b in combinations(CONDS, 2):
                selected = common_rows(filas,cr) if common else filas
                cells = [{f['qid']: f for f in selected if f['generator_model']==g
                          and f['retrieval_condition']==c and isinstance(f.get(cr), (int, float))}
                         for c in (a,b)]
                support = sorted(cells[0].keys() & cells[1].keys())
                per_base = {}
                for k in support:
                    per_base.setdefault(cells[0][k]['base_qid'], []).append(cells[1][k][cr]-cells[0][k][cr])
                values = [mean(per_base[k]) for k in sorted(per_base)]
                point, lo, hi = bootstrap_ci(values)
                out.append(dict(generator_model=g, criterion=cr, from_condition=a,
                                to_condition=b, diff=point, ic95_lo=lo, ic95_hi=hi,
                                n_cells=len(support), n_base=len(values),
                                **contrast_trace(per_base,[dict(key=[k],base_qid=cells[0][k]['base_qid'],
                                                               delta=cells[1][k][cr]-cells[0][k][cr]) for k in support])))
    return out


def common_rows(filas, cr):
    """Soporte celular numérico común de los tres modelos, por criterio."""
    keys = [{(f['qid'],f['retrieval_condition']) for f in filas
             if f['generator_model']==g and isinstance(f.get(cr),(int,float))} for g in MODELOS]
    common = set.intersection(*keys)
    return [f for f in filas if (f['qid'],f['retrieval_condition']) in common]


def h6_niveles(filas, common=False):
    """Niveles macro por generador con IC 95 % (bootstrap sobre preguntas base)."""
    out = []
    for g in MODELOS:
        sub = [f for f in filas if f["generator_model"] == g]
        fila = {"generator_model": g, "capacity": CAPACITY[g], "n_rows": len(sub)}
        for cr in CRIT:
            selected = [f for f in common_rows(filas, cr) if f['generator_model']==g] if common else sub
            por_base: dict[str, list[float]] = {}
            for f in selected:
                v = f.get(cr)
                if isinstance(v, (int, float)):
                    por_base.setdefault(f["base_qid"], []).append(float(v))
            medias_base = [mean(por_base[b]) for b in sorted(por_base)]
            punto, lo, hi = bootstrap_ci(medias_base)
            fila[cr] = punto
            fila[cr + "_ic95"] = [lo, hi] if lo is not None else None
            fila[cr + "_n_base"] = len(medias_base)
            fila[cr + '_n_cells'] = sum(len(v) for v in por_base.values())
            fila[cr + '_unavailable'] = sum(not isinstance(f.get(cr),(int,float)) for f in sub)
            fila[cr + '_excluded_from_support'] = len(sub) - len(selected)
            fila[cr + '_base_means'] = {b: mean(por_base[b]) for b in sorted(por_base)}
            fila[cr + '_support'] = sorted([f['qid'],f['retrieval_condition']] for f in selected if isinstance(f.get(cr),(int,float)))
        out.append(fila)
    return out


def h6_pendientes(filas):
    """Contrastar celdas exactas (qid, estrategia), después macro por base."""
    out = []
    for g_lo, g_hi in combinations(MODELOS, 2):
        for cr in CRIT:
            cells = [{(f["qid"], f["retrieval_condition"]): f for f in filas
                      if f["generator_model"] == g and isinstance(f.get(cr), (int, float))}
                     for g in (g_lo, g_hi)]
            common = sorted(cells[0].keys() & cells[1].keys())
            por_base = {}
            for key in common:
                lo_row, hi_row = cells[0][key], cells[1][key]
                por_base.setdefault(lo_row["base_qid"], []).append(hi_row[cr] - lo_row[cr])
            diffs = [mean(por_base[b]) for b in sorted(por_base)]
            punto, lo, hi = bootstrap_ci(diffs)
            out.append({
                "from_model": g_lo, "from_capacity": CAPACITY[g_lo],
                "to_model": g_hi, "to_capacity": CAPACITY[g_hi],
                "criterion": cr,
                **contrast_trace(por_base,[dict(key=list(k),base_qid=cells[0][k]['base_qid'],
                                               delta=cells[1][k][cr]-cells[0][k][cr]) for k in common]),
                "diff": punto,
                "ic95_lo": lo,
                "ic95_hi": hi,
                "n_cells": len(common),
                "n_base": len(diffs),
            })
    return out


def h6_explicitud(filas, common=False):
    """Diferencia implícita − explícita por pregunta base, emparejada, por generador y criterio."""
    out = []
    for g in MODELOS:
        for cr in CRIT:
            selected = common_rows(filas, cr) if common else filas
            cells = [{(f["base_qid"], f["retrieval_condition"]): f for f in selected
                      if f["generator_model"] == g and f["qid"].endswith('__'+form)
                      and isinstance(f.get(cr), (int, float))}
                     for form in ('explicit', 'implicit')]
            support = sorted(cells[0].keys() & cells[1].keys())
            por_base = {}
            for key in support:
                por_base.setdefault(key[0], []).append(cells[1][key][cr] - cells[0][key][cr])
            diffs = [mean(por_base[b]) for b in sorted(por_base)]
            punto, lo, hi = bootstrap_ci(diffs)
            out.append({
                "generator_model": g, "capacity": CAPACITY[g], "criterion": cr,
                "diff_implicit_minus_explicit": punto,
                **contrast_trace(por_base,[dict(key=list(k),base_qid=k[0],
                                               delta=cells[1][k][cr]-cells[0][k][cr]) for k in support]),
                "ic95_lo": lo,
                "ic95_hi": hi,
                "n_cells": len(support),
                "n_base": len(diffs),
            })
    return out


def h6_interaccion(filas):
    """(Implícita−explícita)_mayor − (implícita−explícita)_menor.

    Positivo indica atenuación de una penalización negativa; no efecto causal
    de capacidad (modelo/familia y capacidad están confundidos).
    """
    out = []
    for a,b in combinations(MODELOS,2):
        for cr in CRIT:
            cells = [{(f['base_qid'],f['retrieval_condition']): f for f in filas
                      if f['generator_model']==g and f['qid'].endswith('__'+form)
                      and isinstance(f.get(cr),(int,float))}
                     for g in (a,b) for form in ('explicit','implicit')]
            common = sorted(set.intersection(*(set(d) for d in cells)))
            effects = [{},{}]
            for key in common:
                for i in range(2):
                    effects[i].setdefault(key[0],[]).append(cells[2*i+1][key][cr]-cells[2*i][key][cr])
            bases = sorted(effects[0])
            values = [mean(effects[1][k])-mean(effects[0][k]) for k in bases]
            point,lo,hi = bootstrap_ci(values)
            out.append(dict(from_model=a,to_model=b,criterion=cr,diff_of_diffs=point,
                            effect_from=mean(mean(effects[0][k]) for k in bases) if bases else None,
                            effect_to=mean(mean(effects[1][k]) for k in bases) if bases else None,
                            ic95_lo=lo,ic95_hi=hi,n_cells=len(common),n_base=len(bases),
                            **contrast_trace({k:[y-x for x,y in zip(effects[0][k],effects[1][k])] for k in bases},
                                             [dict(key=list(k),base_qid=k[0],delta=(cells[3][k][cr]-cells[2][k][cr])-(cells[1][k][cr]-cells[0][k][cr])) for k in common])))
    return out


def build_tables(filas):
    """Contenido principal; all/abstain como sensibilidades, sin imputación."""
    tables: dict[str, Any] = dict(capacity=CAPACITY,capacity_source=CAPACITY_SOURCE,
                  capacity_external_verification=False,scales=SCALES,n_cells=len(filas),
                  unit='base question; exact cell contrasts then macro; successful outputs only',
                  bootstrap=dict(n=N_BOOT,seed=SEED,ic='percentile 95%; indices floor(0.025B),floor(0.975B)'),
                  warnings=['Model identity/family confounds capacity; index user-provided, not externally verified.',
                            'Content metrics on expected abstentions diagnostic only; original scores unchanged.',
                            'Intervals including zero do not establish equivalence or robustness.',
                            'H5 extrema selected descriptively; pairwise intervals unadjusted for multiplicity.'])
    scopes = dict(primary_content=[f for f in filas if f['expected_behavior'] in ('answer','grounded_correction')],
                  sensitivity_all=filas,
                  sensitivity_abstain=[f for f in filas if f['expected_behavior']=='abstain'])
    for name,sub in scopes.items():
        tables[name] = dict(n_cells=len(sub),n_base=len({f['base_qid'] for f in sub}),
                           h6_niveles=h6_niveles(sub),h6_niveles_common=h6_niveles(sub,common=True),
                           h6_pendientes=h6_pendientes(sub),h6_explicitud=h6_explicitud(sub),
                           h6_explicitud_common=h6_explicitud(sub,common=True),
                           h6_interaccion=h6_interaccion(sub),h5_separacion=h5(sub),
                           h5_comparaciones=h5_comparaciones(sub),h5_separacion_common=h5(sub,common=True),
                           h5_comparaciones_common=h5_comparaciones(sub,common=True))
    tables['levels_by_expected_behavior'] = {b: h6_niveles([f for f in filas if f['expected_behavior']==b])
                                            for b in ('answer','grounded_correction','abstain')}
    return tables


def coverage_report(filas,failures):
    """Cobertura conjunta y marginal; fallo de contrato separado de puntuación."""
    dims = ('generator_model','retrieval_condition','explicitness','expected_behavior')
    units = [dict(r,explicitness=r['qid'].rsplit('__',1)[1],accepted=True) for r in filas]
    units += [dict(r,explicitness=r['qid'].rsplit('__',1)[1],accepted=False) for r in failures]
    records = []
    for selected in ((),*( (dim,) for dim in dims),dims):
        groups = {}
        for r in units:
            key = tuple(r[d] for d in selected)
            groups.setdefault(key,[]).append(r)
        for key in sorted(groups):
            sub = groups[key]
            accepted = [r for r in sub if r['accepted']]
            result: dict[str, Any] = dict(group_by='+'.join(selected) or 'all',**{d:'*' for d in dims})
            result.update(zip(selected,key))
            result.update(n_planned=len(sub),n_accepted=len(accepted),n_failed=len(sub)-len(accepted),
                          n_base=len({r['base_qid'] for r in sub}))
            for cr in CRIT:
                n = sum(isinstance(r.get(cr),(int,float)) for r in accepted)
                result[cr+'_n_numeric'] = n
                result[cr+'_n_unavailable'] = len(accepted)-n
            records.append(result)
    return records


def write_csv(path,records,compact=False):
    """Tablas con precisión completa; estructura anidada como JSON válido."""
    def keep(k):
        """Excluye las trazas detalladas cuando se solicita un CSV compacto."""
        return not compact or (k not in ('base_differences','cell_differences') and not k.endswith(('_base_means','_support')))
    fields = list(dict.fromkeys(k for r in records for k in r if keep(k)))
    with path.open('w',encoding='utf-8',newline='') as handle:
        writer = csv.DictWriter(handle,fieldnames=fields,lineterminator='\n')
        writer.writeheader()
        for r in records:
            writer.writerow({k:json.dumps(v,ensure_ascii=False,sort_keys=True,allow_nan=False) if isinstance(v,(dict,list)) else v for k,v in r.items() if keep(k)})


def main(argv=None):
    """Genera las tablas de capacidad y cobertura en un directorio nuevo."""
    parser = argparse.ArgumentParser(description='Offline capacity analysis; fresh CSV/JSON only.')
    parser.add_argument('--output-dir',required=True,type=Path)
    args = parser.parse_args(argv)
    output = args.output_dir.resolve()
    allowed = (BASE/'outputs/local_runs').resolve()
    if not output.is_relative_to(allowed) or output == allowed:
        parser.error('output-dir must be a new directory under outputs/local_runs')
    if output.exists():
        parser.error('output-dir exists; refusing to overwrite')
    filas,failures,sources = cargar()
    tables = build_tables(filas)
    coverage = coverage_report(filas,failures)
    tables['coverage_summary'] = dict(n_planned=len(filas)+len(failures),n_accepted=len(filas),n_failed=len(failures),
                                      by_expected_behavior={b:sum(r['expected_behavior']==b for r in filas) for b in ('answer','grounded_correction','abstain')},
                                      unavailable_by_criterion={cr:sum(not isinstance(r.get(cr),(int,float)) for r in filas) for cr in CRIT})
    tables['coverage'] = coverage
    script = Path(__file__).resolve()
    sources[str(script.relative_to(BASE))] = dict(sha256=hashlib.sha256(script.read_bytes()).hexdigest())
    # Validate everything before allocating a destination. mkdir is race-safe.
    output.mkdir(parents=True,exist_ok=False)
    (output/'tables.json').write_text(json.dumps(tables,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    write_csv(output/'coverage.csv',coverage)
    write_csv(output/'joined_cells.csv',filas)
    write_csv(output/'failures.csv',[{k:r[k] for k in ('qid','base_qid','generator_model','retrieval_condition','expected_behavior','error','failure_source')} for r in failures])
    for family in ('h6_niveles','h6_niveles_common','h6_pendientes','h6_explicitud','h6_explicitud_common','h6_interaccion','h5_separacion','h5_comparaciones','h5_separacion_common','h5_comparaciones_common'):
        records = [dict(scope=scope,**row) for scope in ('primary_content','sensitivity_all','sensitivity_abstain') for row in tables[scope][family]]
        write_csv(output/(family+'.csv'),records,compact=True)
    outputs = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.iterdir())}
    manifest = dict(sources=sources,outputs=outputs,python=platform.python_version(),
                    command='python scripts/analysis_capacity_v3.py --output-dir <fresh-directory-under-outputs/local_runs>',
                    no_model_calls=True,no_historical_writes=True)
    (output/'hash_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(tables['coverage_summary'],ensure_ascii=False,sort_keys=True))


if __name__ == "__main__":
    main()
