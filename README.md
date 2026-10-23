# Comparación de técnicas de recuperación de información en un sistema RAG educativo

**Andrés González Sánchez · Máster en Data Science y Big Data · Universidad de Sevilla**

Este repositorio contiene los documentos del TFM y los materiales para reproducir sus resultados. Los notebooks explican las fases del análisis y ejecutan los cálculos mediante los scripts incluidos.

## Leer la entrega

| Documento | Contenido |
|---|---|
| [Memoria de analista](documentos/tfm_AndresGonzalezSanchez.pdf) | Planteamiento, método, resultados y discusión |
| [Memoria de sponsor](documentos/tfm_sponsor_AndresGonzalezSanchez.pdf) | Síntesis ejecutiva |
| [Apéndices técnicos C, D y E](documentos/tfm_apendices_tecnicos_AndresGonzalezSanchez.pdf) | Configuraciones, contratos y recetas |

Los [antecedentes experimentales](documentos/complementario/antecedentes_experimentales.pdf) quedan como material complementario.


## Organización

```text
v2_entrega_final/
├── README.md
├── REPRODUCIBILIDAD.md
├── THIRD_PARTY_NOTICES.md
├── documentos/
│   └── complementario/
├── reproduccion/
│   ├── notebooks/               # Recorrido principal de reproducción
│   ├── scripts/ y tests/        # Implementación y pruebas
│   ├── config/ y data/          # Contratos y fuentes
│   ├── outputs/                # Evidencia congelada y ejecuciones nuevas
│   ├── environments/           # Entornos de inferencia separados
│   ├── bibliografia/ y figures/
│   ├── docs/                   # Protocolos y validadores
│   └── Fuentes QMD, pyproject.toml y uv.lock
└── verification/               # Informes de las comprobaciones realizadas
```




## Reproducir con los notebooks

Se necesitan Python 3.14 o superior y [uv](https://docs.astral.sh/uv/). Desde la raíz del repositorio:

```bash
cd reproduccion
uv sync --locked --group dev
uv run --no-sync jupyter lab notebooks
```

Seleccione el kernel Python del entorno del proyecto. Los cuadernos se pueden ejecutar de arriba abajo con **Restart Kernel and Run All**. Se recomienda seguir este orden, aunque cada uno inicializa sus propias rutas y no depende de las variables de otro cuaderno:

| Notebook | Contenido |
|---|---|
| [00 · Entorno, corpus y dataset](reproduccion/notebooks/00_entorno_corpus_y_dataset.ipynb) | Fuentes y unidades experimentales |
| [01 · Preguntas, evidencias y qrels](reproduccion/notebooks/01_preguntas_evidencias_y_qrels.ipynb) | Evidencia de referencia y grados de relevancia |
| [02 · Recuperación y explicitud](reproduccion/notebooks/02_recuperacion_y_explicitud.ipynb) | Recálculo de métricas y contraste explícita–implícita |
| [03 · Respuestas, evaluación y decisiones](reproduccion/notebooks/03_respuestas_evaluacion_y_decisiones.ipynb) | Cobertura, fallos y procedencia de las puntuaciones |
| [04 · Comparaciones finales y verificación](reproduccion/notebooks/04_comparaciones_finales_y_verificacion.ipynb) | Reanálisis completo y comparación de los 35 CSV |



Para ejecutar todos los notebooks automáticamente, cada uno en un kernel nuevo:

```bash
uv run --no-sync python notebooks/verify_notebooks.py
```

El verificador guarda copias ejecutadas e informe en un destino REPLAY_ nuevo. La [guía de los notebooks](reproduccion/notebooks/README.md) explica las salidas y las opciones; [REPRODUCIBILIDAD.md](REPRODUCIBILIDAD.md) detalla el alcance y las alternativas por consola.

## Alternativa por consola

Desde reproduccion/:

```bash
uv run --no-sync python scripts/validate_final_results.py
uv run --no-sync python scripts/reproduce_offline.py --run-id tribunal_01
uv run --no-sync python -m pytest -q tests docs/test_validar_apendices.py
```

El validador contrasta once tablas numéricas del contrato final (389 valores) y los documentos entregados. El reanálisis recalcula recuperación, explicitud, comparación de generadores y comparación de recuperadores dentro de cada generador; exige identidad byte a byte de los 35 CSV. Cada ejecución por consola requiere un identificador nuevo.


## Derechos y datos de terceros

Consulte [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) y reproduccion/config/corpus_sources.csv antes de redistribuir el corpus y sus derivados.
