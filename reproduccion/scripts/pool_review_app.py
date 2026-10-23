from __future__ import annotations

import argparse
import json
import os
import tempfile
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Lee los registros JSONL y exige un objeto por línea no vacía."""
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"Line {line_number} in {path} is not a JSON object")
            rows.append(value)
    return rows


def _load_json_array(path: Path) -> list[dict[str, Any]]:
    """Carga un array JSON y comprueba que todos sus elementos sean objetos."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
        raise ValueError(f"{path} must contain a JSON array of objects")
    return value


def _review_view(review: dict[str, Any]) -> dict[str, Any]:
    """Selecciona los campos del juicio auxiliar que se muestran al revisor."""
    return {
        "reviewer_id": review.get("reviewer_id"),
        "grade": review.get("relevance_grade"),
        "canonical": review.get("canonical_candidate"),
        "answerability_conflict": review.get("answerability_conflict", False),
        "confidence": review.get("confidence"),
        "rationale": review.get("rationale", ""),
    }


def build_review_state(
    priority_path: Path,
    golden_path: Path,
    judge1_path: Path,
    judge2_path: Path,
    chunks_path: Path | None = None,
    judge3_path: Path | None = None,
) -> dict[str, Any]:
    """Construye el estado de revisión sin revelar el sistema que recuperó cada candidato."""
    priority = load_jsonl(priority_path)
    golden = {row["qid"]: row for row in load_jsonl(golden_path)}
    review_paths = [judge1_path, judge2_path]
    if judge3_path is not None:
        review_paths.append(judge3_path)
    judge_maps = [
        {row["pool_id"]: row for row in _load_json_array(path)}
        for path in review_paths
    ]
    chunks = (
        {row["chunk_id"]: row for row in load_jsonl(chunks_path)}
        if chunks_path is not None
        else {}
    )

    candidates: list[dict[str, Any]] = []
    forbidden = {
        # Ocultar procedencia y puntuaciones evita sesgar la adjudicación por método.
        "source_system",
        "source_systems",
        "bm25_rank",
        "dense_rank",
        "bm25_score",
        "dense_score",
        "provenance",
    }
    for row in priority:
        qid = row["qid"]
        pool_id = row["pool_id"]
        if qid not in golden:
            raise ValueError(f"Missing golden record for {qid}")
        if any(pool_id not in mapping for mapping in judge_maps):
            raise ValueError(f"Missing auxiliary review for {pool_id}")
        candidate = {key: value for key, value in row.items() if key not in forbidden}
        gold = golden[qid]
        candidate.update(
            {
                "question_type": gold.get("question_type"),
                "answerability": gold.get("answerability"),
                "gold_answer": gold.get("gold_answer"),
                "unanswerable_category": gold.get("unanswerable_category"),
                "formula_risk": chunks.get(row["chunk_id"], {}).get(
                    "formula_risk", False
                ),
                "pdf_pages": chunks.get(row["chunk_id"], {}).get("pdf_pages", []),
                "auxiliary_reviews": [
                    _review_view(mapping[pool_id]) for mapping in judge_maps
                ],
            }
        )
        candidates.append(candidate)

    reviewed = sum(row.get("human_grade") in {0, 1, 2} for row in candidates)
    return {
        "candidates": candidates,
        "summary": {
            "total": len(candidates),
            "reviewed": reviewed,
            "pending": len(candidates) - reviewed,
        },
    }


def _atomic_write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    """Sustituye el pool con un JSONL temporal sincronizado a disco."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def save_human_decision(
    path: Path,
    pool_id: str,
    grade: int | None,
    canonical: bool | None,
    note: str,
    reviewer_id: str,
    reviewed_at: str | None = None,
) -> dict[str, Any]:
    """Valida y guarda el grado, la canonicidad y la nota humana de un candidato."""
    if grade not in {None, 0, 1, 2}:
        raise ValueError("human grade must be 0, 1, 2 or null")
    if grade != 2 and canonical is True:
        raise ValueError("canonical evidence requires grade 2")
    if grade is not None and canonical is None:
        canonical = False

    rows = load_jsonl(path)
    matches = [row for row in rows if row.get("pool_id") == pool_id]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one candidate for {pool_id}")
    target = matches[0]
    target["human_grade"] = grade
    target["human_canonical"] = canonical
    target["human_note"] = note.strip()
    target["human_reviewer_id"] = reviewer_id
    if grade is None:
        target["human_status"] = "pending"
        target.pop("human_reviewed_at", None)
    else:
        from datetime import datetime

        target["human_status"] = "adjudicated"
        target["human_reviewed_at"] = reviewed_at or datetime.now().astimezone().isoformat(
            timespec="seconds"
        )
    _atomic_write_jsonl(path, rows)
    return target


def render_app_html() -> str:
    """Devuelve la interfaz de adjudicación del pool con opiniones auxiliares plegadas."""
    return r"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Revisión ciega del pool</title>
  <style>
    :root { color-scheme: light dark; --bg:#f6f7f9; --card:#fff; --fg:#17202a; --muted:#64748b; --border:#d8dee8; --accent:#2457d6; --ok:#13795b; --warn:#9a6700; --zero:#5b6472; --one:#9a6700; --two:#13795b; }
    @media (prefers-color-scheme: dark) { :root { --bg:#11151b; --card:#181e27; --fg:#edf2f7; --muted:#9ca9bb; --border:#303a48; --accent:#7aa2ff; --ok:#63d6b3; --warn:#e6b95c; --zero:#aab2c0; --one:#e6b95c; --two:#63d6b3; } }
    * { box-sizing:border-box; }
    body { margin:0; background:var(--bg); color:var(--fg); font:15px/1.5 system-ui,-apple-system,sans-serif; }
    header { position:sticky; top:0; z-index:5; background:color-mix(in srgb,var(--bg) 92%,transparent); backdrop-filter:blur(9px); border-bottom:1px solid var(--border); }
    .top { max-width:1500px; margin:auto; padding:12px 20px; display:flex; align-items:center; gap:16px; flex-wrap:wrap; }
    h1 { margin:0; font-size:19px; }
    .progress { flex:1; min-width:220px; }
    progress { width:100%; height:9px; accent-color:var(--accent); }
    .toolbar { display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
    select, button, textarea { font:inherit; color:inherit; }
    select, button { border:1px solid var(--border); background:var(--card); border-radius:8px; padding:7px 10px; }
    button { cursor:pointer; }
    button:hover { border-color:var(--accent); }
    main { max-width:1500px; margin:0 auto; padding:18px 20px 36px; display:grid; grid-template-columns:minmax(0,1fr) 330px; gap:18px; }
    .card { background:var(--card); border:1px solid var(--border); border-radius:12px; padding:18px; }
    .question { font-size:21px; font-weight:650; margin:5px 0 12px; }
    .badges { display:flex; gap:7px; flex-wrap:wrap; margin-bottom:14px; }
    .badge { border:1px solid var(--border); border-radius:999px; padding:3px 9px; color:var(--muted); font-size:12px; }
    .reference { border-left:3px solid var(--accent); padding:9px 12px; background:color-mix(in srgb,var(--accent) 7%,var(--card)); margin:12px 0 18px; }
    .reference strong { display:block; margin-bottom:4px; }
    .chunk-meta { color:var(--muted); font-size:13px; margin-bottom:8px; }
    pre { white-space:pre-wrap; word-break:break-word; font:14px/1.56 ui-monospace,SFMono-Regular,Consolas,monospace; margin:0; max-height:56vh; overflow:auto; padding:14px; border:1px solid var(--border); border-radius:9px; background:color-mix(in srgb,var(--bg) 68%,var(--card)); }
    aside { display:flex; flex-direction:column; gap:12px; align-self:start; position:sticky; top:87px; max-height:calc(100vh - 100px); overflow:auto; padding-right:3px; }
    .grade-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; }
    .grade { font-size:18px; font-weight:700; padding:12px 5px; }
    .grade.selected { outline:3px solid var(--accent); outline-offset:1px; }
    #grade-0 { color:var(--zero); } #grade-1 { color:var(--one); } #grade-2 { color:var(--two); }
    label { display:block; margin:10px 0 5px; font-weight:600; }
    textarea { width:100%; min-height:92px; resize:vertical; border:1px solid var(--border); background:var(--bg); border-radius:8px; padding:9px; }
    .primary { width:100%; background:var(--accent); color:white; border-color:var(--accent); padding:11px; font-weight:700; }
    .row { display:flex; gap:8px; }
    .row button { flex:1; }
    details { border-top:1px solid var(--border); padding-top:10px; }
    summary { cursor:pointer; font-weight:650; }
    .review { margin-top:10px; padding:10px; border:1px solid var(--border); border-radius:8px; }
    .review p { margin:5px 0 0; color:var(--muted); }
    .guide { margin-top:10px; font-size:13px; }
    .guide ol, .guide ul { margin:7px 0; padding-left:20px; }
    .guide li { margin:6px 0; }
    .guide .g0 { color:var(--zero); } .guide .g1 { color:var(--one); } .guide .g2 { color:var(--two); }
    .guide-note { margin:8px 0 0; padding:8px 9px; border-left:3px solid var(--accent); background:color-mix(in srgb,var(--accent) 7%,var(--card)); }
    .shortcut-table { width:100%; border-collapse:collapse; margin-top:8px; font-size:12px; }
    .shortcut-table td { border-top:1px solid var(--border); padding:5px 3px; vertical-align:top; }
    kbd { border:1px solid var(--border); border-bottom-width:2px; border-radius:4px; padding:1px 5px; background:var(--bg); font:11px ui-monospace,monospace; }
    .hint { color:var(--muted); font-size:12px; margin-top:8px; }
    #status { min-height:22px; font-size:13px; color:var(--ok); }
    .empty { text-align:center; color:var(--muted); padding:70px 20px; }
    @media (max-width:900px) { main { grid-template-columns:1fr; } aside { position:static; } pre { max-height:none; } }
  </style>
</head>
<body>
<header><div class="top">
  <h1>Revisión ciega del pool</h1>
  <div class="progress"><div id="progress-label">Cargando…</div><progress id="progress" value="0" max="1"></progress></div>
  <div class="toolbar">
    <select id="qid-filter" title="Filtrar por pregunta"><option value="all">Todas las preguntas</option></select>
    <select id="status-filter" title="Filtrar por estado"><option value="pending">Pendientes</option><option value="all">Todos</option><option value="reviewed">Revisados</option></select>
    <button id="export" title="Descargar copia JSONL">Exportar</button>
  </div>
</div></header>
<main>
  <section class="card" id="candidate-panel">
    <div class="empty" id="empty-state" hidden>No hay candidatos con estos filtros.</div>
    <div id="candidate-content">
    <div class="badges"><span class="badge" id="position"></span><span class="badge" id="qid"></span><span class="badge" id="type"></span><span class="badge" id="answerability"></span><span class="badge" id="conflict" hidden>Conflicto de respondibilidad</span><span class="badge" id="formula-risk" hidden>Riesgo de fórmula: verificar fuente</span></div>
    <div class="question" id="question"></div>
    <div class="reference"><strong id="reference-label">Respuesta de referencia</strong><span id="reference"></span></div>
    <div class="chunk-meta"><span id="chunk-id"></span></div>
    <pre id="chunk"></pre>
    </div>
  </section>
  <aside>
    <section class="card">
      <details id="decision-guide" open>
        <summary>Guía rápida de decisión</summary>
        <div class="guide">
          <ol>
            <li><strong>¿El chunk trata la afirmación solicitada?</strong> Si no, asigna <strong class="g0">0</strong>. Si solo comparte tema o terminología, considera <strong class="g1">1</strong>.</li>
            <li><strong>¿Aporta evidencia directa?</strong> Debe sostener una afirmación de la respuesta, no limitarse a introducir el tema.</li>
            <li><strong>¿Es suficiente?</strong> Si necesita información externa para sostener esa afirmación, asigna <strong class="g1">1</strong>. Si la sostiene de forma directa y suficiente, asigna <strong class="g2">2</strong>.</li>
          </ol>
          <ul>
            <li><strong class="g0">0 — No aporta evidencia útil:</strong> irrelevante, coincidencia superficial o contenido que no ayuda a responder.</li>
            <li><strong class="g1">1 — Relacionado, pero insuficiente:</strong> contexto útil que no respalda por sí mismo una afirmación requerida.</li>
            <li><strong class="g2">2 — Evidencia directa y suficiente:</strong> respalda claramente una afirmación necesaria de la respuesta.</li>
          </ul>
          <p class="guide-note"><strong>Pregunta multichunk:</strong> un chunk puede recibir 2 si cubre de forma suficiente uno de los componentes requeridos, aunque la respuesta completa necesite otros chunks de grado 2.</p>
          <p class="guide-note"><strong>Canónica:</strong> márcala solo en una evidencia de grado 2 cuando sea la fuente principal o preferida para responder. No todos los grados 2 tienen que ser canónicos.</p>
          <p class="guide-note"><strong>Si una pregunta marcada como no respondible parece respondida por el chunk:</strong> asigna el grado que corresponda a la evidencia y deja una nota indicando el posible conflicto de respondibilidad.</p>
        </div>
      </details>
      <details id="shortcut-guide" open>
        <summary>Atajos de teclado</summary>
        <table class="shortcut-table">
          <tr><td><kbd>0</kbd> <kbd>1</kbd> <kbd>2</kbd></td><td>Seleccionar grado</td></tr>
          <tr><td><kbd>C</kbd></td><td>Cambiar canonicidad si el grado es 2</td></tr>
          <tr><td><kbd>N</kbd></td><td>Escribir una nota</td></tr>
          <tr><td><kbd>Enter</kbd></td><td>Guardar y avanzar</td></tr>
          <tr><td><kbd>←</kbd> <kbd>→</kbd></td><td>Navegar sin guardar</td></tr>
          <tr><td><kbd>U</kbd></td><td>Deshacer la última decisión de esta sesión</td></tr>
          <tr><td><kbd>Esc</kbd></td><td>Salir del campo de edición</td></tr>
        </table>
      </details>
    </section>
    <section class="card">
      <strong>Grado humano</strong>
      <div class="grade-grid">
        <button class="grade" id="grade-0" data-grade="0">0</button>
        <button class="grade" id="grade-1" data-grade="1">1</button>
        <button class="grade" id="grade-2" data-grade="2">2</button>
      </div>
      <label><input type="checkbox" id="canonical" disabled> Evidencia canónica <kbd>C</kbd></label>
      <label for="note">Nota <kbd>N</kbd></label>
      <textarea id="note" placeholder="Solo cuando la decisión necesite justificación"></textarea>
      <button class="primary" id="save-next">Guardar y siguiente <kbd>Enter</kbd></button>
      <div class="row"><button id="previous">← Anterior</button><button id="next">Siguiente →</button></div>
      <div class="row"><button id="undo">Deshacer <kbd>U</kbd></button><button id="clear">Dejar pendiente</button></div>
      <div id="status"></div>
      <div class="hint">0/1/2 seleccionan grado · C cambia canonicidad · N abre la nota · flechas navegan.</div>
    </section>
    <section class="card">
      <details id="auxiliary-reviews"><summary>Mostrar opiniones auxiliares</summary><div id="reviews"></div></details>
    </section>
  </aside>
</main>
<script>
let allCandidates = [], visible = [], index = 0, selectedGrade = null, undoStack = [];
const $ = id => document.getElementById(id);
const escapeText = value => value == null ? '' : String(value);

async function loadState(preferredId=null) {
  const response = await fetch('/api/state');
  if (!response.ok) throw new Error(await response.text());
  const state = await response.json();
  allCandidates = state.candidates;
  populateQids();
  applyFilters(preferredId);
  $('progress').max = state.summary.total || 1;
  $('progress').value = state.summary.reviewed;
  $('progress-label').textContent = `${state.summary.reviewed} de ${state.summary.total} revisados · ${state.summary.pending} pendientes`;
}

function populateQids() {
  const select = $('qid-filter'), current = select.value;
  const qids = [...new Set(allCandidates.map(c => c.qid))];
  select.replaceChildren(new Option('Todas las preguntas', 'all'), ...qids.map(q => new Option(q, q)));
  if ([...select.options].some(o => o.value === current)) select.value = current;
}

function applyFilters(preferredId=null) {
  const qid = $('qid-filter').value, status = $('status-filter').value;
  visible = allCandidates.filter(c => (qid === 'all' || c.qid === qid) && (status === 'all' || (status === 'pending' ? c.human_grade == null : c.human_grade != null)));
  if (preferredId) { const found = visible.findIndex(c => c.pool_id === preferredId); index = found >= 0 ? found : Math.min(index, Math.max(0, visible.length - 1)); }
  else index = Math.min(index, Math.max(0, visible.length - 1));
  render();
}

function current() { return visible[index] || null; }
function setText(id, value) { $(id).textContent = escapeText(value); }

function selectGrade(grade) {
  selectedGrade = grade;
  document.querySelectorAll('.grade').forEach(b => b.classList.toggle('selected', Number(b.dataset.grade) === grade));
  $('canonical').disabled = grade !== 2;
  if (grade !== 2) $('canonical').checked = false;
}

function render() {
  const c = current();
  $('empty-state').hidden = Boolean(c);
  $('candidate-content').hidden = !c;
  if (!c) return;
  setText('position', `${index + 1} de ${visible.length}`); setText('qid', c.qid); setText('type', c.question_type); setText('answerability', c.answerability);
  $('conflict').hidden = !c.answerability_conflict;
  $('formula-risk').hidden = !c.formula_risk;
  setText('question', c.question); setText('chunk-id', `${c.chunk_id}${c.pdf_pages?.length ? ` · PDF ${c.pdf_pages.join(', ')}` : ''}`); setText('chunk', c.retrieval_text);
  setText('reference-label', c.answerability === 'unanswerable' ? 'Abstención esperada' : 'Respuesta de referencia');
  setText('reference', c.answerability === 'unanswerable' ? 'La pregunta no puede responderse con el corpus congelado.' : c.gold_answer);
  selectGrade(c.human_grade); $('canonical').checked = c.human_canonical === true; $('note').value = c.human_note || '';
  const reviews = $('reviews'); reviews.replaceChildren();
  c.auxiliary_reviews.forEach((r, i) => {
    const box = document.createElement('div'); box.className = 'review';
    const title = document.createElement('strong'); title.textContent = `Juez ${i + 1}: grado ${r.grade} · canónico ${r.canonical} · confianza ${r.confidence}`;
    const p = document.createElement('p'); p.textContent = r.rationale;
    box.append(title, p); reviews.append(box);
  });
  $('auxiliary-reviews').open = false; $('status').textContent = '';
}

async function persist(decision, goNext=true) {
  const c = current(); if (!c) return;
  if (decision.grade == null && goNext) { $('status').textContent = 'Selecciona un grado 0, 1 o 2.'; return; }
  const before = {pool_id:c.pool_id, grade:c.human_grade, canonical:c.human_canonical, note:c.human_note || ''};
  const response = await fetch('/api/decision', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({pool_id:c.pool_id, ...decision})});
  if (!response.ok) { $('status').textContent = await response.text(); return; }
  if (goNext) undoStack.push(before);
  const nextId = goNext && visible[index + 1] ? visible[index + 1].pool_id : c.pool_id;
  await loadState(nextId); $('status').textContent = 'Guardado.';
}

async function saveNext() { await persist({grade:selectedGrade, canonical:$('canonical').checked, note:$('note').value}, true); }
async function clearDecision() { await persist({grade:null, canonical:null, note:''}, false); }
async function undoLast() {
  const prior = undoStack.pop(); if (!prior) { $('status').textContent = 'No hay cambios de esta sesión para deshacer.'; return; }
  const response = await fetch('/api/decision', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(prior)});
  if (!response.ok) { $('status').textContent = await response.text(); return; }
  await loadState(prior.pool_id); $('status').textContent = 'Última decisión deshecha.';
}

document.querySelectorAll('.grade').forEach(b => b.addEventListener('click', () => selectGrade(Number(b.dataset.grade))));
$('canonical').addEventListener('change', () => {}); $('save-next').addEventListener('click', saveNext); $('clear').addEventListener('click', clearDecision); $('undo').addEventListener('click', undoLast);
$('previous').addEventListener('click', () => { if (index > 0) { index--; render(); } });
$('next').addEventListener('click', () => { if (index + 1 < visible.length) { index++; render(); } });
$('qid-filter').addEventListener('change', () => { index=0; applyFilters(); }); $('status-filter').addEventListener('change', () => { index=0; applyFilters(); });
$('export').addEventListener('click', () => { window.location = '/api/export'; });
document.addEventListener('keydown', event => {
  const editing = ['TEXTAREA','INPUT','SELECT'].includes(document.activeElement.tagName);
  if (editing && event.key !== 'Escape' && !(event.ctrlKey && event.key === 'Enter')) return;
  if (event.key === '0') selectGrade(0);
  else if (event.key === '1') selectGrade(1);
  else if (event.key === '2') selectGrade(2);
  else if (event.key.toLowerCase() === 'c' && selectedGrade === 2) $('canonical').click();
  else if (event.key.toLowerCase() === 'n') $('note').focus();
  else if (event.key === 'Enter') saveNext();
  else if (event.key === 'ArrowLeft' && index > 0) { index--; render(); }
  else if (event.key === 'ArrowRight' && index + 1 < visible.length) { index++; render(); }
  else if (event.key.toLowerCase() === 'u') undoLast();
  else if (event.key === 'Escape') document.activeElement.blur();
});
loadState().catch(error => { document.body.textContent = `No se pudo cargar la aplicación: ${error}`; });
</script>
</body></html>"""


def make_handler(
    priority_path: Path,
    golden_path: Path,
    judge1_path: Path,
    judge2_path: Path,
    judge3_path: Path | None,
    chunks_path: Path,
    reviewer_id: str,
) -> type[BaseHTTPRequestHandler]:
    """Crea el manejador HTTP con las fuentes de revisión y el revisor indicados."""
    class ReviewHandler(BaseHTTPRequestHandler):
        def _send(self, status: int, content_type: str, body: bytes) -> None:
            """Envía el cuerpo HTTP con su tipo y sin almacenamiento en caché."""
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, value: Any, status: int = 200) -> None:
            """Serializa y envía un valor como respuesta JSON."""
            self._send(
                status,
                "application/json; charset=utf-8",
                json.dumps(value, ensure_ascii=False).encode("utf-8"),
            )

        def do_GET(self) -> None:  # noqa: N802
            """Sirve la interfaz, el estado del pool o su descarga JSONL."""
            route = urlparse(self.path).path
            try:
                if route == "/":
                    self._send(200, "text/html; charset=utf-8", render_app_html().encode("utf-8"))
                elif route == "/api/state":
                    self._json(
                        build_review_state(
                            priority_path,
                            golden_path,
                            judge1_path,
                            judge2_path,
                            chunks_path,
                            judge3_path,
                        )
                    )
                elif route == "/api/export":
                    body = priority_path.read_bytes()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
                    self.send_header("Content-Disposition", f'attachment; filename="{priority_path.name}"')
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                else:
                    self._send(404, "text/plain; charset=utf-8", b"Not found")
            except Exception as error:
                self._send(500, "text/plain; charset=utf-8", str(error).encode("utf-8"))

        def do_POST(self) -> None:  # noqa: N802
            """Valida la solicitud de adjudicación y guarda la decisión humana."""
            if urlparse(self.path).path != "/api/decision":
                self._send(404, "text/plain; charset=utf-8", b"Not found")
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length > 100_000:
                    raise ValueError("Request too large")
                payload = json.loads(self.rfile.read(length))
                saved = save_human_decision(
                    priority_path,
                    pool_id=payload["pool_id"],
                    grade=payload.get("grade"),
                    canonical=payload.get("canonical"),
                    note=payload.get("note", ""),
                    reviewer_id=reviewer_id,
                )
                self._json({"saved": saved})
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
                self._send(400, "text/plain; charset=utf-8", str(error).encode("utf-8"))

        def log_message(self, format: str, *args: Any) -> None:
            """Registra la solicitud con la dirección del cliente."""
            print(f"{self.address_string()} - {format % args}")

    return ReviewHandler


def parse_args() -> argparse.Namespace:
    """Recoge las rutas del pool y los jueces junto con las opciones del servidor."""
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Local blind pool adjudication app")
    parser.add_argument("--priority", type=Path, default=root / "data/golden/pool_human_priority_three_judge_v1_22q.jsonl")
    parser.add_argument("--golden", type=Path, default=root / "data/golden/golden_set_pilot_v1.jsonl")
    parser.add_argument("--judge1", type=Path, default=root / "data/golden/reviews/pool_judge1_reviews_2026-08-17.json")
    parser.add_argument("--judge2", type=Path, default=root / "data/golden/reviews/pool_judge2_reviews_2026-08-17.json")
    parser.add_argument("--judge3", type=Path, default=root / "data/golden/reviews/pool_judge3_reviews_2026-08-24.json")
    parser.add_argument("--chunks", type=Path, default=root / "data/processed/chunks_v1.jsonl")
    parser.add_argument("--reviewer-id", default="andres")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    return parser.parse_args()


def main() -> None:
    """Valida las fuentes e inicia el servidor local de revisión del pool."""
    args = parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="pool_review_app")
    build_review_state(
        args.priority,
        args.golden,
        args.judge1,
        args.judge2,
        args.chunks,
        args.judge3,
    )
    handler = make_handler(
        args.priority,
        args.golden,
        args.judge1,
        args.judge2,
        args.judge3,
        args.chunks,
        args.reviewer_id,
    )
    server = ThreadingHTTPServer((args.host, args.port), handler)
    url = f"http://{args.host}:{args.port}"
    print(f"Pool review app: {url}")
    print(f"Data file: {args.priority}")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
