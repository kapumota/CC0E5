## Listas de ejercicios

Utiliza las implementación dadas en clase: [kd-tree](https://github.com/kapumota/CC0E5/blob/main/kd-tree.py), 
[ball-tree](https://github.com/kapumota/CC0E5/blob/main/ball-tree.py), [cover-tree](https://github.com/kapumota/CC0E5/blob/main/cover-tree.py)

### 1. Pruebas avanzadas 

**Contexto general**: Usa `pytest` y **Hypothesis** para diseñar suites de pruebas que garanticen corrección en escenarios límite y cubran invariantes de tus implementaciones.

1. **kd-tree**

   * Crea tests unitarios para insertar y borrar puntos en espacios de 1D, 2D y 10D.
   * Propiedad (Hypothesis): recorrer en-orden siempre devuelve los puntos ordenados según su clave en la dimensión de la raíz.
   * Caso límite: árbol vacío, inserción de muchos duplicados, borrado secuencial de todos los puntos.

2. **ball-tree**

   * Verifica que `nearest_neighbour` y `points_within_distance_from` devuelven el mismo resultado que una búsqueda "brute-force" sobre listas de puntos.
   * Hypothesis: generación aleatoria de n puntos en $[0,1]^d$ y consulta de radio; compara resultados.

3. **cover-tree**

   * Testea que tras insertar y luego eliminar un punto, la estructura resteura invariantes (todos los hijos siguen a nivel correcto y cobertura mínima).
   * Propiedad: para cualquier punto p, tras insertar p y luego `remove(p)`, una consulta k-NN sobre p arroja el mismo vecino que sin haber insertado p.

4. **B-Tree y B+-Tree**

   * Diseña tests de inserción/borrado que forcen splits y merges en nodos interiores y hojas.
   * Propiedad: tras operaciones aleatorias (mezcla de insert/delete), el recorrido in-orden de claves coincide con el ordenamiento de la lista de claves operadas.

5. **R-Tree**

   * Tests de consultas de intersección ("range query"): genera rectángulos aleatorios y comprueba con un método naïve (comprobación par a par).
   * Caso límite: rectángulos degenerados (líneas o puntos), inserciones que provoquen reinserción diferida y splits.


### 2. Benchmarking y perfilado

**Contexto general**: Usa módulos `timeit`, `perf_counter` y/o `pytest-benchmark` para medir tiempos y memoria sobre datasets de diferentes tamaños y distribuciones.

1. **Construcción vs consulta**

   * Para cada estructura (kd, ball, cover, R-Tree), mide el tiempo de construcción con n = 10³, 10⁴, 10⁵ puntos en 2D y 10D; grafica crecimiento (O(n log n) vs O(n²)).
   * Benchmark: búsqueda de 1-NN vs k-NN (k = 1,10,100); compara con búsqueda naïve.

2. **Parámetros críticos**

   * **Cover-Tree**: experimenta cambiando `base` (2.0, 1.5, 3.0) y observa cómo varía tiempo de inserción y altura del árbol.
   * **Ball-Tree**: varía `leaf_size_threshold` (10, 50, 100) y mide consultas de rango.

3. **Memoria**

   * Con `tracemalloc`, evalúa uso de memoria durante construcción para B-Tree vs B+-Tree con m = 50, 100.
   * Grafica número de nodos y altura final frente a n = $10⁴$, $10⁵$ claves.

4. **Paralelización**

   * Implementa (o usa `multiprocessing.Pool`) una versión paralela de construcción de kd-tree **dividiendo** el dataset en trozos, construyendo sub-árboles y luego "mergeando" raíces.
   * Mide speed-up en máquinas multicore (2,4,8 núcleos) y justifica cuándo compensa.


### 3. Mejoras de código y optimizaciones

**Contexto general**: analiza los cuellos de botella con `cProfile` o `line_profiler` y propone refactorizaciones.

1. **kd-tree**

   * Sustituye el método `median()` que ordena toda la lista por un algoritmo "median of medians" O(n) y mide la reducción en tiempo de construcción.
   * Refactor: elimina recálculos de tamaño/altura en cada inserción; mantén contadores actualizados en el **back-tracking** del árbol.

2. **ball-tree**

   * Optimiza el cálculo de pivotes: en lugar de recorrer listas completas, usa una muestra aleatoria o heurística del diámetro para elegir x₀,x₁,x₂. Mide calidad de partición (balance) y rendimiento.

3. **cover-tree**

   * Reemplaza la recomputación completa de candidatos `Q_i` por un índice aproximado (p. ej. k-means en primer nivel) para reducir tamaño de la cola. Comprueba impacto en precisión de k-NN y tiempo total.

4. **B-Tree / B+-Tree**

   * Implementa **bulk-loading**: dada una lista ordenada de claves, construye un B-Tree de altura mínima en O(n). Compara con inserción secuencial.
   * En B+-Tree, mejora `find` con "binary search" en la lista enlazada de hojas (mantén pointers a bloques de hojas) para evitar recorrer toda la cadena.

5. **R-Tree**

   * Sustituye la heurística cuadrática de split por la heurística lineal de Guttman y compara número de páginas usadas (MBR totales) y rendimiento de consultas.
   * Ajusta `reinsert_count` (0%, 30%, 50% de M) y mide su efecto en fragmentación y rendimiento de actualización.


#### Herramientas y datasets sugeridos

* **Datasets de ejemplo**:

  * Puntos uniformes y gaussianos.
  * Rectángulos de tamaños y posiciones aleatorias dentro de un bounding box fijo.
  * Claves numéricas distribuidas uniformemente o con clusters para B-Tree.

* **Librerías**:

  * `pytest`, `hypothesis`, `pytest-benchmark`
  * `numpy` para generación de datos y medición vectorizada
  * `matplotlib` o `plotly` para graficar resultados de benchmarking
  * `cProfile`, `line_profiler` y `tracemalloc` para perfilado


#### Conjunto de datos ejemplos

**kd-tree**

```python
# Puntos en 2D: mezcla de distribución uniforme y cluster gaussiano
sample_kd_points = [
    (0.05, 0.95), (0.15, 0.85), (0.25, 0.75),  # uniforme en primer cuadrante
    (-0.8, -0.2), (-0.9, -0.5),               # uniforme en tercer cuadrante
    ( 1.1,  0.9), ( 1.3,  1.0), ( 0.9,  1.2),  # cluster gaussiano centro (1,1)
    ( 5.0,  5.0),                             
    ( 2.5, -1.5)                              
]
```

**ball-tree**

```python
# Puntos en 10D: tres clusteres de 5 puntos cada uno
import numpy as np
rng = np.random.default_rng(42)
cluster_centers = [np.zeros(10), np.ones(10)*5, np.array([-3,-3]+[0]*8)]
sample_ball_points = []
for μ in cluster_centers:
    sample_ball_points += list(rng.normal(loc=μ, scale=0.2, size=(5, 10)))
# Obtendrás 15 vectores de dimensión 10
```
**cover-tree**

```python
# Usamos los mismos puntos del kd-tree para cover-tree en 2D
sample_cover_points = sample_kd_points.copy()
```

**B-Tree y B+-Tree**

```python
# Claves enteras: secuencia con patrones de inserción/desalojo
sample_keys = [5, 12, 3, 21, 8, 14, 30, 17, 1, 9, 25, 19, 2, 6, 11, 28, 4, 7, 10, 13]
# Para bulk-load: lista ordenada de 1 a 100 con paso 3
bulk_keys = list(range(1, 101, 3))  # [1,4,7,…, 97,100]
```
**R-Tree**

```python
# Rectángulos: (xmin, ymin, xmax, ymax)
sample_rects = [
    (0.0,  0.0, 1.0, 1.0),    # zona origen
    (0.5,  0.5, 2.0, 2.0),    # solapa con anterior
    (-1.0, -1.0, -0.5, -0.5), # cuarto cuadrante negativo
    ( 5.0,  5.0, 6.0, 6.0),   # rectángulo aislado
    ( 1.2, -0.3, 1.8, 0.3),   # línea horizontal
    ( 2.0,  1.0, 2.0,  1.0),  # punto degenerado
]
```

#### Cómo usarlos

* **Pruebas**: itera sobre `sample_kd_points`, inserta/borra, y comprueba invariantes.
* **Benchmarking**: replica cada lista a gran escala (p.ej. 10³-10⁵ elementos) usando `numpy.tile` o generadores aleatorios con semilla fija.
* **Mejoras**: sobre estos datos "particularizados" podrás medir cambios concretos en tiempo y memoria.

A continuación reordeno y emparejo cada bloque de ejercicios con los ficheros de código que has subido (`kd-tree.py`, `ball-tree.py`, `cover-tree.py`, `btree.py`, `b+tree.py`, `r-tree.py`). Así los estudiantes podrán ir directamente al módulo correspondiente.

#### 4. Análisis de complejidad teórica

#### Construcción

* **kd-tree.py**

  * Partiendo de *n* puntos de k-dimensiones, deduce el coste de construcción cuando:

    1. Ordenas el array completo por el eje actual (usando `sorted`): O(n log n) por nivel => O(n log² n).
    2. Seleccionas la mediana con un algoritmo O(n) ("median-of-medians"): O(n log n).
  * Contrasta con el balance de espacio en cada nodo (`axis`, `left`, `right`, `point`).

* **ball-tree.py**

  * Cada partición calcula centroide y radio en O(m) siendo m el tamaño del bloque.
  * Con particiones recursivas aproximadas a mitades: T(n) ≃ 2 T(n/2) + O(n) => O(n log n).
  * Analiza en qué casos (datos muy concentrados) la altura real se dispara.

* **cover-tree.py**

  * Los "niveles de escala" dependen de la distribución de distancias: modelo coste peor caso O(n²), promedio ≈ O(n log n).
  * Examina la estructura de los mapas auxiliares `_level_map`, `_maxdist_map` y su coste en memoria.

#### Consultas de 1-NN y rango

* **kd-tree.py**, **ball-tree.py**, **cover-tree.py**

  * Cuenta las distancias calculadas en:

    1. Nube uniforme en $[0,1]^k$.
    2. Cluster gaussiano .
  * Justifica por qué en k pequeño se poda mucho y en k grande se evalúan casi todos los puntos.

* **r-tree.py**

  * Para consultas por rango (rectángulo), mide nodos visitados en densidades:

    1. Espacio muy disperso.
    2. Clusters compactos.
  * Contrasta poda con MBRs solapados.

#### Inserción y eliminación

* **kd-tree.py**

  * Inserta secuencialmente puntos ordenados vs. aleatorios y mide profundidad resultante (sin rebalanceo).

* **ball-tree.py**

  * Tras cada inserción, recalcula centros y radios sólo en la rama afectada.

* **cover-tree.py**

  * Inserta y luego `remove(point)`; cuenta reinserciones y variación de radios globales.
* **btree.py** & **b+tree.py**

  * Ejecuta secuencias de insert/delete para forzar splits/merges en hojas e internos; mide coste amortizado.


#### Profiling y diagnóstico de rendimiento

Para entender en profundidad cómo se comportan nuestras estructuras de datos y localizar los cuellos de botella, dividiremos el diagnóstico en tres fases: identificación de hotspots en CPU, análisis de la huella de memoria y benchmarking comparativo. Cada paso se aplicará a los módulos `kd-tree.py`, `ball-tree.py`, `cover-tree.py`, `btree.py`, `b+tree.py` y `r-tree.py`.


#### Hotspots de CPU

Lo primero es averiguar qué partes del código consumen más tiempo de cómputo:

1. **Ejecución de cProfile**
   En cada fichero, lanza el perfilado:

   ```bash
   python -m cProfile -o perfil_kd.prof kd-tree.py
   python -m cProfile -o perfil_ball.prof ball-tree.py
   # ...y así sucesivamente
   ```
2. **Extracción de resultados**
   Con herramientas como **snakeviz** o el módulo `pstats` de Python, abre cada `.prof` y extrae las 5 funciones más costosas. Es probable que aparezcan nombres como `select_pivot`, `distance`, `_split` o `_search`.
3. **Documentación de hallazgos**
   Para cada hotspot, anota:

   * **Función**: nombre y ubicación en el fichero.
   * **Tiempo total (%)**: proporción sobre el total de la ejecución.
   * **Número de llamadas**: cuántas veces se invocó.
     Esto te ayudará a centrar futuras optimizaciones (p.ej. reemplazar un cálculo de distancia por vectorizado).


#### Huella de memoria

El siguiente paso es medir cómo crece el consumo de memoria:

1. **Preparación con tracemalloc**
   Inserta estas líneas al inicio de tu script de prueba:

   ```python
   import tracemalloc
   tracemalloc.start()

   # … aquí construyes el árbol y ejecutas consultas …
   tree = KDTree(sample_points)
   tree.nearest_neighbour(query)

   snapshot = tracemalloc.take_snapshot()
   ```
2. **Comparación de snapshots**
   Usa `snapshot.compare_to()` para ver qué objetos (listas, diccionarios como `_index_map`, pilas de llamadas) consumen más memoria **antes y después** de cada operación.
3. **Informe de consumo**
   Documenta:

   * **Memoria total usada** (en MB).
   * **Principales asignaciones** (tipo de objeto y tamaño).
   * **Variación al aumentar n** (repite para n=10³,10⁴,10⁵).

#### 3. Benchmarking comparativo

Para cuantificar la escalabilidad y sensiblidad a la dimensión, realizaremos un benchmarking sistemático con datos sintéticos:

1. **Generación de datasets**
   En un script `benchmarks.py`, construye tres tipos de datos con NumPy y semilla fija:

   ```python
   from numpy.random import default_rng
   import numpy as np

   rng = default_rng(0)

   # 1. Puntos uniformes en el hipercubo [0,1]^k
   data_uniform = rng.random((n, k))

   # 2. Puntos gaussianos alrededor de 0.5 con desviación 0.1
   data_gauss   = rng.normal(loc=0.5, scale=0.1, size=(n, k))

   # 3. Clusters bien separados
   centers      = rng.random((5, k)) * 10
   data_clusters = np.vstack([
       rng.normal(c, 0.2, size=(n // 5, k)) for c in centers
   ])
   ```
2. **Definición de métricas**
   Para cada estructura y cada tipo de dato:

   * Ejecuta **al menos 30 repeticiones**.
   * Registra con `time.perf_counter()`:

     * Tiempo de construcción (`t_construct`).
     * Tiempo medio de consulta 1-NN y de consulta por rango (`t_query`).
   * Incrementa un **contador interno** en cada llamada a `distance()` para saber cuántas distancias se calculan.
3. **Visualización de resultados**
   En un notebook o script aparte, utiliza Matplotlib para generar:

   * **Gráficas log-log** de tiempo vs. *n* y tiempo vs. *k*, donde cada curva represente una de las estructuras.
   * **Diagramas de cajas** (boxplots) de la distribución de tiempos en las 30 ejecuciones, para apreciar la variabilidad.
   * Anotaciones en los puntos donde una estructura supera a otra, o donde la "maldición de la dimensionalidad" hace que pierdan ventaja frente al brute-force.


#### Propuestas iniciales de mejora

Una vez identificados los hotspots y los escenarios donde el rendimiento decae, se podrán ensayar las siguientes optimizaciones:

1. **Selección de pivote en kd-tree**
   Cambiar el sort/median por un algoritmo `median-of-medians` (O(n)) y comparar de nuevo los tiempos de construcción.

2. **Vectorización / Cython**
   En `ball-tree.py` y `cover-tree.py`, sustituir loops explícitos de Python por operaciones de NumPy — por ejemplo, calcular todos los vectores de distancia de una sola vez con `np.linalg.norm`. Como paso avanzado, crear un módulo en Cython para la función `distance()`.

3. **Paralelización de construcción**
   Implementar en `kd-tree.py` un método `build_parallel(points, processes=4)` que:

   * Divida los datos en fragmentos.
   * Construya sub-árboles en procesos independientes.
   * Una vez listos, haga un merge simple de sus raíces para formar el árbol final.

4. **Caching y poda adaptativa**
   En `cover-tree.py`, aplicar un decorador `@lru_cache` para memorizar resultados de `distance(p,q)` y, adicionalmente, ajustar dinámicamente el radio de poda en función de la densidad local de puntos (por ejemplo, reduciéndolo proporcionalmente a 1/√degree).

