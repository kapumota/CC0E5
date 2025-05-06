### Implementación de la API de Treaps: búsqueda, inserción, eliminación y otras operaciones


#### 1. Implementación de la búsqueda

La búsqueda en un treap se realiza de manera similar a la búsqueda en un árbol binario de búsqueda (BST). La clave se busca recorriendo el árbol desde la raíz, eligiendo la rama izquierda o derecha según la comparación de la clave objetivo con la del nodo actual. Se recorre una única rama del subárbol, lo que simplifica el proceso.

#### Pseudocódigo: método `search`

```
function search(node, targetKey) 
    if node == null then 
        return null 
    if node.key == targetKey then  
        return node 
    else if targetKey < node.key then  
        return search(node.left, targetKey)  
    else 
        return search(node.right, targetKey)  
```

#### Explicación:

- **Entrada:** El método `search` recibe un nodo (de un treap) y la clave a buscar. Retorna el nodo que contiene la clave, o `null` si no se encuentra.
- **Caso base:** Si el nodo es `null`, se indica que la clave no se encontró.
- **Clave encontrada:** Si la clave del nodo coincide con la clave objetivo, se retorna el nodo actual.
- **Comparación:** Se evalúa la relación entre la clave objetivo y la clave del nodo actual.
- **Rama izquierda:** Si la clave objetivo es menor, se busca recursivamente en el subárbol izquierdo.
- **Rama derecha:** De lo contrario, se busca en el subárbol derecho.

El método `contains` de la clase Treap simplemente utiliza `search` en la raíz y retorna `true` o `false` según si el resultado es `null` o no.

#### 2. Inserción de una nueva entrada

Insertar una nueva clave en un treap es más complicado que en un BST, ya que, aunque la clave se coloque en la posición correcta, puede romper la invariante del heap respecto a la prioridad.  
Para solucionar esta situación, se realiza una rotación en el nodo cuya prioridad infringe la invariante.

El proceso de inserción se divide en dos pasos:

1. **Inserción como hoja:** Se inserta el nuevo nodo en el lugar adecuado.
2. **Ajuste de prioridades:** Se eleva el nuevo nodo mediante rotaciones si su prioridad es mayor que la de su padre, garantizando que el nodo con mayor prioridad quede en la raíz del subárbol correspondiente.

#### Pseudocódigo: método `insert`

```
function insert(treap, key, priority) 
    node <- treap.root 
    parent <- null 
    newNode <- new Node(key, priority) 
    while node != null do 
        parent <- node 
        if node.key <= key then  
            node <- node.left  
        else 
            node <- node.right 
    if parent == null then 
        treap.root <- newNode  
        return 
    elsif key <= parent.key then 
        parent.left <- newNode  
    else 
        parent.right <- newNode  
    newNode.parent <- parent 
    while newNode.parent != null 
          and newNode.priority < newNode.parent.priority do 
        if newNode == newNode.parent.left then 
            rightRotate(newNode) 
        else 
            leftRotate(newNode) 
    if newNode.parent == null then  
        treap.root <- newNode 
```

#### Explicación:

- **Entrada:** Se recibe la instancia del treap, la clave y la prioridad a insertar. Se permiten duplicados (se agregan al subárbol izquierdo).
- **Inicialización:** Se asigna el nodo actual como la raíz y se declara una variable para el padre.
- **Creación del nodo:** Se crea un nuevo nodo que contendrá la clave y la prioridad.
- **Recorrido:** Se recorre el árbol hasta encontrar un nodo `null`, manteniendo el seguimiento del padre.
- **Actualización del padre:** Se actualiza la variable `parent` mientras el nodo actual no sea `null`.
- **Decisión de la rama:** Si la nueva clave no es mayor que la clave del nodo actual, se toma la rama izquierda.
- **Rama derecha:** En caso contrario, se avanza por la derecha.
- **Inserción en árbol vacío:** Si el árbol estaba vacío (`parent` es `null`), se asigna el nuevo nodo como raíz.
- **Termina la inserción en árbol vacío:** Se finaliza el proceso.
- **Asignación de hijo:** Se verifica si la nueva clave se debe agregar como hijo izquierdo o derecho del `parent`.
- **Establecimiento del enlace:** Se conecta el nuevo nodo con su padre.
- **Ajuste de prioridades:** Se verifica la invariante del heap y se eleva el nodo si es necesario, hasta llegar a la raíz.
- **Rotación a la derecha:** Si el nuevo nodo es hijo izquierdo, se realiza una rotación a la derecha.
- **Rotación a la izquierda:** En caso contrario, se realiza una rotación a la izquierda.
- **Actualización de la raíz:** Si el nuevo nodo se eleva hasta la raíz, se actualiza la propiedad `root` del treap.

**Análisis del tiempo de ejecución:**  

El recorrido para insertar la nueva hoja requiere *O(h)*, donde *h* es la altura del árbol. Además, el proceso de elevación mediante rotaciones, que en el peor caso puede alcanzar la raíz, también requiere *O(h)* operaciones, lo que hace que la inserción global tenga un coste de *O(h)*.


#### 3. Eliminación de una clave

Eliminar una clave en un treap implica un enfoque diferente al de los BST convencionales. En lugar de reemplazar el nodo a eliminar con su sucesor o predecesor (lo cual puede violar la invariante de prioridades), se empuja el nodo hacia abajo hasta convertirlo en una hoja y, finalmente, se desconecta.

El procedimiento consiste en asignar la prioridad más baja posible al nodo a eliminar y corregir las invarianzas del heap, haciendo rotaciones hasta que el nodo se encuentre en el nivel más bajo.

#### Pseudocódigo: método `remove`

```
function remove(treap, key) 
     node <- search(treap.root, key) 
     if node == null then 
         return false 
     if isRoot(node) and isLeaf(node) then  
         treap.root <- null 
         return true 
     while not isLeaf(node) do 
         if node.left != null 
             and (node.right == null 
             or node.left.priority > node.right.priority) then  
             rotateRight(node.left) 
         else 
             rotateLeft(node.right)  
     if isRoot(node.parent) then 
         treap.root <- node.parent 
     if node.parent.left == node then 
         node.parent.left <- null 
     else 
         node.parent.right <- null 
     return true 
```

#### Explicación:

- **Entrada:** Se recibe el treap y la clave a eliminar; se retorna `true` si se elimina la clave o `false` en caso contrario.
- **Búsqueda del nodo:** Se utiliza el método `search` para localizar el nodo que contiene la clave.
- **Clave no encontrada:** Si `search` devuelve `null`, la clave no existe en el treap.
- **Caso especial:** Si el treap tiene un solo nodo (la raíz es también hoja), se elimina asignando `null` a la raíz.
- **Empuje hacia abajo:** Se empuja el nodo hacia abajo hasta que se convierta en hoja.
- **Elección del reemplazo:** Se elige el hijo con mayor prioridad (o, en un min-treap, el valor numérico menor) para la rotación.
- **Rotación a la derecha:** Si se selecciona el hijo izquierdo, se realiza una rotación a la derecha.
- **Rotación a la izquierda:** De lo contrario, se realiza una rotación a la izquierda.
- **Actualización de la raíz:** Si el nodo era hijo de la raíz, se actualiza la propiedad `root` del treap.
- **Desconexión del nodo:** Una vez que el nodo es hoja, se desconecta de su padre asignando `null` al puntero correspondiente.
- **Retorno de resultado:** Se retorna `true` indicando que la eliminación se realizó correctamente.

**Análisis del tiempo de ejecución:**  

En el peor caso, el algoritmo de eliminación tiene un coste de *O(h)*, ya que tanto el empuje hacia abajo como las rotaciones pueden requerir recorrer la altura completa del treap.

#### 4. Operaciones adicionales: top, peek y update

#### a) Operación **peek**

El método `peek` es trivial, ya que se limita a devolver la clave de la raíz del treap, de forma similar a un heap.

#### b) Operación **top**

El método `top` combina la obtención de la clave de la raíz y su eliminación, permitiendo que el treap actúe como un heap. Se utiliza el método `remove` para eliminar la clave.

#### Pseudocódigo: método `top`

```
function top(treap)  
     throw-if treap.root == null  
     key <- treap.root.key 
     remove(treap, key) 
     return key 
```

#### Explicación:

- **Entrada:** Se recibe el treap.
- **Verificación:** Se lanza una excepción si el treap está vacío.
- **Obtención de la clave:** Se almacena la clave presente en la raíz.
- **Eliminación:** Se elimina la clave de la raíz utilizando el método `remove`.
- **Retorno:** Se retorna la clave obtenida.

#### c) Actualización de prioridad (UpdatePriority)

Actualizar la prioridad de una clave requiere elevar el nodo si se incrementa la prioridad o empujarlo hacia abajo si se disminuye, realizando las rotaciones adecuadas para preservar el orden del heap. La implementación es análoga a la de los heaps, aunque en un treap se deben ajustar los enlaces mediante rotaciones en lugar de simples intercambios. 
Esta implementación se deja como ejercicio.

#### 5. Operaciones mínima y máxima (Min/Max)

Las operaciones `min` y `max` retornan, respectivamente, la clave mínima y máxima almacenada en el treap. Estas claves se encuentran en los nodos más a la izquierda y más a la derecha del árbol.

#### Pseudocódigo: método `min`

```
function min(treap)  
   throw-if treap.root == null 
   node <- treap.root 
   while node.left != null do 
       node <- node.left  
   return node.key 
```

#### Explicación:

- **Entrada:** Se recibe el treap.
- **Verificación:** Se lanza una excepción si el treap está vacío, puesto que no existiría un mínimo.
- **Inicialización:** Se asigna la variable `node` a la raíz.
- **Recorrido:** Se recorre continuamente el hijo izquierdo hasta llegar a un nodo cuyo hijo izquierdo sea `null`.
- **Retorno:** Se retorna la clave del nodo más a la izquierda.

El método `max` es análogo y se implementa recorriendo la rama derecha en lugar de la izquierda.

#### 6. Rendimiento

Todas las operaciones en un treap dependen de la altura del árbol (*h*) y, en el peor caso, las operaciones tienen el siguiente coste:

| Operación       | Tiempo de ejecución | Peor caso  |
|-----------------|---------------------|------------|
| **Insert**      | O(h)                | O(n)       |
| **Top**         | O(h)                | O(n)       |
| **Remove**      | O(h)                | O(n)       |
| **Peek**        | O(1)                | O(1)       |
| **Contains**    | O(h)                | O(n)       |
| **UpdatePriority** | O(h)             | O(n)       |
| **Min/Max**     | O(h)                | O(n)       |

- **Dependencia en la altura:** Todas las operaciones dependen de la altura del árbol, *h*, y en el peor de los casos, para árboles degenerados, *O(h)* puede equivaler a *O(n)*.  
- **Espacio adicional:** Cada método requiere únicamente un espacio extra constante.

