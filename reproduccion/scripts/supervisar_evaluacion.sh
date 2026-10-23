#!/usr/bin/env bash
# Supervisor de la evaluación de generación.
#
# Los evaluadores remotos se caen con regularidad —`hermes chat` devuelve error vacío,
# o la sesión desde la que se lanzaron muere— y hasta ahora cada caída costaba un
# relanzamiento a mano. Este guion desacopla los procesos con `setsid` y los relanza
# solos si no avanzan, de modo que la campaña cierra sin intervención.
#
# Uso: bash supervisar_evaluacion.sh
set -uo pipefail

BASE="/home/ags/Documentos/Aprendizaje/0Master DS/ACTUAL/TFM/v2"
RUN="$BASE/outputs/local_runs/generation_scaling_v3"
PY="$BASE/../.venv/bin/python"
TOTAL=604
VENCIMIENTO=480        # segundos sin avanzar antes de relanzar
REVISAR_CADA=120

IN=(
  rag_bm25_top5_qwen35_4b rag_dense_top5_qwen35_4b rag_rrf_top5_qwen35_4b rag_rerank_top5_qwen35_4b
  rag_bm25_top5_gemma4_e4b rag_dense_top5_gemma4_e4b rag_rrf_top5_gemma4_e4b rag_rerank_top5_gemma4_e4b
  rag_bm25_top5_qwen35_9b rag_dense_top5_qwen35_9b rag_rrf_top5_qwen35_9b rag_rerank_top5_qwen35_9b
)
ARGS=()
for s in "${IN[@]}"; do ARGS+=("$RUN/$s.jsonl"); done

declare -A SALIDA=(
  [A]="$RUN/eval_verdicts_v3.jsonl"
  [B]="$RUN/eval_verdicts_v3_juezB.jsonl"
)
declare -A MODELO=( [A]="gpt-6-sol" [B]="mimo-v2.6-pro" )
declare -A PROVEEDOR=( [A]="openai-codex" [B]="opencode-go" )
declare -A LOTE=( [A]="10" [B]="10" )
declare -A EXTRA=( [A]="--reasoning high" [B]="" )
declare -A CONTEO=( [A]="-1" [B]="-1" )
declare -A MARCA=( [A]="0" [B]="0" )
declare -A PID=( [A]="" [B]="" )

conteo_de() {
  [ -f "${SALIDA[$1]}" ] && grep -c . "${SALIDA[$1]}" || echo 0
}

# El PID se resuelve por línea de proceso exacta y se mata por número: `pkill -f` con un
# patrón amplio ya mató la shell que lo lanzaba y al propio supervisor.
pid_de() {
  ps -eo pid,args | grep "[e]valuate_rag_remote_v3.py.*${SALIDA[$1]}" | awk '{print $1; exit}'
}

matar() {
  local pj
  pj=$(pid_de "$1")
  if [ -n "$pj" ] && [ "$pj" -gt 1 ] && [ "$pj" -ne "$$" ]; then
    kill "$pj" 2>/dev/null
    sleep 2
    kill -9 "$pj" 2>/dev/null
    echo "$(date +%T) [$1] evaluador detenido (pid $pj)"
  fi
}

levantar() {
  local j=$1
  echo "$(date +%T) [$j] relanzando ${MODELO[$j]} (faltan $((TOTAL - $(conteo_de $j))))"
  cd "$BASE" || exit 1
  setsid nohup "$PY" scripts/evaluate_rag_remote_v3.py \
    --inputs "${ARGS[@]}" \
    --batches-dir "$RUN/eval_batches" \
    --output "${SALIDA[$j]}" \
    --model "${MODELO[$j]}" --provider "${PROVEEDOR[$j]}" \
    --batch-size "${LOTE[$j]}" ${EXTRA[$j]} \
    --subdir "supervisor_${j}" >> "$RUN/log_supervisor_${j}.txt" 2>&1 &
  sleep 2
  PID[$j]=$(pid_de "$j")
}

echo "supervisor iniciado $(date +%T) — objetivo $TOTAL celdas por juez"
while :; do
  for j in A B; do
    n=$(conteo_de "$j")
    vivo=$(ps -eo args | grep -c "[e]valuate_rag_remote_v3.py.*${SALIDA[$j]}")

    if [ "$n" -ge "$TOTAL" ]; then
      echo "$(date +%T) [$j] COMPLETO — $n/$TOTAL"
      continue
    fi

    if [ "$n" -ne "${CONTEO[$j]}" ]; then
      CONTEO[$j]=$n; MARCA[$j]=$(date +%s)      # ha avanzado: se reinicia el reloj
      [ "$vivo" -eq 0 ] && levantar "$j"
    else
      transcurrido=$(( $(date +%s) - MARCA[$j] ))
      if [ "$transcurrido" -ge "$VENCIMIENTO" ]; then
        echo "$(date +%T) [$j] SIN AVANCE desde hace ${transcurrido}s ($n/$TOTAL)"
        [ "$vivo" -gt 0 ] && matar "$j"
        sleep 3
        levantar "$j"
        MARCA[$j]=$(date +%s)
      fi
    fi
  done

  # salen los dos juntos: evita que el bucle siga solo con uno
  [ "$(conteo_de A)" -ge "$TOTAL" ] && [ "$(conteo_de B)" -ge "$TOTAL" ] && break
  sleep "$REVISAR_CADA"
done

echo "$(date +%T) supervisión terminada — A $(conteo_de A)/$TOTAL · B $(conteo_de B)/$TOTAL"
