"""Análisis descriptivo pareado explícito-implícito de recuperación v3.

Para cada método y métrica se calcula la **diferencia emparejada** explícita − implícita
dentro de cada pareja, y se somete a un **test de signos** exacto. La unidad de análisis es
la pareja, no la formulación: son 26 diferencias, no 52 observaciones.

No asigna ni renombra hipótesis. Holm se añade como corrección post-hoc transparente,
en dos familias separadas: Recall/nDCG principales y Precision/MRR complementarias.
Los contrastes descriptivos entre penalizaciones no declaran confirmación ni equivalencia.

El test de signos se elige sobre una *t* de Student porque las diferencias por pregunta son
discretas y gruesas —Recall con poca evidencia conocida solo admite unos pocos valores—,
y la normalidad de esas diferencias no está garantizada con 26 casos.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from types import SimpleNamespace

from evaluate_retrieval_v3 import sha256, write_csv
from output_safety import guard_cli_outputs

METRICS = ("recall", "precision", "mrr", "ndcg")


def holm_adjust(p_values: list[float]) -> list[float]:
    """Holm step-down adjusted p-values, restored to the input order."""
    adjusted = [0.0] * len(p_values)
    running_max = 0.0
    for rank, index in enumerate(sorted(range(len(p_values)), key=lambda i: (p_values[i], i))):
        running_max = max(running_max, (len(p_values) - rank) * p_values[index])
        adjusted[index] = min(1.0, running_max)
    return adjusted


def sign_test(pos: int, neg: int) -> float:
    """p exacta bilateral para un test de signos, ignorando empates."""
    n = pos + neg
    if n == 0:
        return 1.0
    tail = sum(math.comb(n, k) for k in range(0, min(pos, neg) + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def read_metrics(path: Path) -> list[dict]:
    """Lee las métricas CSV y valida sus valores y denominadores numéricos."""
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["k"] = int(r["k"])
        r["n_relevant"] = int(r["n_relevant"])
        for m in METRICS:
            r[m] = float(r[m])
            if not math.isfinite(r[m]) or not 0 <= r[m] <= 1:
                raise ValueError(f"invalid {m}: {r[m]}")
    return rows


def compute_contrasts(rows: list[dict], bases: list[str]) -> tuple[list[dict], list[dict]]:
    """Calcula diferencias pareadas, contrastes de signos y ajustes Holm por familia."""
    by = {(r["method"], r["base_qid"], r["explicitness"], r["k"]): r for r in rows}
    if len(by) != len(rows):
        raise ValueError("duplicate method/base/formulation/k metric cell")
    methods = sorted({r["method"] for r in rows})
    if not bases:
        raise ValueError("no paired base questions")
    out_rows = []
    per_base = []
    for k in (5, 10):
        for method in methods:
            for m in METRICS:
                difs = []
                for b in bases:
                    e = by.get((method, b, "explicit", k))
                    i = by.get((method, b, "implicit", k))
                    if e is None or i is None:
                        raise ValueError(f"incomplete pair: {method}/{b}/{k}")
                    if e["n_relevant"] != i["n_relevant"]:
                        raise ValueError("formulations must share the base-question grade-2 denominator")
                    dif = e[m] - i[m]
                    difs.append(dif)
                    per_base.append(dict(method=method, k=k, metric=m, base_qid=b,
                                         explicit=e[m], implicit=i[m], diff_explicit_minus_implicit=dif))
                pos = sum(1 for d in difs if d > 0)
                neg = sum(1 for d in difs if d < 0)
                emp = sum(1 for d in difs if d == 0)
                media = sum(difs) / len(difs)
                p = sign_test(pos, neg)
                out_rows.append(dict(method=method, k=k, metric=m, mean_diff=media,
                                     pos=pos, neg=neg, ties=emp, p_sign=p, n_pairs=len(difs),
                                     n_effective=pos + neg,
                                     family="primary" if m in ("recall", "ndcg") else "complementary"))
    for family in ("primary", "complementary"):
        # Cada familia se ajusta por separado, sin mezclar métricas complementarias.
        group = [r for r in out_rows if r["family"] == family]
        for row, adjusted in zip(group, holm_adjust([r["p_sign"] for r in group])):
            row["family_size"] = len(group)
            row["p_holm"] = adjusted
    return out_rows, per_base


def method_effect_differences(per_base: list[dict], cohort: str) -> list[dict]:
    """Descriptive paired differences of explicitness effects; no inferential decision."""
    by = {(r["method"], r["base_qid"], r["k"], r["metric"]): r["diff_explicit_minus_implicit"] for r in per_base}
    methods = sorted({r["method"] for r in per_base})
    bases = sorted({r["base_qid"] for r in per_base})
    result = []
    for a, b in combinations(methods, 2):
        for k in (5, 10):
            for metric in METRICS:
                deltas = [by[(a, base, k, metric)] - by[(b, base, k, metric)] for base in bases]
                pos = sum(d > 0 for d in deltas)
                neg = sum(d < 0 for d in deltas)
                result.append(dict(cohort=cohort, method_a=a, method_b=b, k=k, metric=metric,
                                   mean_effect_a_minus_b=sum(deltas) / len(deltas),
                                   n_pairs=len(deltas), pos=pos, neg=neg, ties=len(deltas) - pos - neg,
                                   n_effective=pos + neg))
    return result


def main() -> int:
    """Exporta los contrastes v3 y la sensibilidad restringida a parejas con grado 2."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--metrics-dir", type=Path, required=True)
    ap.add_argument("--historical-metrics-dir", type=Path,
                    help="Optional frozen per_query.csv for before/after reconstruction (read only).")
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    guard_cli_outputs(SimpleNamespace(output_root=args.output_dir), script="paired_explicitness_v3")
    source = args.metrics_dir / "per_query.csv"
    rows = read_metrics(source)
    methods = sorted({r["method"] for r in rows})
    if set(methods) != {"bm25", "dense", "rrf", "rerank"}:
        raise ValueError("v3 families require exactly four methods")
    bases = sorted({r["base_qid"] for r in rows})
    eligible = sorted({r["base_qid"] for r in rows if r["n_relevant"] > 0})
    if any(len({r["n_relevant"] for r in rows if r["base_qid"] == base}) != 1 for base in bases):
        raise ValueError("grade-2 denominator differs across methods or cuts")
    all_tests, per_base = compute_contrasts(rows, bases)
    sensitivity, eligible_per_base = compute_contrasts(rows, eligible)
    if len(all_tests) != 32 or len(sensitivity) != 32:
        raise ValueError("expected exactly 32 tests per cohort")
    effects = method_effect_differences(per_base, "all_pairs") + method_effect_differences(eligible_per_base, "grade2_eligible")
    inputs = {source.name: sha256(source)}
    upstream_report = args.metrics_dir / "retrieval_correction_report.json"
    upstream = None
    if upstream_report.exists():
        inputs[upstream_report.name] = sha256(upstream_report)
        upstream = json.loads(upstream_report.read_text(encoding="utf-8"))
    before_after = []
    if args.historical_metrics_dir:
        historic = args.historical_metrics_dir / "per_query.csv"
        inputs["historical_per_query.csv"] = sha256(historic)
        legacy = read_metrics(historic)
        if {(r["method"], r["base_qid"], r["explicitness"], r["k"]) for r in legacy} != {(r["method"], r["base_qid"], r["explicitness"], r["k"]) for r in rows}:
            raise ValueError("historical metric coverage differs")
        legacy_tests, _ = compute_contrasts(legacy, bases)
        lookup = {(r["method"], r["k"], r["metric"]): r for r in legacy_tests}
        for row in all_tests:
            old = lookup[(row["method"], row["k"], row["metric"])]
            record = dict(method=row["method"], k=row["k"], metric=row["metric"], n_pairs=len(bases))
            for field in ("mean_diff", "pos", "neg", "ties", "n_effective", "p_sign", "p_holm"):
                record["before_" + field] = old[field]
                record["after_" + field] = row[field]
            before_after.append(record)
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=False)
    write_csv(out / "paired_explicitness_v3.csv", all_tests)
    write_csv(out / "paired_grade2_eligible.csv", sensitivity)
    write_csv(out / "paired_differences_by_base.csv", per_base)
    write_csv(out / "between_method_effect_differences.csv", effects)
    if before_after:
        write_csv(out / "before_after_paired.csv", before_after)
    report = dict(schema_version=1, correction="R07: effective n, exact signs and explicit Holm families",
                  unit="one explicit-minus-implicit difference within each independent base question",
                  direction="explicit - implicit; positive means explicit formulation scores higher",
                  sign_test="exact two-sided Binomial(n_effective, 0.5); min(1, twice smaller inclusive tail); exact zero ties discarded",
                  multiplicity_status="post-hoc analytical correction, not pre-registered; families selected after results were observed",
                  families={name: dict(size=16, metrics=metrics, methods=methods, k=[5, 10])
                            for name, metrics in (("primary", ["recall", "ndcg"]), ("complementary", ["precision", "mrr"]))},
                  sensitivity_multiplicity="same two families adjusted separately on grade2-eligible cohort; diagnostic sensitivity, not an additional confirmatory analysis",
                  cohorts=dict(all_pairs=dict(n_base=len(bases), base_qids=bases),
                               grade2_eligible=dict(n_base=len(eligible), base_qids=eligible)),
                  counts=dict(all_pairs_tests=len(all_tests), grade2_eligible_tests=len(sensitivity),
                              per_base_differences=len(per_base), descriptive_between_method_effects=len(effects)),
                  all_pairs_tests=all_tests, grade2_eligible_tests=sensitivity,
                  before_after=before_after, between_method_effect_differences=effects,
                  between_method_scope="paired effect_A - effect_B across the SAME base questions; descriptive only, no p-values or claims from significance differences",
                  interpretation="No hypothesis confirmation, equivalence or robustness is established by these tables.",
                  upstream_metric_contract=upstream, inputs=inputs,
                  outputs={p.name: sha256(p) for p in sorted(out.iterdir())})
    (out / "paired_correction_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"all pairs: {len(bases)} | grade2 eligible: {len(eligible)} | tests: 32 + 32 sensitivity")
    for row in all_tests:
        print(f"{row['method']:8s} @{row['k']} {row['metric']:9s} delta={row['mean_diff']:+.6f} "
              f"{row['pos']}/{row['neg']}/{row['ties']} n_eff={row['n_effective']} "
              f"p={row['p_sign']:.6f} p_Holm={row['p_holm']:.6f}")
    print(f"salidas: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
