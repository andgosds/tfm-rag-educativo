# Pre-registro del protocolo v3: ampliación del golden set y pares de explicitud

**Versión del protocolo:** `explicitness_v3.2`
**Estado:** congelado antes de la ejecución. Cualquier cambio posterior debe versionarse y justificarse; no se modifica este documento tras observar resultados.
**Fecha de cierre del pre-registro:** 2026-09-22
**Enmienda 1:** 2026-09-23 — se incorpora el **generador como factor** (§3, §5.4, §8, §10) y se fija la **asignación de jueces por fase** (§13). Justificación: la campaña v2 había generado con un único modelo, de modo que el hallazgo sobre el desacople entre recuperación y generación podía depender del generador y no era posible comprobarlo. La enmienda se realiza **antes de ejecutar ninguna generación de v3** y sin haber observado resultado alguno: no es una hipótesis posterior a los datos. Sustituye a la condición de generador único que fijaba §1.

**Enmienda 2:** 2026-09-24 — el generador pasa de dos niveles arbitrarios a una **curva de escala dentro de una familia** (Qwen 3.5 en 2B, 4B y 9B) y se reformula la pregunta asociada en términos de **capacidad del generador**. Justificación: dos puntos permiten constatar una diferencia, pero no estimar cómo cambia la ventaja entre estrategias según la capacidad; tres puntos de una misma versión sí lo permiten. Qwen 3.8 27B se retira del diseño porque cambia de versión de familia y confundiría escala con versión. Se añade además una **barrera previa de viabilidad** del contrato de tres campos, tras comprobar que `qwen3.5:2b` no sostiene la abstención. La enmienda se realiza **antes de ejecutar ninguna generación de v3** y tras una sonda de formato de 9 casos que no contempla métrica alguna de calidad: no es una hipótesis posterior a los datos.

**Enmienda 3:** 2026-09-24 — se fija la **composición final de generadores** y el **techo de contexto** tras la sonda de viabilidad con identificadores de chunk reales. Cuatro generadores: `qwen3.5:4b` y `qwen3.5:9b` (curva de capacidad de una familia, con `9b` como ancla de la campaña v2), `gemma4:e4b` y `gemma3:4b` (contraste de familia, y estos dos últimos junto con `qwen3.5:4b` permiten separar **capacidad** de **arquitectura** al concurrir tres modelos de 4B de familias distintas). Se excluyen `qwen3.5:2b` y `gemma4:e2b`, ambos con **citas truncadas al sufijo** en la sonda con IDs reales —mismo modo de fallo en dos familias distintas, que se reporta como **piso de viabilidad convergente**— y `gemma4:12b`, por latencia y por desbordar la VRAM disponible. Se fija **`num_ctx: 8192` para los cuatro generadores por igual**, tras comprobar que el techo por defecto de Ollama (4096) provocaba salidas vacías en `gemma4:12b` cuando el contexto ocupaba casi toda la ventana; con el techo subido resuelve los tres casos de la sonda. Es un parámetro **uniforme entre condiciones**, que no favorece a ninguna. El *Artificial Analysis Intelligence Index* se incorpora como **eje descriptivo de capacidad** en lugar del número de parámetros; se declara expresamente que, con cuatro modelos, **no se interpreta como correlación**. El juez de evaluación de generación queda pendiente de fijación, pero se establece que será un modelo **más potente que cualquiera de los generadores**, para que ningún modelo evalúe respuestas propias.

**Enmienda 4:** 2026-09-25 — se excluye **`gemma3:4b`** de las métricas de generación y se conserva su tasa de fallo como **medida de capacidad**. Justificación: en el bloque de generación devolvió 47 respuestas no válidas sobre 208 —**22,6 %**—, todas con el error *citation outside retrieved contexts*, el mismo modo de fallo por el que ya se habían excluido `qwen3.5:2b` y `gemma4:e2b`. La regla era pre-registrada y no se aplicó a este modelo cuando se incorporó al diseño, **sin pasar por la sonda de viabilidad**; es una omisión de procedimiento, y se declara como tal. Al excluirlo, las celdas perdidas no son aleatorias: se concentran en los casos que exigen citar con precisión —premisas falsas y respuestas con evidencia—, de modo que analizar solo las válidas habría introducido un sesgo por diseño. Se mantiene en el registro como **cuarto punto del piso de viabilidad**, lo que permite situar el umbral con más precisión: cuatro modelos de familias y tamaños distintos fallan por la misma causa, la dificultad de sostener una referencia exacta bajo una capacidad limitada.

**Enmienda 5:** 2026-09-25 — el análisis de escalado se apoya en los **tres generadores restantes**: `qwen3.5:4b` y `qwen3.5:9b` para la curva de capacidad, y `gemma4:e4b` como contraste de familia. La comparación a igual capacidad entre tres modelos de 4B de familias distintas **queda sin responder**, y así se declara en las limitaciones.

**Enmienda 7:** 2026-09-25 — la evaluación de generación se somete al **mismo esquema de dos jueces** ya usado en la gradación de qrels, en lugar de un juez único con auditoría muestral. Juez A: `gpt-6-sol` (`openai-codex`, `--reasoning high`). Juez B: `mimo-v2.6-pro` (`opencode-go`). Ambos evalúan **las mismas 604 respuestas** con la misma rúbrica, en lotes de diez y por `hermes chat --oneshot`, es decir en sesiones aisladas. La **auditoría humana se aplica sobre las discrepancias**, no sobre una muestra al azar: es donde la duda real, y es ahí donde el esfuerzo humano aporta. Se reporta el **acuerdo A−B por criterio** —faithfulness, factual_correctness, behavior_ok y citations_ok—, para que la dependencia del evaluador sea medible y no una cautela vacía. Se mantiene la cautela ya declarada: `mimo` participó en el diseño de las preguntas; aquí actúa como juez y no como autor, y su coincidencia con el juez A se reporta por origen de pregunta para que ese solape sea observable.

**Enmienda 6:** 2026-09-25 — se amplía el parser del contrato de texto para aceptar **dos realizaciones superficiales de la misma salida semántica**. Motivo: `gemma4:e4b` devuelve la conducta bien declarada y las citas como **identificadores exactos embebidos en el texto** —`[openstax_intro_stats_2e:7.1:chunk-002]`—, pero omite los marcadores `ANSWER:` y `CITATIONS:`. El fallo era de **maquetación, no de fidelidad**, y excluirlo por esa causa habría medido obediencia a una plantilla en lugar de calidad de respuesta. Se declara expresamente que **es un cambio de norma hecho tras observar datos**, y se aplican dos salvaguardas: la realización estricta sigue siendo **la primera que se intenta**, de modo que quien ya la cumple no se ve afectado, y el **validador de contenido es idéntico** en las dos —cada cita debe estar entre las recuperadas, y la abstención no puede llevar citas—. La ampliación se aplica **a todas las condiciones por igual**, y se conserva el registro de fallos bajo la norma estricta para poder reportar los dos resultados y mostrar cuánto depende la conclusión del cambio.

**Enmienda 8:** 2026-09-27 — se **invalida y se repite el primer pase de evaluación de generación**. Causa: los lotes presentaban el contexto recuperado **solo como identificadores de chunk**, sin el texto de los fragmentos, de modo que ningún juez podía verificar nada contra la evidencia. El pase completo —604 celdas por juez con `ragas_rubric_v3`— queda descartado y archivado íntegro en `outputs/local_runs/generation_scaling_v3/eval_invalida_solo_ids_20260927/`; **ningún dato de ese pase entra en análisis alguno**, incluido `behavior_ok`, que se salvaba por no necesitar contexto pero procede del mismo pase defectuoso. Las 604 respuestas de generación **no se tocan**: son válidas y solo se reevalúan. Corrección: cada celda del lote presenta ahora el **texto completo de los cinco fragmentos recuperados**, tomado del corpus por id y verificado celda a celda contra las filas de generación. La **rúbrica y los cuatro criterios no cambian**; cambia únicamente lo que se muestra al juez. Los veredictos se registran con `prompt_version: ragas_rubric_v3.1` para distinguirlos de los invalidados. Se fija además el **tamaño de lote en diez para ambos jueces**, según lo ya pre-registrado en la Enmienda 7: el primer pase había ejecutado el juez B en lotes de veinte, desviación que se cierra aquí sin efecto sobre resultados porque todo se repite. Los dos jueces vuelven a evaluar **las mismas 604 celdas** con el mismo diseño, y el contraste A−B y la auditoría humana sobre discrepancias se recalculan desde cero. La enmienda se escribe **antes de observar ningún resultado válido de evaluación**: el único material observado pertenece al pase invalidado.

**Enmienda 9:** 2026-09-27 — se redefine el criterio **`behavior_ok`** y se repite el pase parcial bajo `ragas_rubric_v3.2`. Diagnóstico sobre los parciales del pase v3.1: `behavior_ok` coincidía **exactamente** con la igualdad entre la etiqueta declarada por el generador y la esperada en las 240 celdas ya evaluadas por el juez A —el juez solo comparaba strings—, de modo que el criterio no medía el comportamiento de la respuesta y dejaba fuera el eje de conducta que sostiene la distinción entre respuesta, corrección fundamentada y abstención. Además, la etiqueta de `qwen3.5:4b` fallaba en ~56 % de las celdas (casi todo `answer → grounded_correction`), y bajo la definición antigua la métrica quedaba dominada por ese artefacto de etiquetado. Cambio: `behavior_ok` pasa a graduar el **comportamiento real de la respuesta** frente a la conducta esperada en escala **0–2** —con anclas para omisión de componente material, abstención justificada y abstención injustificada, y premisa falsa—, **ignorando la etiqueta declarada** cuando contradice lo que la respuesta hace. La conformidad de la etiqueta se conserva como métrica determinista aparte (`label_ok`), que no consume juez y documenta la capacidad de seguir el contrato de etiquetado. Es un **cambio de norma hecho tras observar datos de juicio**, y se declara como tal: el parcial v3.1 (310 celdas A + 40 B) se archiva completo en `generation_scaling_v3/eval_diagnostico_v3.1_parcial/` como evidencia del hallazgo y **ninguna de sus cifras entra en la memoria**. Los otros tres criterios permanecen **textualmente idénticos**, pero se reevalúan igualmente para que los cuatro criterios de cada celda procedan de un único `prompt_version` (`ragas_rubric_v3.2`) y no haya mezcla de protocolos dentro de una misma fila. No se ha redactado aún hipótesis sobre conducta, de modo que la redefinición no se apoya a posteriori en ninguna expectativa de resultado.

**Enmienda 10:** 2026-09-27 — el cierre de las discrepancias A−B pasa por un **arbitraje delegado con validación humana posterior por lotes**, en lugar de la auditoría humana directa prevista. Motivo operativo: la cola de discrepancias es de **158 celdas** y la revisión humana directa de cada celda con su unidad completa desplazaría días de trabajo del investigador. Diseño: un árbitro externo (`gpt-6-astra`, `openai-codex`, `--reasoning high`) resuelve **solo los criterios en discrepancia** de cada celda, juzgando por su cuenta con la evidencia; los dos jueces se presentan **anonimizados** como juez 1 y juez 2 para que la marca no ancle la decisión; se permite un valor intermedio cuando ambos jueces se apartan de la evidencia. Cada decisión queda registrada con `decision_source: arbitro_delegado` y `status: pending_human_validation`, con los puntajes y razonamientos de ambos jueces preservados al lado de la resolución. **El árbitro no sustituye al sujeto humano**: el investigador valida las 158 decisiones por lotes antes del análisis, y solo las decisiones validadas se tratan como adjudicación humana en la memoria; cualquier desacuerdo del validador se conserva y se reporta. El artefacto es `generation_scaling_v3/arbitraje_discrepancias_v3/arbitraje_v3.jsonl` (`arbitration_rubric_v1`, salidas crudas por lote en `raw/`). Se declara además que `gpt-6-astra` **no participó en la generación ni en la evaluación**, con lo que arbitra sin solape de autoría.

Este documento fija las métricas, las repeticiones, el orden de ejecución, el tratamiento de errores y el plan de análisis **antes** de construir las preguntas nuevas ni de ejecutar la campaña. Responde a los puntos del acta del 14/09 que quedaron abiertos: «La selección definitiva de métricas principales queda pendiente antes de ejecutar» y «Cerrar métricas principales, repeticiones, orden de ejecución y tratamiento de errores antes de observar resultados».

---

## 1. Objeto y alcance

El protocolo v3 tiene dos fases:

1. **Ampliación del golden set** de 22 a 30 preguntas base, con la misma profundidad de anotación del piloto: respuesta de referencia redactada solo desde la evidencia anotada, citas literales, conjunto canónico mínimo y grados 0/1/2.
2. **Pares explícito/implícito para las 30 preguntas base**, aplicando la rúbrica de §6.

La comparación de cuatro estrategias —BM25, dense, RRF y RRF con *reranking*— se mantiene bajo el contrato común del piloto: mismo corpus de 288 chunks, misma segmentación, misma instrucción y mismo presupuesto de cinco fragmentos por consulta.

El **generador deja de ser una constante y pasa a ser un factor de escala**, con cuatro niveles locales mediante Ollama: `qwen3.5:4b`, `qwen3.5:9b`, `gemma4:e4b` y `gemma3:4b`, todos con `num_ctx: 8192`. La comparación de estrategias se calcula **por separado dentro de cada generador**; la comparación entre generadores es de robustez y se trata como tal.

El motivo de estructurarlo así, y no como dos modelos arbitrarios, es que la pregunta que este factor responde es **cómo cambia la ventaja entre estrategias de recuperación según la capacidad del generador**. Qwen 3.5 aporta la curva, con dos puntos de una misma versión; Gemma 4 y Gemma 3, en 4B, permiten comprobar que la conclusión no es un artefacto de una familia. La capacidad se operacionaliza con el *Artificial Analysis Intelligence Index*, como medida externa, en lugar del número de parámetros, que confundiría tamaño con capacidad en las variantes eficientes de Gemma.

**Barrera previa de viabilidad.** Antes de generar se somete cada modelo a una prueba de contrato de tres campos —pregunta ordinaria, premisa falsa y no respondible—, con **identificadores de chunk reales del corpus**. Un modelo que no sostenga el formato o no cite con el identificador completo no entra en las métricas de generación, porque su fallo mediría capacidad de seguir instrucciones y no calidad de respuesta: se reporta como **piso de viabilidad** aparte. Son dos registros distintos: `generator_contract_probe.jsonl` (2026-09-24, identificadores abreviados, orientativo) y `generator_contract_probe_realids.jsonl` (2026-09-24, identificadores reales, decisivo). De este segundo salen las exclusiones: `qwen3.5:2b` y `gemma4:e2b` devuelven **citas truncadas al sufijo** —`(chunk-003)` en lugar de `openstax_intro_stats_2e:7.1:chunk-003`—, modo de fallo idéntico en dos familias distintas, y `gemma4:12b` devolvía **cadena vacía** por agotar el techo de contexto, fallo que desaparece al fijar `num_ctx: 8192` pero que lleva a excluirlo igualmente por latencia y por desbordar la VRAM.

---

## 2. Estado epistemológico: exploración y confirmación separadas

Conviene declararlo con precisión, porque de ello depende la fuerza de las conclusiones.

La campaña `explicitness_v2` (7 preguntas base, 14 formulaciones) fue **exploratoria**: sus resultados generaron las hipótesis de §3. La campaña v3 (30 preguntas base, hasta 60 formulaciones) es **confirmatoria** respecto a esas hipótesis. La evidencia de v2 no se reutiliza como confirmación: se reporta por separado y sirve únicamente para justificar el origen de las hipótesis.

Si v3 contradice a v2, se informa de la contradicción y se discute su origen; no se promedia ambas campañas ni se selecciona la que sostenga la conclusión prevista.

---

## 3. Hipótesis pre-registradas

Derivadas del piloto exploratorio v2 y fijadas antes de ver los datos de v3. Todas se evalúan sobre diferencias emparejadas por pregunta base.

- **H1 — Degradación general.** La formulación implícita reduce la calidad de recuperación respecto a la explícita en las cuatro estrategias.
- **H2 — Separación entre cobertura y orden.** El coste de la reformulación se reparte de forma distinta según la estrategia: BM25 pierde cobertura (Recall\@10), mientras que dense y las variantes híbridas conservan la cobertura y pierden orden (MRR\@10).
- **H3 — Desacople entre recuperación y generación.** Las cuatro estrategias degradan su recuperación ante la paráfrasis, pero solo una traslada esa pérdida a la respuesta: dense reduce su conducta consolidada.
- **H4 — Equilibrio de RRF.** RRF mantiene el mejor compromiso conjunto entre recuperación, calidad de respuesta y latencia.

Las cuatro hipótesis anteriores se evalúan **dentro de cada generador por separado**. Las enmiendas 1 y 2 añaden dos hipótesis sobre el factor generador, formuladas ahora como **escalado** y no como simple robustez entre dos modelos:

- **H5 — Escalado de la ventaja entre estrategias.** La ventaja de la mejor estrategia sobre la peor se mantiene o se reduce al aumentar la capacidad del generador, pero **no se invierte**. Un generador más capaz compensa mejor un contexto pobre, de modo que la pendiente esperada es descendente: a mayor capacidad, menor separación entre estrategias. Si la curva fuera plana, se concluye que la elección del recuperador es robusta al generador; si descendente, que deja de ser decisiva a partir de cierta capacidad; si ascendente, que la capacidad amplifica las diferencias. Las tres son resultados admisibles y se reportan como tales.
- **H6 — Sensibilidad de las métricas a la capacidad.** Los valores absolutos de Faithfulness y Factual Correctness aumentan con la capacidad del generador, pero el signo de la diferencia explícita−implícita se conserva a lo largo de la curva. Es decir: la capacidad desplaza el nivel de las métricas, no la conclusión sobre el efecto de la explicitud.

Se registran además, como análisis pre-visto y no exploratorio, las interacciones *capacidad × estrategia* y *capacidad × explicitud*, que son precisamente lo que estima la pendiente de H5. La pregunta que orienta este factor, y a la que responde la curva, es: **¿cómo condiciona la capacidad del generador la ventaja que obtiene una estrategia de recuperación sobre otra?**

Toda hipótesis se reporta como **confirmada, no confirmada o inconcluyente**, con el efecto observado y su intervalo. No se formulan hipótesis adicionales tras ver los datos; cualquier análisis no previsto se etiqueta como exploratorio.

---

## 4. Unidad de análisis y agregación

La **unidad es la pregunta base**, nunca cada formulación como observación independiente. Conforme al acta del 14/09, las reformulaciones de una misma pregunta se contabilizan por separado y no se usan para aumentar el número de preguntas independientes.

- Las diferencias se calculan como *implícita − explícita* por pregunta base.
- Los agregados son medias macro sobre preguntas base.
- El recuento de preguntas independientes sigue siendo 30 tras la ampliación; las formulaciones se reportan como `30 base / N formulaciones`.

---

## 5. Métricas pre-registradas

Cálculo a $k=5$ y $k=10$. Las definiciones son las del piloto y no se alteran.

### 5.1. Recuperación — principales

| Métrica | Definición |
|---|---|
| **Recall\@k** | Proporción de la evidencia de grado 2 conocida que aparece en el top-*k*. Solo el grado 2 cuenta como relevante: recuperar contexto de grado 1 no es acceso suficiente a la evidencia. |
| **nDCG\@k** | Calidad del orden con la escala graduada 0/1/2, ganancia $2^{rel}-1$ y descuento logarítmico. |

### 5.2. Recuperación — complementarias

| Métrica | Definición |
|---|---|
| **Precision\@k** | Proporción de los resultados del top-*k* que son de grado 2. Sigue el mismo criterio estricto que Recall y MRR, para que las cuatro métricas sean comparables entre sí. |
| **MRR\@k** | Posición del primer fragmento de grado 2. |

### 5.3. Recuperación — suficiencia de la evidencia

Métrica nueva, que responde al punto «junto con la suficiencia de la evidencia recuperada» del acta y permite separar *recuperar toda la evidencia relevante* de *recuperar evidencia suficiente para responder*. Se define sobre las preguntas con conjunto canónico; no aplica a las preguntas no respondibles.

| Métrica | Definición |
|---|---|
| **Suficiencia estricta\@k** | Proporción de preguntas cuyo top-*k* contiene **todos** los chunks del conjunto canónico mínimo. |
| **Suficiencia parcial\@k** | Proporción de preguntas cuyo top-*k* contiene **al menos un** chunk del conjunto canónico. |

La comparación entre ambas cuantifica el efecto de la redundancia: si la suficiencia parcial es alta y la estricta baja, Recall infravalora una recuperación que basta para responder.

### 5.4. Generación

| Métrica | Entradas | Alcance |
|---|---|---|
| **Faithfulness** | pregunta, respuesta, contextos | Proporción de afirmaciones inferibles de los contextos. No ve la respuesta de referencia ni comprueba verdad externa. |
| **Factual Correctness** | pregunta, respuesta, respuesta de referencia | Contraste de las afirmaciones con la referencia. |
| **Conducta consolidada 0–2** | rúbrica ciega | 2 cumplimiento completo, 1 parcial, 0 conducta incorrecta. |
| **Validez y presencia de citas** | comprobación determinista | Las citas pertenecen al top-5 suministrado y están presentes cuando la conducta las exige. |

Las cuatro métricas se calculan **para cada generador por separado**, sobre las mismas 416 celdas y con el mismo juez (§13), para que una diferencia entre generadores no pueda confundirse con una diferencia de criterio del evaluador.

Faithfulness y Factual Correctness se consideran **no aplicables** en las abstenciones sin afirmaciones sustantivas. Esa ausencia se reporta con su $n$ y **jamás se sustituye por cero**. El $n$ se reporta por generador, porque una abstención limpia puede no serlo por igual en los dos.

### 5.5. Eficiencia

- **Latencia de recuperación:** 5 rondas de calentamiento y 30 repeticiones de las consultas por condición, índices y modelos cargados, delimitación CUDA en dense y *reranking*.
- **Latencia de generación y tokens:** registros descriptivos, no un benchmark equivalente al de recuperación.

### 5.6. Resumen por comparación

Además del delta medio, cada indicador reporta el número de **mejoras, empates y retrocesos** por pregunta base, conforme al acta («resúmenes de mejora, empate y retroceso»).

---

## 6. Rúbrica de equivalencia de los pares

Instrumento fijado antes de redactar los pares. Se aplica a **todas** las parejas, incluidas las de las preguntas ya existentes.

### 6.1. Definición de las dos versiones

- **Versión explícita.** La pregunta emplea el término técnico de la fuente, presente literal o morfológicamente en el chunk que contiene la respuesta.
- **Versión implícita.** Retira ese término y formula la misma necesidad informativa con lenguaje descriptivo o cotidiano. No se sustituye por un sinónimo técnico que restaure el solape léxico.

### 6.2. Criterios

| ID | Criterio | Comprobación | Resultado |
|---|---|---|---|
| **R1** | Intención idéntica | Ambas versiones piden el mismo contenido; la implícita no es una versión más vaga ni añade una exigencia nueva. | aprueba / suspende |
| **R2** | Conducta esperada idéntica | Si la explícita se responde, la implícita también; si una exige corrección o abstención, la otra exige la misma. | aprueba / suspende |
| **R3** | Término técnico retirado | El término técnico que declara la pareja aparece en la versión explícita y **no** aparece en la implícita, comprobado por coincidencia de lemas. | aprueba / suspende |

R3 se verifica de forma determinista con `scripts/check_equivalence_rubric.py`, no por impresión. Cada pareja declara el término que manipula, y la comprobación exige presencia en la explícita y ausencia en la implícita. La declaración del término deja la comprobación abierta a auditoría.

Se descartó como criterio un cociente de solape léxico global por resultar confundido. Al sustituir un término técnico compacto por una descripción, la descripción reutiliza vocabulario general del fragmento y el cociente puede subir aunque el término se haya retirado; al aplicarlo sobre las siete parejas del piloto reprochó cuatro que sí manipulaban la explicitud. El solape de lemas se informa como dato descriptivo, junto al veredicto, pero no decide la aceptación.

### 6.3. Aplicación y discrepancias

1. El autor aplica R1 y R2 a cada pareja, dejando una justificación de una línea por criterio.
2. Un juez automático aplica R1 y R2 a todas las parejas de forma aislada, sin ver la valoración humana.
3. Las discrepancias se listan y se resuelven por **adjudicación manual documentada**, anotando el criterio resuelto y el motivo.
4. R3 se calcula por script y se conserva su salida junto a cada pareja.

Las parejas que suspendan R1, R2 o R3 se excluyen y se registra el motivo. No se reformulan para salvarlas: una pareja que no manipula una sola dimensión no sirve al experimento.

---

## 7. Criterios de selección de las 8 preguntas nuevas

Las preguntas se eligen para cubrir huecos analíticos, no para aumentar cifras. Reparto previsto:

| # | Tipo | N.º | Hueco que cubre |
|---|---|---:|---|
| 1 | Premisa falsa que el corpus refuta | 2 | La corrección fundamentada pasa de 2 a 4 casos |
| 2 | Evidencia multichunk sin fragmento único suficiente | 2 | Permite cuestionar MRR cuando ninguna posición primera basta |
| 3 | Evidencia redundante en varias secciones | 1 | Separa *toda la evidencia relevante* de *evidencia suficiente* |
| 4 | Fuera de dominio, adyacente al corpus | 1 | Completa la taxonomía de abstención |
| 5 | Exceso de evidencia, piezas sin síntesis | 1 | El caso más delicado de abstención |
| 6 | Síntesis transversal entre capítulos o manuales | 1 | Estresa el presupuesto de cinco fragmentos y a los híbridos |

Se mantiene el reparto de tipos del piloto (factual, explicativa, comparativa, procedimental) y el equilibrio entre los dos manuales.

---

## 8. Repeticiones y orden de ejecución

| Etapa | Repeticiones | Nota |
|---|---|---|
| Recuperación | 1 ejecución por consulta y condición | Determinista dado el índice y la consulta |
| Benchmark de latencia | 5 calentamientos + 30 repeticiones | Igual que §7.4 del piloto |
| Generación | **1 intento por unidad y generador** | Temperatura 0 y semilla fija, conscientes de que no garantizan determinismo. 208 unidades por generador, 416 en total. |
| Evaluación con juez | 1 pasada por unidad | |

**Orden.** La entrada se construye intercalando las preguntas base en orden redondo y alternando formulación, estrategia y **generador**, de modo que ninguna estrategia, ninguna formulación ni ningún generador quede sistemáticamente al principio. Se conserva el archivo de entrada con su orden, tal como en la campaña v2.

La generación se ejecuta en **una sola campaña**, sin mezclar respuestas históricas con nuevas como si sus condiciones fueran idénticas. Cada respuesta lleva su generador registrado; las dos condiciones comparten corpus, recuperación, instrucción, presupuesto de fragmentos y juez.

---

## 9. Tratamiento de errores y ausencias

Reglas vinculantes, ya establecidas en el piloto y aquí confirmadas:

1. Una unidad fallida se conserva como `failed` en su propio archivo y se excluye de los agregados. Se reporta aparte.
2. **Nunca** se reescribe una respuesta generada para convertir un fallo en válido. El diagnóstico aislado de un fallo no lo convierte en resultado.
3. Un fallo terminal no se reintenta al reanudar. La reanudación continúa desde la última unidad aceptada.
4. Una métrica no calculable se registra como ausente con su motivo. **No se sustituye por cero.**
5. Los errores del evaluador, *timeouts* y fallos de parseo se anotan por fila y se cuentan por separado; no se eliminan en silencio.
6. Las puntuaciones automáticas originales no se modifican al consolidar con la revisión humana; la consolidación añade campos nuevos.

---

## 10. Plan de análisis

- Diferencias emparejadas *implícita − explícita* por pregunta base, para cada métrica y estrategia, **calculadas por separado dentro de cada generador**.
- Delta medio con **intervalo de confianza del 95 % por remuestreo** sobre preguntas base (2.000 réplicas, semilla fija).
- Recuento de mejoras, empates y retrocesos.
- Desglose de generación por celda, con el $n$ de cada métrica visible.
- **Robustez (H5):** orden de estrategias por generador y detección de inversiones. Una inversión se reporta como hallazgo, sin promediar los dos generadores.
- **Sensibilidad al generador (H6):** contraste *celda a celda* —misma formulación, misma estrategia, distinto generador— de Faithfulness, Factual Correctness, conducta y citas. Se reporta el desplazamiento de nivel por separado del cambio en la diferencia explícita−implícita.
- **Interacciones** *generador × estrategia* y *generador × explicitud*, con el mismo procedimiento de remuestreo.

Los intervalos por remuestreo son una incorporación nueva, justificada porque con 30 unidades emparejadas son estables. Para mantener coherencia con el análisis principal del piloto, **no se añaden pruebas de significación paramétricas**: el informe se mantiene descriptivo con intervalos, y no se afirma superioridad estadística.

Todo análisis no previsto en este documento se marca como exploratorio.

---

## 11. Reglas de exclusión

Se excluyen, anotando el motivo:

- Las preguntas genuinamente ambiguas, que admitirían varias interpretaciones válidas y exigirían otro protocolo de generación y evaluación.
- Las parejas que suspendan R1, R2 o R3 (§6.3).
- Las preguntas cuya reformulación cambie la conducta esperada.

La exclusión se documenta por registro; no se sustituye en silencio por otra pregunta para alcanzar una cifra.

---

## 12. Lo que no se afirma

- **Fórmulas perdidas en la extracción del corpus.** El 6,9 % de los chunks (20 de 288) ha
  perdido contenido matemático al convertir los manuales a texto, y toca al 8,7 % de las
  unidades de qrels. El sesgo es asimétrico: esos fragmentos tenían más evidencia de grado 2
  que el resto. **No se corrige**, porque re-extraer invalidaría el *chunking* y los qrels sin
  alterar el ranking de estrategias. Las métricas de recuperación se reportan como estimaciones
  por defecto del rendimiento real, y sus valores absolutos no son comparables con los de
  corpus sin degradar. Cuantificación completa en `docs/limitacion-formulas-perdidas.md`.

- El juez local es un **diagnóstico**, no validación humana ni estimación poblacional.
- La auditoría por riesgo **no** es una estimación de precisión poblacional.
- No se mide aprendizaje de estudiantes: se evalúa la **fiabilidad informativa del sistema**, no su eficacia pedagógica.
- No se afirma superioridad estadística entre estrategias.
- El alcance queda limitado a este corpus, este idioma y estas condiciones de ejecución.
- La robustez observada aplica a **dos generadores de la misma familia** (Qwen 3.5 9B y Qwen 3.8 27B). No puede afirmarse que la conclusión sea independiente del generador en general.
- El generador de 27B **no cabe entero en la GPU disponible**: 4,76 GB de 8 GB, con el resto en memoria del sistema. Sus latencias y su coste no son representativos de cómo se comportaría con la memoria suficiente, y se reportan como tales.
- El juez de gradación B participó en el diseño de las preguntas nuevas y de las parejas. Su coincidencia con el juez A se reporta por origen de la pregunta, para que ese solape eventual sea medible y no invisible.

---

## 13. Asignación de jueces por fase

Fijada en la enmienda 1, antes de ejecutar. Cada rol tiene un juez estable aplicado a **todo** el material, para que una diferencia entre fases no pueda confundirse con una diferencia de criterio.

| Fase | Juez A | Juez B | Resolución |
|---|---|---|---|
| Gradación de relevancia — 578 pares base × chunk | `gpt-6-sol` (`openai-codex`, `--reasoning high`) | `mimo-v2.6-pro` (`opencode-go`) | Adjudicación humana del subconjunto de riesgo |
| Generación RAG — 416 celdas | `gpt-6-sol` (`openai-codex`, `--reasoning high`) | `gemma3:4b` (Ollama, sensibilidad) | Auditoría humana de los casos de riesgo |
| Rúbrica de equivalencia R1/R2 | — | — | Ya cerrada: 26 parejas con ratificación humana |
| Generación de respuestas | — | — | `qwen3.5:9b` y `qwen3.8:27b`, ambos locales por Ollama |

Los identificadores son los que devuelve el catálogo del proveedor, no nombres aproximados: `gpt-6-sol` y `gpt-6-sol-900k` son dos entradas distintas de `openai-codex` —la segunda es la variante de contexto largo— y se usa la primera, que basta para el tamaño de nuestras unidades. `mimo-v2.6-pro` es la entrada de `opencode-go`. Cada identificador se escribe tal cual en los qrels.

Mecanismo de invocación idéntico para los dos jueces, como sesiones Hermes aisladas:

```bash
hermes chat --oneshot --query-file <lote> -m gpt-6-sol      --provider openai-codex --reasoning high
hermes chat --oneshot --query-file <lote> -m mimo-v2.6-pro  --provider opencode-go
```

El aislamiento no se fabrica: cada `--oneshot` nace y muere sin acceso a la conversación de trabajo, a la hoja humana ni a las decisiones del otro juez.

### Arbitraje de discrepancias

Las discrepancias entre Juez A y Juez B se resuelven con un **tercer juez árbitro: `gpt-6-astra`** (`openai-codex`, `--reasoning high`), con dos salvaguardas.

1. **Presentación ciega.** El árbitro recibe el par de veredictos con etiquetas anónimas y en **orden aleatorizado por unidad**, de modo que no pueda inferir cuál procede de cuál modelo ni anclarse en la posición. La correspondencia etiqueta ↔ modelo se guarda en un fichero aparte que el árbitro no ve.
2. **Decisión propia.** El árbitro emite **su propio grado**, no una elección entre dos opciones, para que el veredicto no esté anclado a las propuestas.

**Cautela declarada.** `gpt-6-astra` y `gpt-6-sol` son variantes GPT-6 del mismo proveedor, y compartir linaje con una de las partes puede sesgar el arbitraje a su favor. Es la misma razón que excluyó a `mimo-v2.6-pro` de diseñar las preguntas y juzgarlas. La presentación ciega reduce el sesgo de anclaje pero no elimina el de familia, y así se reconoce.

**Validación humana.** El usuario revisa y valida las decisiones del árbitro. El árbitro no sustituye la revisión humana: la reduce a un número manejable. Queda declarado que una parte de las decisiones finales de gradación es automática.

Reglas vinculantes de la asignación:

1. **Un juez por rol en la pasada principal.** Donde hay dos, los dos corren sobre la totalidad del material, nunca uno por mitad.
2. **El mismo juez evalúa las dos condiciones de generador.** Si el evaluador cambiara con el generador, su efecto sería indistinguible del del generador.
3. **Aislamiento.** Cada juicio se emite en sesión independiente, sin acceso a la hoja humana, a los grados del otro juez ni al historial.
4. **Subconjunto de riesgo** de la gradación: cualquier grado 2 propuesto por cualquiera de los dos, toda discrepancia A−B, los conflictos de respondibilidad y los `equivalence_conflict`, y una muestra determinista de consensos 0/0 y 1/1 para auditar el acuerdo.
5. **Traza.** Cada grado registra modelo, versión de la instrucción y fecha de ejecución. La revisión asistida no se presenta nunca como humana.
6. **Las adjudicaciones humanas del piloto prevalecen** sobre cualquier gradación automática nueva y se conservan con su procedencia original.

## Anexo. Trazabilidad

| Artefacto | Contenido |
|---|---|
| `docs/explicitness_v3_preregistration.md` | Este documento, congelado antes de la ejecución |
| `data/golden/golden_set_pilot_v3.jsonl` | Golden set ampliado, 30 preguntas base |
| `config/equivalence_pairs_v3.jsonl` | Parejas explícito/implícito con la salida de R3 |
| `outputs/local_runs/explicitness_v3/` | Salidas de la campaña |
| `docs/explicitness_v3_execution.md` | Acta de fase, con hashes y desviaciones respecto a este pre-registro |
| `config/qrels_review_prompt_v3.md` | Instrucción de gradación de relevancia, versionada |
| `outputs/local_runs/explicitness_v3/pools/` | Pool técnico, cola ciega colapsada y gradaciones por juez |
