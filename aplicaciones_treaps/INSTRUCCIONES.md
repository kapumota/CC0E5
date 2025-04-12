### [Treaps de intervalos](https://github.com/kapumota/CC0E5/blob/main/aplicaciones_treaps/treap_intervalos.cpp) 

#### 1. Estructura y funcionalidad del código

El código implementa dos variantes de treap en C++:

#### a) **Treap de enteros**

- **Estructura:**  
  Cada nodo (definido en `TreapNode`) almacena una clave, una prioridad generada aleatoriamente (usando `rand()`), el tamaño del subárbol (para facilitar las estadísticas de orden) y punteros a los hijos izquierdo y derecho.

- **Operaciones principales:**  
  - **Inserción (`treapInsert`):** Inserta una clave en el árbol, reestructurándolo mediante rotaciones (funciones `rotateRight` y `rotateLeft`) para mantener la propiedad de heap basada en las prioridades.  
  - **Búsqueda (`treapFind`):** Recorre recursivamente el árbol para determinar si una clave existe.  
  - **Eliminación (`treapErase`):** Elimina un nodo; si el nodo tiene dos hijos, utiliza rotaciones para bajarlo y luego retirarlo.  
  - **Estadísticas de orden (`treapGetKth`):** Devuelve el k-ésimo elemento (ordenado in-order), utilizando el tamaño de los subárboles para tomar decisiones.

#### b) **Treap de intervalos**

- **Estructura:**  
  Los intervalos se representan con la estructura `Interval` (con atributos `start` y `end`). Cada nodo en el árbol de intervalos (definido en `IntervalTreapNode`) almacena un intervalo, una prioridad aleatoria y un valor `maxEnd` que indica el mayor valor final dentro del subárbol. Esto permite optimizar las consultas de intersección de intervalos.

- **Operaciones principales:**  
  - **Inserción (`intervalTreapInsert`):** Inserta un intervalo ordenando los nodos por el valor inicial del intervalo. Después de cada inserción, se actualiza el valor `maxEnd` del nodo.  
  - **Consulta de intersección (`intersectingIntervals`):** Dado un intervalo de consulta, recorre el treap para identificar y recolectar aquellos intervalos que se solapan, utilizando la función `doOverlap` para determinar la superposición.

#### 2. Funciones adicionales

#### a) **Pruebas unitarias (`runUnitTests`)**

- Realiza varios tests para comprobar:
  - El recorrido in-order del treap de enteros (asegurando que esté ordenado).
  - La existencia (o no) de ciertos elementos.
  - La obtención correcta del k-ésimo elemento.
  - La correcta eliminación de nodos.
  - La detección de intersecciones en el treap de intervalos.  
- Se utiliza la función `assert` para verificar las condiciones esperadas, deteniendo la ejecución en caso de fallo.

#### b) **Profiling (`runProfiling`)**

- Se mide el rendimiento sobre el treap de enteros con 100,000 elementos:
  - **Inserción:** Se mide el tiempo requerido para insertar todos los elementos.  
  - **Búsqueda:** Se evalúa el tiempo invertido en buscar claves en el treap.  
  - **Consultas k-ésimas:** Se realizan 100 consultas distribuidas a lo largo del árbol para obtener el k-ésimo elemento, midiendo también su tiempo de ejecución.  
- El uso de la biblioteca `<chrono>` permite medir con precisión el tiempo en milisegundos.

#### 3. Modos de ejecución

El programa admite tres modos de ejecución determinados por argumentos de línea de comandos:

- **Modo test:**  
  Ejecutar  
  ```bash
  ./treap_intervalos test
  ```  
  Llama a `runUnitTests()` para validar el funcionamiento de las operaciones.

- **Modo profiling:**  
  Ejecutar  
  ```bash
  ./treap_intervalos profile
  ```  
  Llama a `runProfiling()` para medir el rendimiento en operaciones masivas.

- **Modo demostración:**  
  Ejecutar sin argumentos  
  ```bash
  ./treap_intervalos
  ```  
  Se ejecuta una demostración que realiza operaciones básicas en ambos treaps (inserciones, búsquedas, eliminación y consultas de intervalos).

#### 4. Compilación e integración con CMake

#### a) **Compilación con g++**

Puedes compilar el código (guardado en `treap_intervalos.cpp`) con el siguiente comando:
```bash
g++ -std=c++11 -O2 treap_intervalos.cpp -o treap_intervalos
```
Una vez compilado, utiliza las instrucciones mencionadas para cada modo.

#### b) **Configuración de CMake**

Para integrar este código en un proyecto con CMake, crea un archivo `CMakeLists.txt` en el directorio del proyecto con el siguiente contenido:
```cmake
cmake_minimum_required(VERSION 3.10)
project(TreapIntervalos)

set(CMAKE_CXX_STANDARD 11)

add_executable(programa treap_intervalos.cpp)
```
Pasos para compilar con CMake:
1. **Crear el directorio de compilación:**  
   ```bash
   mkdir build && cd build
   ```
2. **Ejecutar CMake y compilar:**  
   ```bash
   cmake ..
   make
   ```
Esto generará el ejecutable `programa`, el cual se puede ejecutar en cualquiera de los modos descritos.

### [Treaps y concurrencia](https://github.com/kapumota/CC0E5/blob/main/aplicaciones_treaps/treap_concurrencia.cpp)

#### 1. Estructura del código

#### a) **Nodos y funciones básicas**

El código define una estructura básica para el treap concurrente mediante el struct `Node`, que contiene:

- **key:** valor entero que identifica el nodo.
- **priority:** valor aleatorio (obtenido con `rand()`) para mantener la propiedad de heap en el treap.
- **subtreeSize:** tamaño del subárbol, facilitando operaciones de estadísticas o selección basada en orden.
- **Punteros a hijos:** `left` y `right` para los subárboles izquierdo y derecho.

Se incluyen funciones auxiliares como `getSize`, `updateSize` y dos funciones de rotación (`rotateRight` y `rotateLeft`) que permiten mantener el balance del treap durante inserciones y eliminaciones.

#### b) **Operaciones del Treap**

Se implementan las operaciones tradicionales del treap:

- **Inserción (`treapInsert`):** Se inserta un nodo en el lugar correcto; si la prioridad del nuevo nodo es mayor a la del padre, se realiza una rotación (derecha o izquierda) para conservar la propiedad de heap.
- **Búsqueda (`treapFind`):** Función recursiva que recorre el treap para encontrar un nodo con una clave determinada.
- **Eliminación (`treapErase`):** Se localiza el nodo a borrar y, en caso de tener dos hijos, se rota para bajar el nodo hasta que se pueda eliminar sin afectar el árbol.
- **Recorrido In-Order (`inorder`):** Función que imprime el recorrido del treap en orden ascendente.

#### c) **ConcurrentTreap**

La clase `ConcurrentTreap` encapsula la estructura del treap y agrega sincronización mediante un `std::shared_mutex`:

- **Bloqueo:**  
  - Métodos de inserción y eliminación usan `unique_lock` para obtener un bloqueo exclusivo.
  - Métodos de búsqueda y de obtención del recorrido in-order usan `shared_lock` para permitir accesos concurrentes de solo lectura.

- **Métodos principales:**  
  - `insert(int key)`, `erase(int key)` y `find(int key)` para modificar o consultar el treap.
  - `printInorder()` y `getInorder()`: estas funciones muestran el recorrido in-order, siendo `getInorder()` especialmente útil para validar resultados en pruebas unitarias.


#### 2. Funcionalidades adicionales

#### a) **Pruebas unitarias**

La función `runUnitTests()` ejecuta un conjunto de tests que:

- Inserta claves conocidas y verifica que el recorrido in-order obtenido (a través de `getInorder()`) coincida con el vector ordenado esperado.
- Comprueba la función de búsqueda, verificando tanto la existencia como la no existencia de determinados valores.
- Valida la operación de eliminación y se asegura de que el árbol se actualice correctamente.

Se utiliza `assert` para que cualquier error en la validación detenga la ejecución.

#### b) **Profiling**

En la función `runProfiling()` se ejecuta un test de rendimiento concurrente:

- Se lanza un número definido de hilos (en el ejemplo, 8) que realizan simultáneamente 10,000 operaciones (inserciones, búsquedas y eliminaciones) sobre el treap.
- Se introduce un pequeño retardo artificial (`sleep_for`) en cada iteración para simular carga.
- Se mide el tiempo total de ejecución usando `<chrono>` y se muestra el tiempo transcurrido y el número final de elementos en el treap.

#### c) **Demostración**

Si no se pasan argumentos en la línea de comandos, se ejecuta `runDemo()`, donde se lanzan varios hilos (en este caso, 4) para realizar operaciones concurrentes con una cantidad reducida de acciones. Al final se imprime el contenido del treap y se realizan búsquedas secuenciales para demostrar el funcionamiento del sistema.

#### 3. Forma de ejecución

El programa admite tres modos de operación:

- **Pruebas unitarias:**  
  Ejecuta:
  ```bash
  ./treap_concurrencia test
  ```
  Esto ejecuta `runUnitTests()` para validar las operaciones básicas del treap concurrente.

- **Profiling:**  
  Ejecuta:
  ```bash
  ./treap_concurrencia profile
  ```
  Ejecuta `runProfiling()` para medir el rendimiento concurrente del treap.

- **Demostración:**  
  Ejecuta:
  ```bash
  ./treap_concurrencia
  ```
  Sin argumentos, se ejecuta `runDemo()` para mostrar el funcionamiento del treap en un escenario concurrente.


#### 4. Integración con CMake

Para compilar el proyecto usando CMake, crea un archivo `CMakeLists.txt` en el directorio del proyecto con el siguiente contenido:

```cmake
cmake_minimum_required(VERSION 3.10)
project(TreapConcurrencia)

set(CMAKE_CXX_STANDARD 11)

add_executable(programa treap_concurrencia.cpp)
```

Pasos para compilar:

1. **Crear y entrar en el directorio de compilación:**
   ```bash
   mkdir build && cd build
   ```
2. **Ejecutar CMake y construir el proyecto:**
   ```bash
   cmake ..
   make
   ```
Esto generará el ejecutable `programa`, el cual se puede ejecutar en cualquiera de los modos indicados anteriormente.

### [Treap para sistemas distribuidos](https://github.com/kapumota/CC0E5/blob/main/aplicaciones_treaps/treap_distribuido.cpp)

#### 1. Descripción general del código

El código implementa un modelo conceptual de un sistema distribuido basado en treaps que, en cada shard o nodo, almacena registros (records) con la siguiente información:  
- **key:** Clave entera.  
- **value:** Valor representado como string.  
- **version:** Un timestamp o versión para resolver conflictos (actualización por versión).

La estructura se basa en dos niveles:
- **Treap local:** Cada shard posee un treap que almacena registros ordenados por clave.  
- **Sistema distribuido (DistributedTreapSystem):** Consta de varios shards; la asignación de registros se realiza mediante un hash simple sobre la clave.  
  - Se permiten operaciones locales (inserción, eliminación y búsqueda) en cada treap y, además, se implementa una operación de merge (similar a CRDT) en la que, al fusionar dos shards, se conserva la versión más alta de cada registro.

#### 2. Componentes principales

#### a) Estructuras de datos
- **Record:** Define la estructura básica de cada registro, que incluye clave, valor y versión.
- **Node:** Nodo del treap que almacena un Record, junto con la prioridad aleatoria (para mantener la propiedad de heap), punteros a sus hijos y el tamaño del subárbol.
  
#### b) Funciones de operación en el treap
- **Inserción (`treapInsert`):** Inserta un registro en el treap siguiendo el orden binario. Si la clave ya existe, se compara la versión; si la nueva versión es mayor, se actualiza el valor.
- **Eliminación (`treapErase`):** Busca y elimina el nodo correspondiente a una clave, reequilibrando el árbol mediante rotaciones (derecha o izquierda) según las prioridades.
- **Búsqueda (`treapFind`):** Recorre el árbol para localizar un registro dado su key.
- **Recorrido in-Order (`inorderCollect`):** Extrae los registros ordenadamente, facilitando así la verificación y la realización de consultas globales.

#### c) Sistema distribuido
La clase **DistributedTreapSystem** encapsula un vector de treaps (shards).  
- **Inserción, eliminación y búsqueda:** Utilizan un hash sencillo sobre la clave para determinar el shard correspondiente.  
- **Merge entre shards:** Permite fusionar el contenido de dos shards, respetando la versión mayor de cada registro.  
- **Consulta global:** La función `getAllGlobal()` recopila los registros de todos los shards (sin orden global) para posteriores procesamientos o consultas por rango.


#### 3. Funcionalidades adicionales

#### a) Pruebas unitarias (`runUnitTests`)
Esta función ejecuta un conjunto de tests automáticos para validar:
- La correcta inserción de registros y la actualización de valores al recibir una versión mayor.
- La funcionalidad de búsqueda (se comprueba que un registro actualizado se encuentre y que aquellos eliminados no existan).
- La operación de merge, verificando que los registros de cada shard se conserven según lo esperado.
- Se usan `assert` para detener la ejecución si algún test falla.

#### b) Profiling (`runProfiling`)
Esta función simula un entorno de alto volumen de operaciones (100,000 operaciones) en el sistema distribuido:
- Se generan claves y versiones aleatorias y se realizan inserciones y eliminaciones periódicas.
- Se mide el tiempo total de ejecución utilizando `<chrono>`, permitiendo evaluar el rendimiento bajo carga.

#### c) Modo de ejecución
El programa admite tres modos, configurables mediante argumentos en línea de comandos:
- **Modo "test":**  
  ```bash
  ./treap_distribuido test
  ```  
  Ejecuta las pruebas unitarias.
- **Modo "profile":**  
  ```bash
  ./treap_distribuido profile
  ```  
  Ejecuta la rutina de profiling.
- **Modo de demostración:**  
  ```bash
  ./treap_distribuido
  ```  
  Sin argumentos, se corre la demostración original, en la que se inserta un conjunto de registros, se muestran búsquedas y se simula un merge entre shards.

#### 4. Compilación e integración con CMake

#### a) Compilación con g++
Para compilar el código con soporte para C++17, se puede usar el siguiente comando (considerando que el archivo se llama **treap_distribuido.cpp**):
```bash
g++ -std=c++17 treap_distribuido.cpp -o treap_distribuido
```
Luego se ejecuta utilizando:
- `./treap_distribuido test`  
- `./treap_distribuido profile`  
- `./treap_distribuido`

#### b) Ejemplo de CMakeLists.txt
Para integrar el código en un proyecto con CMake, cree un archivo `CMakeLists.txt` con el siguiente contenido:
```cmake
cmake_minimum_required(VERSION 3.10)
project(TreapDistribuido)

set(CMAKE_CXX_STANDARD 17)

add_executable(programa treap_distribuido.cpp)
```
Pasos de compilación:
1. Crear un directorio de compilación y entrar en él:
   ```bash
   mkdir build && cd build
   ```
2. Ejecutar CMake y compilar:
   ```bash
   cmake ..
   make
   ```
### [Treaps para enrutamiento y redes](https://github.com/kapumota/CC0E5/blob/main/aplicaciones_treaps/treap_networks.cpp)


#### 1. Estructura y funcionalidad del código

#### a) Cola de Prioridad -TreapPriorityQueue

- **Objetivo:**  
  Permitir la planificación de paquetes según su prioridad. Para lograr que el paquete de mayor prioridad se encuentre en la raíz, se utiliza como "clave" en el árbol el valor negativo de la prioridad (–priority).

- **Estructura:**  
  Los paquetes se representan con la estructura `Packet`, que contiene un identificador, la prioridad y un contenido (string). Cada nodo del treap (struct `PQNode`) almacena un `Packet`, la clave calculada y un valor aleatorio (randVal) para mantener la propiedad de heap en el árbol.  
  Se implementan funciones clásicas de inserción, rotaciones (rotateRight y rotateLeft), extracción del elemento superior (pqTop y pqPopRoot) y actualización del tamaño del subárbol.

- **Operaciones:**  
  La clase `TreapPriorityQueue` ofrece las funciones `push()`, `top()`, `pop()`, `empty()` y `size()`, las cuales permiten gestionar la inserción y extracción de paquetes en base a su prioridad.

#### b) Tabla de enrutamiento – TreapRoutingTable

- **Objetivo:**  
  Gestionar la información de enrutamiento mediante entradas definidas por destino, nextHop y metric.  
  La clave del BST se basa en el campo `destination` de cada `RouteEntry`.

- **Estructura:**  
  La estructura `RouteEntry` contiene los datos de una entrada de enrutamiento. Los nodos del treap para la tabla (struct `RouteNode`) almacenan estas entradas, junto con un valor aleatorio para la propiedad de heap y punteros a hijos.  
  Se definen funciones de inserción, actualización (en caso de que ya exista la entrada, se actualiza el nextHop y metric), eliminación y búsqueda (rtInsert, rtErase y rtFind). También existe la función inorderPrint para imprimir las entradas en orden.


#### 2. Funcionalidades adicionales

#### a) Pruebas unitarias (runUnitTests)

- **Propósito:**  
  Validar el correcto funcionamiento de ambas estructuras.
  
- **Descripción:**  
  - Para la cola de prioridad, se insertan varios paquetes y se comprueba que el paquete con mayor prioridad (por ejemplo, el que tenga prioridad 30) se encuentre en la raíz. Tras extraer el primer elemento, se valida que la nueva raíz corresponda al siguiente paquete con la siguiente mayor prioridad.
  - Para la tabla de enrutamiento, se insertan varias entradas, se actualiza una de ellas y se eliminan otras, comprobando mediante `assert` que los resultados sean los esperados.

#### b) Profiling (runProfiling)

- **Propósito:**  
  Medir el rendimiento de las operaciones sobre un gran número de elementos.
  
- **Descripción:**  
  - Se realizan 100,000 inserciones seguidas de extracciones en la cola de prioridad, midiendo el tiempo total de ejecución.
  - Asimismo, se insertan 100,000 rutas y se eliminan algunas de forma aleatoria en la tabla de enrutamiento, midiendo el tiempo de inserción y eliminación con la biblioteca `<chrono>`.


#### 3. Modos de ejecución

El programa se adapta según el argumento de línea de comandos:

- **Modo test ("test")**:  
  Ejecuta `runUnitTests()` para validar el comportamiento de las estructuras.
  
- **Modo profiling ("profile")**:  
  Ejecuta `runProfiling()` para medir el rendimiento de un gran número de operaciones.
  
- **Modo demo (sin argumento)**:  
  Se ejecuta la demostración original, mostrando cómo se insertan, procesan y eliminan paquetes en la cola de prioridad, y cómo se gestionan las rutas en la tabla de enrutamiento.

**Ejemplo de ejecución:**
```bash
g++ -std=c++17 -O2 -o network_treap treap_networks.cpp
./network_treap test      # Ejecuta las pruebas unitarias
./network_treap profile   # Ejecuta profiling
./network_treap           # Ejecuta la demo original
```

#### 4. Integración con CMake

Para compilar este código como parte de un proyecto gestionado con CMake, se puede crear un archivo `CMakeLists.txt` con el siguiente contenido:

```cmake
cmake_minimum_required(VERSION 3.10)
project(TreapNetworks)

set(CMAKE_CXX_STANDARD 17)

add_executable(network_treap treap_networks.cpp)
```

**Pasos para compilar con CMake:**
1. Crear un directorio de compilación y acceder a él:
   ```bash
   mkdir build && cd build
   ```
2. Ejecutar CMake y compilar:
   ```bash
   cmake ..
   make
   ```
Esto generará el ejecutable `network_treap`, que se podrá ejecutar en cualquiera de los modos indicados.

### [Treaps de estructuras aleatorizadas](https://github.com/kapumota/CC0E5/blob/main/aplicaciones_treaps/treap_randomized_structs.cpp)

#### 1. Componentes del código

#### a) BST clásico (no balanceado)
- **Implementación:**  
  Se define la estructura `BSTNode` que contiene una clave entera y punteros a sus hijos.  
- **Operaciones:**  
  - `bstInsert()`: Inserta recursivamente una clave en el BST.  
  - `bstFind()`: Realiza la búsqueda de una clave.  
  - `bstHeight()`: Calcula la altura del árbol, como medida del balance (o falta de él).

#### b) Treap (árbol aleatorizado)
- **Implementación:**  
  La estructura `TreapNode` almacena una clave, una prioridad aleatoria (generada con `rand()`) y punteros a los hijos.  
- **Operaciones:**  
  - `treapInsert()`: Inserta una clave respetando las propiedades de BST y de heap; se utilizan rotaciones (rotateRight/rotateLeft) para reestructurar el árbol según la prioridad.  
  - `treapFind()`: Busca una clave en el Treap.  
  - `treapHeight()`: Calcula la altura del Treap, indicador del balance interno.

#### c) SkipList simplificado
- **Implementación:**  
  Se utiliza la estructura `SkipListNode` que almacena una clave y un vector de punteros (para cada nivel) y se define la estructura `SkipList` con un nodo header y un nivel actual.  
- **Operaciones:**  
  - `skipListInsert()`: Inserta una clave en el SkipList utilizando un nivel asignado aleatoriamente (mediante `randomLevel()`).
  - `skipListFind()`: Busca una clave en el SkipList.
  - `skipListHeight()`: En este caso, se toma el número de nodos en el nivel base como métrica aproximada de la “altura” o cantidad de elementos.


#### 2. Módulos de pruebas y profiling

El código incorpora dos funciones principales:

- **Pruebas unitarias y de inserción masiva (`testAllStructures`):**  
  Se genera un vector de NUM_OPER claves aleatorias y se insertan en cada estructura (BST, Treap y SkipList). Se miden los tiempos de inserción y se calcula la altura del BST y del Treap; en el SkipList se cuenta el número de nodos en el nivel 0, usándose como una métrica aproximada.

- **Pruebas de búsqueda aleatoria (`testSearchAllStructures`):**  
  Tras realizar la inserción en las tres estructuras, se generan claves de búsqueda aleatorias y se mide el tiempo que tarda cada estructura en encontrar (o no) dichas claves, contando el número total de aciertos.

Estas pruebas se pueden ejecutar de dos modos:
- **Modo "test":**  
  Ejecuta ambas funciones de pruebas (inserción y búsqueda), validando la operación de cada estructura.
- **Modo "profile":**  
  Ejecuta las mismas funciones pero enfocado en medir y reportar los tiempos de ejecución y la “altura” (o longitud base en el SkipList).


#### 3. Modo de ejecución y uso

El programa se comporta de la siguiente manera según los parámetros recibidos en la línea de comandos:

- **Modo test:**  
  ```bash
  ./randomized_structs test
  ```  
  Ejecuta `testAllStructures()` y `testSearchAllStructures()` y termina.

- **Modo profile:**  
  ```bash
  ./randomized_structs profile
  ```  
  Ejecuta las mismas pruebas pero con un enfoque en la medición del rendimiento.

- **Modo demo (sin argumentos):**  
  ```bash
  ./randomized_structs
  ```  
  Se ejecuta una demostración interactiva que muestra mensajes comparativos basados en los resultados de las pruebas.

Para compilar el código se puede utilizar el siguiente comando:
```bash
g++ -std=c++17 -O2 -o randomized_structs randomized_structs.cpp
```

#### 4. Integración con CMake

Para integrar este código en un proyecto CMake, crea un archivo `CMakeLists.txt` con el siguiente contenido:

```cmake
cmake_minimum_required(VERSION 3.10)
project(RandomizedStructs)

set(CMAKE_CXX_STANDARD 17)

add_executable(randomized_structs treap_randomized_structs.cpp)
```

**Pasos para compilar con CMake:**
1. Crear el directorio de compilación y acceder:
   ```bash
   mkdir build && cd build
   ```
2. Ejecutar CMake y compilar:
   ```bash
   cmake ..
   make
   ```
