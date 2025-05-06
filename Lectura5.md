### Heaps: Fundamentos, estructura y optimización

#### Definición y estructura de un heap

Un heap es una estructura de datos que se utiliza comúnmente para implementar colas de prioridad. Su aplicación principal consiste en permitir la inserción y recuperación de elementos en un orden determinado (ascendente o descendente), uno a la vez. Aunque internamente se utiliza un arreglo para almacenar los elementos, conceptualmente se entiende como un árbol binario que satisface tres invariantes esenciales:

1. **Número de hijos**: Cada nodo tiene como máximo dos hijos.
2. **Completitud y ajuste a la izquierda**: El árbol es completo. Esto significa que, si el heap tiene una altura `H`, todas las hojas se encuentran en el nivel `H` o `H-1`. Además, todos los niveles están "ajustados a la izquierda", lo que quiere decir que en el último nivel las hojas se ubican de manera contigua hacia la izquierda y ningún subárbol derecho tiene una altura mayor que su hermano izquierdo.
3. **Propiedad de prioridad**: Cada nodo posee la mayor prioridad dentro del subárbol que tiene como raíz ese nodo.

Aunque el heap se representa conceptualmente como un árbol, las propiedades estructurales (completitud y ajuste a la izquierda) permiten su representación compacta mediante un arreglo. Esta representación en arreglo elimina la necesidad de punteros para padres e hijos, aprovechando la disposición secuencial de los elementos.

####  Representación en arreglo

La idea central de la representación en arreglo es que, para almacenar N elementos, el árbol se mapea directamente en un arreglo de `N` posiciones. Al asumir que el índice de inicio es 0, la relación entre padres e hijos es la siguiente:

- Para el nodo en la posición **i**:
  - El hijo izquierdo se encuentra en la posición **(2 * i) + 1**.
  - El hijo derecho se encuentra en la posición **2 * (i + 1)**.
  - El padre del nodo (excepto la raíz) se halla en la posición **(i - 1) / 2** (tomando la parte entera en la división).

Por ejemplo, si se observa un nodo ubicado en el índice 1 y con prioridad 3, sus hijos se ubicarán en los índices 3 y 4, y su padre estará en el índice 0. De igual forma, un nodo en la posición 5 tendrá como padre al elemento en el índice 2 y, si existieran hijos (no mostrados en el ejemplo), se ubicarían en los índices 11 y 12.

Esta representación es eficiente en términos de espacio, ya que el arreglo es contiguo en memoria, lo que puede ofrecer ventajas en la localidad de datos, a pesar de que la representación en árbol (con punteros) es conceptualmente más flexible.

#### Invariantes y contrato del heap

La implementación de un heap se basa en garantizar ciertas invariantes que aseguran el correcto funcionamiento de la estructura de datos. De esta forma, se definen dos aspectos fundamentales:

##### a) Modelo de datos y estructura concreta

El heap se implementa utilizando un arreglo que almacena todos los ítems. Cada elemento del arreglo es una tupla que generalmente contiene el dato y su prioridad asociada. Por ejemplo, la estructura puede definirse de la siguiente manera:

```python
class DHeap:
  # type: Array[Pair]
  pairs

  def __init__(self, pairs=[]):
      self.pairs = pairs
```

En este contexto, la notación para asignar y desestructurar las tuplas es importante. Si se tiene una variable `p` que representa una tupla, se puede extraer el elemento y su prioridad con la sintaxis:

```
(element, priority) <- p
```

Además, se puede acceder a los campos de la tupla utilizando la notación `p.element` y `p.priority`.

##### b) API del heap y contrato con el cliente

La interfaz pública (API) que define el comportamiento del heap es la siguiente:

- **top()**: Devuelve el elemento superior de la cola de prioridad (es decir, el de mayor prioridad).
- **peek()**: Permite visualizar el elemento superior sin eliminarlo.
- **insert(element, priority)**: Inserta un nuevo elemento con la prioridad asociada.
- **remove(element)**: Elimina un elemento específico del heap.
- **update(element, newPriority)**: Actualiza la prioridad de un elemento ya existente.

El contrato con el usuario es que el elemento que se devuelva siempre tendrá la mayor prioridad según el criterio definido en la implementación. La estructura de datos subyacente es el arreglo de ítems, y las invariantes garantizan que para cualquier nodo, la prioridad de dicho nodo es mayor (o igual, en algunos casos) que la de sus hijos.

#### Prioridad: Min-Heap vs Max-Heap

La noción de prioridad en un heap es relativa y depende de cómo se interprete el valor numérico asociado a cada elemento. Existen dos variantes principales:

- **Max-Heap**: Se define que un número mayor representa una mayor prioridad. Así, si se tiene dos prioridades `p1` y `p2`, la condición `p1 > p2` indica que `p1` es de mayor prioridad. En un max-heap, el elemento con el valor numérico más alto se encuentra en la cima de la estructura.
  
- **Min-Heap**: Aquí se asume que los números más pequeños tienen mayor prioridad. Esto implica que, para dos prioridades, si `p1 > p2`, se considera que `p2` es la de mayor prioridad. En esta variante, el elemento con el menor valor numérico estará en la cima.

En implementaciones prácticas, es común parametrizar la función de prioridad para generalizar el comportamiento del heap. Sin embargo, en aplicaciones específicas (por ejemplo, en la gestión de tareas) es posible aprovechar el orden natural de ciertas tuplas. Por ejemplo, si se almacenan tareas como pares (edad, tarea) en un min-heap, se extraerá primero la tarea con la edad menor. Si se requiere que la tarea más antigua (con mayor edad) sea la que se extraiga primero, se puede lograr utilizando la transformación de la prioridad, es decir, almacenando las tuplas como (-edad, tarea). 

Dado que si `x.age < y.age`, se tendrá `-x.age > -y.age`, de forma que el min-heap devolverá en primer lugar la tarea con mayor edad.

#### Variante avanzada: Heap d-ario

Aunque la forma más común de implementar un heap es mediante un árbol binario (con factor de ramificación igual a 2), no existe ninguna restricción teórica que limite la estructura a solo dos hijos por nodo. Se puede generalizar a un heap **d-ario**, donde cada nodo tiene hasta **D** hijos, con `D > 1`.

Por ejemplo, en un heap ternario (`D = 3`):

- Los hijos del nodo en la posición **i** se encuentran en:
  - Primer hijo: **3i + 1**
  - Segundo hijo: **3i + 2**
  - Tercer hijo: **3(i + 1)**
- El padre del nodo en la posición **i** se halla en la posición **(i - 1) / 3** (considerando la parte entera).

Las mismas invariantes se mantienen en la variante d-aria:
- Cada nodo puede tener como máximo `D` hijos.
- El árbol debe ser completo, con todos los niveles ajustados a la izquierda.
- Cada nodo contiene la mayor prioridad dentro del subárbol cuya raíz es ese nodo.

Un dato curioso es que, si se toma `D = 1`, el heap se convierte en un arreglo ordenado (o en una lista doblemente enlazada ordenada, según la representación en árbol). En este caso, la construcción del heap se asemeja al algoritmo de ordenamiento por inserción, con una complejidad cuadrática, mientras que las demás operaciones tienen tiempo lineal.

#### Implementación de un heap: aspectos prácticos

Con la base teórica asentada, se aborda ahora la implementación práctica de un heap, enfocándose en los métodos que permiten mantener la propiedad de prioridad tras cada modificación. Las operaciones que pueden alterar la estructura del heap son:

- **Inserción de un nuevo elemento**: Al agregar un nuevo ítem, se coloca inicialmente al final del arreglo y, posteriormente, es necesario "restablecer" el orden del heap.
- **Eliminación del elemento superior**: Al eliminar el elemento en la cima del heap, se debe reestructurar la jerarquía para que el nuevo elemento superior cumpla con la propiedad de prioridad.
- **Actualización de la prioridad de un elemento**: Modificar la prioridad de un ítem puede causar que su posición actual no sea la correcta, por lo que se debe reacomodar el elemento.

Para resolver estos problemas, se definen dos funciones auxiliares que ayudan a restablecer las propiedades del heap: una para "ascender" (bubbleUp) y otra (no descrita en el fragmento proporcionado) para "descender" (comúnmente conocida como "siftDown" o "bubbleDown"). 

#### El método bubbleUp

El método **bubbleUp** se invoca cuando un elemento tiene una prioridad mayor que la de su padre. Este método tiene la finalidad de mover el elemento "hacia arriba" en el heap 
hasta que se encuentre en la posición correcta, es decir, hasta que su prioridad sea menor o igual a la de su nuevo padre o hasta que alcance la raíz.

#####  Pseudocódigo inicial del bubbleUp

El siguiente pseudocódigo describe una implementación básica del método **bubbleUp**:

```
function bubbleUp(pairs, index=|pairs|-1)
  parentIndex <- index
  while parentIndex > 0 do
    currentIndex <- parentIndex
    parentIndex <- getParentIndex(parentIndex)
    if pairs[parentIndex].priority < pairs[currentIndex].priority then
      swap(pairs, currentIndex, parentIndex)
    else
      break
```

**Explicación de cada paso:**

1. **Inicialización**: Se recibe el arreglo `pairs`, que contiene todas las tuplas (elemento, prioridad), y se utiliza un índice, por defecto el último elemento insertado.
2. **Inicio del proceso**: Se asigna el valor del índice actual a `parentIndex` y se entra en el ciclo mientras `parentIndex` sea mayor que 0.  
3. **Comparación de prioridades**: Se actualiza el `currentIndex` al valor actual de `parentIndex`, y luego se calcula el índice del padre mediante la función `getParentIndex` . 
4. **Intercambio si es necesario**: Si la prioridad del elemento en el padre es menor que la del elemento actual, se procede a intercambiar ambos elementos (línea 6).  
5. **Terminación**: Si no se cumple la condición, se asume que el orden del heap se ha restablecido y se termina el ciclo.

Este método realiza, en cada iteración, una comparación e intercambio que, en el peor caso, se repite tantas veces como la altura del heap, la cual es logarítmica respecto al número de elementos almacenados.

##### Ejemplo conceptual del bubbleUp

Imaginemos que en un max-heap (donde los números mayores representan mayor prioridad) se inserta un nuevo elemento con prioridad 9 en la posición 7. Si el padre de este elemento, ubicado en la posición 2, tiene una prioridad de 8, la condición para intercambiar se cumple. Tras el primer intercambio, el elemento con prioridad 9 se mueve a la posición 2. En la siguiente iteración, se compara con el nuevo padre (en la raíz, por ejemplo, con prioridad 10). Al no cumplirse la condición de intercambio (ya que 10 no es menor que 9), el método termina, dejando al elemento en la posición correcta.

##### Optimización del bubbleUp

Si bien la implementación descrita intercambia el elemento en cada iteración, existe una mejora que reduce el número de asignaciones. En la implementación ingenua se realizan tres asignaciones por cada intercambio, lo cual puede ser costoso en términos de rendimiento, especialmente cuando el elemento tiene que subir varios niveles.

La optimización consiste en evitar intercambiar repetidamente el mismo elemento; en lugar de ello, se guarda el elemento en una variable temporal y se van "moviendo" los elementos del camino hacia abajo hasta encontrar la posición correcta donde insertar el elemento almacenado. Este procedimiento es similar al mecanismo utilizado en el algoritmo de ordenamiento por inserción.

El siguiente pseudocódigo muestra la versión optimizada del método **bubbleUp**:

```
function bubbleUp(pairs, index=|pairs|-1)
  current <- pairs[index]
  while index > 0 do
    parentIndex <- getParentIndex(index)
    if pairs[parentIndex].priority < current.priority then
      pairs[index] <- pairs[parentIndex]
      index <- parentIndex
    else
      break
  pairs[index] <- current
```

**Desglose del pseudocódigo optimizado:**

- **Inicialización**: Se asigna a la variable `current` el elemento del arreglo `pairs` ubicado en la posición indicada por `index`. Esta variable guarda el elemento que debe "ascender".
- **Recorrido del camino**: Mientras el índice actual sea mayor que 0, se obtiene el índice del padre con la función `getParentIndex`.
- **Comparación sin intercambio inmediato**: Se verifica si la prioridad del elemento en el padre es menor que la de `current`. Si es así, se copia el elemento del padre a la posición actual (línea 5) y se actualiza el índice a la posición del padre. Este movimiento "baja" el elemento del padre en la jerarquía.
- **Inserción final**: Una vez se encuentra el lugar correcto (cuando la condición deja de cumplirse o se alcanza la raíz), se copia el elemento almacenado en `current` a la posición determinada.

Con esta optimización se evitan múltiples asignaciones redundantes, ya que el elemento "asciende" de forma acumulativa sin realizar intercambios completos en cada iteración. En el peor de los casos, para un camino de altura `H` se realizan `H+1` asignaciones, lo que representa una mejora significativa (ahorrando aproximadamente un 66 % en el número de asignaciones)  respecto a la versión ingenua.
