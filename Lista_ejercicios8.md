### Listas de ejercicios

Utiliza las implementación dadas en clase: [ss-tree](https://github.com/kapumota/CC0E5/tree/main/ss-tree), 
[ss-tree -version1](https://github.com/kapumota/CC0E5/blob/main/ss_tree_1.py), [ss+-tree](https://github.com/kapumota/CC0E5/blob/main/ss%2B-tree.py)


#### Ejercicio 1: Extensión de la API y validación de tipos

**Objetivo**

* Añadir validaciones de entrada y unificación de nombres en la API de `ss_tree.py` y `ss_tree_1.py`.

**Tareas**

1. Implementar en la clase `Point` los métodos `__eq__` y `__hash__`.
2. Extraer la lógica de validación de dimensiones en un método estático compartido (`Point.validate_dimensions(p1, p2)`).
3. Renombrar todos los métodos de inserción a `insert()` y los de consulta k-NN a `knn()`.
4. Añadir comprobaciones en `benchmark.py` para asegurar que `max_points > 0` y lanzar `ValueError` si no.

**Entregables**

* Pull request que modifique `ss_tree.py`, `ss_tree_1.py` y `benchmark.py`.
* Ejemplo de uso en README con casos de éxito y casos de error.

#### Ejercicio 2: Benchmark de memoria y rendimiento cruzado

**Objetivo**

* Extender `benchmark.py` para medir uso de memoria y comparar heurísticas de split.

**Tareas**

1. Integrar un medidor de memoria (por ejemplo, usando `tracemalloc`) que reporte pico de memoria durante construcción e inserción.
2. Añadir en `benchmark_construction` un parámetro `use_variance_split: bool` que seleccione la heurística de varianza vs round-robin.
3. Ejecutar benchmarks sobre árboles con 10 000 puntos 2D y 5 000 puntos 10D, con ambas heurísticas, e interpretar resultados.

**Entregables**

* CSV o tabla con tiempos y memoria consumida para cada configuración.
* Breve informe (1-2 páginas) analizando trade-offs entre tiempo y consumo.

#### Ejercicio 3: Pruebas de estrés y validación frente a implementación naïve

**Objetivo**

* Asegurar precisión de búsquedas k-NN y splits bajo carga.

**Tareas**

1. En `test_sstree.py`, generar 1 000 puntos aleatorios en 3D y para cada uno buscar su vecino más cercano mediante:

   * Tu implementación de SS-Tree
   * Un algoritmo naïve (fuerza bruta) sobre la lista de `Point`
2. Comparar resultados y asertar que coinciden siempre.
3. Diseñar un caso límite donde varios puntos estén exactamente a la misma distancia y verificar comportamiento determinista.

**Entregables**

* Nuevos casos de test que cubran: precisión k-NN, splits correctos (la suma de tamaños de hijos = tamaño del padre), y casos de empate.

#### Ejercicio 4: Implementación de eliminación y reequilibrio en SS+-Tree

**Objetivo**

* Profundizar en la operación `delete()` y en el reequilibrio dinámico.

**Tareas**

1. Revisar el método `delete()` de `ss+-tree.py` y detectar escenarios en los que puede quedar un nodo "pobre" (por debajo de un 50 % de ocupación).
2. Implementar una rutina de fusión o redistribución cuando un nodo caiga por debajo del umbral.
3. Añadir tests que eliminen puntos uno a uno hasta vaciar el árbol, asegurando que tras cada eliminación la estructura cumple invariantes (radio, centroides).

**Entregables**

* Versión extendida de `ss+-tree.py` con reequilibrio.
* Tests en un nuevo módulo `test_ssplus_tree.py`.

#### Ejercicio 5: Serialización, carga y migración de estructura

**Objetivo**

* Garantizar persistencia y compatibilidad binaria entre versiones.

**Tareas**

1. Validar que `to_json()` y `from_json()` en SS+-Tree preservan exactamente la topología y datos.
2. Diseñar un script `migrate_ssplus.py` que:

   * Lea un JSON generado con la versión actual
   * Aplique cambios de API (p. ej. nombres unificados de método)
   * Reescriba un JSON compatible con la nueva versión
3. Medir tiempo de serialización y deserialización con árboles de 50 000 puntos.

**Entregables**

* Script `migrate_ssplus.py` con documentación de uso.
* Benchmark de serialización vs tamaño de archivo.


#### Ejercicio 6: Aplicación práctica: geolocalización de puntos de interés

**Objetivo**

* Integrar SS-Tree en una mini-aplicación de consulta de ubicaciones.

**Tareas**

1. Crear un pequeño dataset (CSV) de 5 000 puntos de interés (latitud, longitud).
2. Cargarlo en un SS-Tree y exponer un endpoint HTTP (usando Flask o FastAPI) `/nearest?lat=…&lng=…&k=…`.
3. Para cada petición, devolver los k puntos más cercanos junto con la distancia real.
4. Añadir en `/benchmark` una ruta que ejecute internamente los benchmarks de inserción y consulta sobre datos reales y muestre tiempos.

**Entregables**

* Código de la aplicación y archivo Dockerfile.
* Instrucciones para probar localmente (`docker-compose up`).
* Demo de 5 consultas con resultados.


#### Ejercicio 7: Documentación y guía de usuario

**Objetivo**

* Refinar la documentación de toda la librería y los scripts de benchmark.

**Tareas**

1. Generar un Sphinx (o MkDocs) site que incluya:

   * Guía de instalación
   * Tutorial paso a paso para construir un SS-Tree y un SS+-Tree
   * Ejemplos de código para inserción, búsqueda, eliminación y serialización
2. Incluir diagramas UML de clases (`Point`, `Node`, `SsTree`, `SsPlusTree`).
3. Publicar la documentación en GitHub Pages.

**Entregables**

* Carpeta `docs/` completa con configuración de Sphinx/MkDocs.
* URL de la página publicada.


#### Ejercicio 8: Clasificación k-NN sobre dataset etiquetado

**Objetivo**
Usar SS-Tree como índice para acelerar un clasificador k-NN en un conjunto de datos etiquetado (por ejemplo, Iris o MNIST reducido).

**Tareas**

1. Cargar un dataset con etiqueta (p. ej., Iris de scikit-learn).
2. Dividirlo en entrenamiento (80 %) y prueba (20 %).
3. Construir una SS-Tree sobre los puntos de entrenamiento (ignorando la etiqueta como dimensión adicional).
4. Para cada punto de prueba, buscar sus k vecinos y decidir la etiqueta mayoritaria.
5. Calcular precisión, recall y F1 del clasificador.

**Entregables**

* Script `knn_classification.py`.
* Informe breve con métricas y comparación de tiempos vs `sklearn.neighbors.KNeighborsClassifier`.

#### Ejercicio 9: Detección de anomalías basada en distancia al vecino más cercano

**Objetivo**
Detectar outliers midiendo la distancia media al k-ésimo vecino en un conjunto de datos de series temporales o sensórica.

**Tareas**

1. Generar o importar un dataset univariable (p. ej., temperatura horaria).
2. Para cada muestra, computar la distancia al 3er vecino más cercano usando SS-Tree.
3. Tomar como anomalías los puntos cuya distancia supere la media + 2·desviación estándar.
4. Visualizar (gráfico de línea) dónde saltan anomalías.

**Entregables**

* Notebook o script `anomaly_detection.py`.
* Gráfico con señales y marcadores de anomalías.


#### Ejercicio 10: Recomendaciones colaborativas simplificadas

**Objetivo**
Implementar un sistema de recomendación "user-based" donde vecinos se definen por similitud de vectores de calificaciones.

**Tareas**

1. Cargar un pequeño dataset de calificaciones (p. ej., MovieLens 100K).
2. Para cada usuario, crear un vector de calificaciones en espacio m-dimensional (m = número de películas).
3. Construir una SS+-Tree con vectores de todos los usuarios.
4. Dado un usuario de prueba, encontrar sus k vecinos más cercanos y promediar sus calificaciones para recomendar las top-N películas.
5. Medir precisión\@N usando hold-out de usuarios.

**Entregables**

* Módulo `user_recommendation.py`.
* Documento corto con precisión\@5 y tiempos de consulta vs fuerza bruta.

#### Ejercicio 11: Recuperación de imágenes similares

**Objetivo**
Indexar descriptores de imágenes (p. ej., vectores SIFT o embeddings de una CNN) en una SS+-Tree para consultas de contenido visual.

**Tareas**

1. Extraer embeddings (de dimensión \~128–512) de 1 000 imágenes con un modelo preentrenado (p. ej., MobileNet).
2. Construir una SS+-Tree con esos vectores.
3. Diseñar un script que dado un embedding de consulta muestre las 5 imágenes más parecidas.
4. Crear un pequeño HTML que muestre consulta y resultados lado a lado.

**Entregables**

* Carpeta `image_retrieval/` con:

  * `build_index.py`,
  * `query_images.py`,
  * `index.html` de demostración.


#### Ejercicio 12: Búsqueda en tiempo real y actualizaciones dinámicas

**Objetivo**
Montar un servicio que admita inserciones y consultas k-NN simultáneamente, midiendo latencia bajo carga.

**Tareas**

1. Implementar un servidor (FastAPI) con dos rutas:

   * `POST /insert` para añadir un punto al SS-Tree.
   * `GET /knn?k=…` para devolver vecinos de un punto dado.
2. Usar `asyncio` o hilos para simular 100 inserciones/segundo y 200 consultas/segundo.
3. Medir latencia p99 de consultas mientras el árbol crece hasta 50 000 puntos.

**Entregables**

* Código de servidor `realtime_knn.py` y cliente de carga `load_test.py`.
* Gráfica de latencia vs número de puntos.

