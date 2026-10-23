from __future__ import annotations

import argparse
import json
import os
import tempfile
import webbrowser
from collections import defaultdict
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

CONDITION_ORDER = {"bm25": 0, "dense": 1, "rrf": 2, "rrf_rerank": 3}
FAITHFULNESS_VALUES = {
    "supported",
    "partially_supported",
    "unsupported",
    "not_applicable",
}
FACTUAL_VALUES = {"correct", "partially_correct", "incorrect", "not_applicable"}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Carga la cola JSONL y comprueba que cada registro sea un objeto."""
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


def _atomic_write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    """Guarda la cola mediante un temporal sincronizado y una sustitución atómica."""
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


def _validate_decision(decision: dict[str, Any]) -> dict[str, Any]:
    """Valida las tres valoraciones humanas y normaliza la nota de revisión."""
    faithfulness = decision.get("faithfulness_assessment")
    factual = decision.get("factual_correctness_assessment")
    behavior = decision.get("behavior_score")
    if faithfulness not in FAITHFULNESS_VALUES:
        raise ValueError("invalid faithfulness assessment")
    if factual not in FACTUAL_VALUES:
        raise ValueError("invalid factual correctness assessment")
    if behavior not in {0, 1, 2}:
        raise ValueError("behavior score must be 0, 1 or 2")
    return {
        "faithfulness_assessment": faithfulness,
        "factual_correctness_assessment": factual,
        "behavior_score": behavior,
        "notes": str(decision.get("notes", "")).strip(),
    }


def save_human_adjudications(
    path: Path,
    *,
    qid: str,
    decisions: dict[str, dict[str, Any]],
    reviewer_id: str,
    reviewed_at: str | None = None,
) -> list[dict[str, Any]]:
    """Guarda juntas las adjudicaciones de todas las condiciones de una pregunta."""
    rows = load_jsonl(path)
    targets = [row for row in rows if row.get("qid") == qid]
    expected_conditions = {row["retrieval_condition"] for row in targets}
    if not targets:
        raise ValueError(f"unknown qid: {qid}")
    if set(decisions) != expected_conditions:
        raise ValueError("decision conditions must exactly match queued conditions for qid")

    validated = {
        condition: _validate_decision(decision)
        for condition, decision in decisions.items()
    }
    timestamp = reviewed_at or datetime.now().astimezone().isoformat(timespec="seconds")
    for row in targets:
        decision = validated[row["retrieval_condition"]]
        current = row.get("human_adjudication", {})
        unchanged = current.get("status") == "adjudicated" and all(
            # El autoguardado no renueva la fecha de decisiones que no han cambiado.
            current.get(field) == value for field, value in decision.items()
        )
        if unchanged:
            continue
        row["human_adjudication"] = {
            "status": "adjudicated",
            **decision,
            "reviewer_id": reviewer_id,
            "reviewed_at": timestamp,
        }
    _atomic_write_jsonl(path, rows)
    return targets


def restore_human_adjudications(
    path: Path,
    *,
    qid: str,
    decisions: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Restaura para una pregunta los estados previos, incluidos los pendientes."""
    rows = load_jsonl(path)
    targets = [row for row in rows if row.get("qid") == qid]
    expected_conditions = {row["retrieval_condition"] for row in targets}
    if not targets:
        raise ValueError(f"unknown qid: {qid}")
    if set(decisions) != expected_conditions:
        raise ValueError("restore conditions must exactly match queued conditions for qid")

    normalized: dict[str, dict[str, Any]] = {}
    for condition, decision in decisions.items():
        status = decision.get("status")
        if status == "pending":
            normalized[condition] = {
                "status": "pending",
                "faithfulness_assessment": None,
                "factual_correctness_assessment": None,
                "behavior_score": None,
                "notes": None,
            }
        elif status == "adjudicated":
            reviewer_id = str(decision.get("reviewer_id", "")).strip()
            reviewed_at = str(decision.get("reviewed_at", "")).strip()
            if not reviewer_id or not reviewed_at:
                raise ValueError("adjudicated restore requires reviewer_id and reviewed_at")
            normalized[condition] = {
                "status": "adjudicated",
                **_validate_decision(decision),
                "reviewer_id": reviewer_id,
                "reviewed_at": reviewed_at,
            }
        else:
            raise ValueError("restore status must be pending or adjudicated")

    for row in targets:
        row["human_adjudication"] = normalized[row["retrieval_condition"]]
    _atomic_write_jsonl(path, rows)
    return targets


def _judge_view(judge: dict[str, Any]) -> dict[str, Any]:
    """Selecciona las puntuaciones, la justificación y los errores del juez auxiliar."""
    return {
        "faithfulness": judge.get("faithfulness"),
        "factual_correctness": judge.get("factual_correctness"),
        "behavior_score": judge.get("behavior_judge_score"),
        "behavior_rationale": judge.get("behavior_judge_rationale"),
        "evaluation_errors": judge.get("evaluation_errors", []),
    }


def build_review_state(path: Path) -> dict[str, Any]:
    """Agrupa la cola por pregunta y resume el avance de la adjudicación por condición."""
    rows = load_jsonl(path)
    keys = [(row["retrieval_condition"], row["qid"]) for row in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate retrieval condition and qid")

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["qid"]].append(row)

    questions = []
    for qid in sorted(grouped):
        source_conditions = sorted(
            grouped[qid],
            key=lambda row: (
                CONDITION_ORDER.get(row["retrieval_condition"], 99),
                row["retrieval_condition"],
            ),
        )
        conditions = [
            {
                **row,
                "judges": {
                    "Gemma 3 4B": _judge_view(row.get("gemma3_4b", {})),
                    "GLM 5.3 Flash (low)": _judge_view(
                        row.get("glm53flash_low", {})
                    ),
                },
            }
            for row in source_conditions
        ]
        first = conditions[0]
        questions.append(
            {
                "qid": qid,
                "question": first["question"],
                "answerability": first.get("answerability"),
                "expected_behavior": first.get("expected_behavior"),
                "reference": first.get("reference"),
                "conditions": conditions,
            }
        )

    reviewed_pairs = sum(
        row.get("human_adjudication", {}).get("status") == "adjudicated"
        for row in rows
    )
    reviewed_questions = sum(
        all(
            row.get("human_adjudication", {}).get("status") == "adjudicated"
            for row in item["conditions"]
        )
        for item in questions
    )
    return {
        "questions": questions,
        "summary": {
            "total_pairs": len(rows),
            "reviewed_pairs": reviewed_pairs,
            "pending_pairs": len(rows) - reviewed_pairs,
            "total_questions": len(questions),
            "reviewed_questions": reviewed_questions,
            "pending_questions": len(questions) - reviewed_questions,
        },
    }


def render_app_html() -> str:
    """Devuelve la interfaz de auditoría RAG con comparación de condiciones y autoguardado."""
    return r"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Auditoría humana de respuestas RAG</title>
  <style>
    :root { color-scheme:light dark; --bg:#f4f6f8; --card:#fff; --fg:#18212f; --muted:#667085; --border:#d7dde5; --accent:#275bc7; --ok:#08795b; --warn:#a15c00; --bad:#b42318; }
    @media (prefers-color-scheme:dark) { :root { --bg:#10141b; --card:#181e27; --fg:#eef2f6; --muted:#a5afbf; --border:#344050; --accent:#7da5ff; --ok:#67d5b5; --warn:#efb45c; --bad:#ff8b83; } }
    * { box-sizing:border-box; }
    body { margin:0; background:var(--bg); color:var(--fg); font:15px/1.5 system-ui,-apple-system,sans-serif; }
    header { position:sticky; top:0; z-index:5; border-bottom:1px solid var(--border); background:color-mix(in srgb,var(--bg) 93%,transparent); backdrop-filter:blur(9px); }
    .top { max-width:1680px; margin:auto; padding:11px 18px; display:flex; gap:14px; align-items:center; flex-wrap:wrap; }
    h1 { margin:0; font-size:19px; }
    .progress { flex:1; min-width:260px; }
    progress { width:100%; height:9px; accent-color:var(--accent); }
    .toolbar { display:flex; gap:8px; flex-wrap:wrap; }
    button, select, textarea { font:inherit; color:inherit; }
    button, select { border:1px solid var(--border); background:var(--card); border-radius:8px; padding:7px 10px; }
    button { cursor:pointer; }
    button:hover { border-color:var(--accent); }
    main { max-width:1680px; margin:auto; padding:18px; }
    .question-card, .condition-card, .guide { background:var(--card); border:1px solid var(--border); border-radius:12px; }
    .question-card { padding:16px 18px; margin-bottom:14px; }
    .badges { display:flex; gap:7px; flex-wrap:wrap; margin-bottom:8px; }
    .badge { border:1px solid var(--border); border-radius:999px; padding:2px 8px; color:var(--muted); font-size:12px; }
    #question { margin:5px 0 11px; font-size:21px; font-weight:680; }
    .reference { border-left:3px solid var(--accent); padding:8px 11px; background:color-mix(in srgb,var(--accent) 7%,var(--card)); }
    #condition-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; align-items:start; }
    .condition-card { padding:16px; min-width:0; }
    .condition-card h2 { margin:0 0 8px; font-size:18px; }
    .reason-list { color:var(--warn); font-size:13px; margin:7px 0 11px; }
    .response { white-space:pre-wrap; padding:12px; border:1px solid var(--border); border-radius:8px; background:color-mix(in srgb,var(--bg) 68%,var(--card)); }
    details { margin-top:10px; border-top:1px solid var(--border); padding-top:9px; }
    summary { cursor:pointer; font-weight:650; }
    pre { max-height:320px; overflow:auto; white-space:pre-wrap; word-break:break-word; font:13px/1.5 ui-monospace,monospace; }
    .metric-table { width:100%; border-collapse:collapse; margin-top:8px; font-size:13px; }
    .metric-table th, .metric-table td { border-bottom:1px solid var(--border); padding:5px; text-align:left; vertical-align:top; }
    .rationale { color:var(--muted); margin:6px 0 12px; }
    .decision { margin-top:13px; padding-top:12px; border-top:2px solid var(--border); }
    .field { margin:9px 0; }
    .field label { display:block; font-weight:650; margin-bottom:4px; }
    .field select, textarea { width:100%; border:1px solid var(--border); background:var(--bg); border-radius:8px; padding:8px; }
    textarea { min-height:72px; resize:vertical; }
    .behavior-buttons { display:grid; grid-template-columns:repeat(3,1fr); gap:7px; }
    .behavior-buttons button { font-weight:750; }
    .behavior-buttons button.selected { outline:3px solid var(--accent); outline-offset:1px; }
    .actions { position:sticky; bottom:0; margin-top:14px; padding:10px; display:flex; gap:8px; justify-content:center; flex-wrap:wrap; border:1px solid var(--border); border-radius:12px; background:color-mix(in srgb,var(--bg) 92%,transparent); backdrop-filter:blur(9px); }
    .primary { background:var(--accent); border-color:var(--accent); color:white; font-weight:700; }
    #status { min-width:220px; align-self:center; color:var(--ok); }
    .guide { margin-top:14px; padding:12px 16px; color:var(--muted); font-size:13px; }
    .guide ul { margin:7px 0; }
    kbd { border:1px solid var(--border); border-bottom-width:2px; border-radius:4px; padding:1px 5px; background:var(--bg); font:11px ui-monospace,monospace; }
    .empty { padding:70px 20px; text-align:center; color:var(--muted); }
    @media (max-width:980px) { #condition-grid { grid-template-columns:1fr; } .actions { position:static; } }
  </style>
</head>
<body>
<header><div class="top">
  <h1>Auditoría humana de respuestas RAG</h1>
  <div class="progress"><div id="progress-label">Cargando…</div><progress id="progress" value="0" max="1"></progress></div>
  <div class="toolbar">
    <select id="qid-filter"><option value="all">Todos los qids</option></select>
    <select id="status-filter"><option value="pending">Pendientes</option><option value="all">Todos</option><option value="reviewed">Revisados</option></select>
    <button id="export">Exportar JSONL</button>
  </div>
</div></header>
<main>
  <section id="empty-state" class="empty" hidden>No hay preguntas con estos filtros.</section>
  <div id="review-content">
    <section class="question-card">
      <div class="badges"><span class="badge" id="position"></span><span class="badge" id="qid"></span><span class="badge" id="answerability"></span><span class="badge" id="expected-behavior"></span></div>
      <div id="question"></div>
      <div class="reference"><strong>Referencia</strong><div id="reference"></div></div>
    </section>
    <section id="condition-grid"></section>
    <section class="actions">
      <button id="previous">← Anterior</button>
      <button class="primary" id="save-next">Guardar qid y siguiente <kbd>Enter</kbd></button>
      <button id="next">Siguiente →</button>
      <button id="undo">Deshacer <kbd>U</kbd></button>
      <button id="clear">Dejar qid pendiente</button>
      <span id="status"></span>
    </section>
    <details class="guide" open><summary>Guía de adjudicación</summary>
      <ul>
        <li><strong>Faithfulness:</strong> supported, partially_supported, unsupported o not_applicable. En abstenciones breves suele ser not_applicable.</li>
        <li><strong>Factual Correctness:</strong> correct, partially_correct, incorrect o not_applicable. En abstenciones sin referencia evaluable es not_applicable.</li>
        <li><strong>Conducta 0/1/2:</strong> incorrecta, parcial o plenamente conforme con el comportamiento esperado.</li>
        <li>Evalúa la respuesta y la evidencia; las opiniones de Gemma 3 4B y GLM 5.3 Flash son auxiliares y están plegadas.</li>
      </ul>
      <div><strong>Autosave:</strong> se activa al completar las tres decisiones de todas las condiciones visibles.</div>
      <div><kbd>0</kbd> <kbd>1</kbd> <kbd>2</kbd> conducta · <kbd>N</kbd> nota · <kbd>Enter</kbd> guardar · <kbd>←</kbd> <kbd>→</kbd> navegar · <kbd>U</kbd> deshacer</div>
    </details>
  </div>
</main>

<template id="condition-template">
  <article class="condition-card">
    <h2 data-role="condition-title"></h2>
    <div class="reason-list" data-role="reasons"></div>
    <strong>Respuesta</strong><div class="response" data-role="response"></div>
    <details><summary>Contextos recuperados</summary><pre data-role="contexts"></pre></details>
    <details><summary>Gemma 3 4B y GLM 5.3 Flash</summary>
      <table class="metric-table"><thead><tr><th>Métrica</th><th>Gemma</th><th>GLM</th></tr></thead><tbody data-role="metrics"></tbody></table>
      <h3>Gemma 3 4B</h3><p class="rationale" data-role="gemma-rationale"></p>
      <h3>GLM 5.3 Flash</h3><p class="rationale" data-role="glm-rationale"></p>
    </details>
    <div class="decision">
      <strong>Decisión humana</strong>
      <div class="field"><label>Faithfulness</label><select data-field="faithfulness_assessment"><option value="">Seleccionar…</option><option value="supported">supported</option><option value="partially_supported">partially_supported</option><option value="unsupported">unsupported</option><option value="not_applicable">not_applicable</option></select></div>
      <div class="field"><label>Factual Correctness</label><select data-field="factual_correctness_assessment"><option value="">Seleccionar…</option><option value="correct">correct</option><option value="partially_correct">partially_correct</option><option value="incorrect">incorrect</option><option value="not_applicable">not_applicable</option></select></div>
      <div class="field"><label>Conducta</label><div class="behavior-buttons"><button data-behavior="0">0</button><button data-behavior="1">1</button><button data-behavior="2">2</button></div></div>
      <div class="field"><label>Notas</label><textarea data-field="notes" placeholder="Justifica desacuerdos o decisiones parciales"></textarea></div>
    </div>
  </article>
</template>

<script>
let allQuestions = [], visible = [], index = 0, activeCard = 0, undoStack = [], autosaveTimer = null, saving = false;
const $ = id => document.getElementById(id);
const text = value => value == null ? '—' : String(value);
const el = (tag, value) => { const node=document.createElement(tag); node.textContent=text(value); return node; };

async function loadState(preferredQid=null) {
  const response = await fetch('/api/state');
  if (!response.ok) throw new Error(await response.text());
  const state = await response.json(); allQuestions = state.questions;
  const select=$('qid-filter'), prior=select.value;
  select.replaceChildren(new Option('Todos los qids','all'), ...allQuestions.map(q=>new Option(q.qid,q.qid)));
  if ([...select.options].some(o=>o.value===prior)) select.value=prior;
  setSummary(state.summary);
  applyFilters(preferredQid);
}

function setSummary(summary) {
  $('progress').max=summary.total_pairs || 1; $('progress').value=summary.reviewed_pairs;
  $('progress-label').textContent=`${summary.reviewed_pairs}/${summary.total_pairs} pares · ${summary.reviewed_questions}/${summary.total_questions} preguntas completas`;
}

async function refreshSummary() {
  const response=await fetch('/api/state'); if(!response.ok)throw new Error(await response.text());
  setSummary((await response.json()).summary);
}

function isReviewed(question) { return question.conditions.every(c=>c.human_adjudication?.status==='adjudicated'); }
function applyFilters(preferredQid=null) {
  const qid=$('qid-filter').value, status=$('status-filter').value;
  visible=allQuestions.filter(q=>(qid==='all'||q.qid===qid)&&(status==='all'||(status==='pending'?!isReviewed(q):isReviewed(q))));
  if (preferredQid) { const found=visible.findIndex(q=>q.qid===preferredQid); index=found>=0?found:Math.min(index,Math.max(0,visible.length-1)); }
  else index=Math.min(index,Math.max(0,visible.length-1));
  render();
}

function setBehavior(card, value) {
  card.dataset.behavior=value == null ? '' : String(value);
  card.querySelectorAll('[data-behavior]').forEach(button=>button.classList.toggle('selected',Number(button.dataset.behavior)===value));
}

const conditionLabels={'bm25':'BM25','dense':'Dense','rrf':'RRF','rrf_rerank':'RRF + reranking'};
function metricRow(name, left, right) { const tr=document.createElement('tr'); tr.append(el('td',name),el('td',left),el('td',right)); return tr; }
function renderCondition(condition, position) {
  const fragment=$('condition-template').content.cloneNode(true), card=fragment.querySelector('.condition-card');
  card.dataset.condition=condition.retrieval_condition; card.addEventListener('click',()=>{activeCard=position;});
  card.querySelector('[data-role="condition-title"]').textContent=conditionLabels[condition.retrieval_condition]||condition.retrieval_condition;
  card.querySelector('[data-role="reasons"]').textContent=`Prioridad: ${(condition.priority_reasons||[]).join(' · ')}`;
  card.querySelector('[data-role="response"]').textContent=condition.response;
  card.querySelector('[data-role="contexts"]').textContent=(condition.retrieved_contexts||[]).map((c,i)=>`[${condition.retrieved_chunk_ids?.[i]||i+1}]\n${c}`).join('\n\n');
  const metrics=card.querySelector('[data-role="metrics"]'), gemma=condition.gemma3_4b||{}, glm=condition.glm53flash_low||{};
  metrics.append(metricRow('Faithfulness',gemma.faithfulness,glm.faithfulness),metricRow('Factual Correctness',gemma.factual_correctness,glm.factual_correctness),metricRow('Conducta',gemma.behavior_judge_score,glm.behavior_judge_score));
  card.querySelector('[data-role="gemma-rationale"]').textContent=gemma.behavior_judge_rationale||'Sin justificación';
  card.querySelector('[data-role="glm-rationale"]').textContent=glm.behavior_judge_rationale||'Sin justificación';
  const human=condition.human_adjudication||{};
  card.querySelector('[data-field="faithfulness_assessment"]').value=human.faithfulness_assessment||'';
  card.querySelector('[data-field="factual_correctness_assessment"]').value=human.factual_correctness_assessment||'';
  card.querySelector('[data-field="notes"]').value=human.notes||''; setBehavior(card,human.behavior_score);
  card.querySelectorAll('select,textarea').forEach(control=>{control.addEventListener('change',scheduleAutosave);control.addEventListener('input',scheduleAutosave);});
  return fragment;
}

function render() {
  clearTimeout(autosaveTimer);
  const q=visible[index]; $('empty-state').hidden=Boolean(q); $('review-content').hidden=!q; if(!q)return;
  $('position').textContent=`${index+1} de ${visible.length}`; $('qid').textContent=q.qid; $('answerability').textContent=q.answerability; $('expected-behavior').textContent=`esperado: ${q.expected_behavior}`;
  $('question').textContent=q.question; $('reference').textContent=q.reference||'Sin respuesta de referencia';
  const grid=$('condition-grid'); grid.replaceChildren(...q.conditions.map(renderCondition)); activeCard=0; $('status').textContent='';
}

function collectDecisions() {
  const decisions={};
  document.querySelectorAll('.condition-card').forEach(card=>{ decisions[card.dataset.condition]={faithfulness_assessment:card.querySelector('[data-field="faithfulness_assessment"]').value,factual_correctness_assessment:card.querySelector('[data-field="factual_correctness_assessment"]').value,behavior_score:card.dataset.behavior===''?null:Number(card.dataset.behavior),notes:card.querySelector('[data-field="notes"]').value}; });
  return decisions;
}

async function post(route,payload) { const response=await fetch(route,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}); if(!response.ok)throw new Error(await response.text()); return response.json(); }
function decisionsComplete(decisions) { return Object.values(decisions).every(d=>d.faithfulness_assessment&&d.factual_correctness_assessment&&[0,1,2].includes(d.behavior_score)); }
function scheduleAutosave() {
  clearTimeout(autosaveTimer); const decisions=collectDecisions(); if(!decisionsComplete(decisions))return;
  $('status').textContent='Autosave pendiente…'; autosaveTimer=setTimeout(()=>saveCurrent(false),700);
}
async function saveCurrent(advance=true) {
  clearTimeout(autosaveTimer); if(saving)return; const q=visible[index]; if(!q)return; const decisions=collectDecisions();
  const prior=Object.fromEntries(q.conditions.map(c=>[c.retrieval_condition,c.human_adjudication])); saving=true;
  try {
    await post('/api/adjudications',{qid:q.qid,decisions}); undoStack.push({qid:q.qid,decisions:prior});
    q.conditions.forEach(c=>{c.human_adjudication={status:'adjudicated',...decisions[c.retrieval_condition]};});
    if(advance){const next=visible[index+1]?.qid;await loadState(next);$('status').textContent='Guardado de forma atómica.';}
    else{await refreshSummary();$('status').textContent='Autosave completado.';}
  } catch(error) { $('status').textContent=error.message; }
  finally { saving=false; }
}
async function undoLast() { const prior=undoStack.pop(); if(!prior){$('status').textContent='No hay cambios de esta sesión.';return;} try{await post('/api/restore',prior);await loadState(prior.qid);$('status').textContent='Último qid restaurado.';}catch(error){$('status').textContent=error.message;} }
async function clearCurrent() { const q=visible[index]; if(!q)return; const decisions=Object.fromEntries(q.conditions.map(c=>[c.retrieval_condition,{status:'pending',faithfulness_assessment:null,factual_correctness_assessment:null,behavior_score:null,notes:null}])); try{await post('/api/restore',{qid:q.qid,decisions});await loadState(q.qid);$('status').textContent='Pregunta pendiente.';}catch(error){$('status').textContent=error.message;} }

document.addEventListener('click',event=>{ const button=event.target.closest('[data-behavior]'); if(button){const card=button.closest('.condition-card');activeCard=[...document.querySelectorAll('.condition-card')].indexOf(card);setBehavior(card,Number(button.dataset.behavior));scheduleAutosave();} });
$('save-next').addEventListener('click',()=>saveCurrent(true)); $('undo').addEventListener('click',undoLast); $('clear').addEventListener('click',clearCurrent);
$('previous').addEventListener('click',()=>{if(index>0){index--;render();}}); $('next').addEventListener('click',()=>{if(index+1<visible.length){index++;render();}});
$('qid-filter').addEventListener('change',()=>{index=0;applyFilters();}); $('status-filter').addEventListener('change',()=>{index=0;applyFilters();}); $('export').addEventListener('click',()=>{window.location='/api/export';});
document.addEventListener('keydown',event=>{ const editing=['TEXTAREA','SELECT','INPUT'].includes(document.activeElement.tagName); if(editing&&event.key!=='Escape'&&!(event.ctrlKey&&event.key==='Enter'))return; const cards=[...document.querySelectorAll('.condition-card')],card=cards[activeCard]; if(event.key==='0'){setBehavior(card,0);scheduleAutosave();} else if(event.key==='1'){setBehavior(card,1);scheduleAutosave();} else if(event.key==='2'){setBehavior(card,2);scheduleAutosave();} else if(event.key.toLowerCase()==='n')card?.querySelector('[data-field="notes"]').focus(); else if(event.key==='Enter')saveCurrent(true); else if(event.key==='ArrowLeft'&&index>0){index--;render();} else if(event.key==='ArrowRight'&&index+1<visible.length){index++;render();} else if(event.key.toLowerCase()==='u')undoLast(); else if(event.key==='Escape')document.activeElement.blur(); });
loadState().catch(error=>{document.body.replaceChildren(el('p',`No se pudo cargar la aplicación: ${error.message}`));});
</script>
</body></html>"""


def make_handler(path: Path, reviewer_id: str) -> type[BaseHTTPRequestHandler]:
    """Crea el manejador HTTP de la cola de respuestas y sus adjudicaciones."""
    class ReviewHandler(BaseHTTPRequestHandler):
        def _send(self, status: int, content_type: str, body: bytes) -> None:
            """Envía una respuesta HTTP con su longitud y sin caché."""
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, value: Any, status: int = 200) -> None:
            """Envía el valor serializado como JSON al navegador."""
            self._send(
                status,
                "application/json; charset=utf-8",
                json.dumps(value, ensure_ascii=False).encode("utf-8"),
            )

        def do_GET(self) -> None:  # noqa: N802
            """Sirve la interfaz, el estado de adjudicación o la exportación de la cola."""
            route = urlparse(self.path).path
            try:
                if route == "/":
                    self._send(
                        200,
                        "text/html; charset=utf-8",
                        render_app_html().encode("utf-8"),
                    )
                elif route == "/api/state":
                    self._json(build_review_state(path))
                elif route == "/api/export":
                    body = path.read_bytes()
                    self.send_response(200)
                    self.send_header(
                        "Content-Type", "application/x-ndjson; charset=utf-8"
                    )
                    self.send_header(
                        "Content-Disposition", f'attachment; filename="{path.name}"'
                    )
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                else:
                    self._send(404, "text/plain; charset=utf-8", b"Not found")
            except Exception as error:
                self._send(
                    500,
                    "text/plain; charset=utf-8",
                    str(error).encode("utf-8"),
                )

        def do_POST(self) -> None:  # noqa: N802
            """Guarda o restaura las decisiones de una pregunta tras validar la solicitud."""
            route = urlparse(self.path).path
            if route not in {"/api/adjudications", "/api/restore"}:
                self._send(404, "text/plain; charset=utf-8", b"Not found")
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length > 200_000:
                    raise ValueError("Request too large")
                payload = json.loads(self.rfile.read(length))
                if route == "/api/adjudications":
                    saved = save_human_adjudications(
                        path,
                        qid=payload["qid"],
                        decisions=payload["decisions"],
                        reviewer_id=reviewer_id,
                    )
                else:
                    saved = restore_human_adjudications(
                        path,
                        qid=payload["qid"],
                        decisions=payload["decisions"],
                    )
                self._json({"saved_count": len(saved)})
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
                self._send(400, "text/plain; charset=utf-8", str(error).encode("utf-8"))

        def log_message(self, format: str, *args: Any) -> None:
            """Escribe el registro HTTP con la dirección del cliente."""
            print(f"{self.address_string()} - {format % args}")

    return ReviewHandler


def parse_args() -> argparse.Namespace:
    """Recoge la cola, el revisor y las opciones del servidor de auditoría."""
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Local RAG response adjudication app")
    parser.add_argument(
        "--input",
        type=Path,
        default=root
        / "outputs/rag_eval/rag_judge_sensitivity_gemma3_4b_vs_glm53flash_low_human_risk_queue_v1_22q.jsonl",
    )
    parser.add_argument("--reviewer-id", default="andres")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--no-browser", action="store_true")
    return parser.parse_args()


def main() -> None:
    """Comprueba la copia de trabajo e inicia la auditoría RAG en localhost."""
    args = parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="rag_review_app")
    if args.host != "127.0.0.1":
        raise ValueError("The review app must bind to 127.0.0.1")
    if not args.input.is_file():
        raise FileNotFoundError(args.input)
    server = ThreadingHTTPServer(
        (args.host, args.port), make_handler(args.input, args.reviewer_id)
    )
    url = f"http://{args.host}:{args.port}"
    print(f"RAG review app: {url}")
    print(f"Working file: {args.input}")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
