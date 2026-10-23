from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "build_chunks.py"


def load_chunker():
    if not MODULE_PATH.exists():
        pytest.fail("El generador de chunks todavía no está implementado")
    spec = importlib.util.spec_from_file_location("build_chunks", MODULE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_record(page: int, text: str, section_id: str = "8.1") -> dict:
    return {
        "record_id": f"book:pdf-{page:04d}",
        "doc_id": "book",
        "source_title": "Statistics Book",
        "source_path": "data/raw/book.pdf",
        "source_sha256": "abc123",
        "license": "CC BY-NC-SA 4.0",
        "chapter_id": "8",
        "chapter_title": "Confidence Intervals",
        "section_id": section_id,
        "section_title": "Population Means",
        "pdf_page": page,
        "printed_page": page - 10,
        "text": text,
        "char_count": len(text),
        "word_count": len(text.split()),
        "extraction_method": "pymupdf_blocks_v1",
    }


def paragraph(prefix: str, words: int) -> str:
    return " ".join([prefix] + [f"word{i}" for i in range(1, words)]) + "."


def test_build_section_chunks_respects_section_and_size_policy():
    chunker = load_chunker()
    records = [
        make_record(20, "\n\n".join(paragraph(f"p{i}", 60) for i in range(1, 6))),
        make_record(21, "\n\n".join(paragraph(f"p{i}", 60) for i in range(6, 9))),
    ]

    chunks = chunker.build_section_chunks(
        records,
        target_words=300,
        max_words=380,
        min_words=100,
        overlap_words=60,
    )

    assert len(chunks) == 2
    assert all(chunk["section_id"] == "8.1" for chunk in chunks)
    assert all(chunk["word_count"] <= 380 for chunk in chunks)
    assert all(chunk["word_count"] >= 100 for chunk in chunks)
    assert chunks[0]["pdf_pages"] == [20]
    assert chunks[1]["pdf_pages"] == [20, 21]
    assert chunks[0]["text"].endswith(paragraph("p5", 60))
    assert chunks[1]["text"].startswith(paragraph("p5", 60))


def sentence(prefix: str, words: int) -> str:
    return " ".join([prefix] + [f"term{i}" for i in range(1, words)]) + "."


def test_overlap_reuses_complete_sentences_when_paragraph_exceeds_budget():
    chunker = load_chunker()
    paragraphs = []
    for paragraph_index in range(1, 6):
        paragraphs.append(
            " ".join(
                sentence(f"P{paragraph_index}S{sentence_index}", 30)
                for sentence_index in range(1, 4)
            )
        )
    records = [make_record(25, "\n\n".join(paragraphs))]

    chunks = chunker.build_section_chunks(records)

    assert len(chunks) == 2
    expected_overlap = "\n\n".join(
        [sentence("P3S3", 30), sentence("P4S1", 30)]
    )
    assert chunks[0]["text"].endswith(expected_overlap)
    assert chunks[1]["text"].startswith(expected_overlap)


def test_build_section_chunks_merges_short_tail():
    chunker = load_chunker()
    records = [
        make_record(
            30,
            "\n\n".join(
                [paragraph("first", 180), paragraph("second", 180), paragraph("tail", 30)]
            ),
        )
    ]

    chunks = chunker.build_section_chunks(
        records,
        target_words=300,
        max_words=380,
        min_words=100,
        overlap_words=60,
    )

    assert len(chunks) == 2
    assert chunks[-1]["word_count"] >= 100
    assert "tail" in chunks[-1]["text"]


def test_build_section_chunks_marks_formula_risk_and_builds_retrieval_text():
    chunker = load_chunker()
    records = [
        make_record(
            40,
            "The density function is shown below.\n\nf(x) =\n\nThe explanation continues.",
        )
    ]

    chunks = chunker.build_section_chunks(records)

    assert len(chunks) == 1
    assert chunks[0]["formula_risk"] is True
    assert chunks[0]["retrieval_text"].startswith(
        "Source: Statistics Book\nChapter 8: Confidence Intervals\n"
        "Section 8.1: Population Means\n\n"
    )
    assert chunks[0]["source_record_ids"] == ["book:pdf-0040"]
    assert chunks[0]["printed_pages"] == [30]


def test_build_all_chunks_keeps_sections_separate_and_ids_stable():
    chunker = load_chunker()
    records = [
        make_record(50, paragraph("alpha", 120), section_id="8.1"),
        make_record(51, paragraph("beta", 120), section_id="8.2"),
    ]

    chunks = chunker.build_all_chunks(records)

    assert [chunk["chunk_id"] for chunk in chunks] == [
        "book:8.1:chunk-001",
        "book:8.2:chunk-001",
    ]
    assert chunks[0]["section_id"] != chunks[1]["section_id"]


def test_run_chunking_writes_real_dataset_and_report(tmp_path):
    chunker = load_chunker()

    report = chunker.run_chunking(
        interim_dir=ROOT / "data" / "interim",
        processed_dir=tmp_path,
    )

    output_path = tmp_path / "chunks_v1.jsonl"
    records = [json.loads(line) for line in output_path.read_text(encoding="utf-8").splitlines()]
    assert report["total_chunks"] == len(records)
    assert report["total_chunks"] > 200
    assert report["total_chunks"] < 400
    assert report["sections"] == 36
    assert all(record["word_count"] <= 380 for record in records)
    assert all(record["word_count"] >= 100 for record in records)
    assert len({record["chunk_id"] for record in records}) == len(records)
    assert (tmp_path / "chunking_report_v1.json").exists()


def test_cli_runs_chunking_with_explicit_paths(tmp_path):
    import shutil
    scripts = tmp_path / 'package/scripts'
    shutil.copytree(ROOT / 'scripts', scripts)
    tmp_path = tmp_path / 'package/outputs/local_runs/fresh'
    result = subprocess.run(
        [
            sys.executable,
            str(scripts / MODULE_PATH.name),
            "--interim-dir",
            str(ROOT / "data" / "interim"),
            "--processed-dir",
            str(tmp_path),
        ],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    assert "chunks" in result.stdout
    assert (tmp_path / "chunks_v1.jsonl").exists()
