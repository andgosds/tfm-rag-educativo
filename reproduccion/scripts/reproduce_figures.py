"""Execute the literal R chunks of the final QMD sources without rendering PDFs.

Requires R with dplyr, ggplot2, jsonlite, knitr and tibble installed in its normal
library. SVGs go into a fresh replay directory; submitted documents stay intact.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from reproduce_offline import destination

ROOT = Path(__file__).resolve().parents[1]


def r_chunks(text: str) -> list[dict]:
    """Extrae los bloques R del QMD con sus etiquetas y dimensiones de figura."""
    chunks = []
    for body in re.findall(r'(?ms)^```\{r\}\n(.*?)^```', text):
        label = re.search(r'(?m)^#\| label: (.+)$', body)
        width = re.search(r'(?m)^#\| fig-width: ([\d.]+)', body)
        height = re.search(r'(?m)^#\| fig-height: ([\d.]+)', body)
        chunks.append({
            'label': label.group(1).strip() if label else None,
            'width': float(width.group(1)) if width else 6.5,
            'height': float(height.group(1)) if height else 4.0,
            'code': body,
        })
    return chunks


R_RUNNER = r'''
args <- commandArgs(trailingOnly = TRUE)
root <- normalizePath(args[1])
out <- normalizePath(args[2])
setwd(root)
documents <- jsonlite::fromJSON(file.path(out, "r_chunks.json"), simplifyVector = FALSE)
for (document in documents) {
  context <- new.env(parent = globalenv())
  for (chunk in document$chunks) {
    value <- NULL
    for (expression in parse(text = chunk$code)) {
      value <- eval(expression, envir = context)
    }
    if (!is.null(chunk$label)) {
      stopifnot(inherits(value, "ggplot"))
      ggplot2::ggsave(file.path(out, paste0(chunk$label, ".svg")),
        plot = value, width = chunk$width, height = chunk$height,
        device = grDevices::svg, bg = "white")
    }
  }
}
writeLines(capture.output(sessionInfo()), file.path(out, "R_sessionInfo.txt"))
'''


def main() -> None:
    """Ejecuta los bloques R originales y verifica los SVG sin modificar los documentos."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id', required=True)
    args = parser.parse_args()
    try:
        output = destination(ROOT, 'figures_' + args.run_id)
    except (ValueError, FileExistsError) as error:
        parser.error(str(error))
    documents = []
    protected = {}
    for name in ('tfm_v2_4.qmd', 'tfm_v2_4_sponsor.qmd'):
        path = ROOT / name
        protected[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        documents.append({'document': name, 'chunks': r_chunks(path.read_text())})
    chunks = [chunk for doc in documents for chunk in doc['chunks']]
    labels = [chunk['label'] for chunk in chunks if chunk['label']]
    assert len(chunks) == 11 and len(labels) == len(set(labels)) == 10
    output.mkdir(parents=True, exist_ok=False)
    (output / 'r_chunks.json').write_text(json.dumps(documents, ensure_ascii=False, indent=2))
    script = output / 'execute_chunks.R'
    script.write_text(R_RUNNER)
    result = subprocess.run(['Rscript', str(script), str(ROOT), str(output)], cwd=ROOT, capture_output=True, text=True)
    (output / 'figures.log').write_text(result.stdout + '\n' + result.stderr)
    if result.returncode:
        raise RuntimeError(f'R chunks failed; see {output / "figures.log"}')
    for label in labels:
        assert (output / (label + '.svg')).stat().st_size > 0
    assert protected == {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in protected}
    report = {
        'documents_changed': False,
        'documents_rendered': False,
        'r_chunks_executed': len(chunks),
        'svg_count': len(labels),
        'source_sha256': protected,
        'output': str(output.relative_to(ROOT)),
        'svg_files': [label + '.svg' for label in labels],
        'note': 'Original plotting code and its assertions executed; SVG byte identity is not asserted across graphics environments.',
    }
    (output / 'figures_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
