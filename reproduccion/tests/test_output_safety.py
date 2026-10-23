import importlib
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))


def test_bm25_refuses_existing_qrels_before_reading_inputs(tmp_path):
    from run_bm25 import run_experiment
    qrels = tmp_path / 'frozen.tsv'
    qrels.write_text('preserved')
    with pytest.raises(FileExistsError, match='destination'):
        run_experiment(run_id='safe', chunks_path=tmp_path/'missing', golden_path=tmp_path/'missing',
                       output_root=tmp_path/'out', qrels_path=qrels, k1=1.5, b=.75, top_k=10, cutoffs=(5,10))
    assert qrels.read_text() == 'preserved'
    assert not (tmp_path/'out').exists()


def test_closure_cli_has_no_implicit_write():
    import ast
    base = Path(__file__).resolve().parents[1]
    source = (base/'scripts/validate_tfm_closure.py').read_text()
    assert '"--output"' in source, 'report writes must require an explicit destination'



@pytest.mark.parametrize('script', ['run_dense', 'run_reranker', 'run_hybrid_rrf', 'benchmark_retrieval_latency', 'build_chunks', 'extract_openstax_chapters', 'build_pooled_qrels', 'compare_pooled_retrieval', 'pool_review_app', 'rag_review_app', 'build_three_judge_priority'])
def test_cli_defaults_fail_before_work(script):
    import subprocess
    base = Path(__file__).resolve().parents[1]
    result = subprocess.run([sys.executable, str(base/'scripts'/f'{script}.py')], capture_output=True, text=True, timeout=15)
    assert result.returncode != 0
    assert 'protected destination' in result.stderr


def test_cli_destination_cannot_escape_root(tmp_path):
    import output_safety
    from argparse import Namespace
    guard = getattr(output_safety, 'guard_cli_outputs', None)
    assert callable(guard), 'missing CLI destination guard'
    with pytest.raises(ValueError, match='protected destination'):
        guard(Namespace(output=tmp_path/'escape.json'), root=tmp_path/'package')

