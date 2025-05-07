### **Arreglo de sufijos**

#### Introducción

Dentro de las estructuras de datos dedicadas al procesamiento de cadenas, los suffix trees y los suffix arrays (arreglos de sufijos) ocupan un lugar 
privilegiado gracias a su capacidad para soportar consultas de subcadenas, búsquedas de patrones y cálculo de repetidos en tiempo casi óptimo. No obstante, su atractivo teórico decae si no encontramos maneras eficientes de construidos: un algoritmo que tarde más que la
sencilla ordenación de sufijos dejaría a estas estructuras relegadas al ámbito académico. 

Por fortuna, a lo largo de los últimos veinte años se han desarrollado técnicas que aprovechan la superposición entre sufijos y simulan comportamientos 
similares a un "merge" múltiple para construir arreglos de sufijos de forma casi lineal. 

En esta nota revisaremos, de manera detallada y fluida, cómo se definen y almacenan los arreglos de sufijos, la manera de  complementar esta información con los arreglos LCP, el algoritmo de Kasai para computarlos, el análisis de complejidad subyacente y las 
técnicas avanzadas de construcción basadas en la clasificación de sufijos en tipos S y L, así como los dos métodos más destacados de la literatura: SA-IS y DivSufSort.


#### Arreglos de sufijos

Un arreglo de sufijos para una cadena `T` de longitud `n` (o `n+1` si incluimos explícitamente la sentinela `"$"`) es un vector de enteros `SA` de tamaño `n` (o `n+1`) donde cada entrada `SA[i]` indica la posición de inicio del i-ésimo sufijo más pequeño de `T` en orden lexicográfico. 
Para asegurar que todos los sufijos sean distintos y haya un único mínimo, suele añadirse al final de `T` un carácter especial `"$"` que sea menor que cualquier otro símbolo del alfabeto.

Por ejemplo, con

```
T = "banana$"
```

los sufijos ordenados lexicográficamente son:

1. `"$"`
2. `"a$"`
3. `"ana$"`
4. `"anana$"`
5. `"banana$"`
6. `"na$"`
7. `"nana$"`

En consecuencia, el arreglo de sufijos queda:

```
SA = [6, 5, 3, 1, 0, 4, 2]
```

puesto que esos son los índices de inicio de cada sufijo en `T`.

La principal ventaja de `SA` es que permite convertir consultas de búsqueda de patrones en simples búsquedas binarias sobre este vector, lo que reduce drásticamente el tiempo de consulta. 
Además, al representar la información únicamente como un arreglo de enteros, se evita la sobrecarga de memoria y gestión de punteros característica de los suffix trees.

#### Ejemplos de almacenamiento de arreglos de sufijos

Aunque no presentamos código, conviene ilustrar con un ejemplo cómo se emplea **SA** en la práctica. Supongamos que queremos encontrar todas las ocurrencias de un patrón `P` en una cadena `T`. La estrategia habitual es ésta:

1. **Búsqueda del límite inferior**
   Usamos búsqueda binaria sobre `SA` para hallar el menor índice `i` tal que el sufijo `T[SA[i]...]` sea, en orden lexicográfico, ≥ `P`.
2. **Búsqueda del límite superior**
   De forma similar, hallamos el menor índice `j` tal que `T[SA[j]...]` sea > `P` cuando se considera cualquier extensión de `P` (equivalente a buscar ≥ `P` concatenado con un carácter "infinito").
3. El intervalo `[i, j)` de posiciones en `SA` contiene exactamente todas las posiciones de inicio de sufijos que comienzan con `P`.

**Ejemplo concreto**

```text
T = "abracadabra$"   (longitud 12, con '$' como sentinela)
P = "abra"
```

Los sufijos de `T` en orden lexicográfico, con sus índices de inicio, son:

```text
i   sufijo
––––––––––––––––––––––––––––––––––––
 0  "$"             (SA[0] = 11)
 1  "a$"            (SA[1] = 10)
 2  "abra$"         (SA[2] =  7)
 3  "abracadabra$"  (SA[3] =  0)
 4  "acadabra$"     (SA[4] =  3)
 5  "adabra$"       (SA[5] =  5)
 6  "bra$"          (SA[6] =  8)
 7  "bracadabra$"   (SA[7] =  1)
 8  "cadabra$"      (SA[8] =  4)
 9  "dabra$"        (SA[9] =  6)
10  "ra$"           (SA[10] = 9)
11  "racadabra$"    (SA[11] = 2)
```

Por tanto,

```text
SA = [11, 10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2]
```

* Para `P = "abra"`, la búsqueda binaria de ≥ `"abra"` devuelve `i = 2` (sufijo `"abra$"` en SA\[2]).
* La búsqueda de > `"abra"` da `j = 4` (el primer sufijo > `"abra..."` es `"acadabra$"` en SA\[4]).
* Entonces, el rango `[2, 4)` = `{2,3}` apunta a SA\[2]=7 y SA\[3]=0, que son precisamente las dos ocurrencias de `"abra"` en `T`.


Un segundo uso frecuente es hallar la **subcadena repetida más larga** en `T`. Si hemos construido también el **arreglo LCP**, basta con localizar su valor máximo `LCP[k]` y traducir `T[SA[k]...SA[k]+LCP[k]-1]` de vuelta a la cadena original. De este modo, con `SA`+`LCP` podemos resolver muy eficientemente problemas de compresión, genómica o detección de fragmentos duplicados en código.

#### Arreglos LCP (Longitud de Prefijo Común)

El **arreglo LCP** de una cadena `T` de longitud `n` es un vector `LCP[0..n-1]` que acompaña al arreglo de sufijos `SA`. Su función es registrar, para cada par de sufijos adyacentes en `SA`, cuántos caracteres comparten desde el inicio antes de diferir:

1. **Definición**

   * `LCP[0] = 0` por convención (no hay sufijo anterior).
   * Para `i > 0`,

     ```
     LCP[i] = ℓ, donde ℓ = la mayor longitud tal que
       T[SA[i] ... SA[i]+ℓ-1] = T[SA[i-1] ... SA[i-1]+ℓ-1].
     ```

2. **Ejemplo con "banana\$"**

   * Cadena:

     ```
     T = "banana$"
     SA = [6, 5, 3, 1, 0, 4, 2]
     ```
   * Sufijos en orden lexicográfico y sus prefijos comunes:

     |  i  | SA\[i] | sufijo    | LCP\[i] | comentario                      |
     | :-: | :----: | :-------- | :-----: | :------------------------------ |
     |  0  |    6   | `$`       |    0    | no hay sufijo previo            |
     |  1  |    5   | `a$`      |    0    | `$` vs `a$` -> no comparten nada |
     |  2  |    3   | `ana$`    |    1    | `a`                             |
     |  3  |    1   | `anana$`  |    3    | `ana`                           |
     |  4  |    0   | `banana$` |    0    | no comparten (empieza con `b`)  |
     |  5  |    4   | `na$`     |    0    | `b` vs `n`                      |
     |  6  |    2   | `nana$`   |    2    | `na`                            |

   El vector resultante es

   ```
   LCP = [0, 0, 1, 3, 0, 0, 2]
   ```

3. **Ventajas y aplicaciones**

   * **Búsqueda de la subcadena repetida más larga**
     Basta con localizar el máximo valor en `LCP`; por ejemplo, `max(LCP)=3` en la posición `i=3` indica que el sufijo en `SA[3]` y el anterior (`SA[2]`) comparten "ana" como subcadena más larga repetida.
   * **Salto de comparaciones**
     Al recorrer `SA` y `LCP` en un solo pase, podemos evitar volver a comparar caracteres que ya hemos comprobado en pares anteriores. Si conocemos `LCP[i]=ℓ`, al comparar el par `(i, i+1)` sabemos que su prefijo común será al menos

     ```
     min( LCP[i], LCP[i+1] )
     ```

     Esto permite algoritmos de barrido en tiempo **O(n)** amortizado, esenciales en minería de secuencias y análisis de repeticiones en datos biológicos o de texto.
   * **Optimización en búsqueda de patrones**
     Cuando hacemos búsquedas sobre `SA`, el conocimiento de `LCP` entre sufijos cercanos ayuda a limitar el número de comparaciones carácter a carácter al ajustar los límites de la búsqueda binaria.

Con `SA` y `LCP` construidos, disponemos de un esquema compacto y altamente eficiente para resolver numerosas operaciones sobre cadenas en tiempo cercano al lineal, manteniendo una sobrecarga de memoria muy reducida.

#### Algoritmo de Kasai

Kasai et al. diseñaron un procedimiento sencillo y eficiente para construir el arreglo **LCP** en **O(n)**, usando únicamente el **arreglo de sufijos** `SA` y la cadena original `T`. A continuación se presenta una descripción paso a paso y un ejemplo ilustrativo.

#### 1. Preparación: el arreglo de rangos (`rank`)

Antes de nada, construimos un arreglo auxiliar `rank[0..n-1]` tal que:

```
rank[ SA[i] ] = i    para todo i ∈ [0..n-1].
```

Es decir, `rank[pos]` nos indica la posición en `SA` donde aparece el sufijo que comienza en `T[pos]`.

#### 2. Bucle principal

1. Inicializar un contador `h = 0`.
2. Recorrer `i` desde `0` hasta `n-1` (es decir, en **orden natural** de sufijos):

   1. Sea `k = rank[i]`.
   2. Si `k == 0`, no hay sufijo anterior en `SA`, así que fijamos `LCP[0] = 0` y seguimos con `i+1`.
   3. En caso contrario, definimos `j = SA[k-1]` (la posición de inicio del sufijo lexicográficamente anterior).
   4. **Extender el prefijo común**:

      ```pseudo
      while i + h < n  AND  j + h < n  AND  T[i+h] == T[j+h]:
          h <- h + 1
      ```
   5. Asignar `LCP[k] = h`.
   6. Si `h > 0`, decrementar `h <- h - 1` (esto amortiza las comparaciones).
3. Al terminar, `LCP` estará completamente llenado.

#### 3. Clave de la amortización

* Cada vez que comparamos caracteres para incrementar `h`, ese coste "se hereda" al siguiente sufijo, y al restar 1 al pasar de `i` a `i+1`, garantizamos que cada carácter de `T` se compare **a lo sumo dos veces**.
* Esto convierte todo el proceso en **O(n)** en el peor caso, sin estructuras auxiliares complejas.

#### 4. Ejemplo paso a paso

Tomemos

```
T = "banana$"   (n = 7)
SA = [6, 5, 3, 1, 0, 4, 2]
```

1. Construimos `rank`:

   ```
   pos:     0 1 2 3 4 5 6
   SA idx:  4 3 6 2 5 1 0   <- SA inverso
   rank:    [4,3,6,2,5,1,0]
   ```

2. Iteramos `i` de 0 a 6, con `h` comenzando en 0:

   |  i  | k=rank\[i] | j=SA\[k-1] | Extensión de `h`                                                     | LCP\[k]=h | h tras decremento |
   | :-: | :----------: | :----------: | :------------------------------------------------------------------- | :---------: | :---------------: |
   |  0  |       4      |   SA\[3]=1   | Compara `T[0]`≠`T[1]` -> h=0                                          |      0      |         0         |
   |  1  |       3      |   SA\[2]=3   | Compara `T[1]`=`a`, `T[3]`=`a` -> h=1; siguiente `T[2]`≠`T[4]` -> stop |      1      |         0         |
   |  2  |       6      |   SA\[5]=4   | Compara `T[2]`≠`T[4]` -> h=0                                          |      0      |         0         |
   |  3  |       2      |   SA\[1]=5   | Compara `T[3]`≠`T[5]` -> h=0                                          |      0      |         0         |
   |  4  |       5      |   SA\[4]=0   | Compara `T[4]`≠`T[0]` -> h=0                                          |      0      |         0         |
   |  5  |       1      |   SA\[0]=6   | Compara `T[5]`≠`T[6]` -> h=0                                          |      0      |         0         |
   |  6  |       0      |       --     | Caso `k=0` -> LCP\[0]=0                                               |      0      |         --       |

3. El `LCP` final queda:

   ```
   LCP = [0, 0, 0, 1, 0, 0, 0]
   ```

   que coincide con las comparaciones esperadas para "banana\$".

#### Análisis de rendimiento

La **construcción ingenua** de un arreglo de sufijos genera explícitamente los `n` sufijos de la cadena y los ordena con un algoritmo de comparación genérico (por ejemplo, mergesort o quicksort). Cada comparación de dos sufijos puede costar hasta **O(n)** en el peor caso, por lo que el coste global asciende a **O(n.log n.n)**. Incluso si empleamos comparaciones aceleradas con hashing o LCP parciales, difícilmente bajamos de **O(n log² n)** en alfabetos grandes.

Por fortuna, al reconocer que los sufijos se superponen y comparten prefijos, podemos diseñar estrategias mucho más eficientes:

1. **Prefix-doubling**

   * En cada fase doblamos la longitud de prefijo considerado y ordenamos por pares de claves de tamaño creciente.
   * Obtiene **O(n log n)** comparaciones de claves, cada una en **O(1)** con radix sort o conteo.
   * Es simple y muy usado en implementaciones educativas, pero en la práctica sufre por constantes elevadas cuando `n` es grande.

2. **Induced Sort / SA-IS**

   * Clasifica los sufijos en tipos **S** y **L**, ordena primero los sufijos LMS y luego "induce" el orden del resto.
   * Con cuidado en la gestión de buckets y sin recursión profunda, alcanza **O(n)** estricto en alfabetos de tamaño constante, o **O(n log k)** si el alfabeto tiene `k` símbolos y usamos radix sort para los buckets.

3. **DivSufSort**

   * Combina histogramas de caracteres, ordenación por buckets y recursión sobre subrangos de sufijos, junto con inducción similar a SA-IS.
   * Su complejidad teórica es **O(n log n)** en el peor caso, pero gracias a optimizaciones de caché y a la división equilibrada de subproblemas, suele superar en velocidad a SA-IS sobre textos reales (desde decenas de megabytes hasta varios gigabytes).

4. **Cálculo de LCP (Kasai)**

   * Independientemente del método empleado para `SA`, Kasai garantiza **O(n)** adicionales para construir `LCP` usando sólo un vector inverso de rangos y un contador amortizado.


**Resumen de complejidades**

| Algoritmo       | Construcción de SA      | Construcción de LCP | Notas prácticas                        |
| --------------- | ----------------------- | ------------------- | -------------------------------------- |
| Naïvo           | O(n² log n)             | --                 | Inviable incluso para `n` ≈ 10⁵        |
| Prefix-doubling | O(n log n)              | O(n)                | Constantes moderadas, giras de memoria |
| SA-IS           | O(n) (ó n log k)        | O(n)                | Línea base en alfabetos pequeños       |
| DivSufSort      | O(n log n) (muy optim.) | O(n)                | Rápido en la práctica, caché‐friendly  |

En la práctica, SA-IS domina cuando necesitamos garantías de tiempo lineal y alfabetos restringidos (por ejemplo, genomas con 4-20 caracteres), mientras que DivSufSort es el estándar de facto en herramientas de procesamiento de texto y compresión por su excelente rendimiento empírico incluso en alfabetos amplios y secuencias masivas.


