"""Pruebas de la interfaz de la cola ciega de explicitud v2."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def _load_app():
    spec = importlib.util.spec_from_file_location(
        "explicitness_blind_review_app", ROOT / "scripts/explicitness_blind_review_app.py"
    )
    if spec is None or spec.loader is None:
        raise ImportError("app module not found")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class BlindReviewAppTests(unittest.TestCase):
    def setUp(self):
        self.app = _load_app()
        self.tmp = tempfile.TemporaryDirectory()
        self.work = Path(self.tmp.name) / "work.jsonl"
        self.chunks_path = ROOT / "data/processed/chunks_v1.jsonl"
        self.golden_path = ROOT / "data/golden/golden_set_pilot_v1_1.jsonl"
        self.pairs_path = ROOT / "data/golden/variants/explicitness_pairs_v1_consolidated.jsonl"
        self.frozen = ROOT / "outputs/explicitness_v2/pools/blind_review_queue.jsonl"

    def tearDown(self):
        self.tmp.cleanup()

    def test_frozen_pool_shape(self):
        rows = self.app.load_jsonl(self.frozen)
        self.assertEqual(len(rows), 122)
        for row in rows:
            self.assertIsNone(row.get("human_decision"))
            self.assertEqual(row.get("annotation_status"), "pending")
            self.assertEqual(row.get("reviews"), [])
            self.assertIn(row.get("explicitness"), {"explicit", "implicit"})
            for key in ("pool_id", "qid", "base_qid", "chunk_id", "retrieval_text"):
                self.assertTrue(row.get(key), key)

    def test_work_copy_created_and_frozen_untouched(self):
        import hashlib

        before = hashlib.sha256(self.frozen.read_bytes()).hexdigest()
        info = self.app.prepare_work_copy(self.frozen, self.work)
        self.assertTrue(info["created"])
        self.assertEqual(info["units"], 122)
        after = hashlib.sha256(self.frozen.read_bytes()).hexdigest()
        self.assertEqual(before, after)
        # segunda llamada reanuda sin recrear
        info2 = self.app.prepare_work_copy(self.frozen, self.work)
        self.assertFalse(info2["created"])

    def test_work_copy_refuses_predecided_source(self):
        rows = self.app.load_jsonl(self.frozen)
        rows[0]["human_decision"] = {"grade": 2}
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            poisoned = Path(handle.name)
        try:
            with self.assertRaises(ValueError):
                self.app.prepare_work_copy(poisoned, self.work)
        finally:
            poisoned.unlink()

    def test_context_covers_every_queue_qid(self):
        context = self.app.load_golden_context(self.golden_path, self.pairs_path)
        rows = self.app.load_jsonl(self.frozen)
        for row in rows:
            self.assertIn(row["qid"], context, row["qid"])
            info = context[row["qid"]]
            if row["explicitness"] == "implicit":
                self.assertEqual(info["question"], row["question"])

    def test_state_and_decision_roundtrip(self):
        context = self.app.load_golden_context(self.golden_path, self.pairs_path)
        self.app.prepare_work_copy(self.frozen, self.work)
        state = self.app.build_review_state(self.work, self.chunks_path, context)
        self.assertEqual(state["summary"]["total"], 122)
        self.assertEqual(state["summary"]["reviewed"], 0)
        first = state["candidates"][0]
        self.assertTrue(first["chunk_text"])
        self.assertTrue(first["question"])
        # guardar decisión
        saved = self.app.save_human_decision(
            self.work, first["pool_id"], 2, True, "evidencia directa", "andres"
        )
        self.assertEqual(saved["grade"], 2)
        self.assertTrue(saved["canonical"])
        # canónica sin grado 2 -> rechazo
        with self.assertRaises(ValueError):
            self.app.save_human_decision(
                self.work, first["pool_id"], 1, True, "", "andres"
            )
        # grado inválido -> rechazo
        with self.assertRaises(ValueError):
            self.app.save_human_decision(
                self.work, first["pool_id"], 3, None, "", "andres"
            )
        state = self.app.build_review_state(self.work, self.chunks_path, context)
        self.assertEqual(state["summary"]["reviewed"], 1)
        self.assertEqual(state["summary"]["pending"], 121)
        updated = [c for c in state["candidates"] if c["pool_id"] == first["pool_id"]][0]
        self.assertEqual(updated["grade"], 2)
        self.assertEqual(updated["note"], "evidencia directa")
        self.assertEqual(updated["reviewed_at"], saved["reviewed_at"])
        # dejar pendiente de nuevo
        self.app.save_human_decision(self.work, first["pool_id"], None, None, "", "andres")
        state = self.app.build_review_state(self.work, self.chunks_path, context)
        self.assertEqual(state["summary"]["reviewed"], 0)

    def test_html_contains_core_controls(self):
        html = self.app.render_app_html()
        for fragment in (
            "Cola ciega de explicitud",
            "id=\"grade-0\"",
            "id=\"grade-2\"",
            "Guardar y siguiente",
            "implícita",
            "/api/decision",
        ):
            self.assertIn(fragment, html)


if __name__ == "__main__":
    unittest.main()
