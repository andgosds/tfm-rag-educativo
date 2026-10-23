"""Pruebas de la comprobación R3 de la rúbrica de equivalencia."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_equivalence_rubric.py"


@pytest.fixture(scope="module")
def rubric():
    spec = importlib.util.spec_from_file_location("check_equivalence_rubric", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_term_present_in_explicit_and_absent_in_implicit(rubric):
    explicit = (
        "How does the width of the confidence interval change when the sample size "
        "increases?"
    )
    implicit = (
        "How does the width of the range estimated from sample data for a population "
        "parameter change when the sample size increases?"
    )
    assert rubric.has_term(explicit, "confidence interval")
    assert not rubric.has_term(implicit, "confidence interval")


def test_inflected_form_counts_as_presence(rubric):
    assert rubric.has_term("The confidence intervals are wide.", "confidence interval")


def test_partial_term_match_is_not_presence(rubric):
    # 'confidence level' no es 'confidence interval'
    assert not rubric.has_term(
        "How does the confidence level affect the estimate?", "confidence interval"
    )


def test_empty_term_never_matches(rubric):
    assert not rubric.has_term("Any question at all.", "")


def test_overlap_is_descriptive_and_does_not_decide(rubric):
    """La paráfrasis reutiliza vocabulario general del fragmento sin restaurar el término.

    Es el caso que motivó descartar el cociente de solape como criterio: la implícita
    comparte 'sample data' y 'population parameter' con el fragmento, pero el término
    manipulado sigue ausente.
    """
    chunk_vocab = (
        "confidence interval width sample data population parameter estimate sample size"
    )
    paraphrase = (
        "How does sample size affect the range estimated from sample data "
        "for a population parameter estimate?"
    )

    assert rubric.lemmas(paraphrase) & rubric.lemmas(chunk_vocab)
    assert not rubric.has_term(paraphrase, "confidence interval")
