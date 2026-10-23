# Cierre de la memoria centrada en el experimento final

Fecha: 2026-09-30. Raíz operativa: TFM/v2.

## Decisión y alcance

El experimento final sustituye las evaluaciones previas como evidencia principal: cuatro recuperadores, 26 preguntas base con dos formulaciones, tres generadores y 604 respuestas aceptadas de 624 previstas. Las veinte fallidas se informan aparte. El inventario ejecutado contiene 17 tareas de respuesta, cinco de corrección y cuatro de abstención; no se confunde con las treinta bases inventariadas.

La memoria principal es `tfm.qmd` / `tfm.pdf`. Los resultados anteriores, sus instrumentos y el benchmark previo de recuperación quedan en `antecedentes_experimentales.qmd` / `antecedentes_experimentales.pdf`. No se alteraron históricos, juicios, identificadores ni pre-registro; tampoco se convirtieron decisiones retrospectivas en prospectivas. Las correcciones R01–R21 y su acta anterior permanecen trazables.

## Comparación y recomendación

El análisis offline está en `outputs/local_runs/final_experiment_20260930/analysis/` y se reproduce con `scripts/analyze_final_experiment.py`. Por generador y criterio se intersectan las formulaciones numéricas de los cuatro recuperadores antes de promediar dentro de base y macroagregar. Se publican todos los 72 contrastes, sus soportes, IC bootstrap puntuales y positivos/negativos/empates.

No existe ganador universal. Con Qwen 4B, reranking maximiza las medias de contenido; con Qwen 9B, RRF maximiza fundamentación y comparte el máximo de citas, mientras reranking maximiza corrección y conducta. Con Gemma, dense maximiza corrección y reranking fundamentación; todas sus estrategias presentan fallos. La memoria no arrastra la recomendación RRF del piloto ni construye un índice compuesto post-hoc. Los máximos son descriptivos, no superioridad ajustada ni equivalencia.

Tiempo y tokens se leen de los registros de generación, separados por aceptación y fallo. Hay datos en las 604 aceptadas y veinte fallidas, con 614 y sesenta intentos respectivamente. Los acumulados no se suman de nuevo al ledger. No son benchmark end-to-end, medida causal del recuperador ni coste monetario.

## Aceptación verificada

Evidencia: `outputs/local_runs/final_experiment_20260930/release_validation/release_acceptance.json` y logs asociados.

| Comprobación | Resultado |
|---|---|
| Suite completa, original y reubicada | 256 pruebas y ocho subtests pasan |
| Tablas numéricas principales | Ocho tablas / 344 cifras contrastadas con fuentes externas |
| Tablas numéricas complementarias | Quince tablas / 314 cifras contrastadas con fuentes externas |
| Reanálisis offline | Diecisiete artefactos byte-idénticos en segunda ejecución y replay reubicado |
| Fuentes protegidas | 677 archivos del análisis y 78 del baseline anterior intactos |
| Notebooks | Diez notebooks / 48 celdas, kernels nuevos, hashes protegidos intactos |
| Memoria PDF | 48 páginas, sin referencias ??, texto y páginas iguales al render reubicado |
| Suplemento PDF | 35 páginas, sin referencias ??, texto y páginas iguales al render reubicado |

Los conteos de tablas corresponden a contratos de resultados, no al número total de tablas de diseño o metadatos del documento. La revisión visual dirigida corrigió el solapamiento del inventario largo convirtiéndolo en fichas, sin perder preguntas ni metadatos, y compactó los encabezados operativos.

La copia reubicada está en scratch, sin hermana v1 ni archivos .env. Las guardas Python bloquean lecturas del proyecto original; no son un sandbox del sistema operativo. El primer replay anidado de notebooks bloqueó su propio intérprete, ubicado dentro de la raíz que la guarda prohibía. La repetición con el entorno externo de kernels completó diez de diez. Se preserva el log fallido y el informe verde, sin ocultar el intento inicial.

## Límites y actividad no realizada

No hubo inferencias, modelos/APIs, nueva adjudicación, benchmark nuevo, commit ni push. La revisión visual no fue exhaustiva página por página. La autonomía verificada es offline y no acredita disponibilidad actual de proveedores ni repetibilidad numérica de una nueva inferencia. El PDF se compara por texto y páginas; los metadatos temporales de Typst pueden variar. Persisten corpus reducido, pooling incompleto, selección retrospectiva y ausencia de validación pedagógica.
