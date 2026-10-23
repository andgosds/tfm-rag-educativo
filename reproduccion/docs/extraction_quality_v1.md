> **Recetas desde la raíz del paquete v2.** Los resultados descritos son históricos. Para operaciones de escritura usar destinos nuevos bajo `outputs/local_runs/`; los defaults congelados se rechazan. Recetas vigentes seguras: `standalone_operations.md`. No ejecutar inferencia mientras siga abierta la adjudicación.

# Calidad de la extracción v1

## Objetivo

Esta nota documenta la primera extracción estructurada de los capítulos seleccionados de OpenStax. El objetivo es comprobar que el texto puede recuperarse con trazabilidad suficiente antes de diseñar el chunking.

## Procedimiento

La extracción se realiza con PyMuPDF 1.28.2 mediante el script:

```bash
uv run python scripts/extract_openstax_chapters.py
```

El script utiliza los marcadores internos de cada PDF para:

1. localizar los capítulos incluidos;
2. detener la extracción antes de términos clave, ejercicios, referencias y soluciones;
3. asignar capítulo y sección a cada página;
4. conservar la página física del PDF y la página impresa;
5. eliminar encabezados y pies de página repetidos;
6. producir un registro JSON por página.

Los metadatos y la selección de capítulos proceden de `../config/corpus_sources.csv`.

## Artefactos

| Artefacto | Contenido |
|---|---|
| `../data/interim/introductory_statistics_2e_pages.jsonl` | Capítulos 6–9 de *Introductory Statistics 2e* |
| `../data/interim/principles_of_data_science_pages.jsonl` | Capítulos 3–4 de *Principles of Data Science* |
| `../data/interim/extraction_report_v1.json` | Rangos, secciones y métricas de extracción |

## Resultados

| Fuente | Páginas extraídas | Capítulos | Secciones | Palabras | Páginas vacías | Páginas cortas |
|---|---:|---:|---:|---:|---:|---:|
| *Introductory Statistics 2e* | 91 | 4 | 25 | 32.488 | 0 | 0 |
| *Principles of Data Science* | 99 | 2 | 11 | 36.007 | 0 | 1 |
| **Total** | **190** | **6** | **36** | **68.495** | **0** | **1** |

La extracción contiene 409.015 caracteres. Los identificadores de registro siguen el patrón `doc_id:pdf-NNNN` y permiten volver directamente a la página del PDF de origen.

## Página corta revisada

El único registro con menos de cien caracteres es:

```text
openstax_principles_ds:pdf-0149
```

Corresponde a la página impresa 139, dentro de la sección 3.5. La revisión visual confirma que la página está prácticamente vacía y solo contiene el valor `0.143`. Por tanto, no se trata de una pérdida general de texto. Durante el chunking, este registro deberá unirse al contenido de la página anterior en lugar de formar un chunk independiente.

## Calidad del texto

La prosa, los títulos y la mayor parte de los ejemplos se extraen con un orden de lectura utilizable. También se conservan:

- identificador del documento;
- título de la fuente;
- licencia y hash del PDF;
- capítulo y sección;
- página física e impresa;
- recuentos de caracteres y palabras;
- método de extracción.

Los encabezados alternos con numeración a izquierda y derecha se eliminan mediante reglas comprobadas por tests. No quedan pies repetidos con el texto `Access for free at openstax.org`.

## Limitación de fórmulas

La extracción básica no conserva de manera fiable todas las fórmulas. En varias páginas aparecen expresiones incompletas, por ejemplo una etiqueta como `f(x) =` sin el contenido matemático situado a continuación. Algunos símbolos se mantienen, pero las fracciones y expresiones maquetadas como objetos gráficos pueden perderse.

Esta limitación implica que los JSONL actuales son adecuados para:

- identificar capítulos y secciones;
- trabajar con prosa conceptual;
- preparar preguntas definicionales e interpretativas;
- diseñar el pipeline de chunking.

Todavía no deben utilizarse como única fuente para preguntas que exijan reproducir o calcular una fórmula. Antes de incorporar ese tipo de preguntas al golden set habrá que contrastar las páginas afectadas con la versión web de OpenStax o utilizar una extracción específica para contenido matemático.

## Decisión de calidad

La extracción se acepta como **intermedia** y trazable. No es todavía el dataset final de recuperación. El siguiente paso será construir chunks que:

1. respeten los límites de sección;
2. puedan unir texto entre páginas consecutivas;
3. eviten registros demasiado cortos;
4. mantengan todas las páginas de procedencia;
5. identifiquen fragmentos con fórmulas para revisión adicional.
