# Guía de redacción académica del TFM

## Propósito

Esta guía establece el criterio de redacción del TFM. Como pauta general, los párrafos argumentativos, explicativos e interpretativos seguirán una versión académica de las estructuras **1/3/1** o **1/5/1**.

Estas estructuras no obligan a escribir cinco o siete frases. Representan una secuencia de funciones que ayuda a construir párrafos con una idea principal, evidencia suficiente, interpretación propia y una conclusión que haga avanzar el argumento.

La regla básica es:

> **Afirmación → delimitación → evidencia → interpretación → conclusión**

Antes de cerrar un párrafo deben poder responderse cinco preguntas:

> **¿Qué afirmo? → ¿Qué significa? → ¿Qué evidencia tengo? → ¿Qué implica? → ¿Adónde conduce?**

## 1. Estructura académica 1/3/1

La estructura 1/3/1 se utilizará cuando una idea pueda desarrollarse mediante una afirmación principal, tres funciones de apoyo y una conclusión.

| Función | Pregunta que responde | Contenido habitual |
|---|---|---|
| Afirmación | ¿Qué sostiene el párrafo? | Idea principal concreta |
| Delimitación | ¿Qué significa exactamente? | Definición, mecanismo o alcance |
| Evidencia | ¿Qué la respalda? | Bibliografía, dato, tabla o resultado |
| Interpretación | ¿Por qué importa? | Relación con el problema del TFM |
| Conclusión | ¿Qué se deriva? | Deducción o transición |

### 1.1. Afirmación principal

La primera frase debe expresar la idea que el párrafo pretende demostrar, explicar o desarrollar. Debe ser concreta, relevante para la sección, coherente con el texto anterior y susceptible de recibir respaldo.

**Apertura débil:**

> En la actualidad, la inteligencia artificial es muy importante.

**Apertura más precisa:**

> La calidad de la recuperación condiciona directamente el rendimiento de un sistema RAG.

La segunda formulación permite anticipar el contenido del párrafo y exige explicar un mecanismo concreto.

### 1.2. Delimitación o explicación

La segunda función aclara el significado de la afirmación. Puede definir un concepto, describir un mecanismo, establecer el alcance o distinguir términos próximos.

> En estas arquitecturas, el modelo generativo produce la respuesta a partir de los fragmentos seleccionados previamente por el componente de recuperación.

Esta unidad evita que la afirmación principal quede en un nivel excesivamente general.

### 1.3. Evidencia

La afirmación debe respaldarse mediante evidencia pertinente. Esta puede proceder de:

- una referencia bibliográfica;
- varios estudios relacionados;
- una tabla o figura;
- una definición académica;
- los resultados del experimento;
- una comparación entre configuraciones;
- una observación sistemática del análisis de errores.

La cita debe situarse junto a la afirmación específica que respalda. No basta con colocar una referencia al final de una opinión general.

> Los marcos de evaluación de RAG distinguen los fallos producidos durante la recuperación de los originados en la generación [@es2024ragas; @ru2024ragchecker].

### 1.4. Interpretación

La interpretación explica qué significa la evidencia dentro del argumento del TFM. Debe responder al menos a una de estas preguntas:

- ¿Qué demuestra la evidencia?
- ¿Por qué es relevante?
- ¿Qué decisión metodológica justifica?
- ¿Qué limitación revela?
- ¿Cómo se relaciona con la pregunta de investigación?

> Esto implica que una evaluación centrada exclusivamente en la respuesta final podría ocultar errores originados durante la recuperación.

Sin esta función, el texto puede convertirse en una sucesión de citas o resultados sin hilo argumental.

### 1.5. Conclusión o transición

La última frase debe indicar qué se deriva del párrafo. Puede cerrar la idea o preparar el siguiente bloque.

**Conclusión interna:**

> En consecuencia, la evaluación del sistema debe considerar separadamente la recuperación y la generación.

**Transición:**

> Esta distinción requiere definir métricas específicas para cada componente del pipeline.

El cierre no debe limitarse a repetir la primera frase con otras palabras.

## 2. Estructura académica 1/5/1

La variante 1/5/1 se utilizará cuando la idea necesite mayor desarrollo:

> **Afirmación → definición → mecanismo → evidencia → contraste → interpretación → conclusión**

Resulta apropiada cuando:

- se introduce un concepto complejo;
- se comparan dos o más enfoques;
- se integran varias fuentes;
- se justifica una decisión metodológica importante;
- se interpreta un resultado con varias explicaciones posibles;
- se necesita introducir una cautela o un contraargumento.

No debe emplearse únicamente para producir un párrafo más largo. Cada unidad debe cumplir una función diferente.

### Ejemplo conceptual

> La recuperación híbrida combina señales léxicas y semánticas para seleccionar documentos relevantes. Los métodos léxicos priorizan la coincidencia de términos, mientras que los densos representan consultas y documentos en un espacio vectorial. La combinación intenta conservar la precisión terminológica de BM25 y añadir la capacidad de detectar relaciones semánticas de los embeddings. La literatura ha mostrado que la fusión de rankings puede superar a recuperadores individuales en determinados escenarios [@cormack2009rrf; @wang2024ragbestpractices]. Sin embargo, la mejora depende del corpus, de los modelos y de la estrategia de fusión utilizada. Por ello, la superioridad del enfoque híbrido no debe asumirse de antemano, sino comprobarse bajo condiciones controladas. Esta necesidad justifica su inclusión como configuración experimental del TFM.

## 3. Cuándo aplicar cada estructura

| Situación | Estructura recomendada |
|---|---|
| Explicar una idea concreta | 1/3/1 |
| Introducir una definición sencilla | 1/3/1 |
| Justificar una métrica | 1/3/1 |
| Comparar varios métodos | 1/5/1 |
| Integrar varias fuentes | 1/5/1 |
| Interpretar un resultado complejo | 1/5/1 |
| Presentar una limitación con matices | 1/5/1 |

Estas pautas se aplicarán principalmente a párrafos argumentativos, explicativos e interpretativos. No es necesario forzarlas en listas, tablas, pies de figura, definiciones muy breves o secuencias puramente procedimentales.

## 4. Reglas generales de estilo

### 4.1. Una idea principal por párrafo

Cada párrafo debe poder resumirse en una afirmación. Si contiene dos conclusiones independientes, probablemente debe dividirse.

### 4.2. Evitar aperturas vacías o grandilocuentes

**Evitar:**

> La inteligencia artificial está llamada a revolucionar la educación.

**Preferir:**

> La inteligencia artificial generativa ha ampliado las posibilidades de apoyo automatizado al aprendizaje.

La segunda versión es más concreta, verificable y adecuada para un texto académico.

### 4.3. Evitar explicaciones antropomórficas

**Evitar:**

> El modelo fabrica una respuesta para satisfacer al usuario.

**Preferir:**

> El modelo puede generar una secuencia lingüísticamente plausible que no esté respaldada por hechos o fuentes verificables.

El modelo genera texto mediante patrones estadísticos; no actúa con una intención consciente.

### 4.4. Matizar afirmaciones absolutas

**Evitar:**

> El daño de una alucinación es inasumible en educación.

**Preferir:**

> Las respuestas incorrectas presentan un riesgo especialmente relevante en educación porque pueden incorporarse al proceso de aprendizaje del estudiante.

Los términos absolutos deben reservarse para casos en los que puedan justificarse con precisión.

### 4.5. Explicar las enumeraciones

Una lista puede identificar elementos, pero no sustituye el razonamiento. Si se afirma que una respuesta incorrecta confunde al estudiante, desperdicia esfuerzo y reduce la confianza, el texto debe explicar cómo se produce cada consecuencia y por qué resulta relevante.

### 4.6. Mantener el foco del TFM

La memoria debe presentar el trabajo como una comparación experimental de técnicas de Information Retrieval dentro de un sistema RAG educativo. El prototipo es soporte experimental, no el producto principal.

Cuando no se evalúen capacidades pedagógicas del sistema, conviene utilizar **sistema RAG educativo** en lugar de describirlo de forma general como **tutor de IA**.

### 4.7. Utilizar términos consistentes

Deben mantenerse distinciones claras entre:

- corrección;
- groundedness o fundamentación;
- faithfulness;
- citation correctness;
- precisión y cobertura del contexto;
- relevancia de la respuesta.

Los términos próximos no deben utilizarse como sinónimos sin una definición operacional.

## 5. Uso de citas y evidencia

### 5.1. Citar la afirmación exacta

Las citas deben colocarse junto a la proposición que respaldan. No deben acumularse al final de un párrafo si no queda claro qué afirmación sostiene cada fuente.

### 5.2. No confundir cita con demostración

Una referencia no convierte automáticamente una opinión en una afirmación demostrada. Debe comprobarse que la fuente respalda exactamente la idea formulada.

### 5.3. Distinguir tres voces

La redacción debe diferenciar entre:

1. **Literatura:** lo que sostienen otros trabajos.
2. **Resultados:** lo que muestran los experimentos ejecutados.
3. **Interpretación:** lo que se deduce de esos resultados.

**Literatura:**

> Lewis et al. introducen una arquitectura que combina recuperación y generación para tareas intensivas en conocimiento [@lewis2020rag].

**Resultado propio:**

> La configuración híbrida obtuvo el mayor Recall@10 en el corpus evaluado.

**Interpretación:**

> Este resultado sugiere que las señales léxicas y semánticas fueron complementarias en la colección estudiada.

La interpretación debe conservar el alcance real del resultado. No debe generalizarse a otros corpus sin evidencia adicional.

### 5.4. No inventar respaldo provisional

No se incorporarán referencias genéricas como `[Autor, año]` en la versión consolidada. Si una afirmación todavía carece de fuente, debe identificarse durante la revisión y documentarse antes de cerrar el apartado.

## 6. Adaptación según el capítulo

### 6.1. Introducción

Secuencia recomendada:

> **Problema → delimitación → evidencia → relevancia → transición**

El cierre debe conducir hacia la pregunta de investigación o los objetivos.

### 6.2. Marco teórico

Secuencia recomendada:

> **Concepto → definición → mecanismo → evidencia → síntesis → relevancia experimental**

El párrafo debe explicar por qué el concepto es necesario para comprender el experimento. El marco teórico no debe convertirse en una revisión enciclopédica de técnicas que no se utilizarán después.

### 6.3. Metodología

Secuencia recomendada:

> **Decisión → descripción → justificación → procedimiento → consecuencia evaluativa**

**Ejemplo:**

> El experimento utiliza Recall@k como métrica principal de cobertura. Esta métrica representa la proporción de elementos relevantes que aparece entre los primeros k resultados. Su elección responde a que un sistema RAG necesita recuperar la evidencia necesaria antes de generar una respuesta fundamentada. El valor se calculará para todas las preguntas del golden set y se agregará por configuración. De este modo, será posible comparar qué técnica pierde menos evidencia relevante durante la recuperación.

### 6.4. Resultados

Secuencia recomendada:

> **Resultado → dato → comparación → observación objetiva → respuesta parcial**

En este capítulo deben evitarse explicaciones causales extensas. Los valores deben proceder de artefactos experimentales reproducibles.

**Ejemplo de forma, no de resultado real:**

> La configuración híbrida presentó el mayor rendimiento de recuperación. La diferencia se observó en Recall@10 y nDCG@10, mientras que la mejora en MRR@10 fue más limitada. Frente a BM25, el método recuperó más evidencia relevante, aunque no siempre la situó en la primera posición. Este patrón fue consistente en la mayoría de los tipos de pregunta evaluados. El resultado aporta evidencia parcial a favor de combinar señales léxicas y semánticas.

### 6.5. Discusión

Secuencia recomendada:

> **Interpretación → relación con resultados → contraste bibliográfico → implicación → cautela**

**Ejemplo de forma:**

> La mejora observada en la configuración híbrida sugiere que las señales léxicas y semánticas resultaron complementarias en el corpus estudiado. Este patrón es coherente con trabajos que combinan rankings procedentes de recuperadores diferentes [@cormack2009rrf; @wang2024ragbestpractices]. La ganancia, sin embargo, debe interpretarse junto con el aumento de latencia y complejidad operativa. En un sistema con restricciones estrictas, una mejora pequeña podría no compensar el coste adicional. Por tanto, la recomendación final dependerá del equilibrio entre calidad y eficiencia requerido por cada escenario.

## 7. Coherencia entre párrafos y secciones

La estructura 1/3/1 se aplica a cada párrafo, pero la sección completa también debe formar una cadena argumentativa. Los párrafos no deben funcionar como bloques aislados.

Para **1.1. Contexto y motivación**, la progresión será:

> **Potencial educativo → requisito de fiabilidad → alucinaciones → consecuencias educativas → RAG como respuesta → importancia de la recuperación → necesidad de comparación**

| Párrafo | Función | Transición esperada |
|---|---|---|
| 1 | Potencial educativo | La utilidad exige fiabilidad |
| 2 | Problema de las alucinaciones | La fluidez no garantiza veracidad |
| 3 | Consecuencias educativas | El problema también es pedagógico |
| 4 | RAG como respuesta | La recuperación es central |
| 5 | Dependencia del retrieval | Las estrategias deben compararse |
| 6 | Motivación experimental | Paso al problema de investigación |

El último párrafo de 1.1 debe preparar **1.2. Problema y pregunta de investigación**, pero no desarrollar todavía todos los objetivos ni anticipar resultados.

## 8. Ejemplo completo de párrafo 1/3/1

> La estrategia de recuperación determina qué evidencia recibe el modelo generativo. En un sistema RAG, los documentos situados en las primeras posiciones se incorporan al contexto utilizado para construir la respuesta. Los marcos de evaluación actuales muestran que los errores de recuperación y de generación pueden diagnosticarse como componentes distintos del pipeline [@es2024ragas; @ru2024ragchecker]. Esto implica que una respuesta incorrecta no puede atribuirse automáticamente al modelo de lenguaje, ya que el fallo puede haberse originado en la selección de los fragmentos. Por consiguiente, el diseño experimental debe evaluar de forma separada la recuperación y la generación.

Funciones:

1. **Afirmación:** la recuperación determina la evidencia disponible.
2. **Delimitación:** se explica cómo llega esa evidencia al modelo.
3. **Evidencia:** se incorpora respaldo bibliográfico.
4. **Interpretación:** se localiza el posible origen del error.
5. **Conclusión:** se deriva una decisión metodológica.

## 9. Lista de revisión de cada párrafo

Antes de considerar cerrado un párrafo, comprobar:

- [ ] ¿Puede resumirse en una idea principal?
- [ ] ¿La primera frase formula esa idea con precisión?
- [ ] ¿Se define o delimita lo necesario?
- [ ] ¿Las afirmaciones externas tienen evidencia?
- [ ] ¿Las citas respaldan exactamente la frase asociada?
- [ ] ¿Se interpreta la evidencia o el resultado?
- [ ] ¿Se distingue literatura, resultado e interpretación?
- [ ] ¿El cierre aporta una deducción o transición?
- [ ] ¿El párrafo prepara el siguiente?
- [ ] ¿Se evita un tono absoluto, grandilocuente o antropomórfico?

## 10. Lista de revisión de cada sección

Antes de cerrar una sección, comprobar:

- [ ] ¿Los párrafos siguen una progresión reconocible?
- [ ] ¿Cada párrafo cumple una función diferente?
- [ ] ¿La sección responde a su título?
- [ ] ¿Se evita invadir el contenido de apartados posteriores?
- [ ] ¿Las decisiones metodológicas están justificadas?
- [ ] ¿Las conclusiones se apoyan en evidencia real?
- [ ] ¿La última frase conduce al siguiente apartado?

## 11. Regla operativa del TFM

La estructura 1/3/1 será la pauta por defecto para los párrafos argumentativos, explicativos e interpretativos. Se utilizará 1/5/1 cuando la complejidad de la idea exija definiciones, mecanismos, contrastes o cautelas adicionales.

La estructura se aplicará con flexibilidad. La prioridad no es cumplir un número de frases, sino asegurar que cada párrafo contiene una afirmación clara, evidencia pertinente, interpretación propia y una conclusión que hace avanzar el argumento general del TFM.
