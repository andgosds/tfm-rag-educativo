"""Regression tests for R01/R07; local fixtures only, no model calls."""
from __future__ import annotations

import math
import json
import csv
import subprocess
import tempfile
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import evaluate_retrieval_v3 as evaluator
import paired_explicitness_v3 as paired


class GlobalIdealTests(unittest.TestCase):
    def test_unretrieved_grade_two_prevents_perfect_ndcg(self):
        # The retrieved grade-1 passage is not the global ideal: a grade-2
        # passage exists outside the run. First show the old semantic defect.
        metric = evaluator.metrics_for([1], 1, 1, qrel_grades=[1, 2])
        self.assertAlmostEqual(metric["ndcg"], 1 / 3)
        self.assertEqual(metric["recall"], 0)
        self.assertEqual(metric["mrr"], 0)

    def test_identical_qrels_give_methods_identical_ideal(self):
        qrels = [2, 2, 1]
        ideal = 3 + 3 / math.log2(3)
        for ranking in ([1], [2, 1], [0, 2]):
            dcg = sum((2 ** grade - 1) / math.log2(i + 2) for i, grade in enumerate(ranking[:2]))
            self.assertAlmostEqual(evaluator.metrics_for(ranking, 2, 2, qrel_grades=qrels)["ndcg"], dcg / ideal)

    def test_no_grade2_keeps_legacy_zero_but_ndcg_uses_grade_one(self):
        result = evaluator.metrics_for([1], 5, 0, qrel_grades=[1, 1])
        self.assertEqual(result["recall"], 0)
        self.assertEqual(result["mrr"], 0)
        self.assertEqual(result["precision"], 0)
        self.assertAlmostEqual(result["ndcg"], 1 / (1 + 1 / math.log2(3)))

    def test_empty_and_zero_gain_ideals_score_zero(self):
        for qrels in ([], [0, 0]):
            self.assertEqual(evaluator.metrics_for([], 5, 0, qrel_grades=qrels),
                             dict(recall=0, precision=0, mrr=0, ndcg=0))

    def test_real_frozen_runs_reproduce_correct_global_ndcg10(self):
        run = ROOT / "outputs/local_runs/explicitness_v3"
        qrels = evaluator.load_jsonl(run / "qrels_final_v3.jsonl")
        known = {}
        for row in qrels:
            known.setdefault(row["base_qid"], {})[row["chunk_id"]] = row["grade"]
        expected = dict(bm25=0.7062394410919206, dense=0.6772392861175022,
                        rrf=0.7282507284720694, rerank=0.7349125143462774)
        for method, value in expected.items():
            grouped = {}
            for row in evaluator.load_jsonl(run / "runs" / f"explicitness_v3_{method}.jsonl"):
                grouped.setdefault(row["qid"], []).append(row)
            scores = []
            for rows in grouped.values():
                rows.sort(key=lambda r: r["rank"])
                qr = known[rows[0]["base_qid"]]
                scores.append(evaluator.metrics_for([qr.get(r["chunk_id"], 0) for r in rows], 10,
                                                    sum(g == 2 for g in qr.values()),
                                                    qrel_grades=list(qr.values()))["ndcg"])
            self.assertEqual(len(scores), 52)
            self.assertAlmostEqual(sum(scores) / len(scores), value, places=14)


class HolmTests(unittest.TestCase):
    def test_stepdown_adjustment_is_monotone_and_keeps_input_order(self):
        self.assertEqual(paired.holm_adjust([0.04, 0.001, 0.03, 0.5]), [0.09, 0.004, 0.09, 0.5])

    def test_exact_sign_test_convention_ignores_zero_effective_pairs(self):
        self.assertEqual(paired.sign_test(0, 0), 1)
        self.assertEqual(paired.sign_test(3, 3), 1)
        self.assertEqual(paired.sign_test(4, 0), 0.125)
        self.assertEqual(paired.sign_test(0, 4), 0.125)
        self.assertEqual(paired.holm_adjust([1, 1]), [1, 1])

    def test_missing_and_duplicate_pairs_are_not_silently_averaged(self):
        row = dict(method="bm25", base_qid="q", explicitness="explicit", k=5,
                   n_relevant=1, recall=0, precision=0, mrr=0, ndcg=0)
        with self.assertRaisesRegex(ValueError, "incomplete pair"):
            paired.compute_contrasts([row], ["q"])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            paired.compute_contrasts([row, row], ["q"])


class SafeOutputTests(unittest.TestCase):
    def test_paired_cli_emits_32_tests_two_explicit_families_and_sensitivity(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "outputs/local_runs") as tmp:
            root = Path(tmp)
            metrics_dir = root / "metrics"
            metrics_dir.mkdir()
            rows = []
            for method in ("bm25", "dense", "rrf", "rerank"):
                for k in (5, 10):
                    for base, n_rel in (("eligible", 2), ("no_grade2", 0)):
                        for side in ("explicit", "implicit"):
                            score = 0.6 if side == "explicit" else 0.4
                            rows.append(dict(method=method, k=k, base_qid=base, explicitness=side,
                                             n_relevant=n_rel, recall=score if n_rel else 0,
                                             precision=score if n_rel else 0, mrr=score if n_rel else 0,
                                             ndcg=score))
            with (metrics_dir / "per_query.csv").open("w", newline="") as fh:
                writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
                writer.writeheader(); writer.writerows(rows)
            output = root / "paired"
            cmd = [sys.executable, str(ROOT / "scripts/paired_explicitness_v3.py"),
                   "--metrics-dir", str(metrics_dir), "--output-dir", str(output)]
            first = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            report = json.loads((output / "paired_correction_report.json").read_text())
            self.assertEqual(report["counts"]["all_pairs_tests"], 32)
            self.assertEqual(report["counts"]["grade2_eligible_tests"], 32)
            self.assertEqual(report["families"]["primary"]["size"], 16)
            self.assertEqual(report["families"]["complementary"]["size"], 16)
            self.assertIn("post-hoc", report["multiplicity_status"])
            with (output / "paired_explicitness_v3.csv").open(newline="") as fh:
                records = list(csv.DictReader(fh))
            recall = next(r for r in records if r["metric"] == "recall")
            ndcg = next(r for r in records if r["metric"] == "ndcg")
            self.assertEqual((int(recall["pos"]), int(recall["neg"]), int(recall["ties"]), int(recall["n_effective"])), (1, 0, 1, 1))
            self.assertEqual((int(ndcg["pos"]), int(ndcg["neg"]), int(ndcg["ties"]), int(ndcg["n_effective"])), (2, 0, 0, 2))
            before = {p.name: p.read_bytes() for p in output.iterdir()}
            again = subprocess.run(cmd, capture_output=True, text=True)
            self.assertNotEqual(again.returncode, 0)
            self.assertEqual(before, {p.name: p.read_bytes() for p in output.iterdir()})
            second = root / "paired_second"
            repeated = subprocess.run(cmd[:-1] + [str(second)], capture_output=True, text=True)
            self.assertEqual(repeated.returncode, 0, repeated.stderr)
            self.assertEqual(before, {p.name: p.read_bytes() for p in second.iterdir()})

    def test_evaluator_requires_fresh_output_and_reports_cohorts(self):
        # CLI fixtures must live under the real allowlisted local_runs root.
        with tempfile.TemporaryDirectory(dir=ROOT / "outputs/local_runs") as tmp:
            root = Path(tmp)
            runs = root / "input/runs"
            runs.mkdir(parents=True)
            qrels = root / "qrels.jsonl"
            qrels.write_text(json.dumps({"base_qid": "q", "chunk_id": "best", "grade": 2}) + "\n"
                             + json.dumps({"base_qid": "q", "chunk_id": "context", "grade": 1}) + "\n")
            rows = [{"qid": "q__" + side, "base_qid": "q", "explicitness": side,
                     "chunk_id": "context", "rank": 1} for side in ("explicit", "implicit")]
            (runs / "explicitness_v3_bm25.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
            output = root / "new"
            cmd = [sys.executable, str(ROOT / "scripts/evaluate_retrieval_v3.py"),
                   "--run-dir", str(runs.parent), "--qrels", str(qrels), "--methods", "bm25"]
            absent = subprocess.run(cmd, capture_output=True, text=True)
            self.assertNotEqual(absent.returncode, 0)
            self.assertFalse((runs.parent / "retrieval_metrics_v3").exists())
            first = subprocess.run(cmd + ["--output-dir", str(output)], capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            report = json.loads((output / "retrieval_correction_report.json").read_text())
            self.assertEqual(report["cohorts"]["all_pairs"]["n_base"], 1)
            self.assertEqual(report["cohorts"]["grade2_eligible"]["n_base"], 1)
            before = {p.name: p.read_bytes() for p in output.iterdir()}
            again = subprocess.run(cmd + ["--output-dir", str(output)], capture_output=True, text=True)
            self.assertNotEqual(again.returncode, 0)
            self.assertEqual(before, {p.name: p.read_bytes() for p in output.iterdir()})
            empty = root / "empty"
            empty.mkdir()
            rejected = subprocess.run(cmd + ["--output-dir", str(empty)], capture_output=True, text=True)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertFalse(list(empty.iterdir()))
            second = root / "second"
            repeated = subprocess.run(cmd + ["--output-dir", str(second)], capture_output=True, text=True)
            self.assertEqual(repeated.returncode, 0, repeated.stderr)
            self.assertEqual(before, {p.name: p.read_bytes() for p in second.iterdir()})


if __name__ == "__main__":
    unittest.main()
