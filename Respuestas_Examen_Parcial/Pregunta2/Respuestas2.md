### Respuesta 2

El programa en Rust parte de la construcción de un árbol de sufijos compactado; para ello convierte, en tiempo lineal, el suffix-array y su vector LCP en la estructura arbórea. 
Sobre ese árbol implementa la función `find_longest_k_frequent_substring(root, text, k)`, que devuelve el substring más largo que aparece al menos k veces y 
la lista de todas sus posiciones iniciales en el texto.

La corrección se justifica así. Cada nodo interno representa el conjunto de sufijos que comparten el prefijo formado por la concatenación de las etiquetas de la ruta desde la raíz. 

El número de hojas de su subárbol coincide, por definición, con la frecuencia de ese prefijo en el texto. Durante un recorrido en profundidad primero se mantiene la profundidad actual de la cadena y se conserva, como candidato, el nodo más profundo cuyo subárbol contiene al menos k hojas. 
Si existe algún substring con frecuencia ≥ k, dicho substring induce un nodo (o una arista) con esa misma propiedad y el algoritmo lo visitará, elegir siempre 
el candidato más profundo garantiza que la longitud devuelta es la máxima posible. 
Las posiciones se obtienen porque las hojas bajo el nodo ganador corresponden exactamente a los sufijos que comienzan con ese substring, de modo que sus índices son los desplazamientos buscados.

En cuanto al coste, la construcción del suffix-array con la variante sencilla de doble ordenación cuesta O(n log² n), el algoritmo de Kasai suministra el LCP 
en O(n) y la transformación SA -> árbol también es lineal. 

La búsqueda posterior recorre cada nodo y cada arista una sola vez, por lo que requiere O(n) tiempo y O(h) memoria adicional, siendo h la altura del árbol (acotada por n y, en la práctica, por log σ n).

En ese contexto, **σ (sigma)** representa el tamaño del alfabeto del texto T, es decir, la cantidad de símbolos distintos que pueden aparecer en la cadena (por ejemplo, 4 para el ADN {A, C, G, T}, 26 para letras minúsculas en inglés, 256 para todos los valores posibles de un byte, etc.).
Cuando se dice que la altura práctica de un árbol de sufijos es *O(log σ n)* se hace referencia a que, en textos largos con un alfabeto moderadamente grande, 
la profundidad típica de los nodos internos tiende a crecer logarítmicamente con la longitud n del texto y depende inversamente del  tamaño del alfabeto: cuanto mayor es σ, antes se "ramifica" el árbol y menor es su altura promedio.
