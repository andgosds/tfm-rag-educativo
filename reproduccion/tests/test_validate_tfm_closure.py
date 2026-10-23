from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]


def test_closure_rebuilds_frozen_results_without_inference_or_mutation():
    script = ROOT / "scripts/validate_tfm_closure.py"
    assert script.exists(), "closure verifier is missing"
    spec = importlib.util.spec_from_file_location("validate_tfm_closure", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    report, products = module.build_report(ROOT, check_tables=False)
    assert report["counts"]["responses"] == 88
    assert report["counts"]["adjudicated_pairs"] == 61
    assert report["counts"]["audit_qids"] == 21
    assert report["source_counts"] == {"human_adjudication": 61, "glm53flash_low": 27}
    assert report["regenerated_equal_to_existing"]
    assert len(products) == 5
    assert report["raw_inputs_unchanged"]
