### **Conjuntos disjuntos y procesamiento en tiempo sublineal**  

#### 1. Introducción al problema  

Un **conjunto disjunto** es una estructura de datos diseñada para gestionar particiones de un conjunto original de elementos en grupos mutuamente excluyentes. Aunque a primera vista el problema puede parecer trivial, su estudio revela sofisticados matices de rendimiento: implementar la solución obvia sin más  análisis conduce a costosas operaciones lineales que, en casos reales de gran escala, resultan inviables. 
Estas notas muestran cómo comenzar por la definición formal del problema, pasar por soluciones ingenuas y, finalmente, sentar las bases para  optimizaciones que permitan alcanzar tiempos casi constantes en las operaciones más críticas.  

El uso de conjuntos disjuntos surge naturalmente en aplicaciones de clustering dinámico, por ejemplo, para agrupar vinos según su sabor o alimentos según sus propiedades. Este mismo paradigma se emplea en sistemas de recomendación no personalizada, donde los productos se agrupan según las compras frecuentes para ofrecer sugerencias instantáneas sin análisis de usuario individual.  

#### 2. Caso de estudio: recomendaciones de e-commerce  

Imagina un sitio de comercio electrónico en fase de lanzamiento, sin históricos de clientes. Una estrategia inicial es ofrecer recomendaciones no personalizadas: las mismas para todos los usuarios, basadas en la frecuencia con que dos productos aparecen juntos en carritos de compra. 
Cada vez que `X` e `Y` se adquieren juntos por encima de un umbral (por ejemplo, más de 500 veces en la última hora), se decide fusionar los grupos de  `X`  y `Y` en un conjunto disjunto común.  

Este mecanismo simplificado de **clustering jerárquico** permite, a su vez, sugerir a cualquier cliente que añada un producto `X` un artículo aleatorio de la misma partición. En sistemas de producción, este enfoque se enriquecería con métricas de confianza 
(p. ej., P(Y|X) = compras (X∧Y) / compras (X)), umbrales más finos y despliegues de múltiples asociaciones, pero la esencia sigue siendo agrupar elementos de un universo dinámico y actualizar particiones de forma eficiente.  

#### 3. Formalización y API de la estructura DisjointSet  

#### 3.1 Definición abstracta  

Sea `U` un universo de `n` elementos (idealmente etiquetados `{0,..,n-1}`), queremos mantener una **relación de equivalencia** (®) sobre `U` que sea reflexiva, simétrica y transitiva. Cada clase de equivalencia es un subconjunto disjunto, y la familia de todas ellas constituye una partición de `U`.  

La **API** esencial de la clase `DisjointSet` incluye las siguientes operaciones:  

- **Constructor** `init(U)`: inicializa la estructura con cada elemento en su propia clase  
- **findPartition(x)**: retorna la representación (identificador o puntero interno) de la clase de `x`  
- **merge(x, y)**: fusiona las clases que contienen `x` e `y` si son distintas  
- **areDisjoint(x, y)**: comprueba si `x` e `y` aún pertenecen a clases separadas  

La implementación debe garantizar que, tras una secuencia de fusiones, cualquier cadena de relaciones `x_1®x_2, x_2®x_3,...` provoque que `x_1` y `x_n` queden en la misma partición.  

#### 3.2 Contrato y propiedades  

- **Validez de entradas**: lanzar error si se invocan métodos con elementos nulos o no previamente agregados  
- **Invariante**: la estructura siempre mantiene un mapeo de cada elemento a su clase  
- **Reutilización**: `areDisjoint` y `merge` se apoyan en `findPartition` para validar entradas y recuperar clases  


#### 4. Solución ingenua y sus limitaciones  

#### 4.1 Diseño con listas y mapas  

La estrategia más inmediata usa dos estructuras:  
1. Un arreglo o lista de todas las **particiones**, cada una representada como una lista enlazada o un `Set`.  
2. Un **mapa** (`HashMap<Elemento, Partición>`) que, para cada elemento, apunta a la lista que lo contiene.  

Con esta representación, `findPartition(x)` es `O(1)`: basta con consultar el diccionario. Del mismo modo, `areDisjoint(x,y)` llama a `findPartition` dos veces y compara resultados, también en tiempo constante.  

#### 4.2 Fusión de particiones  

Para fusionar dos listas `L_1` y `L_2`, la idea básica es:  
1. Obtener `p_1 <- findPartition(x)` y `p_2<- findPartition(y)`.  
2. Si `p_1=p_2`, no hay nada que hacer.  
3. Enlazar el final de una lista al principio de la otra (en listas enlazadas, operación `O(1)`), pero... 
4. **Actualizar** para cada elemento de la lista más pequeña su entrada en el mapa, apuntando ahora a la partición fusionada.  

La asignación de nuevos punteros implica recorrer todos los elementos de la partición pequeña, por lo que en el **peor caso** la operación `merge` es `O(k)`, donde `k` es el tamaño de la partición pequeña. Cuando se repite para muchas fusiones, el costo total puede llegar a `O(n^2)` en aplicaciones reales, un rendimiento intolerable para universos grandes.  

#### 4.3 Pseudocódigo de la solución ingenua  

```  
class DisjointSet:  
    partitionsMap: HashMap<Elemento, Set<Elemento>>

    function __init__(initialSet):  
        partitionsMap <- nuevo HashMap  
        for elem in initialSet:  
            lanzarErrorSi(elem == null o existe(elem))  
            partitionsMap[elem] <- nuevo Set{elem}

    function add(elem):  
        lanzarErrorSi(elem == null)  
        if existe(elem):  
            return false  
        partitionsMap[elem] <- nuevo Set{elem}  
        return true

    function findPartition(elem):  
        lanzarErrorSi(elem == null o no existe(elem))  
        return partitionsMap[elem]

    function areDisjoint(elem1, elem2):  
        p1 <- findPartition(elem1)  
        p2 <- findPartition(elem2)  
        return p1 != p2

    function merge(elem1, elem2):  
        p1 <- findPartition(elem1)  
        p2 <- findPartition(elem2)  
        if p1 == p2: return false  
        // siempre verter p1 en p2  
        for e in p1:  
            p2.add(e)  
            partitionsMap[e] <- p2  
        return true  
```  


#### 5. Análisis de complejidad de la solución ingenua  

- **Constructor**: `O(n)` para agregar `n` elementos iniciales.  
- **add**, **findPartition**, **areDisjoint**: `O(1)` cada una (suponiendo hashes `O(1)`).  
- **merge**: `O(k)` en el peor caso, con `k` el tamaño de la partición menor.  

La mejora de siempre **agregar la lista más pequeña** a la más grande garantiza que ningún elemento cambie de puntero más de `log n` veces a lo
largo de todas las fusiones, llevando el coste amortizado de `merge` a `O(log n)` por operación. Sin embargo, esta heurística no reduce la complejidad asintótica del peor caso de la operación individual: sigue siendo linear en el tamaño de la partición.  


#### 6. Motivación para optimizaciones avanzadas  

Aunque la solución con listas y mapa resuelve correctamente el problema funcional, su rendimiento en escenarios con millones de elementos y miles de 
fusiones por segundo resulta insuficiente. El objetivo último es alcanzar tiempos **casi constantes** (`O(α(n))`, donde `α` es la función inversa de Ackermann, prácticamente constante para cualquier `n` razonable) en las operaciones `find` y `merge`.  

La clave está en cambiar la representación interna: en lugar de múltiples listas, usar un **bosque de árboles** (disjoint-set forest), donde cada
elemento apunta a su "padre" en un árbol cuya raíz identifica la clase. Con técnicas como:  

1. **Unión por rango (rank heuristic)**: el árbol más pequeño se hace subárbol del más grande.  
2. **Compresión de caminos (path compression)**: durante `find`, todos los nodos visitados apuntan directamente a la raíz.  

Estas dos heurísticas combinadas garantizan que la complejidad amortizada de ambas operaciones sea `α(n)`, próximo a `O(1)` incluso para universos con billones de nodos.  

