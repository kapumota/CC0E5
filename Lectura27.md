### **Clustering paralelo**

El clustering es una técnica esencial para descubrir estructuras ocultas en grandes volúmenes de datos sin necesidad de etiquetas previas.
Tradicionalmente, algoritmos como k-means, DBSCAN u OPTICS se han implementado de forma secuencial, analizando cada punto uno tras otro en un único hilo de ejecución. 
Sin embargo, cuando trabajamos con conjuntos de datos de gran tamaño, esta aproximación puede resultar inaceptablemente lenta. Frente a este reto, surgen dos caminos: aprovechar el paralelismo dentro de una misma máquina o distribuir el procesamiento entre varios nodos en red.

En el primer caso, hablamos de cómputo paralelo: múltiples hilos o procesos ejecutándose simultáneamente en una única máquina con memoria compartida.
Gracias a la baja latencia de comunicación interna, del orden de nanosegundos, podemos dividir la carga de trabajo entre los núcleos disponibles y reducir drásticamente el tiempo de ejecución. 

El segundo caso es el cómputo distribuido, donde varias máquinas colaboran a través de la red para procesar fragmentos del dataset. 
Aunque las latencias en este escenario pueden ascender a decenas o cientos de milisegundos, la escalabilidad horizontal que ofrece es esencial cuando los datos superan la capacidad de memoria de un solo servidor.

Para decidir entre paralelo y distribuido conviene considerar el tamaño del dataset, el patrón de comunicación entre subtareas y el coste de coordinación. 
Si todo cabe en la memoria de una sola máquina, generalmente es más eficiente paralelizar localmente. Pero si los datos exceden dicha capacidad, el procesamiento distribuido resulta inevitable.

Tomemos como ejemplo el k-means. Su implementación clásica consta de tres fases: inicializar `k` centroides, asignar cada punto al centroide más cercano y 
recalcular las posiciones de dichos centroides. 
La inicialización aleatoria de centroides, al ser una operación de complejidad *O(k)*, es rápida y apenas justifica paralelismo, salvo casos en que se 
requiera un muestreo sin reemplazo a gran escala. La fase de asignación, en cambio, presenta un coste *O(nkd)*, donde `n` es el número de puntos y `d` la dimensión
de cada uno y se beneficia enormemente de la división de datos en bloques que cada hilo puede procesar de forma independiente. La única comunicación necesaria tiene lugar al final para fusionar asignaciones. 

Finalmente, al recalcular los centroides, podemos asignar a cada hilo la responsabilidad de procesar uno de los `k` grupos, lo que en el mejor escenario se
traduce en un speed-up cercano a `k`, limitándose solo por la parte secuencial restante según la Ley de Amdahl.

Cuando se trata de escalar más allá de una sola máquina, el modelo MapReduce ofrece una abstracción muy útil. En la fase de **Map**, cada nodo recibe un fragmento de datos y emite pares clave-valor (por ejemplo, "cluster\_id" y vectores de puntos). 
Tras un paso de **Shuffle & Sort** que agrupa dichos pares por clave, en la fase de **Reduce** cada nodo agrega vectores y calcula nuevos centroides. 
Este patrón elimina gran parte de la complejidad de la comunicación y de la tolerancia a fallos, y se ha convertido en la base de sistemas como Hadoop, Spark o Flink.

Aun así, existe una técnica previa que puede acelerar notablemente los algoritmos de clustering: el **canopy clustering**. 

>Referencias:

>* [Efficient Clustering of High-Dimensional Data Sets with Application to Reference Matching](http://www.kamalnigam.com/papers/canopy-kdd00.pdf)
>* [Canopy Clustering  ](https://mahout.apache.org/docs/latest/algorithms/clustering/canopy/)

Se trata de un método ligero y  de una única pasada sobre los datos, en el que se definen dos umbrales T₁ y T₂ (siendo T₁ mayor).  Se elige un punto al azar 
como centro de un "canopy", y todos los puntos cuya distancia al centro sea menor que T₁ se añaden al mismo; aquellos cuya distancia sea menor que T₂ se eliminan de la lista de candidatos para futuros canopies. 
El resultado son regiones esféricas superpuestas, obtenidas en tiempo *O(nd)*, mucho menor que *O(nkd)* de k-means. 
Además, al usar métricas aproximadas, como la distancia L1 en lugar de L2 podemos reducir aún más el costo de cómputo.

El canopy clustering se adapta bien tanto al cómputo paralelo como al distribuido. 

En un único nodo, basta con dividir aleatoriamente el conjunto de datos entre varios hilos, cada uno construyendo sus propios canopies y emitiendo centros parciales. En un entorno distribuido, cada nodo procesa su fragmento en la fase Map, generando centros y asignaciones, mientras que la fase 
Reduce agrupa centros cercanos entre sí (según T₁) y consolida las asignaciones. Aunque la consolidación puede requerir comparar `m` canopies entre sí con un coste que crece como O(m²), en la práctica *m* suele ser mucho menor que *n*.

Una de las aplicaciones más valiosas del canopy clustering es su uso como paso previo a k-means. 

Una vez generados `m` pseudo-clusters, podemos calcular el centro de masa de cada uno y, si m ≥ k, escoger `k` de estos centros como centroides iniciales de 
k-means; si `m < k`, completamos la selección con centroides aleatorios adicionales. Esta inicialización más informada acelera la convergencia de k-means y reduce el número de iteraciones necesarias.

Otra aplicación destacada se da en algoritmos basados en densidad, como DBSCAN y OPTICS, que suelen sufrir con densidades no uniformes. 
Aquí, el canopy clustering sirve para segmentar el espacio en regiones más homogéneas: cada canopy se procesa en paralelo con DBSCAN u OPTICS ajustando 
localmente el parámetro `ε`. Después, como las regiones pueden solaparse, es preciso fusionar los resultados de manera inteligente. 
Basta con comprobar, para cada par de clusters en canopies superpuestos, si existen puntos cuya distancia sea menor que el mayor de los `ε` usados, en caso 
afirmativo, los clusters se fusionan. Así, reducimos el tamaño de cada ejecución local y logramos un análisis paramétrico más fino.

Para implementar estos esquemas de manera eficiente conviene seguir algunas buenas prácticas: balancear la carga de trabajo dividiendo datos en fragmentos de
igual tamaño; minimizar los puntos de sincronización, de modo que la reducción de resultados sea lo más esporádica posible; emplear frameworks 
adecuados según el entorno, por ejemplo, OpenMP o scikit-learn con `n_jobs` en un solo nodo, Spark o Dask en varios nodos y aplicar heurísticas de poda,
como límites triangulares o estructuras tipo k-d tree, para descartar cálculos innecesarios de distancias.

En la práctica, la combinación de canopy clustering con modelos MapReduce y k-means distribuido puede transformar flujos de trabajo que antes
tardaban horas en ejecutarse en procesos que se completan en cuestión de minutos. 
Con el auge de infraestructuras de cómputo en la nube y de plataformas como Kubernetes o Airflow, es habitual dividir descargas y procesamiento en
fragmentos que se ejecutan de forma concurrente, lo que reduce drásticamente los tiempos de espera. 

Al final, contar con el paralelismo y la distribución  entre las herramientas a disposición de los ingenieros de datos no es solo una opción, sino una necesidad para afrontar el creciente volumen y complejidad de 
los datasets modernos.

### **MapReduce**

Desde sus inicios, la necesidad de procesar grandes volúmenes de datos de manera eficiente ha impulsado a los ingenieros a buscar modelos de programación que superaran las limitaciones de las arquitecturas tradicionales. 
En aquellas épocas en que el cómputo en GRID dominaba el panorama, los desarrolladores debían gestionar manualmente la orquestación de recursos distribuidos, 
asumiendo complejas tareas de partición, balanceo de carga y tolerancia a fallos. 
Fue en ese contexto que Google, a principios de los años 2000, introdujo y puso en producción el modelo de programación **MapReduce**, patentándolo y popularizándolo para la comunidad de software de código abierto.

La belleza de MapReduce radica en su sencillez conceptual: por un lado, la fase de **Map** (mapeo), que define cómo transformar cada registro de entrada y por otro, la fase de **Reduce** (reducción), que combina o agrega los resultados intermedios. 
Gracias a esta dualidad, los desarrolladores pueden centrarse en la lógica del procesamiento, cómo listar, filtrar, agrupar o combinar datos mientras el framework se encarga de distribuir la carga, reintentar tareas fallidas y gestionar la comunicación entre nodos, asegurando escalabilidad horizontal y tolerancia a fallos.

Con el tiempo surgieron múltiples implementaciones de MapReduce, Apache Hadoop, Hive, CloudDB, Mahout, entre otras  aunque su valor real no reside en la herramienta específica, sino en el paradigma que propone. 
Este modelo ha probado su eficacia en una enorme variedad de problemas: desde la construcción de índices invertidos hasta el cálculo de estadísticas globales, pasando por operaciones de filtrado masivo o joins distribuidos. 
La capacidad de aislar la lógica de negocio de la complejidad de la orquestación hace que MapReduce siga siendo una piedra angular en el procesamiento de big data, especialmente en entornos donde la lectura y escritura de grandes volúmenes domina los costos de I/O.

#### **MapReduce-KMeans**

El clásico algoritmo de **k-means** puede expresarse de manera natural en MapReduce gracias a la independencia de sus dos fases principales:

1. **Clasificación (Map):** cada nodo recibe un subconjunto de puntos y la lista global de centroides; asigna cada punto al centroide más cercano y emite pares `(id_centroide, punto)`.
2. **Re-centrado (Reduce):** cada nodo agrupa los puntos por `id_centroide` y calcula la nueva posición promedio de cada grupo, emitiendo el nuevo centroide.

Sin embargo, MapReduce estándar no está optimizado para iteraciones encadenadas: cada ejecución lee y escribe todo el dataset, lo que haría muy costosa la convergencia de k-means en `m` iteraciones. 
Para resolverlo se introdujo el **MapReduce iterativo**, donde los mappers y reducers se inician una sola vez, manteniendo en memoria el sharding de datos y  recibiendo en cada iteración únicamente la lista actualizada de centroides (mucho más pequeña que el dataset). 
De este modo, el coste de I/O se reduce drásticamente, limitándose al intercambio de centroides, y permitiendo completar múltiples iteraciones con un rendimiento cercano al óptimo.

El otro gran reto es la **inicialización** de los centroides. Para ello existen dos estrategias distribuidas:

* **Muestreo estratificado:** fragmentar aleatoriamente el dataset en shards, extraer muestras aleatorias de cada shard y combinarlas para formar la semilla global.
* **Canopy clustering:** utilizar un algoritmo heurístico que, con dos umbrales de distancia T₁ y T₂, genera "canopies" superpuestos cuyos centroides provisionales se usan como semilla para k-means.

La paralelización de canopy clustering sigue tres pasos:

1. **Shard inicial:** dividir el dataset global en p shards.
2. **Canopy local (Map):** cada mapper ejecuta canopy clustering en su shard, produciendo centroides parciales.
3. **Canopy global (Reduce único):** combinar los centroides parciales y reejecutar canopy clustering sobre este conjunto reducido para asegurar la separación mínima T₂ global.

Así, el trabajo de clasificar todos los puntos se hace en paralelo, y el reagrupamiento definitivo recae en un volumen de datos muy inferior, sin lecturas masivas repetidas.

Para aproximar un número fijo de centroides `k`, se aplican técnicas de búsqueda de umbrales: bien variando T₁/T₂ de forma estocástica y eligiendo el resultado más cercano a k, bien ajustándolos iterativamente (inspirado en descenso de gradiente) hasta converger o agotar iteraciones, guardando la mejor configuración parcial.

El flujo completo de MapReduce-k-means queda entonces:

1. **Shard único** de datos.
2. **MapReduce canopy clustering** para inicializar centroides.
3. **Iterative MapReduce**: cada iteración Map emite asignaciones, Reduce recalcula centroides.
4. **Salida final**: centroides y asignaciones de puntos.

Este esquema aprovecha al máximo la tolerancia a fallos y escalabilidad de MapReduce, minimizando I/O y aprovechando la paralelización para procesar datasets de gran tamaño con decenas o cientos de terabytes.

#### **MapReduce-DBSCAN**

El algoritmo **DBSCAN** (Density-Based Spatial Clustering of Applications with Noise) agrupa puntos según su densidad local, definiendo clusters a partir de vecindarios ε y relaciones de conectividad entre puntos "core". Esta dependencia de las relaciones espaciales y la transitividad hace que DBSCAN no parezca apto para MapReduce al fragmentar aleatoriamente el dataset, pues se dispersarían los ε-vecindarios, impidiendo reconocer correctamente puntos core.

Para resolverlo se emplea un **sharding espacial** basado en un grid regular de celdas rectangulares:

1. **Definición de grid:** dividir el dominio en hiperceldas regulares.
2. **Expansión de bordes:** cada celda se amplía en todas direcciones por `ε`, generando shards solapados con celdas vecinas.
3. **Asignación a shards:** un punto puede pertenecer a varias celdas si cae en la zona expandida.

El proceso completo consta de:

1. **MapReduce de sharding distribuido (Job 0):**

   * **Map:** mappers aleatorios comparan puntos con la cuadrícula (o la buscan mediante un R-tree) y emiten `(id_shard, punto)`.
   * **Reduce:** agrupa los puntos por `id_shard`, produciendo los shards expandidos.

2. **MapReduce de clustering local (Job 1):**

   * **Map:** cada mapper ejecuta DBSCAN en su shard expandidos sin cambiar el algoritmo secuencial, y emite:

     * Lista de clusters locales con índices provisionales.
     * Lista de puntos noise.
     * Lista de puntos en la zona de margen (dentro de ε del borde original).
   * **Reduce por par de shards vecinos:** cada reducer recibe los resultados de dos shards adyacentes, identifica los puntos core en la zona de solapamiento y, usando una estructura **Disjoint Set**, fusiona clusters conectados, emitiendo pares o la propia estructura de fusiones.

3. **Composición final (Job 2, opcional):**

   * Reindexar globalmente los clusters tras todas las fusiones.
   * Generar la asignación definitiva de cada punto y la lista de outliers.

Opcionalmente, la fase de sharding espacial puede distribuirse mediante un MapReduce previo usando R-trees, de modo que incluso la preparación de shards aproveche la paralelización y evite cuellos de botella secuenciales.

De esta manera, MapReduce logra adaptar DBSCAN al procesamiento distribuido: el sharding espacial conserva las vecindades `ε` dentro de al menos un shard, el clustering local aprovecha el algoritmo original y la fase de fusión global recupera la conectividad completa de los datos.



