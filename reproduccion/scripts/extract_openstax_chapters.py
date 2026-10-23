from __future__ import annotations

import argparse
import csv
import json
import re
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any

import pymupdf


OPENSTAX_FOOTER = "Access for free at openstax.org"
HEADER_PATTERNS = (
    re.compile(r"^\d+\s+\d+(?:\.\d+)?\s+•\s+.+$"),
    re.compile(r"^\d+(?:\.\d+)?\s+•\s+.+\s+\d+$"),
)
CHAPTER_PATTERN = re.compile(r"^Chapter\s+(\d+)\s+(.+)$")
SECTION_PATTERN = re.compile(r"^(\d+\.\d+)\s+(.+)$")
EXCLUDED_BOUNDARIES = {
    "Key Terms",
    "Chapter Review",
    "Formula Review",
    "Practice",
    "Homework",
    "Group Project",
    "Critical Thinking",
    "Quantitative Problems",
    "References",
    "Solutions",
}


def parse_chapter_selection(value: str) -> set[int]:
    """Parse comma-separated chapter numbers and inclusive ranges."""
    chapters: set[int] = set()
    for part in value.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            start, end = (int(item.strip()) for item in token.split("-", 1))
            chapters.update(range(start, end + 1))
        else:
            chapters.add(int(token))
    return chapters


def clean_page_blocks(blocks: Iterable[Sequence[Any]]) -> str:
    """Return readable page text without recurring OpenStax furniture."""
    paragraphs: list[str] = []
    for block in blocks:
        text = str(block[4]).strip()
        if not text:
            continue
        if text == OPENSTAX_FOOTER or any(
            pattern.fullmatch(text) for pattern in HEADER_PATTERNS
        ):
            continue
        paragraphs.append(text)
    return "\n\n".join(paragraphs)


def build_chapter_plan(
    toc: Sequence[Sequence[Any]],
    included_chapters: set[int],
    printed_page_offset: int,
) -> list[dict[str, Any]]:
    """Build page and section ranges from a PDF table of contents."""
    plans: list[dict[str, Any]] = []
    chapter_positions: list[tuple[int, int, str, int]] = []
    for index, entry in enumerate(toc):
        level, title, page = int(entry[0]), str(entry[1]), int(entry[2])
        match = CHAPTER_PATTERN.fullmatch(title)
        if level == 1 and match:
            chapter_positions.append((index, int(match.group(1)), match.group(2), page))

    for position, (start_index, chapter_id, chapter_title, start_page) in enumerate(
        chapter_positions
    ):
        if chapter_id not in included_chapters:
            continue
        next_index = (
            chapter_positions[position + 1][0]
            if position + 1 < len(chapter_positions)
            else len(toc)
        )
        next_page = (
            chapter_positions[position + 1][3]
            if position + 1 < len(chapter_positions)
            else start_page + 1
        )
        entries = toc[start_index + 1 : next_index]
        end_page = next_page - 1
        sections: list[dict[str, Any]] = []
        for entry in entries:
            level, title, page = int(entry[0]), str(entry[1]), int(entry[2])
            if level != 2:
                continue
            if title in EXCLUDED_BOUNDARIES:
                # El corte evita incorporar ejercicios y material final al corpus teórico.
                end_page = min(end_page, page - 1)
                break
            if title == "Introduction":
                sections.append(
                    {
                        "section_id": f"{chapter_id}.intro",
                        "section_title": title,
                        "pdf_page_start": page,
                    }
                )
                continue
            section_match = SECTION_PATTERN.fullmatch(title)
            if section_match and int(section_match.group(1).split(".")[0]) == chapter_id:
                sections.append(
                    {
                        "section_id": section_match.group(1),
                        "section_title": section_match.group(2),
                        "pdf_page_start": page,
                    }
                )
        plans.append(
            {
                "chapter_id": str(chapter_id),
                "chapter_title": chapter_title,
                "pdf_page_start": start_page,
                "pdf_page_end": end_page,
                "printed_page_start": start_page - printed_page_offset,
                "printed_page_end": end_page - printed_page_offset,
                "sections": sections,
            }
        )
    return plans


def extract_book(
    pdf_path: Path,
    doc_id: str,
    source_title: str,
    license_name: str,
    source_sha256: str,
    included_chapters: set[int],
    printed_page_offset: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Extract selected textbook pages with chapter and section provenance."""
    document = pymupdf.open(pdf_path)
    try:
        plan = build_chapter_plan(
            document.get_toc(),
            included_chapters=included_chapters,
            printed_page_offset=printed_page_offset,
        )
        records: list[dict[str, Any]] = []
        for chapter in plan:
            sections = sorted(
                chapter["sections"], key=lambda item: item["pdf_page_start"]
            )
            for pdf_page in range(
                chapter["pdf_page_start"], chapter["pdf_page_end"] + 1
            ):
                active_section = sections[0]
                for section in sections:
                    if section["pdf_page_start"] <= pdf_page:
                        active_section = section
                    else:
                        break
                page = document.load_page(pdf_page - 1)
                text = clean_page_blocks(page.get_text("blocks", sort=True))
                records.append(
                    {
                        "record_id": f"{doc_id}:pdf-{pdf_page:04d}",
                        "doc_id": doc_id,
                        "source_title": source_title,
                        "source_path": str(pdf_path),
                        "source_sha256": source_sha256,
                        "license": license_name,
                        "chapter_id": chapter["chapter_id"],
                        "chapter_title": chapter["chapter_title"],
                        "section_id": active_section["section_id"],
                        "section_title": active_section["section_title"],
                        "pdf_page": pdf_page,
                        "printed_page": pdf_page - printed_page_offset,
                        "text": text,
                        "char_count": len(text),
                        "word_count": len(text.split()),
                        "extraction_method": "pymupdf_blocks_v1",
                    }
                )
        return records, plan
    finally:
        document.close()


def build_quality_report(
    records: Sequence[dict[str, Any]],
    plan: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    """Summarize extraction coverage and basic text quality."""
    return {
        "records": len(records),
        "chapters": len({record["chapter_id"] for record in records}),
        "sections": len({record["section_id"] for record in records}),
        "empty_pages": sum(not record["text"].strip() for record in records),
        "short_pages_lt_100_chars": sum(
            record["char_count"] < 100 for record in records
        ),
        "total_chars": sum(record["char_count"] for record in records),
        "total_words": sum(record["word_count"] for record in records),
        "chapter_ranges": list(plan),
    }


def write_jsonl(path: Path, records: Sequence[dict[str, Any]]) -> None:
    """Write records as UTF-8 JSON Lines."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def run_extraction(
    v1_root: Path,
    manifest_path: Path,
    interim_dir: Path,
) -> dict[str, Any]:
    """Extract every included source declared in the corpus manifest."""
    interim_dir.mkdir(parents=True, exist_ok=True)
    with manifest_path.open(encoding="utf-8", newline="") as handle:
        sources = list(csv.DictReader(handle))

    report: dict[str, Any] = {
        "extraction_method": "pymupdf_blocks_v1",
        "total_books": 0,
        "total_records": 0,
        "total_chars": 0,
        "total_words": 0,
        "books": {},
    }
    for source in sources:
        if source["status"] != "included":
            continue
        pdf_path = v1_root / source["raw_path"]
        records, plan = extract_book(
            pdf_path=pdf_path,
            doc_id=source["doc_id"],
            source_title=source["title"],
            license_name=source["license"],
            source_sha256=source["sha256"],
            included_chapters=parse_chapter_selection(source["included_chapters"]),
            printed_page_offset=int(source["printed_page_offset"]),
        )
        for record in records:
            record["source_path"] = source["raw_path"]
        output_path = interim_dir / source["interim_filename"]
        write_jsonl(output_path, records)
        book_report = build_quality_report(records, plan)
        book_report.update(
            {
                "title": source["title"],
                "included_chapters": source["included_chapters"],
                "output_file": source["interim_filename"],
            }
        )
        report["books"][source["doc_id"]] = book_report
        report["total_books"] += 1
        report["total_records"] += book_report["records"]
        report["total_chars"] += book_report["total_chars"]
        report["total_words"] += book_report["total_words"]

    report_path = interim_dir / "extraction_report_v1.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main() -> None:
    """Run the configured v1 extraction from the command line."""
    default_v1_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Extract selected OpenStax chapters with page provenance."
    )
    parser.add_argument("--v1-root", type=Path, default=default_v1_root)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--interim-dir", type=Path)
    args = parser.parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="extract_openstax_chapters")

    v1_root = args.v1_root.resolve()
    manifest_path = args.manifest or v1_root / "config" / "corpus_sources.csv"
    interim_dir = args.interim_dir or v1_root / "data" / "interim"
    report = run_extraction(
        v1_root=v1_root,
        manifest_path=manifest_path,
        interim_dir=interim_dir,
    )
    print(
        f"Extracted {report['total_records']} page records "
        f"from {report['total_books']} books into {interim_dir}."
    )


if __name__ == "__main__":
    main()
