# Reproducción de los resultados

## 1. Preparar el entorno

Desde la raíz del repositorio:

```bash
cd reproduccion
uv sync --locked --group dev
uv run --no-sync jupyter lab notebooks
```

Se necesita Python 3.14 o superior. Las dependencias están fijadas en uv.lock. Los notebooks utilizan el intérprete de su kernel para ejecutar los scripts: seleccione el Python de reproduccion/.venv. No necesitan otra carpeta del TFM.

## 2. Recorrido principal: notebooks

El [índice de notebooks](reproduccion/notebooks/README.md) presenta cinco fases:

1. **Entorno, corpus y dataset:** fuentes, fragmentos y unidades del experimento final.
2. **Preguntas, evidencias y qrels:** formulaciones, comportamientos esperados y grados de relevancia.
3. **Recuperación y explicitud:** recálculo de las métricas y de los contrastes explícita–implícita a partir de rankings congelados.
4. **Respuestas, evaluación y decisiones:** cobertura, fallos, aplicabilidad y procedencia de las puntuaciones finales.
5. **Comparaciones finales y verificación:** reanálisis completo, soportes comunes, comparación de generadores y recuperadores y contraste de los 35 CSV.

Cada notebook puede ejecutarse de arriba abajo de forma independiente. Las explicaciones sitúan las fuentes antes de los cálculos y las tablas después. Los scripts siguen siendo la implementación única de las métricas y del análisis estadístico; no se duplican esas fórmulas en los cuadernos.

**Run All ejecuta los reanálisis offline previstos en el cuaderno.** Las salidas se guardan en directorios REPLAY_ nuevos bajo outputs/local_runs/final_experiment_20260930/. No se sobrescriben fuentes congeladas ni documentos. Las nuevas tablas se muestran desde el destino recién generado, no desde un resultado histórico indistinguible de la ejecución actual.

No se lanzan recuperación neuronal, generación, jueces remotos ni nuevas decisiones humanas. Los cuadernos de v2/notebooks, correspondientes a etapas anteriores, no son el recorrido de esta entrega ni una dependencia suya.

### Ejecución automática de todos los cuadernos

Desde reproduccion/:

```bash
uv run --no-sync python notebooks/verify_notebooks.py
```

El programa ejecuta los cinco notebooks en kernels nuevos con el mismo intérprete, rechaza errores y comprueba la ejecución de todas las celdas de código. Guarda las copias ejecutadas, el informe y las evidencias de reproducción en un destino REPLAY_ nuevo; no modifica los notebooks originales. No depende de un kernelspec local de la máquina del autor.

## 3. Alternativa equivalente por consola

Todos los comandos de esta sección se ejecutan desde reproduccion/, igual que las recetas incluidas en los apéndices.

### Validar tablas, evidencia y documentos

```bash
uv run --no-sync python scripts/validate_final_results.py
uv run --no-sync python docs/validar_apendices.py
```

Se verifican once tablas numéricas y 389 valores del contrato final. El validador técnico comprueba sus dos tablas y siete bloques shell. Los PDF se leen desde ../documentos/, incluido tfm_apendices_tecnicos_AndresGonzalezSanchez.pdf. No se renderizan ni se cambian los QMD. Los validadores editoriales históricos de otras versiones no definen la aceptación actual.

### Recalcular los resultados publicados

```bash
uv run --no-sync python scripts/reproduce_offline.py --run-id tribunal_01
```

El programa valida la evidencia y recalcula las métricas de recuperación, los contrastes de explicitud, la comparación de generadores y la comparación de recuperadores dentro de cada generador. Contrasta los **35 CSV byte a byte** con sus referencias congeladas.

El informe y las salidas se guardan en outputs/local_runs/final_experiment_20260930/REPLAY_tribunal_01/. Para repetirlo hay que elegir otro identificador. Estas carpetas están excluidas de Git.

### Pruebas de los componentes

```bash
uv run --no-sync python -m pytest -q tests docs/test_validar_apendices.py
```

Las pruebas no llaman a modelos ni proveedores. Algunas utilizan destinos temporales o un servidor HTTP local. La ejecución completa de los notebooks se comprueba por separado con el verificador anterior.

## 4. Figuras sin renderizar las memorias

Se necesita R con dplyr, ggplot2, jsonlite, knitr y tibble. El cuaderno final permite activar expresamente esta etapa opcional. También puede ejecutarse por consola:

```bash
uv run --no-sync python scripts/reproduce_figures.py --run-id tribunal_01
```

Se extraen y ejecutan literalmente los nueve bloques R de la memoria y los dos del sponsor. Se generan diez SVG, sin modificar los QMD ni los PDF. El diagrama general es un recurso estático en figures/rag_simple.svg.

El registro histórico de R está en docs/render_environment_20260930.json. No constituye un lock de R; no se afirma una instalación limpia de R ni identidad binaria de los SVG entre entornos gráficos diferentes.

## 5. Qué se reproduce y qué queda fuera

| Operación | Incluida en Run All |
|---|---|
| Inspeccionar corpus, preguntas, qrels y respuestas incluidas | Sí |
| Recalcular resultados desde rankings y puntuaciones congeladas | Sí, en los cuadernos de análisis |
| Contrastar los 35 CSV y validar documentos | Sí, en el cuaderno final |
| Regenerar las figuras con R | Opcional, desactivado por defecto |
| Volver a extraer corpus o ejecutar modelos de recuperación | No |
| Generar respuestas o solicitar nuevos juicios | No |
| Repetir adjudicación humana | No |
| Renderizar memorias o apéndices | No |

Una nueva inferencia necesita los entornos de environments/, pesos de modelos, hardware compatible y Ollama o los proveedores correspondientes. No se distribuyen pesos, cachés, sesiones ni credenciales. La semilla fija y la temperatura cero no garantizan respuestas originales idénticas.

Las comparaciones de calidad utilizan soporte común y agregación por pregunta base. Los fallos de generación y los juicios no aplicables se muestran por separado; no se convierten en ceros ni se imputan. Los tiempos registrados no equivalen a un benchmark end-to-end controlado ni a coste monetario.

## 6. Evidencia de comprobación

[verification/README.md](verification/README.md) distingue los informes históricos de la comprobación de los notebooks actuales. La verificación de esta entrega utiliza una copia reubicada; los mecanismos y límites de bloqueo de rutas y red se detallan en el informe correspondiente. Una guarda Python no es aislamiento del sistema operativo y no restringe R.

Se mantienen los registros históricos de procedencia, con sus rutas originales, y los metadatos científicos necesarios para los validadores. No se requiere un manifiesto global de integridad para utilizar el repositorio.
