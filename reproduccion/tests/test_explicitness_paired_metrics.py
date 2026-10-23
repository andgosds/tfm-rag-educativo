"""Pruebas de las métricas emparejadas de explicitud v2."""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import tempfile
import unittest


def _load_module():
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("explicitness_paired_metrics", root / "scripts" / "explicitness_paired_metrics.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PairedMetricsTests(unittest.TestCase):
    def setUp(self):
        self.mod = _load_module()
        self.tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_evaluate_ranking_definitions(self):
        qrels = {"a": 2, "b": 1, "e": 2}
        # Grade-1 chunks do NOT count for recall/mrr; nDCG keeps the graded scale.
        r = self.mod.evaluate_ranking(["b", "a"], qrels, k=2)
        self.assertEqual(r["recall"], 0.5)  # 1 of 2 grade-2 docs in top-2
        self.assertEqual(r["mrr"], 0.5)  # first grade-2 hit at rank 2
        # DCG(grades [1,2]) = 1/log2(2) + 3/log2(3); IDCG(ideal [2,2]) = 3/log2(2) + 3/log2(3)
        self.assertAlmostEqual(r["ndcg"], (1 / 1 + 3 / math.log2(3)) / (3 / 1 + 3 / math.log2(3)))
        self.assertTrue(0 < r["ndcg"] < 1)

    def test_evaluate_ranking_no_grade2_returns_none(self):
        r = self.mod.evaluate_ranking(["a"], {"a": 1}, k=1)
        self.assertIsNone(r["recall"])
        self.assertIsNone(r["mrr"])

    def test_load_rankings_orders_by_rank(self):
        runs = self.tmp_path / "runs"
        runs.mkdir()
        lines = [
            {"qid": "q", "chunk_id": "c2", "rank": 2},
            {"qid": "q", "chunk_id": "c1", "rank": 1},
        ]
        for method in ("bm25", "dense", "rrf", "rerank"):
            for r in lines:
                r["method"] = method
            (runs / f"explicitness_v2_{method}.jsonl").write_text(
                "\n".join(json.dumps(r) for r in lines) + "\n", encoding="utf-8")
        rankings = self.mod.load_rankings(runs)
        self.assertEqual(rankings["bm25"]["q"], ["c1", "c2"])

    def test_compute_metrics_unknown_qid_raises(self):
        qrels = {"other": {"a": 2}}
        rankings = {"bm25": {"q": ["a"]}}
        with self.assertRaises(ValueError):
            self.mod.compute_metrics(rankings, qrels)

    def test_paired_differences_sign_and_means(self):
        rankings = {
            "bm25": {f"q-v1-001__explicit": ["a", "b"], "q-v1-001__implicit": ["b", "a"]},
        }
        qrels = {"q-v1-001__explicit": {"a": 2}, "q-v1-001__implicit": {"a": 2}}
        self.mod.BASE_QIDS = (1,)
        metrics = self.mod.compute_metrics(rankings, qrels)
        world = self.mod.paired_differences(metrics)
        row = [r for r in world["per_question"] if r["metric"] == "mrr@10"][0]
        self.assertEqual(row["explicit"], 1.0)
        self.assertEqual(row["implicit"], 0.5)
        self.assertAlmostEqual(row["diff_implicit_minus_explicit"], -0.5)
        mean_row = [m for m in world["means"] if m["metric"] == "mrr@10"][0]
        self.assertAlmostEqual(mean_row["mean_diff_implicit_minus_explicit"], -0.5)

    def test_full_pipeline_on_fixture(self):
        import csv
        qr = self.tmp_path / "qrels.tsv"
        qr.write_text("q-v1-001__explicit\t0\ta\t2\nq-v1-001__implicit\t0\ta\t2\n", encoding="utf-8")
        runs = self.tmp_path / "runs"
        runs.mkdir()
        for method in ("bm25", "dense", "rrf", "rerank"):
            (runs / f"explicitness_v2_{method}.jsonl").write_text(
                json.dumps({"qid": "q-v1-001__explicit", "chunk_id": "a", "rank": 1, "method": method}) + "\n"
                + json.dumps({"qid": "q-v1-001__implicit", "chunk_id": "a", "rank": 2, "method": method}) + "\n",
                encoding="utf-8")
        report = self.mod.run_paired_metrics(
            runs_dir=runs, qrels_path=qr,
            output_csv_path=self.tmp_path / "out.csv",
            output_json_path=self.tmp_path / "out.json",
            report_path=self.tmp_path / "rep.json",
        )
        rows = list(csv.DictReader((self.tmp_path / "out.csv").open()))
        self.assertEqual(len(rows), 4 * 1 * 6)  # 4 methods x 1 base qid x 3 metrics x 2 k
        self.assertEqual(report["qrels_sha256"], self.mod._sha256(qr))


if __name__ == "__main__":
    unittest.main()
