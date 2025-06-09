## **B-trees, B+ trees y R-trees**

Los árboles balanceados constituyen una familia fundamental de estructuras de datos para el almacenamiento y recuperación eficiente de información en sistemas de gestión de bases de datos, sistemas de archivos y aplicaciones de indexación espacial.
Entre ellos, los B-trees y sus variantes, como los B+ trees y los R-trees, ofrecen mecanismos escalables para manejar grandes  volúmenes de datos en disco y memoria secundaria, proporcionando tiempos de acceso logarítmicos y una organización jerárquica que minimiza 
las operaciones de lectura/escritura. 

### **1. B-trees**

Los B-trees fueron introducidos por Rudolf Bayer y Edward McCreight en 1972 con el objetivo de crear una estructura en árbol balanceado que minimizara las operaciones de I/O al trabajar con grandes archivos en disco. 
El diseño de los B-trees parte de la necesidad de agrupar claves en nodos (o páginas) de tamaño fijo, acorde con el tamaño de bloque de la 
memoria secundaria, para reducir la profundidad del árbol y, por ende, el número de accesos a disco durante una consulta.

### **1.2. Estructura y propiedades**

Un B-tree de grado mínimo *t* (también llamado árbol *t*-ario) cumple las siguientes condiciones:

1. Cada nodo contiene como máximo 2*t* - 1 claves y, salvo la raíz, como mínimo *t* - 1 claves.
2. Un nodo con *k* claves tiene *k* + 1 hijos, de modo que:

   * Los nodos internos actúan como separadores ordenados de rango.
   * Todas las hojas se encuentran al mismo nivel, garantizando balanceo estricto.
3. La raíz puede contener desde 1 hasta 2*t* - 1 claves.

Este diseño asegura que el árbol mantenga una altura mínima, lo cual es crítico para operaciones de búsqueda: el número máximo de accesos adisco está acotado por la altura del árbol, que crece logarítmicamente con el número de elementos.

### **1.3. Operaciones básicas**

**Búsqueda**

Para buscar una clave *k*, se inicia en la raíz y, en cada nodo, se recorre la lista de claves ordenadas para determinar entre qué par de claves *k* encaja (o si coincide exacta). Si se encuentra, la búsqueda concluye exitosamente. 
De lo contrario, se desciende recursivamente al subárbol correspondiente. Dado que cada nodo tiene hasta 2*t* - 1 claves, la búsqueda en unnodo interno requiere tiempo O(*t*), y la altura del árbol es O(logₜ *N*), resultando en una complejidad global O(*t* logₜ *N*), que en
la práctica se considera O(log *N*) al fijar *t* para aprovechar bloques de disco.

**Inserción**

La inserción de una nueva clave *k* se realiza siguiendo estos pasos:

1. **Descenso especial**
   Se desciende hasta la hoja donde debería ir *k*.
2. **Split anticipado**
   Si durante el descenso se encuentra un nodo lleno (con 2*t* - 1 claves), se divide ("split") en dos nodos de *t* - 1 claves cada uno, elevando la clave central al padre.
3. **Inserción en hoja**
   Se inserta *k* en la posición ordenada dentro del nodo hoja, que ahora tiene espacio tras el posible split.

La técnica de "split a la marcha" garantiza que nunca se intente insertar en un nodo lleno, simplificando la implementación y manteniendo las propiedades de tamaño de nodo y balanceo.

**Eliminación**

La eliminación de una clave *k* en un B-tree requiere varios casos:

1. **Clave en hoja**

   * Si la hoja tiene más de *t* - 1 claves tras remover *k*, simplemente se elimina.
   * Si queda con menos de *t* - 1 claves, se reequilibra ya sea pidiendo una clave prestada al hermano adyacente (rotación) o fusionando ("merge") con un hermano y bajando una clave del padre.

2. **Clave en nodo interno**

   * Se sustituye *k* por su predecesor (clave máxima del subárbol izquierdo) o sucesor (clave mínima del subárbol derecho), y luego se elimina recursivamente esa clave en la hoja correspondiente, aplicando los mismos criterios de reequilibrio.

La eliminación es más compleja que la inserción, pero con estas reglas se asegura que ningún nodo (excepto la raíz) tenga menos de *t* - 1 claves, manteniendo el árbol balanceado.

> Referencia: [B-tree](https://en.wikipedia.org/wiki/B-tree)

### **2. B+ trees**

### **2.1. Origen y diferencias clave**

Los B+ trees surgen como una variante de los B-trees focalizada en optimizar aún más el rendimiento de lectura secuencial y la utilización de páginas de disco. La diferencia principal es que en un B+ tree:

1. **Datos solo en las hojas:** Las claves que acompañan a los datos (o punteros a registros) residen únicamente en los nodos hoja.
2. **Nodos internos con solo guías:** Los nodos internos contienen únicamente copias de claves para direccionamiento, sin almacenar los valores asociados.
3. **Enlaces entre hojas:** Se mantiene un puntero "next" entre cada hoja y su sucesora, formando una lista enlazada que facilita recorridos secuenciales.

### **2.2. Estructura y propiedades**

* **Orden y capacidad:** Similar a los B-trees, un B+ tree de orden *d* permite hasta 2*d* punteros en cada nodo interno y hasta 2*d* pares (clave, valor) en cada hoja.
* **Enlazado de hojas:** Todos los nodos hoja están conectados en una lista simplemente enlazada, lo que convierte al árbol en una estructura híbrida árbol-lista.


### **2.3. Operaciones**

**Búsqueda**

La búsqueda de una clave *k* desciende por los nodos internos, comparando *k* únicamente con claves guía, hasta llegar al nodo hoja que contiene rangos que abarcan *k*. 
En la hoja, se localiza la clave exacta y se retorna el valor correspondiente. Al estar los nodos internos "vacíos" de valores, las comparaciones son más rápidas y el tamaño útil de cada página es mayor.

**Inserción**

La inserción se realiza en la hoja destino:

1. **Inserción directa:** Si la hoja tiene espacio, se inserta el par (clave, valor) en orden.
2. **Overflow y split de hoja:**

   * Cuando la hoja está llena, se divide en dos hojas de *d* elementos cada una.
   * La clave mínima de la segunda hoja se promueve al nodo padre como nuevo separador.
3. **Propagación de split:** Si el padre se llena al recibir una nueva clave de separación, se aplica split recursivamente hacia arriba, pudiendo alcanzar la raíz y aumentar la altura en uno.

**Pseudocódigo: Split en B+ tree hoja**

```pseudo
function splitLeaf(node):
    mid = ceil((order+1)/2)
    leftKeys = node.keys[0:mid]
    rightKeys = node.keys[mid:]
    newNode = LeafNode(rightKeys)
    node.keys = leftKeys
    newNode.next = node.next
    node.next = newNode
    promoteKey = newNode.keys[0]
    insertInParent(node, promoteKey, newNode)
```

**Eliminación**

La eliminación también se restringe a las hojas:

1. **Borrado en hoja:** Se elimina el par (clave, valor).
2. **Underflow:** Si la hoja queda con menos de *d* elementos, se intenta:

   * **Rotación:** Tomar un elemento prestado de un hermano adyacente que tenga más de *d* elementos.
   * **Fusión:** Si ambos hermanos están en umbral mínimo, se fusionan dos hojas y se elimina la clave guía correspondiente del padre, pudiendo desencadenar reequilibrios ascendentes.


> Referencia: [B+tree](https://en.wikipedia.org/wiki/B%2B_tree)

### **3. R-trees**

> **Nota terminológica:** A partir de este punto, se usará consistentemente el término **MBR** (Minimum Bounding Rectangle) para referirsea los rectángulos límite.

### **Motivación para la indexación espacial**

Mientras que los B-trees y B+ trees están diseñados para datos unidimensionales (claves numéricas o lexicográficas), muchas aplicaciones requieren indexar objetos multidimensionales: rectángulos, polígonos, puntos geográficos o regiones en bases de datos GIS  (Geographic Information Systems). 
Los R-trees, introducidos por Antonin Guttman en 1984, extienden la idea de los árboles balanceados para manejar eficientemente esas estructuras espaciales, agrupando regiones en volúmenes mínimos (MBR) y manteniendo balanceo similar al de los B-trees.

### **3.2. Estructura y propiedades**

1. **Nodos con MBRs que encierran objetos:** Cada nodo almacena un conjunto de entradas, donde cada entrada en un nodo interno apunta a un subárbol y lleva asociado un MBR que cubre todas las figuras en ese subárbol.
2. **Hijos y hojas:**

   * **Hojas:** contienen entradas (MBR, objeto real o puntero a objeto).
   * **Nodos internos:** contienen entradas (MBR, puntero a hijo).
3. **Balanceo:** Todas las hojas están al mismo nivel; cada nodo tiene entre *m* y *M* entradas (con *m* ≤ *M*/2), salvo la raíz.

### **3.3 Operaciones**

#### **Búsqueda espacial**

Para buscar todos los objetos que intersectan una región dada *R*, se inicia en la raíz y, en cada nodo, se verifica qué MBRs hijos se intersectan con *R*. Solo se exploran esas ramas, descartando aquellas que no puedan contener resultados. En hojas, se comprueba la intersección con los objetos reales o sus MBRs respectivas.

#### **Inserción**

La inserción de un nuevo objeto con MBR *R\_nuevo* se efectúa así:

1. **Selección de hoja (ChooseLeaf):**
   Se desciende el árbol eligiendo en cada nivel el hijo cuyo MBR necesite el menor aumento de área para cubrir *R\_nuevo* (criterio del menor incremento de cobertura).
2. **Inserción y split de hoja:**

   * Si la hoja tiene espacio (< *M* entradas), se añade la entrada.
   * Si está llena, se aplica *split* según la heurística elegida (**Linear Split** o **Quadratic Split**):

     * **Linear split:** Agrupa pares de MBRs con mayor separación inicial, rápido de calcular, adecuado para cargas dinámicas con bajo coste de procesamiento.
     * **Quadratic split:** Examina todas las parejas de entradas para maximizar el "margen" entre grupos y así minimizar el área conjunta y solapamiento, más costoso pero mejora calidad de partición cuando el solapamiento es crítico.
3. **Propagación de split:**
   Si el padre se llena al recibir una nueva entrada de división, se aplica split recursivamente hacia arriba, pudiendo alcanzar la raíz y aumentar la altura.
4. **Ajuste de MBRs:**
   Tras la inserción, se actualizan los MBRs de todos los nodos ancestros para que incluyan al nuevo MBR.

**Pseudocódigo: Split en R-tree (Quadratic)**

```pseudo
function quadraticSplit(node):
    E = node.entries
    (e1, e2) = pickSeedsQuadratic(E)
    G1 = {e1}, G2 = {e2}
    remove e1,e2 from E
    // 2. Distribuir el resto
    while E not empty:
        if G1.size + E.size == m: assign all E to G1; break
        if G2.size + E.size == m: assign all E to G2; break
        e = pickNextQuadratic(E, G1, G2)
        if areaIncrease(G1,e) < areaIncrease(G2,e): assign e to G1 else to G2
        remove e from E
    return newNodes(G1, G2)
```

#### **Eliminación**

La eliminación de un objeto con MBR *R* implicará:

1. **Búsqueda de hoja:** Se localiza la hoja que contiene la entrada correspondiente a *R*.
2. **Borrado y underflow:**

   * Se elimina la entrada de la hoja.
   * Si la hoja queda con menos de *m* entradas, se elimina del árbol y sus entradas sobrantes se **reinsertan** en el árbol (*reinserción*).
3. **Ajuste de MBRs:**
   Se actualizan los MBRs ascendentes, reduciendo su área según el contenido restante.

> **Reinserción y reducción de solapamientos**
> La reinserción de entradas provenientes de nodos subpoblados ayuda a reducir solapamientos porque permite que dichas entradas encuentren ubicaciones más adecuadas en la estructura ya modificada, en lugar de concentrarse en una misma región tras una fusión. Al reinsertar, se vuelve a aplicar el criterio de selección de hoja (ChooseLeaf) con estados de MBRs ya actualizados, lo que distribuye mejor los rectángulos y minimiza solapamientos futuros.

> Referencia:[R-tree](https://en.m.wikipedia.org/wiki/R-tree)

### **4. Rendimiento práctico y coste I/O**

Para ilustrar el impacto del diseño en operaciones reales, consideremos dos casos de ejemplo:

* **B+ tree de orden óptimo en páginas de 4 KB:**

  * Supongamos claves de 16 bytes y punteros de 8 bytes; cada entrada ocupa 24 bytes.
  * Cada nodo interno de 4 KB puede albergar \~170 entradas; la altura para 1 millón de claves es ≈ 3.
  * Cada búsqueda requeriría \~3 lecturas de página.

* **R-tree con 1 000 000 de puntos geoespaciales (MBRs reducidos):**

  * Asumamos cada MBR codificado en 32 bytes y puntero de 8 bytes; entradas de 40 bytes.
  * Páginas de 4 KB almacenan \~100 entradas; altura ≈ 3.
  * Sin embargo, solapamientos pueden implicar descender por múltiples ramas, aumentando el número de páginas leídas a \~5-7 en búsquedas puntuales.

### **4.1. Impacto de parámetros de sistema**

* **Buffer pool y caching:** Una mayor carga del buffer pool reduce lecturas de disco. Los B+ trees aprovechan mejor la localidad de referencia en recorridos secuenciales de hojas enlazadas.
* **Localidad de referencia:** Los índices espaciales (R-trees) sufren más variabilidad, pues la dispersión de datos geoespaciales puede causar saltos de página impredecibles.
* **Heurísticas de split:** Un *quadratic split* más costoso en CPU puede reducir I/O futuro al disminuir solapamientos; un *linear split* acelera inserción en escenarios de alta carga dinámica, aunque con algo más de solapamiento.

