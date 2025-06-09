### Listas de ejercicios

Utiliza las implementación dadas en clase: [kd-tree](https://github.com/kapumota/CC0E5/blob/main/kd-tree.py), 
[ball-tree](https://github.com/kapumota/CC0E5/blob/main/ball-tree.py), [cover-tree](https://github.com/kapumota/CC0E5/blob/main/cover-tree.py)

**1. Análisis de complejidad teórica**

1.1 **Construcción**

* Partiendo de *n* puntos en ℝᵏ, compara cómo crece el tiempo de construcción de un kd-tree (con ordenación por eje o selección de mediana), un ball-tree (que calcula radios y centroides en cada partición) y un cover-tree (cuyos niveles de escala dependen de la distribución). Reflexiona sobre el coste en el peor caso (por ejemplo, datos ordenados o muy concentrados) frente al promedio, y valora también el espacio ocupado por cada nodo (coordenadas, punteros, radios, niveles, mapas auxiliares).

1.2 **Consultas de vecino más cercano y por rango**

* Explora por qué la búsqueda 1-NN en baja dimensión suele acercarse a `O(log n)` comparaciones, mientras que en alta dimensión se degrada casi a O(n). Diseña ejemplos (nubes uniformes, datos agrupados) y justifica los números de distancias calculadas en kd-tree, ball-tree y cover-tree.
* A continuación, estima el número de nodos y hojas que visita cada estructura al extraer todos los puntos dentro de un radio *r* dado. ¿En qué situaciones (datos muy dispersos, clusters compactos, alta densidad) cada estructura consigue podas más eficaces?

1.3 **Inserción y eliminación**

* Mide el coste amortizado de insertar puntos uno a uno: en kd-tree sin rebalanceo estricto, en ball-tree actualizando radios y centroides, y en cover-tree con subida de niveles y recalibración de radios. Contrasta inserciones aleatorias con secuencias ordenadas y observa en qué partes del algoritmo se concentra el tiempo.
* Para cover-tree, analiza qué sucede al borrar un punto: ¿cuántos nodos deben reinsertarse y cómo crecen o decrecen los radios de cobertura globales?

**2. Profiling y diagnóstico de rendimiento**

2.1 **Hotspots de CPU**

* Usa herramientas como `cProfile` o decoradores de temporización para determinar cuánto tiempo dedican las implementaciones a la selección de mediana, al cálculo recursivo de subárboles, al cómputo de distancias y a la gestión de radios o heaps. Presenta un breve informe señalando las 3–5 funciones más costosas en cada caso.

2.2 **Huella de memoria**

* Con `tracemalloc`, toma instantáneas antes y después de construir el árbol y de realizar un lote de consultas 1-NN. Compara el consumo total y analiza qué estructuras (listas de puntos, diccionarios como `_index_map`, pilas de llamadas) crecen más al aumentar *n*.

2.3 **Variación con tamaño y dimensión**

* Monta un benchmark que evalúe tiempo de construcción, tiempo medio de consulta y pico de memoria para *n* en {10³, 10⁴, 10⁵, 10⁶} y dimensión *k* en {2, 10, 25, 50}. Resume los resultados en tablas o gráficos que muestren claramente cómo cada estructura llega a su límite práctico.

**3. Benchmarking comparativo**

3.1 **Generación de datos de prueba**

* Crea datasets sintéticos que abarcan casos extremos: puntos uniformes en un hipercubo (poca estructura), gaussianos multivariados (alta concentración) y clusters bien separados. Justifica cómo cada patrón de datos afecta la eficacia de poda y partición.

3.2 **Métricas de eficiencia**

* Para cada estructura y cada caso de datos, mide en repetidas corridas (≥ 30):

  * Tiempo de construcción y de consulta 1-NN / rango.
  * Número de distancias calculadas vs. número de puntos finalmente devueltos.
  * Desviación estándar de los tiempos.

3.3 **Visualización e interpretación**

* Prepara gráficas log-log de tiempo vs. *n* y tiempo vs. *k*, así como diagramas de cajas para la variabilidad. Señala en los plots dónde una estructura supera a otra y explica los puntos de inflexión.


**4. Propuestas de mejora de las implementaciones**

4.1 **Selección de pivote en kd-tree**

* Comprueba si emplear el algoritmo "median-of-medians" (`O(n)`) en lugar de ordenar completamente (`O(n log n)`) reduce el tiempo de construcción y si ello impacta en la eficiencia de las podas.

4.2 **Vectorización o Cython**

* Piensa en reemplazar bucles de cálculo de distancias y de actualización de radios en ball-tree y cover-tree por operaciones vectoriales de NumPy o módulos compilados con Cython/Numba, para reducir el overhead de Python puro.

4.3 **Paralelización**

* Propón un esquema de distribución de trabajo en múltiples procesos o nodos (por ejemplo, usando `multiprocessing.Pool` o Dask): ¿cómo dividir el espacio o las consultas sin perder la coherencia del índice?

4.4 **Caching y poda basada en densidad**

* Diseña un pequeño sistema de cache (p. ej. LRU) para memorizar distancias ya calculadas en cover-tree y define criterios adaptativos de poda (ajustar el radio según la densidad local de puntos) que reduzcan las búsquedas redundantes.

**5. Aplicaciones en aprendizaje automático y datos masivos**

5.1 **Clasificador K-NN**

* Simula cómo cambiarían precisión y latencia al usar tus árboles frente a un enfoque brute-force o al índice de scikit-learn para datasets reales (MNIST reducido, CIFAR-10).

5.2 **Inicialización de k-means++**

* Aprovecha la estructura de vecinos más lejanos para acelerar la fase de selección de centroides en k-means++, midiendo tiempo de inicialización y calidad final de clustering.

5.3 **Recomendaciones con embeddings**

* Diseña un servicio que responda en milisegundos consultas de vecinos sobre embeddings de 100–300 dimensiones (usuarios/productos), y mide throughput (QPS) en cargas concurrentes.

5.4 **Integración como índice espacial**

* Explica cómo mapear operaciones de árbol a consultas SQL (PostgreSQL) o REST (Elasticsearch) y qué desafíos de consistencia y shards surgen en entornos distribuidos.

5.5 **Pipeline distribuido**

* Esboza un flujo de datos (Kafka -> Spark/Dask -> construcción del índice -> consultas en tiempo real) y analiza requisitos de serialización de árboles, persistencia y actualizaciones en streaming.

**6. La "maldición de la dimensionalidad"**

6.1 **Degradación de la distancia**

* Mide cómo se acorta la diferencia relativa entre el primer y el décimo vecino conforme aumenta *k*, y determina a partir de qué dimensión (p. ej. *k* > 20) cobra sentido cambiar a métodos aproximados.

6.2 **Umbrales de uso**

* Ejecuta consultas 1-NN a medida que subes *k* y localiza el "punto de quiebre" donde kd-tree, ball-tree o cover-tree dejan de aportar ventaja frente a brute-force.


**7. Búsqueda aproximada y estructuras alternativas**

7.1 **Locality-Sensitive Hashing (LSH)**

* Implementa un esquema LSH ligero para alta dimensión y compara recall\@k y latencia con kd-tree en el mismo dataset.

7.2 **VP-Tree y Annoy**

* Prueba VP-Tree (pivotes por distancia) y Annoy (múltiples árboles aleatorios), midiendo facilidad de uso, precisión y latencia, y propone criterios (tamaño de datos, *k*, requerimientos de latencia) para elegir entre estas y kd-/ball-/cover-trees.

