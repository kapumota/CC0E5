#### 1. Transición de listas a árboles  

Hasta ahora, la implementación ingenua mediante listas ofrecía un `findPartition` en tiempo constante y un `merge` en tiempo lineal en el peor de los casos. Sin embargo, el coste lineal de la fusión (al tener que actualizar el puntero de mapa para cada elemento de la lista pequeña) se vuelve prohibitivo en aplicaciones con millones de elementos y miles de fusiones. La pregunta clave es: **¿podemos mejorar la complejidad de todas las operaciones, no solo de `merge` sino también de `findPartition` y de `areDisjoint`?**  

La respuesta es sí: si en lugar de representar cada partición como una lista, la representamos como un **árbol** (o, en realidad, un bosque de árboles), podemos distribuir el coste de las operaciones de forma mucho más equilibrada. Cada partición se identifica con la raíz de su árbol asociado, y cada nodo almacena únicamente un enlace a su padre. Al mantener los árboles razonablemente balanceados, las operaciones de recorrido (subir del nodo a la raíz) serán logarítmicas en promedio, y las fusiones podrán realizarse en tiempo constante más el coste de recorrer las dos rutas hasta las raíces.  

#### 2. Representación básica del árbol  

En la nueva aproximación:  

- **parentsMap** (antes `partitionsMap`) es un mapa que, para cada elemento, almacena su padre en el árbol.  
- Inicialmente, cada elemento es su propio padre, es decir, cada árbol sólo tiene un nodo y su raíz es él mismo.  
- No se guardan enlaces a hijos, porque las únicas operaciones necesarias son subir al padre y, eventualmente, reajustar ese enlace.  

Con esta representación, identificar la partición de un elemento `x` equivale a subir repetidamente desde `x` a `parentsMap[x]`, hasta llegar a un nodo que sea su propio padre. Esa raíz es el identificador único de la clase de equivalencia.  


#### 3. Implementación ingenua de `findPartition` sobre árboles  

El pseudocódigo para la nueva versión de `findPartition` es:  

```  
function findPartition(elem):  
    throw-if (elem == null or not parentsMap.has(elem))  
    parent <- parentsMap[elem]  
    if parent != elem then  
        parent <- findPartition(parent)  
    return parent  
```  

1. **Validación**: se lanza error si `elem` es nulo o no existe en el mapa.  
2. **Lectura del padre**: `parentsMap[elem]`.  
3. **Caso base**: si el padre es el mismo elemento, hemos alcanzado la raíz, la partición.  
4. **Recursión**: si no, subimos un nivel y seguimos buscando la raíz.  

Cada llamada recursiva equivale a subir un nivel en el árbol, por lo que el tiempo de ejecución es proporcional a la **altura** del árbol.
En el peor caso, si el árbol está completamente desbalanceado (por ejemplo, una lista enlazada), la llamada costaría `O(n)`. En promedio, si los árboles son moderadamente balanceados, el coste será `O(log n)`.  


#### 4. Implementación de `merge` sobre árboles  

La versión árbol de `merge` aprovecha directamente la representación de `parentsMap` sin iterar sobre los nodos de una lista:  

```  
function merge(elem1, elem2):  
    p1 <- findPartition(elem1)  
    p2 <- findPartition(elem2)  
    if p1 == p2 then  
        return false  
    parentsMap[p2] <- p1  
    return true  
```  

1. Se obtienen las raíces `p1` y `p2` de los dos elementos.  
2. Si coinciden, no hay fusión necesaria.  
3. Si son distintas, basta con hacer que la raíz de uno (`p2`) apunte a la raíz del otro (`p1`).  

Así, el único coste adicional al enlace constante de raíz a raíz es el de encontrar ambas raíces, es decir, dos veces `findPartition`. 
En el peor caso, sigue siendo `O(n)` por la posible altura de los árboles; en promedio `O(log n)`.  

#### 5. Balanceo por rango (union by rank)  

Para garantizar alturas logarítmicas en el peor caso —y por tanto un coste siempre `O(log n)` para `findPartition` y `merge`— se introduce la primera heurística: **balanceo por rango**.  

#### 5.1 Idea principal  

- A cada raíz de árbol se le asocia un **rango** (o "rank"), que inicialmente vale 1 en un nodo aislado.  
- Al fusionar dos árboles, en lugar de empotrar siempre uno bajo el otro de forma fija, se **elige como nueva raíz** el árbol que tenga **mayor rango**, y se cuelga el otro como subárbol de éste.  
- Si ambos rangos son iguales, podemos elegir arbitrariamente uno como nuevo padre y **aumentar en 1** el rango de la nueva raíz.  

#### 5.2 Garantías de altura  

Se puede demostrar por inducción que, con esta estrategia, la altura de cualquier árbol de k nodos nunca supera `⌊log⁡_2 k⌋+ 1`. Por ejemplo:  

- Dos árboles de rango 3 (cada uno con al menos 4 nodos) se unen y forman un árbol de rango 4; su altura crece en 1.  
- Si un árbol de rango 5 (≥ 16 nodos) engulle a uno de rango 3 (≥ 8 nodos), la altura del primero no cambia.  

En consecuencia, **el peor caso de altura** de un árbol con n nodos es `O(log n)`.  

#### 6. Compresión de caminos (path compression)  

Aunque el balanceo por rango asegura `log n` como cota superior de altura, podemos **acercarnos aún más** a tiempo prácticamente constante con una segunda heurística: la **compresión de caminos**.  

#### 6.1 Mecanismo  

- En lugar de esperar a `merge` para actualizar ráiz de todos los nodos de un subárbol, dejamos intactos sus `parentsMap` durante la fusión.  
- En cada llamada a `findPartition(x)`, una vez que encontramos la raíz `r`, **retrocedemos** desde `x` hasta `r` actualizando el padre de cada nodo intermedio para que apunte **directamente** a `r`.  

El pseudocódigo modificado de `findPartition` con compresión de caminos es:  

```  
function findPartition(elem):  
    throw-if (elem == null or not parentsMap.has(elem))  
    info <- parentsMap[elem]           // ahora guardamos un objeto Info  
    if info.root != elem then  
        info.root <- findPartition(info.root)  
    return info.root  
```  

Aquí, `info.root` se actualiza tras la llamada recursiva para que `elem` apunte directamente a la raíz.  

#### 6.2 Efecto amortizado  

Gracias a esta heurística, cualquier cadena de llamadas posteriores a `findPartition` sobre nodos ya "comprimidos" tardará **un único** acceso: ir de x a `parentsMap[x]`, ya igual a la raíz.  

El análisis amortizado demuestra que, tras una secuencia de m operaciones (`findPartition` y `merge`) sobre n elementos, el número total de accesos a `parentsMap` es  
`O(m.α(n)`, donde `α(n)` es la función inversa de Ackermann, cuyo crecimiento es tan lento que para cualquier `n` realista `α(n)≤ 5`. En la práctica, esto significa **costo efectivo constante** para cada operación.  


#### 7. Estructura auxiliar `Info`  

Para implementar simultáneamente ambas heurísticas, balanceo por rango y compresión de caminos  necesitamos almacenar dos datos por elemento:  

1. **root**: el identificador de la raíz actual (para compresión de caminos).  
2. **rank**: un entero que indica el "rango" del árbol en ese nodo (solo válido en raíces).  

En el código, se encapsula esta información en una clase interna:  

```  
class Info:  
    function Info(elem):  
        throw-if elem == null  
        this.root <- elem     // cada nodo empieza siendo raíz de sí mismo  
        this.rank <- 1        // rango inicial = 1  
```  

Y `parentsMap: HashMap<Elemento, Info>` asocia cada elemento con su objeto `Info`. Así:  

- En el constructor de `DisjointSet` y en `add(elem)`, ahora hacemos  
  ```  
  parentsMap[elem] = new Info(elem)  
  ```  
- En `findPartition`, recuperamos `info = parentsMap[elem]`, comprobamos `info.root`, recursamos y luego actualizamos `info.root`.  
- En `merge`, tras encontrar las raíces `r1` y `r2`, comparamos `info1.rank` y `info2.rank`:  
  - Si `rank1 > rank2`, colgamos `r2` bajo `r1`.  
  - Si `rank2 > rank1`, colgamos `r1` bajo `r2`.  
  - Si son iguales, elegimos uno como nuevo padre y aumentamos su `rank` en 1.  


#### 8. Pseudocódigo final de `merge` con heurísticas  

```  
function merge(elem1, elem2):  
    r1 <- findPartition(elem1)  
    r2 <- findPartition(elem2)  
    if r1 == r2:  
        return false  

    info1 <- parentsMap[r1]  
    info2 <- parentsMap[r2]  

    // Unión por rango  
    if info1.rank < info2.rank:  
        info1, info2, r1, r2 = info2, info1, r2, r1  // intercambiar roles  
    parentsMap[r2].root = r1     // cuelga r2 bajo r1  

    // Si rangos iguales, elevar rango de la nueva raíz  
    if info1.rank == info2.rank:  
        info1.rank += 1  

    return true  
```  

1. **Obtención de raíces** con posibles compresiones parciales.  
2. **Comparación de rangos** para decidir cuál árbol "absorbe" al otro.  
3. **Actualización de `root`** solo para la raíz de menor rango, en `O(1)`.  
4. **Incremento de rango** en caso de empate, en `O(1)`.  

De este modo, `merge` combina tanto la búsqueda de raíces como el enlace en un coste amortizado `O(α(n))`.  


#### 9. Complejidad amortizada y ventajas prácticas  

Con ambas heurísticas activas:

- **`findPartition`**: amortizado `O(α(n))`.  
- **`merge`**: amortizado `O(α(n))`.  
- **`areDisjoint`**: dos búsquedas de raíz, `O(α(n))`.  

Dado que `α(n)` para cualquier `n` típico es menor que `5`, podemos considerar estas operaciones **prácticamente constantes**. Esto hace posible emplear conjuntos disjuntos en aplicaciones críticas (motores de clustering, detección de ciclos en grafos, algoritmos de Kruskal para árboles de expansión mínima, estructuras de conectividad dinámica, etc.) con garantías de rendimiento muy altas.  

Además, la complejidad real del código adicional para mantener rangos y realizar compresión de caminos es mínima, ¿por qué?.

#### 10. Consideraciones de implementación y memoria  

- **Uso de `Info` versus dos mapas**: Agrupar `root` y `rank` en un solo objeto evita almacenar la misma clave varias veces y reduce el overhead de memoria.  
- **Claves no numéricas**: La solución general con `HashMap<Elemento,Info>` funciona con cualquier tipo `Elemento` que implemente correctamente `equals`/`hashCode` (o equivalente en cada lenguaje).  
- **Coste de objetos**: Aunque cada `Info` es un objeto extra, su peso en memoria es amortiguado por la reducción de duplicidad de claves. Para aplicaciones extremas, se podría usar un wrapper de clave para almacenar referencias en lugar de valores, pero suele no valer la pena el aumento de complejidad.  
- **Recursividad en `findPartition`**: En entornos con límites estrictos de pila, puede reemplazarse por un bucle `while` y luego una segunda pasada para la compresión de caminos.  

#### 11. Plan de adopción en aplicaciones  

Para incorporar esta estructura en un sistema real, bastan unos pocos pasos:  

1. **Definir la clase** `DisjointSet<T>` con `HashMap<T,Info> parentsMap`.  
2. **Implementar**:  
   - Constructor (`initialSet` o vacío).  
   - `add(elem)`.  
   - `findPartition(elem)` con compresión de caminos.  
   - `merge(elem1,elem2)` con unión por rango.  
   - `areDisjoint(elem1,elem2)` reutilizando `findPartition`.  
3. **Probar exhaustivamente** con test unitarios que verifiquen:  
   - Elementos aislados (singleton).  
   - Fusiones sucesivas.  
   - Idempotencia de `merge`.  
   - Correcta compresión de caminos (altura ≤2 tras búsquedas).  
4. **Medir rendimiento** en escenarios sintéticos de gran escala (por ejemplo, `n=10^7` elementos, `m=10^7` fusiones), para validar el tiempo real por operación.  

