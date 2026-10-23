"""Interfaz local para la cola ciega de la campaña de explicitud (v2).

Revisa las 122 unidades formulación-chunk sin juicio previo de
outputs/explicitness_v2/pools/blind_review_queue.jsonl. La copia de trabajo
vive en outputs/local_runs/ (el original congelado nunca se edita).

Guardar escribe en la copia de forma atómica por unidad:
  human_decision = {grade, canonical, note, reviewer, decided_at}
  annotation_status = adjudicated

Lanzar desde la raíz v2:
  uv run --no-sync python scripts/explicitness_blind_review_app.py

Reanudación automática: la cola de trabajo conserva las decisiones ya
guardadas; la app abre en la primera unidad pendiente.
"""
from __future__ import annotations

import argparse
import json
import os
import tempfile
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import importlib.util

def _load_output_safety():
    """Carga la protección de salidas desde el archivo situado junto a la aplicación."""
    spec = importlib.util.spec_from_file_location(
        "output_safety", Path(__file__).resolve().parent / "output_safety.py"
    )
    if spec is None or spec.loader is None:
        raise ImportError("No se pudo cargar output_safety.py junto a esta app")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

output_safety = _load_output_safety()  # noqa: F841 — guarda disponible para recetas futuras

VALID_GRADES = {0, 1, 2}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Lee la cola JSONL y comprueba que cada registro sea un objeto."""
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"Línea {line_number} de {path} no es un objeto JSON")
            rows.append(value)
    return rows


def prepare_work_copy(source: Path, work: Path) -> dict[str, Any]:
    """Crea la copia de trabajo si no existe; nunca toca el archivo congelado."""
    if work.exists():
        return {"created": False, "units": len(load_jsonl(work))}
    work.parent.mkdir(parents=True, exist_ok=True)
    rows = load_jsonl(source)
    for row in rows:
        if row.get("human_decision") is not None or row.get("annotation_status") == "adjudicated":
            raise ValueError(
                f"La cola fuente contiene decisiones ({row.get('pool_id')}); "
                "no debe copiarse a ciegas. Revisa la procedencia antes de continuar."
            )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{work.name}.", suffix=".tmp", dir=work.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, work)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()
    return {"created": True, "units": len(rows)}


def load_golden_context(golden_path: Path, pairs_path: Path) -> dict[str, dict[str, Any]]:
    """Mapa qid (con sufijo __explicit/__implicit) -> contexto de revisión."""
    golden = {row["qid"]: row for row in load_jsonl(golden_path)}
    pairs: dict[str, dict[str, Any]] = {}
    with pairs_path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                row = json.loads(line)
                pairs[row["base_qid"]] = row
    context: dict[str, dict[str, Any]] = {}
    for base_qid, gold in golden.items():
        pair = pairs.get(base_qid, {})
        context[f"{base_qid}__explicit"] = {
            "question": pair.get("explicit_question") or gold.get("question"),
            "gold_answer": gold.get("gold_answer"),
            "question_type": gold.get("question_type"),
            "answerability": gold.get("answerability"),
            "unanswerable_category": gold.get("unanswerable_category"),
        }
        context[f"{base_qid}__implicit"] = {
            "question": pair.get("implicit_question") or gold.get("question"),
            "gold_answer": gold.get("gold_answer"),
            "question_type": gold.get("question_type"),
            "answerability": gold.get("answerability"),
            "unanswerable_category": gold.get("unanswerable_category"),
        }
    return context


def build_review_state(work_path: Path, chunks_path: Path, context: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Combina las unidades de revisión con su contexto y resume el avance humano."""
    rows = load_jsonl(work_path)
    chunks = {row["chunk_id"]: row for row in load_jsonl(chunks_path)}
    candidates: list[dict[str, Any]] = []
    for row in rows:
        qid = row["qid"]
        if qid not in context:
            raise ValueError(f"Sin contexto dorado para {qid}")
        chunk = chunks.get(row["chunk_id"], {})
        info = context[qid]
        decision = row.get("human_decision") or {}
        candidates.append(
            {
                "pool_id": row["pool_id"],
                "qid": qid,
                "base_qid": row.get("base_qid"),
                "explicitness": row.get("explicitness"),
                "question": info["question"],
                "question_type": info["question_type"],
                "answerability": info["answerability"],
                "unanswerable_category": info["unanswerable_category"],
                "gold_answer": info["gold_answer"],
                "chunk_id": row["chunk_id"],
                "pdf_pages": chunk.get("pdf_pages", []),
                "chunk_text": row.get("retrieval_text") or chunk.get("text", ""),
                "grade": decision.get("grade"),
                "canonical": decision.get("canonical"),
                "note": decision.get("note", ""),
                "reviewed_at": decision.get("decided_at"),
            }
        )
    reviewed = sum(c["grade"] in VALID_GRADES for c in candidates)
    return {
        "candidates": candidates,
        "summary": {
            "total": len(candidates),
            "reviewed": reviewed,
            "pending": len(candidates) - reviewed,
        },
    }


def save_human_decision(
    work_path: Path,
    pool_id: str,
    grade: int | None,
    canonical: bool | None,
    note: str,
    reviewer_id: str,
) -> dict[str, Any]:
    """Valida y guarda la decisión humana de una unidad o la deja pendiente."""
    if grade not in {None, *VALID_GRADES}:
        raise ValueError("El grado humano debe ser 0, 1, 2 o null")
    if grade != 2 and canonical is True:
        raise ValueError("La evidencia canónica exige grado 2")
    if grade is not None and canonical is None:
        canonical = False

    rows = load_jsonl(work_path)
    matches = [row for row in rows if row.get("pool_id") == pool_id]
    if len(matches) != 1:
        raise ValueError(f"Se esperaba exactamente una unidad para {pool_id}")
    target = matches[0]
    if grade is None:
        target["human_decision"] = None
        target["annotation_status"] = "pending"
    else:
        decided_at = datetime.now().astimezone().isoformat(timespec="seconds")
        target["human_decision"] = {
            "grade": grade,
            "canonical": canonical,
            "note": note.strip(),
            "reviewer": reviewer_id,
            "decided_at": decided_at,
        }
        target["annotation_status"] = "adjudicated"
    _atomic_write_jsonl(work_path, rows)
    return {
        "pool_id": pool_id,
        "grade": grade,
        "canonical": canonical,
        "annotation_status": target["annotation_status"],
        "reviewed_at": target["human_decision"].get("decided_at") if target["human_decision"] else None,
    }


def _atomic_write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    """Sustituye la cola JSONL mediante un archivo temporal sincronizado."""
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


def render_app_html() -> str:
    """Devuelve la interfaz HTML de revisión ciega con sus controles de anotación."""
    return r"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cola ciega de explicitud — v2</title>
  <style>
    :root { color-scheme: light dark; --bg:#f6f7f9; --card:#fff; --fg:#17202a; --muted:#64748b; --border:#d8dee8; --accent:#2457d6; --ok:#13795b; --zero:#5b6472; --one:#9a6700; --two:#13795b; }
    @media (prefers-color-scheme: dark) { :root { --bg:#11151b; --card:#181e27; --fg:#edf2f7; --muted:#9ca9bb; --border:#303a48; --accent:#7aa2ff; --ok:#63d6b3; --zero:#aab2c0; --one:#e6b95c; --two:#63d6b3; } }
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
    .badge.explicit { color:var(--accent); border-color:var(--accent); }
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
    .decided-note { margin-top:10px; font-size:13px; color:var(--muted); }
    @media (max-width:900px) { main { grid-template-columns:1fr; } aside { position:static; } pre { max-height:none; } }
  </style>
</head>
<body>
<header><div class="top">
  <h1>Cola ciega de explicitud</h1>
  <div class="progress"><div id="progress-label">Cargando…</div><progress id="progress" value="0" max="1"></progress></div>
  <div class="toolbar">
    <select id="qid-filter" title="Filtrar por pregunta"><option value="all">Todas las preguntas</option></select>
    <select id="status-filter" title="Filtrar por estado"><option value="pending">Pendientes</option><option value="all">Todos</option><option value="reviewed">Revisados</option></select>
    <button id="export" title="Descargar copia JSONL">Exportar</button>
  </div>
</div></header>
<main>
  <section class="card" id="candidate-panel">
    <div class="empty" id="empty-state" hidden>No hay unidades con estos filtros.</div>
    <div id="candidate-content">
    <div class="badges"><span class="badge" id="position"></span><span class="badge" id="qid"></span><span class="badge explicit" id="explicitness"></span><span class="badge" id="type"></span><span class="badge" id="answerability"></span></div>
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
          <p class="guide-note"><strong>Pregunta multichunk:</strong> un chunk puede recibir 2 si cubre de forma suficiente uno de los componentes requeridos, aunque la respuesta completa necesite otros chunks de grado 2.</p>
          <p class="guide-note"><strong>Canónica:</strong> márcala solo en una evidencia de grado 2 cuando sea la fuente principal o preferida para responder.</p>
          <p class="guide-note"><strong>Revisión ciega:</strong> estas unidades no tienen juicio previo. No hay opiniones auxiliares que consultar: la decisión es enteramente tuya.</p>
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
      <div id="decided-note" class="decided-note" hidden></div>
      <div class="hint">0/1/2 seleccionan grado · C cambia canonicidad · N abre la nota · flechas navegan. Cada guardado se escribe en disco al instante; puedes cerrar y reanudar cuando quieras.</div>
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
  $('progress-label').textContent = `${state.summary.reviewed} de ${state.summary.total} revisadas · ${state.summary.pending} pendientes`;
}

function populateQids() {
  const select = $('qid-filter'), current = select.value;
  const qids = [...new Set(allCandidates.map(c => c.qid))];
  select.replaceChildren(new Option('Todas las preguntas', 'all'), ...qids.map(q => new Option(q, q)));
  if ([...select.options].some(o => o.value === current)) select.value = current;
}

function applyFilters(preferredId=null) {
  const qid = $('qid-filter').value, status = $('status-filter').value;
  visible = allCandidates.filter(c => (qid === 'all' || c.qid === qid) && (status === 'all' || (status === 'pending' ? c.grade == null : c.grade != null)));
  if (preferredId) { const found = visible.findIndex(c => c.pool_id === preferredId); index = found >= 0 ? found : Math.min(index, Math.max(0, visible.length - 1)); }
  else if (status === 'pending') { const firstPending = visible.findIndex(c => c.grade == null); index = firstPending >= 0 ? firstPending : Math.min(index, Math.max(0, visible.length - 1)); }
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
  if (!c) { $('progress-label').textContent = 'Sin unidades pendientes con estos filtros.'; return; }
  setText('position', `${index + 1} de ${visible.length}`); setText('qid', c.qid);
  setText('explicitness', c.explicitness === 'implicit' ? 'implícita' : 'explícita');
  setText('type', c.question_type); setText('answerability', c.answerability);
  setText('question', c.question); setText('chunk-id', `${c.chunk_id}${c.pdf_pages?.length ? ` · PDF ${c.pdf_pages.join(', ')}` : ''}`); setText('chunk', c.chunk_text);
  setText('reference-label', c.answerability === 'unanswerable' ? 'Abstención esperada' : 'Respuesta de referencia');
  setText('reference', c.answerability === 'unanswerable' ? 'La pregunta no puede responderse con el corpus congelado.' : c.gold_answer);
  selectGrade(c.grade); $('canonical').checked = c.canonical === true; $('note').value = c.note || '';
  const dn = $('decided-note');
  if (c.reviewed_at) { dn.hidden = false; dn.textContent = `Decidido el ${c.reviewed_at}. Guardar de nuevo lo sobrescribe.`; }
  else dn.hidden = true;
  $('status').textContent = '';
}

async function persist(decision, goNext=true) {
  const c = current(); if (!c) return;
  if (decision.grade == null && goNext) { $('status').textContent = 'Selecciona un grado 0, 1 o 2.'; return; }
  const before = {pool_id:c.pool_id, grade:c.grade, canonical:c.canonical, note:c.note || ''};
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
$('save-next').addEventListener('click', saveNext); $('clear').addEventListener('click', clearDecision); $('undo').addEventListener('click', undoLast);
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


def make_handler(work_path: Path, chunks_path: Path, context: dict[str, dict[str, Any]], reviewer_id: str):
    """Crea el manejador HTTP vinculado a la cola y al revisor indicados."""
    class ReviewHandler(BaseHTTPRequestHandler):
        def _send(self, status: int, content_type: str, body: bytes) -> None:
            """Envía una respuesta HTTP sin caché con el cuerpo indicado."""
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, value: Any, status: int = 200) -> None:
            """Serializa el valor como JSON y lo envía al navegador."""
            self._send(
                status,
                "application/json; charset=utf-8",
                json.dumps(value, ensure_ascii=False).encode("utf-8"),
            )

        def do_GET(self) -> None:  # noqa: N802
            """Sirve la interfaz, el estado de revisión o la exportación de la cola."""
            route = urlparse(self.path).path
            try:
                if route == "/":
                    self._send(200, "text/html; charset=utf-8", render_app_html().encode("utf-8"))
                elif route == "/api/state":
                    self._json(build_review_state(work_path, chunks_path, context))
                elif route == "/api/export":
                    body = work_path.read_bytes()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
                    self.send_header("Content-Disposition", f'attachment; filename="{work_path.name}"')
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                else:
                    self._send(404, "text/plain; charset=utf-8", b"Not found")
            except Exception as error:  # noqa: BLE001
                self._send(500, "text/plain; charset=utf-8", str(error).encode("utf-8"))

        def do_POST(self) -> None:  # noqa: N802
            """Recibe y valida una decisión humana para guardarla en la cola."""
            if urlparse(self.path).path != "/api/decision":
                self._send(404, "text/plain; charset=utf-8", b"Not found")
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length > 100_000:
                    raise ValueError("Solicitud demasiado grande")
                payload = json.loads(self.rfile.read(length))
                saved = save_human_decision(
                    work_path,
                    pool_id=payload["pool_id"],
                    grade=payload.get("grade"),
                    canonical=payload.get("canonical"),
                    note=payload.get("note", ""),
                    reviewer_id=reviewer_id,
                )
                self._json({"saved": saved})
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
                self._send(400, "text/plain; charset=utf-8", str(error).encode("utf-8"))

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
            """Registra la solicitud HTTP con la dirección del cliente."""
            print(f"{self.address_string()} - {format % args}")

    return ReviewHandler


def parse_args() -> argparse.Namespace:
    """Recoge las rutas de revisión, el revisor y la dirección del servidor."""
    root = Path(__file__).resolve().parents[1]
    frozen_pool = root / "outputs/explicitness_v2/pools/blind_review_queue.jsonl"
    parser = argparse.ArgumentParser(description="Interfaz de la cola ciega de explicitud v2")
    parser.add_argument("--work", type=Path, default=root / "outputs/local_runs/blind_review_queue_work.jsonl")
    parser.add_argument("--frozen-pool", type=Path, default=frozen_pool)
    parser.add_argument("--golden", type=Path, default=root / "data/golden/golden_set_pilot_v1_1.jsonl")
    parser.add_argument("--pairs", type=Path, default=root / "data/golden/variants/explicitness_pairs_v1_consolidated.jsonl")
    parser.add_argument("--chunks", type=Path, default=root / "data/processed/chunks_v1.jsonl")
    parser.add_argument("--reviewer-id", default="andres")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--no-browser", action="store_true")
    return parser.parse_args()


def main() -> None:
    """Prepara la copia local y arranca el servidor de revisión ciega."""
    args = parse_args()
    frozen_pool = args.frozen_pool.resolve()
    work = args.work.resolve()
    root = Path(__file__).resolve().parents[1].resolve()
    allowed = (root / "outputs/local_runs").resolve()
    if not work.is_relative_to(allowed):
        raise ValueError(f"La copia de trabajo debe vivir en outputs/local_runs/: {work}")
    if frozen_pool.exists() and frozen_pool.is_relative_to(allowed):
        raise ValueError("El pool congelado no puede residir en outputs/local_runs/")
    info = prepare_work_copy(frozen_pool, work)
    if info["created"]:
        print(f"Copia de trabajo creada: {work} ({info['units']} unidades)")
    else:
        print(f"Reanudando copia de trabajo existente: {work} ({info['units']} unidades)")
    context = load_golden_context(args.golden, args.pairs)
    build_review_state(work, args.chunks, context)  # validación temprana
    handler = make_handler(work, args.chunks, context, args.reviewer_id)
    server = ThreadingHTTPServer((args.host, args.port), handler)
    url = f"http://{args.host}:{args.port}"
    print(f"Cola ciega de explicitud: {url}")
    print(f"Copia de trabajo: {work}")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDetenida.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
