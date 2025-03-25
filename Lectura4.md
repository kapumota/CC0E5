### **Introducción y contexto general**

Establecemos las bases para construir estructuras de datos cada vez más avanzadas. Se exploran mejoras sobre estructuras básicas (como heaps binarios y árboles no balanceados) y 
se muestran ejemplos que evidencian que la solución óptima depende siempre del contexto y de los requisitos del problema.  

#### **Mejorando las colas de prioridad: heaps d-arios**

##### *Descripción del problema: manejar la prioridad*  
El primer problema que se aborda es el manejo de tareas basadas en prioridad. Se trata de determinar, dada una colección de tareas con diferentes niveles de urgencia, cuál debe ejecutarse a continuación.  
Ejemplos comunes de este problema son el funcionamiento de salas de emergencias, planificadores de sistemas operativos o aplicaciones móviles para gestionar listas de tareas.

##### *Ejemplo práctico: seguimiento de errores*  
Para ilustrar el problema se propone el caso de un sistema de seguimiento de errores en el que cada error está asociado a una prioridad (por ejemplo, la cantidad de días en que debe ser solucionado, siendo los números menores los de mayor urgencia).  
Se presenta una lista inicial de errores, cada uno con su descripción y severidad (en una escala del 1 al 10). Por ejemplo:  

- Las cargas de la página tardan más de 2 segundos – Severidad 7  
- La interfaz se rompe en el navegador X – Severidad 9  
- Campo de formulario bloqueado en el navegador X el viernes 13 – Severidad 1  
- El estilo CSS causa desalineación – Severidad 8  
- El estilo CSS causa una desalineación de 1px en el navegador X – Severidad 5  

Si se insertan estos errores en orden de aparición, la solución con una lista ordenada produciría un reordenamiento de la siguiente manera:  

- La interfaz se rompe en el navegador X – Severidad 9  
- El estilo CSS causa desalineación – Severidad 8  
- Las cargas de la página tardan más de 2 segundos – Severidad 7  
- El estilo CSS causa una desalineación de 1px – Severidad 5  
- Campo de formulario bloqueado – Severidad 1  

Sin embargo, en un escenario real se descubren nuevos errores y pueden cambiar las prioridades (por ejemplo, la aparición de un error crítico como 
"Contraseña sin encriptar en la base de datos" con severidad 10), lo que exige una solución dinámica para mantener el orden de prioridades.


##### *Soluciones para mantener el orden*  
Una opción es actualizar una lista ordenada cada vez que se inserta, elimina o modifica un elemento. Esto puede funcionar en escenarios con pocos elementos, pero si la lista contiene millones de elementos, el costo de reordenar la lista (con operaciones lineales) se vuelve prohibitivo.  
La solución óptima es utilizar una **cola de prioridad**, que permite mantener un ordenamiento parcial con la garantía de que el siguiente elemento a procesar es siempre el de mayor prioridad. Al renunciar a un ordenamiento total se gana eficiencia: cada operación en la cola puede realizarse en tiempo logarítmico.

##### *Estructura y API de la cola de prioridad*  
Se define la API (el contrato) de la cola de prioridad de la siguiente manera:

```
class PriorityQueue { 
    top() → elemento  
    peek() → elemento  
    insert(elemento, prioridad)  
    remove(elemento)  
    update(elemento, nuevaPrioridad)  
    size() → int
}
```

Esta interfaz establece, por ejemplo, que:
- **top()** devuelve y extrae el elemento con la mayor prioridad.  
- **peek()** devuelve el elemento de mayor prioridad sin extraerlo.  
- **insert(e, p)** añade un nuevo elemento *e* con prioridad *p*.  
- **remove(e)** elimina el elemento *e*.  
- **update(e, p)** actualiza la prioridad del elemento *e*.  
- **size()** retorna el número de elementos almacenados.

Se destaca que la cola de prioridad se considera una "caja negra": el usuario interactúa únicamente a través de esta API sin necesidad de conocer los detalles internos de su implementación. Además, se hace la diferenciación entre la estructura de datos abstracta (la API y las invariantes que debe cumplir) y la implementación concreta (por ejemplo, mediante un heap basado en un arreglo).

##### *Uso práctico de la cola de prioridad*  
Imagina que se insertan los errores en la cola de prioridad. El sistema, a través de su API, permite conocer el número de elementos y obtener el elemento superior (de mayor prioridad) mediante la operación **top()**, la cual extrae dicho elemento. Por ejemplo, al llamar a **top()** se obtendría "La interfaz se rompe en el navegador X" (con severidad 9), y al llamarla nuevamente se obtendría "El estilo CSS causa desalineación" (con severidad 8). Así, el manejo de la prioridad se realiza sin necesidad de ordenar la lista completa en cada modificación.

##### *La prioridad como generalización de FIFO*  
Aunque el orden natural de llegada (FIFO) puede ser considerado justo en algunos casos, existen situaciones donde ciertos elementos deben ser atendidos antes que otros, independientemente del orden de inserción.  
Por ejemplo, en una sala de emergencias o al gestionar correos electrónicos, no se sigue estrictamente el orden de llegada, sino que se evalúa la importancia o urgencia de cada elemento. Esto ilustra cómo las colas de prioridad permiten implementar un mecanismo en el que la "prioridad" del elemento determina el orden de atención.

##### *Implementaciones concretas y comparación de rendimiento*  
Se evalúan tres alternativas para implementar una cola de prioridad utilizando estructuras de datos básicas:
  
- **Arreglo no ordenado:**  
  - Inserción en O(1).  
  - Búsqueda del mínimo en O(1) (si se guarda el valor extra del mínimo), pero eliminación en O(n) (o viceversa, según el método).

- **Arreglo ordenado:**  
  - Inserción en O(n).  
  - Eliminación del mínimo en O(1).

- **Árbol balanceado (heap):**  
  - Ambas operaciones (inserción y eliminación del mínimo) en O(log n).

La siguiente tabla resume el rendimiento de las operaciones:

Tabla: Rendimiento para las operaciones provistas por las colas de prioridad, desglosadas según la estructura de datos subyacente:

Operación         | Arreglo no ordenado | Arreglo ordenado | Árbol balanceado  
------------------|---------------------|------------------|-------------------  
Insertar          | O(1)                | O(n)             | O(log n)  
Encontrar mínimo  | O(1) a              | O(1)             | O(1) a  
Eliminar mínimo   | O(n) b              | O(1) c           | O(log n)  

a) Se asume el costo de mantener un valor extra para el mínimo al insertar y eliminar.  
b) Si se usa un búfer para acelerar la búsqueda del mínimo, al eliminar se debe buscar el siguiente mínimo.  
c) Al almacenar el arreglo en orden inverso, eliminar el último elemento puede implicar simplemente reducir el tamaño del arreglo.

Esta comparación enfatiza la importancia de elegir una estructura de datos adecuada según el tamaño del conjunto y la frecuencia de operaciones, ya que la diferencia entre un comportamiento lineal y uno logarítmico puede ser determinante en aplicaciones a gran escala.

##### *Relación entre estructuras abstractas y concretas*

Toda estructura de datos abstracta (como la cola de prioridad) se implementa mediante una estructura de datos concreta (como un heap).  
- La **estructura abstracta** define la API, las invariantes y el comportamiento esperado.  
- La **implementación concreta** se encarga de la representación interna (por ejemplo, mediante un arreglo) y de los algoritmos específicos que garantizan el cumplimiento de las invariantes.

Esta diferenciación es fundamental para poder utilizar y optimizar la estructura en componentes críticos de sistemas y algoritmos complejos, donde cada operación puede tener un impacto significativo en el rendimiento global.

