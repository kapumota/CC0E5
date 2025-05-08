### **Arreglo de sufijos**

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
| Naive          | O(n² log n)             | --                 | Inviable incluso para `n` ≈ 10⁵        |
| Prefix-doubling | O(n log n)              | O(n)                | Constantes moderadas, giras de memoria |
| SA-IS           | O(n) (ó n log k)        | O(n)                | Línea base en alfabetos pequeños       |
| DivSufSort      | O(n log n) (muy optim.) | O(n)                | Rápido en la práctica, caché‐friendly  |

En la práctica, SA-IS domina cuando necesitamos garantías de tiempo lineal y alfabetos restringidos (por ejemplo, genomas con 4-20 caracteres), mientras que DivSufSort es el estándar de facto en herramientas de procesamiento de texto y compresión por su excelente rendimiento empírico incluso en alfabetos amplios y secuencias masivas.

#### Tipos S y L en la construcción de arreglos de sufijos

Para organizar los sufijos de forma eficiente en **SA-IS**, cada posición de la cadena `T` se etiqueta como **S-Type** o **L-Type**, aprovechando la relación lexicográfica entre sufijos adyacentes. A partir de esta clasificación, se detectan los sufijos más críticos (los **LMS**) y se induce el orden de los demás sin compararlos todos entre sí.

#### 1. Definición de tipos

* **S-Type**
  Una posición `i` es S-Type si el sufijo que comienza en `i` es **menor** que el de `i+1`, es decir,

  ```text
  T[i..] < T[i+1..]  
  ```

  O bien, si `T[i] == T[i+1]` y `i+1` ya ha sido marcado como S-Type.

* **L-Type**
  Una posición `i` es L-Type si el sufijo en `i` es **mayor** que el de `i+1`, o si los caracteres coinciden y `i+1` es L-Type:

  ```text
  T[i..] > T[i+1..]  
  ```

Por convención, el último carácter (la sentinela `$`) se considera S-Type.

#### 2. Detección de sufijos LMS

Dentro de estos dos grupos aparece un subconjunto fundamental:

> **LMS (Left-most S-Type)**:
> Son las posiciones `i` que **son S-Type** y además **`i−1` es L-Type**.

Estos sufijos LMS marcan el "punto de inflexión" entre regiones L y S, y sirven como pivotes para ordenar el resto:

1. **Recopilar todos los sufijos LMS** en el orden que aparecen en `T`.
2. **Ordenar sólo esos sufijos** (mediante un string reducido y posible recursión).
3. **Inducir** luego la posición de los sufijos L (en un barrido ascendente) y de los sufijos S (en uno descendente), rellenando cada bucket de caracteres de forma estable.

#### 3. Ejemplo de clasificación

Para ilustrar, tomemos

```text
T = "banana$"
```

y construyamos un vector `type[0..6]`:

|  i  | T\[i] | Comparación con T\[i+1] | type\[i] | Notas               |
| :-: | :---: | :---------------------: | :------: | :------------------ |
|  6  |   \$  |            —            |  S-Type  | sentinela siempre S |
|  5  |   a   |    "a\$" < "\$" ? No    |  L-Type  | "a\$" > "\$"        |
|  4  |   n   |      "na\$" > "a\$"     |  L-Type  |                     |
|  3  |   a   |     "ana\$" < "na\$"    |  S-Type  |                     |
|  2  |   n   |    "nana\$" > "ana\$"   |  L-Type  |                     |
|  1  |   a   |    "ana\$" < "nana\$"   |  S-Type  |                     |
|  0  |   b   |  "banana\$" > "anana\$" |  L-Type  |                     |

De aquí surgen los sufijos **LMS** en las posiciones `1` y `3`, ya que son S-Type y su anterior (`0` y `2`, respectivamente) son L-Type.

#### 4. Ventajas de la clasificación

* **Reducción de comparaciones**: al ordenar primero los sufijos LMS (mucho menos numerosos) y luego "extender" ese orden, evitamos comparar sufijos completos entre sí.
* **Inducción estable**: los barridos ascendente (L) y descendente (S) rellenan cada bucket respetando el orden parcial ya establecido, garantizando estabilidad y cohesión lexicográfica.
* **Complejidad lineal**: gracias a que cada posición se etiqueta y se induce exactamente una vez, SA-IS alcanza **O(n)** (o **O(n log k)** en alfabetos generales), superando en muchos casos la construcción naive.

Con esta organización, SA-IS convierte la superposición natural de sufijos en una ventaja algorítmica, logrando construir el **Suffix Array** sin ordenar todos los sufijos de forma explícita.

#### Algoritmo SA-IS

**SA-IS** (Suffix Array Induced Sorting), ideado por Nong, Zhang y Chan, construye el arreglo de sufijos en tiempo **O(n)** (o **O(n·log k)** si el alfabeto tiene k símbolos) sin comparar sufijos de forma directa. Su esquema se basa en clasificar posiciones y aprovechar recursión sobre un "string reducido":

1. **Etiquetado de tipos**

   * Recorremos la cadena `T` de derecha a izquierda, asignando a cada índice `i` un **tipo** (S o L) según la relación lexicográfica entre `T[i..]` y `T[i+1..]`.
   * Simultáneamente, detectamos las posiciones **LMS** (S-Type cuyo anterior es L-Type), que actuarán como puntos de anclaje.

2. **Construcción del string reducido**

   * Tomamos cada bloque LMS (subcadena que va de un LMS hasta antes del siguiente LMS) y lo asignamos a un **símbolo único** en una nueva cadena `T'`.
   * Si el número de bloques LMS distintos coincide con la cantidad de símbolos en `T'`, su orden lexicográfico queda resuelto directamente.
   * En caso contrario, aplicamos **recursivamente** SA-IS sobre `T'`, reduciendo el problema a tamaño ≤ n/2.

3. **Inducción de sufijos L (barrido ascendente)**

   * Con la ordenación de bloques LMS ya conocida, colocamos en cada **bucket** de caracteres los sufijos `L` que preceden a cada LMS, recorriendo `SA` de izquierda a derecha.
   * Cada inserción respeta el orden parcial heredado, llenando de forma estable los espacios libres en los buckets.

4. **Inducción de sufijos S (barrido descendente)**

   * Finalmente, recorremos `SA` de derecha a izquierda para insertar los sufijos `S` que siguen a cada LMS, usando el mismo criterio de buckets y manteniendo estabilidad.
   * De este modo, todos los sufijos S-Type se sitúan en su posición correcta sin necesidad de compararlos.


#### Claves del rendimiento lineal

* **Reducción del problema**: al recursar sobre una versión acotada de `T` (el string reducido), la parte más costosa opera sobre un tamaño como máximo n/2.
* **Buckets precomputados**: mantenemos para cada carácter su rango inicial y final en `SA`, lo que permite inserciones por simple incremento/decremento de índices.
* **Sin comparaciones carácter a carácter**: todas las decisiones de posición se basan en tipos y en la recursión, no en comparar sufijos completos.
* **Operaciones locales**: cada sufijo se "visita" y se coloca una sola vez en cada fase (tipado, ordenación LMS, inducción `L` y `S`), garantizando que el trabajo total sea proporcional a **n**.

Gracias a esta combinación de clasificación, reducción recursiva e inducción estable, SA-IS ofrece una construcción de suffix array que aúna simplicidad conceptual y eficiencia práctica, convirtiéndose en la referencia para alfabetos de tamaño moderado o constante.


#### Algoritmo DivSufSort

**DivSufSort**, desarrollado por Yuta Mori, es uno de los métodos más rápidos y usados en la práctica para construir suffix arrays en texto de gran tamaño. Su diseño equilibra la rapidez teórica con un uso muy eficiente de la memoria caché y pocos pasos recursivos. A continuación, presentamos una versión refinada de su flujo de trabajo:

1. **Conteo y delimitación de buckets**

   * Recorremos `T` una vez para **contar** la frecuencia de cada carácter.
   * Con esos conteos, establecemos los **límites** izquierdo y derecho de cada bucket en el arreglo `SA`, de modo que los sufijos que empiecen con el mismo símbolo se ubiquen en un mismo rango contiguo.

2. **Clasificación inicial de sufijos "B\*"**

   * Se identifican los sufijos de tipo **B\*** (análogos a los LMS en SA-IS): son sufijos que marcan una transición de un carácter grande a uno más pequeño.
   * Sin recursión, colocamos estos sufijos B\* al final de sus buckets correspondientes (usando el límite derecho decreciente), obteniendo un orden parcial estable.

3. **Ordenación recursiva de bloques B\***

   * Cada sufijo B\* marca el inicio de un **bloque** de sufijos equivalentes en términos de prefijo.
   * Asignamos un **identificador único** a cada bloque distinto, construyendo un "string reducido" de longitud igual al número de bloques B\*.
   * Si el número de bloques coincide con la cantidad de identificadores, el orden está resuelto; si no, aplicamos DivSufSort recursivamente sobre este string reducido, permitiendo resolver la ordenación de B\* en un tamaño ≤ n/2.

4. **Inducción de sufijos de tipo B (descendente)**

   * Con los B\* ya ordenados, recorremos `SA` de derecha a izquierda.
   * Insertamos en cada bucket los sufijos de tipo **B** (aquellos que sigan a un sufijo B\*) justo antes de sus correspondientes límites derechos, manteniendo el orden inducido por los bloques B\*.

5. **Inducción de sufijos de tipo A (ascendente)**

   * Finalmente, recorremos `SA` de izquierda a derecha para colocar los sufijos de tipo **A** (los que preceden a los B\*), insertándolos justo al inicio de cada bucket (límite izquierdo creciente).
   * Este doble barrido (descendente y ascendente) completa el orden lexicográfico de todos los sufijos.

#### Puntos clave de optimización

* **Uso de memoria caché**:
  Los tablets de buckets y las inserciones contiguas maximizan la localidad espacial, reduciendo fallos de caché incluso en textos de cientos de megabytes.
* **Poca recursión**:
  La recursión sólo actúa sobre el string reducido de sufijos B\*, cuya longitud es una fracción de `n`, con profundidad rara vez superior a **O(log n)**.
* **Evita comparaciones directas**:
  Al igual que SA-IS, DivSufSort induce el orden sin comparar sufijos carácter a carácter, basándose en los identificadores de bloque y en operaciones de asignación de índices.

Aunque su complejidad teórica es **O(n log n)** en el peor caso, las heurísticas de Mori (división equilibrada de subrangos, manejos de histogramas rápidos y barridos eficientes) permiten que DivSufSort supere o iguale en velocidad a algoritmos lineales como SA-IS en la mayoría de aplicaciones reales. Por ello, es la implementación de referencia en bibliotecas de compresión, bioinformática y sistemas de búsqueda de texto.
#### Ejemplo detallado de DivSufSort

A continuación mostraremos paso a paso cómo **DivSufSort** construye el suffix array de la cadena

```text
T = "banana$"
```

donde `$` es la sentinela más pequeña.

#### 1. Conteo de caracteres y delimitación de buckets

Primero contamos la frecuencia de cada símbolo:

| Carácter | `$` | `a` | `b` | `n` |
| :------: | :-: | :-: | :-: | :-: |
|   Frec.  |  1  |  3  |  1  |  2  |

Con esos conteos definimos los **rangos contiguos** en el array `SA` (de tamaño 7) donde irá cada grupo:

| Carácter | Límite izquierdo | Límite derecho |
| :------: | :--------------: | :------------: |
|    `$`   |         0        |        0       |
|    `a`   |         1        |        3       |
|    `b`   |         4        |        4       |
|    `n`   |         5        |        6       |

Inicialmente `SA = [ _, _, _, _, _, _, _]` (todas las posiciones vacías).

#### 2. Clasificación de sufijos (tipo A / tipo B)

Recorremos `T` de derecha a izquierda para etiquetar cada posición `i`:

* **Tipo B** si

  ```
  T[i] < T[i+1]
  o bien
  (T[i] == T[i+1] y pos i+1 también era B)
  ```
* **Tipo A** en caso contrario.
* El sufijo en la sentinela (`i = 6`) se marca siempre **B**.

|  i  | T\[i] | Comparación con T\[i+1] | Tipo |
| :-: | :---: | :---------------------: | :--: |
|  6  |  `$`  |            --            |   B  |
|  5  |  `a`  |         `a`> `$`        |   A  |
|  4  |  `n`  |         `n`> `a`        |   A  |
|  3  |  `a`  |         `a`< `n`        |   B  |
|  2  |  `n`  |         `n`> `a`        |   A  |
|  1  |  `a`  |         `a`< `n`        |   B  |
|  0  |  `b`  |         `b`> `a`        |   A  |

De este modo obtenemos el vector de tipos

```
[A, B, A, B, A, A, B]
```


#### 3. Detección de sufijos **B\*** (análogos a LMS)

Los sufijos **B\*** son aquellos que **son B** y están precedidos por un **A**. Aquí:

* Posición 1 (B, su anterior 0 es A)
* Posición 3 (B, su anterior 2 es A)
* Posición 6 (B, su anterior 5 es A)

En total:

```
B* = { 1, 3, 6 }
```

#### 4. Construcción del "string reducido" y ordenación de B\*

Para cada sufijo B\*, tomamos la subcadena entre esa posición y la siguiente B\* (inclusive la posición final en caso de 6):

| B\* i | Subcadena correspondiente |
| :---: | :-----------------------: |
|   1   |      T\[1..2] = "an"      |
|   3   |      T\[3..5] = "ana"     |
|   6   |      T\[6..6] = "\$"      |

Como las tres subcadenas son **distintas**, podemos mapearlas a símbolos únicos sin recursión:

```
"an" -> 0,    "ana" -> 1,    "$" -> 2
```

El **string reducido** queda `T' = [0,1,2]`. Su orden lexicográfico (0<1<2) nos da la secuencia de sufijos B\* **ordenados**:

```
[6, 1, 3]
```

#### 5. Colocación inicial de los sufijos B\* en SA

Insertamos cada sufijo B\* en el **extremo derecho** de su bucket, según su carácter inicial:

1. Sufijo `6 -> "$"`  -> bucket `$` (pos 0)
2. Sufijo `1 -> "anana$"` -> bucket `a` (pos 3)
3. Sufijo `3 -> "ana$"`   -> bucket `a` (pos 2)

Tras esto:

```
SA = [ 6,  _,  3,  1,  _,  _,  _ ]
```

#### 6. Inducción de sufijos de tipo A (barrido ascendente)

Ahora recorremos `SA` de izquierda a derecha. Cada vez que encontramos un sufijo no vacío en la posición `p = SA[i]`, comprobamos si `p>0` y si `suffix(p−1)` es de **tipo A**. Si lo es, lo ubicamos en el **extremo izquierdo** libre de su bucket:

| Iteración | SA\[i] | p−1 | Tipo(p−1) | Bucket de T\[p−1] |        Posición asignada        |
| :-------: | :----: | :-: | :-------: | :---------------: | :-----------------------------: |
|    i=0    |    6   |  5  |     A     |        `a`        |   primer libre en `[1..3]` -> 1  |
|    i=1    |    5   |  4  |     A     |        `n`        |   primer libre en `[5..6]` -> 5  |
|    i=2    |    3   |  2  |     A     |        `n`        | siguiente libre en `[5..6]` -> 6 |
|    i=3    |    1   |  0  |     A     |        `b`        |      único en `[4..4]` -> 4      |

Después de estas cuatro inserciones, ya no quedan sufijos A pendientes; el array está completo:

```
SA = [6, 5, 3, 1, 0, 4, 2]
```

#### 7. Inducción de sufijos de tipo B

En este ejemplo particular **no quedan sufijos B** por inducir (todos los B que no eran B\* ya se ubican correctamente); en cadenas más complejas se haría un barrido descendente idéntico, insertando cada sufijo B en el extremo derecho libre de su bucket.

#### 8. Resultado final

El **suffix array** de `"banana$"` obtenido es

```text
SA = [6, 5, 3, 1, 0, 4, 2]
```

que coincide con el orden lexicográfico de los sufijos:

```
"$", "a$", "ana$", "anana$", "banana$", "na$", "nana$"
```


Con este ejemplo se ilustra cómo DivSufSort:

1. **Cuenta** caracteres y fija buckets.
2. **Clasifica** sufijos en A/B y extrae los pivotes B\*.
3. Construye un **string reducido** para ordenar relativamente pocos sufijos.
4. **Induce** el orden del resto de sufijos con dos barridos sencillos.

El resultado es un algoritmo extremadamente rápido en la práctica, gracias a la mínima recursión y al uso intensivo de accesos contiguos en memoria.

**Observación**

En este contexto, un **bucket** (o cubo) es simplemente una **región contigua** dentro del arreglo `SA` que agrupa todos los sufijos que comparten un mismo criterio, normalmente el **primer carácter** (o el primer par, triplete, etc., en variantes más avanzadas). La idea viene directamente de la técnica de **bucket sort**, donde:

1. **Se cuentan** las apariciones de cada "clave" (aquí, cada carácter o prefijo) en un primer pase.
2. A partir de esos conteos, se establecen **límites** para cada bucket: un bucket va de la posición L (límite izquierdo) a la posición R (límite derecho) en el arreglo `SA`.
3. Cuando "insertamos" un sufijo en su bucket, lo colocamos en la siguiente posición libre dentro de ese rango, ya sea avanzando L hacia la derecha (insertar por la izquierda) o retrocediendo R hacia la izquierda (insertar por la derecha), según la fase del algoritmo.

Por ejemplo, si T = `"banana$"` y nuestro alfabeto ordenado es \[`$`, `a`, `b`, `n`], podríamos tener buckets como:

| Carácter | Frecuencia | Bucket en SA     |
| :------- | :--------- | :--------------- |
| `$`      | 1          | posiciones `0...0` |
| `a`      | 3          | posiciones `1..3` |
| `b`      | 1          | posiciones `4...4` |
| `n`      | 2          | posiciones `5...6` |

* El bucket de `$` abarca solo `SA[0]`.
* El bucket de `a` va de `SA[1]` a `SA[3]`, y así sucesivamente.

Durante la construcción, colocamos cada sufijo en el bucket correspondiente a su carácter inicial (o a la categoría que estemos usando), respetando siempre el orden interno que dictan los pasos de inducción o recursión. Esto evita tener que comparar sufijos completos y mantiene todo el proceso en tiempo lineal (o casi lineal) al limitar las operaciones a **contar** y **colocar en bins**.

