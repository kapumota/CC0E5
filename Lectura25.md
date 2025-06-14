## **B-, B+ y los R-Tree**

En el ámbito de la gestión de datos a gran escala, la eficiencia de la búsqueda es un pilar fundamental. Cuando los conjuntos de datos no solo son masivos, sino que también poseen múltiples dimensiones, las estructuras de datos convencionales se vuelven insuficientes. 

Este análisis se sumerge en la mecánica interna de tres arquitecturas de datos avanzadas que han sido cruciales para superar estos desafíos: los **B-trees**, su variante optimizada los **B+trees**, y su generalización para el espacio multidimensional, los **R-trees**.


### **B-Trees y B+ Trees**

Para comprender las soluciones a problemas multidimensionales, primero es indispensable dominar los B-trees, ya que los R-trees son una evolución directa de sus principios. Desarrollados para optimizar el acceso a datos en dispositivos de almacenamiento secundario como los discos duros, donde los tiempos de acceso son órdenes de magnitud más lentos que en la memoria principal, su diseño se centra en minimizar las costosas operaciones de entrada/salida (E/S). Esto lo logran manteniendo una estructura de árbol ancha y perfectamente equilibrada.

#### **Invariantes cruciales de los B-Trees**

Un B-tree es un árbol de búsqueda autoequilibrado que extiende la idea de un árbol binario de búsqueda permitiendo que los nodos tengan un número variable de hijos. Sus propiedades o **invariantes** son las reglas que aseguran que el árbol permanezca balanceado, manteniendo una altura logarítmica que garantiza la eficiencia en todas sus operaciones.

1. **Factor de ramificación (`d`)**: Cada B-tree se define por un parámetro entero `d` ≥ 2, conocido como el *orden* o *grado mínimo*. Este valor determina la capacidad de almacenamiento de cada nodo.
2. **Capacidad de los nodos**: Con la excepción de la raíz, cada nodo en el árbol debe contener un mínimo de `d-1` claves y un máximo de `2d-1` claves. La raíz puede contener desde 1 hasta `2d-1` claves. Esta regla asegura que los nodos mantengan una ocupación saludable, evitando el desperdicio de espacio y las divisiones o fusiones demasiado frecuentes.
3. **Número de hijos**: Un nodo interno que alberga `m` claves debe tener precisamente `m+1` hijos. Esta es una consecuencia directa de cómo las claves organizan el espacio de búsqueda.
4. **Claves ordenadas**: Dentro de cada nodo, las claves se almacenan de forma estrictamente ordenada.
5. **Estructura jerárquica de cubárboles**: Las claves en un nodo interno funcionan como pivotes que dividen el universo de datos. Para un nodo con claves `k_0, k_1, ..., k_{m-1}` e hijos `C_0, C_1, ..., C_m`, se cumple que todas las claves en el subárbol `C_i` están acotadas por las claves `k_{i-1}` y `k_i` del nodo padre.
6. **Hojas al mismo nivel**: Todas las hojas del árbol deben residir en el mismo nivel. Esta propiedad es la que define al B-tree como **perfectamente equilibrado** en altura, lo que garantiza un tiempo de acceso uniforme para cualquier dato. La altura de un B-tree con `n` elementos es del orden de `O(log_d n)`.

#### **Ejemplo**

Sea un B-Tree de orden $d=3$ (es decir, cada nodo puede tener entre $d-1=2$ y $2d-1=5$ claves, salvo la raíz que admite también 1 clave). 

**1. Definición preliminar**

* **Orden mínimo** $d = 3$.
* Cada nodo (excepto la raíz) debe contener entre $d-1=2$ y $2d-1=5$ claves.
* La raíz puede tener entre 1 y $2d-1=5$ claves.
* Un nodo con $m$ claves tiene exactamente $m+1$ hijos (si no es hoja).
* Todas las hojas están al mismo nivel.


**2. Secuencia de inserciones**

Insertaremos, en este orden, las claves:

```
10, 20, 5, 6, 12, 30, 7, 17
```

y veremos cómo evoluciona el árbol.

**Insertar 10**

* Árbol vacío => la raíz es hoja.
* Después: raíz contiene $[10]$.

```
               [10]
(nivel 0, altura = 0)
```

> **Verificación de invariantes**
>
> * Raíz con 1 clave (está entre 1 y 5).
> * Sin hijos; nivel uniforme.

**Insertar 20**

* Raíz (hoja) pasa de $[10]$ a $[10,\,20]$.
* Sigue cumpliendo $1 ≤ claves ≤5$.

```
               [10 | 20]
```

**Insertar 5**

* Raíz sigue siendo hoja; ordenamos internamente -> $[5,\,10,\,20]$.
* Ahora $claves=3\le5$.

```
               [5 | 10 | 20]
```

**Insertar 6**

* Añadimos 6 y reordenamos -> $[5,\,6,\,10,\,20]$ ($=4\le5$).

```
           [5 | 6 | 10 | 20]
```

**Insertar 12**

* Añadimos 12 -> $[5,6,10,12,20]$ ($=5\le5$).

```
       [5 | 6 | 10 | 12 | 20]
```

**Insertar 30** -> **split** ("desbordamiento")

* Al agregar 30, la raíz tendría 6 claves $[5,6,10,12,20,30]$, lo cual excede $2d-1=5$.
* **Dividimos** el nodo en dos y promovemos la clave central:

  1. Clave central: el elemento en posición $d=3$ (contando desde 1) -> **10**.
  2. Nodo izquierdo: las dos primeras claves $[5,6]$.
  3. Nodo derecho: las dos últimas $[12,20,30]$.
  4. Nueva raíz: $[10]$ con dos hijos: izquierdo y derecho.

```
               [10]
              /    \
     [5 | 6]        [12 | 20 | 30]
  (hoja, nivel 1)    (hoja, nivel 1)
(nivel 0)               (altura 1)
```

> **Verificación tras split**
>
> * **Raíz**: 1 clave (entre 1 y 5).
> * Cada hijo (hoja) tiene 2 ó 3 claves (entre $d-1=2$ y $5$).
> * Raíz con $m=1$ clave -> tiene $m+1=2$ hijos.
> * Hojas al mismo nivel (nivel 1).


**Insertar 7**

* Comparamos con 10 -> va al subárbol izquierdo $[5,6]$.
* Inserción y reordenamiento -> $[5,\,6,\,7]$ ($=3$, válido).

```
               [10]
              /    \
        [5 | 6 | 7]  [12 | 20 | 30]
```

**Insertar 17**

* 17 > 10 -> subárbol derecho $[12,20,30]$.
* Inserción -> $[12,\,17,\,20,\,30]$ ($=4\le5$).

```
               [10]
              /    \
   [5 | 6 | 7]   [12 | 17 | 20 | 30]
```


**Comprobación final de todas las invariantes**

1. **Orden mínimo $d=3$**
   Definido desde el inicio.

2. **Capacidad de nodos**

   * **Raíz**: 1 clave ($1 ≤ 1 ≤ 5$).
   * **Hojas**:

     * Izquierda $[5,6,7]$: 3 claves ($2 ≤ 3 ≤ 5$).
     * Derecha $[12,17,20,30]$: 4 claves ($2 ≤ 4 ≤ 5$).

3. **Número de hijos**

   * Nodo raíz ($m=1$ clave) => $m+1=2$ hijos.
   * Las hojas no tienen hijos.

4. **Claves ordenadas**

   * Dentro de cada nodo, las claves están en orden creciente.

5. **Jerarquía de árboles**

   * Subárbol izquierdo almacena exactamente las claves menores a 10: $\{5,6,7\}$.
   * Subárbol derecho almacena las mayores: $\{12,17,20,30\}$.
   * No hay traslapes ni huecos en los intervalos.

6. **Hojas al mismo nivel**

   * Ambas hojas están en el nivel 1.
   * La altura del árbol es 1, y todo acceso a un dato requiere descender exactamente un nivel desde la raíz.

**4. Complejidad garantizada**

Con $n=8$ claves y $d=3$, la altura $h$ es tal que

$$
h \le \log_{d} \Bigl(\tfrac{n+1}{2}\Bigr) = \log_3\!(4.5)\approx1.5,
$$

lo cual se refleja en nuestro árbol real con $h=1$.

> **Conclusión técnica**:
> Gracias a estas invariantes el B-Tree permanece siempre **perfectamente balanceado**, garantizando operaciones de búsqueda, inserción y eliminación en **tiempo $O(\log_d n)$**.



### **B+ Trees**

Los B+ trees son una variante de los B-trees que introduce una separación funcional entre los nodos internos y los nodos hoja, lo cual aporta optimizaciones significativas, especialmente en el contexto de las bases de datos.

**Diferencias fundamentales e invariantes adicionales:**

1. **Contenido de nodos internos**: Los nodos internos de un B+ tree almacenan únicamente claves. Estas claves actúan como un mapa o guía para dirigir eficientemente la búsqueda hacia la hoja correcta, sin contener los datos asociados. Esto resulta en nodos internos más ligeros y compactos, permitiendo que una mayor parte del índice quepa en la memoria caché.
2. **Contenido de nodos hoja**: Todos los datos (o, más comúnmente, punteros a los datos) residen de forma exclusiva en los nodos hoja. Por lo tanto, si el árbol indexa `n` ítems, habrá exactamente `n` registros en el nivel de las hojas. Las claves en los nodos internos son duplicados de claves que también se encuentran en las hojas.
3. **Lista enlazada de hojas**: Los nodos hoja están conectados secuencialmente entre sí, formando una lista enlazada. Esta es una de las ventajas más potentes de los B+ trees, ya que permite realizar recorridos de rango (ej. "buscar todos los empleados con salarios entre 50.000 y 60.000") de manera extremadamente eficiente. Una vez que se localiza el inicio del rango, se puede simplemente seguir los punteros de la lista enlazada a través de las hojas, sin necesidad de navegar nuevamente por la estructura del árbol.

#### **Operaciones en B-Trees y B+ Trees**

Las operaciones de inserción y eliminación están diseñadas para preservar rigurosamente los invariantes del árbol a través de mecanismos de división y fusión de nodos.

**Inserción:**

1. **Búsqueda**: Primero, se busca en el árbol para localizar el nodo hoja donde la nueva clave debería ser insertada.
2. **Inserción en hoja**: La clave se añade en la posición ordenada correcta dentro de la hoja.
3. **Manejo de desbordamiento (overflow)**: Si, tras la inserción, el nodo hoja excede su capacidad máxima (`2d-1` claves), se produce un desbordamiento.

   * La hoja se divide en dos nuevas hojas. Las claves se reparten equitativamente entre las dos.
   * La clave mediana del conjunto original se "promociona" al nodo padre para que actúe como un nuevo separador entre las dos hojas recién creadas.
4. **Propagación recursiva**: La promoción de una clave al nodo padre puede, a su vez, causar un desbordamiento en ese nodo. Este proceso de división y promoción puede continuar de forma recursiva hacia arriba, hasta llegar a la raíz. Si la raíz se divide, se crea una nueva raíz por encima de la antigua, y la altura total del árbol aumenta en uno.

**Eliminación:**

1. **Búsqueda**: Se localiza y elimina la clave del nodo correspondiente.
2. **Manejo de subdesbordamiento (underflow)**: Si al eliminar una clave, el número de claves en un nodo cae por debajo del mínimo (`d-1`), se produce un subdesbordamiento.

   * **Redistribución**: El algoritmo primero intenta tomar prestada una clave de un nodo hermano adyacente que tenga más del mínimo de claves. Este proceso implica un reajuste de claves entre los hermanos y el padre.
   * **Fusión**: Si los hermanos adyacentes no tienen claves de sobra, el nodo con subdesbordamiento se fusiona con uno de sus hermanos. Esta operación implica mover todas las claves del nodo y su hermano a un único nodo, junto con la clave separadora del padre.
3. **Propagación recursiva**: La fusión de dos nodos reduce el número de hijos del padre, lo que puede provocar un subdesbordamiento en el nivel superior. Este proceso puede propagarse recursivamente hacia la raíz. Si la raíz queda vacía, su único hijo se convierte en la nueva raíz, disminuyendo la altura del árbol.

#### **Ejemplo**

Veamo un ejemplo paso a paso, muy detallado, de las operaciones de **inserción** y **eliminación** en un **B-Tree** y su contraparte en **B+ Tree**, ambos de orden mínimo $d=2$. Esto significa:

* Cada nodo (salvo la raíz) debe tener entre $d-1=1$ y $2d-1=3$ claves.
* La raíz puede tener de 1 a 3 claves.
* Un nodo con $m$ claves tiene $m+1$ hijos (si no es hoja).


**I. B-Tree (orden $d=2$)**

**A. Inserción**

Vamos a insertar la secuencia de claves:

```
[10, 20, 5, 6, 12, 30, 7, 17]
```

1. **Insertar 10**

   * Árbol inicialmente vacío -> la raíz es hoja.
   * Tras inserción:

     ```
     [10]
     ```

2. **Insertar 20**

   * Añadimos en la raíz (hoja), ordenando:

     ```
     [10 | 20]
     ```

3. **Insertar 5**

   * Sigue siendo hoja; ordenamos:

     ```
     [5 | 10 | 20]   (3 claves, ≤3 -> OK)
     ```

4. **Insertar 6**

   * Tras añadir 6 y ordenar -> $[5,6,10,20]$, 4 claves -> **overflow** (máx 3).
   * **Split** de la hoja:

     * Clave mediana = 10
     * Nodo izquierdo = $[5,6]$
     * Nodo derecho = $[20]$
     * Nueva raíz = $[10]$ con dos hijos.

     ```
             [10]
            /    \
       [5 | 6]   [20]
     ```

5. **Insertar 12**

   * 12 > 10 -> va a subárbol derecho $[20]$.
   * Insertamos en esa hoja -> $[12,20]$ (2 claves, ≤3).

     ```
             [10]
            /    \
       [5|6]   [12|20]
     ```

6. **Insertar 30**

   * 30 > 10 -> subárbol derecho $[12,20]$ -> tras insertar -> $[12,20,30]$ (3 claves, justo el máximo).

7. **Insertar 7**

   * 7 < 10 -> subárbol izquierdo $[5,6]$ -> tras insertar y ordenar -> $[5,6,7]$ (3 claves).

     ```
             [10]
            /    \
      [5|6|7]  [12|20|30]
     ```

8. **Insertar 17**

   * 17 > 10 -> $[12,20,30]$ -> tras insertar y ordenar -> $[12,17,20,30]$ (4 claves -> overflow).

   * **Split** de esa hoja:

     * Mediana = 20
     * Nuevo hijo izquierdo = $[12,17]$
     * Nuevo hijo derecho = $[30]$
     * Promocionamos 20 a la raíz.

     ```
                  [10 | 20]
                 /    |    \
        [5|6|7]  [12|17]  [30]
     ```

   * La raíz pasa a tener 2 claves ($\le3$), 3 hijos.

**B. Eliminación**

Partimos del árbol final anterior e **eliminamos** la clave `6`, luego `17` y finalmente `10`.

1. **Eliminar 6**

   * 6 está en la hoja $[5,6,7]$. Tras borrarla: $[5,7]$ (2 claves, ≥1 -> OK).
   * Árbol queda:

     ```
                  [10 | 20]
                 /    |    \
         [5|7]  [12|17]  [30]
     ```

2. **Eliminar 17**

   * 17 está en $[12,17]$ -> borramos -> $[12]$ (1 clave, ≥1 -> OK).
   * No hay underflow; el nodo sigue teniendo el mínimo.

     ```
                  [10 | 20]
                 /    |    \
         [5|7]    [12]   [30]
     ```

3. **Eliminar 10** (clave interna)

   * 10 está en la raíz. En un B-Tree, reemplazamos por su **predecesor** (máximo de su subárbol izquierdo):

     * Predecesor = 7 (de la hoja $[5,7]$).
     * Sustituimos 10->7 en la raíz y eliminamos 7 de la hoja.

     Antes de rebalanceo:

     ```
                  [7 | 20]
                 /    |    \
         [5|7]    [12]   [30]
     ```

     Tras quitar 7 de la hoja:

     ```
                  [7 | 20]
                 /    |    \
         [5]      [12]   [30]
     ```
   * Ahora el primer hijo $[5]$ tiene sólo 1 clave (mínimo aceptable), no hay underflow.
   * **Resultado final**:

     ```
                  [7 | 20]
                 /    |    \
              [5]   [12]  [30]
     ```


**II. B+Tree (orden $d=2$)**

Las diferencias principales:

* **Sólo las hojas almacenan** todas las claves.
* Los **nodos internos** contienen sólo separadores (copias de algunas claves guía).
* Las hojas están **ligadas entre sí** mediante punteros.

**A. Inserción (misma secuencia)**

1. Empezamos igual que en B-Tree, hasta que aparece el **split** en hojas.

2. Supón que tras insertar `[5,6,7,10,12,17,20,30]`, el resultado es:

   ```
                 [10 | 20]
                /        \
      ┌───────────────────┐   ┌─────────────────┐
      │5|6|7|10│──► hoja1  │   │12|17|20|30│ hoja2 │
      └───────────────────┘   └─────────────────┘
               |── enlace hacia ->⠀
   ```

   * Los nodos internos `[10|20]` sólo guían la búsqueda.
   * Las hojas contienen duplicados de las claves guía (10 y 20).
   * Las hojas están encadenadas: hoja1 -> hoja2.

3. No hay promoción en los internos más allá de insertar los separadores 10 y 20.

**B. Eliminación**

1. Si se elimina, por ejemplo, la clave `17`, sólo la borramos de **la hoja** que la contiene:

   ```
      hoja2: [12,17,20,30] -> [12,20,30]
   ```

2. Si quedan menos de $d-1=1$ claves en una hoja (underflow), se **redistribuye** o **fusiona** con la hoja vecina:

   * P. ej., si eliminamos también 12 -> `[20,30]` (2 claves, ≥1 -> OK).
   * No se cambia el nodo interno a menos que un separador quede obsoleto (p. ej. si ya no hay ninguna clave 20 en la hoja, habría que ajustar el separador 20).

3. Los nodos internos actualizan sus **separadores** para reflejar las claves mínimas de cada hoja tras fusiones o redistribuciones.


### **R-Trees**

Mientras los B-trees gestionan datos unidimensionales con maestría, los datos del mundo real, como coordenadas geográficas o vectores de características de imágenes, son inherentemente multidimensionales. Los **R-trees** adaptan la estructura jerárquica y balanceada de los B+ trees para indexar eficientemente objetos en un espacio k-dimensional.

La estrategia central de un R-tree es agrupar objetos espaciales cercanos (sean puntos, líneas o polígonos) y representar a cada grupo en el nivel superior del árbol mediante su **rectángulo mínimo de delimitación** (Minimum Bounding Rectangle o MBR).

#### Invariantes de los R-Trees

Un R-tree está definido por dos parámetros, `m` y `M`, que son el número mínimo y máximo de entradas por nodo, con la condición de que `m ≤ M/2`.

1. **Contenido de los nodos Hoja**: Cada entrada en un nodo hoja almacena el MBR que encierra a un objeto de datos y un identificador (puntero) a dicho objeto.
2. **Contenido de los nodos internos**: Cada entrada en un nodo interno consiste en un puntero a un nodo hijo y el MBR que encierra herméticamente todos los MBRs contenidos en ese nodo hijo.
3. **Capacidad de los nodos**: Todo nodo, excepto la raíz, debe contener entre `m` y `M` entradas. La raíz debe tener al menos dos hijos, a menos que sea una hoja.
4. **Equilibrio de altura**: Todas las hojas residen en el mismo nivel, lo que convierte al R-tree en una estructura de datos balanceada en altura. La altura máxima de un R-tree con `n` objetos es `O(log_m n)`.
5. **Jerarquía de contención**: El MBR de un nodo padre siempre debe contener completamente los MBRs de todos sus nodos hijos.
6. **Solapamiento permitido**: A diferencia de las particiones disjuntas de otras estructuras como los k-d trees, los MBRs de nodos hermanos en un R-tree **pueden solaparse**. La gestión y minimización de este solapamiento es el desafío central en el diseño y rendimiento de un R-tree, ya que un solapamiento excesivo degrada la eficiencia de la búsqueda.

#### **Operaciones en R-Trees**

Las operaciones son conceptualmente análogas a las de los B-trees, pero la naturaleza multidimensional añade capas de complejidad, especialmente en la toma de decisiones heurísticas.

**Búsqueda (search):**

```
function Search(Node N, Rect S):
    for each entry E in N.entries:
        if overlaps(E.MBR, S):
            if N.isInternal():
                ChildNode <- ReadNode(E.ptr)
                Search(ChildNode, S)
            else:
                // N es hoja
                results.add(E.oid)
```

**Inserción (insert):**

1. **Elección de subárbol (chooseSubtree):**

```
function ChooseSubtree(Node N, Object O):
    if N.isLeaf():
        return N

    // Buscamos la entrada cuyo MBR requiere
    // la menor expansión para incluir O.MBR
    BestEntry <- argmin_{E in N.entries}
                   area(enlarge(E.MBR, O.MBR)) − area(E.MBR)

    ChildNode <- ReadNode(BestEntry.ptr)
    return ChooseSubtree(ChildNode, O)
```

2. **Inserción y manejo de desbordamiento:**

```
function Insert(Node root, Object O):
    L <- ChooseSubtree(root, O)
    L.entries.add(Entry(O.MBR, O.id))

    if L.entries.size > M:
        (N1, N2, promotedEntry) <- SplitNode(L)
        AdjustTree(L, N2, promotedEntry)
    else:
        AdjustMBRsUpwards(L)

function AdjustTree(Node N, Node N2, Entry promotedEntry):
    if N is root:
        // Creamos nueva raíz
        newRoot <- Node()
        newRoot.entries = [Entry(N.MBR, ptr=N),
                           Entry(N2.MBR, ptr=N2)]
        root <- newRoot
        return

    P <- N.parent
    // Reemplazamos la entrada de N por la promovida
    P.updateEntryForChild(N, promotedEntry)
    P.entries.add(Entry(N2.MBR, ptr=N2))

    if P.entries.size > M:
        (P1, P2, newPromoted) <- SplitNode(P)
        AdjustTree(P1, P2, newPromoted)
    else:
        AdjustMBRsUpwards(P)
```

* **SplitNode** implementa la heurística (cuadrática o lineal) para dividir las $M+1$ entradas en dos grupos $N_1$ y $N_2$, y devuelve también la entrada que se promueve al padre.
* **AdjustMBRsUpwards** recorre desde el nodo dado hasta la raíz, ajustando cada MBR para que siga conteniendo correctamente los hijos.

**Ejemplo paso a paso (R-Tree con $m=2,\,M=4$)**

Insertaremos cinco rectángulos etiquetados A-E, cuyas MBR son:

| Objeto | MBR (xmin, ymin, xmax, ymax) |
| ------ | ---------------------------- |
| A      | (1, 1, 2, 2)                 |
| B      | (2, 2, 4, 4)                 |
| C      | (3, 0, 5, 1)                 |
| D      | (0, 3, 1, 5)                 |
| E      | (4, 3, 6, 5)                 |

**1. Insertar A**

* Árbol vacío ⇒ raíz = hoja con A.
* Raíz: $A$ -> MBR raíz = (1,1,2,2).

**2. Insertar B**

* Elige hoja raíz.
* Tras inserción: entradas = $A, B$ (2 ≤ M=4 -> OK).
* MBR hoja = unión(MBR(A),MBR(B)) = (1,1,4,4).

**3. Insertar C**

* Misma hoja: entradas = $A, B, C$ (3 ≤ 4 -> OK).
* MBR hoja = (1,0,5,4).

**4. Insertar D**

* Misma hoja: entradas = $A, B, C, D$ (4 = M -> OK).
* MBR hoja = (0,0,5,5).

```
Hoja L1: [A, B, C, D]    MBR(L1) = (0,0,5,5)
Raíz-> L1
```

**5. Insertar E -> Overflow**

* Intentamos poner E en L1 -> tendríamos 5 entradas > M=4.

* **Split** de L1 en L1₁ y L1₂ con la heurística lineal (minimizar solapamiento):

  * Paso 1: seleccionar dos "semillas" lejanas.

    * Podrían ser C (3,0-5,1) y D (0,3-1,5).
  * Paso 2: asignar A, B, E al grupo cuya expansión de MBR sea menor.

    * A y B van al grupo de D; E va al grupo de C.
  * Resultado:

    * L1₁ = $D, A, B$, MBR₁ = (0,1,4,5)
    * L1₂ = $C, E$,    MBR₂ = (3,0,6,5)

* Promovemos al padre la entrada separadora cuya clave guía es el MBR mínimo común, por ejemplo:

  * Entrada promovida = (MBR₁, ptr->L1₁) y se añade (MBR₂, ptr->L1₂).

* Como L1 era la raíz, **creamos** nueva raíz R:

```
             R
      ┌───────────────┬───────────────┐
      │ (0,1-4,5) L1₁ │ (3,0-6,5) L1₂ │
      └───────────────┴───────────────┘
```

**Búsqueda de, por ejemplo, todos los objetos que intersectan el rectángulo S=(2,1,3,4)**

1. En R comprobamos ambos hijos:

   * MBR₁=(0,1-4,5) **sí** solapa con S -> buscamos en L1₁
   * MBR₂=(3,0-6,5) **sí** solapa con S -> buscamos en L1₂

2. En L1₁ revisamos A, B, D:

   * A=(1,1-2,2) ∩ S ≠ ∅ -> devuelve A
   * B=(2,2-4,4) ∩ S ≠ ∅ -> devuelve B
   * D=(0,3-1,5) ∩ S = ∅ -> descartamos

3. En L1₂ revisamos C, E:

   * C=(3,0-5,1) ∩ S ≠ ∅ -> devuelve C
   * E=(4,3-6,5) ∩ S = ∅ -> descartamos

**Resultado de Search** = {A, B, C}.


Con este ejemplo ves cómo, mediante **splits controlados**, **promociones** y **MBRs jerárquicos**, el R-tree mantiene sus invariantes de capacidad, contención y equilibrio de altura, a la vez que alcanza búsquedas eficientes en espacios multidimensionales.


### **Optimizaciones avanzadas**

#### **Refinar las heurísticas de división en los R-Trees**

El proceso de dividir un nodo desbordado en un R-tree es crítico: de él depende la calidad de los agrupamientos y, por tanto, la eficiencia global de las operaciones de búsqueda e inserción. 

Para comenzar, los métodos clásicos de división lineal y cuadrático buscan semillas de forma sencilla: el primero elige, por cada dimensión, las dos entradas con bordes más extremos y agrupa el resto según la expansión mínima del MBR, mientras que el segundo calcula para cada par la "pérdida" de área al unirlos, eligiendo el peor caso como semillas. El enfoque lineal es muy rápido (`O(n)`) pero genera solapamientos elevados; el cuadrático mejora la partición a costa de un coste `O(n²)` en la selección de semillas.

El R\*-tree introduce dos innovaciones que equilibran calidad y coste. Primero, en lugar de medir solo el área, emplea el **perímetro** de los MBR resultantes: preferir divisiones con menor suma de perímetros tiende a generar rectángulos más compactos y menos solapamiento. Segundo, antes de dividir, aplica una **reinserción forzada**: retira un porcentaje (por ejemplo, 30 %) de las entradas más alejadas del centro del nodo desbordado y las reintroduce desde la raíz. Esto permite redistribuir puntos que quedaban mal agrupados sin aumentar la altura del árbol.

El flujo de inserción en R\*-trees es entonces: localizar la hoja con menor expansión, insertar el objeto y, si hay desbordamiento, ejecutar la reinserción forzada una sola vez. Si tras esto el nodo sigue lleno, se evalúan particiones balanceadas no exhaustivas, calculando para cada una el perímetro total, el área y el solapamiento, y eligiendo la que optimiza primero el perímetro, luego el solapamiento y, por último, el área.

En la práctica, los parámetros de porcentaje de reinserción y el número de particiones consideradas se ajustan según la proporción de inserciones frente a consultas. Además, extensiones como el **Hilbert R-Tree** (que ordena según la curva de Hilbert) o el **Bulk-Loading R\*-Tree** (que agrupa entradas en bloques ordenados espacialmente antes de la construcción) demuestran que estas ideas pueden combinarse con ordenamientos espaciales y cargas masivas para obtener índices aún más eficientes.

Con estos refinamientos, las divisiones de R-trees pasan de reglas sencillas a algoritmos que equilibran perímetro, solapamiento y redistribución dinámica, logrando estructuras más compactas y búsquedas más rápidas en entornos dinámicos y de alta dimensionalidad.

#### **Variantes de B+ Trees para entornos in-memory**

Con el paso del almacenamiento en disco a la RAM, el reto deja de ser la E/S y pasa a ser la jerarquía de caché de la CPU. 
Para optimizar los B+ trees en memoria, primero se ajusta el tamaño de cada nodo al de una línea de caché (por ejemplo 64 B), de modo que un solo fallo cargue el nodo completo. Luego, se aprovecha el prefetching: al recorrer rangos, se anticipan lecturas de nodos hoja enlazados y se emiten instrucciones `PREFETCH` para minimizar esperas.

Más allá de estos ajustes "cache-aware", entran en juego los diseños **cache-oblivious** como el layout van Emde Boas o las Funnelsort trees, que reordenan recursivamente los nodos para maximizar la localidad en todas las capas de memoria sin necesidad de parámetros de caché. Para reducir aún más la sobrecarga, variantes como CSB+ trees agrupan hijos en bloques contiguos y comprimen punteros usando offsets relativos, lo que permite almacenar más claves por línea. Finalmente, estructuras híbridas tipo Fractal Tree o Bε-tree agrupan inserciones en buffers que caben en caché, logrando escrituras muy rápidas sin penalizar las búsquedas. De este modo, los B+ trees in-memory combinan alineación precisa, prefetching inteligente, layouts oblivious y compresión de punteros para explotar al máximo la RAM y las múltiples capas de caché.

#### **Estructuras híbridas R-Tree/k-d Tree**

Al combinar un R-tree global con un k-d tree local, se crea un índice que equilibra la visión panorámica del espacio con particiones muy afinadas en cada región. A nivel superior, el R-tree mantiene el árbol perfectamente balanceado, agrupa objetos en rectángulos mínimos de delimitación (MBR) y dirige las consultas de rango o de proximidad hacia unas pocas hojas relevantes. 
Una vez que esa primera poda global ha reducido drásticamente el número de candidatos, cada hoja despliega su propio k-d tree, construido exclusivamente con los puntos que caen dentro de su MBR.

Esta estrategia de dos niveles atiende de manera natural a patrones mixtos de acceso. Para consultas amplias, como "encuentra todos los objetos en esta región geográfica", basta con recorrer la rama del R-tree y luego hacer búsquedas en cada k-d tree de hoja, donde la poda por ejes evita explorar zonas vacías. 

Para búsquedas de vecinos más cercanos (kNN), el R-tree calcula una lista priorizada de hojas basándose en la distancia mínima desde el punto de consulta hasta cada MBR; después, cada k-d tree local realiza su propio kNN interno con estructuras de backtracking ligeras, devolviendo un puñado de candidatos que se comparan finalmente a escala global.

En cuanto a las inserciones y eliminaciones, el precepto es mantener ambos niveles sincronizados sin sacrificar el rendimiento. Al añadir un nuevo punto, primero se desciende por el R-tree eligiendo la hoja cuya expansión de MBR sea mínima, tras insertar en el k-d tree local, ese índice puede reequilibrarse mediante rotaciones o reconstrucciones parciales cuando su tamaño supera un umbral predefinido (por ejemplo, 1000 elementos). 

Si la hoja acumula demasiados k-d trees desbalanceados o su MBR crece más allá de cierto volumen, el R-tree divide la hoja en dos: cada mitad hereda un subconjunto de puntos y crea un nuevo k-d tree, de manera que la altura global permanece óptima.  El procedimiento inverso se aplica al borrar: se elimina del k-d tree, se reequilibra localmente, y si un k-d tree cae por debajo de un mínimo (por ejemplo, 100 elementos), sus puntos se pueden fusionar con una hoja vecina para evitar overhead de hojas vacías.

El resultado es una estructura altamente adaptable: gestiona millones de puntos multidimensionales con inserciones y borrados dinámicos, ofrece búsquedas de rango en tiempo cercano a `O(log n + k)` y kNN en `O(log m + k)`, donde `n` es el total de objetos y `m` el tamaño de cada k-d tree local. 

Además, al compartir memoria contigua para cada k-d tree de hoja, se mejora la localidad de referencia y se reducen fallos de caché en entornos in-memory. Con una parametrización cuidadosa de los umbrales de hoja y las estrategias de rebalanceo, esta solución híbrida mantiene una latencia baja tanto para operaciones gruesas como finas, adaptándose de forma fluida a patrones de acceso mixtos y escalando de manera efectiva en aplicaciones geoespaciales, búsqueda por similitud en multimedia o análisis de vectores de características de alta dimensión.

#### **Incorporar compresión de nodos, prefetching adaptativo y paralelismo**

Al optimizar R-trees para escenarios de gran escala y altas velocidades de consulta, conviene aprovechar tres líneas de innovación que van de la gestión interna de los nodos hasta la arquitectura subyacente del hardware:

**Compresión de nodos**
En lugar de almacenar claves y punteros sin más, cada página de árbol—típicamente del tamaño de un bloque de disco o página de memoria—puede comprimirse usando algoritmos ligeros (por ejemplo, varint para enteros o Brotli/Oodle en modos rápidos). 

Al reducir el tamaño medio de un nodo, caben más entradas por bloque, lo que disminuye la altura del árbol y el número de accesos necesarios para recorrerlo. Además, como muchas coordenadas o valores de índice presentan redundancias (MBR superpuestos o valores cercanos), la compresión delta entre bordes contiguos resulta muy efectiva. La descompresión en memoria es casi instantánea con técnicas SIMD que expanden vectores comprimidos en pocos ciclos de CPU.

**Prefetching adaptativo**
El patrón clásico de "acceso demanda" a páginas de R-tree introduce latencias de cientos de microsegundos en discos SSD y decenas en RAM. Un sistema adaptativo observa los accesos recientes y predice qué nodos serán necesarios a continuación, por ejemplo  en búsquedas de rango, tras acceder a una hoja se anticipan los vecinos en la lista enlazada de hojas. Entonces emite instrucciones de prefetch (como `PREFETCHT0` o lecturas asíncronas en librerías IO\_uring) para cargar en segundo plano esos nodos antes de que el hilo de búsqueda los solicite. Con perfiles dinámicos de acceso, el sistema ajusta cuántos y cuán lejos en la estructura prefetchar, evitando tanto sobrecarga innecesaria como subutilización del ancho de banda del almacenamiento.

**Indexado paralelo y árboles lock-rree**
En arquitecturas multi-core, procesar inserciones y consultas concurrentes sin bloqueos mejora drásticamente el rendimiento. Los árboles lock-free aplican técnicas como CAS (compare-and-swap) para enlazar o dividir nodos sin barreras globales: si dos hilos intentan dividir el mismo nodo, uno gana la carrera y el otro detecta el cambio y retrocede al punto seguro más cercano. 

Esto permite escalar casi linealmente con el número de núcleos en cargas mixtas de lectura-escritura. Para búsquedas masivas (por ejemplo, kNN de miles de consultas simultáneas), dividir el conjunto de hojas candidatas entre hilos y combinar los resultados parciales reduce la latencia global.

**Hardware especializado (FPGA/ASIC)**
Cuando la demanda supera lo que la CPU y la memoria pueden procesar, introducir aceleradores dedicados marca la diferencia. En FPGA, se puede implementar un pipeline de decisión de nodo muy ancho y profundo: mientras un bloque de lógica evalúa si la consulta cae en el hijo izquierdo o derecho, otro bloque ya está leyendo la siguiente entrada comprimida y otro más descorriendo valores para el próximo nivel. Todo esto a frecuencias de cientos de megahercios o incluso gigahercios internos, con latencias de acceso a nodo contadas en nanosegundos. 

En ASIC, se pueden integrar controladores de prefetch personalizados y motores de descompresión de alto rendimiento conectados directamente al bus de memoria, eliminando overhead de software. Estos diseños son especialmente valiosos en centros de datos de alta frecuencia, motores de recomendación en tiempo real o análisis de video en streaming, donde cada microsegundo cuenta.

En conjunto, comprimir cada nodo para caber más MBR en cada acceso, predecir y traer datos proactivamente, coordinar múltiples hilos sin bloqueos y, finalmente, descargar la lógica de decisión a hardware dedicado, convierten un índice R-tree corriente en una máquina de consulta espacial capaz de procesar millones de operaciones por segundo con latencias mínimas.
