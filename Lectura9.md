###  Análisis de rendimiento en la implementación de un heap d-ario y su aplicación en la codificación de Huffman

**Referencia:** [Análisis completo del código de Huffman](https://github.com/kapumota/CC0E5/blob/main/Codigo_Huffman.ipynb)

#### Conceptos generales

El conjunto de códigos presentados combina dos componentes fundamentales: por un lado, la implementación de un heap d-ario (`DWayHeap`) y, por 
otro, la construcción de un árbol de Huffman a partir de una tabla de frecuencias derivada de un texto o incluso de una imagen (codificada en 
base64). 
La estructura del heap d-ario permite ajustar el factor de ramificación (`D`), lo que influye de manera directa en el comportamiento y rendimiento
de las operaciones fundamentales del heap, como la inserción y la extracción del elemento de mayor prioridad. 
El análisis de performance se centra en cómo varía el rendimiento al modificar este parámetro, explorando el trade-off entre la profundidad del árbol y el número de comparaciones realizadas en cada nivel.

El proceso de codificación de Huffman, por su parte, se apoya en el heap para seleccionar repetidamente los dos nodos con menor frecuencia
(o, en este caso, utilizando prioridades invertidas para trabajar con un heap máximo) y combinarlos en un nuevo nodo. De esta forma, se construye 
un árbol de codificación que asocia a cada símbolo un código binario único.


#### Análisis de la implementación del heap d-ario (DWayHeap)

**Estructura interna y principales operaciones**

La clase `DWayHeap` es una implementación genérica de un heap que permite especificar el número máximo de hijos (`D`) por nodo. En la construcción del heap se recibe una lista de elementos junto con sus prioridades asociadas, y se valida que ambas listas tengan la misma longitud. La estructura interna se mantiene mediante una lista de tuplas, donde cada tupla contiene la prioridad y el elemento correspondiente.

Entre las operaciones fundamentales se destacan:

- **Inserción (`insert`)**: Se agrega un nuevo par elemento/prioridad y se utiliza la operación `_bubble_up` para mantener la invariante del heap. Esta operación recorre el árbol desde el nodo insertado hacia la raíz, realizando intercambios si el nuevo elemento posee una prioridad mayor que la de su padre.

- **Extracción del elemento de mayor prioridad (`top`)**: Se extrae el primer elemento (la raíz) del heap. Para reestablecer la propiedad del heap, se coloca el último elemento en la raíz y se llama a `_push_down`, que lo desplaza hacia abajo mediante intercambios sucesivos con el hijo de mayor prioridad.

- **Operaciones auxiliares**: Las funciones `_first_child_index` y `_parent_index` calculan, de manera aritmética, los índices correspondientes al primer hijo y al padre de un nodo. Asimismo, la función `_highest_priority_child_index` se encarga de determinar, entre los hijos de un nodo, aquel con la mayor prioridad.

Cada una de estas operaciones se beneficia del uso de un heap d-ario, ya que al permitir un número variable de hijos se puede influir en la altura del árbol y, por consiguiente, en la cantidad de pasos que deben ejecutarse durante la inserción o extracción.

**Invariantes y validación**

El método `_validate` se encarga de comprobar que se cumplan las tres invariantes esenciales del heap:

1. **Número máximo de hijos**: Cada nodo tiene, como máximo, `D` hijos. Esta propiedad se garantiza a través del cálculo de índices.
2. **Árbol completo y alineado a la izquierda**: La estructura del heap se asegura de ser completa, lo que significa que todos los niveles están completamente llenos, excepto posiblemente el último, que se llena de izquierda a derecha.
3. **Propiedad de heap**: Cada nodo contiene la mayor prioridad dentro del subárbol cuya raíz es dicho nodo.

La validación recorre los nodos internos (aquellos que tienen hijos) y, para cada uno, compara su prioridad con la de sus hijos. En caso de encontrar algún hijo con prioridad mayor, se considera que la invariante se ha roto.


#### Integración con la codificación de Huffman

**Generación de la tabla de frecuencias**

El proceso inicia con la función `_create_frequency_table`, que recibe un texto (o contenido de una imagen en el caso de datos codificados en base64) y construye una tabla de frecuencias utilizando el módulo `collections.Counter`. Esta tabla asocia cada carácter o símbolo a su número de ocurrencias. El uso de esta estructura permite obtener de manera rápida y eficiente la frecuencia de cada elemento, información fundamental para la construcción del árbol de Huffman.

**Conversión de la tabla de frecuencias a un heap**

Una vez obtenida la tabla de frecuencias, la función `_frequency_table_to_heap` se encarga de convertirla en un heap d-ario. Se crea un nodo de Huffman para cada carácter, donde la prioridad se define como el negativo de la frecuencia (esto se hace para aprovechar la implementación de un heap máximo, ya que un menor número de ocurrencias se traduce en una prioridad mayor en términos absolutos después de la inversión).

La elección del factor de ramificación (`branching_factor`) en este paso es determinante, ya que influye en el comportamiento posterior del heap. Un factor de ramificación menor (por ejemplo, 2) implica una mayor profundidad del árbol, lo que puede aumentar la cantidad de intercambios en operaciones como `_bubble_up` y `_push_down`. Por otro lado, un valor mayor reduce la profundidad pero incrementa el número de comparaciones que se deben realizar en cada nivel.

**Construcción del árbol de Huffman**

La función `_heap_to_tree` implementa la lógica de construcción del árbol de Huffman. En un ciclo iterativo, se extraen los dos nodos con mayor prioridad del heap (esto equivale a obtener los nodos con menor frecuencia debido a la inversión de prioridades) y se combinan en un nuevo nodo. Este nodo combinado tiene como símbolos la concatenación de los símbolos de los nodos extraídos y como prioridad la suma de las prioridades (es decir, la suma de las frecuencias originales).

Una vez creado el nuevo nodo, se inserta de nuevo en el heap, de manera que el proceso se repite hasta que solo queda un nodo, que será la raíz del árbol de Huffman. Este procedimiento, basado en la estructura de heap, se beneficia de la eficiencia de las operaciones de inserción y extracción, y por ello resulta crucial el análisis de performance de dichas operaciones.

#### Análisis de rendimiento y la búsqueda del mejor factor de ramificación

**Impacto del factor de ramificación en las operaciones del heap**

El factor de ramificación, o branching factor, es un parámetro que define cuántos hijos puede tener cada nodo en el heap. Este parámetro afecta directamente la estructura interna del heap:

- **Con un factor de ramificación bajo (por ejemplo, 2)**: El heap se comporta como un heap binario. La profundidad del árbol será mayor, lo que puede derivar en un mayor número de pasos en operaciones recursivas o iterativas (como `_bubble_up` y `_push_down`). Cada paso implica la comparación entre el nodo actual y su padre o entre el nodo y sus hijos, lo que puede aumentar la latencia de la operación en función de la altura del árbol.

- **Con un factor de ramificación alto (por ejemplo, 20 o más)**: El árbol será más superficial, lo que puede disminuir la cantidad de niveles que se deben recorrer durante las operaciones de inserción y extracción. Sin embargo, el costo de comparar todos los hijos en cada nivel aumenta, ya que en cada nodo se deben evaluar potencialmente muchos más hijos para determinar cuál tiene la mayor prioridad.

Este comportamiento genera un trade-off en el que se debe encontrar un punto óptimo: un valor de `D` que minimice el tiempo total de ejecución para una determinada aplicación, en este caso la codificación de Huffman. La optimización de este parámetro se vuelve especialmente relevante en aplicaciones en las que se realizan múltiples operaciones de inserción y extracción, y donde el costo de las comparaciones puede ser un factor limitante.

**Trade-off entre profundidad y número de comparaciones**

El análisis de performance se centra en dos métricas principales:
 
- **Tiempo por llamada (_per_call_time_)**: Mide el tiempo promedio invertido en cada llamada a las funciones clave del heap (por ejemplo, `_bubble_up`, `_push_down`, `top`, `insert`).  
- **Tiempo acumulado (_cumulative_time_)**: Representa el tiempo total empleado por una función a lo largo de todas las llamadas realizadas durante la ejecución del algoritmo.

Al aumentar el factor de ramificación, se observa una reducción en la profundidad del árbol, lo que disminuye la cantidad de iteraciones en cada recorrido hacia arriba o hacia abajo. No obstante, en cada nivel se deben evaluar más hijos, lo que puede aumentar el costo computacional en ese nivel. De esta forma, se establece un equilibrio entre la profundidad y el número de comparaciones, el cual depende también del tamaño de la entrada y de la distribución de frecuencias en el caso del algoritmo de Huffman.

**Técnicas de profiling**

El conjunto de pruebas de profiling, implementado a través de la clase `HuffmanProfile`, ejecuta múltiples casos de prueba sobre diferentes archivos de texto e imágenes. Se varía el factor de ramificación desde 2 hasta 23, y se realizan numerosas ejecuciones (por ejemplo, 1000 iteraciones para archivos de texto y 200 para imágenes) para obtener una muestra estadística robusta del comportamiento.

Durante cada ejecución, se utilizan herramientas de profiling (como `cProfile` y `pstats`) para recolectar datos sobre el rendimiento de las funciones críticas, especialmente aquellas que contienen la palabra "heap" en su nombre o que están relacionadas con la función `create_encoding`. Estos datos se registran en archivos CSV (como `stats_huffman.csv`) para su posterior análisis mediante scripts de visualización basados en `pandas` y `matplotlib`.

Entre los gráficos generados se encuentran:

- **Box plots**: Que muestran la dispersión del tiempo de ejecución para cada valor del factor de ramificación. Estos gráficos permiten visualizar la variabilidad en el tiempo por llamada y cómo se comporta el algoritmo ante diferentes configuraciones.
- **Gráficas de promedios**: Que representan la media del tiempo de ejecución en función del factor de ramificación, facilitando la identificación del valor óptimo para un conjunto determinado de entradas.

La recopilación y análisis de estos datos de profiling proporcionan una base empírica para determinar cuál es el factor de ramificación que ofrece el mejor rendimiento en cada caso, teniendo en cuenta las diferencias en la naturaleza de las entradas (por ejemplo, archivos de texto versus imágenes).

A partir de los datos obtenidos, se puede observar que en escenarios donde la entrada es un archivo de texto extenso, la eficiencia del heap se ve afectada significativamente por la profundidad del árbol. Un factor de ramificación bajo implica más niveles y, por tanto, más llamadas recursivas o iterativas en las operaciones de reordenamiento, lo que incrementa el tiempo total. Por el contrario, en casos en los que se utiliza un factor de ramificación alto, el menor número de niveles puede compensar el costo adicional de comparar múltiples hijos en cada paso.

El análisis empírico, basado en los datos de profiling, permite determinar que existe un punto intermedio en el cual se optimiza el rendimiento global del algoritmo de Huffman. Este punto se encuentra al balancear el costo de las comparaciones y el número de intercambios necesarios para mantener la propiedad del heap.

#### El misterio con el heapify

**Rol y funcionamiento de la operación heapify**

La función `_heapify` es fundamental en la construcción del heap, ya que a partir de una lista desordenada de pares (prioridad, elemento) se construye una estructura que cumple con las invariantes del heap. Este proceso se realiza de manera eficiente mediante la aplicación de la función `_push_down` a cada nodo interno, empezando desde el último nodo que tiene hijos y avanzando hacia la raíz.

El procedimiento se basa en la idea de que, al ajustar los nodos en orden inverso, se garantiza que al llegar a la raíz, todos los subárboles ya cumplen con la propiedad del heap. Esta técnica, aunque conceptualmente simple, puede presentar ciertos comportamientos "misteriosos" en cuanto al número de intercambios (swaps) realizados durante el proceso.

**Análisis teórico y empírico del número de intercambios**

El misterio reside en el hecho de que, a pesar de que el algoritmo de heapify tiene una complejidad teórica de `O(n)`, el número real de intercambios depende de la estructura del árbol y, de manera directa, del factor de ramificación `D`. En el código se implementa la función `_push_down`, la cual es la responsable de reacomodar el subárbol a partir de un nodo dado. Esta función compara el elemento actual con el de mayor prioridad entre sus hijos y realiza intercambios sucesivos hasta que se restablece la invariante.

El comportamiento observado en la ejecución empírica puede variar notablemente entre diferentes ejecuciones, y es en este punto donde el análisis de profiling adquiere relevancia. Al ejecutar múltiples iteraciones y analizar la media y la dispersión del tiempo por llamada a `_push_down`, se puede inferir el número promedio de intercambios realizados durante el proceso de heapify para distintos valores de `D`. Esta información es esencial para entender cómo optimizar la función y ajustar parámetros para casos específicos.

#### Límite en el número de intercambios de _heapify

**La función heapify_swaps y su interpretación**

Dentro del código se define la función `heapify_swaps(n: int, D: int)`, que tiene como objetivo estimar el número de intercambios (swaps) que se realizarán durante la operación de heapify para un heap con `n` elementos y un factor de ramificación `D`. La fórmula utilizada en la función es la siguiente:

```python
return n / D * sum([math.ceil(h / (D**h)) for h in range(int(math.log(n, D)))])
```

Esta expresión busca capturar el comportamiento del heapify considerando dos factores clave:

- **El número de nodos internos**: Aproximadamente `n/D`, que corresponde a la cantidad de nodos que tienen al menos un hijo.
- **La suma de intercambios en cada nivel**: Se estima a través de una suma que involucra la función `math.ceil` aplicada a una relación que decrece exponencialmente en función de `D` y la altura `h` del nodo.

La función suma, a lo largo de h desde 0 hasta logaritmo en base `D` de `n`, una cantidad que intenta reflejar la cantidad máxima de intercambios necesarios en cada nivel del heap. La utilización de `math.ceil` garantiza que se cuente al menos un intercambio en niveles donde la división no resulte en un número entero, lo que es fundamental para obtener una cota superior del número de swaps.

**Comparativa para diferentes valores de n y D**

Al evaluar la función `heapify_swaps` para distintos valores de `n` (por ejemplo, 100, 1000, 10000, 100000) y variando el factor `D` entre 2 y 22, se observa una tendencia interesante:  
- Para un `n` fijo, al aumentar `D` se reduce la profundidad del árbol, lo que disminuye la cantidad de intercambios acumulados.  
- Sin embargo, el término `n/D` en la fórmula indica que a medida que `D` crece, el número total de nodos internos decrece, pero la suma de los intercambios en cada nivel puede comportarse de forma no lineal, debido a la función `ceil` y a la naturaleza logarítmica del rango.

La representación gráfica de estos datos, generada mediante matplotlib con una escala logarítmica en el eje y, permite visualizar cómo varía el número de swaps en función del factor de ramificación. Se puede apreciar que para ciertos valores intermedios de `D` se alcanza un mínimo en el número de intercambios, lo que sugiere un valor óptimo en términos de eficiencia del proceso de heapify.

Este análisis se vuelve especialmente relevante cuando se compara el comportamiento teórico estimado con los datos empíricos recolectados a través del profiling. En muchos casos, la cantidad de intercambios observada en la práctica se acerca a la cota superior calculada por la función `heapify_swaps`, lo que valida el uso de dicha función como herramienta predictiva y analítica.

#### Consideraciones adicionales en el profiling de la codificación de Huffman

**Casos de prueba: texto y imagen**

El sistema de profiling implementado contempla dos grandes categorías de casos de prueba:  
- **Casos de prueba de texto**: Utilizando archivos literarios (por ejemplo, "alice.txt", "candide.txt", "gullivers_travels.txt"), se puede analizar cómo la distribución de caracteres y la longitud del texto afectan el rendimiento global del algoritmo.  
- **Casos de prueba de imagen**: Aunque en este caso la imagen se procesa leyendo los bytes y codificándolos en base64, el proceso de construir una tabla de frecuencias y posteriormente un heap para la codificación de Huffman resulta muy diferente al de un texto. La naturaleza de los datos (mayor diversidad y diferente distribución de frecuencias) puede provocar que el rendimiento se vea afectado de manera distinta.

Cada uno de estos casos de prueba se ejecuta múltiples veces para acumular suficientes datos que permitan realizar un análisis estadístico robusto. La salida de estas ejecuciones se almacena en archivos CSV, lo que facilita la generación de gráficos y la comparación de métricas como el tiempo total, el tiempo acumulado y el tiempo por llamada para las funciones críticas del heap.

**Impacto de la distribución de frecuencias en el rendimiento**

En el contexto de la codificación de Huffman, la distribución de frecuencias es un factor determinante en la estructura final del árbol y, por ende, en el comportamiento de las operaciones de heap. Por ejemplo, en un texto donde ciertos caracteres se repiten de forma muy marcada, el heap contendrá muchos nodos con prioridades muy bajas (o, en este caso, valores altos debido a la inversión de la frecuencia) y otros con prioridades relativamente altas. Este desbalance puede influir en el número de intercambios realizados en la operación `_heapify`, ya que los nodos con menor frecuencia tienden a estar más "profundos" en la estructura.

El análisis de performance a través de las métricas de profiling permite observar cómo esta distribución se refleja en el tiempo de ejecución. Se pueden identificar patrones en los que, para una misma longitud de entrada, la variabilidad en la frecuencia de los símbolos influye de manera directa en la eficiencia de las operaciones de extracción e inserción en el heap.

Además, el uso de diferentes factores de ramificación interactúa con la distribución de frecuencias: un factor de ramificación alto puede amortiguar en cierta medida el costo de la reordenación en un heap desbalanceado, mientras que un factor bajo puede resultar en una mayor cantidad de intercambios, afectando negativamente el rendimiento en escenarios con alta variabilidad en las frecuencias.
