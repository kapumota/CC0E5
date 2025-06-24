from __future__ import annotations
from dataclasses import dataclass, field
from math import ceil, sqrt
from typing import List, Optional, Tuple, Union, Any, Generator
import json
import bisect

@dataclass(frozen=True, slots=True)
class Point:
    """
    Representa un punto en un espacio de dimensión arbitraria.
    Los puntos son inmutables y almacenan una tupla de coordenadas.
    """
    coords: Tuple[float, ...]

    def distance_sq(self, other: Point) -> float:
        """
        Calcula la distancia al cuadrado entre este punto y otro.
        Comprueba que ambas coordenadas tengan la misma dimensión.
        """
        if len(self.coords) != len(other.coords):
            raise ValueError("Dimensión de puntos incompatible")
        return sum((a - b) ** 2 for a, b in zip(self.coords, other.coords))

    @staticmethod
    def centroid(points: List[Point]) -> Point:
        """
        Calcula el centroide (promedio) de una lista de puntos.
        """
        dim = len(points[0].coords)
        sums = [0.0] * dim
        n = len(points)
        # Sumar coordenadas por dimensión
        for p in points:
            for i, v in enumerate(p.coords):
                sums[i] += v
        # Dividir entre el número de puntos
        return Point(tuple(s / n for s in sums))

@dataclass
class _Node:
    """
    Estructura de nodo interna de SsPlusTree.
    Puede ser hoja (contiene puntos) o nodo interno (contiene hijos).
    Mantiene estadísticas: centroide, radio al cuadrado y tamaño.
    """
    centroid: Point       # Centroide del nodo
    radius_sq: float      # Radio (al cuadrado) que engloba todos los puntos/hijos
    size: int             # Número total de puntos en este subárbol
    is_leaf: bool         # Indica si es hoja
    points: Optional[List[Point]] = None      # Lista de puntos si es hoja
    children: Optional[List[_Node]] = None    # Lista de nodos hijos si no es hoja

    @classmethod
    def create_leaf(cls, pts: List[Point]) -> _Node:
        """
        Crea un nodo hoja a partir de una lista de puntos,
        calcula su centroide y radio.
        """
        cent = Point.centroid(pts)
        radius = max(p.distance_sq(cent) for p in pts) if pts else 0.0
        return cls(centroid=cent, radius_sq=radius, size=len(pts), is_leaf=True, points=list(pts))

    @classmethod
    def create_internal(cls, children: List[_Node]) -> _Node:
        """
        Crea un nodo interno a partir de una lista de nodos hijos,
        calcula su centroide ponderado y radio.
        """
        n = sum(c.size for c in children)
        dims = len(children[0].centroid.coords)
        sums = [0.0] * dims
        # Sumar centroides ponderados
        for c in children:
            for i, v in enumerate(c.centroid.coords):
                sums[i] += v * c.size
        cent = Point(tuple(s / n for s in sums))
        radius = max(c.centroid.distance_sq(cent) + c.radius_sq for c in children)
        return cls(centroid=cent, radius_sq=radius, size=n, is_leaf=False, children=list(children))

    def to_dict(self) -> dict:
        """
        Serializa el nodo a un diccionario para JSON.
        """
        if self.is_leaf:
            return {
                'leaf': [p.coords for p in self.points],
                'centroid': self.centroid.coords,
                'radius_sq': self.radius_sq,
                'size': self.size
            }
        return {
            'children': [c.to_dict() for c in self.children],
            'centroid': self.centroid.coords,
            'radius_sq': self.radius_sq,
            'size': self.size
        }

    @staticmethod
    def from_dict(data: dict) -> _Node:
        """
        Reconstruye un nodo a partir de un diccionario (JSON).
        """
        if 'leaf' in data:
            pts = [Point(tuple(c)) for c in data['leaf']]
            node = _Node.create_leaf(pts)
        else:
            children = [_Node.from_dict(c) for c in data['children']]
            node = _Node.create_internal(children)
        # Ajustar campos para exactitud
        object.__setattr__(node, 'centroid', Point(tuple(data['centroid'])))
        object.__setattr__(node, 'radius_sq', data['radius_sq'])
        object.__setattr__(node, 'size', data['size'])
        return node

class SsPlusTree:
    """
    Estructura principal SS⁺-Tree.
    Ofrece inserción, eliminación, k-NN, persistencia y serialización.
    """
    def __init__(
        self,
        dim: int,
        max_children: int = 8,
        use_variance_split: bool = True
    ):
        # Dimensión de puntos
        self.dim = dim
        # Máximo de elementos hijos o puntos por nodo
        self.max_children = max_children
        # Usar heurística de varianza en splits
        self.use_variance_split = use_variance_split
        self.root: Optional[_Node] = None
        # Conjunto para prevenir duplicados
        self._points_set: set[Tuple[float, ...]] = set()

    def add(self, pt: Point) -> bool:
        """
        Inserta un punto en el árbol.
        Retorna False si ya existe (duplicado) o True si se añade.
        """
        if len(pt.coords) != self.dim:
            raise ValueError("Dimensión de punto inválida")
        key = tuple(pt.coords)
        if key in self._points_set:
            return False
        self._points_set.add(key)
        # Si está vacío, crear raíz hoja
        if self.root is None:
            self.root = _Node.create_leaf([pt])
        else:
            self._insert(self.root, pt)
            # Si la raíz excede tamaño, dividirla
            if self.root.size > self.max_children * self.max_children:
                self._split_root()
        return True

    def delete(self, pt: Point) -> bool:
        """
        Elimina un punto si existe.
        Retorna True si se elimina, False si no se encuentra.
        """
        if self.root is None or tuple(pt.coords) not in self._points_set:
            return False
        removed = self._delete(self.root, pt)
        if removed:
            self._points_set.remove(tuple(pt.coords))
        return removed

    def _delete(self, node: _Node, pt: Point) -> bool:
        """
        Método recursivo para eliminación.
        """
        if node.is_leaf:
            try:
                node.points.remove(pt)
                self._update_node(node)
                return True
            except ValueError:
                return False
        else:
            for child in node.children:
                # Comprobar si el punto puede estar en el subárbol
                if pt.distance_sq(child.centroid) <= child.radius_sq:
                    if self._delete(child, pt):
                        # Si el hijo quedó vacío, eliminar referencia
                        if child.size == 0:
                            node.children.remove(child)
                        self._update_node(node)
                        return True
            return False

    def knn(self, target: Point, k: int) -> List[Tuple[Point, float]]:
        """
        Retorna la lista de k vecinos más cercanos al punto target.
        Usa poda y heap de tamaño k.
        """
        heap: List[Tuple[float, Point]] = []  # max-heap vía distancias negativas
        def recurse(node: _Node):
            if node is None:
                return
            # Cota inferior de distancia
            dist_cent = target.distance_sq(node.centroid)
            lower = max(0.0, dist_cent - node.radius_sq)
            if len(heap) == k and lower >= -heap[0][0]:
                return
            if node.is_leaf:
                for p in node.points:
                    d = target.distance_sq(p)
                    if len(heap) < k:
                        bisect.insort(heap, (-d, p))
                    elif d < -heap[0][0]:
                        heap.pop(0)
                        bisect.insort(heap, (-d, p))
            else:
                # Recorrer hijos en orden heurístico
                for c in sorted(node.children, key=lambda c: max(0.0, target.distance_sq(c.centroid) - c.radius_sq)):
                    recurse(c)
        recurse(self.root)
        return [(p, sqrt(-d)) for d, p in sorted(heap, reverse=True)]

    def _insert(self, node: _Node, pt: Point) -> None:
        """
        Inserción recursiva con ajuste de estadísticas y splits.
        """
        if node.is_leaf:
            node.points.append(pt)
        else:
            # Elegir hijo que requiera mínima expansión
            best = min(node.children, key=lambda c: self._expansion(c, pt))
            self._insert(best, pt)
        self._update_node(node)
        # Dividir si excede capacidad
        if (node.is_leaf and len(node.points) > self.max_children) or (not node.is_leaf and len(node.children) > self.max_children):
            self._split(node)

    def _expansion(self, child: _Node, pt: Point) -> float:
        """
        Calcula cuánto debería crecer el radio de un nodo hijo para incluir pt.
        """
        d = pt.distance_sq(child.centroid)
        return max(0.0, d - child.radius_sq)

    def _update_node(self, node: _Node) -> None:
        """
        Recalcula centroide, radio y tamaño de un nodo.
        """
        if node.is_leaf:
            pts = node.points
            cent = Point.centroid(pts)
            rad = max(p.distance_sq(cent) for p in pts) if pts else 0.0
            object.__setattr__(node, 'centroid', cent)
            object.__setattr__(node, 'radius_sq', rad)
            object.__setattr__(node, 'size', len(pts))
        else:
            new = _Node.create_internal(node.children)
            object.__setattr__(node, 'centroid', new.centroid)
            object.__setattr__(node, 'radius_sq', new.radius_sq)
            object.__setattr__(node, 'size', new.size)

    def _split(self, node: _Node) -> None:
        """
        Realiza el split de un nodo en grupos basados en fan-out.
        """
        items = node.points if node.is_leaf else node.children
        groups = self._split_groups(items)
        if node.is_leaf:
            # Convertir hoja en nodo interno
            object.__setattr__(node, 'is_leaf', False)
            object.__setattr__(node, 'children', [_Node.create_leaf(g) for g in groups])
            object.__setattr__(node, 'points', None)
        else:
            object.__setattr__(node, 'children', [_Node.create_internal(g) for g in groups])
        self._update_node(node)

    def _split_groups(self, items: List[Any]) -> List[List[Any]]:
        """
        Agrupa elementos para split, el tamaño de cada grupo
        se basa en max_children y heurística opcional.
        """
        n = len(items)
        k = ceil(n / self.max_children)
        if isinstance(items[0], Point) or not self.use_variance_split:
            keyfn = lambda x: x.coords[0] if isinstance(x, Point) else x.centroid.coords[0]
        else:
            coords = [p.coords if isinstance(p, Point) else p.centroid.coords for p in items]
            dims = len(coords[0])
            vars = []
            for i in range(dims):
                mean = sum(c[i] for c in coords) / n
                vars.append(sum((c[i] - mean) ** 2 for c in coords) / n)
            dim_idx = vars.index(max(vars))
            keyfn = lambda x: x.coords[dim_idx] if isinstance(x, Point) else x.centroid.coords[dim_idx]
        items.sort(key=keyfn)
        size = ceil(n / k)
        return [items[i:i+size] for i in range(0, n, size)]

    def _split_root(self) -> None:
        """
        Divide la raíz cuando excede la capacidad máxima permitida.
        """
        root = self.root
        items = root.points if root.is_leaf else root.children
        groups = self._split_groups(items)
        children = []
        for g in groups:
            if isinstance(g[0], Point):
                children.append(_Node.create_leaf(g))
            else:
                children.append(_Node.create_internal(g))
        self.root = _Node.create_internal(children)

    def nearest(self, target: Point) -> Optional[Tuple[Point, float]]:
        """
        Busca el punto más cercano a target.
        """
        if self.root is None:
            return None
        best: Tuple[Optional[Point], float] = (None, float('inf'))
        def recurse(node: _Node):
            nonlocal best
            d_cent = target.distance_sq(node.centroid)
            lower = max(0.0, d_cent - node.radius_sq)
            if lower >= best[1]:
                return
            if node.is_leaf:
                for p in node.points:
                    d = target.distance_sq(p)
                    if d < best[1]:
                        best = (p, d)
            else:
                for c in sorted(node.children, key=lambda c: max(0.0, target.distance_sq(c.centroid)-c.radius_sq)):
                    recurse(c)
        recurse(self.root)
        return (best[0], sqrt(best[1])) if best[0] else None

    def to_json(self) -> str:
        """
        Serializa el árbol completo a JSON.
        """
        return json.dumps(self.root.to_dict()) if self.root else 'null'

    @staticmethod
    def from_json(data: str) -> SsPlusTree:
        """
        Reconstruye un árbol desde un string JSON.
        """
        obj = json.loads(data)
        if obj is None:
            return SsPlusTree(0)
        root = _Node.from_dict(obj)
        tree = SsPlusTree(len(root.centroid.coords))
        tree.root = root
        tree._points_set = set(tree._gather_points(root))
        return tree

    def _gather_points(self, node: _Node) -> Generator[Tuple[float, ...], None, None]:
        """
        Generador interno para recolectar todas las coordenadas de puntos.
        """
        if node.is_leaf:
            for p in node.points:
                yield tuple(p.coords)
        else:
            for c in node.children:
                yield from self._gather_points(c)

    def save(self, filepath: str) -> None:
        """
        Guarda el árbol en un archivo JSON.
        """
        with open(filepath, 'w') as f:
            f.write(self.to_json())

    @staticmethod
    def load(filepath: str) -> SsPlusTree:
        """
        Carga un árbol desde un archivo JSON.
        """
        with open(filepath, 'r') as f:
            data = f.read()
        return SsPlusTree.from_json(data)

# Ejemplos de uso:
# tree = SsPlusTree(dim=2)
# tree.add(Point((1,2)))
# tree.delete(Point((1,2)))
# vecinos = tree.knn(Point((0,0)), k=5)
# tree.save('tree.json')
# cargado = SsPlusTree.load('tree.json')

