# Comprobación de la entrega

## Notebooks actuales

Los cinco cuadernos de reproduccion/notebooks/ se han ejecutado en una copia reubicada, cada uno con un kernel nuevo. La comprobación incluye el PDF de apéndices con su nombre actual: tfm_apendices_tecnicos_AndresGonzalezSanchez.pdf.

| Archivo | Contenido |
|---|---|
| [notebooks_validation.json](notebooks_validation.json) | Informe de ejecución, preservación de archivos y límites de la comprobación |
| [notebooks/](notebooks/) | Cinco copias ejecutadas, logs y prueba de bloqueo de acceso a los árboles originales |
| [notebooks/tests.log](notebooks/tests.log) | Suite de pruebas del paquete |
| [code_documentation_validation.json](code_documentation_validation.json) | Docstrings de los 51 scripts y equivalencia de su lógica antes y después de documentarlos |
| [appendix_reproducibility_revision.json](appendix_reproducibility_revision.json) | Actualización del apéndice E al recorrido mediante notebooks, render y comprobación de la entrega |

Los cuadernos ejecutan el reanálisis, contrastan los 35 CSV con las referencias y muestran las tablas resultantes. También se ha probado la opción de figuras: once bloques R y diez SVG, sin renderizar las memorias. Las copias ejecutadas permiten consultar las salidas sin repetir los cálculos.

La guarda Python bloqueó la lectura de v1, v2 y v2_entrega_final originales y las conexiones externas. No equivale a aislamiento del sistema operativo ni restringe R. Se utilizaron los paquetes R ya instalados; no se comprobó una instalación limpia de R ni se ejecutó nueva inferencia.

## Comprobaciones anteriores

Los archivos siguientes se conservan como registro de verificaciones previas. Sus rutas y nombres de PDF corresponden al momento en que se generaron.

| Archivo | Contenido |
|---|---|
| final_results_validation.json | Contrato de once tablas y 389 valores |
| reproduction_report.json | Reanálisis offline y 35 CSV idénticos |
| figures_report.json y figures/ | Ejecución de los bloques R y gráficos obtenidos |
| tests.txt | Suite anterior a los notebooks actuales |
| python_environment.txt y R_sessionInfo.txt | Entornos utilizados en aquella comprobación |
| independence.json | Guarda de lectura/red y preservación documental |
| [reorganization_validation.json](reorganization_validation.json) y [reorganized/](reorganized/) | Comprobación posterior a la separación de documentos y paquete técnico |

Los destinos REPLAY_ citados en esos informes no se incluyen completos para evitar duplicar resultados. Las referencias congeladas están en reproduccion/outputs/; los comandos y notebooks crean salidas nuevas.

## Procedencia

PROVENANCE.json conserva la selección inicial de archivos y sus omisiones. [reorganization.json](reorganization.json) registra el cambio de carpetas realizado después. Son registros históricos, no inventarios actualizados: los nuevos notebooks no formaban parte de aquella selección y el autor ha renombrado el PDF técnico.

El repositorio no requiere un manifiesto global de integridad. Se mantienen los metadatos científicos que utilizan los validadores para contrastar las fuentes y los resultados.
