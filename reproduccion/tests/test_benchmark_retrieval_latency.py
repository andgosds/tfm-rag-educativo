from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/benchmark_retrieval_latency.py"


def load_module():
    spec = importlib.util.spec_from_file_location("benchmark_retrieval_latency", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_summarize_latencies_reports_mean_median_p95_and_std():
    benchmark = load_module()

    summary = benchmark.summarize_latencies([1.0, 2.0, 3.0, 4.0])

    assert summary == pytest.approx(
        {
            "sample_count": 4,
            "mean_ms": 2.5,
            "median_ms": 2.5,
            "p95_ms": 3.85,
            "std_ms": 1.2909944487358056,
            "min_ms": 1.0,
            "max_ms": 4.0,
        }
    )


def test_build_condition_samples_sums_serial_pipeline_stages():
    benchmark = load_module()
    stages = [
        {"bm25_ms": 2.0, "dense_ms": 6.0, "fusion_ms": 0.1, "rerank_ms": 40.0},
        {"bm25_ms": 3.0, "dense_ms": 7.0, "fusion_ms": 0.2, "rerank_ms": 50.0},
    ]

    samples = benchmark.build_condition_samples(stages)

    assert samples == {
        "bm25": [2.0, 3.0],
        "dense": [6.0, 7.0],
        "hybrid_rrf_serial": [8.1, 10.2],
        "hybrid_rrf_rerank_serial": [48.1, 60.2],
    }


def test_build_condition_samples_rejects_missing_stage():
    benchmark = load_module()

    with pytest.raises(ValueError, match="missing latency stage"):
        benchmark.build_condition_samples([{"bm25_ms": 2.0}])
