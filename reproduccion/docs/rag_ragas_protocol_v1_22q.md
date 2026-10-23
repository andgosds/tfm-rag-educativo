# Protocolo RAG y RAGAS reducido v1

## Objetivo

Comprobar si la mejora de orden obtenida por RRF con reranking frente a RRF se traduce en respuestas más correctas y fundamentadas, manteniendo constante la generación.

## Diseño congelado

- Preguntas: 22 registros del golden set v1.
- Condiciones: RRF y RRF con reranking MiniLM-L6-v2.
- Contexto: top-5 chunks ordenados por cada condición.
- Generador: Qwen 3.5 9B mediante Ollama.
- Decodificación: temperatura 0, semilla 20260902 y máximo 300 tokens de salida.
- Prompt: `rag_answer_prompt_v1`.
- Respuestas: una por pregunta y condición; 44 en total.
- Idioma: inglés, como el golden set y el corpus.
- Juez: Gemma 3 4B mediante Ollama, separado de la familia del generador.
- RAGAS: versión 0.4.3 en un entorno Python 3.12 aislado.

El generador solo puede usar los cinco contextos suministrados. Debe responder con citas de identificadores de chunk, corregir expresamente una premisa falsa cuando exista evidencia contradictoria o declarar exactamente que no puede responder a partir de los contextos cuando la evidencia sea insuficiente. La salida emplea un contrato textual de tres campos porque Qwen 3.5 9B no respetó de forma consistente el esquema JSON de Ollama en el smoke test. Si una salida altera el formato o cita un identificador ajeno al top-5, no se filtra ni se repara silenciosamente: se solicita una regeneración correctiva con la lista cerrada de identificadores permitidos, hasta un máximo de tres intentos. Las salidas brutas, los intentos, la latencia y los tokens acumulados quedan registrados.

## Conductas esperadas

1. `answer`: respuesta ordinaria para las trece preguntas respondibles.
2. `grounded_correction`: corrección fundamentada para q-v1-008 y q-v1-020.
3. `abstain`: abstención para las siete preguntas restantes sin evidencia suficiente.

## Métricas

### RAGAS

- Faithfulness: se calcula para todas las respuestas y estima el apoyo de sus afirmaciones en los contextos recuperados.
- Factual Correctness: se calcula solo cuando existe referencia: respuestas ordinarias y correcciones fundamentadas. No se aplica a abstenciones sin respuesta de referencia.

### Deterministas

- Coincidencia entre comportamiento declarado y esperado.
- Validez de citas: todas las citas deben pertenecer al top-5 entregado.
- Presencia de citas: se exige al responder o corregir y se exige ausencia de citas al abstenerse.

### Rúbrica auxiliar

Gemma 3 4B asigna 0, 1 o 2 a la adecuación del comportamiento. La identidad de la condición de retrieval no se incluye en el prompt del juez. La puntuación automática sirve para priorizar auditoría humana y no sustituye la adjudicación final. RAGAS y la rúbrica usan temperatura 0 y semilla 20260902. El smoke test repetido mostró que Faithfulness puede variar incluso con estos parámetros —0,5 y 1,0 para el mismo ejemplo—, por lo que la semilla se interpreta como control de trazabilidad, no como garantía de determinismo del backend local.

## Latencia y coste

Se registran por respuesta:

- latencia generativa observada;
- tokens de entrada y salida informados por Ollama;
- latencia del juez de comportamiento;
- latencia total de evaluación.

Los modelos son locales, por lo que no existe un cargo API variable. El coste computacional de hardware, energía y amortización no se monetiza.

## Cola de riesgo

Se priorizan para revisión humana:

- Faithfulness o Factual Correctness inferiores a 0,5;
- diferencia absoluta entre ambas métricas igual o superior a 0,5;
- puntuación de comportamiento inferior a 2;
- discrepancia entre comportamiento declarado y esperado.

## Regla de cierre

La fase termina cuando existen 44 respuestas reproducibles, puntuaciones por caso, agregados por condición, cola de riesgo, análisis emparejado y auditoría de los casos prioritarios. No se ajustan prompt, modelos ni top-k después de observar qué condición obtiene mejores resultados.
