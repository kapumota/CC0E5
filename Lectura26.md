### **SS-Tree: contexto, estructura y operaciones**

#### **Contexto y motivación de los árboles de búsqueda por similitud**

En aplicaciones como recuperación de imágenes, recomendación de productos o búsquedas geoespaciales, necesitamos estructuras capaces de responder consultas
de **vecinos más cercanos** (nearest neighbor), **búsquedas de rango** (region search) y, en tiempo real, versiones **aproximadas** de estas búsquedas. 

Si bien los **k-d trees** funcionan bien en pocas dimensiones, su rendimiento se degrada drásticamente con la cantidad de dimensiones (la "maldición de la dimensionalidad").

Los **R-trees** organizan puntos o MBRs (mínimos rectángulos envolventes) en nodos solapados, controlando el crecimiento en dimensiones intermedias. 
Los **SS-trees** generalizan este enfoque liberando la restricción de usar rectángulos alineados a los ejes y empleando en su lugar **esferas** (centroide + radio) como envolventes. 

Este simple cambio: pasar de MBRs a esferas muestra, tanto teórica como empíricamente, una reducción en el número promedio de hojas tocadas por una consulta de vecino más cercano o de rango.

**Parámetros básicos (ejemplo m = 20, M = 50):**

| Parámetro | Descripción                       |
| --------- | --------------------------------- |
| m         | Mínimo de hijos o puntos por nodo |
| M         | Máximo de hijos o puntos por nodo |
| k         | Dimensionalidad del espacio       |

Cada nodo mantiene los atributos:

1. **Centroide**: el punto medio de sus hijos.
2. **Radio**: máxima distancia entre el centroide y cualquiera de los hijos.

Este par $\langle \text{centroide}, \text{radio}\rangle$ define la **esfera** que hace de envolvente.

#### **Estructura de datos y modelo de clases para SS-trees**

En un diseño agnóstico al lenguaje:

* **`SsNode`** (abstracta)

  * Atributos comunes: `children`, `points`, `isLeaf`
  * Métodos: `recalculateCentroid()`, `recalculateRadius()`
* **`SsLeafNode`** y **`SsInternalNode`** heredan de `SsNode`.
* **`SsTree`**

  * Parámetros: `m`, `M`, `k`, y `root`
  * Operaciones: `search()`, `insert()`, `delete()`, `nearestNeighbor()`, `rangeSearch()`

#### **Búsqueda en SS-trees**

#### **Búsqueda exacta (Search)**

Para localizar un punto $Z$:

1. Desde la raíz, **descender** a una hoja siguiendo el hijo cuyo **centroide** esté más cercano a $Z$.
2. Una vez en la hoja, verificar si $Z$ existe.
3. **Backtracking**: después de encontrar un candidato inicial o descender, retroceder y explorar **todas** las ramas cuya esfera tenga distancia $\leq$ a la mejor distancia encontrada.

Este proceso garantiza **completitud**; elimina ramas que no pueden contener $Z$ y explora las que sí, con coste esperado $O(\log n)$ en dimensiones bajas y $O(n)$ en el peor caso si hay solapamientos excesivos.

```pseudocode
function search(node, Z):
    if node.isLeaf:
        return Z ∈ node.points
    else:
        bestChild = argmin_{c ∈ node.children} distance(c.centroid, Z)
        found = search(bestChild, Z)
        if found:
            return true
        // backtracking:
        for each c ≠ bestChild with dist(sphere(c), Z) ≤ bestDistance:
            if search(c, Z): return true
        return false
```

#### **Búsqueda heurística / greedy**

Si, en cambio, aceptamos el **primer** candidato y **no** retrocedemos, renunciamos a la completitud y obtenemos un recorrido único de altura $O(\log_m n)$, sacrificando exactitud por velocidad.

#### Complejidad de las búsquedas

* **Nearest Neighbor**

  * Esperado: $O(\log n)$ en dimensiones bajas.
  * Peor caso: $O(n)$ si hay solapamiento masivo.
* **Range Search**

  * $O(\log n + |R|)$ bajo distribuciones uniformes.

####  **Varianza multidimensional en divisiones**

Para dividir un nodo (heurística **minVarianceSplit**):

1. Calcular la **varianza univariada** de las coordenadas por dimensión (coste *O(kM)*).
2. Elegir la dimensión de máxima varianza.
3. Ordenar hijos según su valor en esa dimensión.
4. Probar divisiones entre índices $i = m..M-m$, sumando varianzas de ambos grupos.

> **Nota**: no usamos la matriz de covarianzas completa  para mantener el cálculo eficiente.

#### **Eliminación y reequilibrio**

Tras eliminar $Z$:

1. Buscar en todas las ramas cuya esfera contenga $Z$.
2. Si la hoja resultante tiene $j < m$:

   * **Borrow**: pedir prestado del hermano que cause **menor expansión del radio** (criterio análogo a R\*-tree).
   * Si no hay préstamo viable: **Merge** con el hermano que minimice la expansión de la esfera resultante.
3. **Backtracking** hasta la raíz si es necesario.

**Estrategias de parada:**

* **Depth-first completo**: explora todas las ramas.
* **Stop at first found**: detiene al encontrar la primera ocurrencia.


#### **Variantes y extensiones: SS⁺-trees**

Los **SS⁺-trees** añaden reinserciones antes de splits:

* **Reinserción al 30 % de ocupación**: extrae entradas para reinsertarlas, reduciendo solapamientos.
* **Diferencias con R\*-tree**: SS⁺ usa esferas; R\* maneja MBRs y reinserciones basadas en solapamiento.
* **Resultados empíricos**: reducción de hasta un 20 % en hojas visitadas frente a SS-tree básica.

*Ejemplo de uso y código en Python disponible en: [Snippet SS-tree básico](https://github.com/kapumota/CC0E5/tree/main/ss-tree).*

### **¿Son los SS-trees mejores?**

Para responder a si los SS-trees superan a k-d trees y R-trees, conviene comparar sus características fundamentales y sus consecuencias sobre el rendimiento:

#### **Comparación con k-d trees**

* **Equilibrado automático**: A diferencia de los k-d trees, donde la división sucede según un eje fijo y puede generar árboles desequilibrados para ciertas
   distribuciones, los SS-trees se auto‐balancean de modo que todas las hojas se encuentran a la misma profundidad.
  Esto garantiza, en promedio, una eficiencia más estable en las operaciones de búsqueda e inserción.
* **Evitar la maldición de la dimensionalidad**: Las particiones unidimensionales en k-d trees se realizan siempre a lo largo de un solo eje, por lo que en
   espacios de alta dimensión el número de regiones crece exponencialmente y la utilidad de cada división disminuye.
  En los SS-trees, las envolventes esféricas agrupan puntos en todas las direcciones simultáneamente, lo que tiende a reducir la complejidad de las  particiones en espacios multidimensionales.

#### **Comparación con R-trees**

* **Forma de la envolvente**: Los R-trees emplean hiperro­ctángulos, que pueden ajustar asimétricamente su volumen en cada dimensión, adaptándose mejor a
  distribuciones sesgadas. Las hiperesferas, por simetría, definen la misma distancia en todas las direcciones, lo que puede implicar que zonas sin puntos
   queden "vacías" dentro de la esfera y representen espacio desperdiciado.
* **Cálculo de distancia más sencillo**: La distancia al centro de una esfera se calcula mediante la norma Euclidiana, sin necesidad de manejar dimensiones
   independientes.Esto permite, por ejemplo, aprovechar aceleraciones de hardware o simplificar la evaluación de si un punto está dentro o fuera de la región.
* **Volumen y crecimiento en alta dimensión**: En un espacio de `k` dimensiones, el volumen de una esfera de radio `r` crece proporcionalmente al radio elevado a la k-ésima potencia, multiplicado por un factor fijo que depende de `k` (ese factor combina $\pi$ y la función gamma). Por su parte, el volumen de un cubo que mida dos veces el radio en cada dimensión crece proporcionalmente a la misma potencia del radio, pero multiplicada por dos elevado a `k`.

Como ese factor fijo de la esfera resulta siempre menor que dos elevado a `k` cuando la dimensión `k` es al menos uno, el volumen de la esfera crece más despacio que el volumen del cubo. En la práctica, esto implica que, cuando los puntos de los datos forman agrupaciones aproximadamente esféricas, emplear envolventes hiperesféricas genera menos espacio vacío y por tanto menos desperdicio que usar hipercubos.

#### **Comportamiento en el peor caso**

Ni los SS-trees ni los R-trees garantizan tiempos de búsqueda logarítmicos en el peor caso. En escenarios adversos, es posible que haya que recorrer todas las hojas (hasta *n*/m, donde *n* es el número de puntos y *m* la capacidad mínima de un nodo), resultando en costes lineales. 
A continuación se muestra una tabla comparativa de la complejidad teórica de las principales operaciones:

| Operación            | k-d tree       | R-tree | SS-tree |
| -------------------- | -------------- | ------ | ------- |
| Búsqueda (search)    | O(log n)       | O(n)   | O(n)    |
| Inserción (insert)   | O(log n)       | O(n)   | O(n)    |
| Eliminación (remove) | O(n^{1-1/k})   | O(n)   | O(n)    |
| nearestNeighbor      | O(2^k + log n) | O(n)   | O(n)    |
| pointsInRegion       | O(n)           | O(n)   | O(n)    |

Se observa que, a pesar de las mejoras en la forma de los nodos, la complejidad asintótica en el peor caso sigue siendo lineal para R-trees y SS-trees. 
No obstante, los SS-trees suelen mostrar un rendimiento práctico superior en búsquedas típicas, dado que atraviesan menos hojas gracias a la menor superposición.

#### **Mitigación de las limitaciones de las hiperesferas**

Aunque las hiperesferas ofrecen ventajas en distribuciones uniformes, cuando los datos se distribuyen de forma sesgada o en forma alargada surgen ineficiencias: la esfera mínima que cubre un conjunto de puntos, calculada habitualmente con centro en el centro de masas y radio igual a la distancia al
punto más lejano suele dejar huecos vacíos significativos. Para atajar este problema se han propuesto dos aproximaciones principales:

#### **Uso de elipsoides**

En lugar de hiperesferas, usar ellipsoides permite ajustar el radio en cada dirección de forma independiente, adaptándose mejor a grupos elongados. 
No obstante, el cálculo de la distancia entre un punto de consulta y la frontera del elipsoide, situada a lo largo de la dirección desde el centro al punto, 
requiere proyectar el vector de diferencia sobre un eje arbitrario. 

Esto complica tanto la indexación como la búsqueda, encareciendo la evaluación de pertenencia al elipsoide y anulando parte de las ventajas de eficiencia delas esferas.

#### **Aproximación de la esfera mínima envolvente**

Calcular la esfera de radio mínimo que cubra exactamente todos los puntos de un clúster es un problema de complejidad exponencial en la dimensión. 
Sin embargo, se puede emplear un método aproximado:

1. Partir del **centro de masas** de los puntos como centro inicial de la esfera.
2. Iterativamente desplazar el centro en dirección al punto actualmente más lejano.
3. En cada iteración, reducir el tamaño máximo del desplazamiento proporcional al avance previo, garantizando convergencia.

Este algoritmo no garantiza un óptimo global exacto, pero produce una esfera de volumen significativamente menor que la definida por el radio máximo desde el centro de masas. 
Su coste, aunque mayor que el de la esfera trivial, resulta asumible para nodos de tamaño moderado, y amortiza en búsquedas posteriores.

#### **Heurística mejorada de partición en SS+-trees**

La construcción dinámica de un SS-tree implica dividir nodos que exceden su capacidad máxima *M*, así como fusionar o redistribuir puntos cuando quedan por 
debajo de la mínima *m*. 
Estas operaciones, si se basan únicamente en particiones ortogonales o en la máxima varianza unidimensional, pueden producir grupos desiguales o con mucho solapamiento. Para mejorar la calidad de las divisiones, SS+-trees introducen la siguiente heurística de split:

#### **Objetivo de la heurística**

Encontrar dos subgrupos de puntos que:

* **Sean lo más homogéneos posible**, agrupando puntos cercanos.
* **Respeten la capacidad** máxima de cada nodo (*M* puntos).

### **Implementación mediante k-means**

1. **Número de clústeres** fijo a *k* = 2.
2. **Límite superior** de puntos por clúster igual a *M*.
3. Se ejecuta k-means sobre el conjunto de *M + 1* puntos que desencadenan el split.
4. Cada iteración reagrupa puntos según el centroide más próximo, hasta convergencia o tras un máximo de *j* iteraciones.

El coste de k-means en este caso es O(*j d M*), frente a O(*d M*) de la heurística original de partición basada en varianza unidimensional (que calcularía unipso'). 
Aunque la complejidad aumenta linealmente con el número de iteraciones, la calidad de la partición, medida en reducción de solapamiento y tamaño de envolventes,  mejora notablemente, amortizando el coste en operaciones de búsqueda posteriores.

#### **Ventajas**

* **Reducción del solapamiento**: Al agrupar puntos realmente cercanos, las esferas resultantes solapan menos.
* **Mayor equilibrio**: Evita la creación de grupos muy desiguales en tamaño o distribución.
* **Flexibilidad**: Ajustando *j*, se equilibra calidad de la partición y coste de cómputo.

#### **Reducción del solapamiento entre nodos**

Aunque la heurística de split mejora significativamente las divisiones iniciales, operaciones posteriores (fusiones, redistribuciones, movimientos de puntos) pueden reintroducir solapamiento. Para combatir este fenómeno, SS+-trees incorporan un mecanismo de **reorganización**:

#### **Detección de solapamiento significativo**

Se comprueba si alguno de los envolventes hiperesféricos está completamente contenido en otro o si el solapamiento excede un umbral. 

Para evitar el cálculo exacto de la intersección de dos hiperesferas en *k* dimensiones que requiere evaluar integrales complejas se emplea un criterio aproximado:

* Sean dos esferas de radios *R* y *r* (*R* ≥ *r*) y centros separados por distancia *d*.
* Si *d* ≤ (*R* - *r*) · *τ*, con *τ* un factor de tolerancia cercano a 1, se considera que hay solapamiento excesivo o inclusión.

#### **Heurística de reorganización**

Cuando la detección supera el umbral, se aplica un proceso similar a k-means, pero esta vez sobre las **nietas** de un nodo *N*:

1. Recopilar los puntos o centroides de los hijos de los hijos de *N*.
2. Ejecutar k-means con *k* igual al número de hijos originales de *N*.
3. Reemplazar los hijos de *N* por las nuevas agrupaciones obtenidas.

Este mecanismo redistribuye de forma global las regiones de *N*, reduciendo la varianza y el solapamiento. Dado su coste O(*j M k*), se recomienda:

* **Aplicarlo con moderación**, por ejemplo tras operaciones de split o tras acumular suficientes inserciones/eliminaciones en el subárbol.
* **Introducir umbrales** de número de operaciones antes de disparar la reorganización.

Así se evita un sobrecoste continuo y se optimiza el árbol sólo cuando el beneficio potencial justifica el esfuerzo.

### **Aplicaciones de la búsqueda de vecinos más próximos**

La estructura SS+-tree, con sus envolventes esféricas y sus heurísticas avanzadas, resulta adecuada para múltiples escenarios donde se requieren consultas de proximidad o regiones en espacios de alta dimensión:

1. **Recuperación de imágenes por contenido (CBIR)**: Los descriptores visuales (SIFT, SURF, histogramas de color) suelen vivir en espacios de 64-256 dimensiones. Un índice que minimice solapamiento acelera la búsqueda de las imágenes más similares.
2. **Sistemas de recomendación**: Al modelar usuarios y productos mediante vectores de características (latentes o explícitas), una búsqueda de *k* vecinos más próximos permite sugerir ítems similares con baja latencia.
3. **Búsqueda geoespacial** en múltiples atributos: Cuando se combinan coordenadas geográficas con otras dimensiones (hora, tipo de punto de interés, valor de precio), las hiperesferas facilitan consultas regionales.
4. **Minería de datos y detección de anomalías**: Agrupar datos de sensores o transacciones financieras y detectar puntos fuera de la esfera envolvente propia sirve para identificar anomalías.
5. **Aprendizaje basado en instancias** (kNN): Modelos de clasifcación/regresión que, en tiempo de predicción, buscan los vecinos más cercanos para determinar la etiqueta o valor. Índices eficaces son esenciales para que estos métodos escalen.

En todos estos casos, la minimización del número de nodos recorridos y por tanto del número de lecturas de disco o memoria  se traduce en mejoras directas de rendimiento y escalabilidad. Los SS+-trees, mediante sus prácticas de balanceo y minimización de solapamientos, ofrecen una base sólida para implementar sistemas de búsqueda de vecinos más próximos que mantengan un buen rendimiento incluso en dimensiones elevadas y distribuciones complejas.

#### **Recomendaciones para la implementación**

* **Primera fase**: Implementar un SS-tree básico con envolventes hiperesféricas centradas en el centro de masas y división sencilla por varianza máxima.
* **Perfilado**: Medir el número de nodos visitados por consulta y la distribución de los radios en su aplicación real.
* **Optimización progresiva**: Si el SS-tree resulta un cuello de botella (más de un 5-10 % del tiempo de consulta), introducir primero la heurística k-means para splits.
* **Reorganizaciones selectivas**: Aplicar el chequeo de solapamiento y reorganización sólo tras operaciones de split o tras superar un umbral de actualizaciones en un subárbol.
* **Aproximación de mínima esfera**: Considerar, según presupuesto de cómputo, la aproximación iterativa al menor radio para nodos críticos.

Con este enfoque gradual y basado en mediciones, podrás aprovechar al máximo las ventajas de SS+-trees sin incurrir en sobrecostes innecesarios, adaptando la complejidad del índice a las necesidades reales de tu aplicación.


**Referencias**

* [Fast and Robust Smallest Enclosing Balls](https://people.inf.ethz.ch/gaertner/subdir/texts/own_work/esa99_final.pdf).
* [The SS+ -tree: An Improved Index Structure for Similarity Searches in a High-Dimensional Feature Space](https://www.researchgate.net/profile/Jesse-Jin-3/publication/2332909_The_SS-tree_An_Improved_Index_Structure_for_Similarity_Searches_in_a_High-Dimensional_Feature_Space/links/546e22390cf2b5fc17604581/The-SS-tree-An-Improved-Index-Structure-for-Similarity-Searches-in-a-High-Dimensional-Feature-Space.pdf)

