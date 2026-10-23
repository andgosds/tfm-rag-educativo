"""Pruebas del constructor de qrels v2 de la campaña de explicitud."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
import tempfile
import unittest


def _load_module():
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("build_explicitness_qrels", root / "scripts" / "build_explicitness_qrels.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_jsonl(path: Path, rows) -> Path:
    """Write either a single JSON object (dict) or JSONL rows (list/iterable)."""
    if isinstance(rows, dict):
        path.write_text(json.dumps(rows, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    return path


class BuildExplicitnessQrelsTests(unittest.TestCase):
    def setUp(self):
        self.mod = _load_module()
        self.tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmp.name)
        self.reuse = _write_jsonl(self.tmp_path / "reuse.jsonl", {
            "adjudications": [{
                "pool_id": "q-v1-001__explicit::c:1", "qid": "q-v1-001__explicit",
                "base_qid": "q-v1-001", "explicitness": "explicit", "chunk_id": "c:1",
                "human_decision": {"decision": "confirm_reuse"},
            }],
            "grade_1_2_proposals": [{
                "pool_id": "q-v1-002__implicit::c:2", "qid": "q-v1-002__implicit",
                "base_qid": "q-v1-002", "explicitness": "implicit", "chunk_id": "c:2",
                "human_decision": {"decision": "reuse_with_grade_adjustment", "final_grade": 1},
            }],
        })
        self.blind = _write_jsonl(self.tmp_path / "blind.jsonl", [
            {"pool_id": "q-v1-001__explicit::c:3", "qid": "q-v1-001__explicit", "base_qid": "q-v1-001",
             "explicitness": "explicit", "chunk_id": "c:3", "human_decision": {"grade": 2, "canonical": False}},
            {"pool_id": "q-v1-001__explicit::c:4", "qid": "q-v1-001__explicit", "base_qid": "q-v1-001",
             "explicitness": "explicit", "chunk_id": "c:4", "human_decision": {"grade": 0, "canonical": False}},
        ])
        self.pool = _write_jsonl(self.tmp_path / "pool.jsonl", [
            {"pool_id": pid} for pid in (
                "q-v1-001__explicit::c:1", "q-v1-001__explicit::c:3", "q-v1-001__explicit::c:4",
                "q-v1-002__implicit::c:2",
            )
        ])
        self.golden = _write_jsonl(self.tmp_path / "golden.jsonl", [{
            "qid": "q-v1-001",
            "evidence": [{"chunk_id": "c:1", "relevance_grade": 2, "is_canonical": True}],
        }])
        self.pooled = self.tmp_path / "pooled.tsv"
        self.pooled.write_text("q-v1-002\t0\tc:2\t2\n", encoding="utf-8")
        self.kwargs = dict(
            reuse_book_path=self.reuse,
            blind_work_path=self.blind,
            technical_pool_path=self.pool,
            golden_path=self.golden,
            pooled_qrels_path=self.pooled,
        )

    def tearDown(self):
        self.tmp.cleanup()

    def _build(self, **overrides):
        return self.mod.build_explicitness_qrels(**{**self.kwargs, **overrides})

    def test_builds_qrels_with_expected_grades(self):
        out = self.tmp_path / "qrels.tsv"
        report = self._build(output_qrels_path=out, provenance_path=self.tmp_path / "p.jsonl", report_path=self.tmp_path / "r.json")
        rows = {}
        for line in out.read_text().splitlines():
            qid, _, chunk_id, grade = line.split("\t")
            rows[(qid, chunk_id)] = grade
        self.assertEqual(rows[("q-v1-001__explicit", "c:1")], "2")
        self.assertEqual(rows[("q-v1-001__explicit", "c:3")], "2")
        self.assertEqual(rows[("q-v1-002__implicit", "c:2")], "2")
        self.assertNotIn("c:4", {c for _, c in rows})
        self.assertEqual(report["qrel_rows_total"], 3)
        self.assertEqual(report["decided_units_total"], 4)

    def test_coverage_mismatch_raises(self):
        short = _write_jsonl(self.tmp_path / "short.jsonl", [{"pool_id": "q-v1-001__explicit::c:1"}])
        with self.assertRaises(ValueError):
            self._build(technical_pool_path=short, output_qrels_path=self.tmp_path / "q.tsv",
                        provenance_path=self.tmp_path / "p.jsonl", report_path=self.tmp_path / "r.json")

    def test_blind_without_grade_raises(self):
        bad = _write_jsonl(self.tmp_path / "bad.jsonl", [
            {"pool_id": "q-v1-001__explicit::c:3", "qid": "q-v1-001__explicit", "base_qid": "q-v1-001",
             "explicitness": "explicit", "chunk_id": "c:3", "human_decision": {"grade": None}},
        ])
        with self.assertRaises(ValueError):
            self._build(blind_work_path=bad, output_qrels_path=self.tmp_path / "q.tsv",
                        provenance_path=self.tmp_path / "p.jsonl", report_path=self.tmp_path / "r.json")

    def test_reuse_unit_without_historic_grade_raises(self):
        golden2 = _write_jsonl(self.tmp_path / "golden2.jsonl", [{
            "qid": "q-v1-001", "evidence": [{"chunk_id": "OTHER", "relevance_grade": 2, "is_canonical": False}],
        }])
        with self.assertRaises(ValueError):
            self._build(golden_path=golden2, output_qrels_path=self.tmp_path / "q.tsv",
                        provenance_path=self.tmp_path / "p.jsonl", report_path=self.tmp_path / "r.json")

    def test_duplicate_qid_chunk_raises(self):
        extra_blind = _write_jsonl(self.tmp_path / "extra.jsonl", [
            {"pool_id": "q-v1-001__explicit::c:9", "qid": "q-v1-001__explicit", "base_qid": "q-v1-001",
             "explicitness": "explicit", "chunk_id": "c:1", "human_decision": {"grade": 1, "canonical": False}},
        ])
        pool2 = _write_jsonl(self.tmp_path / "pool2.jsonl", [
            {"pool_id": pid} for pid in (
                "q-v1-001__explicit::c:1", "q-v1-001__explicit::c:3", "q-v1-001__explicit::c:4",
                "q-v1-002__implicit::c:2", "q-v1-001__explicit::c:9",
            )
        ])
        with self.assertRaises(ValueError):
            self._build(blind_work_path=extra_blind, technical_pool_path=pool2,
                        output_qrels_path=self.tmp_path / "q.tsv",
                        provenance_path=self.tmp_path / "p.jsonl", report_path=self.tmp_path / "r.json")

    def test_lote3_downgrade_overrides_historic_grade(self):
        reuse2 = _write_jsonl(self.tmp_path / "reuse2.jsonl", {
            "adjudications": [],
            "grade_1_2_proposals": [{
                "pool_id": "q-v1-002__implicit::openstax_intro_stats_2e:9.4:chunk-006",
                "qid": "q-v1-002__implicit", "base_qid": "q-v1-002",
                "explicitness": "implicit", "chunk_id": "openstax_intro_stats_2e:9.4:chunk-006",
                "human_decision": {"decision": "reuse_with_grade_adjustment", "final_grade": 1},
            }],
        })
        pooled2 = self.tmp_path / "pooled2.tsv"
        # Historic adjudication said grade 2 for this chunk under the base question.
        pooled2.write_text("q-v1-002\t0\topenstax_intro_stats_2e:9.4:chunk-006\t2\n", encoding="utf-8")
        pool2 = _write_jsonl(self.tmp_path / "pool2.jsonl", [{"pool_id": "q-v1-002__implicit::openstax_intro_stats_2e:9.4:chunk-006"}])
        out = self.tmp_path / "qrels2.tsv"
        self._build(
            reuse_book_path=reuse2, blind_work_path=_write_jsonl(self.tmp_path / "empty_blind.jsonl", []),
            technical_pool_path=pool2, pooled_qrels_path=pooled2,
            output_qrels_path=out, provenance_path=self.tmp_path / "p2.jsonl", report_path=self.tmp_path / "r2.json",
        )
        self.assertIn("\topenstax_intro_stats_2e:9.4:chunk-006\t1\n", out.read_text())

    def test_delegated_provenance_is_not_human(self):
        rows = self.mod._load_jsonl(self.blind)
        for row in rows:
            row["human_decision"]["reviewer"] = "assistant"
            row["decision_provenance"] = {"adjudication_mode": "assistant_under_explicit_user_delegation", "historical_reviewer": "andres"}
        _write_jsonl(self.blind, rows)
        self._build(output_qrels_path=self.tmp_path / "q.tsv", provenance_path=self.tmp_path / "p.jsonl", report_path=self.tmp_path / "r.json")
        row = next(x for x in self.mod._load_jsonl(self.tmp_path / "p.jsonl") if x["decision_source"] == "blind_review")
        self.assertEqual(row["reviewer"], "assistant")
        self.assertEqual(row["decision_provenance"]["historical_reviewer"], "andres")

    def test_grade0_units_only_audited(self):
        out = self.tmp_path / "qrels.tsv"
        report = self._build(output_qrels_path=out, provenance_path=self.tmp_path / "p.jsonl", report_path=self.tmp_path / "r.json")
        self.assertEqual(report["audited_grade_0_count"], 1)
        self.assertNotIn("c:4", out.read_text())


if __name__ == "__main__":
    unittest.main()
