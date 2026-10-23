from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "extract_openstax_chapters.py"


def load_extractor():
    if not MODULE_PATH.exists():
        pytest.fail("El extractor estructurado todavía no está implementado")
    spec = importlib.util.spec_from_file_location("extract_openstax_chapters", MODULE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_clean_page_blocks_removes_openstax_header_and_footer():
    extractor = load_extractor()
    blocks = [
        (0, 0, 500, 20, "336  6 • The Normal Distribution\n", 0, 0),
        (0, 20, 500, 30, "6.1 • The Standard Normal Distribution     337\n", 1, 0),
        (0, 30, 500, 100, "First paragraph.\n", 2, 0),
        (0, 110, 500, 180, "Second paragraph.\n", 3, 0),
        (0, 760, 500, 780, "Access for free at openstax.org\n", 4, 0),
    ]

    text = extractor.clean_page_blocks(blocks)

    assert text == "First paragraph.\n\nSecond paragraph."


def test_build_chapter_plan_stops_before_supplementary_material():
    extractor = load_extractor()
    toc = [
        [1, "Chapter 6 The Normal Distribution", 347],
        [2, "Chapter Objectives", 347],
        [2, "Introduction", 347],
        [2, "6.1 The Standard Normal Distribution", 348],
        [2, "6.2 Using the Normal Distribution", 352],
        [2, "Key Terms", 363],
        [2, "Chapter Review", 363],
        [1, "Chapter 7 The Central Limit Theorem", 377],
    ]

    plan = extractor.build_chapter_plan(toc, {6}, printed_page_offset=12)

    assert plan == [
        {
            "chapter_id": "6",
            "chapter_title": "The Normal Distribution",
            "pdf_page_start": 347,
            "pdf_page_end": 362,
            "printed_page_start": 335,
            "printed_page_end": 350,
            "sections": [
                {
                    "section_id": "6.intro",
                    "section_title": "Introduction",
                    "pdf_page_start": 347,
                },
                {
                    "section_id": "6.1",
                    "section_title": "The Standard Normal Distribution",
                    "pdf_page_start": 348,
                },
                {
                    "section_id": "6.2",
                    "section_title": "Using the Normal Distribution",
                    "pdf_page_start": 352,
                },
            ],
        }
    ]


def test_extract_book_preserves_real_page_chapter_and_section_traceability():
    extractor = load_extractor()
    pdf_path = (
        ROOT
        / "data"
        / "raw"
        / "openstax"
        / "openstax_introductory_statistics_2e.pdf"
    )

    records, plan = extractor.extract_book(
        pdf_path=pdf_path,
        doc_id="openstax_intro_stats_2e",
        source_title="Introductory Statistics 2e",
        license_name="CC BY-NC-SA 4.0",
        source_sha256="a79a953b75e570030c74ea6f700b8bd70f41dc8c01bf4e9618e6a0adba3a382a",
        included_chapters={6, 7, 8, 9},
        printed_page_offset=12,
    )

    assert len(plan) == 4
    assert len(records) == 91
    assert records[0]["record_id"] == "openstax_intro_stats_2e:pdf-0347"
    assert records[0]["pdf_page"] == 347
    assert records[0]["printed_page"] == 335
    assert records[0]["chapter_id"] == "6"
    assert records[0]["section_id"] == "6.intro"
    assert records[-1]["pdf_page"] == 497
    assert records[-1]["chapter_id"] == "9"
    assert records[-1]["section_id"] == "9.6"
    assert all(record["text"] for record in records)
    assert all("Access for free at openstax.org" not in record["text"] for record in records)


def test_parse_chapter_selection_supports_ranges_and_individual_chapters():
    extractor = load_extractor()

    assert extractor.parse_chapter_selection("3-4,6,8-9") == {3, 4, 6, 8, 9}


def test_build_quality_report_summarizes_records_and_provenance():
    extractor = load_extractor()
    records = [
        {
            "chapter_id": "3",
            "section_id": "3.1",
            "text": "short text",
            "char_count": 10,
            "word_count": 2,
        },
        {
            "chapter_id": "3",
            "section_id": "3.2",
            "text": "x" * 150,
            "char_count": 150,
            "word_count": 1,
        },
    ]
    plan = [{"chapter_id": "3", "pdf_page_start": 113, "pdf_page_end": 149}]

    report = extractor.build_quality_report(records, plan)

    assert report["records"] == 2
    assert report["chapters"] == 1
    assert report["sections"] == 2
    assert report["empty_pages"] == 0
    assert report["short_pages_lt_100_chars"] == 1
    assert report["total_chars"] == 160
    assert report["total_words"] == 3
    assert report["chapter_ranges"] == plan


def test_run_extraction_writes_two_jsonl_files_and_report(tmp_path):
    extractor = load_extractor()
    manifest_path = ROOT / "config" / "corpus_sources.csv"

    report = extractor.run_extraction(
        v1_root=ROOT,
        manifest_path=manifest_path,
        interim_dir=tmp_path,
    )

    assert report["total_records"] == 190
    assert report["total_books"] == 2
    assert report["books"]["openstax_intro_stats_2e"]["records"] == 91
    assert report["books"]["openstax_principles_ds"]["records"] == 99
    assert report["books"]["openstax_intro_stats_2e"]["output_file"] == (
        "introductory_statistics_2e_pages.jsonl"
    )
    intro_path = tmp_path / "introductory_statistics_2e_pages.jsonl"
    principles_path = tmp_path / "principles_of_data_science_pages.jsonl"
    assert len(intro_path.read_text(encoding="utf-8").splitlines()) == 91
    assert len(principles_path.read_text(encoding="utf-8").splitlines()) == 99
    first_intro_record = json.loads(
        intro_path.read_text(encoding="utf-8").splitlines()[0]
    )
    assert first_intro_record["source_path"] == (
        "data/raw/openstax/openstax_introductory_statistics_2e.pdf"
    )
    assert (tmp_path / "extraction_report_v1.json").exists()


def test_cli_runs_extraction_with_explicit_paths(tmp_path):
    import shutil
    scripts = tmp_path / 'package/scripts'
    shutil.copytree(ROOT / 'scripts', scripts)
    tmp_path = tmp_path / 'package/outputs/local_runs/fresh'
    result = subprocess.run(
        [
            sys.executable,
            str(scripts / MODULE_PATH.name),
            "--v1-root",
            str(ROOT),
            "--manifest",
            str(ROOT / "config" / "corpus_sources.csv"),
            "--interim-dir",
            str(tmp_path),
        ],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    assert "190 page records" in result.stdout
    assert (tmp_path / "extraction_report_v1.json").exists()
