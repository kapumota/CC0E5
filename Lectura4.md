### Optimización de tareas con colas de prioridad

#### El problema: Manejar la prioridad

El primer problema que vamos a abordar es el manejo de tareas basadas en la prioridad. Esto es algo con lo que todos estamos familiarizados de alguna manera. El problema puede describirse en estos términos: dada una colección de tareas con diferentes prioridades, determinar qué tarea debe ejecutarse a continuación.

Podemos encontrar muchos ejemplos en el mundo real donde aplicamos, consciente o inconscientemente, técnicas que nos ayudan a decidir qué hacer a continuación. Nuestras vidas diarias están llenas de tareas; generalmente, el orden en el que las realizamos es resultado de las limitaciones de tiempo y de la importancia que les asignamos.

Un ejemplo común de un entorno en el que las tareas se ejecutan por prioridad es una sala de emergencias, donde los pacientes son atendidos, no según el orden en que llegaron, sino en función de la urgencia de sus condiciones. Si nos acercamos a nuestro dominio de IT, existen muchas herramientas y sistemas que tienen el mismo comportamiento. Piensa, por ejemplo, en el planificador de tu sistema operativo o en una aplicación móvil para gestionar una lista de tareas.


#### Prioridad en la práctica: Seguimiento de errores

El ejemplo que me gustaría utilizar, sin embargo, es un sistema de seguimiento de errores. Probablemente ya estés familiarizado con una herramienta de este tipo. Cuando trabajas en equipo, necesitas una forma de rastrear errores y tareas para que no dos personas trabajen en el mismo problema y se duplique el esfuerzo, asegurándote a la vez de que los problemas se aborden en el orden correcto (según el modelo de negocio).

Para simplificar nuestro ejemplo, limitemos el caso a una herramienta de seguimiento de errores donde cada error está asociado con una prioridad, expresada como el número de días dentro de los cuales necesita ser solucionado (números menores indican mayor prioridad). Además, supongamos que los errores son independientes, por lo que ningún error requiere solucionar otro error como requisito previo. Para nuestro ejemplo, consideremos la siguiente lista de errores (en orden disperso) para una aplicación web de una sola página.

Cada error se verá como una tupla: `<descripción de la tarea, importancia de no cumplir con el plazo>`. Así, por ejemplo, podríamos tener lo siguiente:

##### Versión 1

| Descripción de la tarea                                                        | Severidad (1-10) |
| ------------------------------------------------------------------------------ | ---------------- |
| Las cargas de la página tardan más de 2 segundos                                 | 7                |
| La interfaz se rompe en el navegador X                                         | 9                |
| Campo de formulario opcional bloqueado al usar el navegador X el viernes 13      | 1                |
| El estilo CSS causa desalineación                                              | 8                |
| El estilo CSS causa una desalineación de 1px en el navegador X                   | 5                |

Siempre que los recursos (por ejemplo, desarrolladores) sean limitados, surge la necesidad de priorizar los errores. Por lo tanto, algunos errores son más urgentes que otros, y por ello se les asocia una prioridad.

Ahora, supongamos que una desarrolladora de nuestro equipo termina su tarea actual. Ella le pide a nuestro sistema que le indique el siguiente error que necesita ser solucionado. Si esta lista fuera estática, el software de nuestro sistema podría simplemente ordenar los errores una vez y devolverlos en ese orden.

##### Versión 2

| Descripción de la tarea                                                        | Severidad (1-10) |
| ------------------------------------------------------------------------------ | ---------------- |
| La interfaz se rompe en el navegador X                                         | 9                |
| El estilo CSS causa desalineación                                              | 8                |
| Las cargas de la página tardan más de 2 segundos                                 | 7                |
| El estilo CSS causa una desalineación de 1px en el navegador X                   | 5                |
| Campo de formulario opcional bloqueado al usar el navegador X el viernes 13      | 1                |

Como puedes imaginar, sin embargo, ese no es el caso. Primero, se descubren nuevos errores todo el tiempo, por lo que se añadirán nuevos elementos a la lista. Supón que se descubre un desagradable error de encriptación. Además, la prioridad de los errores puede cambiar con el tiempo. Por ejemplo, tu CEO podría decidir que debes enfocarte en la cuota de mercado que usa mayoritariamente el navegador X, y tienes un gran lanzamiento de funcionalidad el próximo viernes 13, por lo que realmente necesitas solucionar ese error, el que estaba al final, en un par de días.

##### Versión 3

| Descripción de la tarea                                                        | Severidad (1-10) |
| ------------------------------------------------------------------------------ | ---------------- |
| Contraseña sin encriptar en la base de datos                                   | 10               |
| La interfaz se rompe en el navegador X                                         | 9                |
| Campo de formulario opcional bloqueado al usar el navegador X el viernes 13      | 8                |
| El estilo CSS causa desalineación                                              | 8                |
| Las cargas de la página tardan más de 2 segundos                                 | 7                |
| El estilo CSS causa una desalineación de 1px en el navegador X                   | 5                |


#### Soluciones a la mano: Mantener una lista ordenada

Obviamente, podríamos actualizar nuestra lista ordenada cada vez que se inserta, elimina o modifica un elemento. Esto puede funcionar bien si estas operaciones son poco frecuentes y el tamaño de nuestra lista es pequeño.

Cualquiera de estas operaciones, de hecho, requeriría que un número lineal de elementos cambie de posición, tanto en el peor caso como en el caso promedio. Para este caso de uso, probablemente funcionaría. Pero si nuestra lista tuviera millones o miles de millones de elementos, lo más probable es que tendríamos problemas.

#### De listas ordenadas a colas de prioridad

Afortunadamente para nosotros, hay una solución mejor. Este es el caso de uso perfecto para una de las estructuras de datos fundamentales. Una **cola de prioridad** mantendrá un ordenamiento parcial de los elementos, con la garantía de que el siguiente elemento devuelto de la cola tendrá la mayor prioridad.

Al renunciar al requisito de un ordenamiento total (que no necesitaríamos en este caso, porque solo consumimos tareas una por una), ganamos en rendimiento: cada una de las operaciones en la cola ahora puede requerir solo tiempo logarítmico.

Como nota adicional, esto nos recuerda lo importante que es definir correctamente nuestros requisitos antes de implementar cualquier solución. Necesitamos asegurarnos de no sobrecomplicar nuestro trabajo y requisitos: por ejemplo, mantener una lista de elementos ordenada cuando lo único que necesitamos es un ordenamiento parcial desperdicia recursos y complica nuestro código, haciéndolo más difícil de mantener y escalar.

#### Describiendo la API de la estructura de datos: Colas de prioridad

Cada estructura de datos se puede descomponer en algunos componentes de nivel inferior:

- **API** — La API es el contrato que una estructura de datos (ED) establece con los clientes externos. Incluye definiciones de métodos, así como algunas garantías sobre el comportamiento de los métodos que se proporcionan en la especificación de la ED. Por ejemplo, una cola de prioridad (PQ) proporciona estos métodos y garantías:
  - `top()` - Devuelve y extrae el elemento con la mayor prioridad.
  - `peek()` - Al igual que `top()`, devuelve el elemento con la mayor prioridad, pero sin extraerlo de la cola.
  - `insert(e, p)` - Agrega un nuevo elemento `e` con prioridad `p` a la PQ.
  - `remove(e)` - Elimina el elemento `e` de la cola.
  - `update(e, p)` - Cambia la prioridad del elemento `e` y la establece en `p`.

- **Invariantes** - (Opcional) Propiedades internas que se mantienen verdaderas a lo largo de la vida de la estructura de datos. Por ejemplo, una lista ordenada tendría la invariante de que cada elemento no es mayor que su sucesor. El propósito de las invariantes es asegurarse de que se cumplan siempre las condiciones necesarias para respetar el contrato con los clientes externos. Son las contrapartes internas de las garantías en la API.

- **Modelo de datos** - Donde se alojan los datos. Esto puede ser un bloque de memoria sin procesar, una lista, un árbol, etc.

- **Algoritmos** - La lógica interna que se utiliza para actualizar la estructura de datos asegurándose de que no se violen las invariantes.

##### API y contrato para la cola de prioridad

**Estructura de datos abstracta:** Cola de prioridad

```
class PriorityQueue {
    top() -> elemento
    peek() -> elemento
    insert(elemento, prioridad)
    remove(elemento)
    update(elemento, nuevaPrioridad)
    size() -> int
}
```

>**Contrato con el cliente:**  
>El elemento superior devuelto por la cola es siempre el elemento con la mayor prioridad actualmente almacenado en la cola.

Existe una diferencia entre una estructura de datos abstracta y las estructuras de datos concretas. La primera incluye la API e invariantes, describiendo a un alto nivel cómo interactuarán los clientes con ella y los resultados y el rendimiento de las operaciones. La segunda se basa en los principios y la API expresados por la descripción abstracta, añadiendo una implementación concreta para su estructura y algoritmos (modelo de datos y algoritmos).

Esta es exactamente la relación entre las colas de prioridad y los *heaps*. Una cola de prioridad es una estructura de datos abstracta que se puede implementar de muchas formas (incluida como una lista ordenada). Un *heap* es una implementación concreta de la cola de prioridad que utiliza un arreglo para contener los elementos y algoritmos específicos para hacer cumplir las invariantes.


#### Cola de prioridad en acción

Imagina que se te proporciona una cola de prioridad. Esta puede provenir de una biblioteca de terceros o de una biblioteca estándar (muchos lenguajes, como C++ o Scala, ofrecen una implementación de colas de prioridad en su librería de contenedores estándar).

No necesitas conocer los detalles internos de la biblioteca en este punto; solo necesitas seguir su API pública y usarla, confiado en que está implementada correctamente. Este es el enfoque de "caja negra".

Por ejemplo, supongamos que añadimos nuestros errores a nuestra PQ en el mismo orden que vimos anteriormente:

##### Versión 4

| Descripción de la tarea                                                        | Severidad (1-10) |
| ------------------------------------------------------------------------------ | ---------------- |
| Las cargas de la página tardan más de 2 segundos                                 | 7                |
| La interfaz se rompe en el navegador X                                         | 9                |
| Campo de formulario opcional bloqueado al usar el navegador X el viernes 13      | 1                |
| El estilo CSS causa desalineación                                              | 8                |
| El estilo CSS causa una desalineación de 1px en el navegador X                   | 5                |

Si devolviéramos las tareas en el mismo orden en que se insertaron, simplemente estaríamos implementando una cola sencilla.

En cambio, supongamos que ahora tenemos nuestra cola de prioridad conteniendo esos cinco elementos; aún no conocemos los detalles internos de la PQ, pero podemos consultarla a través de su API. Por ejemplo, podemos comprobar cuántos elementos contiene e incluso echar un vistazo al que está en la parte superior. O podemos pedirle directamente que nos devuelva el elemento superior (el de mayor prioridad) y lo elimine de la cola.

##### Versión 5

| Descripción de la tarea                                                        | Severidad (1-10) |
| ------------------------------------------------------------------------------ | ---------------- |
| La interfaz se rompe en el navegador X                                         | 9                |
| El estilo CSS causa desalineación                                              | 8                |
| Las cargas de la página tardan más de 2 segundos                                 | 7                |
| El estilo CSS causa una desalineación de 1px en el navegador X                   | 5                |
| Campo de formulario opcional bloqueado al usar el navegador X el viernes 13      | 1                |

Si en la siguiente llamada a `top()` el elemento devuelto es **"La interfaz se rompe en el navegador X"**, el tamaño de la cola se convertirá en 4. Si llamamos a `top()` nuevamente, el siguiente elemento será **"El estilo CSS causa desalineación"** y el tamaño se convertirá en 3.

Mientras la cola de prioridad esté implementada correctamente y dadas las prioridades en nuestros ejemplos, podemos estar seguros de que esos dos elementos serán los devueltos primero, independientemente del orden en el que se hayan insertado.


#### La prioridad importa: Generalizar FIFO

Ahora, la pregunta es cómo elegimos la prioridad de un elemento. A menudo, el orden natural dado por el tiempo que un elemento espera en una fila puede considerarse el más justo. Sin embargo, a veces hay algo especial en algunos elementos que podría sugerir que deberían ser atendidos antes que otros que han esperado más tiempo. Por ejemplo, no siempre lees tus correos electrónicos en el orden en que los recibiste, sino que a menudo te saltas boletines o chistes "divertidos" de amigos para leer primero los mensajes relacionados con el trabajo. Del mismo modo, en una sala de emergencias, el siguiente caso atendido no será necesariamente el que ha estado esperando más tiempo.

Más bien, cada caso se evalúa a la llegada y se le asigna una prioridad, y se llamará al de mayor prioridad cuando un médico esté disponible. Esa es la idea detrás de las colas de prioridad: se comportan como colas regulares y sencillas, excepto que el frente de la cola se determina dinámicamente en función de algún tipo de prioridad. Las diferencias que introduce la prioridad en la implementación son profundas, lo suficiente como para merecer un tipo especial de estructura de datos.

Pero eso no es todo: incluso podemos definir contenedores básicos como bolsas o pilas como casos especiales de colas de prioridad. Este es un tema interesante para profundizar en la comprensión del funcionamiento de las colas de prioridad, aunque en la práctica esos contenedores usualmente se implementan de forma ad hoc, ya que podemos lograr un mejor rendimiento aprovechando sus características específicas.

#### Estructuras de datos concretas

Pasemos ahora de las estructuras de datos abstractas a las concretas. Conocer cómo funciona la API de una cola de prioridad es suficiente para utilizarla, pero a menudo no es suficiente para usarla de manera óptima. Especialmente en componentes críticos en tiempo o en aplicaciones intensivas en datos, es necesario comprender los detalles internos de las estructuras de datos y de su implementación para asegurarnos de poder integrarla en nuestra solución sin introducir un cuello de botella.

Toda abstracción debe implementarse utilizando una estructura de datos concreta. Por ejemplo, una pila se puede implementar usando una lista, un arreglo o en teoría, incluso un heap. La elección de la estructura de datos subyacente influirá únicamente en el rendimiento del contenedor. Escoger la mejor implementación suele ser un compromiso: algunas estructuras de datos aceleran ciertas operaciones, pero harán que otras sean más lentas.

#### Comparando el rendimiento

Para la implementación de una cola de prioridad, inicialmente consideraremos tres alternativas ingenuas utilizando las estructuras de datos fundamentales:

- **Arreglo no ordenado:** simplemente se añaden elementos al final.
- **Arreglo ordenado:** se restablece el orden cada vez que se añade un nuevo elemento.
- **Árboles balanceados:** de los cuales los *heaps* son un caso especial.

Comparemos, en la tabla 1, los tiempos de ejecución para operaciones básicas implementadas con estas estructuras de datos.

#### Tabla 1: Rendimiento para las operaciones de las colas de prioridad

| Operación        | Arreglo no ordenado | Arreglo ordenado | Árbol balanceado |
| ---------------- | ------------------- | ---------------- | ---------------- |
| Insertar         | O(1)                | O(n)             | O(log n)         |
| Encontrar mínimo | O(1)¹               | O(1)             | O(1)¹            |
| Eliminar mínimo  | O(n)²               | O(1)³            | O(log n)         |

¹ Se asume que se guarda un valor extra con el mínimo y se asume el costo de mantenerlo al insertar y eliminar.  
² Si se usa un búfer para acelerar la búsqueda del mínimo, al eliminar se debe encontrar el siguiente mínimo.  
³ Al almacenar el arreglo en orden inverso, eliminar el último elemento podría ser solo cuestión de reducir el tamaño del arreglo o llevar la cuenta del último elemento.

Además, la mayoría de las veces los contenedores, y las colas de prioridad en particular, se usan como estructuras de soporte, lo que significa que forman parte de algoritmos o estructuras de datos más complejos. Cada ciclo del algoritmo principal puede llamar a operaciones en la cola de prioridad varias veces. Por ejemplo, para un algoritmo de ordenamiento, esto podría significar pasar de `O(n²)` (inviable para n tan grande como 1 millón o incluso menos) a `O(nlog(n))`, lo que sigue siendo tratable incluso para entradas de tamaño de 1 billón o más. Sin embargo, esto tiene un costo, ya que la implementación de árboles binarios balanceados generalmente no es trivial.
