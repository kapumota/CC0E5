from __future__ import annotations
import math
import statistics
import heapq
from typing import List, Tuple, Generator, Optional, Iterable
from dataclasses import dataclass

# Constantes y Configuración
_DEFAULT_MAX_CHILDREN = 8
_EPSILON = 1e-9

# Clases de datos y utilidades 

@dataclass(frozen=True, slots=True)
class Point:
    _coords: tuple[float, ...]
    
    @property
    def dimensionality(self) -> int:
        return len(self._coords)

    def coordinate(self, index: int) -> float:
        return self._coords[index]

    def distance_sq_to(self, other: Point) -> float:
        """Distancia al cuadrado entre dos puntos."""
        return sum((c1 - c2) ** 2 for c1, c2 in zip(self._coords, other._coords))

    def distance_to(self, other: Point) -> float:
        """Distancia euclídea entre dos puntos."""
        return math.sqrt(self.distance_sq_to(other))

    @staticmethod
    def centroid(points: Iterable[Point]) -> Point:
        point_list = list(points)
        if not point_list:
            raise ValueError("No se puede calcular el centroide de una colección vacía.")
        dim = point_list[0].dimensionality
        centroid_coords = [sum(p.coordinate(i) for p in point_list) / len(point_list) for i in range(dim)]
        return Point(tuple(centroid_coords))

# Clase principal del árbol 

class SsTree:
    def __init__(
        self,
        points: Optional[Iterable[Point]] = None,
        max_children: int = _DEFAULT_MAX_CHILDREN,
        use_variance_split: bool = True
    ):
        initial_points = list(points) if points else []
        self._max_children = max_children
        self._use_variance_split = use_variance_split
        self._points_set: set[Point] = set(initial_points)
        self._k: Optional[int] = None
        
        if initial_points:
            self._k = initial_points[0].dimensionality
            self._root = _Node.build(
                initial_points,
                self._k,
                self._max_children,
                use_variance_split=self._use_variance_split,
                depth=0
            )
        else:
            self._root = _Node.create_empty_leaf(max_children)

    def add(self, point: Point) -> None:
        if point in self._points_set:
            return  # duplicado, O(1)
        if self._root.size == 0:
            self._k = point.dimensionality
            self._root = _Node.build([point], self._k, self._max_children, use_variance_split=self._use_variance_split)
            self._points_set.add(point)
            return
        if point.dimensionality != self._k:
            raise ValueError("Inconsistencia de dimensionalidad.")

        new_nodes = self._root.add(point)
        self._points_set.add(point)
        if new_nodes:
            self._root = _Node.create_internal(new_nodes, self._k, self._max_children)
    
    def nearest_neighbour(self, target: Point) -> Optional[Tuple[Point, float]]:
        """
        Encuentra el punto más cercano en el árbol al punto `target`.
        Devuelve una tupla (punto, distancia) o None si el árbol está vacío o hay inconsistencia de dimensionalidad.
        """
        if self.size == 0 or target.dimensionality != self._k:
            return None
        result = self._root.nearest_neighbour(target)
        # result devuelve (punto, d_sq), convertir distancia al valor real
        if result:
            p, d_sq = result
            return (p, math.sqrt(d_sq))
        return None

    @property
    def dimensionality(self) -> Optional[int]:
        return self._k

    @property
    def size(self) -> int:
        return self._root.size

    def __len__(self) -> int:
        return self.size
    
    def __contains__(self, point: Point) -> bool:
        if self.size == 0 or point.dimensionality != self._k:
            return False
        return point in self._points_set
    
    def __repr__(self) -> str:
        return f"SsTree(dimensionality={self._k}, size={self.size}, height={self._root.height})"

# Clase interna del nodo 

@dataclass(slots=True)
class _Node:
    max_children: int
    size: int
    centroid: Optional[Point]
    radius: float
    sum_of_coords: Optional[tuple[float, ...]]
    dimensionality: Optional[int]
    points: Optional[list[Point]] = None
    children: Optional[list[_Node]] = None

    @classmethod
    def create_empty_leaf(cls, mc: int) -> _Node:
        return cls(mc, 0, None, 0.0, None, None, points=[])

    @classmethod
    def create_leaf(cls, pts: list[Point], k: int, mc: int) -> _Node:
        s = len(pts)
        sc = tuple(sum(p.coordinate(d) for p in pts) for d in range(k))
        c = Point(tuple(coord / s for coord in sc))
        r = max((p.distance_to(c) for p in pts), default=0.0)
        return cls(mc, s, c, r, sc, k, points=pts)

    @classmethod
    def create_internal(cls, ch: list[_Node], k: int, mc: int) -> _Node:
        s = sum(c.size for c in ch)
        sc = tuple(sum(coords) for coords in zip(*(c.sum_of_coords for c in ch)))
        c = Point(tuple(coord / s for coord in sc))
        r = max((child.centroid.distance_to(c) + child.radius for child in ch), default=0.0)
        return cls(mc, s, c, r, sc, k, children=ch)

    @classmethod
    def build(
        cls,
        pts: list[Point],
        k: int,
        mc: int,
        use_variance_split: bool = True,
        depth: int = 0
    ) -> _Node:
        if len(pts) <= mc:
            return cls.create_leaf(pts, k, mc)
        
        # Selección de dimensión de split: por varianza o por heurística alterna
        if use_variance_split or depth == 0:
            variances = [statistics.variance(p.coordinate(d) for p in pts) if len(pts) > 1 else 0 for d in range(k)]
            split_dim = variances.index(max(variances))
        else:
            split_dim = depth % k

        pts.sort(key=lambda p: p.coordinate(split_dim))
        m = math.ceil(len(pts) / mc)
        children = [
            cls.build(pts[i:i + m], k, mc, use_variance_split, depth + 1)
            for i in range(0, len(pts), m)
        ]
        return cls.create_internal(children, k, mc)

    @property
    def is_leaf(self) -> bool:
        return self.children is None

    @property
    def height(self) -> int:
        if self.is_leaf:
            return 1
        return 1 + max(c.height for c in self.children) if self.children else 1

    def add(self, point: Point) -> Optional[list[_Node]]:
        if self.is_leaf:
            self.points.append(point)
            if len(self.points) > self.max_children:
                return self._split_leaf()
        else:
            closest = min(
                self.children,
                key=lambda c: point.distance_sq_to(c.centroid)
            )
            new_nodes = closest.add(point)
            if new_nodes:
                self.children.remove(closest)
                self.children.extend(new_nodes)
                if len(self.children) > self.max_children:
                    return self._split_internal()
        self._update_stats()
        return None

    def _split_leaf(self) -> list[_Node]:
        variances = [
            statistics.variance(p.coordinate(d) for p in self.points) if len(self.points) > 1 else 0
            for d in range(self.dimensionality)
        ]
        split_dim = variances.index(max(variances))
        self.points.sort(key=lambda p: p.coordinate(split_dim))
        m = math.ceil(len(self.points) / self.max_children)
        return [
            _Node.create_leaf(self.points[i:i + m], self.dimensionality, self.max_children)
            for i in range(0, len(self.points), m)
        ]

    def _split_internal(self) -> list[_Node]:
        centroids = [c.centroid for c in self.children]
        variances = [
            statistics.variance(p.coordinate(d) for p in centroids) if len(centroids) > 1 else 0
            for d in range(self.dimensionality)
        ]
        split_dim = variances.index(max(variances))
        self.children.sort(key=lambda c: c.centroid.coordinate(split_dim))
        m = math.ceil(len(self.children) / self.max_children)
        return [
            _Node.create_internal(self.children[i:i + m], self.dimensionality, self.max_children)
            for i in range(0, len(self.children), m)
        ]

    def _update_stats(self) -> None:
        if self.is_leaf:
            self.size = len(self.points)
            if self.size == 0:
                self.centroid, self.radius, self.sum_of_coords = None, 0.0, None
                return
            k = self.points[0].dimensionality
            self.sum_of_coords = tuple(
                sum(p.coordinate(d) for p in self.points) for d in range(k)
            )
            self.centroid = Point(tuple(c / self.size for c in self.sum_of_coords))
            self.radius = max(p.distance_to(self.centroid) for p in self.points)
        else:
            valid = [c for c in self.children if c.sum_of_coords is not None]
            if not valid:
                self.size, self.centroid, self.radius, self.sum_of_coords = 0, None, 0.0, None
                return
            self.size = sum(c.size for c in valid)
            k = valid[0].dimensionality
            self.sum_of_coords = tuple(
                sum(coords) for coords in zip(*(c.sum_of_coords for c in valid))
            )
            self.centroid = Point(tuple(c / self.size for c in self.sum_of_coords))
            self.radius = max(c.centroid.distance_to(self.centroid) + c.radius for c in valid)

    def contains(self, point: Point) -> bool:
        if self.centroid is None or point.distance_to(self.centroid) > self.radius + _EPSILON:
            return False
        if self.is_leaf:
            return point in self.points
        return any(child.contains(point) for child in self.children)

    def nearest_neighbour(self, target: Point) -> Optional[Tuple[Point, float]]:
        """
        Búsqueda de vecino más cercano usando poda por esferas.
        Devuelve (Point, distancia_al_cuadrado) o None.
        """
        heap: list[tuple[float, _Node]] = [(0.0, self)]
        best_p, best_ds = None, float('inf')

        while heap:
            lb, node = heapq.heappop(heap)
            if lb >= best_ds:
                continue
            if node.is_leaf:
                for p in node.points:
                    ds = target.distance_sq_to(p)
                    if ds < best_ds:
                        best_ds, best_p = ds, p
            else:
                for child in node.children:
                    if child.centroid is None:
                        continue
                    lb_child = max(0.0, target.distance_sq_to(child.centroid) - child.radius**2)
                    if lb_child < best_ds:
                        heapq.heappush(heap, (lb_child, child))

        return (best_p, best_ds) if best_p is not None else None

if __name__ == "__main__":
    # Creamos algunos puntos de ejemplo en 2D
    pts = [
        Point((1.0, 2.0)),
        Point((3.5, -1.0)),
        Point((0.0, 0.0)),
        Point((2.2, 2.2)),
        Point((-1.0, 4.0))
    ]
    tree = SsTree(pts, max_children=3)

    # Añadimos un nuevo punto
    nuevo = Point((1.1, 2.1))
    tree.add(nuevo)

    # Mostramos info del árbol
    print(tree)  # p.ej. SsTree(dimensionality=2, size=6, height=3)

    # Buscamos el vecino más cercano de un punto objetivo
    objetivo = Point((1.0, 1.0))
    resultado = tree.nearest_neighbour(objetivo)
    if resultado:
        vecino, distancia = resultado
        print(f"Vecino más cercano a {objetivo._coords}: {vecino._coords} a distancia {distancia:.4f}")
    else:
        print("No se encontró ningún vecino.")

