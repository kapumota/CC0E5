import math
import random
import logging

logging.basicConfig(level=logging.INFO)

# Clase Point
class Point:
    """
    Representa un punto en un espacio de k dimensiones.
    """
    def __init__(self, coordinates):
        if not isinstance(coordinates, (list, tuple)):
            raise TypeError("Las coordenadas deben ser una lista o tupla")
        self._coordinates = tuple(float(c) for c in coordinates)
        self.dimensionality = len(self._coordinates)

    def coordinate(self, dim_index):
        if not 0 <= dim_index < self.dimensionality:
            raise IndexError(f"Índice de dimensión {dim_index} fuera de rango para dimensionalidad {self.dimensionality}")
        return self._coordinates[dim_index]

    def distance_to(self, other_point):
        if not isinstance(other_point, Point):
            raise TypeError("other_point debe ser una instancia de Point")
        if self.dimensionality != other_point.dimensionality:
            raise ValueError("Los puntos deben tener la misma dimensionalidad para calcular la distancia")
        dist_sq = sum((s - o) ** 2 for s, o in zip(self._coordinates, other_point._coordinates))
        return math.sqrt(dist_sq)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self._coordinates == other._coordinates

    def equals(self, other_point):
        return self == other_point

    def __hash__(self):
        return hash(self._coordinates)

    @property
    def coordinates(self):
        return self._coordinates

    def __getitem__(self, index):
        return self.coordinate(index)

    def __len__(self):
        return self.dimensionality

    @staticmethod
    def validate_point_array(points, expected_dimensionality=None, context=""):
        if not isinstance(points, list):
            raise TypeError(f"{context}: Se esperaba una lista de puntos.")
        if not points:
            return expected_dimensionality

        if expected_dimensionality is None:
            if not isinstance(points[0], Point):
                 raise TypeError(f"{context} (punto 0): Se esperaba un objeto Point, se obtuvo {type(points[0])}.")
            expected_dimensionality = points[0].dimensionality

        for i, p in enumerate(points):
            Point.validate_point(p, expected_dimensionality, f"{context} (punto {i})")
        return expected_dimensionality

    @staticmethod
    def validate_point(point, expected_dimensionality, context=""):
        if not isinstance(point, Point):
            raise TypeError(f"{context}: Se esperaba un objeto Point, se obtuvo {type(point)}.")
        if expected_dimensionality is not None and point.dimensionality != expected_dimensionality:
            raise ValueError(
                f"{context}: El punto tiene dimensionalidad {point.dimensionality}, se esperaba {expected_dimensionality}."
            )

    def __repr__(self):
        return f"Point({list(self._coordinates)})"

# Clase Ball
class Ball:
    """
    Representa una hiperesfera (ball) definida por un punto central y un radio.
    """
    def __init__(self, center, radius):
        Point.validate_point(center, None, "Constructor de Ball (center)")
        if not isinstance(radius, (int, float)) or radius < 0:
            raise ValueError(f"El radio debe ser un número no negativo, se obtuvo {radius}.")

        self.center = center
        self.radius = float(radius)
        self.dimensionality = center.dimensionality

    def contains_point(self, point):
        Point.validate_point(point, self.dimensionality, "Ball.contains_point")
        return point.distance_to(self.center) <= self.radius + 1e-9

    def intersects_ball(self, other_ball):
        if not isinstance(other_ball, Ball):
            raise TypeError("El argumento debe ser un objeto Ball.")
        if self.dimensionality != other_ball.dimensionality:
            return False
        dist_centers = self.center.distance_to(other_ball.center)
        return dist_centers <= (self.radius + other_ball.radius) + 1e-9

    def min_dist_to_point(self, point):
        Point.validate_point(point, self.dimensionality, "Ball.min_dist_to_point")
        dist_to_center = point.distance_to(self.center)
        return max(0.0, dist_to_center - self.radius)

    def min_dist_sq_to_point(self, point):
        dist_to_center = point.distance_to(self.center)
        val = max(0.0, dist_to_center - self.radius)
        return val * val

    def __repr__(self):
        return f"Ball(center={self.center}, radius={self.radius:.3f})"

#Funciones auxiliares
def _calculate_mean_point(points, dimensionality=None):
    if not points:
        return None
    current_dimensionality = dimensionality if dimensionality is not None else points[0].dimensionality
    mean_coords = [0.0] * current_dimensionality
    num_points = len(points)

    for p in points:
        for i in range(current_dimensionality):
            mean_coords[i] += p.coordinate(i)

    mean_coords = [c / num_points for c in mean_coords]
    return Point(mean_coords)

def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)

# Clase interna _BallNode
class _BallNode:
    _DIST_EPSILON = 1e-9

    def __init__(self, points, leaf_size_threshold, dimensionality, depth=0):
        self.dimensionality = dimensionality
        self.leaf_size_threshold = leaf_size_threshold
        self.depth = depth
        self.ball = None
        self.left_child = None
        self.right_child = None
        self.is_leaf = False
        self.points_in_leaf = []
        self.num_points_in_subtree = len(points)

        if not points:
            self.is_leaf = True
            return

        current_center = _calculate_mean_point(points, self.dimensionality)
        if current_center is None:
            self.is_leaf = True
            return

        current_radius = 0.0 if len(points) == 1 else max(p.distance_to(current_center) for p in points)
        self.ball = Ball(current_center, current_radius)

        # Un nodo con 1 punto siempre es una hoja.
        # O si el número de puntos es menor que el umbral para dividir.
        if len(points) <= 1 or len(points) < self.leaf_size_threshold:
            self.is_leaf = True
            self.points_in_leaf = list(points)
            return

        self.is_leaf = False
        # Estrategia de selección de pivotes
        x0 = random.choice(points)
        x1 = max(points, key=lambda p: p.distance_to(x0))
        x2 = max(points, key=lambda p: p.distance_to(x1))

        SL_points, SR_points = [], []

        if x1.distance_to(x2) < self._DIST_EPSILON: # Eje degenerado
            SL_points, SR_points = self._fallback_split(points)
        else:
            # Proyección y partición
            v_axis_coords = [c1 - c2_coord for c1, c2_coord in zip(x1.coordinates, x2.coordinates)]
            # Comprensión de lista optimizada para projected_data
            projected_data = []
            for p_current in points:
                v_point_to_x2_coords = [pc - x2c for pc, x2c in zip(p_current.coordinates, x2.coordinates)]
                dot_product = sum(a * b for a, b in zip(v_point_to_x2_coords, v_axis_coords))
                projected_data.append({'value': dot_product, 'point': p_current})
            
            min_proj_val = min(item['value'] for item in projected_data)
            max_proj_val = max(item['value'] for item in projected_data)

            if (max_proj_val - min_proj_val) < self._DIST_EPSILON: # Todas las proyecciones son iguales
                SL_points, SR_points = self._fallback_split(points)
            else:
                projected_data.sort(key=lambda item: item['value'])
                median_projection_value = projected_data[len(projected_data) // 2]['value']
                current_SL_points = [item['point'] for item in projected_data if item['value'] < median_projection_value]
                current_SR_points = [item['point'] for item in projected_data if item['value'] >= median_projection_value]

                # Fallback si la partición basada en valor mediano falla en dividir los puntos
                if points and (not current_SL_points or not current_SR_points):
                    points_sorted_by_proj = [item['point'] for item in projected_data]
                    SL_points, SR_points = self._fallback_split(points_sorted_by_proj)
                else:
                    SL_points = current_SL_points
                    SR_points = current_SR_points
        
        # Llamadas recursivas
        self.left_child = _BallNode(SL_points, self.leaf_size_threshold, self.dimensionality, self.depth + 1)
        self.right_child = _BallNode(SR_points, self.leaf_size_threshold, self.dimensionality, self.depth + 1)

    def _fallback_split(self, point_list):
        if not point_list: return [], []
        mid_idx = len(point_list) // 2
        # Esta división simple asegura que si point_list tiene >0 puntos,
        # SR_points siempre tendrá puntos. SL_points podría ser vacío si len=1 y mid_idx=0.
        # Pero la condición de hoja len(points) <= 1 ya debería haber manejado el caso de 1 punto.
        return point_list[:mid_idx], point_list[mid_idx:]

    def nearest_neighbour(self, target_point, current_best_point, current_best_dist_sq):
        if self.is_leaf:
            if not self.points_in_leaf: return current_best_point, current_best_dist_sq
            for p_leaf in self.points_in_leaf:
                dist_sq = sum((tp - lp) ** 2 for tp, lp in zip(target_point.coordinates, p_leaf.coordinates))
                if dist_sq < current_best_dist_sq:
                    current_best_dist_sq, current_best_point = dist_sq, p_leaf
            return current_best_point, current_best_dist_sq

        if self.ball is None or self.ball.min_dist_sq_to_point(target_point) >= current_best_dist_sq:
            return current_best_point, current_best_dist_sq

        dist_sq_left = float('inf')
        if self.left_child and self.left_child.ball: # Asegurarse que el hijo y su bola existen
            dist_sq_left = sum((tp - lc) ** 2 for tp, lc in zip(target_point.coordinates, self.left_child.ball.center.coordinates))
        
        dist_sq_right = float('inf')
        if self.right_child and self.right_child.ball: # Asegurarse que el hijo y su bola existen
            dist_sq_right = sum((tp - rc) ** 2 for tp, rc in zip(target_point.coordinates, self.right_child.ball.center.coordinates))

        first_child, second_child = (self.left_child, self.right_child) if dist_sq_left < dist_sq_right else (self.right_child, self.left_child)

        if first_child: # Verificar si el hijo existe
            current_best_point, current_best_dist_sq = first_child.nearest_neighbour(target_point, current_best_point, current_best_dist_sq)
        
        if second_child and second_child.ball and \
           second_child.ball.min_dist_sq_to_point(target_point) < current_best_dist_sq: # Verificar si el hijo y su bola existen
            current_best_point, current_best_dist_sq = second_child.nearest_neighbour(target_point, current_best_point, current_best_dist_sq)
        
        return current_best_point, current_best_dist_sq

    def points_within_distance_from(self, query_center_point, query_radius, results_list):
        query_radius_sq = query_radius * query_radius
        if self.is_leaf:
            if not self.points_in_leaf: return
            for p_leaf in self.points_in_leaf:
                if sum((qc - lp) ** 2 for qc, lp in zip(query_center_point.coordinates, p_leaf.coordinates)) <= query_radius_sq:
                    results_list.append(p_leaf)
            return

        if self.ball is None or self.ball.min_dist_to_point(query_center_point) > query_radius + self._DIST_EPSILON:
            return

        if query_center_point.distance_to(self.ball.center) + self.ball.radius <= query_radius + self._DIST_EPSILON:
            self._collect_all_points_in_subtree(results_list)
            return

        if self.left_child: self.left_child.points_within_distance_from(query_center_point, query_radius, results_list)
        if self.right_child: self.right_child.points_within_distance_from(query_center_point, query_radius, results_list)

    def _collect_all_points_in_subtree(self, results_list):
        if self.is_leaf: results_list.extend(self.points_in_leaf)
        else:
            if self.left_child: self.left_child._collect_all_points_in_subtree(results_list)
            if self.right_child: self.right_child._collect_all_points_in_subtree(results_list)

    def __iter__(self):
        if self.is_leaf: yield from self.points_in_leaf
        else:
            if self.left_child: yield from self.left_child
            if self.right_child: yield from self.right_child

    @property
    def height(self):
        if self.is_leaf: return 1
        left_h = self.left_child.height if self.left_child else 0
        right_h = self.right_child.height if self.right_child else 0
        return 1 + max(left_h, right_h)

# Clase BallTree
class BallTree:
    _DEFAULT_LEAF_SIZE_THRESHOLD = 20

    def __init__(self, points=None, leaf_size_threshold=None, handle_duplicates="store"):
        if points is None: points = []
        if not isinstance(points, list):
            raise TypeError("El parámetro 'points' debe ser una lista de objetos Point.")

        self._dimensionality = None
        self._root = None
        self._size = 0

        if leaf_size_threshold is None: self.leaf_size_threshold = self._DEFAULT_LEAF_SIZE_THRESHOLD
        elif isinstance(leaf_size_threshold, int) and leaf_size_threshold >= 1: self.leaf_size_threshold = leaf_size_threshold
        else: raise ValueError("leaf_size_threshold debe ser un entero >= 1.")

        processed_points = list(points)
        if handle_duplicates == "unique" and processed_points:
            unique_point_set = set()
            temp_unique_list = []
            for p in processed_points:
                if p not in unique_point_set:
                    unique_point_set.add(p)
                    temp_unique_list.append(p)
            processed_points = temp_unique_list
            logging.info(f"Manejo de duplicados 'unique': {len(points)} puntos originales -> {len(processed_points)} puntos únicos para construcción.")

        if processed_points:
            self._dimensionality = Point.validate_point_array(processed_points, None, 'BallTree.__init__')
            if self._dimensionality is None and processed_points:
                self._dimensionality = processed_points[0].dimensionality
            
            self._root = _BallNode(processed_points, self.leaf_size_threshold, self._dimensionality)
            self._size = self._root.num_points_in_subtree if self._root else 0
        else:
            self._root = _BallNode([], self.leaf_size_threshold, 0) # Dimensionality 0 para árbol vacío
            self._size = 0

    @property
    def dimensionality(self):
        return self._dimensionality

    @property
    def size(self):
        return self._size
    
    def __len__(self):
        return self.size

    @property
    def height(self):
        if self.is_empty(): return 0
        return self._root.height

    def is_empty(self):
        return self._size == 0

    def nearest_neighbour(self, target_point):
        if self.is_empty(): return None
        Point.validate_point(target_point, self.dimensionality, 'BallTree.nearest_neighbour (target_point)')
        best_point, _ = self._root.nearest_neighbour(target_point, None, float('inf'))
        return best_point

    def points_within_distance_from(self, center_point, distance):
        if self.is_empty(): return []
        Point.validate_point(center_point, self.dimensionality, 'BallTree.points_within_distance_from (center_point)')
        if not _is_number(distance) or distance < 0:
            raise ValueError(f"La distancia debe ser un número no negativo, se obtuvo {distance}.")
        results = []
        self._root.points_within_distance_from(center_point, float(distance), results)
        return results

    def __iter__(self):
        if not self.is_empty(): yield from self._root

    def __repr__(self):
        dims_str = str(self._dimensionality if self._dimensionality is not None else "indefinida")
        return f"<BallTree size={self.size} dims={dims_str} height={self.height}>"

# Uso de ejemplo y pruebas con asserts
if __name__ == '__main__':
    print("Inicializando pruebas para BallTree (con asserts)")

    # Caso de prueba 1: Puntos 2D simples
    points_2d = [
        Point([2, 3]), Point([5, 4]), Point([9, 6]), Point([4, 7]),
        Point([8, 1]), Point([7, 2]), Point([6, 5]), Point([1, 1]),
        Point([3, 8]), Point([10, 3])
    ]
    ball_tree_2d = BallTree(points_2d, leaf_size_threshold=2)
    assert len(ball_tree_2d) == len(points_2d), "Test 1A: Tamaño incorrecto"
    print(f"Árbol 2D creado: {ball_tree_2d}")

    target_2d = Point([6, 4])
    nn_2d = ball_tree_2d.nearest_neighbour(target_2d)
    assert nn_2d in [Point([5,4]), Point([6,5])], f"Test 1B: NN incorrecto para {target_2d}, obtuvo {nn_2d}"
    print(f"Vecino más cercano a {target_2d}: {nn_2d}, Distancia: {target_2d.distance_to(nn_2d):.3f}")

    query_center_2d = Point([5, 5])
    query_radius_2d = 2.5
    points_in_range_2d = ball_tree_2d.points_within_distance_from(query_center_2d, query_radius_2d)
    expected_in_range_2d = {Point([5,4]), Point([4,7]), Point([6,5])}
    assert set(points_in_range_2d) == expected_in_range_2d, f"Test 1C: Puntos en rango incorrectos. Esperado {expected_in_range_2d}, Obtenido {set(points_in_range_2d)}"
    print(f"Puntos dentro de {query_radius_2d} de {query_center_2d}: {points_in_range_2d}")
    print("-" * 20)

    # Caso de prueba 2: Mayor dimensionalidad (3D) 
    points_3d = [Point([1,1,1]), Point([5,5,5]), Point([0,0,0]), Point([10,10,10])]
    ball_tree_3d = BallTree(points_3d, leaf_size_threshold=1) # leaf_size_threshold=1 es la clave del problema anterior
    assert len(ball_tree_3d) == 4, "Test 2A: Tamaño 3D incorrecto"
    print(f"Árbol 3D creado: {ball_tree_3d}") # Se espera que ahora funcione
    target_3d = Point([4,4,4])
    nn_3d = ball_tree_3d.nearest_neighbour(target_3d)
    assert nn_3d == Point([5,5,5]), f"Test 2B: NN 3D incorrecto para {target_3d}, obtuvo {nn_3d}"
    print(f"Vecino más cercano a {target_3d}: {nn_3d}")
    print("-" * 20)

    # Caso de prueba 3: Árbol vacío
    empty_tree = BallTree()
    assert empty_tree.is_empty(), "Test 3A: Árbol vacío no detectado como tal"
    assert len(empty_tree) == 0, "Test 3B: len(árbol_vacío) no es 0"
    assert empty_tree.nearest_neighbour(Point([0,0])) is None, "Test 3C: NN en árbol vacío no es None"
    assert empty_tree.points_within_distance_from(Point([0,0]), 1) == [], "Test 3D: Rango en árbol vacío no es lista vacía"
    print("Pruebas de árbol vacío pasadas.")
    print("-" * 20)
    
    # Caso de prueba 4: Árbol con un solo punto
    single_point = Point([10, 20])
    single_point_tree = BallTree([single_point], leaf_size_threshold=1) # Esto ahora debería ser una hoja directamente
    assert not single_point_tree.is_empty(), "Test 4A: Árbol de un solo punto detectado como vacío"
    assert len(single_point_tree) == 1, "Test 4B: len(árbol_un_punto) no es 1"
    assert single_point_tree._root.is_leaf, "Test 4X: Árbol de un solo punto no es hoja raíz"
    assert single_point_tree.nearest_neighbour(Point([11,21])) == single_point, "Test 4C: NN en árbol de un solo punto"
    assert single_point_tree.points_within_distance_from(Point([10,20]), 5) == [single_point], "Test 4D: Rango en árbol de un solo punto"
    print("Pruebas de árbol con un solo punto pasadas.")
    print("-" * 20)

    # Caso de prueba 5: Todos los puntos idénticos
    identical_points = [Point([5,5]), Point([5,5]), Point([5,5])]
    identical_tree_store = BallTree(identical_points, leaf_size_threshold=2)
    assert len(identical_tree_store) == 3, "Test 5A: Tamaño con duplicados (store)"
    identical_tree_unique = BallTree(identical_points, leaf_size_threshold=2, handle_duplicates="unique")
    assert len(identical_tree_unique) == 1, "Test 5B: Tamaño con duplicados (unique)"
    nn_identical = identical_tree_unique.nearest_neighbour(Point([5.1,5.1]))
    assert nn_identical == Point([5,5]), f"Test 5C: NN con puntos idénticos. Esperado Point([5,5]), Obtenido {nn_identical}"
    points_in_id_range_unique = identical_tree_unique.points_within_distance_from(Point([5,5]),1)
    assert len(points_in_id_range_unique) == 1 and points_in_id_range_unique[0] == Point([5,5]), "Test 5D: Rango con duplicados (unique)"
    points_in_id_range_store = identical_tree_store.points_within_distance_from(Point([5,5]),1)
    assert len(points_in_id_range_store) == 3, "Test 5E: Rango con duplicados (store), se esperan todos"
    assert all(p == Point([5,5]) for p in points_in_id_range_store), "Test 5F: Rango con duplicados (store), todos deben ser el punto"
    print("Pruebas con puntos idénticos pasadas.")
    print("-" * 20)

    # Caso de prueba 6: Puntos colineales
    collinear_points = [Point([1,1]), Point([2,2]), Point([3,3]), Point([4,4]), Point([0,0])]
    collinear_tree = BallTree(collinear_points, leaf_size_threshold=2)
    assert len(collinear_tree) == len(collinear_points), "Test 6A: Tamaño árbol colineal"
    target_collinear = Point([2.1, 2.1]) 
    nn_collinear = collinear_tree.nearest_neighbour(target_collinear)
    assert nn_collinear == Point([2,2]), f"Test 6B: NN puntos colineales. Esperado Point([2,2]), Obtenido {nn_collinear}"
    print("Pruebas con puntos colineales pasadas.")
    print("-" * 20)
    
    # Caso de prueba 7: Un solo punto y k_leaf_threshold > 1
    tree_one_point_large_k = BallTree([Point([5,5])], leaf_size_threshold=10)
    assert len(tree_one_point_large_k) == 1, "Test 7A: Tamaño un punto, k grande"
    if tree_one_point_large_k._root:
        assert tree_one_point_large_k._root.is_leaf, "Test 7B: Raíz debe ser hoja"
    assert tree_one_point_large_k.nearest_neighbour(Point([4,4])) == Point([5,5]), "Test 7C: NN un punto, k grande"
    print("Pruebas con un punto y k_leaf_threshold grande pasadas.")
    print("-" * 20)

    print("Pruebas de BallTree (con asserts) finalizadas")