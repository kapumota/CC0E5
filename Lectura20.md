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
   De forma similar, hallamos el menor índice `j` tal que `T[SA[j]...]` sea > `P` cuando se considera cualquier extensión de `P` (equivalente a buscar ≥ `P` concatenado con un carácter “infinito”).
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


Un segundo uso frecuente es hallar la **subcadena repetida más larga** en `T`. Si hemos construido también el **arreglo LCP**, basta con localizar su valor máximo `LCP[k]` y traducir `T[SA[k]...SA[k]+LCP[k]−1]` de vuelta a la cadena original. De este modo, con `SA`+`LCP` podemos resolver muy eficientemente problemas de compresión, genómica o detección de fragmentos duplicados en código.

#### Arreglos LCP (Longitud de Prefijo Común)

El **arreglo LCP** de una cadena `T` de longitud `n` es un vector `LCP[0..n−1]` que acompaña al arreglo de sufijos `SA`. Su función es registrar, para cada par de sufijos adyacentes en `SA`, cuántos caracteres comparten desde el inicio antes de diferir:

1. **Definición**

   * `LCP[0] = 0` por convención (no hay sufijo anterior).
   * Para `i > 0`,

     ```
     LCP[i] = ℓ, donde ℓ = la mayor longitud tal que
       T[SA[i] ... SA[i]+ℓ−1] = T[SA[i−1] ... SA[i−1]+ℓ−1].
     ```

2. **Ejemplo con “banana\$”**

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
     Basta con localizar el máximo valor en `LCP`; por ejemplo, `max(LCP)=3` en la posición `i=3` indica que el sufijo en `SA[3]` y el anterior (`SA[2]`) comparten “ana” como subcadena más larga repetida.
   * **Salto de comparaciones**
     Al recorrer `SA` y `LCP` en un solo pase, podemos evitar volver a comparar caracteres que ya hemos comprobado en pares anteriores. Si conocemos `LCP[i]=ℓ`, al comparar el par `(i, i+1)` sabemos que su prefijo común será al menos

     ```
     min( LCP[i], LCP[i+1] )
     ```

     Esto permite algoritmos de barrido en tiempo **O(n)** amortizado, esenciales en minería de secuencias y análisis de repeticiones en datos biológicos o de texto.
   * **Optimización en búsqueda de patrones**
     Cuando hacemos búsquedas sobre `SA`, el conocimiento de `LCP` entre sufijos cercanos ayuda a limitar el número de comparaciones carácter a carácter al ajustar los límites de la búsqueda binaria.

Con `SA` y `LCP` construidos, disponemos de un esquema compacto y altamente eficiente para resolver numerosas operaciones sobre cadenas en tiempo cercano al lineal, manteniendo una sobrecarga de memoria muy reducida.
