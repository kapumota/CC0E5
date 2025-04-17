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
  remove(key) → value
  contains(key) → value
}
```

**Contrato con el cliente:**  
Un diccionario almacena de forma permanente todos los pares añadidos por el(los) cliente(s). Si se añadió un par `(K,V)` al diccionario (y no se eliminó posteriormente), entonces `contains(K)` devolverá `V`.

Con esta API definida, podemos esbozar una solución para nuestro problema inicial.

Cuando los usuarios inician sesión en su correo, el cliente recibe una lista de contactos del servidor y los almacena en un diccionario que podemos mantener en memoria (tener tantos contactos que no quepan en el almacenamiento de sesión del navegador sería una situación excepcional incluso para una estrella de Instagram). Si el usuario añade un nuevo contacto a la libreta de direcciones, realizamos una llamada a `insert` en el diccionario. De igual forma, si los usuarios eliminan un contacto existente, simplemente mantenemos el diccionario sincronizado llamando a `remove`. 

Cada vez que un usuario escribe un correo e inserta un destinatario, primero verificamos el diccionario, y solo si el contacto no está en la libreta de direcciones mostramos una ventana emergente preguntando a los usuarios si desean guardar el nuevo contacto.

De esta forma, nunca realizamos una llamada HTTP al servidor (y a su vez a la base de datos) para verificar si un contacto está en nuestra libreta de direcciones, y solo leemos de la base de datos una vez al iniciar (o la primera vez durante una sesión en que redactamos un correo electrónico).  

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
  contains(key) → true/false  
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

Los bloom filters es una estructura de datos nombrada en honor a Burton Howard Bloom, quien los inventó en la década de 1970. Existen cuatro diferencias notables entre las tablas hash y los bloom filters: 

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

Aunque lo último no garantiza independencia entre las funciones hash generadas, se ha demostrado que podemos relajar esta restricción con un incremento mínimo en la tasa de falsos positivos. Para mantener las cosas simples, en nuestra implementación usamos doble hasheo con dos funciones hash independientes: [Murmur hashing](https://en.wikipedia.org/wiki/MurmurHash) y [Fowler-Noll-Vo](https://en.wikipedia.org/wiki/Fowler%E2%80%93Noll%E2%80%93Vo_hash_function) (fnv1) hashing.

El formato general de nuestra i-ésima función hash, para i entre 0 y `k-1`, será 

```
Hᵢ(key) = murmurhash(key) + i * fnv1(key) + i * i
```
