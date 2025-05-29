### k-d trees para indexación multidimensional

#### Introducción

En sistemas de gran escala, como aplicaciones de comercio electrónico que sirven a millones de clientes diarios, resulta crítico poder responder en tiempo real a consultas espaciales, por ejemplo:

> "¿Cuál es el almacén más cercano que tiene disponible un producto para un cliente ubicado en una posición cualquiera del mapa?"

Un k-d tree (árbol k-dimensional) es una estructura de datos que permite particionar recursivamente un espacio k-dimensional mediante divisiones
binarias alternas, ofreciendo búsquedas de vecinos cercanos con complejidad logarítmica esperada en lugar de recorrer linealmente  todos los puntos *O(n)*.

#### Contexto y motivación

Partimos de un caso de ejemplo en 2-D con puntos que representan ciudades y almacenes:

```python
# Datos conceptuales para ciudades y almacenes
# Cada punto es un diccionario con nombre y coordenadas (x, y)

ciudades_ejemplo = [
    {"nombre": "CiudadA", "x": 10, "y": 50},
    {"nombre": "CiudadB", "x": 30, "y": 60},
    {"nombre": "CiudadImaginariaC", "x": 25, "y": 20}
]

almacenes_ejemplo = [
    {"nombre": "Almacen1", "x": 15, "y": 45},
    {"nombre": "Almacen2", "x": 35, "y": 55},
    {"nombre": "AlmacenImaginario3", "x": 20, "y": 15}
]

print("Ciudades de ejemplo:", ciudades_ejemplo)
print("Almacenes de ejemplo:", almacenes_ejemplo)
```

En un entorno productivo, sin embargo, no trabajamos con unas pocas docenas de puntos, sino con millones de clientes y miles de almacenes. Una búsqueda de fuerza bruta, que compara la distancia a cada almacén, es inviable por su coste computacional lineal.

#### Desafíos de la búsqueda multidimensional

La búsqueda de vecinos cercanos en espacios de alta dimensión presenta varios retos que van más allá de los algoritmos y estructuras de datos unidimensionales. A continuación profundizamos en cada uno de ellos:

1. **Fuerza bruta ineficiente**
   La aproximación más directa consiste en calcular la distancia del punto de consulta a cada uno de los $n$ puntos almacenados y elegir el mínimo. Aunque es conceptualmente sencilla, implica un coste de $\mathcal{O}(n)$ en tiempo por consulta: si atendemos a millones de clientes y miles de almacenes, cada consulta requeriría iterar sobre todos los almacenes, lo cual puede traducirse en decenas o centenas de milisegundos por petición. En sistemas de alta demanda, este retardo es inaceptable y escala de forma lineal con el tamaño del conjunto de datos, lo que condena la solución a ser impracticable conforme crece la base de clientes o puntos de referencia.

2. **Limitaciones de estructuras unidimensionales**
   Estructuras como *heaps*, tablas de dispersión (*hash tables*) o árboles binarios de búsqueda (BST) están diseñadas para organizar datos en un espacio de una sola dimensión, ya sea un valor numérico o una clave de orden total. Cuando se enfrentan a puntos en un espacio $k$-dimensional, pierden la capacidad de representar la geometría intrínseca de los datos. Por ejemplo, un *heap* puede devolver el elemento mínimo global, pero no guarda información sobre distancias entre puntos; una tabla hash distribuye elementos según una función de hash que destruye relaciones espaciales; un BST ordena puntos según una proyección unidimensional (por ejemplo, solo la coordenada $x$), ignorando las demás dimensiones y, por tanto, no garantiza eficacia en consultas de "cercanía" en el sentido euclídeo o métricas similares.

3. **Necesidad de partición espacial**
   Para superar estos límites es esencial **dividir el espacio** de forma jerárquica, de modo que, al procesar una consulta, podamos descartar de golpe regiones completas que no contienen vecinos candidatas. La idea clave es organizar los puntos en subregiones disjuntas (por ejemplo, rectángulos en 2D o paralelepípedos en 3D), asociadas a nodos de un árbol. Cuando consultamos un punto $q$, recorremos el árbol comparando únicamente la coordenada pertinente en cada nivel, y seguimos solo la rama que contiene a $q$. Gracias a esta partición:

   * **Podemos podar** subárboles enteros sin explorarlos si la región que representan está demasiado lejos de $q$.
   * El coste de la búsqueda se aproxima a $\mathcal{O}(\log n)$ en escenarios equilibrados, pues la alternancia de ejes reduce la profundidad del árbol.
   * Evitamos calcular distancias a puntos en regiones sepultadas detrás de la frontera de partición, concentrando el trabajo en un número limitado de candidatos próximos.

   Asimismo, la alternancia de ejes (dividir primero según $x$, luego $y$, luego $z$, etc.) garantiza que ninguna dimensión domine el proceso de partición, evitando que las regiones resultantes se extiendan infinitamente en otras direcciones y manteniendo un reparto más homogéneo de puntos por subregión.

En conjunto, estos desafíos justifican la adopción de estructuras como los k-d trees, que combinan la lógica de un BST con comparaciones multidimensionales, permitiendo búsquedas de vecinos cercanos de manera escalable y eficiente.


#### Heurística de Bentley: k-d trees

La solución clásica propuesta por Jon Louis Bentley consiste en:

* **Dividir el espacio en dos** subregiones en cada paso, alternando ejes.
* En 2-D se alterna entre líneas verticales (eje *x*) y horizontales (eje *y*).
* Cada nodo del árbol almacena un punto pivote y un eje de partición `axis = depth % k`.
* El subárbol izquierdo agrupa puntos con coordenada menor al pivote; el derecho agrupa el resto.

Esta construcción recursiva genera un **árbol binario balanceado** que indexa eficientemente los puntos.

A continuación vamos a profundizar en la **Heurística de Bentley** para construir un k-d tree, y luego veremos un **ejemplo manual en 2-D** paso a paso con un pequeño conjunto de puntos.

#### Ejemplo manual en 2-D

Tomemos este conjunto de **7** puntos:

```
A (2,3),  B (5,4),  C (9,6),
D (4,7),  E (8,1),  F (7,2),
G (1,5)
```

| Punto | $x$ | $y$ |
| :---: | :-: | :-: |
|   A   |  2  |  3  |
|   B   |  5  |  4  |
|   C   |  9  |  6  |
|   D   |  4  |  7  |
|   E   |  8  |  1  |
|   F   |  7  |  2  |
|   G   |  1  |  5  |


#### Paso 0: raíz

* **Profundidad** = 0 -> `axis = 0 mod 2 = 0` => **eje *x***.
* Ordenamos por *x*:

  $$G(1),A(2), D(4), B(5), F(7),E(8),C(9)$$
  
* **Pivote** = mediana = cuarto = **B(5,4)**.
* Subárbol izquierdo: puntos con *x* < 5 -> $\{G,A,D\}$.
* Subárbol derecho: puntos con *x* > 5 -> $\{F,E,C\}$.

```
               B(5,4)
              /     \
  {G,A,D}           {F,E,C}
```


#### Paso 1: hijos de B (depth=1)

#### 1.1. Subárbol izquierdo de B

* **Profundidad** = 1 -> `axis = 1 mod 2 = 1` => **eje *y***.
* Conjunto $\{G(1,5), A(2,3), D(4,7)\}$, ordenamos por *y*:

  $$A(2,3), G(1,5), D(4,7)$$
* **Pivote** = G(1,5).
* Izquierda de G: $\{A\}$ (y<5).
* Derecha de G:   $\{D\}$ (y>5).

#### 1.2. Subárbol derecho de B

* **Profundidad** = 1 -> `axis = 1 mod 2 = 1` => **eje *y***.
* Conjunto $\{F(7,2), E(8,1), C(9,6)\}$, ordenamos por *y*:

  $$E(8,1),F(7,2), C(9,6)$$

* **Pivote** = F(7,2).
* Izquierda de F: $\{E\}$ (y<2).
* Derecha de F:   $\{C\}$ (y>2).

```
                     B(5,4)
                    /      \
           G(1,5)             F(7,2)
           /    \             /    \
        {A}    {D}        {E}     {C}
```

#### Paso 2: hojas

Todos los conjuntos $\{A\},\{D\},\{E\},\{C\}$ son de tamaño 1 -> **hojas** del árbol, sin más particiones.


#### Árbol final

```
               B(5,4)       <- depth=0, axis= x
              /     \
        G(1,5)       F(7,2)  <- depth=1, axis= y
        /  \         /   \
 A(2,3)  D(4,7)  E(8,1) C(9,6)  <- hojas (depth=2, axis= x)
```

Y cada nodo **"corta"** el plano:

1. **B** con $x=5$ separa $\{x<5\}$ / $\{x>5\}$.
2. **G** con $y=5$ separa, en $\{x<5\}$, las porciones $\{y<5\}$ / $\{y>5\}$.
3. **F** con $y=2$ separa, en $\{x>5\}$, las porciones $\{y<2\}$ / $\{y>2\}$.

De este modo, **ciclamos** ejes en cada nivel, cada partición es **binaria** y, si elegimos la mediana, el resultado es un **árbol balanceado** con coste medio $O(\log n)$ para búsquedas e inserciones.

#### Ejemplo de partición manual en 2D 

Para ilustrar el proceso de partición, a continuación se muestra un ejemplo manual con ocho puntos etiquetados. El código siguiente implementa los primeros tres pasos de partición:

```python
from dataclasses import dataclass, field
from typing import Any, List, Tuple

# Usaremos una estructura simple para los puntos en esta ilustración específica
# ya que el foco está en el proceso de partición manual descrito.
puntos_fig2_dict = {
    "R": (5, 4), "W": (2, 7), "P": (1, 8), "O": (3, 9),
    "Q": (4, 1), "U": (3, 6), "S": (7, 5), "T": (8, 3)
}
# Convertimos a una lista de tuplas con nombre para facilitar el manejo
lista_puntos_fig2 = [{"nombre": k, "coords": v} for k, v in puntos_fig2_dict.items()]

print("[Partición 1]")
# Primer pivote: R (5, 4), división vertical (eje x, dimensión 0)
pivote1_nombre = "R"
pivote1_coords = puntos_fig2_dict[pivote1_nombre]
dimension_division1 = 0 # x
print(f"[Paso 1] Pivote: {pivote1_nombre}{pivote1_coords}, Dimensión de división: {dimension_division1} (x-axis)")

izquierda_particion1 = []
derecha_particion1 = []

for p_data in lista_puntos_fig2:
    if p_data["nombre"] == pivote1_nombre:
        continue
    if p_data["coords"][dimension_division1] < pivote1_coords[dimension_division1]:
        izquierda_particion1.append(p_data)
    else:
        derecha_particion1.append(p_data)

print(f"  [INFO] Puntos a la izquierda de {pivote1_nombre} (x < {pivote1_coords[0]}): {[p['nombre'] for p in izquierda_particion1]}")
print(f"  [INFO] Puntos a la derecha de {pivote1_nombre} (x >= {pivote1_coords[0]}): {[p['nombre'] for p in derecha_particion1]}")

# Siguiente pivote en la partición izquierda: W (2, 7), división horizontal (eje y, dimensión 1)
# (considerando solo puntos en izquierda_particion1)
puntos_en_izquierda_obj = izquierda_particion1
pivote2_nombre = "W"
pivote2_coords = puntos_fig2_dict[pivote2_nombre] # W tiene coords (2,7)
dimension_division2 = 1 # y
print(f"[Paso 2] Considerando partición izquierda. Pivote: {pivote2_nombre}{pivote2_coords}, Dimensión de división: {dimension_division2} (y-axis)")

inferior_particion2 = []
superior_particion2 = []

for p_data in puntos_en_izquierda_obj:
    if p_data["nombre"] == pivote2_nombre:
        continue
    # Se indican que P, O, U están en una sub-partición (superior izq) y Q en otra (inferior izq).
    # W=(2,7). P=(1,8), O=(3,9), U=(3,6), Q=(4,1).
    # Para que P,O,U estén juntos y Q separado por una línea horizontal a través de W(y=7):
    # P(y=8)>7, O(y=9)>7. Pero U(y=6)<7 y Q(y=1)<7. Esto no agrupa P,O,U.
    # "Divide la partición de tonalidad más clara en dos nuevas particiones:
    # una en el área superior izquierda del plano, que contiene P, O y U, y otra en el
    # área inferior izquierda, con solo Q."
    # Esto implica que la línea de división horizontal (y=constante) asociada a W
    # separa {P,O,U} de {Q}.
    # Si la línea de corte es, por ejemplo, y=5 (hipotético para coincidir con la agrupación textual):
    linea_corte_y_fig2 = 5 # Valor hipotético para ilustrar agrupación textual
    if p_data["coords"][dimension_division2] < linea_corte_y_fig2: # Asumiendo que W está en el lado de P,O,U
         inferior_particion2.append(p_data)
    else: # >= linea_corte_y_fig2
         superior_particion2.append(p_data)

print(f"  [INFO] (Ilustrativo de la agrupación textual con corte y={linea_corte_y_fig2})")
print(f"  [INFO] Sub-Partición 'inferior' respecto a y={linea_corte_y_fig2} (ej. Q): {[p['nombre'] for p in inferior_particion2]}")
print(f"  [INFO] Sub-Partición 'superior' respecto a y={linea_corte_y_fig2} (ej. P,O,U): {[p['nombre'] for p in superior_particion2]}")

# División posterior en el área superior izquierda en el punto P (1,8), línea vertical (eje x)
puntos_en_superior_izquierda = [p for p in superior_particion2 if p["nombre"] in ["P","O","U"]] # Asumiendo P,O,U
pivote3_nombre = "P"
pivote3_coords = puntos_fig2_dict[pivote3_nombre]
dimension_division3 = 0 # x
print(f"[Paso 3] Considerando sub-partición superior izquierda. Pivote: {pivote3_nombre}{pivote3_coords}, Dimensión: {dimension_division3} (x-axis)")
# ... y así sucesivamente.
```

En cada paso alternamos el eje de partición (*x* primero, luego *y*, luego de nuevo *x*). Así se generan recursivamente subregiones delineadas por líneas verticales y horizontales.

####  Definición formal de un k-d tree como BST

Un **k-d tree** puede describirse como un árbol de búsqueda binaria (BST) cuyos nodos contienen puntos k-dimensionales y utilizan un método de comparación que solo considera la coordenada `axis = depth mod k`. Cada nodo:

* Mantiene un punto pivote.
* Divide el espacio en dos subespacios según la coordenada `axis`.
* El subárbol izquierdo agrupa puntos con coordenada < pivote; el derecho, ≥.

Este esquema preserva las ventajas de las particiones binarias de un BST, mientras que el método de comparación cíclico aborda la multidimensionalidad.


#### Construcción de un k-d tree unidimensional (k=1)

En el caso 1-D, el algoritmo se simplifica a un BST balanceado construido por medianas:

```python
from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class Node1D:
    point: Any              # El valor del punto en 1D
    axis: int = 0           # Siempre 0 en 1D
    left: Optional['Node1D'] = None
    right: Optional['Node1D'] = None
    depth: int = 0

    def __repr__(self, level=0, prefix="Raíz:"):
        line = "\t" * level + f"{prefix} D{self.depth}: {self.point} (eje {self.axis})\n"
        if self.right:
            line += self.right.__repr__(level + 1, "R---")
        if self.left:
            line += self.left.__repr__(level + 1, "L---")
        return line


def build_kdtree_1d(points: List[Any], depth: int = 0) -> Optional[Node1D]:
    if not points:
        return None

    # Eje fijo para 1D
    axis = 0

    # Ordenar y seleccionar mediana como pivote
    sorted_points = sorted(points)
    mid = len(sorted_points) // 2
    pivot = sorted_points[mid]

    print(f"[Construcción 1D] Profundidad={depth}, Eje={axis}, Pivote={pivot}")
    print(f"  -> Lista original: {points}")
    print(f"  -> Lista ordenada: {sorted_points}")
    print(f"  -> Sublista izquierda: {sorted_points[:mid]}")
    print(f"  -> Sublista derecha: {sorted_points[mid+1:]}")

    node = Node1D(point=pivot, axis=axis, depth=depth)
    node.left = build_kdtree_1d(sorted_points[:mid], depth + 1)
    node.right = build_kdtree_1d(sorted_points[mid+1:], depth + 1)
    return node



# Ejemplo de uso
sample_points = [50, 30, 70, 20, 80, 25, 60, 90]
print("\n[Iniciando construcción del k-d tree 1D]")
tree = build_kdtree_1d(sample_points)
print("\n[Resultado] k-d tree 1D construido:")
print(tree or "El árbol está vacío.")

```

* **Ordenación y mediana** garantizan un árbol aproximado balanceado.
* La búsqueda en este caso reduce a comparaciones en una única coordenada, replicando un BST tradicional.

#### Construcción manual de un k-d tree 2D

En un ejemplo 2-D manual, se eligen pivotes concretos para ilustrar cómo el árbol crece:

```python
from dataclasses import dataclass
from typing import Any, List, Optional, Dict

@dataclass
class Node2D:
    """
    Nodo para un k-d tree en 2D.
    point_data: tupla (nombre, (x, y)).
    axis: eje de partición (0 para x, 1 para y).
    left, right: hijos izquierdo y derecho.
    depth: profundidad en el árbol.
    """
    point_data: Any
    axis: int
    left: Optional['Node2D'] = None
    right: Optional['Node2D'] = None
    depth: int = 0

    def __repr__(self, level=0, prefix="Raíz:") -> str:
        """
        Representación en texto del subárbol para depuración.
        Muestra nombre, coordenadas, eje y profundidad.
        """
        nombre, coords = self.point_data
        indent = "    " * level
        texto = f"{indent}{prefix} D{self.depth}: {nombre}{coords} (eje={self.axis})\n"
        # Mostrar hijo derecho primero
        if self.right:
            texto += self.right.__repr__(level + 1, "R---")
        if self.left:
            texto += self.left.__repr__(level + 1, "L---")
        return texto


def ejemplo_manual_kdtree_2d(ciudades: List[Tuple[str, Tuple[float, float]]]):
    """
    Construcción manual de los dos primeros niveles de un k-d tree en 2D.
    Argumento:
      - ciudades: lista de tuplas (nombre, (x, y)).
    """
    # Paso 1: raíz (eje x)
    pivot1 = ciudades[0]  # primer pivote
    depth1 = 0
    axis1 = depth1 % 2  # 0 -> eje x
    nombre1, coord1 = pivot1
    nodo_raiz = Node2D(point_data=pivot1, axis=axis1, depth=depth1)
    print(f"[Paso 1] Raíz: {nombre1} en {coord1}, eje={axis1} (x)")

    # Dividir en izquierda y derecha según x
    resto = [c for c in ciudades if c[0] != nombre1]
    izquierda = [c for c in resto if c[1][axis1] < coord1[axis1]]
    derecha  = [c for c in resto if c[1][axis1] >= coord1[axis1]]
    print(f"  Puntos con x < {coord1[0]}: {[c[0] for c in izquierda]}")
    print(f"  Puntos con x >= {coord1[0]}: {[c[0] for c in derecha]}")

    # Paso 2: subdividir la partición derecha (eje y)
    depth2 = 1
    axis2 = depth2 % 2  # 1 -> eje y
    pivot2 = next(c for c in derecha if c[0] == ciudades[1][0])
    nombre2, coord2 = pivot2
    nodo_raiz.right = Node2D(point_data=pivot2, axis=axis2, depth=depth2)
    print(f"[Paso 2] Nodo derecho: {nombre2} en {coord2}, eje={axis2} (y)")

    # Dividir subregión derecha por y
    resto_d = [c for c in derecha if c[0] != nombre2]
    abajo = [c for c in resto_d if c[1][axis2] < coord2[axis2]]
    arriba = [c for c in resto_d if c[1][axis2] >= coord2[axis2]]
    print(f"  Puntos con y < {coord2[1]}: {[c[0] for c in abajo]}")
    print(f"  Puntos con y >= {coord2[1]}: {[c[0] for c in arriba]}")

    # Mostrar árbol parcial
    print("\nÁrbol parcial tras dos niveles:")
    print(nodo_raiz)
    return nodo_raiz

# Ejemplo de uso:
ciudades_ej = [
    ("Opal City",  (6, 1.5)),
    ("Civic City", (7, 2.8)),
    ("New Carthage", (9, 6)),
    ("Happy Harbor", (10, 5)),
    ("Gotham City",  (7.6,1.4)),
    ("Metropolis",    (7.1,0.6))
]

i
```

Este proceso manual deja claro cómo alternar ejes en cada nivel (`depth % 2`) y cómo conectar nodos en un BST.


#### Ejemplo manual en 3-D

Aquí tienes un ejemplo **paso a paso** de cómo se construye un k-d tree en **3 dimensiones** (k=3) sobre un pequeño conjunto de puntos, mostrando explícitamente la elección de la coordenada de corte en cada nivel:

#### Conjunto de puntos de ejemplo

| Etiqueta | $x$ | $y$ | $z$ |
| :------: | :-: | :-: | :-: |
|   **A**  |  2  |  3  |  5  |
|   **B**  |  5  |  4  |  2  |
|   **C**  |  9  |  6  |  7  |
|   **D**  |  4  |  7  |  9  |
|   **E**  |  8  |  1  |  5  |
|   **F**  |  7  |  2  |  6  |
|   **G**  |  3  |  5  |  8  |


#### Nivel 0  $(i=0)$ -> coordenada $d = 0 \bmod 3 = 0$ (eje $x$)

1. **Ordenamos** todos los puntos por su $x$:

   $$A(2),G(3), D(4), B(5), F(7), E(8), C(9).$$
2. **Pivote** = mediana = cuarto elemento = **B**$(5,4,2)$.
3. **Particiones**:

   * **Izquierda** ($x < 5$): $\{A,G,D\}$.
   * **Derecha**  ($x > 5$): $\{F,E,C\}$.


#### Nivel 1  $(i=1)$ -> coordenada $d = 1 \bmod 3 = 1$ (eje $y$)

#### 1. Subárbol izquierdo de **B** con $\{A,G,D\}$

* Orden por $y$:

  $$A(3), G(5), D(7).$$
* Pivote = **G**$(3,5,8)$.
* Particiones:

  * Izquierda ($y < 5$): $\{A\}$.
  * Derecha  ($y > 5$): $\{D\}$.

#### 2. Subárbol derecho de **B** con $\{F,E,C\}$

* Orden por $y$:

  $$E(1), F(2), C(6)$$
* Pivote = **F**$(7,2,6)$.
* Particiones:

  * Izquierda ($y < 2$): $\{E\}$.
  * Derecha  ($y > 2$): $\{C\}$.

#### Nivel 2  $(i=2)$ -> coordenada $d = 2 \bmod 3 = 2$ (eje $z$)

En este nivel cada partición resultante tiene **solo un punto**, así que se convierten en hojas. Si alguna tuviese más, ordenaríamos por $z$ y elegiríamos la mediana.

#### Representación final del árbol

```
                       B (5,4,2)  [corte en x]
                      /           \
       G (3,5,8) [corte en y]     F (7,2,6) [corte en y]
        /       \                  /         \
A(2,3,5)[hoja] D(4,7,9)[hoja]  E(8,1,5)[hoja] C(9,6,7)[hoja]
```

* Entre corchetes indicamos **la coordenada usada** para partir en ese nivel.
* Cada nodo tiene **dos hijos** (o ninguno si es hoja).
* La profundidad $i$ determina el eje: $i\mod3 = 0\mapsto x$, $1\mapsto y$, $2\mapsto z$.

##### ¿Qué hemos logrado?

* **Binario**: cada partición es **solo** en dos mitades, independientemente de $k$.
* **Ciclo de ejes**: recorremos las $k$ coordenadas de forma cíclica.
* **Regiones acotadas**: tras $k$ cortes (uno por cada eje), cada caja está limitada en todas las dimensiones.
* **Búsqueda e inserción**: idénticas a un BST, comparando sucesivamente con la coordenada correspondiente.

Este mismo procedimiento funciona para **cualquier $k$**: basta con rotar la elección de eje mediante $d = i \bmod k$. Así obtenemos un **k-d tree** que crece en tiempo $O(n\log n)$ y permite búsquedas de vecinos cercanos en $O(\log n)$ promedio.


#### Construcción automática de un k-d tree 2D

Para generar de forma automática un árbol balanceado, se usa la mediana de cada sublista como pivote:

```python
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

@dataclass
class Node2D:
    """
    Nodo para un k-d tree en 2D.
    point_data: tupla (nombre, (x, y)).
    axis: eje de partición (0 para x, 1 para y).
    left, right: subárboles.
    depth: profundidad en el árbol.
    """
    point_data: Tuple[str, Tuple[float, float]]
    axis: int
    left: Optional['Node2D'] = None
    right: Optional['Node2D'] = None
    depth: int = 0

    def __repr__(self, level=0, prefix="Raíz:") -> str:
        nombre, coords = self.point_data
        indent = "    " * level
        texto = f"{indent}{prefix} D{self.depth}: {nombre}{coords} (eje={self.axis})\n"
        if self.right:
            texto += self.right.__repr__(level+1, "R---")
        if self.left:
            texto += self.left.__repr__(level+1, "L---")
        return texto


def build_kdtree_2d(
    points: List[Tuple[str, Tuple[float, float]]],
    depth: int = 0
) -> Optional[Node2D]:
    """
    Construye un k-d tree balanceado en 2D usando mediana como pivote.
    """
    if not points:
        return None

    k = 2
    axis = depth % k

    try:
        sorted_points = sorted(points, key=lambda p: p[1][axis])
    except Exception as e:
        print(f"[Error] al ordenar puntos por eje {axis}: {e}")
        return None

    median = len(sorted_points) // 2
    pivot = sorted_points[median]
    print(f"[Construcción 2D] Profundidad={depth}, Eje={axis}, Pivote={pivot[0]}{pivot[1]}")

    node = Node2D(point_data=pivot, axis=axis, depth=depth)
    node.left = build_kdtree_2d(sorted_points[:median], depth+1)
    node.right = build_kdtree_2d(sorted_points[median+1:], depth+1)

    return node

# Lista de ciudades: tuplas (nombre, (x, y))
ciudades = ciudades_mapa_dc_list
print("[Iniciando construcción del k-d tree 2D]")
arbol = build_kdtree_2d(ciudades)
print("\n[Árbol resultante]")
print(arbol if arbol else "El árbol está vacío.")

```

El uso de **medianas** en cada nivel tiende a generar árboles balanceados, reduciendo la profundidad máxima y mejorando la eficiencia de búsqueda.


#### Generalización a 3D y dimensiones superiores

El mismo enfoque se extiende a espacios k-dimensionales. Para k=3, alternamos entre ejes *x*, *y* y *z*:

```python
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

@dataclass
class Node3D:
    """
    Nodo de un k-d tree en 3D.

    point_data: tupla (nombre, (x, y, z)).
    axis: eje de partición (0: x, 1: y, 2: z).
    left, right: subárboles izquierdo y derecho.
    depth: profundidad en el árbol.
    """
    point_data: Tuple[str, Tuple[float, float, float]]
    axis: int
    left: Optional['Node3D'] = None
    right: Optional['Node3D'] = None
    depth: int = 0

    def __repr__(self, level: int = 0, prefix: str = "Raíz:") -> str:
        nombre, coords = self.point_data
        indent = "    " * level
        texto = f"{indent}{prefix} D{self.depth}: {nombre}{coords} (eje={self.axis})\n"
        if self.right:
            texto += self.right.__repr__(level + 1, "R---")
        if self.left:
            texto += self.left.__repr__(level + 1, "L---")
        return texto


def build_kdtree_3d(
    points: List[Tuple[str, Tuple[float, float, float]]],
    depth: int = 0
) -> Optional[Node3D]:
    """
    Construye recursivamente un k-d tree en 3D usando la mediana como pivote.
    La coordenada a comparar se elige cíclicamente según depth % 3.
    """
    if not points:
        return None

    axis = depth % 3
    try:
        sorted_points = sorted(points, key=lambda p: p[1][axis])
    except Exception as e:
        print(f"[Error] No se pudo ordenar por el eje {axis}: {e}")
        return None

    median_idx = len(sorted_points) // 2
    pivot = sorted_points[median_idx]
    nombre, coords = pivot
    print(f"[Construcción 3D] Profundidad={depth}, Eje={axis}, Pivote={nombre}{coords}")

    nodo = Node3D(point_data=pivot, axis=axis, depth=depth)
    nodo.left = build_kdtree_3d(sorted_points[:median_idx], depth + 1)
    nodo.right = build_kdtree_3d(sorted_points[median_idx + 1:], depth + 1)
    return nodo


# Ejemplo de uso:
puntos_3d = [
        ("A", (10, 20, 30)),
        ("B", (5, 25, 35)),
        ("C", (15, 15, 25)),
        ("D", (12, 22, 32)),
        ("E", (3, 18, 28)),
        ("F", (18, 12, 22)),
        ("G", (8, 8, 8))
    ]
print("[Iniciando la construcción de un k-d tree 3D]")
arbol = build_kdtree_3d(puntos_3d)
print("\n[Árbol resultante]")
print(arbol if arbol else "El árbol está vacío.")

```

Más allá de 3D, no existe una representación geométrica intuitiva, pero el mismo ciclo `axis = depth % k` y la mediana como pivote permiten construir árboles en cualquier dimensión.

####  Cobertura y eficiencia en la búsqueda

**Cobertura jerárquica de cada nodo**
En un k-d tree, cada nodo representa un pivote y divide el espacio en dos según la coordenada que le corresponda (eje = profundidad mod k). 
La región "cubierta" por un nodo $N$ es el conjunto de puntos que, al buscarse, atraviesan $N$. 
Formalmente, la región de $N$ es la intersección de todos los semiespacios definidos por sus ancestros: para cada ancestro $A$ con eje de partición $a_A$ y pivote $p_A$, le 
corresponde una condición $x_{a_A}<p_{A,a_A}$ si $N$ está en el subárbol izquierdo de $A$, o $x_{a_A}\ge p_{A,a_A}$ si está en el derecho. De este modo, cada nodo define un hiperrectángulo que encierra exactamente los puntos que caen dentro de esa serie de restricciones.

**Búsqueda exacta en un k-d tree**
Para determinar si existe un punto $X$ (o en qué hoja terminaría su recorrido), partimos de la raíz y, en cada nodo con pivote $p$ y 
eje $a$, comparamos $X_a$ con $p_a$. Si $X_a<p_a$ descendemos al hijo izquierdo; en caso contrario, al hijo derecho.
Avanzamos incrementando la profundidad y ciclando el eje, hasta encontrar $X$ o llegar a un subárbol vacío. 
Cada comparación descarta inmediatamente toda la mitad opuesta del espacio, lo que, en promedio, produce un recorrido de longitud $O(\log n)$.

**Alternancia de ejes y balance espacial**
Si siempre partiéramos según la misma coordenada (por ejemplo, $x$), generaríamos particiones infinitas paralelas al eje $y$ y regiones sin 
acotar en esa dirección. 
En cambio, al alternar ejes $x,y,x,y,\dots$ en 2-D, o ciclando entre las $k$ dimensiones en $\mathbb R^k$, tras $k$ niveles cada región queda limitada por dos planos en cada dimensión. Esto reduce la superposición de particiones y favorece que, con pivotes tipo mediana, el árbol resulte aproximadamente balanceado.

**Complejidad y eficiencia**

* **Construcción**: si en cada nivel seleccionamos la mediana (ordenando o con `nth_element`), la recurrencia $T(n)=2T(n/2)+O(n)$ da $O(n\log n)$.
* **Búsqueda exacta**: en promedio $O(\log n)$, pues cada comparación descarta la mitad de los puntos; en el peor caso (árbol degenerado) puede llegar a $O(n)$.
* **Búsqueda de k vecinos más cercanos**: parte de la misma idea, pero tras descender a la hoja más profunda se "retrocede" y poda subárboles cuya región está demasiado lejos, manteniendo un coste típico $O(\log n)$ por vecino.
* **Búsqueda de rango ortogonal**: explora todos los nodos cuyas regiones intersectan el rango; su coste es $O(n^{1-1/k}+m)$, donde $m$ es el número de puntos reportados.

**5.¿Por qué es rápido?**

El k-d tree combina la simplicidad y las garantías de un BST (comparaciones binarias y recorrido logarítmico en promedio) con un método de comparación cíclico que acota regiones en todas las dimensiones. Así, cada comparación permite **podar** de manera inmediata grandes porciones del espacio de búsqueda, logrando consultas muy eficientes tanto para búsquedas exactas como para vecinos más cercanos o rangos multidimensionales.



