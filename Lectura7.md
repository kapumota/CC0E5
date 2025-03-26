### Uso de heaps en algoritmos avanzados

Los heaps son estructuras de datos fundamentales en informática que permiten gestionar colas de prioridad de forma eficiente. 
Su aplicación abarca desde la selección de los `k` elementos más grandes de un conjunto, hasta problemas en grafos como los algoritmos de Dijkstra 
y Prim, y la compresión de datos mediante códigos de Huffman. 

#### 1. Caso de uso: encontrar los `k` elementos más grandes

Cuando se dispone de un conjunto de `n` elementos, existen diversas estrategias para extraer los `k` elementos más grandes.  
Algunas soluciones ingenuas son:

- **Ordenar la entrada completa:**  
  Se puede ordenar el arreglo y tomar los últimos `k` elementos. Esta solución requiere O(nlog(n)) comparaciones y, dependiendo del algoritmo
  de ordenación, puede necesitar memoria adicional.

- **Selección repetida:**  
  Se puede buscar el elemento mayor, moverlo al final del arreglo, luego buscar el siguiente mayor entre los `n-1` elementos restantes, y repetir este proceso `k` veces.
  Esta estrategia se asemeja al ciclo interno del algoritmo de ordenamiento de selección, requiriendo O(k) intercambios y O(nk) comparaciones.

Sin embargo, ambas aproximaciones se vuelven ineficientes cuando `n` es mucho mayor que `k`, situación frecuente en escenarios donde `n` puede ser del orden de millones o miles de millones y `k` apenas unos pocos cientos o miles.

##### 1.1 Estrategia con heap pequeño (min-heap de tamaño `k`)

La solución óptima consiste en mantener un heap auxiliar de tamaño `k`. En lugar de construir un heap con los `n` elementos (lo que requeriría O(n) espacio y O(n + klog(n)) tiempo al extraer `k` elementos), se utiliza un **min-heap** limitado a `k` elementos. 
El procedimiento es el siguiente:

1. Se recorre la lista de entrada y, mientras el heap tenga menos de `k` elementos, se insertan directamente los nuevos elementos.
2. Una vez que el heap contiene `k` elementos, se compara cada nuevo elemento con la cima del heap.
3. Dado que en un min-heap la cima es el elemento más pequeño de los `k` elementos almacenados, si el nuevo elemento es mayor que dicho valor,
4. significa que este nuevo elemento es candidato a formar parte de los `k` elementos más grandes.
5. En ese caso, se extrae la cima del heap (el elemento más pequeño) y se inserta el nuevo elemento, manteniendo así el tamaño del heap en `k`.

Con este enfoque, cada iteración de actualización del heap se realiza en tiempo O(log k), y el recorrido de la lista completa tiene un 
coste de O(n). En total, el algoritmo utiliza O(n + klog(k)) comparaciones y O(k) espacio extra, lo que es muy eficiente cuando `k` es 
mucho menor que `n`.

##### 1.2 Pseudocódigo para seleccionar los `k` elementos más grandes

A continuación se presenta el pseudocódigo que ilustra esta estrategia:

```
function topK(A, k)
  heap ← DWayHeap()
  for el in A do
    if (heap.size == k and heap.peek() < el) then
      heap.top()
    if (heap.size < k) then
      heap.insert(el)
  return heap
```

**Explicación detallada de cada paso:**

- **Paso 1:** Se crea un heap vacío. En este caso se utiliza un heap d-ario (DWayHeap), aunque para este problema en particular se puede usar un min-heap.
- **Paso 2:** Se itera sobre cada elemento del arreglo A.
- **Paso 3:** Si el heap ya tiene `k` elementos, se compara el nuevo elemento con la cima del heap (el elemento mínimo entre los `k` almacenados).
- **Paso 4:** Si el nuevo elemento es mayor, se extrae la cima del heap. Esta operación elimina el elemento que ya no forma parte de los `k` más grandes.
- **Paso 5:** Si el tamaño del heap es menor que `k`, el elemento actual se inserta en el heap.
- **Paso: 6** Al finalizar la iteración, el heap contiene los `k` elementos más grandes, que se devuelven como resultado.

Este enfoque es especialmente útil en aplicaciones en las que se deben procesar grandes flujos de datos y se requiere mantener en memoria solo un subconjunto reducido de los elementos más relevantes.


#### 2. Heaps en aplicaciones de grafos

Los heaps son herramientas esenciales en muchos algoritmos de grafos, ya que permiten procesar y actualizar información de forma eficiente.

##### 2.1 Algoritmo de Dijkstra y A*

Para problemas de caminos mínimos en grafos, como el algoritmo de Dijkstra y el algoritmo A*, se utilizan colas de prioridad para seleccionar el vértice con la distancia mínima en cada iteración. La eficiencia de estos algoritmos depende en gran medida de la implementación de la cola de prioridad. Tradicionalmente, un heap binario se utiliza para gestionar los vértices, permitiendo actualizaciones en O(log(n)) y extracciones en el mismo orden.

La ventaja de usar un heap es que, en cada iteración, se puede obtener el vértice con la menor distancia de manera eficiente, lo que reduce el tiempo total de ejecución. En implementaciones modernas, la sustitución de un heap binario por uno d-ario o incluso por un Fibonacci heap puede mejorar aún más la velocidad, especialmente en grafos densos.

##### 2.2 Algoritmo de Prim para árboles de expansión mínima

El algoritmo de Prim se utiliza para encontrar el árbol de expansión mínima (MST) de un grafo no dirigido y conectado. La idea es construir un MST a partir de un vértice fuente y, en cada paso, añadir el vértice más cercano al conjunto de vértices ya incluidos en el árbol.

Al igual que en el algoritmo de Dijkstra, una cola de prioridad (heap) se utiliza para seleccionar el siguiente vértice con la arista de menor peso. La complejidad del algoritmo varía según la implementación de la cola de prioridad:
- Con arreglos (ordenados o no), el tiempo de ejecución es O(V²).
- Con heaps binarios o d-arios, se obtiene un tiempo de O(Vlog(V) + Elog(V)).
- Con Fibonacci heaps, se puede alcanzar una complejidad de O(Vlog(V) + E).

La elección del tipo de heap influye directamente en el rendimiento del algoritmo de Prim y, por ende, en la eficiencia en la construcción del MST para grafos grandes.

#### 3. Uso de heaps en la compresión de datos: códigos de Huffman

El algoritmo de Huffman es uno de los métodos de compresión de datos más conocidos. Su objetivo es generar códigos binarios de longitud variable para representar los caracteres de un texto, asignando códigos más cortos a los caracteres más frecuentes. 
Este algoritmo es greedy y se construye de abajo hacia arriba, utilizando una cola de prioridad (min-heap) para seleccionar los dos nodos con la menor frecuencia en cada iteración.

#### 3.1 Proceso del algoritmo de Huffman

El algoritmo se puede dividir en varias etapas:

1. **Cálculo de frecuencias:**  
   Se analiza el texto de entrada para construir un mapa de frecuencias, que asocia a cada carácter la cantidad de veces que aparece en el texto.

2. **Creación de nodos iniciales:**  
   Para cada carácter, se crea un nodo (TreeNode) que contiene el carácter y su frecuencia. Estos nodos se insertan en una cola de prioridad, donde la prioridad se determina por la frecuencia (los nodos con frecuencia menor tienen mayor prioridad en un min-heap).

3. **Construcción del árbol de Huffman:**  
   Mientras la cola de prioridad tenga más de un elemento, se realizan los siguientes pasos:
   - Se extraen de la cola los dos nodos con menor frecuencia (denominados *left* y *right*).
   - Se crea un nuevo nodo *parent* que combina los caracteres de *left* y *right* y cuya frecuencia es la suma de las frecuencias de ambos.
   - Se asigna *left* y *right* como hijos del nuevo nodo.
   - Se inserta el nodo *parent* de vuelta en la cola de prioridad.

4. **Generación de la tabla de compresión:**  
   Una vez que solo queda un nodo en la cola de prioridad (la raíz del árbol de Huffman), se recorre el árbol para construir la tabla de compresión. Esta tabla asigna a cada carácter la secuencia de bits correspondiente, determinada por el camino desde la raíz hasta la hoja (donde se agrega un 0 al tomar la rama izquierda y un 1 al tomar la rama derecha).

##### 3.2 Pseudocódigo del algoritmo de Huffman

El siguiente pseudocódigo describe el proceso completo para construir el árbol de Huffman y generar la tabla de compresión:

```
function huffman(text)
  charFrequenciesMap ← ComputeFrequencies(text)
  priorityQueue ← MinHeap()
  for (char, frequency) in charFrequenciesMap do
    priorityQueue.insert(TreeNode([char], frequency))
  while priorityQueue.size > 1 do
    left ← priorityQueue.top()
    right ← priorityQueue.top()
    parent ← TreeNode(left.chars + right.chars,
                       left.frequency + right.frequency)
    parent.left ← left
    parent.right ← right
    priorityQueue.insert(parent)
  return buildTable(priorityQueue.top(), [], Map())
```

**Explicación de las etapas:**

- Se inicia calculando las frecuencias de cada carácter en el texto mediante la función *ComputeFrequencies(text)*.
- Se crea una cola de prioridad (min-heap) y se insertan en ella todos los nodos correspondientes a los caracteres, cada uno con su respectiva frecuencia.
- Mientras queden más de un nodo en la cola, se extraen los dos nodos con la frecuencia más baja. Estos se combinan en un nuevo nodo cuya frecuencia es la suma de las dos, y cuyos hijos son los nodos extraídos.
- El nuevo nodo se inserta nuevamente en la cola y el proceso se repite hasta que solo quede un nodo, que representará la raíz del árbol de Huffman.
- Finalmente, se invoca la función *buildTable* para recorrer el árbol y generar la tabla de compresión.

##### 3.3 Generación de la tabla de compresión

El método *buildTable* se encarga de recorrer recursivamente el árbol de Huffman para construir un mapa que asocia cada carácter con su secuencia de bits. El pseudocódigo es el siguiente:

```
function buildTable(node, sequence, charactersToSequenceMap)
  if node.characters.size == 1 then
    charactersToSequenceMap[node.characters[0]] ← sequence 
  else
    if node.left <> null then
      buildTable(node.left, 0 + sequence, charactersToSequenceMap) 
    if node.right <> null then
      buildTable(node.right, 1 + sequence, charactersToSequenceMap) 
  return charactersToSequenceMap
```

**Detalle del proceso:**

- Se verifica si el nodo actual es una hoja (es decir, contiene un único carácter). Si es así, se asigna la secuencia acumulada a ese carácter.
- Si el nodo tiene hijos, se realizan llamadas recursivas:
  - Al recorrer el hijo izquierdo se añade un 0 al principio de la secuencia.
  - Al recorrer el hijo derecho se añade un 1.
- El proceso continúa hasta que se asigna una secuencia a cada carácter.

##### 3.4 Representación de la tabla de compresión

Como ejemplo, se puede considerar la siguiente tabla de compresión derivada de un árbol de Huffman:

| Carácter | Secuencia de bits | Frecuencia |
|----------|-------------------|------------|
| A        | 0                 | 0.6        |
| B        | 10                | 0.2        |
| C        | 1100              | 0.07       |
| D        | 1101              | 0.06       |
| E        | 1110              | 0.05       |
| F        | 1111              | 0.02       |

En esta tabla, cada secuencia de bits cumple la propiedad de código prefijo, lo que significa que ninguna secuencia es el prefijo de otra. Esta propiedad es esencial para la decodificación del mensaje comprimido, ya que permite determinar de manera única la separación de los códigos en la secuencia binaria.

#### 4. Implementación en Python

Para ilustrar la transición del pseudocódigo a una implementación real, se presenta a continuación un ejemplo simplificado en Python que muestra cómo se podrían implementar algunas de las funciones clave, en particular las operaciones utilizadas en el algoritmo de Huffman y en la selección de los `k` elementos más grandes.

##### 4.1 Ejemplo de código para el algoritmo de Huffman

```python
class TreeNode:
    def __init__(self, chars, frequency):
        self.chars = chars          # Lista o cadena de caracteres
        self.frequency = frequency  # Frecuencia combinada de los caracteres
        self.left = None            # Hijo izquierdo
        self.right = None           # Hijo derecho

def compute_frequencies(text):
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    total = sum(freq.values())
    # Normalizar las frecuencias
    for char in freq:
        freq[char] /= total
    return freq

import heapq

def huffman(text):
    char_freq = compute_frequencies(text)
    # Crear la cola de prioridad como un min-heap
    heap = []
    for char, frequency in char_freq.items():
        node = TreeNode(char, frequency)
        heapq.heappush(heap, (frequency, node))
    
    # Combinar nodos hasta que solo quede uno en el heap
    while len(heap) > 1:
        left_freq, left_node = heapq.heappop(heap)
        right_freq, right_node = heapq.heappop(heap)
        parent = TreeNode(left_node.chars + right_node.chars, left_freq + right_freq)
        parent.left = left_node
        parent.right = right_node
        heapq.heappush(heap, (parent.frequency, parent))
    
    # La raíz del árbol es el único nodo restante
    _, root = heap[0]
    return build_table(root, "")

def build_table(node, sequence):
    table = {}
    def traverse(n, seq):
        if len(n.chars) == 1:
            table[n.chars] = seq
        else:
            if n.left is not None:
                traverse(n.left, seq + "0")
            if n.right is not None:
                traverse(n.right, seq + "1")
    traverse(node, sequence)
    return table

# Ejemplo de uso
texto = "AAABBCDEFAAA"
compression_table = huffman(texto)
print("Tabla de compresión:", compression_table)
```

**Aspectos del código:**

- La función *compute_frequencies* calcula la frecuencia de cada carácter y normaliza los valores.
- Se utiliza la librería *heapq* de Python para implementar la cola de prioridad como un min-heap. Cada elemento del heap es una tupla formada por la frecuencia y el nodo correspondiente.
- El bucle principal del algoritmo extrae los dos nodos con la frecuencia menor, crea un nuevo nodo combinando ambos y lo vuelve a insertar en el heap.
- La función *build_table* recorre el árbol de Huffman para construir la tabla de compresión, asignando a cada carácter la secuencia de bits obtenida desde la raíz.

##### 4.2 Ejemplo de código para la celección de los `k` elementos más grandes

La siguiente implementación muestra cómo utilizar un min-heap para mantener los `k` elementos más grandes de un conjunto:

```python
def topK(A, k):
    # Usamos heapq para implementar un min-heap
    heap = []
    for el in A:
        # Si el heap tiene k elementos, comparar el elemento actual con el mínimo
        if len(heap) == k and heap[0] < el:
            heapq.heappop(heap)
        if len(heap) < k:
            heapq.heappush(heap, el)
    return heap

# Ejemplo de uso
A = [2, 4, 1, 3, 7, 6]
k = 3
k_largest = topK(A, k)
print("Los k elementos más grandes son:", k_largest)
```

**Aspectos destacados:**

- Se recorre la lista de elementos A.
- Si el heap ya contiene `k` elementos, se verifica si el nuevo elemento es mayor que la raíz del min-heap.
- En caso afirmativo, se extrae la raíz y se inserta el nuevo elemento, manteniendo el tamaño del heap en `k`.
- Al final, el heap contendrá los `k` elementos más grandes.


#### 5. Otras aplicaciones de heaps en diversos contextos

Los heaps son estructuras de datos versátiles que se utilizan en una amplia variedad de aplicaciones. Además de la selección de los `k` elementos más grandes y la compresión de datos, destacan los siguientes casos de uso:

##### 5.1 Aplicaciones en grafos

- **Dijkstra y A\*:**  
  Los algoritmos para encontrar el camino más corto en grafos (como Dijkstra y A\*) dependen de una cola de prioridad para seleccionar el vértice con la distancia mínima en cada paso. La eficiencia del algoritmo mejora significativamente cuando se utiliza un heap para gestionar los vértices pendientes de procesar.

- **Algoritmo de Prim:**  
  Para encontrar el árbol de expansión mínima (MST) en un grafo no dirigido, el algoritmo de Prim utiliza una cola de prioridad para determinar cuál es la arista de menor peso que conecta el conjunto de vértices ya incluidos en el MST con el resto del grafo. La implementación con heaps permite reducir la complejidad de la operación de selección y actualización de vértices.

##### 5.2 Compresión de datos con códigos de Huffman

Como se ha descrito anteriormente, la construcción de códigos de Huffman es otro caso de uso emblemático de los heaps. La capacidad para extraer rápidamente los dos elementos con la menor frecuencia permite construir el árbol de codificación de forma eficiente. La técnica de fusión de nodos basada en una cola de prioridad es la clave para lograr una compresión efectiva y para garantizar que el código resultante sea un código prefijo.

##### 5.3 Procesamiento en flujos de datos

En situaciones donde los datos se reciben de forma continua (por ejemplo, flujos de datos en tiempo real), el uso de un min-heap limitado a 
`k` elementos permite mantener siempre los `k` elementos más grandes vistos hasta el momento sin necesidad de almacenar todo el conjunto de datos. Esta característica resulta especialmente útil en aplicaciones de monitoreo y análisis en tiempo real, donde el volumen total de datos puede ser muy elevado, pero solo es necesario conservar un subconjunto representativo.

#### 6. Aspectos generales en la aplicación de heaps

La elección de la estructura de datos adecuada es crucial en el diseño de algoritmos eficientes. En el caso de los heaps, es importante tener en cuenta varios factores:

- **Selección de la estrategia apropiada:**  
  Cuando se necesita encontrar un subconjunto de elementos (por ejemplo, los `k` elementos más grandes), es esencial utilizar un heap de tamaño limitado en lugar de procesar un heap con todos los elementos disponibles. Esto reduce tanto el uso de memoria como el tiempo de procesamiento.

- **Optimización de operaciones:**  
  Las operaciones básicas en un heap, como *insert*, *top* (extracción de la raíz) y *update*, deben estar optimizadas para mantener la complejidad logarítmica. La implementación de funciones auxiliares, como *bubbleUp* y *pushDown*, es fundamental para asegurar que la propiedad de prioridad se mantenga en todo momento.

- **Adaptabilidad a diferentes algoritmos:**  
  La modularidad en la implementación de heaps permite adaptar fácilmente la estructura para diversos algoritmos. Por ejemplo, cambiar un max-heap por un min-heap es tan simple como invertir el criterio de comparación. Esta flexibilidad es vital para aplicaciones en grafos, compresión de datos y procesamiento de flujos.

- **Implementación en diferentes lenguajes:**  
  La transición del pseudocódigo a un lenguaje de programación concreto implica considerar detalles como el manejo de arreglos (estáticos o dinámicos), el uso de estructuras auxiliares (como diccionarios o mapas hash) y la eficiencia en el cálculo de índices. Cada lenguaje tiene sus propias ventajas y limitaciones, y la elección de uno u otro puede influir significativamente en el rendimiento global de la solución.

- **Uso en algoritmos de compresión:**  
  En la compresión de datos, la capacidad de generar un código prefijo es esencial para la decodificación. Los heaps permiten construir de forma eficiente el árbol de Huffman, asegurando que la tabla de compresión resultante asigne a cada carácter una secuencia de bits que no sea el prefijo de otra, lo cual es clave para la integridad del proceso de compresión.

