from __future__ import annotations

import argparse
import json
import re
from collections import OrderedDict
from collections.abc import Sequence
from pathlib import Path
from statistics import mean, median
from typing import Any


FORMULA_RISK_PATTERNS = (
    re.compile(
        r"(?:^|\n)\s*[A-Za-z][A-Za-z0-9_]*(?:\([^\n)]*\))?\s*=\s*(?=\n|$)"
    ),
    re.compile(r"(?:^|\n)\s*[xyz]\s*=\s*(?=\n|$)", re.IGNORECASE),
)
SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
CHUNKING_METHOD = "section_paragraphs_300w_overlap60_v1"


def word_count(text: str) -> int:
    """Cuenta las palabras separadas por espacios en el texto."""
    return len(text.split())


def split_long_unit(text: str, max_words: int) -> list[str]:
    """Split an oversized paragraph at sentence boundaries where possible."""
    if word_count(text) <= max_words:
        return [text]
    sentences = [item.strip() for item in SENTENCE_BOUNDARY.split(text) if item.strip()]
    if len(sentences) == 1:
        words = text.split()
        return [
            " ".join(words[start : start + max_words])
            for start in range(0, len(words), max_words)
        ]
    units: list[str] = []
    current: list[str] = []
    current_words = 0
    for sentence in sentences:
        sentence_words = word_count(sentence)
        if sentence_words > max_words:
            if current:
                units.append(" ".join(current))
                current = []
                current_words = 0
            units.extend(split_long_unit(sentence, max_words))
            continue
        if current and current_words + sentence_words > max_words:
            units.append(" ".join(current))
            current = []
            current_words = 0
        current.append(sentence)
        current_words += sentence_words
    if current:
        units.append(" ".join(current))
    return units


def page_units(records: Sequence[dict[str, Any]], max_words: int) -> list[dict[str, Any]]:
    """Turn page paragraphs and sentences into provenance-aware atomic units."""
    units: list[dict[str, Any]] = []
    for record in records:
        paragraphs = [part.strip() for part in record["text"].split("\n\n") if part.strip()]
        for paragraph_index, paragraph in enumerate(paragraphs):
            sentences = [
                item.strip()
                for item in SENTENCE_BOUNDARY.split(paragraph)
                if item.strip()
            ]
            for sentence_index, sentence in enumerate(sentences):
                for part_index, text in enumerate(split_long_unit(sentence, max_words)):
                    units.append(
                        {
                            "text": text,
                            "separator": (
                                "\n\n"
                                if sentence_index == 0 and part_index == 0
                                else " "
                            ),
                            "word_count": word_count(text),
                            "pdf_page": record["pdf_page"],
                            "printed_page": record["printed_page"],
                            "record_id": record["record_id"],
                            "paragraph_index": paragraph_index,
                        }
                    )
    return units


def trailing_overlap(units: Sequence[dict[str, Any]], overlap_words: int) -> list[dict[str, Any]]:
    """Select complete trailing units without exceeding the overlap budget."""
    selected: list[dict[str, Any]] = []
    total = 0
    for unit in reversed(units):
        if total + unit["word_count"] > overlap_words:
            break
        selected.append(unit)
        total += unit["word_count"]
    return list(reversed(selected))


def unique_in_order(values: Sequence[Any]) -> list[Any]:
    """Elimina valores repetidos conservando su orden de aparición."""
    return list(dict.fromkeys(values))


def formula_risk(text: str) -> bool:
    """Flag common signs of mathematical content lost during PDF extraction."""
    return any(pattern.search(text) for pattern in FORMULA_RISK_PATTERNS)


def render_units(units: Sequence[dict[str, Any]]) -> str:
    """Render units while preserving paragraph breaks from the source."""
    parts: list[str] = []
    for index, unit in enumerate(units):
        if index == 0:
            parts.append(unit["text"])
        else:
            parts.append(unit["separator"] + unit["text"])
    return "".join(parts)


def materialize_chunk(
    units: Sequence[dict[str, Any]],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    """Construye un fragmento con texto recuperable, metadatos y procedencia de sus unidades."""
    text = render_units(units)
    retrieval_text = (
        f"Source: {metadata['source_title']}\n"
        f"Chapter {metadata['chapter_id']}: {metadata['chapter_title']}\n"
        f"Section {metadata['section_id']}: {metadata['section_title']}\n\n"
        f"{text}"
    )
    return {
        "doc_id": metadata["doc_id"],
        "source_title": metadata["source_title"],
        "source_path": metadata["source_path"],
        "source_sha256": metadata["source_sha256"],
        "license": metadata["license"],
        "chapter_id": metadata["chapter_id"],
        "chapter_title": metadata["chapter_title"],
        "section_id": metadata["section_id"],
        "section_title": metadata["section_title"],
        "pdf_pages": unique_in_order([unit["pdf_page"] for unit in units]),
        "printed_pages": unique_in_order([unit["printed_page"] for unit in units]),
        "source_record_ids": unique_in_order([unit["record_id"] for unit in units]),
        "text": text,
        "retrieval_text": retrieval_text,
        "word_count": word_count(text),
        "char_count": len(text),
        "formula_risk": formula_risk(text),
        "chunking_method": CHUNKING_METHOD,
    }


def build_section_chunks(
    records: Sequence[dict[str, Any]],
    target_words: int = 300,
    max_words: int = 380,
    min_words: int = 100,
    overlap_words: int = 60,
) -> list[dict[str, Any]]:
    """Build chunks within one section using complete text units."""
    if not records:
        return []
    section_keys = {(record["doc_id"], record["section_id"]) for record in records}
    if len(section_keys) != 1:
        raise ValueError("build_section_chunks accepts records from exactly one section")
    if not (0 <= overlap_words < target_words <= max_words):
        raise ValueError("Expected 0 <= overlap < target <= maximum")

    units = page_units(records, max_words=max_words)
    if not units:
        return []
    groups: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    current_words = 0
    for unit in units:
        unit_words = unit["word_count"]
        if current and current_words + unit_words > target_words:
            groups.append(current)
            current = trailing_overlap(current, overlap_words)
            current_words = sum(item["word_count"] for item in current)
        current.append(unit)
        current_words += unit_words
    if current:
        groups.append(current)

    if len(groups) > 1 and sum(unit["word_count"] for unit in groups[-1]) < min_words:
        tail = groups.pop()
        previous = groups[-1]
        # El solapamiento ya presente no debe duplicarse al fusionar el último grupo.
        previous_ids = {id(unit) for unit in previous}
        additions = [unit for unit in tail if id(unit) not in previous_ids]
        if sum(unit["word_count"] for unit in previous + additions) <= max_words:
            groups[-1] = previous + additions
        else:
            moved: list[dict[str, Any]] = []
            while previous and sum(unit["word_count"] for unit in tail) < min_words:
                candidate = previous[-1]
                if candidate in tail:
                    break
                moved.insert(0, previous.pop())
            groups[-1] = previous
            groups.append(moved + tail)
            groups = [group for group in groups if group]

    metadata = records[0]
    return [materialize_chunk(group, metadata) for group in groups]


def build_all_chunks(
    records: Sequence[dict[str, Any]],
    target_words: int = 300,
    max_words: int = 380,
    min_words: int = 100,
    overlap_words: int = 60,
) -> list[dict[str, Any]]:
    """Build stable chunks for all documents without crossing section boundaries."""
    sections: OrderedDict[tuple[str, str], list[dict[str, Any]]] = OrderedDict()
    for record in records:
        sections.setdefault((record["doc_id"], record["section_id"]), []).append(record)

    chunks: list[dict[str, Any]] = []
    for (_, section_id), section_records in sections.items():
        section_chunks = build_section_chunks(
            section_records,
            target_words=target_words,
            max_words=max_words,
            min_words=min_words,
            overlap_words=overlap_words,
        )
        for index, chunk in enumerate(section_chunks, start=1):
            chunk["chunk_id"] = (
                f"{chunk['doc_id']}:{section_id}:chunk-{index:03d}"
            )
            chunk["chunk_index_in_section"] = index
            chunks.append(chunk)
    return chunks


def percentile(values: Sequence[int], fraction: float) -> float:
    """Interpola un percentil sobre los tamaños ordenados de los fragmentos."""
    ordered = sorted(values)
    if len(ordered) == 1:
        return float(ordered[0])
    position = (len(ordered) - 1) * fraction
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def build_report(chunks: Sequence[dict[str, Any]], input_records: int) -> dict[str, Any]:
    """Resume tamaños, cobertura documental y señales de riesgo de los fragmentos."""
    lengths = [chunk["word_count"] for chunk in chunks]
    return {
        "chunking_method": CHUNKING_METHOD,
        "parameters": {
            "boundary": "section",
            "target_words": 300,
            "max_words": 380,
            "min_words": 100,
            "overlap_words": 60,
            "overlap_unit": "complete_text_units",
        },
        "input_page_records": input_records,
        "total_chunks": len(chunks),
        "documents": len({chunk["doc_id"] for chunk in chunks}),
        "chapters": len({(chunk["doc_id"], chunk["chapter_id"]) for chunk in chunks}),
        "sections": len({(chunk["doc_id"], chunk["section_id"]) for chunk in chunks}),
        "formula_risk_chunks": sum(chunk["formula_risk"] for chunk in chunks),
        "chunks_below_100_words": sum(length < 100 for length in lengths),
        "chunks_above_380_words": sum(length > 380 for length in lengths),
        "word_count": {
            "minimum": min(lengths),
            "mean": round(mean(lengths), 2),
            "median": round(median(lengths), 2),
            "p25": round(percentile(lengths, 0.25), 2),
            "p75": round(percentile(lengths, 0.75), 2),
            "maximum": max(lengths),
        },
        "output_file": "chunks_v1.jsonl",
    }


def read_page_records(interim_dir: Path) -> list[dict[str, Any]]:
    """Reúne los registros de páginas siguiendo el orden de los archivos intermedios."""
    records: list[dict[str, Any]] = []
    for path in sorted(interim_dir.glob("*_pages.jsonl")):
        records.extend(
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    return records


def write_jsonl(path: Path, records: Sequence[dict[str, Any]]) -> None:
    """Guarda los registros como líneas JSON conservando los caracteres Unicode."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def run_chunking(interim_dir: Path, processed_dir: Path) -> dict[str, Any]:
    """Genera los fragmentos del corpus y su informe de segmentación."""
    records = read_page_records(interim_dir)
    chunks = build_all_chunks(records)
    processed_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(processed_dir / "chunks_v1.jsonl", chunks)
    report = build_report(chunks, input_records=len(records))
    (processed_dir / "chunking_report_v1.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return report


def main() -> None:
    """Segmenta los registros de páginas usando las rutas indicadas por consola."""
    default_v1_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Build section-bounded retrieval chunks for corpus v1."
    )
    parser.add_argument(
        "--interim-dir",
        type=Path,
        default=default_v1_root / "data" / "interim",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=default_v1_root / "data" / "processed",
    )
    args = parser.parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="build_chunks")
    report = run_chunking(args.interim_dir, args.processed_dir)
    print(
        f"Built {report['total_chunks']} chunks from "
        f"{report['input_page_records']} page records."
    )


if __name__ == "__main__":
    main()
