### Invariantes, métodos y aplicaciones de los k-d trees

**1. Invariantes fundamentales de un k-d tree**
Un k-d tree es esencialmente un árbol de búsqueda binaria cuyos elementos son puntos en un espacio k-dimensional. Para que funcione correctamente, debe cumplir cuatro invariantes:

1. **Dimensión uniforme**: todos los puntos almacenados tienen exactamente `k` coordenadas.
2. **Coordenada de división por nivel**: cada nivel del árbol está asociado a un índice `j`, entre `0` y `k-1`.
3. **Alternancia de la coordenada**: si un nodo N usa la coordenada `j`, sus hijos utilizarán `(j+1) mod k`.
4. **Orden en subárboles**: para un nodo `N` con índice `j`, todos los puntos `L` en el subárbol izquierdo satisfacen L\[j] < N\[j], mientras que los puntos `R` en el subárbol derecho cumplen R\[j] ≥ N\[j].

Estos invariantes garantizan que, al descender por el árbol, se va "cortando" el espacio en hiperplanos ortogonales según la coordenada correspondiente al nivel, de forma análoga a cómo un BST usa la única clave para particionar.


**2. La necesidad de un árbol balanceado**
Como en un BST clásico, la eficiencia de las operaciones de búsqueda e inserción depende de la altura h del árbol. Si el árbol está equilibrado, es decir, cada partición divide aproximadamente en dos partes iguales, la altura es `O(log n)`. Sin embargo, un k-d tree **no** es autoajustable: el orden de inserción de los puntos determina la forma final, y una secuencia mal elegida puede producir un árbol con altura lineal `O(n)`.

Rebalancear al vuelo, como en los árboles rojo-negro, resulta extremadamente costoso o incluso inviable. Por ello, cuando el conjunto de datos es estático o conocido de antemano, suele optarse por construir el árbol de forma balanceada desde cero. Si en cambio se prevén muchas inserciones y eliminaciones dinámicas, se recomiendan heurísticas que mejoren el balance promedio (p. ej. variando cómo se resuelven empates).


**3. Modelo de datos: clases básicas**
Para implementar un k-d tree necesitamos dos clases: un nodo que almacena un punto y referencias a sus hijos, y la propia estructura del árbol.

> **Listado 1. La clase KdTree**
>
> ```pseudocode
> class KdNode
>   #typetuple(k)
>   point
>   #typeKdNode
>   left
>   #typeKdNode
>   right
>   #typeinteger
>   level
>   function KdNode(point, left, right, level)
>
> class KdTree
>   #typeKdNode
>   root
>   #typeinteger
>   k
>   function KdTree(points=[])
> ```
>
> * **KdNode**: guarda el punto k-dimensional, punteros a los hijos izquierdo y derecho, y el nivel (que determina la coordenada de división).
> * **KdTree**: contiene solo el puntero a la raíz y el valor `k`. Su constructor puede recibir una lista inicial de puntos, pero habitualmente comienza con la raíz en `null`.


**4. Funciones auxiliares para comparar coordenadas**
En lugar de duplicar la lógica de "extraer la coordenada apropiada según el nivel" en cada método, definimos un pequeño conjunto de funciones:

> **Listado 2. Funciones auxiliares**
>
> ```pseudocode
> function getNodeKey(node)
>   return getPointKey(node.point, node.level)
>
> function getPointKey(point, level)
>   j <- level % k
>   return point[j]
>
> function compare(point, node)
>   return sign(getPointKey(point, node.level) - getNodeKey(node))
>
> function splitDistance(point, node)
>   return abs(getPointKey(point, node.level) - getNodeKey(node))
> ```
>
> * `getNodeKey` y `getPointKey` devuelven el componente j-ésimo (`j = level mod k`) de un punto.
> * `compare` retorna -1, 0 o +1 según la comparación entre la coordenada del punto buscado y la del nodo en ese nivel.
> * `splitDistance` calcula la "distancia" al hiperplano de división, útil más adelante en operaciones como búsqueda de vecinos.


**5. Búsqueda en k-d trees**
La operación de búsqueda (`search`) es casi idéntica a la de un BST, salvo que la comparación usa solo una coordenada en cada nivel.

> **Listado 3. El método search**
>
> ```pseudocode
> function search(node, target)
>   if node == null then
>     return null
>   elsif node.point == target then
>     return node
>   elsif compare(target, node) < 0 then
>     return search(node.left, target)
>   else
>     return search(node.right, target)
> ```
>
> 1. Si llegamos a un subárbol vacío (`node == null`), no existe el punto.
> 2. Si encontramos el punto exacto, devolvemos el nodo.
> 3. En caso contrario, usamos `compare` para decidir si girar a la izquierda o a la derecha y continuamos recursivamente.

**Complejidad**: proporcional a la altura `h`. Con un árbol balanceado, `O(log n)`; en el peor caso (árbol degenerado), `O(n)`.

**6. Inserción de un nuevo punto**
Insertar en un k-d tree sigue el mismo patrón de "buscar la posición" que en un BST, creando un nuevo nodo cuando se alcanza un hueco:

> **Listado 4. El método insert**
>
> ```pseudocode
> function insert(node, newPoint, level=0)
>   if node == null then
>     return newKdNode(newPoint, null, null, level)
>   elsif node.point == newPoint then
>     return node
>   elsif compare(newPoint, node) < 0 then
>     node.left  <- insert(node.left,  newPoint, node.level + 1)
>     return node
>   else
>     node.right <- insert(node.right, newPoint, node.level + 1)
>     return node
> ```
>
> * Al recorrer, incrementamos el nivel para alternar la coordenada.
> * Si se detecta un duplicado, simplemente lo ignoramos (pero se pueden adoptar políticas alternativas).
> * Este enfoque no reutiliza `search`, pero permite un código más conciso sin sacrificar claridad.

**Tiempo**: igual que search, `O(h)`.


**7. Estrategias para mejorar el balance promedio**
Dado que no hay rebalanceo automático, un truco sencillo para evitar sesgos por empates en coordenadas consiste en alterar la función `compare`:

> **Listado 5. Compare mejorado para empates**
>
> ```pseudocode
> function compare(point, node)
>   s <- sign(getPointKey(point, node.level) - getNodeKey(node))
>   if s == 0 then
>     return (node.level % 2 == 0) ? -1 : +1
>   else
>     return s
> ```
>
> En lugar de devolver 0 cuando las coordenadas coinciden, resolvemos el empate de forma consistente según la paridad del nivel. Esto rompe patrones degenerados y mejora el balance **en promedio**, aunque no garantiza un peor caso `O(log n)`.


**8. Construcción balanceada a partir de un conjunto estático**
Si conocemos de antemano todos los puntos que tendremos, la forma óptima de obtener un k-d tree balanceado en el peor caso es construirlo "por niveles" eligiendo medianas:

> **Listado 6. ConstructKdTree**
>
> ```pseudocode
> function constructKdTree(points, level=0)
>   if size(points) == 0 then
>     return null
>   elsif size(points) == 1 then
>     return newKdNode(points[0], null, null, level)
>   else
>     (median, leftPts, rightPts) <- partition(points, level)
>     leftTree  <- constructKdTree(leftPts,  level + 1)
>     rightTree <- constructKdTree(rightPts, level + 1)
>     return newKdNode(median, leftTree, rightTree, level)
> ```
>
> * `partition` actúa como el de quicksort, hallando el elemento mediano según la coordenada `level mod k`.
> * Al dividir siempre en dos mitades, garantizamos `altura ≃ log₂(n)`.
> * La construcción completa requiere `O(nlog n)` de tiempo (o `O(n)` si usamos partición in-place) y `O(n)` de memoria para el árbol.


**9. Eliminación de un punto**
Borrar de un k-d tree es más complejo que en un BST clásico, principalmente porque el sucesor para la coordenada `j` puede no hallarse simplemente siguiendo la rama izquierda del subárbol derecho:

1. **Caso hoja**: simplemente eliminar el nodo.
2. **Nodo con un solo hijo**: redirigir al padre para conectar directamente con ese hijo.
3. **Nodo con dos hijos**: buscar el sucesor mínimo para la misma coordenada de división, eliminarlo recursivamente y reemplazar el nodo actual por ese punto.

**10. Búsqueda del mínimo en una coordenada dada**
Para encontrar el nodo con valor mínimo en la coordenada `coordinateIndex`, definimos:

> **Listado 7. El método findMin**
>
> ```pseudocode
> function findMin(node, coordinateIndex)
>   if node == null then
>     return null
>   elsif node.level == coordinateIndex then
>     if node.left == null then
>       return node
>     else
>       return findMin(node.left, coordinateIndex)
>   else
>     leftMin  <- findMin(node.left,  coordinateIndex)
>     rightMin <- findMin(node.right, coordinateIndex)
>     return min(node, leftMin, rightMin)
> ```
>
> * Si `node.level == coordinateIndex`, el mínimo estará en la rama izquierda o en el propio nodo.
> * Si no coincide la coordenada de división, no sabemos en cuál subárbol está, así que exploramos ambos y comparamos con el nodo actual.

Esto eleva el coste de findMin a `O(n^(1−1/k))` amortizado, y domina el coste de la operación de eliminación.

**11. Eliminación completa**
Uniendo todo lo anterior:

> **Listado 8. El método remove**
>
> ```pseudocode
> function remove(node, point)
>   if node == null then
>     return null
>   elsif node.point == point then
>     if node.right != null then
>       minNode <- findMin(node.right, node.level)
>       newRight <- remove(node.right, minNode.point)
>       return newKdNode(minNode.point, node.left, newRight, node.level)
>     elsif node.left != null then
>       minNode <- findMin(node.left, node.level)
>       newRight <- remove(node.left, minNode.point)
>       return newKdNode(minNode.point, null, newRight, node.level)
>     else
>       return null
>   elsif compare(point, node) < 0 then
>     node.left  <- remove(node.left,  point)
>     return node
>   else
>     node.right <- remove(node.right, point)
>     return node
> ```
>
> * Primero buscamos el nodo a eliminar.
> * Si tiene dos hijos, reemplazamos con el mínimo correcto y repararemos su subárbol.
> * Si tiene un solo hijo, lo "esquivamos" enlazando directamente con el hijo único.
> * El coste de remove está dominado por las llamadas a findMin, y puede llegar a `O(n^(1−1/k))` promedio (por ejemplo, `O(√n)` en 2D).


**12. Complejidad global y recomendaciones**

* **Search/Insert**: `O(h)`, con `h = O(log n)` en el árbol balanceado, `O(n)` en el peor caso.
* **Remove**: peor coste amortizado superior debido a findMin.
* **Construcción balanceada**: `O(n log n)` o `O(n)` si se optimiza la partición in-place, altura `O(log n)`.

**Recomendaciones prácticas**:

* Si el conjunto de puntos es estático, usar siempre la construcción balanceada.
* Para datos dinámicos, incorporar heurísticas de desempate (Listado 5) y, si la frecuencia de eliminaciones/inserciones es baja frente al tamaño, reconstruir periódicamente el árbol.
* En aplicaciones de k-NN o rangos, aprovechar `splitDistance` para poda eficiente.

###  **Aplicaciones**

#### **1. Búsqueda del vecino más cercano**

En la versión más sencilla, buscamos el único punto más cercano al objetivo, aunque en el conjunto de datos ese objetivo quizás no exista como punto guardado. El procedimiento básico consiste en:

1. Recorrer el k-d tree desde la raíz hacia la hoja que contendría al objetivo, usando la misma lógica de comparación por coordenada que en insert y search.
2. Al descender, mantener un registro del vecino más cercano encontrado hasta el momento (su punto y su distancia).
3. Una vez alcanzada una hoja, retroceder ("backtracking"), comprobando en cada nodo si la rama opuesta a la explorada podría contener puntos más cercanos que el actual NN. Esto se decide comparando la distancia mínima al hiperplano de división con la mejor distancia encontrada.

El pseudocódigo que implementa esta lógica es el siguiente:

```pseudocode
function nearestNeighbor(node, target, (nnDist, nn) = (inf, null))
  if node == null then
    return (nnDist, nn)
  else
    dist <- distance(node.point, target)
    if dist < nnDist then
      (nnDist, nn) <- (dist, node.point)
    if compare(target, node) < 0 then
      closeBranch <- node.left
      farBranch   <- node.right
    else
      closeBranch <- node.right
      farBranch   <- node.left
    (nnDist, nn) <- nearestNeighbor(closeBranch, target, (nnDist, nn))
    if splitDistance(target, node) < nnDist then
      (nnDist, nn) <- nearestNeighbor(farBranch, target, (nnDist, nn))
    return (nnDist, nn)
```

**Explicación paso a paso:**

* **Condición base**: si el nodo es nulo, regresamos el par `(nnDist, nn)` tal como está, pues no hay nada nuevo que explorar.
* **Cálculo de distancia**: se mide la distancia euclidiana (o la métrica que corresponda) entre el punto del nodo y el objetivo.
* **Actualización del mejor vecino**: si esa distancia es menor que `nnDist`, actualizamos `nnDist` y `nn` para reflejar el nuevo vecino más cercano.
* **Elección de rama más cercana**: con `compare(target, node)` decidimos si el objetivo cae en el subárbol izquierdo o derecho (según la coordenada de división en el nivel actual). Llamamos a ese subárbol `closeBranch` y al otro `farBranch`.
* **Recursión en rama cercana**: exploramos primero `closeBranch`, pasando los valores actuales de `(nnDist, nn)` para que puedan mejorar.
* **Poda de la rama opuesta**: si la distancia del objetivo al hiperplano (`splitDistance`) es menor que `nnDist`, entonces **podría** haber un punto en la `farBranch` más cercano que el actual vecino. En ese caso, recursamos también en `farBranch`.
* **Retorno**: devolvemos finalmente el par `(nnDist, nn)` tras haber probado ambas ramas pertinentes.

Este método combina una búsqueda en profundidad con poda geométrica, evitando explorar regiones demasiado lejanas.

#### Importancia del orden de exploración

Recorrer primero la rama "cercana" mejora la poda, porque reduce `nnDist` cuanto antes. Un valor más bajo de `nnDist` implica que la condición de poda `splitDistance < nnDist` fallará más a menudo, evitando llamar innecesariamente a la rama lejana. Aunque la ordenación perfecta de exploración no es evidente, usar la comparación simple sobre la coordenada de división suele ser un buen compromiso entre simplicidad y eficiencia.

#### **2. Búsqueda de los n vecinos más cercanos**

Para casos en que nos interesan los `n` vecinos más próximos, el algoritmo extiende la lógica anterior usando una cola de prioridad de tamaño acotado (max‐heap). En ella, el elemento de mayor distancia entre los `n` encontrados se mantiene siempre en la cima, de modo que la condición de poda compara contra ese valor límite. El pseudocódigo principal es:

```pseudocode
function nNearestNeighbor(node, target, n)
  pq <- new BoundedPriorityQueue(n)
  pq.insert((inf, null))
  pq <- nNearestNeighbor(node, target, pq)
  (nnnDist, _) <- pq.peek()
  if nnnDist == inf then
    pq.top()
  return pq

function nNearestNeighbor(node, target, pq)
  if node == null then
    return pq
  else
    dist <- distance(node.point, target)
    pq.insert((dist, node.point))
    if compare(target, node) < 0 then
      closeBranch <- node.left
      farBranch   <- node.right
    else
      closeBranch <- node.right
      farBranch   <- node.left
    pq <- nNearestNeighbor(closeBranch, target, pq)
    (nnnDist, _) <- pq.peek()
    if splitDistance(target, node) < nnnDist then
      pq <- nNearestNeighbor(farBranch, target, pq)
    return pq
```

**Inicialización de la cola acotada**

* Se crea `pq` con capacidad `n`.
* Se inserta un guardián `(inf, null)` para asegurar que, hasta tener al menos `n` elementos reales, la cima sea infinita y no provoque poda prematura.

**Recursión y poda**

* En cada nodo, calculamos `dist` y tratamos de insertar `(dist, node.point)` en `pq`. Su política interna retiene solo las n tuplas de menor distancia.
* Igual que en `nearestNeighbor`, definimos `closeBranch` y `farBranch` según la comparación.
* Exploramos primero `closeBranch`, luego, tras conocer la nueva distancia al n-ésimo vecino (`pq.peek()`), decidimos si `splitDistance < nnnDist` para visitar `farBranch`.
* Al terminar, `pq` contiene los `n` puntos más cercanos, ordenados por distancia.

Este enfoque adapta la poda geométrica al caso múltiple, asegurando que solo ramas capaces de mejorar el umbral actual sean recorridas.

#### **3. Complejidad de la búsqueda de vecinos**

En el peor caso, incluso en un k-d tree balanceado, podría requerirse recorrer todo el árbol. Sin embargo, de manera promedio y en árboles balanceados, la complejidad de la búsqueda de un vecino más cercano es `O(2ᵏ + log(n))`. La intuición geométrica en 2D, por ejemplo, es que tras llegar a la hoja adecuada (coste `O(log n)`), solo necesitamos considerar las regiones adyacentes dentro de la distancia mínima encontrada. Con particiones regulares, son aproximadamente 4 en dos dimensiones o 8 en tres, etc., lo que genera el término `2ᵏ`. Para `k` fijos y `n` grandes, esto suele ser muy favorable respecto a `O(n)`.


#### **4. Búsquedas por región**

Además de vecinos, los k-d trees permiten consultar qué puntos caen dentro de una región arbitraria, aprovechando el mismo mecanismo de poda:

**Puntos dentro de una hiperesfera**

Para recuperar todos los puntos a distancia *≤ R* de un centro dado, se modifica `nearestNeighbor` dejando de actualizar un único vecino y recolectando todos los que cumplen la condición:

```pseudocode
function pointsInSphere(node, center, radius)
  if node == null then
    return []
  else
    points <- []
    dist   <- distance(node.point, center)
    if dist < radius then
      points.insert(node.point)
    if compare(center, node) < 0 then
      closeBranch <- node.left
      farBranch   <- node.right
    else
      closeBranch <- node.right
      farBranch   <- node.left
    points.insertAll(pointsInSphere(closeBranch, center, radius))
    if splitDistance(center, node) < radius then
      points.insertAll(pointsInSphere(farBranch, center, radius))
    return points
```

* Se inspecciona el nodo actual y si está dentro de la esfera, se añade al resultado.
* Se determina la rama "cercana" y se explora sin condiciones adicionales.
* Si la esfera cruza el hiperplano, la rama lejana se explora también; de lo contrario, se poda.

**Puntos dentro de un hiperrectángulo**

Cuando la región es un rectángulo alineado con los ejes, la decisión de poda se simplifica comparando coordenadas con los límites:

```pseudocode
function pointsInRectangle(node, rectangle)
  if node == null then
    return []
  else
    points <- []
    if (rectangle[i].min ≤ node.point[i] ≤ rectangle[i].max
         0 ≤ i < k) then
      points.insert(node.point)
    if intersectLeft(rectangle, node) then
      points.insertAll(pointsInRectangle(node.left,  rectangle))
    if intersectRight(rectangle, node) then
      points.insertAll(pointsInRectangle(node.right, rectangle))
    return points
```

* **Comprobación de inclusión**: si el punto del nodo está dentro de todos los rangos de cada dimensión, lo recogemos.
* **Intersección con subárboles**: con funciones auxiliares `intersectLeft` e `intersectRight` (que comparan el rango con la coordenada de división), decidimos si explorar cada subárbol.


#### **5. Rendimiento de consultas por región**

* **Pequeñas regiones**: si la región toca únicamente una hoja, podemos podar la mayoría de ramas y bajar por un único camino (`O(log n)`).
* **Regiones grandes**: si cubren prácticamente todo el espacio, recorremos casi todos los nodos (`O(n)`).
* En general, el coste varía entre `O(log n)` y `O(n)`, según el tamaño y forma de la región y la capacidad de poda.


Los k-d trees transforman búsquedas lineales en operaciones mucho más eficientes mediante particiones recursivas del espacio. La búsqueda de vecino más cercano incorpora un backtracking inteligente y poda basada en la distancia al hiperplano. La extensión a `n` vecinos utiliza colas de prioridad acotadas para mantener el umbral de poda. 

Finalmente, las consultas por región (esféricas o rectangulares) reutilizan la misma idea de poda geométrica para incluir solo los nodos relevantes. Aunque en el peor caso algunos costosos recorridos completos pueden ser necesarios, en la práctica y para dimensiones moderadas (k ≤ 10) y árboles balanceados, estas operaciones son muy superiores a la fuerza bruta, ofreciendo tiempos cercanos a `O(log n)` o amortizados `O(2ᵏ + log n)`.
