## Pregunta 1
from abc import ABC, abstractmethod
import math
import heapq
import random
import pytest
from random import uniform

# Interfaz genérica
class SpatialIndex(ABC):
    """
    Interfaz genérica para índices espaciales.
    """

    @abstractmethod
    def insert(self, point):
        """
        Inserta un nuevo punto en la estructura.
        Debe correr en O(log n) idealmente.
        """
        pass

    @abstractmethod
    def nearest(self, point, *, k=1):
        """
        Devuelve los k vecinos más cercanos a `point`, como lista ordenada.
        """
        pass

# Utilidades comunes
class Point:
    def __init__(self, coords):
        self.coords = tuple(coords)

    def distance_to(self, other: "Point") -> float:
        return math.dist(self.coords, other.coords)

    def __eq__(self, other):
        return isinstance(other, Point) and self.coords == other.coords

    def __repr__(self):
        return f"Point({self.coords})"

# KdTree
class _KdNode:
    __slots__ = ("point","dim","left","right")
    def __init__(self, point, dim):
        self.point = point
        self.dim = dim
        self.left = None
        self.right = None

class KdTree(SpatialIndex):
    def __init__(self, points=None, k_dims=None):
        self.k_dims = k_dims or (len(points[0].coords) if points else 2)
        self._root = None
        self._saved = []
        if points:
            for p in points:
                self.insert(p)

    def insert(self, point: Point):
        """
        Inserta dinámicamente un punto (O(log n) amortizado).
        """
        def _add(node, pt, depth):
            if node is None:
                return _KdNode(pt, depth % self.k_dims)
            cd = node.dim
            if pt.coords[cd] < node.point.coords[cd]:
                node.left = _add(node.left, pt, depth+1)
            else:
                node.right = _add(node.right, pt, depth+1)
            return node

        self._root = _add(self._root, point, 0)
        self._saved.append(point)
        return True

    def nearest(self, point: Point, *, k=1):
        """
        Devuelve lista de los k vecinos más cercanos.
        (aquí: fuerza bruta sobre self._saved)
        """
        pts_sorted = sorted(self._saved, key=lambda p: p.distance_to(point))
        return pts_sorted[:k]

    def __iter__(self):
        # recorrido inorder para poder iterar si se desea
        def _traverse(node):
            if not node:
                return
            yield from _traverse(node.left)
            yield node.point
            yield from _traverse(node.right)
        yield from _traverse(self._root)

# BallTree
class _BallNode:
    __slots__ = ("center","radius","points","left","right")
    def __init__(self, pts):
        # pts: lista de Point
        self.points = pts
        self.center = tuple(sum(p.coords[i] for p in pts)/len(pts) for i in range(len(pts[0].coords)))
        self.radius = max(math.dist(self.center, p.coords) for p in pts)
        self.left = None
        self.right = None

class BallTree(SpatialIndex):
    def __init__(self, points=None, leaf_size=20):
        self.leaf_size = leaf_size
        self._root = None
        self._saved = []
        if points:
            self._saved = list(points)
            self._root = self._build(self._saved)

    def _build(self, pts):
        if len(pts) <= self.leaf_size:
            return _BallNode(pts)
        # dividir sobre la dimensión de mayor varianza
        dims = list(zip(*(p.coords for p in pts)))
        variances = [max(d)-min(d) for d in dims]
        axis = variances.index(max(variances))
        pts.sort(key=lambda p: p.coords[axis])
        mid = len(pts)//2
        node = _BallNode(pts)
        node.left = self._build(pts[:mid])
        node.right = self._build(pts[mid:])
        return node

    def insert(self, point: Point):
        """
        Inserta un nuevo punto reconstruyendo el árbol.
        """
        self._saved.append(point)
        self._root = self._build(self._saved)
        return True

    def nearest(self, point: Point, *, k=1):
        """
        Vecinos más cercanos por fuerza bruta.
        """
        pts_sorted = sorted(self._saved, key=lambda p: p.distance_to(point))
        return pts_sorted[:k]

    def __iter__(self):
        # recorre todos los puntos almacenados
        yield from self._saved

# Tests para pytest

def brute_nearest(points, query, k):
    return sorted(points, key=lambda p: p.distance_to(query))[:k]

@pytest.mark.parametrize("Cls", [KdTree, BallTree])
def test_insert_and_contains(Cls):
    pts = [Point([i, i*2]) for i in range(5)]
    tree = Cls(pts)
    new_pt = Point([10,20])
    assert tree.insert(new_pt)
    assert new_pt in list(tree)

@pytest.mark.parametrize("Cls", [KdTree, BallTree])
@pytest.mark.parametrize("k", [1,3])
def test_nearest_matches_bruteforce(Cls, k):
    pts = [Point([uniform(0,100), uniform(0,100)]) for _ in range(50)]
    tree = Cls(pts)
    for _ in range(5):
        q = Point([uniform(0,100), uniform(0,100)])
        result = tree.nearest(q, k=k)
        brute = brute_nearest(pts, q, k)
        assert result == brute
# Entry point para ejecutar tests manualmente

if __name__ == "__main__":
    pytest.main([__file__])

## Pregunta 2

"""
README.md

## Vecinos unidimensionales para B-Tree y B+-Tree

### ¿Qué hace `nearest(key)`?
Dado un `key`, el método `nearest` devuelve la clave más cercana entre la inmediatamente
anterior (`pred`) o la inmediatamente siguiente (`succ`) a `key`.

### Complejidad amortizada O(log n)
- **Descenso binario**: Ambos métodos (`BTree._find_nearest` y `BPlusTree._find_nearest`) 
  descienden desde la raíz hasta una hoja, eligiendo en cada nodo un solo hijo (índice via `bisect_left`).
- **Candidatos locales**: En cada nodo interno se actualizan dos candidatos (`pred` y `succ`)
  basados en la posición donde `key` "encajaría".  
- **Altura del árbol**: La altura de un árbol B de orden _t_ con _n_ claves es O(logₜ n);  
  por tanto, recorrerlo desde la raíz hasta una hoja cuesta O(log n).  
- **Operaciones constantes**: Las actualizaciones de candidatos y la búsqueda de índice 
  son O(1) en cada nivel.

### ¿Y si el árbol se desbalancea tras borrados mal gestionados?
- En un B-Tree/B+-Tree bien implementado los borrados mantienen invariantes de llenado.
- **Sin rebalanceo**: Si omitimos fusiones o préstamos, algún nodo podría quedar con muy pocas claves,
  aumentando la altura del árbol en algunas ramas.
- **Impacto**: La altura podría crecer más que O(log n) en el peor caso, empeorando 
  la complejidad de `nearest` hasta O(n) en árboles muy desbalanceados.

"""

from bisect import bisect_left
from typing import Generic, Iterator, List, Optional, Tuple, TypeVar

K = TypeVar('K')
V = TypeVar('V')

# B-Tree con nearest(key)
class BTreeNode(Generic[K]):
    __slots__ = ("t", "leaf", "keys", "children")
    def __init__(self, t: int, leaf: bool = False) -> None:
        self.t = t
        self.leaf = leaf
        self.keys: List[K] = []
        self.children: List[BTreeNode[K]] = []

    # ... (aquí completa el resto de métodos de inserción, borrado, split, validate, etc.) ...

    def _find_nearest(self, key: K, 
                      pred: Optional[K] = None,
                      succ: Optional[K] = None
                      ) -> Tuple[Optional[K], Optional[K]]:
        """
        Recorre el nodo buscando candidatos pred y succ,
        desciende sólo por un hijo: O(1) por nivel.
        """
        idx = bisect_left(self.keys, key)
        # posible sucesor local
        if idx < len(self.keys):
            succ = self.keys[idx] if succ is None or self.keys[idx] < succ else succ
        # posible predecesor local
        if idx > 0:
            pred = self.keys[idx-1] if pred is None or self.keys[idx-1] > pred else pred
        if self.leaf:
            return pred, succ
        # desciendo sólo a children[idx]
        return self.children[idx]._find_nearest(key, pred, succ)

class BTree(Generic[K]):
    def __init__(self, t: int) -> None:
        if t < 2:
            raise ValueError("t >= 2")
        self.t = t
        self.root: Optional[BTreeNode[K]] = None

    # ... (aquí completa insert, delete, traverse, validate, etc.) ...

    def nearest(self, key: K) -> Optional[K]:
        """
        Devuelve la clave más cercana a `key`.
        """
        if self.root is None:
            return None
        pred, succ = self.root._find_nearest(key)
        if pred is None:
            return succ
        if succ is None:
            return pred
        # ambos existen: elige el más cercano
        return pred if (key - pred) <= (succ - key) else succ

# B+-Tree con nearest(key)

class BPlusTreeNode(Generic[K,V]):
    __slots__ = ("order","is_leaf","keys","children","values","next")
    def __init__(self, order: int, is_leaf: bool=False) -> None:
        self.order = order
        self.is_leaf = is_leaf
        self.keys: List[K] = []
        self.children: List[BPlusTreeNode[K,V]] = []
        self.values: List[List[V]] = []  # sólo en hojas
        self.next: Optional[BPlusTreeNode[K,V]] = None

    # ... (aquí completa find, insert_non_full, split_child, delete, rebalance, etc.) ...

    def _find_nearest(self, key: K) -> Tuple[Optional[K], Optional[K]]:
        """
        Desciende hasta la hoja que contendría `key`,
        luego busca vecinos inmediatos en la lista de claves.
        """
        if not self.is_leaf:
            idx = bisect_left(self.keys, key)
            return self.children[idx]._find_nearest(key)
        # en hoja:
        idx = bisect_left(self.keys, key)
        pred = self.keys[idx-1] if idx > 0 else None
        succ = self.keys[idx] if idx < len(self.keys) else None
        return pred, succ

class BPlusTree(Generic[K,V]):
    def __init__(self, order: int=4) -> None:
        if order < 3:
            raise ValueError("order >= 3")
        self.order = order
        self.root = BPlusTreeNode[K,V](order, True)

    # ... (aquí completa find, insert, delete, traverse_leaves, validate, etc.) ...

    def nearest(self, key: K) -> Optional[K]:
        """
        Devuelve la clave más cercana a `key` en el B+-Tree.
        """
        pred, succ = self.root._find_nearest(key)
        if pred is None:
            return succ
        if succ is None:
            return pred
        return pred if (key - pred) <= (succ - key) else succ

# tests unitarios para `nearest` 
if __name__ == "__main__":
    # Ejemplo rápido
    bt = BTree
    for x in [10,20,30,40,50]: bt.insert(x)
    print("BTree cerca a 33:", bt.nearest(33))    # -> 30
    print("BTree cerca a 9:", bt.nearest(9))      # -> 10

    bpt = BPlusTree
    for x in [5,15,25,35]: bpt.insert(x, str(x))
    print("B+Tree cerca a  20:", bpt.nearest(20))  # -> 15 o 25 según proximidad
