> **Recetas desde la raíz del paquete v2.** Los resultados descritos son históricos. Para operaciones de escritura usar destinos nuevos bajo `outputs/local_runs/`; los defaults congelados se rechazan. Recetas vigentes seguras: `standalone_operations.md`. No ejecutar inferencia mientras siga abierta la adjudicación.

# Estrategia de preparación y chunking v1

## Decisión metodológica

El corpus v1 se divide mediante un chunking jerárquico limitado por secciones. Ningún chunk puede mezclar secciones, capítulos o libros diferentes. Dentro de cada sección, el texto se agrupa utilizando párrafos y frases completas hasta alcanzar un tamaño objetivo de 300 palabras.

La configuración se identifica como `section_paragraphs_300w_overlap60_v1` y utiliza estos parámetros:

| Parámetro | Valor |
|---|---:|
| Límite estructural | Sección |
| Tamaño objetivo | 300 palabras |
| Máximo flexible | 380 palabras |
| Mínimo orientativo | 100 palabras |
| Solapamiento máximo | 60 palabras |
| Unidad del solapamiento | Frases completas |

El tamaño objetivo actúa como punto de corte operativo, no como una longitud obligatoria. El algoritmo conserva los párrafos y, cuando necesita unidades menores para aplicar el solapamiento, utiliza límites de frase. Un fragmento final inferior al mínimo se redistribuye o se integra con el anterior sin superar el máximo flexible.

## Justificación

Las 36 secciones de la capa intermedia presentan una mediana de 1.178 palabras y un máximo de 8.563. Por tanto, utilizar secciones completas como unidades de recuperación generaría fragmentos demasiado extensos y heterogéneos. Un tamaño objetivo de 300 palabras conserva suficiente contexto para definiciones, condiciones y explicaciones breves sin incorporar tanto contenido como para diluir la evidencia relevante.

El solapamiento evita que la información situada junto a un límite quede aislada en un único fragmento. Se permite reutilizar hasta 60 palabras mediante frases completas. Esta decisión evita cortes mecánicos dentro de una frase y conserva la legibilidad del texto. El solapamiento se aplica únicamente entre chunks consecutivos de una misma sección.

## Campos de salida

Cada chunk contiene:

- identificador estable;
- libro y ruta relativa de la fuente;
- licencia y hash del PDF;
- capítulo y sección;
- índice del chunk dentro de la sección;
- páginas físicas e impresas implicadas;
- identificadores de los registros intermedios utilizados;
- texto original del fragmento;
- texto de recuperación enriquecido con títulos;
- recuentos de palabras y caracteres;
- método de chunking;
- indicador de posible degradación de fórmulas.

El identificador sigue el patrón:

```text
openstax_intro_stats_2e:8.2:chunk-003
```

El campo `text` conserva el contenido extraído. El campo `retrieval_text` antepone el libro, el capítulo y la sección para aportar contexto terminológico durante la indexación. Esta separación permitirá analizar posteriormente el efecto de los títulos sin modificar la evidencia original.

## Trazabilidad entre páginas

Las páginas no actúan como límites obligatorios. Un chunk puede utilizar texto de varias páginas consecutivas de la misma sección. En ese caso se conservan todas las páginas físicas, páginas impresas e identificadores de registros intermedios empleados.

La página corta `openstax_principles_ds:pdf-0149`, que solo contiene el valor `0.143`, queda integrada con el contenido previo de su sección y no genera un fragmento independiente.

## Tratamiento de contenido matemático

Las fórmulas no se reconstruyen automáticamente cuando la extracción del PDF resulta incompleta. El generador aplica reglas conservadoras para marcar expresiones que terminan en un signo igual sin contenido matemático recuperado. Estos chunks conservan la página original y se identifican mediante `formula_risk = true`.

La marca no demuestra que toda la fórmula sea incorrecta ni detecta necesariamente todas las pérdidas posibles. Su función es priorizar la revisión manual antes de utilizar esos fragmentos como evidencia para preguntas de cálculo o reproducción de expresiones matemáticas.

## Resultado ejecutado

La ejecución real se realiza con:

```bash
uv run python scripts/build_chunks.py
```

A partir de 190 registros de página se han generado 288 chunks:

| Indicador | Resultado |
|---|---:|
| Documentos | 2 |
| Capítulos | 6 |
| Secciones | 36 |
| Chunks | 288 |
| Longitud mínima | 107 palabras |
| Longitud media | 281,62 palabras |
| Mediana | 291 palabras |
| Percentil 25 | 281 palabras |
| Percentil 75 | 296 palabras |
| Longitud máxima | 327 palabras |
| Chunks con riesgo de fórmula | 5 |
| Chunks inferiores a 100 palabras | 0 |
| Chunks superiores a 380 palabras | 0 |

La distribución por fuente es:

| Fuente | Chunks |
|---|---:|
| *Introductory Statistics 2e* | 139 |
| *Principles of Data Science* | 149 |

Respecto a las páginas de procedencia, 108 chunks utilizan una página, 171 utilizan dos y 9 abarcan tres páginas consecutivas.

## Auditoría del solapamiento

Los 288 chunks producen 252 límites internos entre fragmentos consecutivos de una misma sección. Todos contienen algún solapamiento. La longitud observada se sitúa entre 3 y 60 palabras, con una media de 50,05 palabras. La variación se debe a que el algoritmo prioriza frases completas y no fuerza un corte para alcanzar exactamente 60 palabras.

## Validación

La suite del pipeline contiene 14 pruebas superadas. Las pruebas específicas de chunking comprueban:

- respeto de los límites de sección;
- tamaños mínimo y máximo;
- solapamiento mediante frases completas;
- tratamiento de fragmentos finales cortos;
- construcción del texto enriquecido;
- identificación de fórmulas potencialmente degradadas;
- estabilidad de identificadores;
- generación del dataset y del informe;
- ejecución desde línea de comandos.

La auditoría adicional comprobó la unicidad de los 288 identificadores, la correspondencia de páginas e identificadores de origen, la coherencia de los recuentos y el uso de rutas relativas.

## Artefactos

| Artefacto | Función |
|---|---|
| `../scripts/build_chunks.py` | Implementación reproducible |
| `../tests/test_build_chunks.py` | Pruebas automatizadas |
| `../data/processed/chunks_v1.jsonl` | Dataset de recuperación |
| `../data/processed/chunking_report_v1.json` | Estadísticas y parámetros |

## Uso experimental

El mismo archivo de chunks se utilizará en la comparación principal de BM25, recuperación densa, recuperación híbrida y reranking. Mantener constante esta representación permite atribuir las diferencias observadas principalmente al método de recuperación y no a cambios simultáneos en la segmentación del corpus.
