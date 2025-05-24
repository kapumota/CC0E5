### Respuesta 1

* **Heap de mínimas prioridades**: la raíz siempre tiene la **menor** `priority`.
  (Elegir min-heap simplifica la comparación porque "prioridad baja = más arriba". Cambiar a max-heap solo invierte los signos en las rotaciones).
* Cada nodo mantiene:

  * `key` (clave BST),
  * `value` (dato de usuario),
  * `priority` (aleatoria o dada),
  * `left`, `right`,
  * `subtree_max` -> `max(value, left.subtree_max, right.subtree_max)`.
* **Rotaciones**: `rotate_left`, `rotate_right` actualizan `subtree_max` tras intercambiar enlaces.

**Operaciones soportadas**

| Operación                 | Descripción                                                                              | Complejidad esperada                             | Peor caso |
| ------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------ | --------- |
| `insert`                  | Inserción BST seguida de *burbujas* con rotaciones mientras el heap lo exija             | **O(log N)**                                     | **O(N)**  |
| `delete`                  | Búsqueda BST, luego rotar hijos hacia arriba hasta convertir el nodo en hoja y liberarlo | **O(log N)**                                     | **O(N)**  |
| `find_max_value_in_range` | Consulta óptima usando `subtree_max`                                                     | **O(log N + R)** (R = nodos realmente visitados) | **O(N)**  |


#### Análisis teórico

**Altura esperada O(log N)**

Sea `u_i` la prioridad i.i.d. continua de cada clave.
*Un nodo j es ancestro de otro i* si y solo si `u_j` es el mínimo entre las prioridades de las claves en el intervalo `[min(i,j), max(i,j)]`.
La probabilidad de ese mínimo es `1/|i-j|+1`.
Sumando probabilidades de ser ancestro sobre todos los pares se obtiene altura esperada

$$
\mathbb{E}[H_N] = \sum_{k=0}^{N-1} \frac{1}{k+1} = H_N = O(\log N).
$$

**Complejidad**

* **Esperada**: caminamos un único camino de raíz a hoja -> `O(log N)` inserción/eliminación/búsqueda.
* **Peor caso**: si las prioridades llegan ordenadas (monótonas), el Treap se degrada en lista enlazada -> `O(N)`.

**Consulta `find_max_value_in_range`**

* Al aprovechar `subtree_max` podas subárboles completos:

  * Si `node.key < key_min` -> todo su subárbol izquierdo queda fuera.
  * Si `node.key ∈ [key_min, key_max]` y `node.right.key ≤ key_max`, puedes usar `node.right.subtree_max` sin descender.
* **Esperada**: `O(log N + α)` con `α` nodos cuyos rangos se solapan estrictamente; para rangos pequeños suele ser `O(log N)`.
* **Ingenuo**: recolectar en-rango (`O(log N + k)`) + máximo (`O(k)`) => `O(log N + k)` visitas. Cuando `k` = Θ(N) la diferencia es 2×, pero para rangos amplios ahorramos una recursión completa por cada rama podada.

**Mantenimiento de `subtree_max`**

1. **Después de rotar**: rotación solo re-coloca un padre con su hijo, por lo que basta con llamar `_update`/`update` primero al nodo movido hacia abajo y luego al nuevo padre.
2. **Después de insertar o borrar**: al retornar por la recursión se llama `update` en cada ancestro visitado, propagando el valor correcto.

