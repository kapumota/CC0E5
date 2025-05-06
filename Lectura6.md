### Operaciones en heaps: PushDown, Insert, Top y Update

El manejo eficiente de un heap requiere el uso de operaciones auxiliares que garanticen el mantenimiento de las propiedades estructurales y de prioridad definidas para la estructura. Entre estas operaciones se destacan dos métodos básicos: uno que mueve un elemento hacia arriba (bubbleUp, tratado en otra sección) y otro que lo desplaza hacia abajo (pushDown). 

Además, se cuenta con operaciones que permiten la inserción de nuevos elementos, la extracción del elemento superior y la actualización de la prioridad de un elemento existente. A continuación se presentan en detalle las operaciones **pushDown**, **insert**, **top** y **update**.

#### Operación pushDown

El método **pushDown** se utiliza cuando un elemento, al haber sufrido una modificación o tras la eliminación de la raíz, podría violar la invariante de prioridad en relación con sus hijos. Aunque el elemento modificado mantenga la propiedad respecto a su padre, es posible que, al compararlo con sus hijos, se encuentre que alguno de ellos posee una prioridad superior. 

Esto ocurre, por ejemplo, cuando se extrae la raíz del heap y se reemplaza con el último elemento del arreglo o cuando se disminuye la prioridad de un nodo. La función pushDown garantiza que, moviendo el elemento hacia abajo, se restablezca el orden del heap.

**Pseudocódigo del método pushDown**

```pseudo
function pushDown(pairs, index=0)
  currentIndex <- index
  while currentIndex < firstLeafIndex(pairs) do
    (child, childIndex) <- highestPriorityChild(currentIndex)
    if child.priority > pairs[currentIndex].priority then
      swap(pairs, currentIndex, childIndex)
      currentIndex <- childIndex
    else
      break
```

**Explicación línea por línea**

- Se inicia estableciendo el índice actual en el valor de entrada (por defecto 0, que corresponde a la raíz del heap).  
- Se continúa iterando mientras el índice actual sea menor que el índice de la primera hoja, ya que las hojas no tienen hijos y no es necesario reubicarlas.  
- En cada iteración se identifica cuál de los hijos del nodo actual tiene la mayor prioridad mediante la función `highestPriorityChild`.  
- Si el hijo identificado tiene una prioridad mayor que el nodo actual, se procede a intercambiar ambos elementos y se actualiza el índice actual para continuar evaluando el nodo en su nueva posición.  
- Si no se cumple la condición de intercambio, se termina el proceso, ya que el nodo se encuentra en la posición adecuada.

**Versión optimizada de pushDown**

Esta versión evita intercambios innecesarios. En lugar de realizar un intercambio en cada iteración, se guarda el elemento actual en una variable temporal y se "mueven" los hijos de mayor prioridad hacia arriba hasta encontrar el sitio correcto para insertar el elemento.

```pseudo
function pushDown(pairs, index=0)
  current <- pairs[index]
  while index < firstLeafIndex(pairs) do
    (child, childIndex) <- highestPriorityChild(index)
    if child.priority > current.priority then
      pairs[index] <- pairs[childIndex]
      index <- childIndex
    else
      break
  pairs[index] <- current
```

En esta versión, se almacena en `current` el elemento a reubicar. Durante la iteración, si se detecta que un hijo tiene mayor prioridad que `current`, se mueve ese hijo hacia la posición actual y se actualiza el índice. Cuando ya no se cumple la condición, se coloca `current` en su posición definitiva, evitando múltiples intercambios y reduciendo el número de asignaciones.

#### Operación de inserción (insertar)

La operación de inserción permite agregar un nuevo elemento al heap, manteniendo las propiedades estructurales y de prioridad. Inicialmente, el nuevo elemento se añade al final del arreglo que representa el heap, lo que preserva la propiedad de completitud. No obstante, es posible que este nuevo elemento viole la invariante de prioridad (por ejemplo, en un max-heap, si tiene una prioridad mayor que la de su padre). Por ello, se utiliza la función **bubbleUp** para desplazar el elemento hacia arriba hasta su posición correcta.

**Pseudocódigo para la inserción**

```pseudo
function insert(element, priority)
  p <- Pair(element, priority)
  pairs.append(p)
  bubbleUp(pairs, |pairs| - 1)
```

**Explicación del proceso**

- Se crea una estructura que asocia el elemento con su prioridad.  
- Este par se añade al final del arreglo, manteniendo la propiedad de árbol completo.  
- Finalmente, se invoca la función **bubbleUp** con el índice del nuevo elemento, para desplazarlo hacia arriba y restaurar la invariante de prioridad.

La complejidad de esta operación depende de la altura del heap, siendo logarítmica en función del número de elementos.

#### Operación top (extracción del elemento superior)

El método **top** extrae el elemento superior del heap, es decir, el de mayor (o menor, en un min-heap) prioridad. Esta operación es fundamental para el uso de colas de prioridad, ya que permite obtener de forma eficiente el elemento "más importante". Al extraer la raíz, se genera un "hueco" que debe ser rellenado para mantener la estructura y la invariante del heap.

**Pseudocódigo del método top**

```pseudo
function top()
  if pairs.isEmpty() then error()
  p <- pairs.removeLast()
  if pairs.isEmpty() then
    return p.element
  else  
    (element, priority) <- pairs[0]
    pairs[0] <- p
    pushDown(pairs, 0)
    return element
```

**Explicación detallada**

- Se verifica que el heap no esté vacío; de lo contrario, se lanza un error.  
- Se elimina el último elemento del arreglo y se almacena en una variable temporal.  
- Si, tras esta eliminación, el arreglo queda vacío (lo que sucede cuando solo había un elemento), se retorna directamente ese elemento.  
- Si aún quedan elementos, se almacena el contenido de la raíz y se reemplaza con el último elemento extraído.  
- Se llama a **pushDown** para reubicar el nuevo elemento en la raíz, asegurando que se mantenga la invariante del heap.  
- Finalmente, se retorna el elemento original de la raíz.

Debido a que tanto la eliminación del último elemento como la operación pushDown son logarítmicas, la complejidad total de top() es ` O(log_D(n)) ` en el peor de los casos.

#### Operación update (actualización de prioridad)

El método **update** permite modificar la prioridad de un elemento ya existente en el heap. Esta operación es especialmente útil en escenarios donde las prioridades pueden cambiar en función de eventos externos o del progreso de ciertos procesos. Al actualizar la prioridad, el elemento podría quedar desubicado, por lo que es necesario aplicar bubbleUp o pushDown según convenga.

**Pseudocódigo del método update**

```pseudo
function update(oldValue, newPriority)
  index <- pairs.find(oldValue)
  if index ≥ 0 then
    oldPriority <- pairs[index].priority
    pairs[index] <- Pair(oldValue, newPriority)
    if (newPriority < oldPriority) then
      bubbleUp(pairs, index)
    elsif (newPriority > oldPriority) then        
      pushDown(pairs, index)
```

**Desglose del proceso**

- Se localiza la posición del elemento a actualizar mediante la función `pairs.find(oldValue)`.  
- Si el elemento se encuentra, se almacena su prioridad antigua y se actualiza el par con la nueva prioridad.  
- Se compara la nueva prioridad con la antigua:  
  - Si la nueva prioridad es menor (en un max-heap, esto indica que el elemento podría estar demasiado alto), se invoca **bubbleUp** para moverlo hacia arriba.  
  - Si la nueva prioridad es mayor, se utiliza **pushDown** para desplazar el elemento hacia abajo y restaurar el orden correcto.
  
El rendimiento de esta operación depende, en primer lugar, de la eficiencia en la búsqueda del elemento a actualizar. En implementaciones simples esta búsqueda puede ser lineal; sin embargo, es común emplear estructuras auxiliares (como un mapa hash) para lograr búsquedas en tiempo amortizado O(1). Además, las funciones bubbleUp y pushDown, que se aplican después de la actualización, tienen una complejidad logarítmica.

#### Manejo de duplicados

Hasta ahora hemos asumido que nuestro heap no contiene duplicados. Sin embargo, si esta suposición no se cumple, debemos enfrentar desafíos adicionales, en particular, definir el orden a seguir cuando existan elementos duplicados.

**El problema**

Considera el siguiente escenario:  
- Tenemos dos duplicados, a los que llamaremos **X** e **Y**, siendo uno hijo del otro.  
- Supongamos que **X** es hijo de **Y** y se llama al método `update` para aumentar la prioridad de **X**.

Dentro de `update`, después de ajustar las prioridades de ambos elementos, se deben ejecutar dos llamadas a `bubbleUp`: una para **X** y otra para **Y**.  
Si se ejecutan en el orden incorrecto, podría generarse un heap inconsistente, violando las propiedades fundamentales de la estructura.

**Ejemplo del problema**

- **Caso 1:**  
  Se hace llamar `bubbleUp(X)` primero.  
  - **X**, al compararse con su padre **Y**, encuentra que ambos tienen el mismo valor (o que **Y** no cumple la condición para intercambiarse) y se detiene.  
  - Posteriormente, al llamar `bubbleUp(Y)`, se descubre que el padre de **Y** tiene una prioridad menor, lo que hace que **Y** ascienda.  
  - Como consecuencia, **X** no se vuelve a reexaminar y permanece en una posición incorrecta, dejando el heap fuera de balance.

**Posibles soluciones**

- **Orden de llamadas:**  
  Ejecutar las llamadas a `bubbleUp` siguiendo un orden de izquierda a derecha garantiza que, al actualizar cada nodo, se verifiquen las relaciones padre-hijo de forma consistente.

- **Ajuste de condiciones:**  
  Modificar las condiciones en `bubbleUp` y en el método complementario `pushDown` para detener el proceso solo cuando se encuentre:
  - Un padre con una prioridad **estrictamente mayor** (y, respectivamente, hijos con prioridad **estrictamente menor**).

- **Actualización dinámica:**  
  Permitir que los nodos se ajusten (ascendiendo o descendiendo) conforme se actualizan.  
  Esta alternativa, aunque posible, generalmente implica un mayor número de intercambios y puede afectar el rendimiento en el peor de los casos.

#### Heapify

La inicialización de un heap puede realizarse de dos formas:

1. **Inserción secuencial:**  Crear un heap vacío y añadir los elementos uno por uno, lo que tiene una complejidad de `O(nlog n)`.

2. **Heapify directo:**  Inicializar el heap con el conjunto completo de n elementos en cualquier orden y luego reorganizar el arreglo para cumplir las propiedades del heap.

**Concepto y procedimiento**

Cada posición del arreglo se puede considerar la raíz de un subheap. Las hojas son subheaps triviales (con un solo elemento) y, por lo tanto, ya cumplen la propiedad del heap.

**Pseudocódigo de método heapify**

```pseudo
function heapify(pairs)
  for index in { (|pairs| - 1) / D  ..  0 } do     
    pushDown(pairs, index)
```

- **D:** Factor de ramificación (por ejemplo, `D = 2` para un heap binario).  
- **pushDown:** Se encarga de asegurar que el subheap con raíz en el índice dado sea un heap válido.

**Análisis del tiempo de ejecución**

En un heap binario:
- Aproximadamente la mitad de los nodos son hojas, las cuales requieren a lo sumo un intercambio.
- Los subheaps de mayor altura (más cercanos a la raíz) requieren más intercambios, pero su número es menor.

El análisis completo muestra que el número total de intercambios está limitado por una serie geométrica. Esto implica que, en el peor de los casos, la complejidad de `heapify` es **O(n)**.

#### Más allá de la API: verificación de existencia (*contains*)

Una de las operaciones para las que los heaps no están optimizados es la verificación de si un elemento se encuentra en la estructura. Sin una estrategia adicional, se requiere recorrer todo el arreglo, lo que implica una complejidad **O(n)**.

**Soporte para incrementos/decrementos de prioridad**

En aplicaciones donde es fundamental modificar la prioridad de un elemento de manera eficiente, se sugiere:
- Agregar un campo auxiliar (por ejemplo, un **HashMap**) que mapea cada elemento a su posición en el heap.  
- Esto permite que la operación `contains` (y la búsqueda de la posición del elemento) se realice en tiempo constante, en promedio.

**Pseudocódigo del método contains**

```pseudo
function contains(elem)
  index <- elementToIndex[elem]
  return index >= 0
```

**Supuestos:**
- `elementToIndex[elem]` retorna -1 por defecto si el elemento no se encuentra.
- No se permiten claves duplicadas. Si existieran duplicados, se debería almacenar una lista de índices por cada clave.


#### Rendimiento

Se resumen a continuación las operaciones principales de un heap, sus tiempos de ejecución y el espacio extra requerido:

**Tabla: operaciones en heaps (con `n` elementos)

| Operación         | Tiempo de ejecución | Espacio extra     |
| ----------------- | ------------------- | ----------------- |
| **Insertar**      | O(log n)            | O(1)              |
| **Top**           | O(log n)            | O(1)              |
| **Remover**       | O(log n)¹           | O(n)¹             |
| **Peek**          | O(1)                | O(1)              |
| **Contains (ingenuo)** | O(n)          | O(1)              |
| **Contains (avanzado)** | O(1)¹         | O(n)¹             |
| **UpdatePriority**| O(log n)¹           | O(n)¹             |
| **Heapify**       | O(n)                | O(1)              |

¹ Usando la versión avanzada de `contains` y manteniendo un mapa extra de elementos a índices.

#### Consideraciones de tiempo y espacio

- **Trade-off entre tiempo y espacio:**  Algoritmos que consumen espacio cuadrático pueden ser aceptables para volúmenes pequeños, pero en escenarios con grandes volúmenes de datos (big data), es preferible utilizar algoritmos que requieran espacio constante o logarítmico.

- **Garantías amortizadas:**  Para operaciones como `insert` y `top`, si se utiliza un arreglo dinámico, algunas llamadas pueden requerir tiempo lineal durante la redimensión. Sin embargo, se garantiza que, en promedio, el rendimiento es logarítmico.

- **Importancia de una estructura auxiliar:**  El rendimiento de `remove` y `updatePriority` depende de una implementación eficiente de `contains`. Esto generalmente requiere una segunda estructura de datos (por ejemplo, una tabla hash o un filtro Bloom) para lograr búsquedas eficientes.

- **Optimización en lenguajes gestionados:**  En lenguajes como Java, se recomienda inicializar los heaps a un tamaño esperado si se tiene una estimación razonable, para evitar costosos redimensionamientos y mejorar la eficiencia en la asignación y recolección de basura.

#### Integración de las operaciones en la API del Heap

Con las funciones auxiliares bubbleUp y pushDown bien definidas, las operaciones principales del heap (insert, top y update) se simplifican considerablemente. Cada operación se apoya en estas funciones para garantizar que, tras cualquier modificación (ya sea la adición, extracción o actualización de un elemento), las propiedades del heap se mantengan sin violaciones:

- **Inserción:** Se añade el nuevo elemento al final del arreglo y se llama a bubbleUp para posicionarlo correctamente.  
- **Extracción (top):** Se elimina la raíz, se reemplaza por el último elemento y se ajusta su posición mediante pushDown.  
- **Actualización:** Se modifica la prioridad de un elemento y, en función del cambio, se utiliza bubbleUp o pushDown para reubicarlo correctamente.

El diseño modular de estas operaciones facilita la adaptación del heap a diferentes requerimientos. Por ejemplo, la distinción entre max-heap y min-heap puede lograrse variando las condiciones de comparación en bubbleUp y pushDown o ajustando la función de prioridad, sin modificar la estructura base del código.

La implementación compacta del heap, basada en un arreglo, permite que la asignación de memoria sea contigua, favoreciendo la localidad de referencia y, en consecuencia, mejorando la eficiencia en el acceso a los elementos.

#### Consideraciones adicionales sobre la manipulación del heap

**Manejo del tamaño del arreglo**

En la implementación práctica es fundamental el manejo del arreglo que almacena los pares (elemento, prioridad). Dependiendo del lenguaje y la estructura de datos utilizada, el arreglo puede ser estático o dinámico:
- En un **arreglo estático** se define un tamaño máximo al crearlo, limitando el número de elementos pero garantizando que las operaciones se realicen en tiempo logarítmico.  
- En un **arreglo dinámico** el tamaño se redimensiona automáticamente conforme se agregan elementos. Aunque la redimensión puede implicar un costo momentáneo, este se distribuye de forma amortizada, manteniendo la eficiencia global.

**Impacto del factor de ramificación**

La complejidad de las operaciones en un heap también depende del factor de ramificación `D`. En un heap binario (`D = 2`) se realizan menos comparaciones por nivel, mientras que en un heap d-ario (` D > 2 `) se evalúan más hijos en cada iteración, lo que puede aumentar el número de comparaciones en pushDown. Sin embargo, al aumentar `D` se reduce la altura del heap, lo que puede compensar el mayor número de comparaciones. La elección del factor de ramificación es, por tanto, un equilibrio entre el número de comparaciones por nodo y la profundidad del árbol.

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
El ahorro obtenido al optimizar estas operaciones, reduciendo el número de asignaciones mediante el uso de variables temporales y evitando intercambios innecesarios– se traduce en una mejora significativa del rendimiento en escenarios con un alto volumen de datos. Además, la posibilidad de mantener un índice actualizado de cada elemento, mediante estructuras auxiliares, permite que la operación update se ejecute en tiempo cercano al óptimo, incluso en implementaciones con arreglos dinámicos.

### Consistencia y el mantenimiento de la propiedad del heap

Cada una de las operaciones presentadas (pushDown, insert, top y update) se centra en mantener tres propiedades fundamentales del heap:

1. **Propiedad estructural:**  
   El heap debe representarse mediante un arreglo que corresponde a un árbol completo, donde todas las hojas están en el nivel más bajo o en el penúltimo, manteniendo un ajuste a la izquierda.

2. **Propiedad de prioridad:**  
   En un max-heap, cada nodo debe tener una prioridad mayor o igual que la de sus hijos; en un min-heap, la situación es la inversa. Las operaciones bubbleUp y pushDown se encargan de restablecer esta propiedad tras modificaciones en la estructura.

3. **Integridad del arreglo:**  
   La representación en arreglo del heap permite acceder de forma eficiente a los elementos. Las operaciones de inserción y eliminación se aprovechan de la facilidad para añadir o quitar elementos del final del arreglo, y se garantizan mediante métodos auxiliares que reubican el elemento modificado sin necesidad de redirigir punteros.

El correcto funcionamiento del heap depende de la coordinación entre estas propiedades y de la implementación modular de las operaciones. Cada cambio, ya sea la inserción de un nuevo elemento, la actualización de la prioridad de uno existente o la extracción del elemento superior– se realiza de forma que la estructura global se mantiene coherente y lista para futuras operaciones.

La combinación de estas técnicas permite que el heap actúe como una estructura de datos muy versátil y eficiente en contextos de alta demanda, donde la rapidez en la selección del elemento "más importante" es crucial. Además, la posibilidad de ajustar el criterio de prioridad de forma parametrizable hace que esta estructura se adapte a una amplia variedad de escenarios, sin necesidad de reescribir la lógica subyacente.
