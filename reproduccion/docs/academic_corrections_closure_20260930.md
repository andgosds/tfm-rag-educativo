# Cierre de correcciones académicas R01–R21

**Fecha:** 2026-09-30. **Versión principal:** v2. **Alcance:** correcciones aceptadas de la memoria, reanálisis offline y verificación reproducible. No se han repetido inferencias ni adjudicaciones, ni se han hecho commits o pushes.

Este cierre sustituye las interpretaciones anteriores de capacidad, explicitud y significación, no los archivos experimentales congelados. Las anotaciones de septiembre en TASK_QUEUE.md se conservan como historial y no deben leerse como conclusiones vigentes.

## 1. Fuentes definitivas

Todas las rutas parten de la carpeta v2. El directorio de correcciones es **outputs/local_runs/academic_corrections_20260930/**:

- Recuperación: `retrieval/evaluation/`; contrastes: `retrieval/paired/`. `retrieval/verification_report.json` acredita la recomputación de 416 filas, 52 ideales globales y 64 tests, con once artefactos idénticos en dos ejecuciones. Su log de suite contiene fallos intermedios y no constituye la verificación final.
- Generación: `capacity/release_run1/`, no los destinos preliminares. `capacity/release_reproducibility_report.json` comprueba quince productos idénticos en dos ejecuciones, 648 contrastes reconstruidos y la preservación de 674 archivos de la campaña de generación.
- Documento: `tfm.qmd` y `tfm.pdf`. El validador final está en `final_validation/closure_release/tfm_closure_validation_v1_22q.json`: el nombre histórico del archivo no limita su cobertura, que incluye piloto, explicitud exploratoria y v3.
- Aceptación final: `final_validation/release_acceptance.json`; suite: `final_validation/release_tests.log`; notebooks: `final_validation/notebooks_release_green.json` y su log.
- Recetas y límites: `docs/academic_corrections_reproduction_20260930.md`, `docs/standalone_operations.md`, `docs/render_environment_20260930.json`.

## 2. Registro de cierre

| ID | Corrección aplicada | Evidencia y alcance |
|---|---|---|
| R01 | IDCG se calcula con todos los qrels de la consulta, independiente del ranking. | evaluate_retrieval_v3.py, pruebas de regresión y before_after.csv; históricos conservados, métricas y memoria actualizadas. |
| R02 | Correspondencia entre hipótesis original y H1–H6. | Tabla tbl-hipotesis y veredictos revisados; no se atribuye superioridad híbrida a H1/H2 ni contraste inexistente a H3. |
| R03 | Emparejamiento por celdas exactas antes de agregar por base. | analysis_capacity_v3.py y productos common; cobertura y fallos separados de calidad condicional al éxito. |
| R04 | Interacción directa entre efectos de formulación. | h6_interaccion.csv, tabla tbl-capacidad-interaccion y conclusión sin absorción demostrada; resumen y abstract coherentes. |
| R05 | Extremos distintos y comparaciones identificadas. | h5_comparaciones_common.csv y h5_separacion_common.csv; no comparación de una estrategia consigo misma ni equivalencia inferida de IC. |
| R06 | Retirada la jerarquía general de importancia generador > recuperador. | Sección de generador, resumen y conclusiones: ambos factores varían, sin orden causal de influencia establecido. |
| R07 | p nominal y Holm posterior, familias explícitas y n efectivo correcto. | paired_explicitness_v3.py: dos familias de dieciséis; 26 bases y sensibilidad de veinte separadas. Ningún p ajustado < 0,05. |
| R08 | Retirada la predicción de cruce del umbral con unas pocas preguntas. | Trabajo futuro exige potencia, tasa de empate, efecto, multiplicidad y tamaño fijados; ampliación acumulada no se llama confirmación independiente. |
| R09 | Instrumentos y aplicabilidad por campaña, no equivalencia RAGAS/rúbrica. | Tablas de campañas/instrumentos y reanálisis primary_content, sensitivity_all y sensitivity_abstain; citas v3 0–1. |
| R10 | Tres campañas delimitadas en todo el relato. | Piloto 22/88; exploración 7 parejas/55 válidas + 1 fallo; v3 inventario 30, ejecución 26 parejas/604 válidas + 20 fallos. |
| R11 | Procedencia explícita de las cifras del resumen y abstract. | Métricas y latencias del piloto rotuladas; explicitud y generadores atribuidos a su propia campaña; emparejamiento condicionado al soporte común. |
| R12 | Atribución humana, asistida, automática y arbitraje diferenciados. | Procedencia por campaña y criterio; v3: 233 discrepancias validadas en 158 celdas, no revisión humana de las 604 respuestas. |
| R13 | Respuestas válidas, medias marginales y pares completos separados. | 55 válidas, 27 pares completos (54 respuestas), una sin contraparte; tablas tbl-expl-generacion y tbl-expl-generacion-pareada verificadas. |
| R14 | Dos controles de pérdida matemática explicados y causalidad retirada. | Cinco fragmentos del control inicial frente a veinte del barrido posterior; corpus congelado; no se garantiza orden inalterado ni límite inferior. |
| R15 | Dirección del defecto de etiqueta corregida. | Qwen 4B sobredeclara grounded_correction en respuestas ordinarias; conformidad de etiqueta no se denomina calibración de confianza. |
| R16 | Lenguaje descriptivo y límites revisados. | Retiradas equivalencia, robustez general y ausencia de efecto no demostradas; conclusiones distinguen descripción, contraste e interpretación. |
| R17 | Citas próximas a técnicas centrales y ficha oficial E5 incorporada. | Bibliografía v2 adaptada y manifiesto actualizado. AA sin captura verificable se excluye del eje analítico principal; no se inventa una validación externa. |
| R18 | Una única raíz v2, argumentos y destinos nuevos. | Apéndice E y recetas offline ejercitadas; replay, inferencia y adjudicación diferenciados. Copia sin v1, entorno uv fresco, suite y render reales. |
| R19 | Validador actualizado y cobertura no vacía. | Trece tablas históricas/218 cifras y ocho académicas/284 cifras; contratos derivados de artefactos, escalas, hashes y denominadores independientes. |
| R20 | Trazabilidad v3 completa y cambios respecto al plan delimitados. | Apéndice E y documento de reproducción: pares, qrels, rankings, generación, pases inválidos/válidos, árbitro, acta, consolidación y reanálisis. |
| R21 | Título, autoría, remisiones, tablas y saltos Typst corregidos. | YAML académico y salida visible; sin referencias tabla/figura sin definición ni ??; entorno R/Quarto documentado y PDF renderizado. |

## 3. Resultado de las verificaciones

### Pruebas y reproducción offline

La última suite sobre la copia reubicada devuelve **201 passed, 4 subtests passed**. Una guarda de lectura Python bloquea el acceso al proyecto original; se comprobó que estaba activa con una lectura negativa. No equivale a aislamiento del sistema operativo.

La copia se creó sin .venv ni carpeta hermana v1 y se instaló con `uv sync --frozen`. Quarto generó un PDF de 68 páginas cuyo texto extraído es idéntico al de la versión principal. Los PDFs no son byte-idénticos: difieren las fechas de creación/modificación incorporadas por Typst. La reconstrucción empleó el entorno R/Quarto instalado, no un contenedor limpio.

Los diez notebooks se ejecutaron con kernels nuevos en una segunda copia, sin inferencia y con guardas de lectura, escritura y red: **10/10, 48 celdas, cero errores y archivos protegidos intactos**. El primer intento detectó el estado obsoleto del cuaderno 09: esperaba 59 confirmaciones y 39 pendientes. Se añadió una regresión RED→GREEN y se corrigió su lectura a 98 confirmadas, incluidas dos con ajuste. No se modificó el libro de decisiones ni el pool ciego. `notebooks_initial_red.json` y `notebooks_release.log` preservan el intento fallido; `notebooks_release_green.json` acredita la ejecución final.

### Tablas, fuentes y PDF

El validador contrasta **502 celdas numéricas de 21 tablas**, incluidas 284 de las ocho tablas académicas corregidas. Excluye de los datos los dígitos de nombres como BM25, pero los conserva al comparar etiquetas; una adulteración a BM26 provoca fallo. También verifica las 604 celdas finales, 20 fallos, 233 discrepancias, 159 registros del acta (158 decisiones y una convención), escalas, procedencia y disponibilidad por criterio.

La comprobación final releyó los SHA-256 de **78 entradas/fuentes verificadas**, todas coincidentes con el informe. Las **21 referencias distintas a tablas o figuras** tienen definición. El PDF contiene el resumen y abstract actualizados, el ajuste Holm y la conclusión de interacción, sin referencias ?? sin resolver.

Se inspeccionaron visualmente las páginas 1, 3, 4, 46 y 47: título e índice, resumen, abstract y tablas de generador/extremos/interacción, sin recortes o solapamientos apreciables. Es una revisión visual dirigida, no una auditoría de maquetación exhaustiva de las 68 páginas.

PDF entregado: `tfm.pdf`, **481569 bytes**. SHA-256:

`9960ea194709bd690fa15bd4d9f33e662bce2920afd80ccae6bdfaa5cce1cee6`

## 4. Límites que no deben ocultarse

- No se repitió inferencia local/remota, benchmark end-to-end ni disponibilidad actual de proveedores.
- El índice AA no tiene captura recuperable; se conserva solo como metadato de usuario no verificado y no sustenta conclusiones de capacidad. No se ha auditado externamente toda la bibliografía.
- La consolidación humana histórica v3 conserva un paso manual/asistido documentado. El validador reconstruye su regla en lectura; no se inventa una CLI de consolidación.
- No se realizan 604 revisiones humanas: el consenso automático sigue diferenciado de las 158 celdas con validación de discrepancias.
- No se establece eficacia pedagógica, equivalencia de recuperadores, absorción de implicitud ni una curva causal de capacidad entre familias.
- La wiki incorpora las lecciones y el seguimiento en learning/ sin elevar el dominio personal a partir de tests automáticos.

**Conclusión:** R01–R21 quedan corregidas en el alcance académico y documental acordado. El cierre no convierte los límites pendientes en verificaciones realizadas. La versión resultante está preparada para lectura del tutor, con resultados corregidos y evidencia de ejecución; no es una validación externa completa del sistema ni una campaña nueva.
