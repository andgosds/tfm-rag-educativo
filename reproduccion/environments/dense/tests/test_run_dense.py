from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SCRIPT = ROOT / "v1/scripts/run_dense.py"


def load_dense():
    spec = importlib.util.spec_from_file_location("run_dense", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_e5_inputs_use_asymmetric_prefixes():
    dense = load_dense()

    assert dense.build_query_input("What is a confidence interval?") == (
        "query: What is a confidence interval?"
    )
    assert dense.build_passage_input("A confidence interval estimates a population parameter.") == (
        "passage: A confidence interval estimates a population parameter."
    )


def test_rank_embeddings_uses_dot_product_and_deterministic_chunk_ties():
    dense = load_dense()
    document_ids = ["chunk-b", "chunk-a", "chunk-c"]
    document_embeddings = dense.np.asarray(
        [
            [1.0, 0.0],
            [1.0, 0.0],
            [0.0, 1.0],
        ],
        dtype=dense.np.float32,
    )
    query_embedding = dense.np.asarray([1.0, 0.0], dtype=dense.np.float32)

    ranking = dense.rank_embeddings(query_embedding, document_embeddings, document_ids, top_k=3)

    assert [chunk_id for chunk_id, _ in ranking] == ["chunk-a", "chunk-b", "chunk-c"]
    assert ranking[0][1] == ranking[1][1] == 1.0
    assert ranking[2][1] == 0.0


def test_cli_accepts_method_independent_external_qrels():
    dense = load_dense()
    root = Path("/project")

    defaults = dense.build_parser(root).parse_args([])
    selected = dense.build_parser(root).parse_args(
        ["--qrels-input", "/data/pooled.tsv"]
    )

    assert defaults.qrels_input is None
    assert selected.qrels_input == Path("/data/pooled.tsv")
