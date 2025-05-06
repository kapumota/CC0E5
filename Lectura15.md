### Bloom filters: Reducción de la memoria para rastrear contenido

#### El problema del diccionario: Llevar un registro de cosas

Imagina que trabajas en una gran empresa con su propio servicio de correo electrónico legado, con un equipo limitado y recursos escasos. El nuevo CTO pide un cliente moderno con funcionalidades avanzadas, entre ellas un gestor de contactos inteligente. En la interfaz web, al añadir un destinatario, la aplicación debe comprobar localmente si ya existe en la libreta de direcciones y, de no ser así, preguntar al usuario si desea guardarlo.

Debido a restricciones de infraestructura, no es factible realizar llamadas constantes al servidor o a la base de datos: el sistema heredado apenas soporta unas pocas consultas por segundo, mientras que la carga estimada llega a cientos de correos por segundo.

La solución práctica consiste en descargar la lista completa de contactos una sola vez, guardarla en el **almacenamiento de sesión** del navegador y luego realizar todas las búsquedas contra esta copia local. Este patrón de uso —almacenar un conjunto de claves en memoria para consultas rápidas— es un ejemplo clásico del **problema del diccionario** en ciencias de la computación: cómo representar un conjunto de elementos (las claves) de forma que podamos hacer búsquedas e inserciones de manera eficiente.

#### Alternativas para implementar un diccionario

El nombre no debería sorprender; es exactamente como cuando necesitas buscar una palabra en un diccionario o incluso en una guía telefónica.

Para resumir, la aplicación web de contactos necesita:

- Descargar la lista de contactos desde un servidor  
- Crear una copia local para una búsqueda/almacenamiento rápido  
- Permitir buscar un contacto  
- Proporcionar la opción de agregar un nuevo contacto si la búsqueda no tiene éxito  
- Sincronizar con el servidor cuando se añade un nuevo contacto (o se modifica uno existente)  

Lo que realmente necesitamos es una estructura de datos especializada en este tipo de operaciones; necesitamos que soporte inserciones rápidas y al mismo tiempo, proporcione una forma de buscar una entrada por valor.

Para ser claros, cuando usamos un arreglo simple, no tenemos un método eficiente de los arreglos que nos diga el índice de un elemento `X` ni un método eficiente (es decir, sublineal, p. ej. `O(log n)`) para decirnos si un elemento está o no en el arreglo. La única manera de saber si un elemento está en el arreglo es recorriendo todos los elementos, aunque en un arreglo ordenado podríamos usar búsqueda binaria para acelerar la búsqueda.

Por ejemplo, podríamos almacenar las cadenas `["the", "lazy", "fox"]` en un arreglo, y para buscar `"lazy"`, tendríamos que recorrer todo el arreglo, elemento por elemento.

Un **diccionario** (o **arreglo asociativo**), en cambio, por definición tiene un método nativo que accede eficientemente a las entradas almacenadas mediante una búsqueda por clave. Usualmente esta estructura permite almacenar pares `(clave, valor)`. Por ejemplo, tendríamos una lista como `<("the", "artículo"), ("lazy", "adjetivo"), ("fox", "sustantivo")>`. Podríamos buscar `"lazy"` y el diccionario devolvería `"adjetivo"`.

Otra diferencia con los arreglos regulares es que el orden de inserción en un diccionario no importa; ni siquiera está bien definido. Ese es el precio que pagas por acelerar la búsqueda por valor.

#### Descripción de la API de la estructura de datos: Diccionario

Un diccionario se compone de una colección de pares `(clave, valor)`, de tal forma que:

- Cada clave posible aparece como máximo una vez en la colección.  
- Cada valor puede ser recuperado directamente a través de la clave correspondiente.  

La forma más sencilla de captar la esencia de los diccionarios es pensar en los arreglos regulares como un caso especial: las claves son simplemente el conjunto de índices entre 0 y el tamaño del arreglo menos 1, y siempre podemos recuperar un valor proporcionando su índice. De modo que el arreglo simple `["the", "lazy", "fox"]` puede interpretarse como un diccionario que almacena las asociaciones `(0, "the")`, `(1, "lazy")` y `(2, "fox")`.

Los diccionarios generalizan este concepto, permitiendo que las claves provengan de prácticamente cualquier dominio posible.

**Estructura de datos abstracta: Diccionario (alias arreglo asociativo)**

```  
class Dictionary {
  insert(key, value)
  remove(key) -> value
  contains(key) -> value
}
```

**Contrato con el cliente:**  
Un diccionario almacena de forma permanente todos los pares añadidos por el(los) cliente(s). Si se añadió un par `(K,V)` al diccionario (y no se eliminó posteriormente), entonces `contains(K)` devolverá `V`.

Con esta API definida, podemos esbozar una solución para nuestro problema inicial.

Cuando los usuarios inician sesión en su correo, el cliente recibe una lista de contactos del servidor y los almacena en un diccionario que podemos mantener en memoria (tener tantos contactos que no quepan en el almacenamiento de sesión del navegador sería una situación excepcional incluso para una estrella de Instagram). Si el usuario añade un nuevo contacto a la libreta de direcciones, realizamos una llamada a `insert` en el diccionario. De igual forma, si los usuarios eliminan un contacto existente, simplemente mantenemos el diccionario sincronizado llamando a `remove`. 

Cada vez que un usuario escribe un correo e inserta un destinatario, primero verificamos el diccionario, y solo si el contacto no está en la libreta de direcciones mostramos una ventana emergente preguntando a los usuarios si desean guardar el nuevo contacto.

De esta forma, nunca realizamos una llamada HTTP al servidor (y a su vez a la base de datos) para verificar si un contacto está en la libreta de direcciones, y solo leemos de la base de datos una vez al iniciar (o la primera vez durante una sesión en que redactamos un correo electrónico).  

### Estructuras de datos concretas

Hasta ahora, la teoría ha ido bien, pero  implementar arreglos asociativos para ser usados en sistemas reales es algo completamente distinto.

En teoría, si el dominio (el conjunto de claves posibles) es lo suficientemente pequeño, aún podemos usar arreglos definiendo un orden total sobre las claves y utilizando su posición en dicho orden como índice para un arreglo real. Por ejemplo, si el dominio está compuesto por las palabras `{"a", "terrible", "choice"}`, podríamos ordenar las claves lexicográficamente y luego almacenar los valores en un arreglo de cadenas simple; por ejemplo, `{"article", "noun", "adjective"}`. Si necesitamos representar un diccionario que solo contenga un valor para la clave `"choice"`, podríamos hacerlo configurando los valores correspondientes a las claves ausentes en `null`: `{null, "noun", null}`.

Usualmente, sin embargo, no es el caso, y el conjunto de valores posibles para las claves es lo suficientemente grande como para hacer impráctico usar un arreglo con un elemento para cada posible valor de clave; simplemente requeriría demasiada memoria, la cual permanecería en gran parte sin utilizar.

Para superar este problema con la memoria, presentamos dos implementaciones simples y tres de las alternativas más ampliamente utilizadas.

#### Arreglo no ordenado: inserción rápida, búsqueda lenta

Supongamos que necesitamos buscar una palabra específica en este texto, tal vez un nombre como `"Bloom"` y anotar todos los lugares donde aparece. 

Una opción es recorrer el texto desde la primera página, palabra por palabra, hasta encontrarla. Si necesitamos encontrar todas las apariciones de `"Bloom"`, tendríamos que recorrer el texto de principio a fin. Un texto visto como una colección de palabras en el orden en que están impresas es como un arreglo no ordenado.

La siguiente tabla resume el rendimiento de las operaciones principales utilizando este enfoque con arreglos no ordenados:

| Operación                   | Tiempo de ejecución | Memoria extra |
|-----------------------------|---------------------|---------------|
| Crear la estructura         | O(1)                | Ninguna       |
| Buscar una entrada          | O(n)                | Ninguna       |
| Insertar una entrada nueva  | O(1)                | Ninguna       |
| Eliminar una entrada        | O(1)                | Ninguna       |

Los arreglos no ordenados tienen la ventaja de no requerir trabajo extra al crearlos y agregar una nueva entrada es sencillo, siempre que haya capacidad disponible.

#### Arreglos ordenados y búsqueda binaria: inserción lenta, búsqueda rápida

Si, después de recorrer todo el texto, necesitamos buscar una segunda palabra, como `"filter"`, tenemos que empezar de nuevo y hacer otra pasada por las cientos de miles de palabras. Por eso, muchos textos incluyen un índice al final, allí se encuentra una lista ordenada alfabéticamente de las palabras menos comunes. Las palabras comunes no aparecen porque se usan con demasiada frecuencia (artículos como `"the"` y `"a"` suelen aparecer en cada página) y su presencia en el índice aportaría poco valor. Por el contrario, cuanto más rara es una palabra, más importante es incluirla.

Así, podemos consultar el índice y buscar `"Bloom"`. Al estar en orden lexicográfico, se aplica la búsqueda binaria: se abre el índice en una posición cercana al medio, se mira la primera palabra de esa página y se salta hacia adelante o atrás según corresponda. 

Por ejemplo, si abrimos donde aparece `"Kurtz"`, sabes que `"Bloom"` estará antes, si se abre donde aparece `"Barrow"` sabemos que estará después.

Volviendo al problema de los contactos, un enfoque podría ser ordenar tus contactos y buscarlos usando búsqueda binaria.

| Operación                   | Tiempo de ejecución | Memoria extra |
|-----------------------------|---------------------|---------------|
| Crear la estructura         | O(n log n)          | O(n)          |
| Buscar una entrada          | O(log n)            | Ninguna       |
| Agregar una entrada nueva   | O(n)                | Ninguna       |
| Eliminar una entrada        | O(n)                | Ninguna       |

#### Tabla hash: tiempo constante en promedio, a menos que necesites ordenamiento

Lo principal de las tablas hash es que se usan para implementar arreglos asociativos donde las claves posibles provienen de un conjunto muy grande (por ejemplo, todas las cadenas posibles o todos los enteros), pero normalmente solo se almacenan unas pocas de ellas. Para ello, usamos una función de hash que mapea el dominio (conjunto fuente) a un conjunto más pequeño de `M` elementos (codominio), los índices de un arreglo simple donde guardamos los valores asociados a cada clave.

Dado que el codominio es más pequeño que el dominio, habrá colisiones: al menos dos claves se mapearán al mismo índice. Las tablas hash usan estrategias para resolver conflictos, como **encadenamiento** o **direccionamiento abierto**.

También distinguimos entre **hash maps** y **hash sets**. El primero asocia un valor a cada clave; el segundo solo registra la presencia o ausencia de una clave. Un hash set es un caso especial de diccionario cuyo valor se fija en booleano; el segundo parámetro de `insert` se vuelve redundante, pues se asume que el valor asociado es `true`.

**Estructura de datos abstracta: Set**  
```  
class Set {  
  insert(key)  
  remove(key)  
  contains(key) -> true/false  
}
```

**Contrato con el cliente:**  
Un set mantiene un conjunto de claves. Si se agregó una clave `K` (y no se eliminó posteriormente), `contains(K)` devolverá `true`; en caso contrario, devolverá `false`.

Todas las operaciones en una tabla hash (y en un hash set) se pueden realizar en tiempo amortizado `O(1)`.

#### Árbol de búsqueda binaria: cada operación es logarítmica

Los árboles de búsqueda binaria (BST) son un tipo especial de árbol binario que almacena claves sobre las cuales se define un orden total. Esto significa que, para cada par de claves, debe ser posible compararlas y decidir cuál es menor, o si son iguales. Un orden total es una relación ≤ que, en un conjunto S, cumple cuatro propiedades:

- **Reflexiva:** x ≤ x  
- **Antisimétrica:** si x ≤ y, y ≤ x, entonces x = y  
- **Transitiva:** si x ≤ y,  y ≤ z, entonces x ≤ z  
- **Comparabilidad:** para todo x, y en S, o bien x ≤ y o bien y ≤ x  

Los BST aprovechan estas propiedades para ubicar cada clave recorriendo un único camino desde la raíz hasta una hoja. Al insertar una clave:

1. La comparamos con la clave en la raíz.  
2. Si es menor, bajamos al subárbol izquierdo; si es mayor o igual, al subárbol derecho.  
3. Repetimos hasta encontrar una posición libre y colocamos la nueva clave allí.

La altura de un BST balanceado es `O(log n)`, donde `n` es el número de claves, de modo que las operaciones básicas (búsqueda, inserción y eliminación) toman tiempo `O(log n)`.

Aunque las tablas hash ofrecen tiempo amortizado `O(1)` en esas operaciones, los BST tienen ventajas adicionales:

- **Predecesor y sucesor:** `O(log n)`  
- **Mínimo y máximo:** `O(log n)`  
- **Recorrido ordenado (in‑order):** `O(n)` para recuperar todas las claves en orden ascendente  

En una tabla hash, esas mismas operaciones requieren primero extraer todas las claves (`O(n)`), luego ordenarlas (`O(nlog n)`), o bien escanear todo el dominio (`O(M + n)`), donde `M` es el tamaño del arreglo subyacente.

##### Comparativa de complejidades

| Operación                   | Arreglo no ordenado | Arreglo ordenado | BST balanceado | Tabla hash (amortizado) |
|-----------------------------|---------------------|------------------|----------------|-------------------------|
| Crear la estructura         | O(1)                | O(nlog n)       | O(n log n)     | O(n)                    |
| Buscar una entrada          | O(n)                | O(log n)         | O(log n)       | O(1)                    |
| Agregar una entrada nueva   | O(1)                | O(n)             | O(log n)       | O(1)                    |
| Eliminar una entrada        | O(1)                | O(n)             | O(log n)       | O(1)                    |
| Recuperar lista ordenada    | O(nlogn)          | O(n)             | O(n)           | O(n log n)              |
| Mínimo / Máximo             | O(n)                | O(1)             | O(log n)       | O(n)                    |
| Predecesor / Sucesor        | O(n)                | O(1)             | O(log n)       | O(n)                    |


### Bloom filter

Los bloom filters (filtrados de Bloom) es una estructura de datos nombrada en honor a Burton Howard Bloom, quien los inventó en la década de 1970. Existen cuatro diferencias notables entre las tablas hash y los bloom filters: 

- Los bloom filters básicos no almacenan datos; solo responden a la pregunta, ¿está un dato en el conjunto? En otras palabras, implementan la API de un hash set, no la API de una tabla hash.
- Los bloom filters requieren menos memoria en comparación con las tablas hash; esta es la principal razón de su uso.
- Mientras que una respuesta negativa es 100% precisa, puede haber falsos positivos. Por ahora, ten en cuenta que a veces un bloom filter podría responder que un valor fue agregado cuando en realidad no lo fue.
- No es posible eliminar un valor de un bloom filter. 

Existe un compromiso entre la precisión de un bloom filter y la memoria que utiliza. Cuanta menos memoria, más falsos positivos devuelve. 

Por suerte, existe una fórmula exacta que, dado el número de valores que necesitamos almacenar, puede determinar la cantidad de memoria necesaria para mantener la tasa de falsos positivos dentro de cierto umbral.  

#### ¿Cómo funcionan los bloom filters? 

Adentrémonos ahora en los detalles de la implementación de los bloom filters. Un bloom filter está compuesto por dos elementos: 

- Un arreglo de `m` elementos
- Un conjunto de `k` funciones hash 

El arreglo es (conceptualmente) un arreglo de bits, cada uno de los cuales se establece inicialmente en 0,  cada función hash devuelve un índice entre 0 y `m-1`. 

Es crucial aclarar lo antes posible que no existe una correspondencia 1 a 1 entre los elementos del arreglo y las claves que agregamos al bloom filter. Más bien, usaremos `k` bits (y por lo tanto `k` elementos del arreglo) para almacenar cada entrada en el bloom filter. `k` aquí es típicamente mucho menor que `m`. 

Cabe destacar que `k` es una constante que elegimos al crear la estructura de datos, por lo que cada entrada que agregamos se almacena utilizando la misma cantidad de memoria, exactamente `k` bits. Con valores de tipo cadena, esto es bastante asombroso, ya que significa que podemos agregar cadenas de longitud arbitraria a nuestro filtro utilizando una cantidad constante de memoria, solo `k` bits. 

Cuando insertamos una nueva clave en el filtro, calculamos `k` índices para el arreglo, dados por los valores `h₀(key)` hasta `h₍ₖ₋₁₎(key)` y establecemos esos bits a 1. 

Cuando buscamos una entrada, también necesitamos calcular los `k` hashes para ella como se describió en la inserción, pero esta vez verificamos los `k` bits en los índices devueltos por las funciones hash y devolvemos true si y solo si todos los bits en esas posiciones están establecidos en 1. 

Idealmente, necesitaríamos `k` funciones hash independientes diferentes, de modo que no se dupliquen dos índices para el mismo valor. No es fácil diseñar un gran número de funciones hash independientes, pero podemos obtener buenas aproximaciones. 

Existen algunas soluciones comúnmente usadas: 

- Utilizar una función hash paramétrica `H(i)`. Esta meta-función, que es un generador de funciones hash, toma como entrada un valor inicial `i` y devuelve una función hash `Hᵢ = H(i)`. Durante la inicialización del bloom filter, podemos crear `k` de estas funciones, de `H₀` a `H₍ₖ₋₁₎`, llamando al generador `H` con `k` valores diferentes (y usualmente aleatorios). 
- Utilizar una única función hash `H` pero inicializar una lista `L` de `k` valores aleatorios (y únicos). Para cada clave que se inserte/busque, se crean  `k` valores sumando o concatenando `L[i]` a la clave, y luego se les aplica `H`. (Recuerda que las funciones hash bien diseñadas producirán resultados muy diferentes ante pequeños cambios en la entrada). 
- Utilizar doble o triple hasheo. 

Aunque lo último no garantiza independencia entre las funciones hash generadas, se ha demostrado que podemos relajar esta restricción con un incremento mínimo en la tasa de falsos positivos. Para mantener las cosas simples, en la implementación usamos doble hasheo con dos funciones hash independientes: [Murmur hashing](https://en.wikipedia.org/wiki/MurmurHash) y [Fowler-Noll-Vo](https://en.wikipedia.org/wiki/Fowler%E2%80%93Noll%E2%80%93Vo_hash_function) (fnv1) hashing.

El formato general de la i-ésima función hash, para i entre 0 y `k-1`, será 

```
Hᵢ(key) = murmurhash(key) + i * fnv1(key) + i * i
```

 ### Implementación

Volviendo a la aplicación de contactos: ¿cómo usaríamos un bloom filter para hacerla más rápida? Pues necesitamos usarlo como un diccionario, así que vamos a crear un nuevo bloom filter cuando inicie la aplicación de correo electrónico, recuperar todos los contactos del servidor y agregarlos al bloom filter. 

El listado siguiente resume este proceso de inicialización.

```
//Arranque de una aplicación de correo electrónico

function initBloomFilter(server, minSize)
  contactsList <- server.loadContacts()
  size <- max(2 * |contactsList|, minSize)
  bloomFilter <- new BloomFilter(size)
  for contact in contactsList do
    bloomFilter.insert(contact)
  return bloomFilter
```

- El método `initBloomFilter` toma una interfaz a un servidor (un objeto fachada) y el tamaño mínimo que se debe usar para inicializar el Bloom filter; devuelve el Bloom filter recién creado.  
- Al iniciar, carga opcionalmente la lista de contactos desde un servidor que se encarga del almacenamiento permanente.  
- El tamaño del Bloom filter debe ser al menos el doble del tamaño actual de la lista de contactos, pero al menos igual a `minSize`, un valor mínimo que se puede pasar como argumento.  
- Crea un Bloom filter vacío con el tamaño adecuado.  
- Recorre la lista de contactos.  
- Para cada contacto, lo añade al Bloom filter.

Una vez configurada la aplicación de directorio, tenemos dos operaciones en las que estamos principalmente interesados: comprobar si un contacto está en la lista y agregar un nuevo contacto al directorio.

Para la primera operación, mostrada en el listado siguiente, podemos comprobar el bloom filter, y si dice que el contacto nunca ha sido agregado, entonces tenemos la respuesta, el contacto no está en el sistema. Si, sin embargo, el bloom filter devuelve `true`, entonces podría tratarse de un falso positivo, por lo que necesitamos contactar al servidor para corroborarlo.

```
// Comprobando un correo electrónico

function checkContact(bloomFilter, server, contact)
  if bloomFilter.contains(contact) then
    return server.contains(contact)
  else
    return false
```

- El método `checkContact` verifica si un contacto de correo electrónico está almacenado en la aplicación. Toma un bloom filter, una fachada de servidor y el contacto a comprobar. Devuelve `true` si el contacto ya está en la libreta de contactos.  
- Comprueba el Bloom filter para el contacto pasado al método.  
- Si el Bloom filter devolvió `true`, necesitamos verificar si el servidor realmente almacena el contacto, ya que podría tratarse de un falso positivo.  
- De lo contrario, dado que los bloom filters no tienen falsos negativos (sino solo falsos positivos), podemos devolver `false`.

Para agregar nuevos contactos, siempre debemos sincronizarnos con nuestro almacenamiento permanente, como se muestra a continuación. Dado que esto probablemente implica una conexión remota a través de una red, existe una probabilidad no negligente de que la llamada al servidor falle; por lo tanto, necesitamos manejar las posibles fallas y asegurarnos de que la llamada remota tenga éxito antes de actualizar también el bloom filter.

```
// Agregando un nuevo contacto

function addContact(bloomFilter, server, contact)
  if server.storeContact(contact) then
    bloomFilter.insert(contact)
    return true
  else
    return false
```

- El método `addContact` añade un nuevo contacto al sistema; toma un bloom filter, un objeto servidor y el nuevo contacto a agregar. Devuelve `true` si y solo si la operación tiene éxito.  
- Intenta agregar el contacto al servidor, y si tiene éxito entonces lo añade también al bloom filter y devuelve `true`.  
- De lo contrario, la inserción falló, por lo que se devuelve `false`.

#### Lectura y escritura de bits

Ahora, pasemos a la implementación de un bloom filter, comenzando, como de costumbre, con los métodos auxiliares que nos darán los bloques básicos para construir la implementación de la API.

En particular, necesitamos:

- Alguna forma de leer y escribir bits en cualquier ubicación del buffer de nuestro filtro.  
- Un mapeo entre una clave de entrada y los índices de los bits en el buffer.  
- Un conjunto de funciones hash generadas de forma determinista que se usarán para transformar claves en una lista de índices.

Si estamos usando bloom filters para ahorrar memoria, no tendría sentido almacenar bits de forma ineficiente. Necesitaremos empaquetar bits en el tipo entero más pequeño disponible en el lenguaje de programación que elijamos; por lo tanto, tanto leer como escribir un bit nos obliga a mapear el índice del bit a un par de coordenadas: el elemento del arreglo que contiene el bit y el desplazamiento del bit dentro de ese elemento.

El pseudocódigo muestra cómo calcular esas coordenadas.

```
// Calcular coordenas
function findBitCoordinates(index)
  byteIndex <- floor(index / BITS_PER_INT)
  bitOffset <- index mod BITS_PER_INT
  return (byteIndex, bitOffset)
```

- La función `findBitCoordinates` es un método utilitario que, dada la posición de un bit en un arreglo de bits, devuelve el índice del arreglo y el desplazamiento del bit con respecto al elemento del arreglo en ese índice.  
- Dado el índice del bit a recuperar, extraemos el índice del byte; es decir, qué elemento del buffer del arreglo contiene el bit a extraer. `BITS_PER_INT` es una constante (del sistema) cuyo valor es el número de bits usados para almacenar un `int` en el lenguaje de programación utilizado (para la mayoría de los lenguajes es 32).  
- Extrae el desplazamiento del bit dentro del byte del buffer mediante una operación módulo.  
- Devuelve el índice del byte y el desplazamiento del bit como un par de valores.

Una vez que tenemos esos dos índices, podemos leer o escribir cualquier bit fácilmente; se trata simplemente de un asunto de álgebra de bits. El listado muestra el método `readBit`.

```
// Método readBit

function readBit(bitsArray, index)
  (element, bit) <- findBitCoordinates(index)
  return (bitsArray[element] & (1 << bit)) >> bit
```

- El método `readBit` extrae el bit en la posición `index` del arreglo de bits pasado como primer argumento. Devuelve el valor del bit, es decir, `0` o `1`.  
- Recupera el índice del elemento y el desplazamiento para el bit en el arreglo de bits.  
- Utiliza una máscara de un solo bit y operaciones AND y shift para extraer el valor del bit.

El pseudocódigo muestra la contraparte de escritura, el método `writeBit`.

```
// Método writeBit

function writeBit(bitsArray, index)
  (element, bit) <- findBitCoordinates(index)
  bitsArray[element] <- bitsArray[element] | (1 << bit)
  return bitsArray
```

- El método `writeBit` toma el arreglo de bits y el índice del bit donde se debe escribir un `1`; devuelve el arreglo de bits después de modificarlo.  
- Recupera el índice del elemento y el desplazamiento para el bit en el arreglo de bits.  
- Realiza una operación OR con una máscara de un solo bit para establecer el bit en `1` (nunca se escriben ceros en esta versión).

**Ejemplo de funcionamiento**  
Supongamos que tenemos el buffer `B = [157, 25, 44, 204]` con `BITS_PER_INT = 8`.

- Llamamos a `readBit(B, 19)`; entonces obtenemos `element == 2`, `bit == 3`.  
  - `bitsArray[element]` evalúa a `44`.  
  - `(1 << bit)` es `8`.  
  - `44 & 8` es `8`, y al desplazarlo obtenemos `1`.



- Llamamos a `writeBit(B, 15)`; entonces obtenemos `element == 1`, `bit == 7`.  
  - `bitsArray[element]` evalúa a `25`.  
  - `(1 << bit)` es `128`.  
  - `25 | 128` es `153`.  
  - El buffer se actualiza a `B = [157, 153, 44, 204]`.
 
##### Encontrar dónde se almacena una clave

Para generar todos los índices de los bits usados para almacenar una clave, seguimos un proceso de dos pasos, descrito en el pseudocódigo. Ten en cuenta que nuestro objetivo final es transformar una cadena en *k* posiciones, entre 0 y *m* – 1.

Primero, usamos dos funciones hash sobre cadenas muy diferentes entre sí: *murmur hashing* y *fnv1 hashing*. Las probabilidades de que, para una cadena dada, ambas produzcan el mismo resultado son ínfimas.

Luego, para cada uno de los *k* bits que tenemos que almacenar, recuperamos la función hash correspondiente en nuestro conjunto. Para cada posición *i* entre 0 y *k* -1 hemos generado (en la inicialización) una función de doble hasheo *hₖ*. El *i*-ésimo bit será, por lo tanto, devuelto por `hᵢ(hM, hF)`, donde **hM** es el resultado de aplicar *murmur hashing* a la clave de entrada y **hF** el resultado de aplicar *fnv1 hashing*.

Aunque el mayor nivel de aleatoriedad se obtendría con una semilla aleatoria para cada ejecución, necesitamos forzar un comportamiento determinista tanto para las pruebas como para recrear un bloom filter que pueda interpretar un buffer dado (por ejemplo, tras serializarlo o reiniciar tras una falla). Por lo tanto, también deberíamos dejar la opción de pasar la semilla al constructor del bloom filter.

```
//Método key2Positions
function key2Positions(hashFunctions, seed, key)
  hM <- murmurHash32(key, seed)
  hF <- fnv1Hash32(key)
  return hashFunctions.map(h => h(hM, hF))
```

- El método **key2Positions** toma un arreglo de funciones hash como entrada, junto con una semilla para inicializar estas funciones y la clave que se va a hashear. Devuelve el conjunto de índices de bits que se actualizarán en el bloom filter para leer/escribir la clave.  

- Aplica murmur hashing a la clave, con la semilla dada.  
- Aplica fnv1 hashing a la clave.  
- Usa programación funcional: crea una lambda que aplica cada función `h` del arreglo `hashFunctions` a los dos valores `hM` y `hF`, devolviendo así un arreglo de enteros.

##### Generando funciones hash

En el listado anterior describimos cómo, en `key2Positions`, pasamos un arreglo de funciones hash y lo usamos para transformar una clave en una lista de índices: las posiciones en el arreglo de bits del filtro donde almacenamos la clave. Ahora veamos en el listado siguiente cómo inicializamos estas *k* funciones hash necesarias.

El conjunto de funciones se creará utilizando **doble hashing** para combinar los dos argumentos de *k* formas diferentes. Comparado con hashing lineal o cuadrático, el doble hashing aumenta el número de posibles funciones de O(*k*) a O(*k*²). Aunque sigue lejos de O(*k*! ) de un hashing completamente uniforme, en la práctica basta para mantener baja la tasa de colisiones.

```
// Método initHashFunctions

function initHashFunctions(numHashFunctions, numBits)
  return range(0, numHashFunctions).map(i =>
    (h1, h2) => (h1 + i * h2 + i * i) mod numBits
  )
```

- El método **initHashFunctions** toma el número de funciones deseadas y el número de bits que contiene el bloom filter, y crea una lista de *numHashFunctions* funciones de doble hashing.  
- Usamos programación funcional: mapeamos cada entero `i` de 0 a `numHashFunctions–1` a una lambda que, dados dos hashes `h1` y `h2`, devuelve `(h1 + i·h2 + i²) mod numBits`.


#### 4.6.5 Constructor

Pasemos ahora a la API pública, que reflejará la API para `set`. El constructor debe preparar todo el estado interno de un bloom filter, incluyendo la matemática para calcular el número de bits y de funciones hash necesarias para cumplir la precisión solicitada.

```
// Constructor del bloom filter

function BloomFilter(maxSize, maxTolerance=0.01, seed=random())
  this.size <- 0
  this.maxSize <- maxSize
  this.seed <- seed
  this.numBits <- ceil(-maxSize * ln(maxTolerance) / ln(2) / ln(2))
  if this.numBits > MAX_SIZE then
    throw new Error("Overflow")
  this.numHashFunctions <- ceil(-ln(maxTolerance) / ln(2))
  numElements <- ceil(this.numBits / BITS_PER_INT)
  this.bitsArray <- [0 ... 0]  // numElements enteros inicializados a 0
  this.hashFunctions <- initHashFunctions(this.numHashFunctions, this.numBits)
```

- El argumento **maxTolerance** tiene un valor por defecto de 0.01; **seed** se inicializa por defecto a un entero aleatorio. No todos los lenguajes de programación proveen una sintaxis explícita para valores por defecto en las firmas de funciones, pero existen soluciones para aquellos que no lo hacen.  
- Inicialmente, no se almacena ningún elemento en el filtro, por lo que el tamaño se inicializa a 0.  
- Almacenamos en variables de clase los argumentos (locales) para el constructor.  
- Calcula el número óptimo de bits necesarios:  m = -n*ln(p)/ ln(2)^2
  donde **ceil(x)** es la función techo estándar que devuelve el entero más pequeño mayor o igual a *x*.  
- Verifica que el tamaño quepa en memoria sin problemas.  
- Lanza un error que puede ser manejado por el cliente.  
- Calcula el número óptimo de funciones hash necesarias. Equivalentemente, puede escribirse como : k = m/n * ln(2).
- Calcula el número de elementos para el búfer (entero) al dividir el número total de bits necesarios por el número de bits por entero, usando techo.  
- Crea el búfer que almacenará los bits del filtro, todos inicializados a 0.  
- Crea y almacena las funciones hash que se usarán para obtener los índices de bits para una clave.  

Al crear el filtro, solo necesitamos proporcionar el número máximo de elementos que se espera que contenga. Si en algún momento se almacenan más de **maxSize** elementos, la buena noticia es que no se quedará sin espacio, pero la mala noticia es que ya no podremos garantizar la precisión esperada.

Podemos pasar un segundo parámetro opcional para establecer la precisión deseada. Por defecto, el umbral para la probabilidad de un falso positivo (**maxTolerance**) es del 1%, pero podemos afinarlo pasando un valor menor (mejor precisión) o conformarnos con uno mayor (menos memoria) pasando un valor mayor.

El último parámetro opcional (**seed**) permite forzar un comportamiento determinista para el filtro. Cuando el llamador omite este parámetro, se genera un valor aleatorio para la semilla.

Después de validar los argumentos, establecemos los campos base y calculamos el tamaño del búfer, asegurándonos de que quepa en memoria. A continuación, calculamos el número óptimo de hashes para mantener baja la tasa de falsos positivos.


##### Comprobando una clave

Ahora podemos empezar a componer los métodos auxiliares para construir la API del bloom filter. Ten en cuenta que asumimos que las claves serán cadenas; si usas objetos serializables, necesitarás una función de serialización consistente que convierta objetos equivalentes en la misma cadena.

> **Nota:** El procesamiento y preprocesamiento de datos a menudo son tan importantes, o más que los algoritmos mismos.

Con las funciones auxiliares definidas, comprobar la existencia de una clave es muy sencillo: recuperamos las posiciones de los bits y verificamos que todos estén en 1. El pseudocódigo está en el listado siguiente:

```
// Método contains

function contains(key, positions=null)
  if positions == null then
    positions <- key2Positions(this.hashFunctions, this.seed, key)
  return positions.all(i => readBit(this.bitsArray, i) != 0)
```

- **contains** toma una clave y devuelve **true** solo si todos los bits correspondientes están en 1.  
- Permite pasar el arreglo de posiciones precomputadas para ahorrar el cálculo doble.  
- Usa **readBit** para comprobar cada posición; devuelve **false** si alguno es 0.

Quizá notes que comprobamos `!= 0` en lugar de `== 1` para evitar desplazamientos adicionales y ahorrar unos milisegundos en cada operación.

#### 4.6.7 Almacenando una clave

Almacenar una clave es muy similar a comprobarla, solo que necesitamos un esfuerzo extra para llevar un control del número de elementos añadidos al filtro y usar `write` en lugar de `read`. Nótese que en esta implementación para `insert`, mostrada en el pseudocódigo siguiente, cuando calculamos el tamaño del filtro, llevamos la cuenta del número de elementos únicos añadidos al filtro, en lugar del número total de veces que se llama al método `add`.

```
function insert(key)
  positions <- key2Positions(key)
  if not contains(key, positions) then
    this.size <- this.size + 1
    positions.map(i => writeBit(this.bitsArray, i))
```

- La función `insert` toma una clave y la almacena en el filtro.  
- Transforma la clave en una secuencia de *k* índices de bits con `key2Positions`.  
- Antes de incrementar el tamaño y escribir en los bits, comprobamos que la clave no esté ya contenida en el filtro; así garantizamos contar solo elementos únicos. Nótese cómo pasamos el arreglo de posiciones a `contains` para evitar recalcularlo.  
- Para cada índice, escribimos un `1` en el búfer usando `writeBit`.

Esto se debe a que añadir la misma clave múltiples veces no afecta la precisión del filtro: siempre se cuenta como un único elemento.

Sin embargo, hay un matiz: si una nueva clave única colisiona en todos sus índices con bits ya establecidos en `1`, se considera duplicada y no incrementa `size`. Esto tiene sentido, pues `contains(x)` ya habría devuelto un falso positivo de todas formas.

En este listado también vemos por qué `contains` acepta un parámetro opcional de posiciones precomputadas: dentro de `insert` leemos y luego escribimos, y calcular los índices de bits puede ser costoso. Pasar el resultado a `contains` evita repetir ese cálculo. Para mantener limpia la API, esa sobrecarga debería restringirse a métodos internos (por ejemplo, usando sobrecarga o métodos privados).

Otra alternativa para ahorrar el cálculo duplicado es modificar `writeBit` para que devuelva un booleano indicando si realmente cambió el bit; así, `insert` podría saber si al menos uno cambió y contar en consecuencia. Esa versión alternativa está disponible en el repositorio.

En cualquier caso, contar con precisión las claves únicas tiene un coste; si no esperas muchas inserciones duplicadas, quizá no merezca la pena. Pero es necesario para estimar correctamente la probabilidad de falsos positivos.

##### Estimando la exactitud

La última tarea es proporcionar un método para estimar la probabilidad de un falso positivo basándonos en el estado actual del filtro: el número de elementos almacenados frente a su capacidad máxima. Veamos una implementación básica:

```
function falsePositiveProbability()
  return pow(
    1 - pow(E, this.numHashes * this.size / this.numBits),
    this.numHashes
  )
```
