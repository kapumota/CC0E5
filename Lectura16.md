### Bloom filters: Reducción de la memoria para rastrear contenido

#### El problema del diccionario: Llevar un registro de cosas

Imagina que trabajas en una gran empresa con su propio servicio de correo electrónico legado, con un equipo limitado y recursos escasos. El nuevo CTO pide un cliente moderno con funcionalidades avanzadas, entre ellas un gestor de contactos inteligente. En la interfaz web, al añadir un destinatario, la aplicación debe comprobar localmente si ya existe en la libreta de direcciones y, de no ser así, preguntar al usuario si desea guardarlo. Debido a restricciones de infraestructura, no es factible realizar llamadas constantes al servidor o a la base de datos: el sistema heredado apenas soporta unas pocas consultas por segundo, mientras que la carga estimada llega a cientos de correos por segundo.

La solución práctica consiste en descargar la lista completa de contactos una sola vez, guardarla en el almacenamiento de sesión del navegador, y luego  realizar todas las búsquedas contra esta copia local. Este patrón de uso de almacenar un conjunto de claves en memoria para consultas rápidas es un ejemplo clásico del **problema del diccionario** en ciencias de la computación: cómo representar un conjunto de elementos (las claves) de forma que podamos hacer búsquedas e inserciones de manera eficiente.

#### Alternativas para implementar un diccionario

El nombre no debería sorprender; es exactamente como cuando necesitas buscar una palabra en un diccionario o incluso en una guía telefónica.

Para resumir, nuestra aplicación web de contactos necesita:

- Descargar la lista de contactos desde un servidor  
- Crear una copia local para una búsqueda/almacenamiento rápido  
- Permitir buscar un contacto  
- Proporcionar la opción de agregar un nuevo contacto si la búsqueda no tiene éxito  
- Sincronizar con el servidor cuando se añade un nuevo contacto (o se modifica uno existente)  

Lo que realmente necesitamos es una estructura de datos especializada en este tipo de operaciones; necesitamos que soporte inserciones rápidas, y al mismo tiempo proporcione una forma de buscar una entrada por valor.

Para ser claros, cuando usamos un arreglo simple, no tenemos un método eficiente de los arreglos que nos diga el índice de un elemento X, ni un método eficiente (es decir, sublineal) para decirnos si un elemento está o no en el arreglo. La única manera de saber si un elemento está en el arreglo es recorriendo todos los elementos del arreglo, aunque en un arreglo ordenado podríamos usar búsqueda binaria para acelerar la búsqueda.

Por ejemplo, podríamos almacenar las cadenas `["the", "lazy", "fox"]` en un arreglo, y para buscar "lazy", tendríamos que recorrer todo el arreglo, elemento por elemento.

Un arreglo asociativo, en cambio, por definición tiene un método nativo que accede eficientemente a las entradas almacenadas mediante una búsqueda por valor. Usualmente esta estructura permite almacenar pares (clave, valor). Por ejemplo, tendríamos una lista como <(“the”, artículo), (“lazy”, adjetivo), (“fox”, sustantivo)>. Podríamos buscar “lazy” y el arreglo asociativo devolvería adjetivo.

Otra diferencia con los arreglos regulares sería que el orden de inserción en un arreglo asociativo no importa; ni siquiera está bien definido. Ese es el precio que pagas por acelerar la búsqueda por valor.

#### Descripción de la API de la estructura de datos: Arreglo asociativo

Un arreglo asociativo (también referido como diccionario, tabla de símbolos, o simplemente mapa), se compone de una colección de pares `(clave, valor)`, de tal forma que:

- Cada clave posible aparece como máximo una vez en la colección.  
- Cada valor puede ser recuperado directamente a través de la clave correspondiente.  

La forma más sencilla de captar la esencia de los arreglos asociativos es pensar en los arreglos regulares como un caso especial: las claves son simplemente
el conjunto de índices entre 0 y el tamaño del arreglo menos 1, y siempre podemos recuperar un valor proporcionando su índice, de modo que el arreglo (simple)
`["the", "lazy", "fox"]` puede interpretarse como un diccionario que almacena las asociaciones `(0, "the")`, `(1, "lazy")` y `(2, "fox")`.

Los arreglos asociativos generalizan este concepto, permitiendo que las claves provengan de prácticamente cualquier dominio posible.

**Estructura de datos abstracta: Arreglo asociativo (alias diccionario)**

```  
class Dictionary {
  insert(key, value)
  remove(key) → value
  contains(key) → value
}
```

**Contrato con el cliente:**  
Un diccionario almacena de forma permanente todos los pares añadidos por el(los) cliente(s). Si se añadió un par `(K,V)` al diccionario  (y no se eliminó posteriormente), entonces `contains(K)` devolverá `V`.  

Con esta API definida, podemos esbozar una solución para nuestro problema inicial.

Cuando los usuarios inician sesión en su correo, nuestro cliente recibe una lista de contactos del servidor y los almacena en un diccionario que  podemos mantener en memoria (tener tantos contactos que no quepan en el almacenamiento de sesión del navegador sería una situación excepcional incluso 
para una estrella de Instagram). Si el usuario añade un nuevo contacto a nuestra libreta de direcciones, realizamos una llamada a `insert` en el diccionario. 
De igual forma, si los usuarios eliminan un contacto existente, simplemente mantenemos el diccionario sincronizado llamando a `remove`. 
Cada vez que un usuario escribe un correo e inserta un destinatario, primero verificamos el diccionario, y solo si el contacto no está en la libreta de direcciones mostramos una ventana emergente preguntando a los usuarios si desean guardar el nuevo contacto.

De esta forma, nunca realizamos una llamada HTTP a nuestro servidor (y a su vez a la base de datos) para verificar si un contacto está en nuestra libreta de direcciones, y solo leemos de la base de datos una vez al iniciar (o la primera vez durante una sesión en que redactamos un correo electrónico).

### Estructuras de datos concretas

Hasta ahora, la teoría ha ido bien, pero, por supuesto, implementar arreglos asociativos para ser usados en sistemas reales es algo completamente distinto.

En teoría, si el dominio (el conjunto de claves posibles) es lo suficientemente pequeño, aún podemos usar arreglos definiendo un orden total sobre las claves
y utilizando su posición en dicho orden como el índice para un arreglo real. Por ejemplo, si nuestro dominio está compuesto por las palabras `{"a", "terrible", "choice"}`, podríamos ordenar las claves lexicográficamente, y luego almacenaríamos los valores en un arreglo de cadenas 
simple; por ejemplo, `{"article", "noun", "adjective"}`. 
Si necesitamos representar un diccionario que solo contenga un valor para la clave "choice", podríamos hacerlo configurando  los valores correspondientes a las claves ausentes en null: `{null, "noun", null}`.

Usualmente, sin embargo, no es el caso, y el conjunto de valores posibles para las claves es lo suficientemente grande como para hacer impráctico usar un arreglo con un elemento para cada posible valor de clave; simplemente requeriría demasiada memoria, la cual permanecería en gran parte sin utilizar.

Para superar este problema con la memoria, presentamos dos implementaciones ingenuas y tres de las alternativas más ampliamente utilizadas.

####  Arreglo no ordenado: Inserción rápida, búsqueda lenta

Supón que necesitas buscar una palabra específica en este curso, tal vez un nombre como Bloom, y anotar todos los lugares donde aparece. Una opción que tienes es recorrer el curso desde la primera página, palabra por palabra, hasta encontrarla. Si necesitas encontrar todas las apariciones de la palabra Bloom, tendrás que recorrer el curso de principio a fin.

Un curso tomado como una colección de palabras, en el orden en que están impresas, es como un arreglo no ordenado. 

La tabla siguiente no ordenados como diccionarios resume el rendimiento de las operaciones principales necesarias utilizando este enfoque con arreglos no ordenados.

| Operación            | Tiempo de ejecución | Memoria extra |
|----------------------|---------------------|---------------|
| Crear la estructura  | O(1)                | No            |
| Buscar una entrada   | O(n)                | No            |
| Insertar una entrada nueva | O(1)        | No            |
| Eliminar una entrada | O(1)                | No            |

Los arreglos no ordenados tienen la ventaja de no requerir trabajo extra al crearlos, y agregar una nueva entrada es bastante sencillo, siempre que tengas suficiente capacidad.

#### Arreglos ordenados y búsqueda binaria: Inserción lenta, búsqueda rápida (más o menos)

Eso no es exactamente práctico, como te puedes imaginar. Si, después de recorrer todo el curso, necesitas buscar una segunda palabra, como "filter", tendrías
que empezar de nuevo y hacer una segunda pasada a través de las cientos de miles de palabras del curso. Por eso, la mayoría de los cursos tienen lo que se 
llama un índice, usualmente hacia el final del curso; allí puedes encontrar una lista ordenada alfabéticamente de las palabras (y nombres) menos comunes  utilizadas en el curso. Las palabras comunes no aparecen en esta lista porque se usan con demasiada frecuencia (artículos como "the" y "a" probablemente se usan en cada página) y no vale la pena listarlas, ya que el valor de encontrar lugares donde se usan sería mínimo. Por el contrario, cuanto más rara es una palabra en inglés (y los nombres son el ejemplo perfecto aquí), mayor importancia tiene cuando se usa en tu texto.

Así, puedes consultar el índice y buscar el nombre Bloom. Al estar en orden lexicográfico, podrías recorrerlo desde el inicio hasta encontrar la palabra 
que buscas; no debería tomar mucho tiempo con Bloom. No tendrías tanta suerte con términos como hashing o, aún peor, tree, que estarán hacia el final del índice.

Es por ello que, naturalmente, realizamos búsquedas en listas ordenadas utilizando, de forma subconsciente, la búsqueda binaria: con una guía telefónica,  la abres en una página aleatoria alrededor del medio (o más cerca del inicio o final, si tienes una idea de dónde podría estar el nombre que buscas), luego  miras la primera letra de la primera palabra de esa página, y saltas hacia páginas anteriores o posteriores dependiendo de lo que buscas. 
Por ejemplo, si sigues buscando Bloom, y abres una guía telefónica en una página donde el primer apellido es Kurtz, entonces sabes que puedes  descartar todas las páginas después de esa, y mirar solo las páginas anteriores. Abres aleatoriamente otra página (a la izquierda de la que tiene a Kurtz) 
y el último apellido en esa página es Barrow; entonces sabes que Bloom estará en una página después de la que tiene a Barrow y antes de la que tiene a Kurtz.

Volviendo al problema con la lista de contactos, un enfoque podría ser ordenar tus contactos y buscarlos usando búsqueda binaria.

| Operación              | Tiempo de ejecución | Memoria extra |
|------------------------|---------------------|---------------|
| Crear la estructura    | O(nlog(n))         | O(n)          |
| Buscar una entrada     | O(log(n))           | No            |
| Agregar una entrada nueva | O(n)             | No            |
| Eliminar una entrada   | O(n)                | No            |

#### Tabla hash: Tiempo constante en promedio, a menos que necesites ordenamiento

Lo principal a destacar sobre las tablas hash es que se usan para implementar arreglos asociativos donde los valores posibles a almacenar provienen deun conjunto muy grande (por ejemplo, todas las cadenas posibles o todos los enteros), pero normalmente solo necesitamos almacenar un número limitado de ellos. Si ese es el caso, entonces usamos una función de hash para mapear el conjunto de valores posibles (el dominio, o conjunto fuente) a un conjunto más pequeño de M elementos (el codominio, o conjunto objetivo), los índices de un arreglo simple donde almacenamos los valores asociados a cada clave. Típicamente, el conjunto de valores en el dominio se denomina claves, y los valores en el codominio son índices de 0 a M–1.

Dado que el conjunto objetivo de una función de hash es normalmente más pequeño que el conjunto fuente, habrá colisiones: al menos dos valores se mapearán al mismo índice. Las tablas hash usan algunas estrategias para resolver conflictos, como encadenamiento o direccionamiento abierto.

Lo otro importante a tener en cuenta es que distinguimos entre hash maps y hash sets. El primero nos permite asociar un valor a una clave, el segundo solo 
registra la presencia o ausencia de una clave en un conjunto. Los hash sets implementan un caso especial de diccionario, el **Set**.  Con respecto a nuestra definición de diccionario como estructura de datos abstracta, dada al inicio de esta sección, un set es una especialización de
un diccionario, donde el tipo de valor se fija en Booleano; el segundo parámetro de `insert` se vuelve redundante, ya que se asumirá implícitamente que 
el valor asociado a una clave en el hash set es verdadero.

**Estructura de datos abstracta: Set**  
```  
class Set {  
  insert(key)  
  remove(key)  
  contains(key) → true/false  
}  
```

**Contrato con el cliente:**  
Un set mantiene un conjunto de claves. Si una clave K fue agregada al set (y no eliminada posteriormente), entonces `contains(K)` devolverá true, de lo contrario, devolverá false.

Todas las operaciones en una tabla hash (y en un hash set) se pueden realizar en tiempo amortizado `O(1)`.

#### Árbol de búsqueda binaria: Cada operación es logarítmica

Los árboles de búsqueda binaria (BST) son otro viejo conocido nuestro.

Un BST es un tipo especial de árbol binario que puede almacenar claves sobre las cuales se define un orden total: esto significa que para cada par de claves, debe ser posible compararlas y decidir cuál es menor, o si son iguales. Un orden total se beneficia de las propiedades reflexiva, simétrica y transitiva.

**Relaciones de orden**  
Dado un conjunto S sobre el cual definimos una relación de orden ≤, esta relación es un orden total si, para cualesquiera tres claves x, y, z, se cumplen lassiguientes propiedades:

- Reflexiva: x ≤ x  
- Simétrica: si x ≤ y, entonces y ≤ x  
- Transitiva: si x ≤ y y y ≤ z, entonces x ≤ z  

Los BST utilizan estas propiedades para asegurarse de que la posición de una clave en el árbol se pueda determinar simplemente observando un único camino desde la raíz hasta una hoja.

Cuando insertamos una nueva clave, de hecho, la comparamos con la raíz del árbol. Si es menor, tomamos un giro a la izquierda, recorriendo el subárbol  izquierdo de la raíz; de lo contrario, seguimos por el subárbol derecho. En el siguiente paso, repetimos la comparación con la raíz del subárbol, y así
sucesivamente hasta llegar a una hoja, y esa es exactamente la posición donde necesitamos insertar la clave.

Si recuerdas lo que vimos sobre heaps  todas las operaciones en un BST toman un tiempo proporcional a la altura del árbol 
(el camino más largo desde la raíz hasta una hoja). En particular, para los BST balanceados, todas las operaciones toman `O(ln(n))` tiempo, donde `n` es el número de claves añadidas al árbol.

Por supuesto, comparado con el tiempo de ejecución amortizado `O(1)` de las tablas hash, incluso los BST balanceados no parecen ser una buena elección 
para implementar un arreglo asociativo. La salvedad es que, aunque su rendimiento en los métodos fundamentales es ligeramente más lento, los BST permiten una mejora sustancial para métodos como encontrar el predecesor y sucesor de una clave, y encontrar el mínimo y el máximo: todos se ejecutan en tiempo 
asintótico `O(ln(n))` para BST, mientras que las mismas operaciones en una tabla hash requieren `O(n)` tiempo.

Además, los BST pueden devolver todas las claves (o valores) almacenados, ordenados por clave, en tiempo lineal, mientras que para las tablas hash  necesitas ordenar el conjunto de claves después de recuperarlo, por lo que toma `O(M + nln(n))` comparaciones.

Ahora que hemos descrito las estructuras de datos básicas más comúnmente utilizadas para implementar diccionarios, parece un buen momento para recapitular  lo que hemos descrito hasta ahora. 

La tabla siguiente reúne los tiempos de ejecución de las operaciones principales en las posibles implementaciones de diccionarios que mencionamos.

| Operación            | Arreglos no ordenados | Arreglos ordenados | BST            | Tabla hash     |
|----------------------|-----------------------|--------------------|----------------|----------------|
| Crear la DS          | O(1)                  | O(nlog(n))        | O(nlog(n))    | O(n)           |
| Buscar una entrada   | O(n)                  | O(log(n))          | O(log(n))      | O(n/M)         |
| Agregar una entrada  | O(1)                  | O(n)               | O(log(n))      | O(n/M)         |
| Eliminar una entrada | O(1)                  | O(n)               | O(log(n))      | O(n/M)         |
| Lista ordenada       | O(nlog(n))           | O(n)               | O(n)           | O(M + nlog(n))|
| Mín/Máx              | O(n)                  | O(1)               | O(1)           | O(M + n)       |
| Predecesor/Sucesor   | O(n)                  | O(1)               | O(log(n))      | O(M + n)       |


#### Bloom filter: Tan rápido como las tablas hash, pero ahorra memoria (con una salvedad)

Aún no hemos presentado oficialmente esta estructura de datos en el curso, pero hay muchas posibilidades de que ya hayas oído hablar de los Bloom filters.Se trata de una estructura de datos nombrada en honor a Burton Howard Bloom, quien los inventó en la década de 1970.

Existen tres diferencias notables entre las tablas hash y los Bloom filters:

- Los Bloom filters básicos no almacenan datos; solo responden a la pregunta, ¿está un dato en el conjunto?En otras palabras, implementan la API de un hash set, no la API de una tabla hash.  
- Los Bloom filters requieren menos memoria en comparación con las tablas hash; esta es la principal razón de su uso.  
- Mientras que una respuesta negativa es 100 % precisa, puede haber falsos positivos. Explicaremos esto en detalle en unas cuantas secciones. Por ahora, ten en cuenta que a veces un Bloom filter podría responder que un valor fue agregado cuando en realidad no lo fue.  
- No es posible eliminar un valor de un Bloom filter.  

Existe un compromiso entre la precisión de un Bloom filter y la memoria que utiliza. Cuanta menos memoria, más falsos positivos devuelve. 
Por suerte, existe una fórmula exacta que, dado el número de valores que necesitamos almacenar, puede determinar la cantidad de memoria necesaria para mantener la tasa de falsos positivos dentro de cierto umbral.

### ¿Cómo funcionan los Bloom filters?

Adentrémonos ahora en los detalles de la implementación de los Bloom filters. Un Bloom filter está compuesto por dos elementos:

- Un arreglo de `m` elementos  
- Un conjunto de `k` funciones hash  

El arreglo es (conceptualmente) un arreglo de bits, cada uno de los cuales se establece inicialmente en 0; cada función hash devuelve un índice entre `0` y `m-1``.

Es crucial aclarar lo antes posible que no existe una correspondencia 1 a 1 entre los elementos del arreglo y las claves que agregamos al Bloom filter. 
Más bien, usaremos `k` bits (y por lo tanto `k` elementos del arreglo) para almacenar cada entrada en el Bloom filter. `k` aquí es típicamente mucho menor que `m`.

Cabe destacar que `k` es una constante que elegimos al crear la estructura de datos, por lo que cada entrada que agregamos se almacena utilizando la misma cantidad de memoria, exactamente `k` bits. 
Con valores de tipo cadena, esto es bastante asombroso, ya que significa que podemos agregar cadenas de longitud arbitraria a nuestro filtro utilizando 
una cantidad constante de memoria, solo `k` bits.

Cuando insertamos una nueva clave en el filtro, calculamos `k` índices para el arreglo, dados por los valores `h₀(key)` hasta `h₍ₖ₋₁₎(key)` y establecemos esos bits a 1.

Cuando buscamos una entrada, también necesitamos calcular los `k` hashes para ella como se describió en la inserción, pero esta vez verificamos los `k` bits en 
los índices devueltos por las funciones hash y devolvemos `true` si y solo si todos los bits en esas posiciones están establecidos en 1.

Idealmente, necesitaríamos `k` funciones hash independientes diferentes, de modo que no se dupliquen dos índices para el mismo valor.  No es fácil diseñar un gran número de funciones hash independientes, pero podemos obtener buenas aproximaciones. Existen algunas soluciones comúnmente usadas:

1. **Función hash paramétrica H(i).** Esta meta-función, que es un generador de funciones hash, toma como entrada un valor inicial *i* y devuelve una función hash Hᵢ = H(i). Durante la inicialización del Bloom filter, podemos crear k de estas funciones, de H₀ a H₍ₖ₋₁₎, llamando al generador H con k valores diferentes (y usualmente aleatorios).  
2. **Lista de valores aleatorios L.** Utilizar una única función hash H pero inicializar una lista L de k valores aleatorios (y únicos). Para cada clave que se inserte/busque, se crean k valores sumando o concatenando L[i] a la clave, y luego se les aplica H. (Recuerda que las funciones hash bien diseñadas producirán resultados muy diferentes ante pequeños cambios en la entrada).  
3. **Doble o triple hasheo.** Aunque no garantiza independencia total, se ha demostrado que se puede relajar esta restricción con un incremento mínimo en la tasa de falsos positivos. Para mantener la simplicidad, en nuestra implementación usamos doble hasheo con dos funciones hash independientes: Murmur hashing y Fowler–Noll–Vo (fnv1) hashing.

El formato general de nuestra *i*-ésima función hash, para *i* entre 0 y k–1, será:  
```
Hᵢ(key) = murmurhash(key) + i * fnv1(key) + i * i
```
