### **Práctica calificada 3 CC0E5**

**Consideraciones generales para todos los proyectos:**

1. **Alcance:**

   * Implementación funcional y eficiente del núcleo de la estructura o algoritmo elegido, incluyendo al menos una optimización clave basada en bibliografía o variantes de rendimiento documentadas.
   * No es necesario cubrir todas las variantes posibles; basta con justificar por qué se escogen las optimizaciones seleccionadas.

2. **Repositorio público:**

   * Lenguaje: Python, C++ o Rust.
   * Código modular, bien comentado (especialmente en secciones complejas), fácil de entender y mantener.
   * **README.md** exhaustivo que incluya:

     * Descripción del proyecto y su motivación teórica.
     * Instrucciones de compilación/ejecución (dependencias, comandos paso a paso).
     * Estructura del proyecto (organización de carpetas y archivos).
     * Documentación de la API pública (firma de funciones, parámetros, valores de retorno, excepciones).
   * **Drivers/demo** que muestren usos avanzados de la estructura (casos de uso variados).
   * **Suite de pruebas unitarias** (pytest, Google Test, etc.) con alta cobertura, y scripts para profiling/benchmarking comparativo (por ejemplo, medir tiempos en distintos tamaños de datos).

3. **Documentación adicional (informe técnico PDF, 3–5 páginas):**

   * Teoría subyacente (pruebas de correctitud, complejidad, referencias bibliográficas).
   * Decisiones de diseño (alternativas estudiadas, por qué se eligió la opción final).
   * Análisis empírico de rendimiento (resultados de benchmarking y comparación con implementaciones existentes).
   * Limitaciones actuales y posibles mejoras o extensiones futuras.

4. **Exposición (12 de junio):**

   * Cada grupo debe preparar una presentación (PowerPoint, PDF, etc.) que explique brevemente la teoría, la implementación y los resultados experimentales.
   * Se valorará la claridad al responder preguntas sobre diseño y benchmarking.
   * Si el número de estudiantes o grupos excede el tiempo disponible el 12 de junio, o por problemas de horario, se reservará un segundo día adicional para que los grupos pendientes realicen su exposición (con las mismas condiciones de preguntas y ponderación).

En ese caso, se comunicará oportunamente la fecha y hora exacta a los grupos que aún no hayan expuesto.

5. **Ponderación de calificaciones:**

   * Entrega del repositorio (README, código, pruebas, benchmarking, informe PDF): 5 puntos.
   * Exposición oral y respuesta de preguntas: 15 puntos.

Se priorizará el manejo de los conceptos y códigos vistos en la clase, así como la capacidad de explicar decisiones de diseño y resultados experimentales.

### Proyectos propuestos

1. **KD-Tree con heurística de reconstrucción periódica y comparación frente a Ball-Tree**

   * **Temáticas combinadas:** kd-tree; Ball-Tree; benchmarking comparativo.
   * **Descripción breve:**

     1. Implementar un **KD-Tree básico** en el lenguaje elegido (Python/C++/Rust), capaz de insertar y buscar vecinos más cercanos (1-NN y k-NN).
     2. Incluir una **heurística de reconstrucción perezosa**: por ejemplo, reequilibrar el árbol cada 2^h inserciones o cuando la profundidad exceda cierto umbral. Justificar esta heurística con bibliografía.
     3. Paralelamente, implementar un **Ball-Tree** (basado en hiperesferas) con alguna optimización (p. ej., usar partición basada en centroides aproximados en lugar de medianas estrictas).
     4. Desarrollar un **driver de benchmarking** que compare tiempos de construcción e índices en consulta (1-NN y k-NN) para datos sintéticos de distintas dimensiones (p. ej., 2D, 10D, 50D).
     5. Analizar empíricamente la "maldición de la dimensionalidad" y mostrar hasta qué dimensión cada estructura rinde mejor.

2. **Cover Tree con variación de heurística "nearest‐neighbor first" y cuantización sencilla**

   * **Temáticas combinadas:** Cover Tree; Product Quantization (PQ).
   * **Descripción breve:**

     1. Implementar desde cero un **Cover Tree** según la definición original (Beygelzimer et al.), capaz de soportar inserciones y k-NN queries.
     2. Añadir una **heurística "nearest-neighbor first"** para acelerar la construcción: en cada nivel, escoger el pivot de manera aproximada a partir de un muestreo pequeño del conjunto de puntos.
     3. Implementar una versión reducida de **Product Quantization** (PQ) para resumir cada punto en un código de baja dimensión (ej. dos subcuantizadores de tamaño fijo). Usar PQ para acelerar la búsqueda aproximada dentro del Cover Tree.
     4. Realizar pruebas comparativas entre:

        * Cover Tree puro vs. Cover Tree + PQ (búsqueda aproximada).
        * Métricas: tiempo de construcción, tiempo de consulta (1-NN), error medio de distancia.
     5. Documentar claramente las fórmulas de PQ, subdivisión de espacios y asignación de códigos.

3. **VP-Tree con selección de pivotes basados en "maximizar diversidad" y análisis de escalabilidad**

   * **Temáticas combinadas:** VP-Tree; Region Search; Comparison con KD-Tree.
   * **Descripción breve:**

     1. Construir un **Vantage-Point Tree (VP-Tree)** que, en vez de seleccionar pivotes al azar, use un **heurística de "máxima diversidad"** (pivote = punto que maximiza la media de distancias al resto del conjunto).
     2. Implementar la operación de búsqueda de los k vecinos más cercanos.
     3. Incluir un modo de **"region search"** (buscar todos los puntos dentro de una distancia R de la query).
     4. Comparar empíricamente con una implementación básica de **KD-Tree** (puede ser la del proyecto 1), midiendo tiempos de consulta y memoria utilizada.
     5. Analizar cómo escala la estructura al aumentar el número de dimensiones (2D, 5D, 20D) y con datos reales (p. ej., embeddings de texto sintéticos).

4. **Randomized k-d Forest con referenciación a variantes "Median-of-Medians"**

   * **Temáticas combinadas:** Randomized k-d Forests; optimización de mediana lineal (Median-of-Medians).
   * **Descripción breve:**

     1. Implementar una **Randomized k-d Forest (RkF)**, es decir, varias KD-Trees aleatorizadas (con ejes de partición y subconjuntos de datos distintos en cada árbol).
     2. Para cada KD-Tree interna, usar el algoritmo **Median-of-Medians** para seleccionar la mediana en O(n) en lugar de O(n log n) por ordenamiento.
     3. Permitir consultas de k-NN que unan resultados de todos los árboles (p. ej., mediante un min-heap global).
     4. Evaluar el **trade-off** entre número de árboles (p. ej., 3 vs. 7) y precisión en las consultas vs. tiempo de respuesta.
     5. Comparar contra un KD-Tree "no aleatorizado" (misma implementación de mediana eficiente) y medir: tiempo de construcción, memoria, tasa de aciertos (exactitud) vs. aproximada.

5. **Locality Sensitive Hashing (LSH) para búsqueda aproximada y Product Quantization avanzada**

   * **Temáticas combinadas:** LSH; Product Quantization (PQ); benchmarking de búsqueda aproximada.
   * **Descripción breve:**

     1. Implementar un esquema estándar de **LSH (p. ej., para distancia euclidiana)** con tablas de hash basadas en proyecciones aleatorias (Random Projection LSH).
     2. Complementar con un **Product Quantizer optimizado** (OPQ): reorientar vectores antes de cuantizarlos para minimizar error.
     3. Construir un **driver** que genere índices LSH vs. índices PQ (y OPQ) y compare:

        * Tiempo de indexación y espacio ocupado.
        * Precisión en k-NN approximate vs. exacta (medida de recall\@k).
     4. Incluir dataset sintético (p. ej., 100 000 puntos en 64 dimensiones) y, si caben un dataset real pequeño (p. ej., descriptors SIFT de 1 000 000 de vectores reducidos).

6. **M-Tree en disco con comparación frente a B-Tree para persistencia de índices espaciales**

   * **Temáticas combinadas:** M-Tree; B-Tree; estructuras LSM y streaming.
   * **Descripción breve:**

     1. Implementar un **M-Tree minimalista** (p. ej., basándose en conceptos de Rangé Tree para índices espaciales), pero diseñado para funcionar en disco:

        * Nodos serializados en archivos (p. ej., ficheros binarios o LevelDB/LMDB si se usa Rust).
        * Páginas de disco simuladas (p. ej., bloques de 4 KB).
     2. Implementar un **B-Tree** clásico (de clave-entero) para comparativa de rendimiento en disco.
     3. Desarrollar un **mecanismo LSM (Log-Structured Merge Tree) sencillo**: inserciones van primero a un buffer en memoria; cuando crece, se "mergean" a un archivo en disco.
     4. Benchmark: medir tiempos de inserción y búsqueda de k-NN (o rango) en M-Tree vs. B-Tree vs. LSM.
     5. Analizar cómo cambia el rendimiento al aumentar el tamaño de datos (p. ej., de 100 000 a 1 000 000 de puntos).

7. **RMI (Recursive Model Index) básico sobre array de enteros y comparativa con B-Tree**

   * **Temáticas combinadas:** RMI; B-Tree; benchmarking de índices basados en modelos vs. tradicionales.
   * **Descripción breve:**

     1. Implementar un **RMI de dos niveles** sobre un array ordenado de enteros (o strings codificados).

        * Nivel 0: modelo lineal que predice rango aproximado.
        * Nivel 1: modelos lineales más pequeños (uno por tramo) para afinar la predicción de posición.
     2. Construir un **B-Tree** clásico en memoria (o una B+Tree simplificada) para servir de comparador.
     3. Medir:

        * Tiempo de construcción de índices.
        * Tiempo de búsqueda exacta de un entero (por ejemplo, rank query).
        * Espacio ocupado (parámetros de modelo vs. punteros de B-Tree).
     4. Documentar la forma de entrenar modelos lineales (mínimos cuadrados) y cómo ajustarlos para minimizar error de posición.

8. **ALEX (Adaptive Learned Index) simplificado y análisis evolución adaptativa**

   * **Temáticas combinadas:** ALEX; RMI; comparación con árboles B.
   * **Descripción breve:**

     1. Implementar una versión reducida de **ALEX**, es decir, un índice adaptativo que combina un modelo base con una estructura de árbol que se reconfigura cuando el error excede cierto umbral.

        * Nivel 0: modelo global (lineal).
        * Nivel 1: buckets dinámicos (cada bucket con un mini-árbol o arreglo), que se reorganizan si crecen demasiado.
     2. Comparar con:

        * RMI ya implementado en el proyecto 7.
        * B-Tree estático usado como índice tradicional.
     3. Evaluar la **adaptación online**: insertar claves de manera incremental y mostrar cómo ALEX ajusta sus buckets (p. ej., splits y merges).
     4. Benchmark: medir latencias de inserción y consulta en entornos con cargas mixtas (50 % búsquedas, 50 % inserciones).

9. **R-Tree con búsqueda de región y comparación vs. SS+ Tree**

   * **Temáticas combinadas:** R-Tree; SS+ Tree (Similarity Search+ Tree).
   * **Descripción breve:**

     1. Implementar un **R-Tree** (bulk-loading opcional) capaz de almacenar rectángulos o puntos (en 2D) y soportar:

        * Búsqueda de rango ("return all points/rectángulos dentro de un área").
        * k-NN search aproximada (usando heurística de cercanía al rectángulo MBR).

     2. Implementar un **SS+ Tree** (basado en White & Jain), que usa hiperesferas para particionar:

        * Modificar la heurística de split original para "mitigar hiperesfera" (p. ej., dividir cuando overlap > umbral).

     3. Desarrollar un **driver comparativo**:

        * Insertar un conjunto de 100 000 puntos 2D (distintos patrones: uniforme, clusterizado).
        * Medir:

          | Estructura | Tiempo construcción | Memoria usada | Tiempo region search | Tiempo k-NN un punto |
          | ---------- | ------------------- | ------------- | -------------------- | -------------------- |
          | R-Tree     | ...                   | ...             | ...                    | ...                    |
          | SS+ Tree   | ...                   | ...             | ...                    | ...                    |

     4. Analizar en el informe cómo cambia el performance según densidad de datos y distribución.

10. **Estructura Learn-VS-Index: combinación RMI + LSH para vectores altos dimensionales**

    * **Temáticas combinadas:** RMI; LSH; Learned indexes; Similarity search.
    * **Descripción breve:**

      1. Diseñar un **índice híbrido**:

         * En niveles superiores, un **RMI** que predice "hot bucket" (conjunto aproximado de vectores donde la query puede estar).
         * En cada "bucket", usar **LSH** (con hash random projection) para filtrar rápidamente los candidatos.
      2. Construir un **dataset sintético** de vectores de 50-100 dimensiones (p. ej., 500 000 vectores).
      3. Comparar con:

         * LSH puro (sin RMI).
         * RMI puro seguido de búsqueda lineal dentro del bucket.
         * KD-Tree puro (para bajas dimensiones, p. ej., 10).
      4. Medir: latencia promedio de k-NN (approx), recall\@10, tamaño de índice, tiempo de construcción.

11. **Implementación de LSM-Tree simple con índice secundario basado en B-Tree**

    * **Temáticas combinadas:** Estructuras LSM (Log-Structured Merge Tree); B-Tree; streaming.
    * **Descripción breve:**

      1. Desarrollar una **LSM-Tree simplificada**:

         * MemTable en memoria (mapa ordenado).
         * SSTable en disco: ficheros planos (sorted strings tables).
         * Merge incremental (configurable).
      2. Añadir un **índice secundario** basado en B-Tree para uno de los atributos (p. ej., timestamp o clave secundaria).
      3. Implementar operaciones de inserción, búsqueda exacta y búsqueda por rango en clave secundaria.
      4. Benchmark: medir

         * Throughput de inserciones secuenciales (1 M registros).
         * Latencia de búsqueda exacta vs. rango en clave secundaria, comparando:

           * LSM sin índice secundario (búsqueda full-scan en SSTable).
           * LSM con B-Tree secundario.
      5. Analizar trade-offs espacio/tiempo y frecuencia de merges.

12. **M-Tree distribuido (cliente-servidor ligero) con sincronización vía HTTP**

    * **Temáticas combinadas:** M-Tree; Distribución (HTTP communication); Sincronización de inventario.
    * **Descripción breve:**

      1. Implementar un **servidor HTTP REST** (p. ej., con Flask en Python, Rocket en Rust o Boost.Beast en C++) que exponga endpoints para:

         * Insertar punto (con metadatos).
         * Consultar k-NN (query por vector).
         * Sincronizar nodos (GET/POST de snapshots parciales).
      2. El **servidor mantiene un M-Tree** en memoria (o disco), capaz de inserción y búsqueda básica.
      3. Implementar un **cliente ligero** (en el mismo lenguaje o distinto) que:

         * Le envía peticiones HTTP al servidor.
         * Mantiene en caché local un subconjunto de puntos (inventario parcial).
         * Sincroniza inventario cada N minutos u operaciones (configurable).
      4. Simular un escenario de "inventario" donde varios clientes agregan/buscan puntos, y el servidor central debe mantener la consistencia eventual.
      5. Benchmark: medir latencias de consulta local vs. consulta al servidor, y ancho de banda de sincronización. Documentar lecciones aprendidas (p. ej., problemas de concurrencia).

13. **Comparativa de RMI vs. ALEX vs. B-Tree en base de datos on-disk (aplicación centralizada)**

    * **Temáticas combinadas:** RMI; ALEX; B-Tree; Aplicación centralizada (filtrado de puntos).
    * **Descripción breve:**

      1. Diseñar una **API REST centralizada** (Flask, FastAPI, etc.) que permita:

         * Insertar un par (clave, vector corta).
         * Filtrar puntos por rango de clave (búsqueda por clave entera).
         * Obtener los k vectores más cercanos (k-NN en espacio de vectores 10D).
      2. Implementar tres variantes de índice "backend" para el mismo servicio:

         * **RMI** (tal y como en proyecto 7).
         * **ALEX** (tal y como en proyecto 8).
         * **B-Tree** (estático, en disco).
      3. La API debe poder arrancar usando cualquiera de los tres índices (flag de arranque).
      4. Proporcionar un **driver de benchmarking** (en Python o cualquier lenguaje) que:

         * Envíe cargas mixtas de inserciones y consultas (e.g., 70 % lectura, 30 % escritura).
         * Compare latencia y throughput para cada índice.
      5. Analizar resultados, discutir en qué escenarios conviene cada índice (volumen de datos, mix lectura/escritura).

14. **SS+ Tree con variantes de heurística de split y concurrente (modo multihilo)**

    * **Temáticas combinadas:** SS+ Tree; Similarity search; Concurrencia (threads).
    * **Descripción breve:**

      1. Implementar un **SS+ Tree** siguiendo White & Jain, que utilice hipótesis de hiperesferas para partición:

         * Implementar dos heurísticas de split: una "original" y otra "mejorada" (p. ej., minimizando overlap).
      2. Adaptar la estructura para que sea **thread-safe**: permitir inserciones concurrentes desde múltiples hilos (usa locks finos o lock-free si el tiempo lo permite).
      3. Incluir operaciones de búsqueda de rango y k-NN concurrente (múltiples hilos pueden hacer consultas simultáneas).
      4. Evaluar el rendimiento en escenarios multihilo:

         * Inserciones concurrentes vs. secuenciales.
         * Consultas concurrentes vs. secuenciales.
      5. Comparar la heurística original vs. la heurística "mejorada" en términos de overlap, reclasificación y tiempo de consulta.

15. **Integración de Learned Index (ALEX) en aplicación distribuida ligera con HTTP y sincronización**

    * **Temáticas combinadas:** ALEX; Distribución (HTTP); Sincronización de índices.
    * **Descripción breve:**

      1. Desarrollar un **servidor REST** (Flask/FastAPI/Rocket) que mantenga un **ALEX** en memoria (o con persistencia ligera).
      2. Crear un **cliente desktop o script** que:

         * Envíe inserciones y consultas (exactas y rango).
         * Mantenga una copia local reducida del índice (solo modelos de nivel 0), y consulte al servidor cuando la predicción local no tenga suficiente confianza (error mayor a umbral).
         * Sincronice parámetros del índice (p.ej., cuando el servidor reentrena buckets).
      3. Incluir un **mecanismo de notificaciones** sencillo (p. ej., WebSockets o polling HTTP) para que el cliente sepa cuándo reentrenar localmente su modelo de nivel 0.
      4. Benchmark: evaluar la latencia de consulta en cliente "sincronizado" vs. "no sincronizado"; analizar costo de comunicación vs. ganancia en latencia.
      5. Discutir en el informe los desafíos de sincronizar índices basados en modelos en entornos distribuidos (problemas de consistencia eventual).


### Notas finales

* Dado el tiempo limitado, se aconseja partir siempre de pseudocódigo o bibliografía existente, adaptándolo al lenguaje y estilo, en lugar de desarrollar desde cero sin guía.
* En todos los casos, se sugiere dedicar, al menos:

  - **6 horas** a diseñar/planificar la arquitectura del código y decidir las optimizaciones.
  - **9 horas** a codificar la estructura central y las optimizaciones principales.
  - **4 horas** a implementar pruebas unitarias y scripts de benchmarking/profiling.
  - **2 horas** a redactar el informe técnico y pulir el README y la presentación final.

