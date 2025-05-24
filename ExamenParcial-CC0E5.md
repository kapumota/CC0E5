### Examen parcial de algoritmos y estructura de datos avanzados

**Instrucciones:**  
Este examen consta de 3 preguntas. Para cada pregunta, se espera que proporciones:

- **Implementaciones de código** robustas y eficientes (se prefiere código funcional en Python o el lenguaje que domines; el pseudocódigo detallado solo se aceptará si es excepcionalmente claro y el tiempo es un factor crítico extremo).  
- **Justificaciones detalladas** de tus elecciones de diseño algorítmico y estructuras de datos.  
- **Pruebas de corrección** convincentes (argumentos lógicos formales, invariantes, o casos de prueba exhaustivos que cubran escenarios típicos y límites).  
- **Análisis de rendimiento** riguroso (complejidad temporal y espacial, en el peor caso y caso esperado cuando aplique).

> **Importante:**  
> Este examen ha sido diseñado para evaluar una comprensión profunda y la capacidad de extender conceptos fundamentales. Se espera que los estudiantes aborden los problemas con un enfoque analítico y demuestren un razonamiento computacional. Debes completar los ejercicios en su totalidad para que se considere la puntuación completa del ejercicio. Las respuestas incompletas o superficiales recibirán una puntuación de a lo más 1 en cualquiera de las 3 preguntas del examen.

Utiliza el repositorio del curso si lo consideras necesario.

**Entrega:**  
Presenta un archivo comprimido con tus nombres y apellidos y código (ej.: `Apellidos_Nombres_ExamenParcial.zip`). Dentro, incluye tres carpetas llamadas `Pregunta1`, `Pregunta2` y `Pregunta3` con tus respuestas (código, análisis escrito, etc.).


### Pregunta 1: Treap aumentado para consultas complejas

Un Treap combina las propiedades de un árbol de búsqueda binaria (BST) para las claves y un heap para las prioridades asignadas aleatoriamente. Se busca extender su funcionalidad para soportar consultas más complejas de manera eficiente.

#### (a) Implementación de Treap con inserción, eliminación y análisis de profundidad (4 puntos)

**Código:**

- Implementa una clase `TreapNode` y las funciones  
  ```python
  insert(root, key, value, priority)
  delete(root, key)
  ```

para un Treap.

* La prioridad se proporcionará en la inserción; para la eliminación, asume que la clave es única.
* La inserción y eliminación deben mantener las propiedades de BST por `key` y de max-heap (o min-heap, especifica tu elección) por `priority`.
* Deberás implementar las rotaciones

  ```python
  rotate_left(node)
  rotate_right(node)
  ```

  y usarlas adecuadamente.

**Análisis y propiedades:**

* Explica por qué las prioridades aleatorias (o uniformemente distribuidas) llevan a que el Treap tenga una altura esperada de O(log N).
* Proporciona el análisis asintótico esperado y en el peor caso para las operaciones de inserción y eliminación. Justifica cualquier diferencia entre ambos casos.


#### (b) Consulta de rango con agregación optimizada 

**Diseño y código:**

* Modifica la estructura del nodo `TreapNode` (y consecuentemente las operaciones de `insert`, `delete` y rotaciones) para que cada nodo almacene, además de sus datos habituales, el valor máximo (`max_value_in_subtree`) contenido en el subárbol que representa (considerando el atributo `value` de los nodos).
* Implementa la función

  ```python
  find_max_value_in_range(root, key_min, key_max)
  ```

  que utilice esta información aumentada para encontrar eficientemente el valor máximo en el rango `[key_min, key_max]`. No se debe recolectar todos los nodos y luego buscar el máximo; debe aprovechar la información aumentada.

**Análisis y pruebas:**

* Analiza la complejidad temporal de tu función `find_max_value_in_range` y compárala con un enfoque ingenuo.
* Detalla cómo se mantiene `max_value_in_subtree` correctamente durante rotaciones, inserciones y eliminaciones.
* Describe casos de prueba clave para verificar la corrección de:

  - Inserción y eliminación (propiedades BST y heap).
  - `find_max_value_in_range` (correcta manutención de `max_value_in_subtree`).


### Pregunta 2: Búsqueda de substrings k-frecuentes usando un árbol de sufijos

Dado un string `S` y un entero `k`, encontrar el substring más largo que aparece al menos k veces es un problema con aplicaciones significativas. Se utilizará un árbol de sufijos (suffix tree), que es una versión compactada de un suffix trie.

#### (a) Encontrar el substring k-frecuente más largo y sus ocurrencias

**Algoritmo y código:**

* Usando el árbol de sufijos construido (con conteo de sufijos en nodos internos), describe e implementa

  ```python
  find_longest_k_frequent_substring(suffix_tree_root, text_length, k)
  ```

  que devuelva:

  * El substring más largo que se repite al menos k veces.
  * Una lista de todas las posiciones de inicio de este substring.
* Si hay varios de la misma longitud, puedes devolver cualquiera.

> **Pista:** Un substring que se repite al menos k veces corresponde a un camino desde la raíz hasta un nodo interno cuyo subárbol tiene ≥ k hojas. La “profundidad de string” de ese nodo es la longitud del substring.

#### (b) Corrección y complejidad de búsqueda

* Argumenta formalmente por qué tu algoritmo encuentra correctamente el substring más largo y todas sus posiciones.
* ¿Cuál es la complejidad de tu algoritmo sobre el árbol ya construido? Explica tu respuesta.


### Pregunta 3: Diseño de un motor híbrido de planificación y análisis de flujos

Estás encargado de diseñar el núcleo de un sistema híbrido que combine un programador de tareas de un SO con un módulo de análisis de eventos en tiempo real sobre grandes volúmenes de datos. Debes implementar:

1. Una **cola de prioridades** con inserciones, extracciones y actualizaciones de prioridad en tiempo sublogarítmico.
2. Un **Count-Min Sketch** que estime frecuencias con error controlado y uso mínimo de memoria.
3. Una estructura **Union-Find** para conectividad dinámica mediante transacciones sucesivas.

### (a) Cola de prioridades con actualización dinámica

* Diseña la clase `DHeap` parametrizada por grado d, con métodos:

  ```python
  __init__(d)
  insert(task_id, priority)
  extract_max()
  _sift_up(idx)
  _sift_down(idx)
  ```
* Diseña la clase `SkipListIndex` con métodos:

  ```python
  insert(key, idx)
  search(key)
  delete(key)
  ```
* Explica cómo cooperan para implementar `update_priority(task_id, new_priority)`:

  - Búsqueda en Skip List.
  - Modificación de prioridad en el heap.
  - Llamada a `_sift_up` o `_sift_down`.
* Deriva las recurrencias de altura y de sift en un d-heap de N elementos y grado d. Calcula la complejidad de `insert`, `extract_max` y `update_priority`. Justifica cuándo conviene elegir d>2.
* Describe un plan de pruebas unitarias e integradas y cómo usar herramientas de profiling (latencia media, p95, contadores de comparaciones) para detectar cuellos de botella.

#### (b) Estimación de frecuencias con Count-Min Sketch

* Define la clase `CountMinSketch(width, depth)` con métodos:

  ```python
  update(item, count=1)
  estimate(item)
  ```
* Indica cómo generar las d funciones hash (por ejemplo, `hash(item, seed)%width`).
* Explica el algoritmo interno de actualización y consulta (recorrido por filas y uso de mínimos).
* Relaciona `width` y `depth` con error aditivo ε y probabilidad de fallo δ. Explica por qué sobreestima y nunca subestima.
* Propon un conjunto de experimentos (distribuciones Zipf, uniformes y picos) para medir error medio y p95, variando `width` y `depth`.

#### (c) Gestión de conectividad dinámica con Union-Find

* Diseña `UnionFind(n)` con métodos `find(i)` y `union(i,j)`, usando heurísticas de unión por rango y compresión de caminos.
* Esboza el pseudocódigo de `find` (con compresión) y de `union` (por tamaño).
* Describe cómo procesarías un flujo de transacciones que une pares de elementos y responder consultas `connected(x,y)`.
* Calcula la complejidad amortizada de `find` y `union` con heurísticas y compárala con la versión ingenua.

#### (d) Orquestación e integración global

* Propón una arquitectura modular donde `process_event(event)` decida si un evento va al heap, CMS o Union-Find.
* Explica cómo coordinar la sincronización de índices y coherencia de datos.
* Señala posibles cuellos de botella en concurrencia y volumen, y describe estrategias de escalabilidad: sharding, paralelización y balanceo de carga.

