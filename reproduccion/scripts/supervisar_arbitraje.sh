#!/usr/bin/env bash
# Supervisor del arbitraje delegado de discrepancias (generación v3).
#
# Mismo patrón que supervisar_evaluacion.sh: carril desacoplado con `setsid`, detección de
# atasco por número de filas y relanzamiento por PID explícito (nunca `pkill -f`, que ya mató
# la shell que lo lanzaba). Objetivo: 158 casos resueltos.
set -uo pipefail

BASE="/home/ags/Documentos/Aprendizaje/0Master DS/ACTUAL/TFM/v2"
RUN="$BASE/outputs/local_runs/generation_scaling_v3"
ARB="$RUN/arbitraje_discrepancias_v3"
PY="$BASE/../.venv/bin/python"
SALIDA="$ARB/arbitraje_v3.jsonl"
TOTAL=158
VENCIMIENTO=480
REVISAR_CADA=120

CONTEO=-1
MARCA=$(date +%s)

conteo() { [ -f "$SALIDA" ] && grep -c . "$SALIDA" || echo 0; }

pid_de() {
  ps -eo pid,args | grep "[a]rbitrate_rag_discrepancies_v3.py" | grep -F "$SALIDA" | awk '{print $1; exit}'
}

matar() {
  local pj
  pj=$(pid_de)
  if [ -n "$pj" ] && [ "$pj" -gt 1 ] && [ "$pj" -ne "$$" ]; then
    kill "$pj" 2>/dev/null
    sleep 2
    kill -9 "$pj" 2>/dev/null
    echo "$(date +%T) árbitro detenido (pid $pj)"
  fi
}

levantar() {
  echo "$(date +%T) relanzando árbitro (faltan $((TOTAL - $(conteo))))"
  cd "$BASE" || exit 1
  setsid nohup "$PY" scripts/arbitrate_rag_discrepancies_v3.py \
    --output "$SALIDA" \
    --batches-dir "$ARB" \
    --model gpt-6-astra --provider openai-codex --reasoning high \
    --batch-size 5 >> "$ARB/log_arbitraje.txt" 2>&1 &
  sleep 2
}

echo "supervisor de arbitraje iniciado $(date +%T) — objetivo $TOTAL casos"
while :; do
  n=$(conteo)
  vivo=$(ps -eo args | grep -c "[a]rbitrate_rag_discrepancies_v3.py")

  if [ "$n" -ge "$TOTAL" ]; then
    echo "$(date +%T) COMPLETO — $n/$TOTAL"
    break
  fi

  if [ "$n" -ne "$CONTEO" ]; then
    CONTEO=$n; MARCA=$(date +%s)
    [ "$vivo" -eq 0 ] && levantar
  else
    transcurrido=$(( $(date +%s) - MARCA ))
    if [ "$transcurrido" -ge "$VENCIMIENTO" ]; then
      echo "$(date +%T) SIN AVANCE desde hace ${transcurrido}s ($n/$TOTAL)"
      [ "$vivo" -gt 0 ] && matar
      sleep 3
      levantar
      MARCA=$(date +%s)
    fi
  fi
  sleep "$REVISAR_CADA"
done

echo "$(date +%T) supervisión de arbitraje terminada — $(conteo)/$TOTAL"
