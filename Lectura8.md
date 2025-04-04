### Análisis del factor de ramificación

Generalmente, los heaps binarios son suficientes para la mayoría de nuestras necesidades de programación. La principal ventaja de esta estructura de datos es que garantiza un tiempo de ejecución logarítmico para cada una de las operaciones comunes.  
En particular, al ser un árbol binario balanceado, se garantiza que las operaciones principales requieren, en el peor de los casos, un número de comparaciones proporcional a _log₂(N)_.

Como hemos mencionado en clase, los factores constantes son irrelevantes para el análisis del tiempo de ejecución; es decir, `O(c·N) = O(N)`. Y sabemos por álgebra que dos logaritmos con distintas bases solo difieren en un factor constante. En particular:

```math
\log_b(N) = \frac{\log_2(N)}{\log_2(b)}
```

Así, en conclusión, tenemos:

```math
O(\log_2(N)) = O(\log_3(N)) = O(\log(N))
```

Sin embargo, cuando pasamos a la implementación, **los factores constantes importan**. Importan tanto que, en algunos casos extremos, algoritmos que serían mejores según el análisis asintótico resultan más lentos que algoritmos más simples con peor complejidad, al menos para cualquier entrada práctica.

Un ejemplo destacado de este comportamiento lo proporcionan los [*heaps* de Fibonacci](https://en.wikipedia.org/wiki/Fibonacci_heap): en teoría, ofrecen tiempo amortizado constante para algunas operaciones cruciales como la inserción o la actualización de prioridad, pero en la práctica son complicados de implementar y lentos para cualquier tamaño de entrada razonable.

Los factores constantes, en general, se deben a diversas razones, entre ellas:

- La latencia al leer/escribir en memoria (lecturas dispersas vs. localizadas).
- El costo de mantener contadores o iterar bucles.
- El costo de la recursión.
- Los detalles minuciosos del código que el análisis asintótico abstrae (por ejemplo, como hemos visto, arreglos estáticos vs. dinámicos).

Por tanto, a este punto debería quedar claro que en cualquier implementación debemos esforzarnos por mantener estos multiplicadores constantes lo más bajos posible.

Considera de nuevo esta fórmula:

```math
\log_b(N) = \frac{\log_2(N)}{\log_2(b)}
```

Si `b > 2`, es evidente que `log_b(N) < log_2(N)`. Por lo tanto, si tenemos un factor logarítmico en el tiempo de ejecución de nuestro algoritmo, y logramos implementar una versión que, en lugar de requerir _log_2(N)_ pasos, requiera _log_b(N)_, mientras que todos los demás factores se mantienen constantes, entonces habremos conseguido una aceleración adicional en tiempo constante.


### Tiempo de ejecución

Entonces, la respuesta es sí: **existe una ventaja en ajustar el factor de ramificación del heap**, pero el compromiso es la clave.

- **Inserción:** Siempre será más rápida con factores de ramificación mayores, ya que como máximo necesitamos hacer ascender (burbujeando el nuevo elemento hasta la raíz) con `O(log_D(n))` comparaciones e intercambios.
- **Eliminación y actualización de prioridades:** En estos casos, el factor de ramificación afecta el rendimiento. Para cada nodo, primero debemos encontrar el de mayor prioridad entre todos sus hijos y luego compararlo con el elemento que estamos empujando hacia abajo.

Cuanto mayor es el factor de ramificación, menor es la altura del árbol (se reduce logarítmicamente). Pero, por otro lado, el número de hijos a comparar en cada nivel también crece linealmente con el factor de ramificación. Como puedes imaginar, un factor de ramificación de 1000 no funcionaría muy bien (¡y se traduciría en una búsqueda casi lineal incluso con menos de 1001 elementos!).

En la práctica, a través de perfiles y pruebas de rendimiento, se ha concluido que, en la mayoría de los casos, `D = 4` es el mejor compromiso.


### Encontrando el factor de ramificación óptimo

Si buscas un valor óptimo de `D` que funcione en **todas** las situaciones, te decepcionarás. Hasta cierto punto, la teoría viene al rescate mostrándonos un rango razonable de valores óptimos. Se puede demostrar que el valor óptimo no puede ser mayor que 5. Dicho de otra forma, se puede probar matemáticamente que:

- El equilibrio entre inserción y eliminación es mejor con `2 ≤ D ≤ 5`.
- Un heap de 3 vías es, en teoría, más rápido que uno de 2 vías.
- Los heaps de 3 y 4 vías tienen un rendimiento similar.
- Los heaps de 5 vías son ligeramente más lentos.

En la práctica, el mejor valor para `D` depende de los detalles de la implementación y de los datos que vas a almacenar en el heap. El factor de ramificación óptimo solo puede determinarse **empíricamente, caso por caso**.  
No existe un valor universalmente óptimo: depende de los datos reales, de la proporción entre inserciones y eliminaciones, o de lo costoso que sea calcular la prioridad frente a copiar elementos, entre otras cosas.

Según la experiencia común:

- Los heaps binarios **nunca son los más rápidos**.
- Los heaps de 5 vías **rara vez** lo son (aunque útiles en dominios muy pequeños).
- La mejor elección suele situarse entre 3 y 4, dependiendo de las sutilezas.

Así que, aunque se sugiere comenzar con un factor de ramificación de 4, si esta estructura de datos se utiliza en una sección crítica de tu aplicación y una pequeña mejora en el rendimiento puede marcar una diferencia relevante, entonces será necesario ajustar el factor de ramificación como parámetro.


### Factor de ramificación y la memoria

Se sugiere el mayor de los dos valores con mejor rendimiento por una razón adicional: **la localidad de referencia**.

Cuando el tamaño del heap excede la caché o la memoria disponible, o en cualquier situación donde intervienen varios niveles de almacenamiento, en promedio un heap binario requiere más fallos de caché o de página que un heap _d_-ario.  
Intuitivamente, esto se debe a que los hijos se almacenan en grupos, y al actualizar o eliminar, se deben examinar todos los hijos de cada nodo alcanzado. Cuanto mayor es el factor de ramificación, más "ancho y bajo" se vuelve el heap, y **mayor es el beneficio en términos de localidad**.

El heap _d_-ario parece ser la mejor estructura de datos tradicional para reducir los fallos de página. Se han propuesto otras alternativas enfocadas en mejorar la localidad de referencia, como los [_splay trees_](https://en.wikipedia.org/wiki/Splay_tree).

Aunque estas alternativas no siempre logran el mismo equilibrio entre rendimiento práctico y teórico que los heaps, cuando el costo de los fallos de página o del acceso a disco domina, podría ser mejor optar por un algoritmo linealítmico (`O(n log n)`, para entrada de tamaño _n_) con mejor localidad que por uno lineal con pobre localidad.
