## Miniproyectos  CC0E5

* **Evaluación:** Cada proyecto se califica sobre un máximo de 7 puntos. La calidad de la implementación, las pruebas y el análisis de rendimiento (cuaderno de resultados) constituyen hasta 6 puntos.
* **Presentación:** La entrega del trabajo aporta como máximo 1 punto. La presentación y exposición puntúa sobre 6.

* **Fecha de presentación:** 1 de junio, a partir de las 9:00 am. Y forma parte de un trabajo adicional solicitado relacionado al examen parcial del curso. 

* **Entregable:** Un archivo comprimido contiene el cuaderno de resultados detallado con pruebas funcionales, benchmarking (comparativas de tiempo y uso de memoria) y profiling (análisis de puntos críticos del código).
* **No se presenta el código fuente directamente en la exposición, sino los resultados y análisis.**. El código fuente es un apoyo a tu exposición.


### Miniproyectos propuestos

#### 1. Sistema de consultas geográficas dinámicas 

* **Temas:** Range Tree Dinámico, kd-trees extendidos, Segment Trees (para indexación auxiliar), Disjoint-Set Union con rollback.
* **Descripción:** Implementar un sistema que maneje un conjunto de puntos 2D que pueden añadirse o eliminarse. Debe soportar eficientemente consultas de rango ortogonales (contar/reportar puntos en un rectángulo) y consultas de vecino más cercano. Se utilizará un Range Tree dinámico como estructura principal. Adicionalmente, se explorará el uso de DSU con rollback para gestionar "versiones" temporales del conjunto de puntos y un kd-tree como comparativa.
* **Métricas:** Tiempo de inserción/eliminación, tiempo de consulta de rango, tiempo de consulta NN, uso de memoria, comparación de rendimiento entre Range Tree y kd-tree, impacto del rollback en DSU.

#### 2. Indexación eficiente para big data textual

* **Temas:** Enhanced Suffix Arrays, Wavelet Trees, Range Minimum Query (RMQ) con RMQ-Cartesian Trees, Cuckoo Hashing.
* **Descripción:** Construir un índice para grandes volúmenes de texto que permita búsquedas rápidas de subcadenas, conteo de ocurrencias y consultas de rango sobre el texto (ej. encontrar la k-ésima letra en un rango). Se implementará un Suffix Array mejorado y un Wavelet Tree. Se usará RMQ para acelerar ciertas operaciones y Cuckoo Hashing para gestionar un diccionario auxiliar.
* **Métricas:** Tiempo de construcción del índice, tiempo de búsqueda de patrones, tiempo de consultas de rango, uso de memoria, eficiencia de Cuckoo Hashing (rehashes), comparación con implementaciones más simples.


#### 3. Motor de base de datos In-Memory con soporte transaccional básico

* **Temas:** LSM-Trees (Log-Structured Merge Trees), ART (Adaptive Radix Tree), Bloomier Filters, Path Copying Persistent Union–Find.
* **Descripción:** Diseñar un motor de base de datos clave-valor en memoria. Las inserciones/actualizaciones se gestionarán con una estructura LSM-Tree simulada. Las claves se indexarán usando un ART. Se usarán Bloomier Filters para optimizar las búsquedas antes de acceder a las estructuras principales. Se implementará un DSU persistente para manejar "snapshots" o versiones básicas de la base de datos.
* **Métricas:** Throughput (operaciones/segundo) para inserciones, lecturas y actualizaciones; latencia de cada operación; uso de memoria; efectividad del Bloomier Filter; coste de la persistencia en DSU.

#### 4. Análisis de conectividad en redes sociales dinámicas

* **Temas:** Euler–Tour Trees (o HDT), Fully Dynamic Connectivity, Misra–Gries / Frequent Algorithm, Segment Trees con Lazy Propagation.
* **Descripción:** Simular una red social donde usuarios (nodos) y amistades (aristas) pueden añadirse o eliminarse. El sistema debe mantener la conectividad (¿están dos usuarios conectados?) y responder consultas sobre propiedades de los componentes conexos (ej. tamaño, suma de algún atributo) usando Euler-Tour Trees o una implementación de conectividad dinámica. Se usará Misra-Gries para encontrar los usuarios más "influyentes" (con más conexiones) en tiempo real y Segment Trees para agregar información en los árboles.
* **Métricas:** Tiempo de actualización (añadir/quitar arista/nodo), tiempo de consulta de conectividad, precisión y rendimiento de Misra-Gries, eficiencia de las consultas agregadas con Segment Trees.


#### 5. Sistema de detección de similitud y clustering aproximado

* **Temas:** MinHash / LSH, Count–Min Sketch, Partitioning Trees (ANN), Cuckoo Hashing.
* **Descripción:** Implementar un sistema para encontrar documentos o ítems similares en una colección grande. Se usarán MinHash y LSH para generar "firmas" y agrupar ítems candidatos. Se empleará Count–Min Sketch para estimar frecuencias de características. Para la búsqueda rápida de vecinos aproximados (ANN), se implementará un Partitioning Tree (como un k-d tree o similar) y Cuckoo Hashing para la gestión interna de los buckets de LSH.
* **Métricas:** Precisión vs. Recall en la detección de similitud, tiempo de indexación, tiempo de consulta ANN, precisión de Count-Min Sketch, rendimiento de Cuckoo Hashing.

#### 6. Optimizador de rutas y flujos en redes complejas

* **Temas:** Dinic (o Push–Relabel), A* con Heaps avanzados (Violation Heaps o Lazy Binomial Queues), Johnson’s All-Pairs Shortest Paths, Sparsification Dinámica.
* **Descripción:** Desarrollar una herramienta para analizar redes (transporte, comunicación). Implementar A* usando un heap avanzado para encontrar rutas óptimas. Implementar Dinic para calcular flujos máximos. Usar el algoritmo de Johnson para encontrar todas las rutas más cortas en grafos con pesos negativos (pero sin ciclos negativos). Investigar la esparsificación para acelerar cálculos en grafos densos.
* **Métricas:** Tiempo de cálculo de A*, Dinic y Johnson; comparación de rendimiento entre heaps avanzados y heaps estándar; impacto de la esparsificación en la velocidad y precisión (si aplica); uso de memoria.



#### 7. Procesamiento de streams de datos con estimaciones

* **Temas:** Count–Min Sketch, AMS Sketch, HyperLogLog++, Stream Summary (Space-Saving), Sliding Window Aggregation, Fenwick Trees.
* **Descripción:** Crear una librería para procesar flujos (streams) de datos masivos con memoria limitada. Implementar algoritmos para estimar frecuencias (Count-Min, Space-Saving), momentos (AMS), cardinalidad (HyperLogLog++) y realizar agregaciones sobre ventanas deslizantes. Se usará un Fenwick Tree para algunas agregaciones acumulativas eficientes.
* **Métricas:** Precisión de las estimaciones (error relativo/absoluto), uso de memoria, velocidad de procesamiento (elementos/segundo), rendimiento de las ventanas deslizantes y Fenwick Tree.

#### 8. Estructuras de datos geométricas para modelado 3D 

* **Temas:** Delaunay Triangulation (Bowyer–Watson), Convex Hull (Graham Scan), Dobkin–Kirkpatrick Hierarchy, Orthogonal Range Queries.
* **Descripción:** Implementar un conjunto de herramientas para geometría computacional. Generar triangulaciones de Delaunay para un conjunto de puntos. Calcular la envolvente convexa 3D. Implementar la jerarquía de Dobkin-Kirkpatrick para consultas rápidas de distancia entre poliedros convexos. Añadir soporte para consultas de rango ortogonales en 3D.
* **Métricas:** Tiempo de construcción de Delaunay y Convex Hull, tiempo de consulta de distancia (Dobkin-Kirkpatrick), tiempo de consulta de rango, robustez numérica, uso de memoria.


#### 9. Skip Lists vs. Van Emde Boas Trees para diccionarios ordenados

* **Temas:** Skip Lists, Van Emde Boas Trees, X-Fast Tries (como comparativa teórica o implementación parcial), Dynamic k-ary Heaps.
* **Descripción:** Implementar y comparar el rendimiento de Skip Lists y Van Emde Boas Trees como diccionarios ordenados. Analizar sus complejidades teóricas y medirlas empíricamente para inserciones, eliminaciones, búsquedas y búsquedas de sucesor/predecesor. Se podría implementar un heap k-ario dinámico como estructura auxiliar o como otro punto de comparación.
* **Métricas:** Tiempo de operaciones (inserción, borrado, búsqueda, sucesor), uso de memoria, impacto del universo de claves en Van Emde Boas, impacto de la aleatoriedad en Skip Lists, rendimiento del heap k-ario.

#### 10. Implementación y análisis de hashing avanzado y filtros

* **Temas:** Cuckoo Hashing, Bloomier Filters, Rendezvous (HRW) Hashing, MinHash.
* **Descripción:** Desarrollar y comparar varias técnicas de hashing avanzadas. Implementar Cuckoo Hashing con diferentes políticas de resolución de ciclos. Construir Bloomier Filters para mapeos asociativos aproximados. Implementar HRW Hashing para distribución consistente. Usar MinHash para comparar la efectividad en la generación de firmas.
* **Métricas:** Factor de carga, tasa de fallos/rehashes (Cuckoo), falsos positivos (Bloomier), distribución (HRW), tiempo de operaciones, uso de memoria, colisiones (MinHash).

#### 11. Estructuras persistentes para edición colaborativa 

* **Temas:** Rope con persistencia completa, Finger Trees persistentes, Path Copying Persistent Union–Find, Segment Trees con Lazy Propagation (persistentes).
* **Descripción:** Simular un sistema de edición de texto o datos estructurados que permita "viajar en el tiempo" y mantener múltiples versiones eficientemente. Implementar Ropes persistentes para manejar texto largo y Finger Trees para secuencias más generales. Usar DSU persistente para gestionar el historial de versiones/ramas. Aplicar Segment Trees persistentes para consultas sobre versiones anteriores del texto/datos.
* **Métricas:** Tiempo de edición (inserción/borrado), tiempo de acceso a versiones anteriores, coste de la persistencia (espacio y tiempo), rendimiento de las consultas sobre versiones.

#### 12. Algoritmos de grafos para emparejamiento y cortes mínimos 

* **Temas:** Hopcroft–Karp, Stoer–Wagner, Dinic (usado como subrutina o comparativa), Euler–Tour Trees (para análisis estructural).
* **Descripción:** Implementar algoritmos fundamentales para problemas de grafos. Desarrollar Hopcroft-Karp para encontrar el emparejamiento máximo en grafos bipartitos. Implementar Stoer-Wagner para hallar el corte mínimo global en grafos no dirigidos. Se puede usar Dinic para verificar resultados de cortes (teorema max-flow min-cut) o como alternativa. Euler-Tour Trees pueden usarse para analizar la estructura del grafo durante los algoritmos.
* **Métricas:** Tiempo de ejecución de Hopcroft-Karp y Stoer-Wagner, tamaño del emparejamiento/corte encontrado, comparación con enfoques basados en flujo (Dinic), eficiencia del análisis estructural.


#### 13. Write-Heavy DB Index

* **Temas:** LSM-Trees, ART (Adaptive Radix Tree), Cuckoo Hashing (para *memtable*).
* **Descripción:** Diseña el núcleo de un índice para bases de datos optimizadas para escritura. Usa un LSM-Tree (simulando *memtable* y *SSTables*) como estructura principal. Implementa ART para indexar claves dentro de las tablas o como índice primario alternativo. Explora Cuckoo Hashing para la *memtable*.
* **Métricas:** *Throughput* de inserción/lectura (IOPS), latencia (p50, p99), *write amplification* (simulada), uso de memoria y disco.


#### 14. Skip Lists vs. VEB Trees 

* **Temas:** Skip Lists, Van Emde Boas Trees, X-Fast y Y-Fast Tries.
* **Descripción:** Implementa y realiza un *benchmark* profundo de *Skip Lists* y *Van Emde Boas Trees* para operaciones de diccionario ordenado. Como desafío adicional, implementa X-Fast y/o Y-Fast Tries y compara su rendimiento teórico y práctico (considerando el universo de claves).
* **Métricas:** Tiempo de inserción/borrado/búsqueda/sucesor, uso de memoria, impacto del tamaño del universo (VEB/Tries), impacto de la aleatoriedad (*Skip Lists*).


