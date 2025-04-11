### [Treaps de intervalos](https://github.com/kapumota/CC0E5/blob/main/aplicaciones_treaps/treap_intervalos.cpp) 

### 1. Estructura y funcionalidad del código

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

### 2. Funciones adicionales

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

### 3. Modos de ejecución

El programa admite tres modos de ejecución determinados por argumentos de línea de comandos:

- **Modo test:**  
  Ejecutar  
  ```bash
  ./programa test
  ```  
  Llama a `runUnitTests()` para validar el funcionamiento de las operaciones.

- **Modo profiling:**  
  Ejecutar  
  ```bash
  ./programa profile
  ```  
  Llama a `runProfiling()` para medir el rendimiento en operaciones masivas.

- **Modo demostración:**  
  Ejecutar sin argumentos  
  ```bash
  ./programa
  ```  
  Se ejecuta una demostración que realiza operaciones básicas en ambos treaps (inserciones, búsquedas, eliminación y consultas de intervalos).

### 4. Compilación e integración con CMake

#### a) **Compilación con g++**

Puedes compilar el código (guardado en `treap_intervalos.cpp`) con el siguiente comando:
```bash
g++ -std=c++11 -O2 treap_intervalos.cpp -o programa
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

### 1. Estructura del código

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


### 2. Funcionalidades adicionales

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

### 3. Forma de ejecución

El programa admite tres modos de operación:

- **Pruebas unitarias:**  
  Ejecuta:
  ```bash
  ./programa test
  ```
  Esto ejecuta `runUnitTests()` para validar las operaciones básicas del treap concurrente.

- **Profiling:**  
  Ejecuta:
  ```bash
  ./programa profile
  ```
  Ejecuta `runProfiling()` para medir el rendimiento concurrente del treap.

- **Demostración:**  
  Ejecuta:
  ```bash
  ./programa
  ```
  Sin argumentos, se ejecuta `runDemo()` para mostrar el funcionamiento del treap en un escenario concurrente.


### 4. Integración con CMake

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
  ./programa test
  ```  
  Ejecuta las pruebas unitarias.
- **Modo "profile":**  
  ```bash
  ./programa profile
  ```  
  Ejecuta la rutina de profiling.
- **Modo de demostración:**  
  ```bash
  ./programa
  ```  
  Sin argumentos, se corre la demostración original, en la que se inserta un conjunto de registros, se muestran búsquedas y se simula un merge entre shards.

#### 4. Compilación e integración con CMake

#### a) Compilación con g++
Para compilar el código con soporte para C++17, se puede usar el siguiente comando (considerando que el archivo se llama **treap_distribuido.cpp**):
```bash
g++ -std=c++17 treap_distribuido.cpp -o programa
```
Luego se ejecuta utilizando:
- `./programa test`  
- `./programa profile`  
- `./programa`

#### b) Ejemplo de CMakeLists.txt
Para integrar el código en un proyecto con CMake, cree un archivo `CMakeLists.txt` con el siguiente contenido:
```cmake
cmake_minimum_required(VERSION 3.10)
project(TreapConcurrencia)

set(CMAKE_CXX_STANDARD 17)

add_executable(programa treap_concurrencia.cpp)
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

