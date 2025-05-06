### Treaps: Usando la aleatorización para balancear árboles binarios de búsqueda

Hemos visto cómo es posible almacenar elementos y recuperarlos basándonos en sus prioridades utilizando heap, y cómo podemos mejorar sobre los  heap binarios usando un factor de ramificación mayor.

Las colas de prioridad son especialmente útiles cuando necesitamos consumir elementos en un cierto orden en una lista que cambia dinámicamente (por ejemplo, la lista de tareas de una CPU). Con una cola de prioridad, en cada instante podemos obtener el siguiente elemento según un criterio, removerlo de la lista y, generalmente, no preocuparnos por reordenar los demás elementos.  
  
La diferencia con una lista ordenada es que en la cola de prioridad cada elemento se recorre una sola vez, ya que, al removido, ya no inciden en el ordenamiento.

Sin embargo, si se requiere hacer seguimiento del orden de los elementos, o recorrerlos varias veces (como cuando se renderiza una lista de objetos en una página web), una cola de prioridad podría no ser la opción idónea. Además, a veces se necesitan operaciones adicionales:  

- Recuperar de forma eficiente el elemento mínimo o máximo de la colección.  
- Acceder al _i_-ésimo elemento sin tener que remover todos los anteriores.  
- Encontrar el predecesor o sucesor de un elemento dentro del ordenamiento.

En estos casos, los árboles (especialmente los árboles binarios de búsqueda) se presentan como el mejor compromiso, ya que si el árbol está balanceado, la inserción, eliminación y búsqueda (además de obtener el mínimo y el máximo) se realizan en tiempo logarítmico.

El problema surge porque, en general, los árboles binarios no garantizan el balanceo; dependiendo del orden de inserción se pueden generar árboles muy balanceados o muy sesgados.


#### Problema: Multi-indexación

Imagina que tu familia tiene una pequeña tienda de comestibles y deseas ayudar a tus padres a llevar el inventario. Para sorprenderlos y demostrar el valor de la informática, decides diseñar una herramienta digital de gestión de inventarios que cumpla dos requisitos fundamentales:

- **Búsqueda eficiente:** Poder buscar productos por nombre para actualizar el stock.
- **Atención prioritaria:** Obtener, en cualquier momento, el producto con la menor cantidad de existencias para planificar el próximo pedido.

Aunque podrías utilizar una hoja de cálculo predefinida, el verdadero reto y diversión radica en diseñar una estructura de datos en memoria que permita consultas según dos criterios diferentes.

En el mundo real, los escenarios pueden ser aún más complejos. Por ejemplo, cada producto podría requerir diferentes tiempos de envío, agruparse según el proveedor para reducir costos, variar de precio a lo largo del tiempo o incluso estar indisponible temporalmente. Toda esta complejidad se puede capturar en una función heurística, que se utiliza en lugar del mero recuento de inventario.

Una solución ingenua podría consistir en usar dos estructuras de datos distintas:  

- Una tabla hash para la búsqueda eficiente por nombre.  
- Una cola de prioridad para identificar el artículo a reabastecer.

Sin embargo, esto implica coordinar dos contenedores y, probablemente, duplicar el uso de memoria. ¿No sería ideal disponer de una única estructura de datos que maneje ambos aspectos de forma nativa y eficiente?

#### La esencia de la solución

El objetivo no es solo optimizar todas las operaciones en un contenedor, sino manejar entradas que tienen dos partes "medibles":  
- **Clave:** Por ejemplo, el nombre del producto, que se puede ordenar alfabéticamente.  
- **Prioridad:** La cantidad en stock, que permite comparar qué productos son más escasos y requieren atención inmediata.

Si ordenamos las entradas por nombre, para encontrar un producto según el stock se necesitaría escanear toda la lista. En cambio, un heap mínimo permite acceder rápidamente al producto con menor stock, pero dificulta la búsqueda por nombre.

Por ello, ninguna de las estructuras tradicionales (ni la cola de prioridad ni los árboles simples) es suficiente para resolver este desafío por sí sola.

#### API y contrato para SortedPriorityQueue

Se define una estructura de datos abstracta (ADT) que fusiona las propiedades de ambos contenedores:

```
class SortedPriorityQueue { 
    top() -> element 
    peek() -> element 
    insert(element, priority) 
    remove(element) 
    update(element, newPriority) 
    contains(element) 
    min() 
    max() 
}
```

- **Contrato:**  
  Las entradas se mantienen ordenadas por la clave, pero en cualquier momento los métodos `top()` y `peek()` devuelven el elemento con la mayor prioridad (por ejemplo, el producto más escaso).  
  Se añaden nuevos métodos que permiten buscar una clave dada y recuperar la clave mínima o máxima.

Esta estructura se puede pensar como una fusión entre heaps y listas enlazadas, que reúne las ventajas de ambas.

### Treap: La fusión de un árbol y un heap

El término _treap_ es un acrónimo de _tree_ (árbol) y _heap_.  
- **Árboles binarios de búsqueda (BST):** Ofrecen un rendimiento promedio excelente en operaciones de inserción, eliminación y búsqueda (además de obtener mínimo y máximo).  
- **Heaps:** Permiten llevar un registro eficiente de las prioridades usando una estructura similar a la de un árbol.

Dado que un heap binario es a su vez un árbol binario, surge la idea de fusionar ambas estructuras. No obstante, existe una dificultad teórica: para un conjunto de datos unidimensional no es posible imponer simultáneamente la invariante del BST y la del heap. Es decir, debemos elegir entre:  

1. **Restricción horizontal:**  
   Para un nodo _N_ con hijos _L_ (izquierdo) y _R_ (derecho), todas las claves en el subárbol izquierdo deben ser menores que la clave de _N_ y todas las claves del subárbol derecho mayores.
2. **Restricción vertical:**  
   La clave en la raíz de cualquier subárbol debe ser la menor del subárbol (como en un heap mínimo).

En nuestro caso, cada entrada tiene dos valores (nombre y cantidad en stock), lo que permite imponer:

- La restricción del BST sobre los nombres (estableciendo un orden total de izquierda a derecha).  
- La restricción del heap sobre las cantidades (estableciendo un orden jerárquico vertical en el que cada nodo hijo tiene un stock mayor que su padre, sin un orden específico entre hermanos).

De esta forma, se obtiene una estructura que permite búsquedas eficientes por nombre y, además, el acceso rápido al elemento con mayor prioridad (el producto más escaso), que siempre estará en la raíz.

Sin embargo, extraer el elemento superior no resulta tan sencillo como en un heap tradicional, pues se debe respetar también la invariante del BST. Asimismo, al insertar o eliminar un nodo, no basta con utilizar el algoritmo clásico del BST: una inserción basada únicamente en la posición correcta de la clave mantendría la propiedad del BST, pero podría violar las restricciones del heap sobre la prioridad.

#### Implementación del treap

A continuación se muestra un ejemplo de cómo podría implementarse la estructura principal del treap. Se utiliza una clase auxiliar para modelar los nodos, en la que cada nodo almacena:  
- Una **clave** (por ejemplo, el nombre del producto).  
- Una **prioridad** (en nuestro caso, la cantidad en stock; se asume un valor de tipo _double_, aunque otros tipos pueden funcionar si tienen un orden total).  
- Punteros (o referencias) a sus dos hijos (`left` y `right`) y a su padre.

**Clase Treap**

```
class Node { 
    key 
    // type double 
    priority 
  
    // type Node 
    left 
    // type Node 
    right 
    // type Node 
    parent 
  
    function Node(key, priority)  { 
        (this.key, this.priority) ← (key, priority) 
        this.left ← null 
        this.right ← null 
        this.parent ← null 
    } 
  
    function setLeft(node)  { 
        this.left ← node 
        if (node != null) then 
            node.parent ← this 
    } 
} 
  
class Treap { 
    // type Node 
    root 
  
    function Treap() { 
        root ← null 
    } 
}
```

- **Constructor de Node:**  
  Establece la clave y la prioridad basándose en los argumentos recibidos, y asigna `null` a los enlaces de los hijos y del padre.
  
- **Método setLeft:**  
  Asigna el nodo proporcionado como hijo izquierdo y, si éste no es `null`, actualiza también la referencia del padre. (Existe un método `setRight` similar, que no se muestra por cuestiones de espacio).


En esta implementación, la clase **Treap** es en su mayoría un contenedor para la raíz del árbol real, cada nodo del árbol posee dos atributos: una **clave** (que puede ser de cualquier tipo, siempre y cuando exista un orden total definido sobre los posibles valores) y una **prioridad**, que en este caso asumimos es un número de doble precisión (aunque también podría usarse un entero o cualquier tipo que defina un orden total, se ha observado que un double puede funcionar mejor).

Además, los nodos contendrán punteros (o referencias) a dos hijos, **left** y **right**, y a su **padre**.  

El constructor de un nodo simplemente establecerá los atributos de clave y prioridad a partir de sus argumentos e inicializará los punteros **left** y **right** a *null*, creando efectivamente una hoja. Las dos ramas pueden configurarse después de la construcción o, alternativamente, se puede proporcionar una versión sobrecargada del constructor que también reciba los dos hijos.


#### Rotaciones

Existe una operación en los árboles binarios de búsqueda que puede ayudarnos: **las rotaciones**. Esta operación es común en muchas estructuras de BST (como los árboles rojo-negro o los árboles 2-3) y consiste en transformar la relación entre dos nodos adyacentes, invirtiendo la relación padre-hijo entre ellos.

En una rotación queremos que el nodo hijo se convierta en el nodo padre y viceversa, pero no basta con intercambiar los dos nodos, ya que hacerlo de manera directa podría violar el ordenamiento de claves. Lo que se debe hacer es remover parte del subárbol y reestructurar las conexiones: se retira el subárbol con raíz en el nodo padre, se reemplaza con el (más pequeño) subárbol con raíz en el hijo y luego se reconectan los nodos removidos en este nuevo subárbol, de modo que se mantenga la propiedad del BST.

Para ello es necesario distinguir dos casos, según se trate de un hijo izquierdo o de un hijo derecho. Aunque son simétricos, se explicará principalmente el caso en el que el nodo hijo es el izquierdo.

A continuación se muestran los pseudocódigos para las rotaciones a la **derecha** y a la **izquierda**, junto con una explicación detallada de cada paso.


**Rotación a la derecha**

```
function rightRotate(treap, x) 
    if x == null or isRoot(x) then  
        throw 
    y ← x.parent 
    throw - if y.left != x  
    p ← y.parent 
    if p != null then  
        if p.left == y then  
            p.setLeft(x) 
        else 
            p.setRight(x) 
    else 
        treap.root ← x 
    y.setLeft(x.right) 
    x.setRight(y) 
```

**Explicación de cada paso:**

- El método `rightRotate` recibe un nodo del treap, `x`, y realiza una rotación a la derecha. No retorna nada, pero modifica la estructura del treap.  
- Se verifica si `x` es *null* o si es la raíz del árbol. En cualquiera de esos casos, se produce un error; se podría optar por retornar sin hacer nada, pero generalmente es preferible lanzar una excepción. La función `isRoot` debe implementarse verificando si el nodo carece de padre.  
- Se obtiene el padre de `x` y se asigna a la variable `y`. Dado que `x` no es la raíz, `y` no será *null*.  
- Sólo es posible realizar una rotación a la derecha si `x` es el hijo izquierdo de `y`. Si no es así (es decir, si `x` es el hijo derecho), se produce un error.  
- Se obtiene el padre de `y` y se asigna a la variable `p`, para facilitar la actualización de enlaces.  
- Se comprueba si `p` es *null* o no, ya que se debe actualizar el enlace desde `p` a `y` según corresponda.  
- Dado que `p` no es *null*, se determina si `y` es el hijo izquierdo o derecho de `p`, para saber qué enlace actualizar.  
- Se actualiza el enlace en `p`, sustituyendo a `y` por `x` como hijo, mediante los métodos `setLeft` o `setRight` que se encargan de mantener la integridad de los enlaces (incluyendo la actualización de los punteros de padre en los nodos involucrados).  
- Si `p` es *null*, significa que `y` era la raíz del treap y, por lo tanto, se actualiza la raíz del treap asignando `x` como nuevo nodo raíz.  
- Una vez que `x` ha sido conectado al árbol (como hijo de `p` o como nueva raíz), se actualiza el subárbol izquierdo de `y`. Específicamente, se asigna el subárbol derecho de `x` como el nuevo subárbol izquierdo de `y`.  
- Finalmente, se reconecta `y` al árbol configurándolo como el nuevo hijo derecho de `x`.

En resumen, lo que se logra es remover a `y` de su posición original y actualizar los enlaces de forma que `x` asuma el lugar de `y` en la jerarquía, preservando la propiedad de búsqueda del árbol.

**Rotación a la izquierda**

```
function leftRotate(treap, x) 
    if x == null or isRoot(x) then
        throw 
    y ← x.parent 
    throw - if y.right != x  
    p ← y.parent 
    if p != null then 
        if p.left == y then  
            p.setLeft(x) 
        else 
            p.setRight(x) 
    else 
        treap.root ← x 
    y.setRight(x.left)  
    x.setLeft(y) 
```

**Explicación de cada paso:**

- El método `leftRotate` toma un nodo del treap, `x`, y realiza una rotación a la izquierda. La función tiene efectos secundarios sobre la estructura del treap y no retorna ningún valor.  
- Se verifica si `x` es *null* o si es la raíz del árbol, lo cual impediría efectuar la rotación, por lo que se lanza una excepción en esos casos.  
- Se asigna a la variable `y` el padre de `x`, con la seguridad de que `y` no será *null*.  
- Para poder realizar una rotación a la izquierda, es necesario que `x` sea el hijo derecho de `y`. Si no es así (es decir, si `x` es el hijo izquierdo), se produce un error.  
- Se obtiene el padre de `y` y se guarda en la variable `p` para facilitar la actualización de enlaces.  
- Se comprueba si `p` es *null* o no, para determinar la necesidad de actualizar el enlace desde el padre de `y`.  
- Si `p` no es *null*, se determina si `y` es hijo izquierdo o derecho de `p` para actualizar el enlace correspondiente.  
- Se actualiza el enlace desde `p` reemplazando a `y` por `x` utilizando los métodos `setLeft` o `setRight`, según corresponda.  
- Si `p` es *null*, significa que `y` era la raíz del treap y se actualiza la raíz del treap asignando `x` como nueva raíz.  
- Se actualiza el subárbol derecho de `y` para que apunte al antiguo subárbol izquierdo de `x`.  
- Finalmente, se reconecta a `y` al árbol configurándolo como el nuevo hijo izquierdo de `x`.

En este caso, tras realizar la rotación a la izquierda, `x` asume la posición del padre `y` y, de esta forma, se reorganizan los nodos para mantener la propiedad de búsqueda en el árbol.

**Observaciones**

- La operación de **rotación** se puede interpretar de manera intuitiva como el hecho de "pivotar" la estructura del árbol sobre un nodo específico. Por ejemplo, al aplicar una rotación a la derecha sobre el nodo `X` (que es hijo izquierdo de `Y`), se consigue que `X` suba en la jerarquía y que `Y` pase a ser hijo derecho de `X`.  
- Al efectuar la rotación se actualizan ciertos enlaces: el enlace entre padre e hijo se invierte y se transfiere parte del subárbol (en estos casos, el subárbol derecho de `X` o el subárbol izquierdo de `X`, según la rotación) para garantizar que el árbol resultante sigue cumpliendo la propiedad de que para cada nodo, todas las claves en el subárbol izquierdo son menores (o iguales) y las del subárbol derecho son mayores.  
- Es importante notar que las rotaciones siempre preservan las restricciones propias de un árbol binario de búsqueda (BST). Sin embargo, en el caso de los **treaps**, aunque las rotaciones se usan para reparar violaciones en la estructura (especialmente cuando se alteran las prioridades), una rotación aplicada a un árbol que ya es un BST válido podría romper las invarianzas del heap que se basan en las prioridades de los nodos.


#### Algunas preguntas de diseño

Los treaps son, en esencia, heaps que además son árboles binarios de búsqueda. Recordamos que los heaps pueden implementarse utilizando arrays, lo que ofrece una representación más eficiente en espacio y aprovecha la localidad de referencia.

**¿Podemos implementar un treap usando un array?**  
Es importante analizar los pros y los contras de usar un array frente a un árbol y considerar cuáles podrían ser los puntos críticos de esta elección.


#### Representación en array vs. árbol

Uno de los problemas fundamentales con la representación en array es su falta de flexibilidad. Esta solución funciona muy bien si solo intercambiamos elementos al azar y agregamos o removemos exclusivamente desde el final del array. Sin embargo, si necesitamos mover elementos en posiciones intermedias, se complica notablemente:  

- **Inserciones en medio del array:** Al insertar un nuevo elemento en medio, todos los elementos posteriores deben desplazarse, lo que implica un costo promedio de *O(n)* asignaciones.
  
Los heaps, al ser árboles completos, balanceados y alineados a la izquierda, se benefician de esta representación en array. Esto es posible porque los heaps no mantienen un orden total sobre sus claves, por lo que es viable agregar y eliminar elementos desde el final del array y, a continuación, reacomodar únicamente el elemento afectado para restablecer las propiedades del heap.

Por otro lado, los treaps son árboles binarios de búsqueda y, por lo tanto, deben mantener un orden total en las claves. Esto requiere que se realicen rotaciones al insertar o eliminar elementos, operando sobre subárboles completos. Dichas operaciones, que consisten en mover un subárbol (por ejemplo, el subárbol derecho de un nodo X) al subárbol izquierdo de su padre Y (o viceversa), se ejecutan en tiempo constante cuando se usan punteros en los nodos. En cambio, si se intentara llevar a cabo este tipo de reestructuración en un array, la operación resultaría en un proceso costoso en tiempo lineal. Por ello, la representación en array no es práctica para treaps ni para árboles binarios de búsqueda.

#### Consideración del factor de ramificación

Otra cuestión de diseño relevante es el factor de ramificación para el heap. Anteriormente se vio que los heaps pueden tener factores de ramificación distintos de 2, y se demostró que, en algunas aplicaciones, un heap con un factor de ramificación de 4 o superior puede superar al heap binario.

**¿Podríamos implementar un treap con un factor de ramificación mayor que 2?**  

La respuesta no es sencilla. Dado que estamos utilizando árboles binarios de búsqueda, un árbol con factor de ramificación diferente de 2 resultaría incompatible; de hecho, si el factor de ramificación del heap no coincide con el del árbol de búsqueda, se crearían serios problemas en la estructura.

Aunque se pudiera considerar la idea de usar árboles de búsqueda ternarios o su generalización, esto complicaría enormemente las operaciones de rotación. Con ello, el código de la implementación se volvería más complejo y desordenado, lo que probablemente incidiría en un peor rendimiento. Además, mantener el árbol balanceado se volvería más difícil, salvo que se optase por estructuras específicamente diseñadas para ello (como un árbol 2-3, que ya garantiza el balanceo desde su construcción).
