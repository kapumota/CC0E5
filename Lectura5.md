### Implementación y análisis de heaps

En esta lectura se explica en detalle qué es un heap, sus propiedades fundamentales, la representación en arreglo, las variantes en función de la prioridad y la ramificación, y 
cómo se implementa mediante métodos clave como el "bubbleUp". Se aborda tanto el concepto teórico como los aspectos prácticos de la implementación, ofreciendo 
ejemplos de pseudocódigo para ilustrar cada paso.

#### Definición y estructura de un heap

Un heap es una estructura de datos que se utiliza comúnmente para implementar colas de prioridad. Su aplicación principal consiste en permitir la inserción y recuperación de elementos en un orden determinado (ascendente o descendente), uno a la vez. Aunque internamente se utiliza un arreglo para almacenar los elementos, conceptualmente se entiende como un árbol binario que satisface tres invariantes esenciales:

1. **Número de hijos**: Cada nodo tiene como máximo dos hijos.
2. **Completitud y ajuste a la izquierda**: El árbol es completo. Esto significa que, si el heap tiene una altura H, todas las hojas se encuentran en el nivel H o H-1. Además, todos los niveles están "ajustados a la izquierda", lo que quiere decir que en el último nivel las hojas se ubican de manera contigua hacia la izquierda y ningún subárbol derecho tiene una altura mayor que su hermano izquierdo.
3. **Propiedad de prioridad**: Cada nodo posee la mayor prioridad dentro del subárbol que tiene como raíz ese nodo.

Aunque el heap se representa conceptualmente como un árbol, las propiedades estructurales (completitud y ajuste a la izquierda) permiten su representación compacta mediante un arreglo. Esta representación en arreglo elimina la necesidad de punteros para padres e hijos, aprovechando la disposición secuencial de los elementos.

####  Representación en arreglo

La idea central de la representación en arreglo es que, para almacenar N elementos, el árbol se mapea directamente en un arreglo de N posiciones. Al asumir que el índice de inicio es 0, la relación entre padres e hijos es la siguiente:

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
(element, priority) ← p
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

- **Max-Heap**: Se define que un número mayor representa una mayor prioridad. Así, si se tiene dos prioridades p1 y p2, la condición p1 > p2 indica que p1 es de mayor prioridad. En un max-heap, el elemento con el valor numérico más alto se encuentra en la cima de la estructura.
  
- **Min-Heap**: Aquí se asume que los números más pequeños tienen mayor prioridad. Esto implica que, para dos prioridades, si p1 > p2, se considera que p2 es la de mayor prioridad. En esta variante, el elemento con el menor valor numérico estará en la cima.

En implementaciones prácticas, es común parametrizar la función de prioridad para generalizar el comportamiento del heap. Sin embargo, en aplicaciones específicas (por ejemplo, en la gestión de tareas) es posible aprovechar el orden natural de ciertas tuplas. Por ejemplo, si se almacenan tareas como pares (edad, tarea) en un min-heap, se extraerá primero la tarea con la edad menor. Si se requiere que la tarea más antigua (con mayor edad) sea la que se extraiga primero, se puede lograr utilizando la transformación de la prioridad, es decir, almacenando las tuplas como (-edad, tarea). 
Dado que si x.age < y.age, se tendrá -x.age > -y.age, de forma que el min-heap devolverá en primer lugar la tarea con mayor edad.

#### Variante avanzada: Heap d-ario

Aunque la forma más común de implementar un heap es mediante un árbol binario (con factor de ramificación igual a 2), no existe ninguna restricción teórica que limite la estructura a solo dos hijos por nodo. Se puede generalizar a un heap **d-ario**, donde cada nodo tiene hasta **D** hijos, con D > 1.

Por ejemplo, en un heap ternario (D = 3):

- Los hijos del nodo en la posición **i** se encuentran en:
  - Primer hijo: **3i + 1**
  - Segundo hijo: **3i + 2**
  - Tercer hijo: **3(i + 1)**
- El padre del nodo en la posición **i** se halla en la posición **(i - 1) / 3** (considerando la parte entera).

Las mismas invariantes se mantienen en la variante d-aria:
- Cada nodo puede tener como máximo D hijos.
- El árbol debe ser completo, con todos los niveles ajustados a la izquierda.
- Cada nodo contiene la mayor prioridad dentro del subárbol cuya raíz es ese nodo.

Un dato curioso es que, si se toma D = 1, el heap se convierte en un arreglo ordenado (o en una lista doblemente enlazada ordenada, según la representación en árbol). En este caso, la construcción del heap se asemeja al algoritmo de ordenamiento por inserción, con una complejidad cuadrática, mientras que las demás operaciones tienen tiempo lineal.

#### Implementación de un heap: aspectos prácticos

Con la base teórica asentada, se aborda ahora la implementación práctica de un heap, enfocándose en los métodos que permiten mantener la propiedad de prioridad tras cada modificación. Las operaciones que pueden alterar la estructura del heap son:

- **Inserción de un nuevo elemento**: Al agregar un nuevo ítem, se coloca inicialmente al final del arreglo y, posteriormente, es necesario “restablecer” el orden del heap.
- **Eliminación del elemento superior**: Al eliminar el elemento en la cima del heap, se debe reestructurar la jerarquía para que el nuevo elemento superior cumpla con la propiedad de prioridad.
- **Actualización de la prioridad de un elemento**: Modificar la prioridad de un ítem puede causar que su posición actual no sea la correcta, por lo que se debe reacomodar el elemento.

Para resolver estos problemas, se definen dos funciones auxiliares que ayudan a restablecer las propiedades del heap: una para “ascender” (bubbleUp) y otra (no descrita en el fragmento proporcionado) para “descender” (comúnmente conocida como “siftDown” o “bubbleDown”). En el presente contenido se detalla el método **bubbleUp**.

#### El Método BubbleUp

El método **bubbleUp** se invoca cuando un elemento tiene una prioridad mayor que la de su padre. Este método tiene la finalidad de mover el elemento "hacia arriba" en el heap 
hasta que se encuentre en la posición correcta, es decir, hasta que su prioridad sea menor o igual a la de su nuevo padre o hasta que alcance la raíz.

#####  Pseudocódigo inicial del BubbleUp

El siguiente pseudocódigo describe una implementación básica del método **bubbleUp**:

```
function bubbleUp(pairs, index=|pairs|-1)
  parentIndex ← index
  while parentIndex > 0 do
    currentIndex ← parentIndex
    parentIndex ← getParentIndex(parentIndex)
    if pairs[parentIndex].priority < pairs[currentIndex].priority then
      swap(pairs, currentIndex, parentIndex)
    else
      break
```

**Explicación de cada paso:**

1. **Inicialización**: Se recibe el arreglo `pairs`, que contiene todas las tuplas (elemento, prioridad), y se utiliza un índice, por defecto el último elemento insertado (línea 1).  
2. **Inicio del proceso**: Se asigna el valor del índice actual a `parentIndex` y se entra en el ciclo mientras `parentIndex` sea mayor que 0 (línea 3).  
3. **Comparación de prioridades**: Se actualiza el `currentIndex` al valor actual de `parentIndex`, y luego se calcula el índice del padre mediante la función `getParentIndex` (línea 4).  
4. **Intercambio si es necesario**: Si la prioridad del elemento en el padre es menor que la del elemento actual (línea 5), se procede a intercambiar ambos elementos (línea 6).  
5. **Terminación**: Si no se cumple la condición, se asume que el orden del heap se ha restablecido y se termina el ciclo (línea 7).

Este método realiza, en cada iteración, una comparación e intercambio que, en el peor caso, se repite tantas veces como la altura del heap, la cual es logarítmica respecto al número de elementos almacenados.

##### Ejemplo conceptual del BubbleUp

Imaginemos que en un max-heap (donde los números mayores representan mayor prioridad) se inserta un nuevo elemento con prioridad 9 en la posición 7. Si el padre de este elemento, ubicado en la posición 2, tiene una prioridad de 8, la condición para intercambiar se cumple. Tras el primer intercambio, el elemento con prioridad 9 se mueve a la posición 2. En la siguiente iteración, se compara con el nuevo padre (en la raíz, por ejemplo, con prioridad 10). Al no cumplirse la condición de intercambio (ya que 10 no es menor que 9), el método termina, dejando al elemento en la posición correcta.

##### Optimización del BubbleUp

Si bien la implementación descrita intercambia el elemento en cada iteración, existe una mejora que reduce el número de asignaciones. En la implementación ingenua se realizan tres asignaciones por cada intercambio, lo cual puede ser costoso en términos de rendimiento, especialmente cuando el elemento tiene que subir varios niveles.

La optimización consiste en evitar intercambiar repetidamente el mismo elemento; en lugar de ello, se guarda el elemento en una variable temporal y se van "moviendo" los elementos del camino hacia abajo hasta encontrar la posición correcta donde insertar el elemento almacenado. Este procedimiento es similar al mecanismo utilizado en el algoritmo de ordenamiento por inserción.

El siguiente pseudocódigo muestra la versión optimizada del método **bubbleUp**:

```
function bubbleUp(pairs, index=|pairs|-1)
  current ← pairs[index]
  while index > 0 do
    parentIndex ← getParentIndex(index)
    if pairs[parentIndex].priority < current.priority then
      pairs[index] ← pairs[parentIndex]
      index ← parentIndex
    else
      break
  pairs[index] ← current
```

**Desglose del pseudocódigo optimizado:**

- **Inicialización**: Se asigna a la variable `current` el elemento del arreglo `pairs` ubicado en la posición indicada por `index` (línea 2). Esta variable guarda el elemento que debe “ascender”.
- **Recorrido del camino**: Mientras el índice actual sea mayor que 0, se obtiene el índice del padre con la función `getParentIndex` (línea 4).
- **Comparación sin intercambio inmediato**: Se verifica si la prioridad del elemento en el padre es menor que la de `current`. Si es así, se copia el elemento del padre a la posición actual (línea 5) y se actualiza el índice a la posición del padre (línea 6). Este movimiento "baja" el elemento del padre en la jerarquía.
- **Inserción final**: Una vez se encuentra el lugar correcto (cuando la condición deja de cumplirse o se alcanza la raíz), se copia el elemento almacenado en `current` a la posición determinada (línea 8).

Con esta optimización se evitan múltiples asignaciones redundantes, ya que el elemento "asciende” de forma acumulativa sin realizar intercambios completos en cada iteración. En el peor de los casos, para un camino de altura H se realizan H+1 asignaciones, lo que representa una mejora significativa (ahorrando aproximadamente un 66 % en el número de asignaciones) 
respecto a la versión ingenua.


### Operaciones en heaps: PushDown, Insert, Top y Update

El manejo eficiente de un heap requiere el uso de operaciones auxiliares que garanticen el mantenimiento de las propiedades estructurales y de prioridad definidas para la estructura. Entre estas operaciones se destacan dos métodos básicos: uno que mueve un elemento hacia arriba (bubbleUp, tratado en otra sección) y otro que lo desplaza hacia abajo (pushDown). Además, se debe contar con operaciones que permitan la inserción de nuevos elementos, la extracción del elemento superior y la actualización de la prioridad de un elemento existente. A continuación se presentan en detalle las operaciones pushDown, insert, top y update.

#### Operación PushDown

##### *Objetivo de PushDown*

El método **pushDown** se utiliza cuando un elemento, al haber sufrido una modificación o tras la eliminación de la raíz, podría violar la invariante de prioridad en relación con sus hijos. Es decir, aunque el elemento modificado mantenga la propiedad respecto a su padre, es posible que al compararlo con sus hijos se encuentre que alguno de ellos posee una prioridad superior. Esto se presenta, por ejemplo, cuando se extrae la raíz del heap y se reemplaza con el último elemento del arreglo o cuando se disminuye la prioridad de un nodo. La función pushDown garantiza que, moviendo el elemento hacia abajo, se restablezca el orden del heap.

##### Pseudocódigo del método pushDown

El siguiente fragmento de pseudocódigo describe una implementación básica del método pushDown:

```
function pushDown(pairs, index=0)
  currentIndex ← index                                         ❶
  while currentIndex < firstLeafIndex(pairs) do               ❷
    (child, childIndex) ← highestPriorityChild(currentIndex)  ❸
    if child.priority > pairs[currentIndex].priority then     ❹
      swap(pairs, currentIndex, childIndex)                   ❺
      currentIndex ← childIndex
    else                                                      ❻
      break
```

##### *Explicación línea por línea*

1. **Inicialización (línea 1):**  
   Se comienza en el índice especificado (por defecto, 0, que corresponde a la raíz del heap). Se asigna a `currentIndex` el valor del índice inicial, ya que es el nodo que se evaluará para determinar si cumple con la propiedad de prioridad respecto a sus hijos.
2. **Condición del bucle (línea 2):**  
   Se establece que el proceso se repetirá mientras `currentIndex` sea menor que el índice de la primera hoja del heap. Dado que las hojas no tienen hijos, no es necesario moverlas; por ello, la función `firstLeafIndex(pairs)` devuelve el índice a partir del cual los nodos son hojas, asegurando que solo se evalúen nodos internos.
3. **Selección del hijo de mayor prioridad (línea 3):**  
   Para el nodo actual, se identifica cuál de sus hijos tiene la mayor prioridad. Esta operación es crucial, pues solo se permite mover el nodo actual si alguno de sus hijos supera su prioridad. La función `highestPriorityChild(currentIndex)` retorna una tupla que contiene tanto el hijo con la mayor prioridad como su índice en el arreglo.
4. **Comparación y evaluación (línea 4):**  
   Se compara la prioridad del hijo identificado con la del nodo actual. Si la prioridad del hijo es mayor, se determina que la posición del nodo actual es incorrecta.
5. **Intercambio y actualización (línea 5 y siguiente):**  
   En caso de que el hijo tenga mayor prioridad, se intercambian los elementos del nodo actual y del hijo. Posteriormente, se actualiza `currentIndex` al índice del hijo, para continuar evaluando si el nodo que se acaba de mover hacia abajo cumple con la propiedad en el siguiente nivel.
6. **Finalización del bucle (línea 6):**  
   Si la condición de intercambio no se cumple (es decir, la prioridad del nodo actual es mayor o igual a la de su hijo con mayor prioridad), se termina el bucle, ya que el nodo se encuentra en la posición adecuada.

##### *Consideraciones sobre eficiencia en pushDown*

El método pushDown realiza, en el peor de los casos, un número de iteraciones proporcional a la altura del heap. Dado que un heap es un árbol completo balanceado, su altura es logarítmica respecto al número de elementos. En particular, para un heap con factor de ramificación \( D \) y \( n \) elementos, el tiempo de ejecución puede aproximarse a \( O(D \times \log_D(n)) \). Es importante notar que, aunque ambos métodos (bubbleUp y pushDown) son logarítmicos, pushDown puede requerir un mayor número de comparaciones en cada nivel debido a la evaluación de todos los hijos del nodo actual.

##### *Versión optimizada de pushDown*

Al igual que en el caso de bubbleUp, es posible optimizar pushDown evitando intercambios innecesarios. En lugar de intercambiar el elemento en cada iteración, se almacena el elemento actual en una variable temporal y se “mueven” los hijos de mayor prioridad hacia arriba hasta encontrar el sitio correcto para insertar el elemento. La versión optimizada se presenta a continuación:

```
function pushDown(pairs, index=0)
  current ← pairs[index]                                   ❶
  while index < firstLeafIndex(pairs) do                   ❷
       (child, childIndex) ← highestPriorityChild(index)   ❸
    if child.priority > current.priority then              ❹
      pairs[index] ← pairs[childIndex]                     ❺
      index ← childIndex
    else                                                   ❻
      break
  pairs[index] ← current                                   ❼
```

- **Línea 1:** Se guarda el elemento que se desea mover en la variable `current`.  
- **Línea 2:** Se evalúa el bucle mientras el índice actual sea menor que el de la primera hoja.  
- **Línea 3:** Se identifica el hijo con la mayor prioridad.  
- **Línea 4:** Si la prioridad del hijo supera a la de `current`, se copia el hijo a la posición actual en el arreglo, moviendo efectivamente el elemento hacia arriba en la jerarquía.  
- **Línea 5 y 6:** Se actualiza el índice al del hijo y se continúa la iteración; si no se cumple la condición, se rompe el bucle.  
- **Línea 7:** Finalmente, se coloca el elemento almacenado en `current` en su posición correcta.

Esta versión evita intercambiar en cada paso y, por tanto, reduce el número total de asignaciones, mejorando el rendimiento en aplicaciones con un gran número de elementos o en situaciones donde la operación pushDown se realiza con frecuencia.

#### Operación de inserción (insertar)

##### *Objetivo de la inserción en un heap*

La operación de inserción permite agregar un nuevo elemento al heap, manteniendo las propiedades estructurales y de prioridad. Al insertar, se añade inicialmente el nuevo elemento al final del arreglo que representa el heap. Esto garantiza que la propiedad de completitud se preserve. Sin embargo, este nuevo elemento podría violar la invariante de que cada nodo debe tener una prioridad mayor que la de sus hijos (en un max-heap, o menor en un min-heap). Por ello, se utiliza el método bubbleUp para “hacerlo ascender” y colocarlo en la posición correcta.

##### *Pseudocódigo para la inserción*

El siguiente pseudocódigo describe la operación de inserción en un heap:

```
function insert(element, priority)
  p ← Pair(element, priority)         ❶
  pairs.append(p)                     ❷
  bubbleUp(pairs, |pairs| – 1)        ❸
```

##### *Explicación de cada paso en la inserción*

1. **Creación del par (línea 1):**  
   Se crea una nueva tupla o par que contiene el elemento y la prioridad asociada. Esto encapsula ambos datos en una estructura que será manipulada en el heap.

2. **Adición al arreglo (línea 2):**  
   El par recién creado se añade al final del arreglo que representa el heap. Dado que los arreglos se usan para representar el heap de forma compacta, esta operación preserva la propiedad de que el árbol es completo, ya que se añade el nuevo elemento en la siguiente posición disponible.

3. **Restablecimiento de las propiedades (línea 3):**  
   Tras la inserción, se llama a la función **bubbleUp** pasando como argumento el índice del nuevo elemento (que es el último índice del arreglo). Esta llamada se encarga de mover el elemento hacia arriba, si es necesario, para que la invariante de prioridad se mantenga. En un max-heap, por ejemplo, si el nuevo elemento tiene una prioridad mayor que la de su padre, se intercambiará hasta alcanzar la posición correcta.

##### *Consideraciones sobre la inserción*

El proceso de inserción tiene una complejidad que depende de la altura del heap. Cada intercambio en bubbleUp mueve el elemento un nivel hacia la raíz, y dado que la altura es logarítmica en función del número de elementos, se requerirá como máximo \( O(\log_D(n)) \) intercambios en un heap d-ario.  
Un aspecto adicional es el manejo del tamaño del arreglo. Si se utiliza un arreglo estático, es necesario prever la cantidad máxima de elementos. En cambio, si se usa un arreglo dinámico, la operación de inserción es logarítmica en promedio (amortizada), aunque ocasionalmente se deba redimensionar el arreglo, lo cual incurre en un costo adicional momentáneo.


#### Operación top (extracción del elemento superior)

##### *Objetivo de la operación top*

El método **top** se encarga de extraer el elemento superior del heap, es decir, el que tiene la mayor (o menor, en el caso de min-heaps) prioridad. Esta operación es fundamental en el uso de colas de prioridad, ya que permite obtener de forma eficiente el elemento “más importante”. Al extraer la raíz, se genera un “hueco” en la estructura del heap que debe ser rellenado para mantener la propiedad de completitud y la invariante de prioridad.

##### *Pseudocódigo del método top*

El pseudocódigo para extraer el elemento superior se muestra a continuación:

```
function top()
  if pairs.isEmpty() then error()   ❶
  p ← pairs.removeLast()            ❷
  if pairs.isEmpty() then           ❸
    return p.element
  else  
    (element, priority) ← pairs[0]   ❹
    pairs[0] ← p                    ❺
    pushDown(pairs, 0)              ❻
    return element
```

##### *Explicación detallada del proceso*

1. **Verificación de vaciedad (línea 1):**  
   Antes de proceder a extraer el elemento superior, se comprueba que el heap no esté vacío. En caso de que lo esté, se lanza un error o se retorna un valor nulo, ya que no es posible extraer de una estructura sin elementos.

2. **Extracción del último elemento (línea 2):**  
   Se elimina el último elemento del arreglo mediante la operación `removeLast()` y se almacena en una variable temporal `p`. Esta operación resulta eficiente en arreglos, ya que la eliminación se realiza desde el final.

3. **Caso de único elemento (línea 3):**  
   Se vuelve a comprobar si, tras la eliminación, el arreglo queda vacío. Esto ocurre cuando el heap contenía un solo elemento. En ese caso, se retorna directamente el elemento extraído, ya que este es, por definición, la raíz del heap.

4. **Reemplazo de la raíz (línea 4 y 5):**  
   Si el heap contiene más elementos, se procede a almacenar el par que actualmente se encuentra en la raíz (índice 0) en una variable temporal.
   A continuación, se reemplaza el primer elemento del arreglo con el elemento almacenado en `p` (el último elemento extraído). Esta operación llena el "hueco" dejado por la eliminación de la raíz, aunque es posible que la nueva raíz no cumpla con la propiedad de prioridad.

6. **Restablecimiento del orden (línea 6):**  
   Tras colocar el último elemento en la raíz, se invoca el método **pushDown** para moverlo hacia abajo hasta encontrar la posición en la que la propiedad de prioridad se mantenga. Esta llamada asegura que el heap recupere su orden interno.

7. **Retorno del elemento superior (última línea):**  
   Finalmente, se retorna el elemento que originalmente ocupaba la raíz (almacenado previamente en la variable temporal). Este es el valor que se desea extraer del heap.

### 3.4 Consideraciones de Rendimiento para top()

La operación top combina la eliminación del último elemento con la operación pushDown. Dado que ambos procesos son logarítmicos en la altura del heap, la complejidad total de top() se sitúa en el orden de \( O(\log_D(n)) \) en el peor de los casos. Es importante señalar que el manejo correcto del tamaño del arreglo es fundamental para evitar costos adicionales en casos de redimensionamiento, en particular si se emplean arreglos dinámicos.

#### Operación update (actualización de prioridad)

##### **Objetivo de la operación update**

El método **update** permite modificar la prioridad de un elemento existente en el heap. Esta operación es especialmente útil en aplicaciones donde las prioridades de los elementos pueden cambiar en función de eventos externos o del progreso de ciertos procesos. Al actualizar un elemento, es posible que su nueva prioridad lo desubique del orden correcto, por lo que se deben aplicar las operaciones bubbleUp o pushDown según corresponda.

##### **Pseudocódigo del método update**

El siguiente pseudocódigo muestra cómo se implementa la actualización de la prioridad:

```
function update(oldValue, newPriority)
  index ← pairs.find(oldValue)                     ❶
  if index ≥ 0 then                                ❷
    oldPriority ← pairs[index].priority
    pairs[index] ← Pair(oldValue, newPriority)
    if (newPriority < oldPriority) then            ❸
      bubbleUp(pairs, index)                       ❹
    elsif (newPriority > oldPriority) then        
      pushDown(pairs, index)                       ❺
```

##### Desglose del proceso de actualización

1. **Búsqueda del elemento (línea 1):**  
   El proceso comienza localizando la posición del elemento cuya prioridad se desea modificar. Se utiliza la función `pairs.find(oldValue)` para obtener el índice en el arreglo que contiene dicho elemento. Esta búsqueda puede ser costosa en implementaciones simples, ya que podría requerir recorrer el arreglo de manera lineal.

2. **Verificación y actualización (línea 2):**  
   Se verifica que el elemento exista en el heap (es decir, que el índice encontrado sea válido). Si el elemento se encuentra, se procede a almacenar su prioridad antigua en una variable `oldPriority` y se actualiza el contenido del arreglo en esa posición con la nueva prioridad, manteniendo el mismo valor del elemento.

3. **Determinación del movimiento necesario (línea 3):**  
   Se compara la nueva prioridad con la antigua para determinar en qué dirección se debe mover el elemento.  
   - Si la nueva prioridad es menor que la antigua (en un max-heap, esto implica que el elemento podría estar demasiado "alto"), se invoca bubbleUp para mover el elemento hacia arriba, asegurando que la invariante de prioridad se cumpla en relación a sus padres.  
   - Si, por el contrario, la nueva prioridad es mayor que la antigua, se llama a pushDown para mover el elemento hacia abajo y restablecer la correcta jerarquía respecto a sus hijos.

4. **Selección del algoritmo apropiado (líneas 4 y 5):**  
   La elección entre `bubbleUp` y `pushDown` depende directamente de cómo la modificación de la prioridad afecta la posición del elemento dentro del heap. Este enfoque segmentado permite que la operación update mantenga su eficiencia, ya que solo se realiza el ajuste necesario en función del cambio introducido.

##### *Consideraciones de rendimiento en update*

El rendimiento global del método update depende en gran medida de la eficiencia de la búsqueda del elemento a actualizar. En implementaciones básicas, la búsqueda se realiza en tiempo lineal, lo que puede degradar el rendimiento si se realizan múltiples actualizaciones. Para mitigar este problema, es común mantener estructuras auxiliares (por ejemplo, un mapa hash) que asocien cada elemento con su índice en el heap, permitiendo una búsqueda en tiempo amortizado O(1).  
Además, las operaciones bubbleUp y pushDown que se ejecutan tras la actualización tienen una complejidad de O(log_D(n)), lo que garantiza que, en conjunto, la actualización mantenga una eficiencia aceptable para estructuras grandes.


#### Integración de las operaciones en la API del Heap

Con las funciones auxiliares bubbleUp y pushDown bien definidas, las operaciones principales del heap (insert, top y update) se simplifican considerablemente. Cada una de estas operaciones se apoya en las funciones auxiliares para garantizar que, tras cualquier modificación (ya sea la adición, extracción o actualización de un elemento), las propiedades del heap se mantengan sin violaciones.

- **Inserción:**  
  La operación insert añade el nuevo elemento al final del arreglo y llama a bubbleUp para posicionarlo correctamente, sin necesidad de preocuparse por la reestructuración del árbol de forma manual.

- **Extracción (Top):**  
  Al eliminar el elemento superior, se utiliza la técnica de reemplazar la raíz con el último elemento del arreglo y luego ajustar su posición mediante pushDown, lo que simplifica la eliminación y minimiza los movimientos innecesarios.

- **Actualización:**  
  La operación update es la más compleja desde el punto de vista de la lógica, ya que debe determinar si el cambio en la prioridad requiere un ajuste ascendente o descendente. El uso condicional de bubbleUp o pushDown permite manejar ambas situaciones de manera uniforme.

El diseño modular de estas operaciones facilita también la adaptación del heap a diferentes requerimientos. Por ejemplo, la distinción entre max-heap y min-heap se puede implementar variando las condiciones de comparación en bubbleUp y pushDown, o incluso intercambiando la función de prioridad sin alterar la estructura base del código.

La implementación compacta del heap, basada en un arreglo, permite además que la asignación de memoria se realice de manera contigua, lo que favorece la localidad de referencia en memoria y, en consecuencia, mejora la eficiencia en términos de velocidad de acceso a los elementos.


#### Consideraciones adicionales sobre la manipulación del heap

##### Manejo del tamaño del arreglo

Un aspecto relevante en la implementación práctica es el manejo del arreglo que almacena los pares (elemento, prioridad). Dependiendo del lenguaje de programación y de la estructura de datos utilizada, puede tratarse de un arreglo estático o dinámico.  
- En un **arreglo estático**, se debe definir el tamaño máximo del heap en el momento de su creación. Esto implica una limitación en el número de elementos que se pueden almacenar, pero garantiza que las operaciones de inserción y extracción se realicen en tiempo logarítmico en el peor caso.  
- En un **arreglo dinámico**, el tamaño se redimensiona automáticamente conforme se agregan elementos. Aunque la redimensión tiene un costo, este se distribuye de forma amortizada, haciendo que la mayoría de las operaciones mantengan una complejidad logarítmica.

##### Impacto del factor de ramificación

La complejidad de las operaciones en un heap también depende del factor de ramificación D. Mientras que en un heap binario D = 2 se realizan menos comparaciones en cada nivel, en un heap d-ario con D > 2 se requiere evaluar más hijos en cada iteración, lo que puede aumentar el número de comparaciones en el método pushDown.  
Sin embargo, al aumentar D, se reduce la altura del heap, lo que puede compensar el mayor número de comparaciones por nivel. Por ello, la elección del factor de ramificación es un equilibrio entre el número de comparaciones por nodo y la profundidad del árbol.

##### Aplicación en diferentes contextos

Las operaciones descritas son fundamentales en una gran variedad de aplicaciones:
- **Gestión de tareas:**  
  En sistemas de planificación, se utiliza el heap para determinar la tarea con la prioridad más alta en un momento dado. Por ejemplo, al insertar una tarea urgente, se llama a insert y se utiliza bubbleUp para garantizar que la tarea se posicione en la parte superior de la cola de prioridad.
- **Sistemas operativos:**  
  Los heaps se utilizan en la gestión de procesos y en la planificación de la CPU, donde la operación top extrae el proceso de mayor prioridad para asignarle recursos.
- **Algoritmos de grafos:**  
  En algoritmos como Dijkstra o Prim, el heap se utiliza para seleccionar el nodo con la distancia o peso mínimo, dependiendo de si se implementa como min-heap o max-heap. La actualización de las distancias se maneja mediante la operación update, permitiendo ajustar de forma dinámica la prioridad de cada nodo conforme se descubren nuevas rutas o se modifican los pesos.

##### Adaptabilidad y modularidad

La modularidad en la implementación de las operaciones de un heap –con funciones auxiliares claramente definidas para bubbleUp y pushDown– permite que la misma estructura de datos se adapte a diferentes requerimientos. Por ejemplo, para transformar un min-heap en un max-heap se puede simplemente invertir el criterio de comparación en las funciones auxiliares, sin necesidad de modificar la lógica de inserción, extracción o actualización.  
Esta adaptabilidad es particularmente útil en aplicaciones de propósito general, donde se puede parametrizar la función de prioridad según las necesidades específicas del problema. De esta forma, la misma estructura base de heap puede utilizarse en contextos tan variados como la gestión de colas de procesos, algoritmos de planificación o incluso en la implementación de estructuras de datos más complejas.

##### Relevancia en el rendimiento global del sistema

El rendimiento de las operaciones sobre un heap tiene un impacto directo en el rendimiento global del sistema que lo utiliza. La eficiencia en la ejecución de pushDown y bubbleUp, por ejemplo, es crítica en aplicaciones donde se realizan múltiples actualizaciones y extracciones en tiempo real.  
El ahorro obtenido al optimizar estas operaciones –reduciendo el número de asignaciones mediante el uso de variables temporales y evitando intercambios innecesarios– se traduce en una mejora significativa del rendimiento en escenarios con un alto volumen de datos. Además, la posibilidad de mantener un índice actualizado de cada elemento, mediante estructuras auxiliares, permite que la operación update se ejecute en tiempo cercano al óptimo, incluso en implementaciones con arreglos dinámicos.


#### Consistencia y el mantenimiento de la propiedad del heap

Cada una de las operaciones presentadas (pushDown, insert, top y update) se centra en mantener tres propiedades fundamentales del heap:

1. **Propiedad estructural:**  
   El heap debe representarse mediante un arreglo que corresponde a un árbol completo, donde todas las hojas están en el nivel más bajo o en el penúltimo, manteniendo un ajuste a la izquierda.

2. **Propiedad de prioridad:**  
   En un max-heap, cada nodo debe tener una prioridad mayor o igual que la de sus hijos; en un min-heap, la situación es la inversa. Las operaciones bubbleUp y pushDown se encargan de restablecer esta propiedad tras modificaciones en la estructura.

3. **Integridad del arreglo:**  
   La representación en arreglo del heap permite acceder de forma eficiente a los elementos. Las operaciones de inserción y eliminación se aprovechan de la facilidad para añadir o quitar elementos del final del arreglo, y se garantizan mediante métodos auxiliares que reubican el elemento modificado sin necesidad de redirigir punteros.

El correcto funcionamiento del heap depende de la coordinación entre estas propiedades y de la implementación modular de las operaciones. Cada cambio –ya sea la inserción de un nuevo elemento, la actualización de la prioridad de uno existente o la extracción del elemento superior– se realiza de forma que la estructura global se mantiene coherente y lista para futuras operaciones.

La combinación de estas técnicas permite que el heap actúe como una estructura de datos muy versátil y eficiente en contextos de alta demanda, donde la rapidez en la selección del elemento “más importante” es crucial. Además, la posibilidad de ajustar el criterio de prioridad de forma parametrizable hace que esta estructura se adapte a una amplia variedad de escenarios, sin necesidad de reescribir la lógica subyacente.


#### Detalles técnicos y comparaciones de implementación

A nivel técnico, la implementación del heap en un lenguaje de programación moderno puede beneficiarse de optimizaciones específicas en el manejo de memoria y operaciones aritméticas para calcular índices. Por ejemplo:

- **Cálculo de índices:**  
  Para un heap representado en un arreglo con índice inicial 0, el cálculo del índice del hijo izquierdo se realiza como 2*i + 1 y del hijo derecho como 2 *(i + 1). De manera similar, el índice del padre se obtiene como \lfloor (i - 1) / D \rfloor para un heap d-ario. Estas fórmulas permiten un acceso directo y rápido a los elementos relacionados sin el uso de punteros, lo que resulta en un menor consumo de memoria y una mayor eficiencia en el acceso a datos.

- **Comparación con otras estructuras:**  
  Aunque los heaps se inventaron para superar ciertas limitaciones de los arreglos y para evitar punteros innecesarios en árboles, su implementación en arreglo aprovecha la localidad de memoria. Esto contrasta con árboles binarios implementados con punteros, que pueden sufrir de una mayor latencia debido a la dispersión de datos en la memoria. La elección entre un heap y otras estructuras (como árboles de búsqueda binaria o listas enlazadas) depende del uso específico, pero en escenarios de colas de prioridad, el heap ofrece una solución optimizada tanto en términos de espacio como de tiempo.

- **Eficiencia amortizada vs. peor caso:**  
  Es relevante distinguir entre la eficiencia en el peor caso y la eficiencia amortizada. Por ejemplo, la operación de inserción en un arreglo dinámico puede requerir una redimensión que, en el peor caso, tenga un costo mayor; sin embargo, este costo se distribuye a lo largo de múltiples operaciones, haciendo que la complejidad amortizada se mantenga en \( O(\log(n)) \). Este aspecto es fundamental al evaluar la aplicabilidad del heap en sistemas con altos volúmenes de datos.

- **Uso de estructuras auxiliares:**  
  En la operación update, la búsqueda del elemento a actualizar puede ser costosa si se realiza de forma lineal. Para mejorar este rendimiento, se recomienda la utilización de estructuras auxiliares (por ejemplo, tablas hash) que asocien cada elemento con su índice en el arreglo. De esta forma, se puede alcanzar una búsqueda en tiempo constante, lo que permite que la actualización global se mantenga eficiente incluso en heaps de gran tamaño.

