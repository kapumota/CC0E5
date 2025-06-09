### **Estructuras de datos espaciales: Kd-Tree, Ball-Tree y Cover-Tree**

En el campo de la informática, la búsqueda de puntos cercanos en un conjunto de datos es un problema fundamental, especialmente en áreas como el aprendizaje automático y las bases de datos. Para resolver este problema de manera eficiente, se han desarrollado diversas estructuras de datos espaciales. Entre las más destacadas se encuentran los **Kd-Trees**, **Ball-Trees** y **Cover-Trees**. 

#### **Glosario de términos clave**

* **Hiperesfera**: Una generalización de una esfera a cualquier número de dimensiones. En un Ball-Tree, cada nodo representa una hiperesfera que encierra un subconjunto de puntos.
* **Poda (Pruning)**: El proceso de eliminar ramas enteras de un árbol de búsqueda que no pueden contener un resultado mejor que el ya encontrado. Es la clave para la eficiencia de estas estructuras.
* **Métrica de distancia**: Una función que define la "distancia" entre dos puntos en un espacio (ej. Euclidiana, Manhattan).
* **Dimensión intrínseca**: Una medida de la complejidad o grados de libertad de los datos, que puede ser mucho menor que la dimensión del espacio en el que residen (dimensión extrínseca).
* **k-NN (k-Nearest Neighbors)**: Algoritmo que busca los 'k' puntos más cercanos a un punto de consulta dado.

#### **1. Kd-Tree (árbol de k-dimensiones)**

El **Kd-Tree** organiza puntos en un espacio k-dimensional mediante particiones recursivas a lo largo de los ejes de coordenadas. En cada nivel, se elige un eje y se utiliza la mediana de los puntos para dividir el espacio en dos con un hiperplano.

#### **Análisis de complejidad**

* **Complejidad temporal:**
    * **Construcción**: $O(k \cdot n \log n)$, donde 'n' es el número de puntos y 'k' la dimensionalidad. Encontrar la mediana en cada paso toma tiempo lineal.
    * **Búsqueda k-NN (promedio)**: $O(k \log n)$ en espacios de baja dimensión.
    * **Búsqueda k-NN (peor caso)**: $O(k \cdot n)$, especialmente en alta dimensionalidad, donde la poda es ineficaz.
* **Complejidad Espacial**: $O(k \cdot n)$ para almacenar las coordenadas de todos los puntos en el árbol.

#### **Ejemplo de búsqueda 1-NN (vecino más cercano)**

Imaginemos un Kd-Tree con los puntos `A(2,3)`, `B(5,4)`, `C(9,6)`, `D(4,7)`, `E(8,1)`, `F(7,2)`. El punto raíz es `F(7,2)` (división en eje x). La consulta es para `Q(8,5)`.

1.  **Descenso**:
    * Empezamos en la raíz `F(7,2)`. `Q(8,5)` tiene x=8 > 7, vamos a la derecha.
    * El nodo derecho es `C(9,6)` (división en eje y). `Q(8,5)` tiene y=5 < 6, vamos a la izquierda.
    * Llegamos a una hoja. Supongamos que es `E(8,1)`.

2.  **Actualización y poda**:
    * **Mejor candidato actual**: `E(8,1)`. Distancia a `Q(8,5)` es `4.0`. Creamos un radio de búsqueda de `4.0` alrededor de `Q`.
    * **Retrocedemos (backtracking)** al nodo padre `C(9,6)`.
    * Calculamos la distancia a `C`: `dist(Q, C) = dist((8,5), (9,6)) = sqrt(1^2 + 1^2) = 1.41`.
    * `1.41 < 4.0`, así que `C(9,6)` es el **nuevo mejor candidato**. Actualizamos el radio de búsqueda a `1.41`.
    * Ahora revisamos si la otra rama de `C` (la derecha) podría contener un punto mejor. La división fue en el eje `y=6`. La distancia desde `Q(8,5)` hasta este plano de división es `|5-6| = 1`.
    * Como `1 < 1.41` (distancia al plano < radio actual), **debemos explorar** la otra rama. Supongamos que está vacía.
    * **Retrocedemos** a la raíz `F(7,2)`.
    * `dist(Q, F) = dist((8,5), (7,2)) = sqrt(1^2 + 3^2) = 3.16`. No es mejor que `1.41`.
    * Revisamos la otra rama de `F` (la izquierda). La división fue en el eje `x=7`. La distancia de `Q(8,5)` al plano es `|8-7| = 1`.
    * Como `1 < 1.41`, **debemos explorar** la rama izquierda. Tras explorarla (con los puntos A, B, D), no encontraremos ningún punto a una distancia menor a `1.41`.

3.  **Resultado**: El vecino más cercano es `C(9,6)`.


#### **2. Ball-Tree (árbol de bolas)**

Un **Ball-Tree** particiona los datos en hiperesferas anidadas. Cada nodo define una hiperesfera (con un centroide y un radio) que contiene a todos sus puntos hijos.

#### **Análisis de complejidad**

* **Complejidad temporal:**
    * **Construcción**: $O(k \cdot n \log n)$.
    * **Búsqueda k-NN**: $O(k \log n)$, y su rendimiento se degrada más lentamente que el del Kd-Tree en dimensiones altas.
* **Complejidad espacial**: $O(k \cdot n)$, ya que además de los puntos se deben almacenar los centroides y radios de las hiperesferas.

#### **Ajuste de parámetros**

El parámetro clave es el **umbral de hoja (`leaf_size_threshold`)**, que indica el número máximo de puntos en un nodo hoja.
* **Umbral bajo**: Crea un árbol más profundo, con más nodos. La construcción es más lenta, pero las consultas pueden ser más rápidas porque las hiperesferas son más pequeñas y ajustadas, permitiendo una poda más agresiva.
* **Umbral alto**: Crea un árbol más superficial. La construcción es rápida, pero las consultas pueden ser más lentas, ya que en las hojas se debe realizar una búsqueda lineal sobre más puntos.

#### **Pseudocódigo de búsqueda k-NN con Poda**

La búsqueda se realiza con una cola de prioridad (heap) para visitar siempre el nodo más prometedor primero.

```pseudocode
funcion busqueda_knn(query_point, k):
  // El heap almacena tuplas (distancia, nodo)
  // Almacena las distancias negativas para simular un max-heap
  // que guarde los k mejores candidatos.
  mejores_candidatos = nuevo MaxHeap(k) 
  
  // La cola de búsqueda prioriza nodos más cercanos a Q.
  cola_de_busqueda = nuevo MinHeap()
  cola_de_busqueda.push((0.0, nodo_raiz))

  while not cola_de_busqueda.is_empty():
    (dist_a_nodo, nodo_actual) = cola_de_busqueda.pop()

    // --- Poda principal ---
    // Si la distancia al nodo más cercano en la cola
    // es mayor que la distancia al k-ésimo vecino encontrado,
    // ningún otro nodo en la cola podrá mejorar el resultado.
    if dist_a_nodo > mejores_candidatos.peek_largest_distance():
      break // Podemos terminar la búsqueda

    if nodo_actual es una hoja:
      para cada punto p en nodo_actual.puntos:
        dist_a_p = distancia(query_point, p)
        mejores_candidatos.push(p, dist_a_p)
    else: // Es un nodo interno
      // Empujar a los hijos a la cola, priorizando el más cercano
      dist_hijo1 = distancia(query_point, nodo_actual.hijo1.centroide)
      dist_hijo2 = distancia(query_point, nodo_actual.hijo2.centroide)
      cola_de_busqueda.push((dist_hijo1, nodo_actual.hijo1))
      cola_de_busqueda.push((dist_hijo2, nodo_actual.hijo2))
      
  return mejores_candidatos.get_all()
```
**La poda ocurre implícitamente**: Si la distancia desde el punto de consulta hasta el **límite** de una hiperesfera (`distancia(query, nodo.centroide) - nodo.radio`) es mayor que la distancia al k-ésimo vecino más lejano encontrado hasta ahora, esa hiperesfera (y todas sus hijas) no necesita ser explorada. El algoritmo del heap logra esta poda de forma natural.

#### **3. Cover-Tree (árbol de cobertura)**

El **Cover-Tree** es una estructura multinivel basada en escalas. Cada nivel `i` es un "resumen" del nivel `i-1`. Su rendimiento depende de la dimensión intrínseca de los datos.

#### **Análisis de complejidad**

La complejidad depende de una propiedad de los datos llamada **constante de expansión ($c$)**. Para muchos conjuntos de datos del mundo real, $c$ es pequeña.
* **Complejidad temporal:**
    * **Construcción**: $O(c^{12} \cdot n \log n)$. La constante es alta, pero en la práctica es mucho mejor.
    * **Búsqueda k-NN**: $O(c^6 \cdot \log n + k)$. Es independiente de la dimensión extrínseca.
* **Complejidad espacial**: $O(n)$.

#### **Ajuste de parámetros**

El parámetro clave es la **base (`base`)**, que define el factor de escala entre niveles (usualmente 2).
* **Base pequeña (ej. 1.3)**: Más niveles, árbol más "delgado". La poda puede ser más fina, pero la profundidad del árbol aumenta.
* **Base grande (ej. 3.0)**: Menos niveles, árbol más "ancho". Reduce la profundidad, pero cada nodo tiene más hijos, lo que puede ralentizar la búsqueda en cada paso. Una base de **2** es un compromiso estándar y robusto.

#### **Pseudocódigo de búsqueda k-NN**

La búsqueda aprovecha las invariantes de cobertura y separación para descartar candidatos.

```pseudocode
funcion busqueda_knn(query_point, k):
  // Conjunto de candidatos actuales para cada nivel.
  // Empezamos con el conjunto de nodos en el nivel raíz.
  Q_i = {nodos_raiz} 
  
  // Heap para los k mejores resultados encontrados hasta ahora.
  resultados = nuevo MaxHeap(k)

  para i = nivel_maximo hasta nivel_minimo:
    // 1. Crear el conjunto de candidatos para el siguiente nivel inferior.
    // Extendemos el conjunto actual con todos los hijos de los nodos en Q_i.
    Candidatos = Q_i U {hijos de todos los nodos en Q_i}

    // 2. Poda del conjunto de candidatos.
    // Mantenemos solo aquellos cuya distancia al punto de consulta
    // sea menor que la distancia al peor de los k-vecinos actuales.
    // dist_peor_vecino es la distancia al k-ésimo vecino más lejano en 'resultados'.
    dist_peor_vecino = resultados.peek_largest_distance()
    
    Q_i_siguiente = nuevo Set()
    para cada nodo n en Candidatos:
      // --- Poda principal ---
      // Si la distancia al punto del nodo n, menos el radio de cobertura de ese nivel,
      // es mayor que la distancia al peor vecino ya encontrado, no puede haber
      // un punto mejor en la cobertura de n.
      if distancia(query_point, n.point) <= dist_peor_vecino + 2^i:
        Q_i_siguiente.add(n)
        
        // Mientras estamos aquí, intentamos mejorar nuestro conjunto de resultados.
        dist_actual = distancia(query_point, n.point)
        resultados.push(n.point, dist_actual)

    Q_i = Q_i_siguiente

  return resultados.get_all()
```
Este proceso desciende eficientemente a través de las escalas, refinando el conjunto de candidatos en cada nivel gracias a la poderosa poda garantizada por las propiedades del árbol.

#### **Utilidad y aplicaciones en datos masivos y alta dimensionalidad**

En entornos de **datos masivos** y **espacios de alta dimensionalidad**, la elección y configuración de la estructura de índice es crítica para garantizar rendimiento y escalabilidad:

1. **Kd-Tree**:

   * **Limitaciones**: En dimensiones superiores a 20-30, la eficacia de la poda decae y la búsqueda se aproxima a un escaneo lineal.
   * **Aplicaciones**: Ideal para **filtrado previo** en pipelines de ML, **búsqueda espacial** en GIS 2D/3D y **árboles híbridos** con splitting adaptativo en primeros niveles.

2. **Ball-Tree**:

   * **Fortalezas**: Mantiene poda efectiva hasta dimensiones medias (50–100). Soporta métricas diversas.
   * **Casos de uso**: Índices de **vectores de embeddings** en sistemas de recomendación, análisis de **clusters de texto** basado en distancias coseno, preprocesamiento de datos para **t-SNE** o **UMAP**.

3. **Cover-Tree**:

   * **Escalabilidad**: Su complejidad depende de la dimensión intrínseca, no de la extrínseca, por lo que es muy adecuado para **datos altamente redundantes** (p. ej. embeddings multimodales).
   * **Implementaciones**: Usa en bibliotecas como **MLpack**, **Scikit-learn** (opción `leaf_size`), y en frameworks distribuídos (Spark MLlib, H2O) para **búsqueda k-NN escalable**.

