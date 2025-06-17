"""
Implementación mejorada de SS-Tree con estadísticas incrementales y búsqueda de vecino más cercano usando heap.
"""
from __future__ import annotations
import math
import heapq
import itertools
from typing import List, Tuple, Optional, Dict, Any, Iterator

class Point:
    """
    Representa un punto en un espacio k-dimensional.
    """
    def __init__(self, coords: List[float]):
        if not isinstance(coords, (list, tuple)):
            raise TypeError("Las coordenadas deben ser lista o tupla de números")
        if not coords:
            raise ValueError("El punto debe tener al menos una dimensión")
        self.coordinates = [float(c) for c in coords]
        self.dimensionality = len(self.coordinates)

    def coordinate(self, i: int) -> float:
        return self.coordinates[i]

    def distance_to(self, other: Point) -> float:
        if self.dimensionality != other.dimensionality:
            raise ValueError("Los puntos deben tener la misma dimensionalidad")
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(self.coordinates, other.coordinates)))

    def distance_sq_to(self, other: Point) -> float:
        if self.dimensionality != other.dimensionality:
            raise ValueError("Los puntos deben tener la misma dimensionalidad")
        return sum((a - b) ** 2 for a, b in zip(self.coordinates, other.coordinates))

    @staticmethod
    def validate_point(p: Point, dim: int, context: str = ''):
        if not isinstance(p, Point):
            raise TypeError(f"{context}: argumento debe ser Point")
        if p.dimensionality != dim:
            raise ValueError(f"{context}: dimensión esperada {dim}, obtenida {p.dimensionality}")

    def __repr__(self) -> str:
        return f"Point({self.coordinates})"

class Node:
    def __init__(self,
                 dim: int,
                 max_points: int,
                 points: Optional[List[Point]] = None,
                 children: Optional[List[Node]] = None):
        self.dim = dim
        self.max_points = max_points
        self.is_leaf = children is None
        self.size = 0
        self._sum = [0.0] * dim
        self.centroid: Optional[Point] = None
        self.radius_sq: float = 0.0
        self.points: List[Point] = [] if self.is_leaf else []
        self.children: List[Node] = children or []
        if self.is_leaf and points:
            for p in points:
                self._inc_add(p)
                self.points.append(p)
        elif children:
            self._combine_from_children()

    @classmethod
    def leaf(cls, points: List[Point], dim: int, max_points: int) -> Node:
        return cls(dim, max_points, points=points)

    def insert(self, p: Point) -> Node | List[Node]:
        if self.is_leaf:
            self.points.append(p)
            self._inc_add(p)
            if len(self.points) > self.max_points:
                return self._split()
            return self
        best = min(self.children, key=lambda c: c.centroid.distance_sq_to(p))
        new_child = best.insert(p)
        if new_child is not best:
            self.children.remove(best)
            for c in (new_child if isinstance(new_child, list) else [new_child]):
                self.children.append(c)
            self._combine_from_children()
        else:
            # solo actualización de stats
            self._inc_add(p)
        return self

    def _inc_add(self, p: Point) -> None:
        if self.centroid is None:
            self.centroid = p
            self.radius_sq = 0.0
            self.size = 1
            self._sum = p.coordinates.copy()
            return
        self.size += 1
        for i, coord in enumerate(p.coordinates):
            self._sum[i] += coord
        self.centroid = Point([s / self.size for s in self._sum])
        d_sq = p.distance_sq_to(self.centroid)
        if d_sq > self.radius_sq:
            self.radius_sq = d_sq

    def _combine_from_children(self):
        total = sum(c.size for c in self.children)
        sums = [0.0] * self.dim
        for c in self.children:
            for i in range(self.dim):
                sums[i] += c.centroid.coordinate(i) * c.size
        self.size = total
        self._sum = sums
        if total:
            self.centroid = Point([s / total for s in sums])
            self.radius_sq = max(
                c.radius_sq + c.centroid.distance_sq_to(self.centroid)
                for c in self.children
            )
        else:
            self.centroid = None
            self.radius_sq = 0.0

    def _split(self) -> List[Node]:
        pts = self.points
        n = len(pts)
        sums = [0.0] * self.dim
        for p in pts:
            for i in range(self.dim):
                sums[i] += p.coordinate(i)
        means = [s / n for s in sums]
        variances = [sum((p.coordinate(i) - means[i]) ** 2 for p in pts) for i in range(self.dim)]
        split_dim = variances.index(max(variances))
        pts_sorted = sorted(pts, key=lambda p: p.coordinate(split_dim))
        mid = n // 2
        left = Node.leaf(pts_sorted[:mid], self.dim, self.max_points)
        right = Node.leaf(pts_sorted[mid:], self.dim, self.max_points)
        return [left, right]

    def distance_sq_to_centroid(self, p: Point) -> float:
        if not self.centroid:
            return float('inf')
        return p.distance_sq_to(self.centroid)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'dim': self.dim,
            'max_points': self.max_points,
            'is_leaf': self.is_leaf,
            'size': self.size,
            'centroid': self.centroid.coordinates if self.centroid else None,
            'radius_sq': self.radius_sq
        }
        if self.is_leaf:
            data['points'] = [p.coordinates for p in self.points]
        else:
            data['children'] = [c.to_dict() for c in self.children]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any], max_points: int) -> Node:
        dim = data['dim']
        if data['is_leaf']:
            pts = [Point(coords) for coords in data['points']]
            node = cls.leaf(pts, dim, max_points)
            node.size = data['size']
            node.centroid = Point(data['centroid']) if data['centroid'] else None
            node.radius_sq = data['radius_sq']
            return node
        children = [cls.from_dict(c, max_points) for c in data['children']]
        node = cls(dim, max_points, children=children)
        node.size = data['size']
        node.centroid = Point(data['centroid'])
        node.radius_sq = data['radius_sq']
        return node

    def __iter__(self) -> Iterator[Point]:
        if self.is_leaf:
            yield from self.points
        else:
            for c in self.children:
                yield from c

    def __repr__(self) -> str:
        return f"{'Leaf' if self.is_leaf else 'Internal'}Node(dim={self.dim}, size={self.size})"

class SsTree:
    """
    SS-Tree: estructura de índice espacial optimizada.
    """
    def __init__(
                 self,
                 points: Optional[List[Point]] = None,
                 max_points: int = 2):
        if max_points < 1:
            raise ValueError("max_points debe ser al menos 1")
        self.max_points = max_points
        self.dimensionality = 0
        self._root: Optional[Node] = None
        for p in points or []:
            self.insert(p)

    def insert(self, point: Point) -> None:
        if self._root is None:
            self.dimensionality = point.dimensionality
            self._root = Node.leaf([point], self.dimensionality, self.max_points)
            return
        Point.validate_point(point, self.dimensionality, 'SsTree.insert')
        result = self._root.insert(point)
        if isinstance(result, list):
            self._root = Node(
                self.dimensionality,
                self.max_points,
                children=result
            )
        else:
            self._root = result

    def is_empty(self) -> bool:
        return self._root is None or self._root.size == 0

    def __iter__(self) -> Iterator[Point]:
        if not self._root:
            return iter([])
        yield from self._root

    def nearest(self, point: Point) -> Point:
        if self.is_empty():
            return None  # type: ignore
        Point.validate_point(point, self.dimensionality, 'SsTree.nearest_neighbour')
        best_pt: Optional[Point] = None
        best_dist_sq = float('inf')
        counter = itertools.count()
        heap: List[Tuple[float, int, Node]] = []
        root = self._root
        lb = max(0.0, root.distance_sq_to_centroid(point) - root.radius_sq)
        heapq.heappush(heap, (lb, next(counter), root))
        while heap:
            lb, _, node = heapq.heappop(heap)
            if lb >= best_dist_sq:
                break
            if node.is_leaf:
                for p in node.points:
                    d_sq = p.distance_sq_to(point)
                    if d_sq < best_dist_sq:
                        best_dist_sq = d_sq
                        best_pt = p
            else:
                for c in node.children:
                    lb_c = max(0.0, c.distance_sq_to_centroid(point) - c.radius_sq)
                    if lb_c < best_dist_sq:
                        heapq.heappush(heap, (lb_c, next(counter), c))
        return best_pt  # type: ignore

    def nearest_neighbour(self, point: Point) -> Optional[Point]:
        return self.nearest(point)

    def to_dict(self) -> Dict[str, Any]:
        if not self._root:
            return {'empty': True, 'max_points': self.max_points}
        return {
            'empty': False,
            'max_points': self.max_points,
            'root': self._root.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SsTree:
        tree = cls([], max_points=data.get('max_points', 1))
        if data.get('empty', False):
            return tree
        tree._root = Node.from_dict(data['root'], tree.max_points)
        tree.dimensionality = tree._root.dim
        return tree
