# Notebooks del experimento final

Estos cinco cuadernos reproducen el análisis de la entrega: 26 preguntas base, 52 formulaciones, cuatro recuperadores y tres generadores. Utilizan los rankings, las respuestas y las decisiones incluidos en el repositorio.

| Cuaderno | Contenido |
|---|---|
| [00 · Entorno, corpus y dataset](00_entorno_corpus_y_dataset.ipynb) | Documentos de origen, fragmentación y unidades experimentales |
| [01 · Preguntas, evidencias y qrels](01_preguntas_evidencias_y_qrels.ipynb) | Formulaciones, conductas esperadas, relevancia y procedencia de los qrels |
| [02 · Recuperación y explicitud](02_recuperacion_y_explicitud.ipynb) | Recálculo de métricas, diferencias emparejadas y comparación con los CSV de referencia |
| [03 · Respuestas, evaluación y decisiones](03_respuestas_evaluacion_y_decisiones.ipynb) | Cobertura, intentos, puntuaciones, validación humana y lectura de una respuesta con su evidencia |
| [04 · Comparaciones finales y verificación](04_comparaciones_finales_y_verificacion.ipynb) | Reanálisis completo, 35 CSV, soportes comunes, comparaciones y tiempos de generación |

## Abrir y ejecutar

Desde reproduccion/:

```bash
uv sync --locked --group dev
uv run --no-sync jupyter lab notebooks
```

Seleccione el kernel del entorno del proyecto y ejecute las celdas en orden. Cada cuaderno inicializa sus propias rutas; no necesita variables de otro notebook. El orden de la tabla ayuda a seguir el análisis, pero se puede ejecutar directamente el 04 para comprobar todos los resultados numéricos.

Los cuadernos 00, 01 y 03 leen las fuentes y hacen comprobaciones en memoria. El 02 recalcula recuperación y explicitud. El 04 llama al programa de reanálisis completo, comprueba los 35 CSV y muestra las tablas desde las salidas recién generadas. Los scripts mantienen la implementación de las métricas y de los contrastes estadísticos.

Los cuadernos 02 y 04 crean directorios nuevos con prefijo REPLAY_ en outputs/local_runs/final_experiment_20260930/. Al terminar muestran la ruta utilizada. Puede repetir Run All sin sobrescribir resultados previos ni fuentes congeladas.

## Ejecución completa desde consola

```bash
uv run --no-sync python notebooks/verify_notebooks.py
```

El verificador abre un kernel nuevo para cada cuaderno y utiliza el mismo Python con el que se ha lanzado. Guarda un informe y cinco copias ejecutadas bajo un destino REPLAY_ nuevo. Comprueba que todas las celdas de código se han ejecutado y que los archivos del paquete permanecen intactos, salvo las salidas nuevas y las cachés.

Las [copias ejecutadas de la comprobación de entrega](../../verification/notebooks/) permiten consultar las tablas sin volver a calcularlas. El [informe de esa comprobación](../../verification/notebooks_validation.json) distingue las etapas ejecutadas y sus límites.

## Figuras y nueva inferencia

El cuaderno 04 incluye una celda con REGENERAR_FIGURAS = False. Cambiarla a True ejecuta los bloques R de las memorias y genera diez SVG en otro directorio nuevo. Requiere R con dplyr, ggplot2, jsonlite, knitr y tibble. También se puede comprobar la colección completa con esta opción:

```bash
uv run --no-sync python notebooks/verify_notebooks.py --figures
```

Ninguna de estas ejecuciones vuelve a generar respuestas, solicita juicios externos o modifica adjudicaciones. Repetir la inferencia sería una campaña distinta y necesita modelos, servicios y configuración adicionales. Los cuadernos tampoco renderizan los PDF de entrega.
