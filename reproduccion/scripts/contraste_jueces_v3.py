"""Contrasta los dos jueces de la evaluación de generación y prepara la auditoría.

Paso 1: deduplicar por la clave real de la celda —generador + estrategia + pregunta—.
       Las caídas y reanudaciones de la tarde pueden haber dejado filas repetidas, y sin
       esta comprobación los 604 de cada juez no serían 604 celdas distintas.
Paso 2: acuerdo entre jueces por criterio, con la misma lógica usada en la gradación de
       qrels (matriz, desacuerdos extremos, cola para revisión humana).
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

RUN = Path("outputs/local_runs/generation_scaling_v3")
JUECES = {"A": RUN / "eval_verdicts_v3.jsonl", "B": RUN / "eval_verdicts_v3_juezB.jsonl"}
CRITERIOS = ("faithfulness", "factual_correctness", "behavior_ok", "citations_ok")


def clave(d):
    """Identifica una celda por generador, estrategia y pregunta."""
    return (d.get("generator_model"), d.get("retrieval_condition"), d.get("qid"))


def cargar(path):
    """Lee los juicios conservando solo la primera fila de cada celda."""
    filas, vistas = [], {}
    for l in path.open(encoding="utf-8"):
        if not l.strip():
            continue
        d = json.loads(l)
        k = clave(d)
        if k in vistas:
            continue                      # duplicado: se conserva la primera
        vistas[k] = d
        filas.append(d)
    return filas


for j, p in JUECES.items():
    total = sum(1 for l in p.open(encoding="utf-8") if l.strip())
    filas = cargar(p)
    print(f"juez {j}: {total} filas → {len(filas)} celdas únicas ({total - len(filas)} duplicadas)")

a = {clave(d): d for d in cargar(JUECES["A"])}
b = {clave(d): d for d in cargar(JUECES["B"])}
comunes = sorted(set(a) & set(b))
print(f"celdas con doble juicio: {len(comunes)}\n")

print("acuerdo entre jueces por criterio")
print(f"  {'criterio':22s} {'acuerdo':>8s} {'kappa':>7s}")
discrepancias = defaultdict(list)
for c in CRITERIOS:
    iguales = sum(1 for k in comunes if a[k].get(c) == b[k].get(c))
    # kappa de Cohen: acuerdo observado frente al esperado por azar
    marg_a = Counter(a[k].get(c) for k in comunes)
    marg_b = Counter(b[k].get(c) for k in comunes)
    n = len(comunes)
    esperado = sum(marg_a[v] / n * marg_b[v] / n for v in set(marg_a) | set(marg_b))
    po = iguales / n
    kappa = (po - esperado) / (1 - esperado) if esperado < 1 else 1.0
    print(f"  {c:22s} {po:7.1%} {kappa:7.3f}")
    for k in comunes:
        if a[k].get(c) != b[k].get(c):
            discrepancias[k].append(c)

print(f"\nceldas con alguna discrepancia: {len(discrepancias)} / {len(comunes)}"
      f" ({len(discrepancias) / len(comunes):.1%})")

def num(v):
    """Convierte la puntuación a entero y usa cero si el valor no es convertible."""
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


extremas = [k for k, cs in discrepancias.items()
            if any(abs(num(a[k].get(c)) - num(b[k].get(c))) >= 2 for c in cs)]
print(f"desacuerdos extremos (diferencia ≥ 2): {len(extremas)}")

salida = RUN / "contraste_jueces_v3.jsonl"
with salida.open("w", encoding="utf-8") as out:
    for k in sorted(discrepancias):
        out.write(json.dumps({
            "generator_model": k[0], "retrieval_condition": k[1], "qid": k[2],
            "criterios": discrepancias[k], "extremo": k in extremas,
            "juezA": {c: a[k].get(c) for c in CRITERIOS},
            "juezB": {c: b[k].get(c) for c in CRITERIOS},
            "rationaleA": a[k].get("rationale"), "rationaleB": b[k].get("rationale"),
        }, ensure_ascii=False) + "\n")
print(f"\ndiscrepancias para auditoría humana → {salida}")
