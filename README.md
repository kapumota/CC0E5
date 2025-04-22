## Notas del curso de algoritmos y estructuras de datos - CC0E5

Este curso avanzado explora las estructuras de datos más utilizadas en el desarrollo de software moderno, así como técnicas avanzadas para optimización, búsqueda y procesamiento eficiente en diferentes contextos: memoria interna, externa, grafos y clustering. Se brindan conocimientos tanto teóricos como prácticos que permitirán comprender el rendimiento de algoritmos y estructuras aplicadas en sistemas reales.

#### Donde practicar

- [Codeforces](https://codeforces.com)
- [DMOJ](https://dmoj.ca)
- [Kattis](https://open.kattis.com)
- [POJ](https://poj.org)
- [SPOJ](https://spoj.com)
- [UVa](https://uva.onlinejudge.org)


### Índice

- [Capítulo 1: Fundamentos y mejoras en estructuras de datos](#capítulo-1-fundamentos-y-mejoras-en-estructuras-de-datos)
- [Capítulo 2: Consultas multidimensionales y clustering](#capítulo-2-consultas-multidimensionales-y-clustering)
- [Capítulo 3: Estructuras de datos avanzadas](#capítulo-3-estructuras-de-datos-avanzadas)


#### Capítulo 1: Fundamentos y mejoras en estructuras de datos

#### Introducción a las estructuras de datos  

- Definición y descripción de una estructura de datos.
- Diferencia entre algoritmos y estructuras de datos.
- Planteamiento de problemas y "setting goals".
- Ejemplos prácticos: la mochila y la abstracción del problema.

#### Mejoras en colas de prioridad: d-ary heaps  

- Problemas prácticos de manejo de prioridades.
- De listas ordenadas a colas de prioridad.
- Descripción de la API y operaciones: inserción, actualización, heapify.
- Análisis de rendimiento y casos de uso: por ejemplo, encontrar los *k* elementos más grandes.

#### Treaps: Uso de aleatorización para balancear BST  

- Concepto de treap y balanceo aleatorio.
- Rotaciones, búsqueda, inserción y eliminación.
- Comparación de rendimiento y aplicaciones prácticas.

#### Estructuras complementarias  

- **Bloom filters:** Ahorro de memoria en búsquedas. Funcionamiento interno, funciones hash y precisión.
- **Disjoint sets (Union-Find):** Implementación, mejoras con *path compression* y *union by rank*. Aplicaciones en grafos como Kruskal.


#### Capítulo 2: Consultas multidimensionales y clustering

#### Búsqueda de vecinos más cercanos y árboles k-d  

- Planteamiento del problema de *nearest neighbors*.
- Espacios k-dimensionales y soluciones.
- Construcción y búsqueda en árboles k-d.
- Aplicaciones en recuperación de imágenes.

#### Árboles de búsqueda de similitud y clustering  

- Árboles SS-tree y SS+-tree: inserción y búsqueda aproximada.
- Métodos de clustering: K-means, DBSCAN, OPTICS.
- Aplicaciones: reducción de color, agrupamiento en bases de datos.
- Introducción al *clustering* paralelo: MapReduce y *Canopy clustering*.

#### Capítulo 3: Estructuras de datos avanzadas

#### Introducción a grafos y recorridos  

- Definiciones básicas, representación y recorridos: BFS y DFS.
- Aplicaciones en optimización de rutas, como entregas.
  
#### Rutas en grafos: Dijkstra y A*  

- Implementación del algoritmo de Dijkstra.
- Introducción al algoritmo A* y uso de heurísticas.

#### Modelo de memoria externa y B-trees  

- Modelo externo vs RAM.
- B-trees: balanceo, búsqueda, inserción, eliminación.
- Comparación con B⁺-trees.
- Casos de uso en bases de datos como MySQL.


#### Bε-trees y LSM-trees  

- Buffering en Bε-trees: mecánica y análisis de costos.
- LSM-trees: funcionamiento y uso en sistemas distribuidos (e.g. Cassandra).

#### Ordenamiento en memoria externa  

- Casos de uso: robótica, genómica.
- Algoritmos: Merge-sort (M/B-way), variantes de quick-sort.
- Justificación teórica de la optimalidad del merge-sort externo.


#### Optimización en grafos y algoritmos  

- Técnicas de optimización.
- Descenso de gradiente aplicado a grafos y clustering avanzado.

#### Integración y casos prácticos  

- Repaso general de estructuras y algoritmos avanzados.
- Ejercicios: fusión de listas ordenadas, aplicaciones reales.


#### Otros tópicos finales

#### Exploración adicional  

- Introducción opcional a:
  - RSA y fundamentos criptográficos.
  - Algoritmos cuánticos.
  - Tendencias futuras en estructuras de datos.



#### Metodología

Este curso combina teoría avanzada con resolución de problemas reales, mediante prácticas calificadas y casos de estudio. Se recomienda el uso de cuadernos de Jupyter o Google Colab para las pruebas de código y análisis empírico de algoritmos.

### Referencias:

- Introduction to Algorithms, fourth edition 4th Edición de Thomas H. Cormen (Author), Charles E. Leiserson (Author), Ronald L. Rivest. The MIT Press; 4a edición (5 Abril 2022).
- Algorithms and Data Structures for Massive Datasets.  Dzejla Medjedovic. Manning Publications  (5 Julio 2022). 
- Efficient Algorithm Design: Unlock the power of algorithms to optimize computer programming. Masoud Makrehchi. Packt Publishing (31 Octubre 2024).
- Graph-Powered Machine Learning, Allesandro Nego. Manning Publications (P) 2022. 
- Graph Databases in Action, Dave Bechberger,  Josh Perryman. Manning; Primera edición (24 Noviembre 2020) 
- 50 Algorithms Every Programmer Should Know: Tackle computer science challenges with classic to modern algorithms in machine learning, software design, data systems, and cryptography. Imran Ahmad. Packt Publishing; Segunda edición. (29 Septiembre 2023) 
