## Introducción a los algoritmos aleatorizados

El análisis de estructuras de datos avanzadas, como los **treaps** y los **filtros Bloom** requiere, muchas veces, comprender la base de los algoritmos aleatorizados, una clase de métodos de computación en los que la aleatoriedad juega un rol crucial. En la percepción común de muchos desarrolladores y científicos de la computación, la palabra "algoritmo" suele asociarse de inmediato a una serie de instrucciones deterministas, en las que, dada una entrada específica, se espera siempre la misma salida tras ejecutar la misma secuencia de pasos. No obstante, esta visión resulta limitada cuando se estudian técnicas en las que el comportamiento interno se apoya en decisiones aleatorias.

### Problemas de decisión y su relevancia en algoritmos aleatorizados

Para abordar la complejidad de ciertos algoritmos, es fundamental comprender los **problemas de decisión**, en particular aquellos clasificados como problemas de decisión binaria. En este contexto, se trata de determinar si una determinada propiedad se cumple o no para un conjunto dado de datos. Cuando se implementan algoritmos de clasificación binaria, se asignan, en esencia, dos etiquetas, por ejemplo "verdadero" o "falso" a cada instancia de entrada. Esta aproximación, aunque simplificada conceptualmente, tiene profundas implicaciones en la optimización de problemas complejos.

#### **1. Conceptualización de los problemas de decisión**

Un problema de decisión puede pensarse como una pregunta binaria cuya respuesta es "sí" o "no". La importancia de este tipo de problemas radica en que gran cantidad de problemas de optimización pueden reformularse como problemas de decisión. Por ejemplo, si se desea encontrar el camino más corto en un grafo, se puede transformar el problema optimizacional en uno de decisión estableciendo un umbral **T**. La pregunta sería: "¿Existe un camino cuya longitud sea, a lo sumo, T?" Al resolver este problema para distintos valores de **T** mediante métodos como la búsqueda binaria, es posible reconstruir la solución al problema original.

Esta formulación resulta especialmente relevante para los algoritmos aleatorizados, ya que muchas de estas técnicas se apoyan en la comparación y verificación de condiciones de éxito en tiempo real y con limitaciones en los recursos computacionales. En entornos donde los datos son masivos o la complejidad del problema es alta, reestructurar la pregunta en términos de decisiones binarias simplifica significativamente el proceso de validación y evaluación del algoritmo.

#### **2. Aplicaciones en la vida real**

Los problemas de decisión se encuentran en diversas áreas del conocimiento. En aprendizaje automático, por ejemplo, la clasificación de imágenes o la detección de fraudes se aborda mediante algoritmos que, en esencia, deben decidir entre múltiples posibilidades. En estos casos, el desempeño del algoritmo no solo depende de la rapidez con la que responde sino, más importante aún, de la fiabilidad y exactitud de sus respuestas.

Asimismo, en dominios donde se manejan datos sesgados o desequilibrios en las clases (como en el diagnóstico de enfermedades raras en medicina), comprender cómo se comportan los algoritmos de decisión resulta vital para evitar interpretaciones erróneas que puedan comprometer el análisis y la posterior toma de decisiones clínicas. La capacidad de transformar problemas de optimización en problemas de decisión incrementa el espectro de estrategias aplicables, permitiendo el uso de herramientas y métodos de verificación fundamentados en la teoría de la computación.


### **Algoritmos de Las Vegas** 

Dentro del campo de los algoritmos aleatorizados, los algoritmos de **Las Vegas** ocupan un lugar particular debido a sus características de funcionamiento. Estos algoritmos tienen la peculiaridad de siempre producir un resultado correcto o, en caso contrario, reportar de forma explícita la imposibilidad de hallar la solución. Sin embargo, lo que varía es el tiempo o los recursos consumidos durante la ejecución, los cuales son impredecibles a priori.

#### **1. Características y definición**

Un algoritmo de Las Vegas se define mediante dos propiedades clave:
- **Correctitud garantizada:** Independientemente de la secuencia de decisiones aleatorias tomadas durante la ejecución, el algoritmo siempre entrega como salida la solución correcta al problema, o en su defecto, indica que no ha logrado encontrarla.
- **Recursos aleatorios:** La cantidad de recursos (tiempo, memoria, operaciones computacionales) necesarios para alcanzar la solución es variable y no se puede determinar con antelación en función del único tamaño o tipo de la entrada.

Una consecuencia directa de estas propiedades es que el análisis del rendimiento de dichos algoritmos se centra en el estudio de su consumo en promedio, en lugar de garantizar un límite determinista en el peor de los casos. Esto significa que, si bien el resultado es siempre correcto, el tiempo de ejecución puede variar ampliamente entre ejecuciones, lo que introduce un componente probabilístico en el estudio del rendimiento computacional.

>Revisar : [When to Choose Randomized Algorithms: Understanding Las Vegas and Monte Carlo Algorithms](https://medium.com/@sachin.shreya21/when-to-choose-randomized-algorithms-understanding-las-vegas-and-monte-carlo-algorithms-9324d5e9f996)

#### 2. Ejemplo del Quicksort aleatorizado

Uno de los ejemplos más emblemáticos de algoritmo de Las Vegas es el **quicksort aleatorizado**. Este algoritmo ordena un conjunto de elementos mediante el uso de un pivote seleccionado aleatoriamente en cada paso recursivo. La ventaja de elegir el pivote de forma aleatoria es que se reduce significativamente la probabilidad de enfrentar el peor caso, que en el caso del quicksort determinista se presenta cuando los datos están ordenados o casi ordenados.

Aunque la solución del quicksort aleatorizado es siempre correcta, es decir, la lista se ordena de manera adecuada, el número de comparaciones y el número de intercambios entre elementos puede fluctuar, oscilando en promedio alrededor de *O(nlog n)*, pero pudiendo alcanzar *O(n²)* en casos atípicos. Este fenómeno evidencia la esencia de los algoritmos de Las Vegas: un compromiso entre la certeza en la salida y la imprevisibilidad en el consumo de recursos.

####  3. Implicaciones en el diseño de algoritmos

El uso de algoritmos de Las Vegas tiene profundas implicaciones para el diseño de sistemas y aplicaciones que requieren robustez y fiabilidad. Al garantizar que la salida es correcta, estos algoritmos permiten enfocar la optimización en la eficiencia y la adaptación de recursos. En aplicaciones prácticas, como el análisis de grandes bases de datos o la simulación de sistemas complejos, se puede aceptar la incertidumbre en los tiempos de ejecución a cambio de asegurar resultados verídicos y precisos.

Además, la característica de recursos impredecibles conduce al diseño de sistemas híbridos, en los que se combina un algoritmo de Las Vegas con mecanismos que limitan la cantidad de recursos disponibles. Por ejemplo, en entornos con restricciones de tiempo real, es posible detener el algoritmo después de un número específico de operaciones y recurrir a un método de Monte Carlo para obtener una solución aproximada, lo que da lugar a un interesante intercambio entre exactitud y eficiencia.

### Algoritmos de Monte Carlo

Los **algoritmos de Monte Carlo** representan otra vertiente de los algoritmos aleatorizados, en la que la aleatoriedad se utiliza de manera diferente. A diferencia de los algoritmos de Las Vegas, los métodos Monte Carlo pueden producir soluciones incorrectas, pero garantizan que el consumo de recursos es determinista, lo que permite predecir tiempos de ejecución o requerimientos de memoria.

#### 1. Definición y propiedades esenciales

Un algoritmo de Monte Carlo se caracteriza por:

- **Salida potencialmente incorrecta:** La respuesta generada puede, en ciertas ocasiones, ser equivocada. La probabilidad de error se controla como un compromiso con los recursos utilizados; es decir, al invertir más recursos se puede reducir la probabilidad de equivocación.
- **Consumo de recursos determinista:** A diferencia de los algoritmos de Las Vegas, el uso de recursos se fija de antemano y no varía de forma aleatoria entre ejecuciones. Esto es especialmente valioso en aplicaciones donde la predictibilidad del rendimiento es crítica.

Dentro de este marco, se distinguen tres escenarios particulares en problemas de decisión binaria:
- Un algoritmo que es siempre correcto cuando la salida es **falsa** (conocido como algoritmo con sesgo hacia el falso).
- Un algoritmo que es siempre correcto cuando devuelve **verdadero** (algoritmo con sesgo hacia el verdadero).
- Un algoritmo que puede fallar indistintamente en ambos casos.

Esta clasificación posibilita diseñar aplicaciones que se adapten a las necesidades específicas de cada situación. Por ejemplo, en ciertos sistemas de seguridad informática, puede ser preferible que el algoritmo sea riguroso al negar una condición (es decir, que al devolver "falso" la predicción siempre sea correcta), mientras que en otros ámbitos es más crítico el acierto cuando se predice "verdadero".

#### 2. Compromisos entre precisión y recursos

El enfoque Monte Carlo introduce la posibilidad de intercambiar exactitud por eficiencia. Consideremos un algoritmo **A** que siempre encuentra la solución correcta, pero cuyo consumo de recursos es impredecible. En un escenario real, si se dispone de una cantidad finita de recursos, se puede ejecutar el algoritmo **A** solo hasta cierto límite de recursos (por ejemplo, un número fijo de intercambios o un límite temporal). Si el algoritmo no ha concluido, se devuelve la mejor solución aproximada obtenida hasta ese momento. Este mecanismo es fundamental en aplicaciones donde una solución aproximada es aceptable a cambio de predecir y controlar el uso de recursos.

Los algoritmos de Monte Carlo se emplean a menudo en situaciones donde la exactitud completa es menos crítica que la obtención de una respuesta en un tiempo razonable. En simulaciones, en estimaciones probabilísticas y en la optimización de problemas complejos, la utilización de estos métodos permite obtener resultados aceptables sin comprometer de forma excesiva la eficiencia computacional. Por ejemplo, en la simulación de procesos físicos o en la resolución de problemas de integración numérica en espacios de alta dimensión, la precisión puede ser controlada y afinada en función de la cantidad de muestras aleatorias generadas.

#### 3. Ejemplos prácticos y aplicaciones

Entre los ejemplos prácticos de algoritmos de Monte Carlo se encuentra la aproximación de ciertos cálculos matemáticos o integrales, donde la alta dimensionalidad impide la utilización de métodos analíticos convencionales. Otro ejemplo es la estimación de la confiabilidad de sistemas complejos mediante simulaciones, en los cuales las condiciones iniciales se varían aleatoriamente para explorar diferentes escenarios. Asimismo, en la criptografía se utilizan técnicas Monte Carlo para evaluar la solidez de ciertos algoritmos y protocolos, basándose en el análisis probabilístico de posibles ataques.

En el ámbito del aprendizaje automático, muchos clasificadores se entrenan mediante métodos que implican una componente aleatoria, y se pueden evaluar utilizando parámetros como la precisión y la exahustividad (ver sección de métricas a continuación). En estos casos, aunque el algoritmo pueda incurrir en errores en ciertas instancias, la robustez del modelo general se asegura mediante técnicas de validación cruzada y ajuste de parámetros, permitiendo un equilibrio óptimo entre recursos y calidad de la predicción.


### Métricas de clasificación en algoritmos aleatorizados

El análisis de algoritmos aleatorizados no se limita únicamente a su tiempo de ejecución y consumo de memoria. En muchos contextos, especialmente en aplicaciones de machine learning y estructuras de datos, es fundamental evaluar la calidad de la solución en términos de clasificación. Esto implica utilizar métricas que midan no solo la cantidad de aciertos, sino también la distribución de los errores y la capacidad del modelo para discriminar correctamente entre distintas clases.

#### 1. Evaluación con exactitud

Una forma de medir la calidad de un algoritmo de clasificación es evaluar su **tasa de predicciones correctas**. Supongamos que, sobre un conjunto de `NP` puntos que en realidad pertenecen a la clase **verdadera**:

- `PP` son predichos como verdaderos.
- `TP`, conocidos como **verdaderos positivos**, son aquellos puntos que fueron predichos como verdaderos y que en efecto pertenecen a la clase verdadera.

De manera similar, sea `NN` el número de puntos que pertenecen a la **clase falsa**:

- `PN` es el número total de puntos para los cuales nuestro algoritmo predijo la clase falsa.
- `TN`, llamados **verdaderos negativos**, representan la cantidad de veces en que tanto la clase predicha como la real de un punto son falsas.

Con estos valores, podemos definir la **exactitud**: `(TP + TN)/(PN + TN)`

> Cuando la exactitud es 1, significa que tenemos un algoritmo que **siempre acierta**.

Sin embargo, salvo en ese caso ideal, la exactitud **no siempre es una buena medida** de la calidad de nuestros algoritmos. Considera un caso extremo donde el **99% de los puntos en una base de datos pertenecen a la clase verdadera**. Observa los siguientes tres clasificadores:

- Un clasificador que etiqueta correctamente el 100% de los puntos falsos y el 98.98% de los verdaderos.
- Un clasificador que etiqueta correctamente solo el 0.5% de los puntos falsos, pero el 99.49% de los verdaderos.
- Un clasificador que **siempre retorna "verdadero"** como etiqueta.

Sorprendentemente, este último tiene **mejor exactitud** que los otros dos, aunque **falla completamente** en reconocer los puntos falsos.


En aprendizaje automático, si usáramos esta métrica sobre un conjunto de entrenamiento **desbalanceado de forma similar**, obtendríamos un modelo terrible, o más precisamente, un modelo que probablemente **generalice muy mal**.

#### 2.  **Precisión y recall**

Para mejorar la evaluación más allá de la exactitud simple, necesitamos tener en cuenta la información **por categoría**. Para esto, se pueden definir dos métricas adicionales:

- **Precisión** (también llamada **valor predictivo positivo**): se define como la proporción de puntos verdaderos correctamente predichos (**verdaderos positivos**) sobre el número total de puntos que el algoritmo predijo como "verdaderos".

    precision = `TP/PP`
  
- **Recall** (también conocido como **exahustividad**): se define como la fracción de verdaderos positivos sobre el número total de puntos que en realidadpertenecen a la clase verdadera.

    recall = `TP/PN`

También es posible redefinir precisión y recall introduciendo:

- **FP (falsos positivos)**: puntos que en realidad pertenecen a la clase falsa pero que el algoritmo predijo como verdaderos.
- **FN (falsos negativos)**: puntos que en realidad pertenecen a la clase verdadera pero que el algoritmo predijo como falsos.

  precision = `TP/TP + FP`

  recall = `TP/TP + FN`
  

De forma intuitiva, mientras que la exactitud solo mide qué tan bien realizamos las predicciones en general, **precisión y recall ponderan nuestros aciertos considerando los errores en la categoría contraria**.

De hecho, precisión y recall **no son independientes**: una puede expresarse en función de la otra, por lo que no es posible mejorar ambas indefinidamente. En general, si mejoras el recall, probablemente **sacrifiques algo de precisión**, y viceversa.

En clasificadores de aprendizaje automático, cada modelo puede representarse con una **curva de precisión/recall**, y los parámetros del modelo se pueden ajustar durante el entrenamiento para encontrar un equilibrio entre ambas características.


#### Interpretación de precisión y recall

- Para una clasificación binaria, tener una **precisión del 100%** significa que todos los puntos etiquetados como "verdaderos" realmente pertenecen a la clase verdadera.
- Tener un **recall del 100%** significa que **no hay falsos negativos**, es decir, todos los verdaderos fueron correctamente identificados.

#### 3. La medida F y otras métricas adicionales

Adicionalmente a la precisión y la exahustividad, se ha propuesto la utilización de la **medida F** para integrar ambas métricas en un único indicador de desempeño. La medida **F** es especialmente útil en escenarios donde se desea una comparación equilibrada entre la capacidad del algoritmo para identificar correctamente casos positivos y para minimizar los errores. Aunque la fórmula exacta de la medida **F** (por ejemplo, la **F1**) combina de manera armónica la precisión y la exahustividad, su uso se extiende principalmente a fines comparativos y de ajuste en modelos de aprendizaje automático.

Al abordar el desempeño de clasificadores en ámbitos complejos, se pueden definir otras métricas, tales como la tasa de falsos positivos y la tasa de falsos negativos, las cuales permiten comprender en detalle el perfil de errores del algoritmo. Este análisis minucioso es indispensable cuando se desarrollan sistemas donde los costos de equivocación son elevados, ya sea en seguridad, finanzas o aplicaciones médicas.

Si continuamos con la analogía de los filtros Bloom, podemos resumir el significado de las métricas en ese contexto:

- **Exactitud** responde a: *¿Qué porcentaje de las llamadas a `contains` fueron correctas?*
- **Precisión** responde a: *¿Qué porcentaje de las llamadas a `contains` que retornaron "true" fueron correctas?*
- **Recall** responde a: *Entre todas las llamadas a `contains` sobre elementos realmente contenidos en el filtro, ¿qué porcentaje devolvió "true"?* (En este caso, **siempre será 100%** para los filtros Bloom).

### Integración de algoritmos aleatorizados en aplicaciones reales

La implementación de algoritmos de Las Vegas y de Monte Carlo no se limita a la teoría; su aplicación en el desarrollo de sistemas robustos y eficientes es extensa en la práctica. A continuación, se examinan algunas áreas en las que estos algoritmos han demostrado su eficacia.

#### 1. Optimización y computación de alta dimensión

En problemas de optimización de alta dimensión, el uso de técnicas aleatorizadas resulta fundamental para explorar el espacio de soluciones de forma eficiente. Algoritmos como el quicksort aleatorizado o métodos basados en la simulación Monte Carlo permiten abordar problemas que, de otra manera, serían intratables mediante métodos deterministas convencionales. Estas técnicas son especialmente valoradas en contextos de inteligencia artificial y análisis de grandes volúmenes de datos, donde la variabilidad en la ejecución se convierte en una herramienta para evitar soluciones locales subóptimas.

El enfoque aleatorizado, al introducir variabilidad en la exploración de posibles soluciones, permite superar barreras que imponen las condiciones estrictamente deterministas. Por ejemplo, en problemas de optimización combinatoria, la búsqueda de la solución óptima se facilita al incorporar elementos aleatorios que permiten escapar de óptimos locales, ampliando la posibilidad de identificar la mejor solución global.

#### 2. Simulación y modelado estocástico

En el campo de la simulación y el modelado estocástico, los algoritmos Monte Carlo son una herramienta esencial para estimar parámetros y comprender el comportamiento de sistemas complejos. Estas simulaciones se utilizan en finanzas para la valoración de derivados, en física para modelar procesos de partículas, y en ingeniería para la realización de análisis de riesgos. En cada uno de estos casos, el compromiso entre la precisión de la aproximación y el consumo determinista de recursos es cuidadosamente ajustado, permitiendo obtener resultados útiles sin necesidad de una ejecución completa y exhaustiva del algoritmo.

La naturaleza estocástica de estos métodos posibilita la generación de distribuciones de resultados que, al ser analizadas estadísticamente, ofrecen una imagen del desempeño y la estabilidad del sistema modelado. Esta capacidad de cuantificar la incertidumbre resulta especialmente valiosa en contextos donde la variabilidad intrínseca es alta y los métodos deterministas no capturan la complejidad del fenómeno.

#### 3. Aplicaciones en criptografía y seguridad informática

El uso de algoritmos aleatorizados es también una constante en la criptografía y en el diseño de protocolos de seguridad. La generación de claves, la creación de números aleatorios seguros y la evaluación de la robustez de algoritmos de cifrado son áreas en las que la aleatoriedad es aprovechada para mejorar la seguridad. En estos escenarios, la capacidad de los algoritmos de Monte Carlo para operar bajo un consumo predecible de recursos resulta esencial para garantizar una respuesta en tiempo real y prevenir vulnerabilidades derivadas de la predictibilidad de los procesos.

Además, los algoritmos de Las Vegas se utilizan en el contexto del análisis de vulnerabilidades, donde la certeza en la identificación de potenciales brechas es crucial. La garantía de obtener resultados correctos, aun cuando se incurra en un consumo variable de recursos, permite diseñar sistemas de monitoreo que detecten anomalías de manera precisa, mejorando la resiliencia del sistema ante ataques.

### Desafíos y consideraciones de implementación en algoritmos aleatorizados

El uso de algoritmos aleatorizados, si bien ofrece ventajas evidentes en términos de eficiencia y simplicidad, también presenta desafíos que deben abordarse para garantizar su viabilidad en aplicaciones críticas.

#### 1. Generación y calidad de la aleatoriedad

Uno de los aspectos fundamentales es la generación de números aleatorios de alta calidad. La seguridad y la robustez de un algoritmo aleatorizado dependen en gran medida de la entropía utilizada en la toma de decisiones internas. Los generadores pseudoaleatorios, si bien son adecuados para muchas aplicaciones, pueden resultar insuficientes en escenarios donde la predicción de resultados puede comprometer la seguridad o la integridad del sistema. Por ello, se hace imprescindible el uso de generadores de números aleatorios criptográficamente seguros en aplicaciones sensibles.

#### 2. Gestión de recursos en entornos limitados

En situaciones donde los recursos computacionales son limitados, encontrar un balance entre el uso de algoritmos de Las Vegas y Monte Carlo se vuelve esencial. La adaptación dinámica de la cantidad de iteraciones o de la tolerancia al error puede marcar la diferencia en la obtención de soluciones aceptables dentro de límites impuestos por el hardware o por restricciones de tiempo. Este ajuste fino requiere un monitoreo constante del desempeño del algoritmo y la capacidad de interrumpir procesos en curso cuando se sobrepasan umbrales críticos de consumo.

#### 3. Verificación y validación de resultados

La naturaleza inherente de los algoritmos aleatorizados implica que, en determinados casos, puedan generarse soluciones erróneas. Por ello, es fundamental desarrollar mecanismos de verificación que permitan asegurar la validez de los resultados, especialmente en aplicaciones donde una eventual equivocación puede generar consecuencias graves. La incorporación de pruebas de consistencia y de validación cruzada se convierte en un componente indispensable del proceso de desarrollo, permitiendo identificar y corregir desviaciones en el comportamiento del algoritmo.


