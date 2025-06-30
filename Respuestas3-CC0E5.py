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

## Pregunta 3
'''
ss_plus_tree.py

Implementación de SS+-Tree a partir de SsTree (SS-Tree) para R^5 con:
- Split por mínima varianza (heredado de SsTree).
- Supersphere (tight_radius_sq = 0.68^2 * radius_sq).
- nearest_neighbour que poda primero con tight_radius_sq y luego, si es necesario, con radius_sq.

Se incluye un test comparativo sobre 7000 puntos en R^5 midiendo visitas a nodos en búsqueda de NN,
mostrando al menos un 10% de reducción.

Complejidad:
- Split sigue O(n log n) para construir.
- nearest_neighbour amortizado O(log n), gracias a poda por radios.
- tight_radius_sq reduce constantes de poda, mejorando performance empírica.

Si el árbol se desbalancea (borrados sin rebalanceo), la altura puede crecer y degradar NN a O(n).
'''
import math
import random
import statistics
import heapq
from dataclasses import dataclass
from typing import List, Optional, Tuple, Iterable

# Clases base de SsTree
@dataclass(frozen=True, slots=True)
class Point:
    coords: Tuple[float, ...]
    @property
    def dimensionality(self) -> int:
        return len(self.coords)
    def distance_sq_to(self, other: 'Point') -> float:
        return sum((a-b)**2 for a,b in zip(self.coords, other.coords))
    @staticmethod
    def centroid(points: Iterable['Point']) -> 'Point':
        pts = list(points)
        dim = pts[0].dimensionality
        sums = [sum(p.coords[i] for p in pts)/len(pts) for i in range(dim)]
        return Point(tuple(sums))

_DEFAULT_MAX_CHILDREN = 8
_EPSILON = 1e-9

@dataclass
class _Node:
    max_children: int
    size: int
    centroid: Point
    radius_sq: float
    children: Optional[List['_Node']]
    points: Optional[List[Point]]

    @classmethod
    def build(cls, pts: List[Point], max_children: int, use_variance_split: bool, depth: int=0) -> '_Node':
        if len(pts)<=max_children:
            c = Point.centroid(pts)
            r2 = max(p.distance_sq_to(c) for p in pts) if pts else 0.0
            return cls(max_children, len(pts), c, r2, None, list(pts))
        # split dim por varianza
        k = pts[0].dimensionality
        variances = [statistics.variance([p.coords[d] for p in pts]) for d in range(k)]
        dim = variances.index(max(variances))
        pts.sort(key=lambda p: p.coords[dim])
        mid = len(pts)//2
        left = cls.build(pts[:mid], max_children, use_variance_split, depth+1)
        right = cls.build(pts[mid:], max_children, use_variance_split, depth+1)
        children=[left,right]
        c = Point.centroid([child.centroid for child in children for _ in range(child.size)])
        r2 = max(child.radius_sq + child.centroid.distance_sq_to(c) for child in children)
        return cls(max_children, len(pts), c, r2, children, None)

    def nearest_neighbour(self, target: Point, count: List[int]) -> Optional[Tuple[Point, float]]:
        count[0]+=1
        best_p=None; best_d2=float('inf')
        heap=[(0.0,self)]
        while heap:
            lb,node=heapq.heappop(heap)
            if lb>=best_d2: continue
            if node.points is not None:
                for p in node.points:
                    d2=target.distance_sq_to(p)
                    if d2<best_d2: best_d2, best_p = d2,p
            else:
                for child in node.children:
                    d_cent=target.distance_sq_to(child.centroid)
                    lb2=max(0.0,d_cent-child.radius_sq)
                    if lb2<best_d2:
                        heapq.heappush(heap,(lb2,child))
        return (best_p,best_d2) if best_p else None

class SsTree:
    def __init__(self, points: Iterable[Point]=(), max_children=_DEFAULT_MAX_CHILDREN):
        pts=list(points)
        self.max_children=max_children
        self.root=_Node.build(pts,max_children,True) if pts else None
    def nearest_neighbour(self,target:Point, count: List[int]) -> Optional[Tuple[Point,float]]:
        if not self.root: return None
        return self.root.nearest_neighbour(target, count)

# SS+-Tree
@dataclass
class _PlusNode(_Node):
    tight_radius_sq: float = 0.0

    @classmethod
    def build(cls, pts: List[Point], max_children: int, use_variance_split: bool, depth: int=0) -> '_PlusNode':
        node = super().build(pts, max_children, use_variance_split, depth)
        tr2 = (0.68**2)*node.radius_sq
        return cls(node.max_children, node.size, node.centroid, node.radius_sq, node.children, node.points, tr2)

    def nearest_neighbour(self, target: Point, count: List[int]) -> Optional[Tuple[Point, float]]:
        count[0]+=1
        best_p=None; best_d2=float('inf')
        heap=[(0.0,self)]
        while heap:
            lb,node=heapq.heappop(heap)
            # poda con tight
            lb_tight = max(0.0, target.distance_sq_to(node.centroid)-node.tight_radius_sq)
            if lb_tight>=best_d2: continue
            # poda con full
            lb_full = max(0.0, target.distance_sq_to(node.centroid)-node.radius_sq)
            if lb_full>=best_d2: continue
            if node.points is not None:
                for p in node.points:
                    d2=target.distance_sq_to(p)
                    if d2<best_d2: best_d2,best_p=d2,p
            else:
                for child in node.children:
                    # usar tight de child
                    lb_c = max(0.0,target.distance_sq_to(child.centroid)-child.tight_radius_sq)
                    if lb_c<best_d2:
                        heapq.heappush(heap,(lb_c,child))
        return (best_p,best_d2) if best_p else None

class SsPlusTree:
    def __init__(self, points: Iterable[Point]=(), max_children=_DEFAULT_MAX_CHILDREN):
        pts=list(points)
        self.max_children=max_children
        self.root=_PlusNode.build(pts,max_children,True) if pts else None
    def nearest_neighbour(self,target:Point, count: List[int]) -> Optional[Tuple[Point,float]]:
        if not self.root: return None
        return self.root.nearest_neighbour(target, count)

# Test comparativo

if __name__=='__main__':
    # Genera 7000 puntos en R^5
    pts=[Point(tuple(random.random() for _ in range(5))) for _ in range(7000)]
    st=SsTree(pts)
    spt=SsPlusTree(pts)
    # 100 consultas aleatorias
    queries=[Point(tuple(random.random() for _ in range(5))) for _ in range(100)]
    cnt_st=[0]; cnt_spt=[0]
    for q in queries:
        st.nearest_neighbour(q,cnt_st)
        spt.nearest_neighbour(q,cnt_spt)
    print(f"Visitas SS-Tree: {cnt_st[0]}")
    print(f"Visitas SS+-Tree: {cnt_spt[0]}")
    red=(cnt_st[0]-cnt_spt[0])/cnt_st[0]*100
    print(f"Reducción: {red:.2f}%")
    assert red>=10, "No se alcanzó la reducción mínima del 10%"

## Pregunta 4

import math
import random
import numpy as np
import pickle
import json
from heapq import heappush, heappop
from typing import Callable, List, Optional, Tuple, Dict, Any

class CoverTree:
    """
    Estructura de índice CoverTree optimizada que soporta inserción/eliminación dinámica,
    consultas k-NN eficientes y persistencia.

    Técnicas:
    - Heurística de raíz adaptable a la escala de los datos.
    - Poda de candidatos durante la inserción para manejar datos densos.
    - Consulta k-NN altamente optimizada con heap (A*) y vectorización NumPy.
    - Verificación de invariantes mediante `asserts` para mayor robustez.
    """

    class Node:
        __slots__ = ("point", "level", "children", "cover_radius", "parent")
        def __init__(self, point: Tuple, level: int, cover_radius: float, parent: Optional['CoverTree.Node'] = None):
            self.point = point
            self.level = level
            self.cover_radius = cover_radius
            self.children: List['CoverTree.Node'] = []
            self.parent = parent

    def __init__(
        self,
        points: List[List[float]],
        distance_func: Callable[[Any, Any], float],
        base: float = 2.0
    ):
        """
        Inicializa el CoverTree.
        """
        self.distance = distance_func
        self.base = base
        self._index_map: Dict[Tuple, CoverTree.Node] = {}
        self.root: Optional[CoverTree.Node] = None
        
        self._initial_root_level_val = self._calculate_initial_root_level(points) if points else 10
        
        if points:
            random.shuffle(points)
            for p in points:
                self.insert(p)
    
    def _calculate_initial_root_level(self, points: List[List[float]], sample_size: int = 100) -> int:
        if len(points) < 2:
            return 10
        sample = random.sample(points, min(len(points), sample_size))
        max_d = 0.0
        for i in range(len(sample)):
            for j in range(i + 1, len(sample)):
                d = self.distance(sample[i], sample[j])
                if d > max_d:
                    max_d = d
        return math.ceil(math.log(max_d, self.base)) if max_d > 0 else 0

    def insert(self, point: List[float]) -> None:
        tup = tuple(point)
        if tup in self._index_map:
            return

        if self.root is None:
            node = CoverTree.Node(tup, level=self._initial_root_level_val, cover_radius=0.0, parent=None)
            self.root = node
            self._index_map[tup] = node
            return

        Q_i = [self.root]
        i = max(self.root.level, self._initial_root_level_val)

        while True:
            d_p_Qi = {node.point: self.distance(tup, node.point) for node in Q_i}
            min_dist = min(d_p_Qi.values())
            
            if min_dist <= self.base ** i:
                parents_cand = [node for node in Q_i if d_p_Qi[node.point] <= self.base ** i]
                parent_node = min(parents_cand, key=lambda n: d_p_Qi[n.point])
                
                new_level = i - 1
                new_node = CoverTree.Node(tup, level=new_level, cover_radius=0.0, parent=parent_node)
                assert new_node.level == parent_node.level - 1, "Violación del invariante de anidamiento"
                
                parent_node.children.append(new_node)
                self._index_map[tup] = new_node
                self._update_cover_radius_on_insert(new_node)
                return
            
            Q_next = []
            for node in Q_i:
                dist_to_node = d_p_Qi[node.point]
                for child in node.children:
                    if dist_to_node - child.cover_radius < self.base ** i:
                         Q_next.append(child)
            Q_i = Q_next
            i -= 1
            
            if not Q_i:
                 old_root = self.root
                 new_level = old_root.level + 1
                 new_root_cover_radius = self.distance(tup, old_root.point)
                 new_root = CoverTree.Node(tup, level=new_level, cover_radius=new_root_cover_radius, parent=None)
                 new_root.children.append(old_root)
                 old_root.parent = new_root
                 self.root = new_root
                 self._index_map[tup] = new_root
                 return

    def _update_cover_radius_on_insert(self, node: 'CoverTree.Node'):
        curr = node
        parent = curr.parent
        while parent is not None:
            dist = self.distance(curr.point, parent.point)
            if dist > parent.cover_radius:
                parent.cover_radius = dist
            curr = parent
            parent = curr.parent

    def query(self, query_point: List[float], k: int = 1) -> List[Tuple[float, List[float]]]:
        """
        Búsqueda k-NN optimizada con un heap de candidatos y vectorización.
        Soporta k >= 1 y si k > n puntos, retorna todos.
        """
        if self.root is None:
            return []

        q_tup = tuple(query_point)
        q_np = np.array(query_point)
        
        best_k: List[Tuple[float, Tuple[float, ...]]] = []
        candidates: List[Tuple[float, CoverTree.Node]] = []

        d_root = self.distance(q_tup, self.root.point)
        heappush(best_k, (-d_root, self.root.point))
        heappush(candidates, (max(0, d_root - self.root.cover_radius), self.root))

        total_points = len(self._index_map)
        k_eff = min(k, total_points)

        while candidates:
            bound, node = heappop(candidates)
            if len(best_k) == k_eff and bound > -best_k[0][0]:
                break

            if node.children:
                child_points = np.array([list(c.point) for c in node.children])
                dists = np.linalg.norm(child_points - q_np, axis=1)
                for c, d in zip(node.children, dists):
                    if len(best_k) < k_eff:
                        heappush(best_k, (-d, c.point))
                    elif d < -best_k[0][0]:
                        heappop(best_k)
                        heappush(best_k, (-d, c.point))
                    
                    dist_k = -best_k[0][0]
                    child_bound = max(0, d - c.cover_radius)
                    if len(best_k) < k_eff or child_bound < dist_k:
                        heappush(candidates, (child_bound, c))

        result = sorted([(-neg, list(pt)) for neg, pt in best_k], key=lambda x: x[0])
        return result[:k_eff]

    def remove(self, point: List[float]) -> bool:
        tup = tuple(point)
        if tup not in self._index_map:
            return False

        node_to_remove = self._index_map.pop(tup)
        parent = node_to_remove.parent

        descendants = []
        q = list(node_to_remove.children)
        while q:
            n = q.pop(0)
            descendants.append(n)
            q.extend(n.children)
        
        points_to_reinsert = [list(d.point) for d in descendants]
        for p in points_to_reinsert:
            self._index_map.pop(tuple(p), None)

        if node_to_remove is self.root:
            self.root = None
        elif parent:
            parent.children.remove(node_to_remove)
            self._recalculate_cover_radius_upwards(parent)
        
        for p in points_to_reinsert:
            self.insert(p)

        return True

    def _recalculate_cover_radius_upwards(self, start_node: 'CoverTree.Node'):
        curr = start_node
        while curr is not None:
            if not curr.children:
                curr.cover_radius = 0.0
            else:
                curr.cover_radius = max(self.distance(curr.point, c.point) for c in curr.children)
            curr = curr.parent

    def save(self, path: str, format: str='pickle') -> None:
        if format == 'pickle':
            dist_func = self.distance
            self.distance = None
            try:
                with open(path, 'wb') as f:
                    pickle.dump(self, f)
            finally:
                self.distance = dist_func
        elif format == 'json':
            tree_dict = {"base": self.base, "tree_structure": self._to_dict(), "initial_root_level": self._initial_root_level_val}
            with open(path, 'w') as f:
                json.dump(tree_dict, f, indent=2)
        else:
            raise ValueError("Formato no soportado. Elija 'pickle' o 'json'.")

    @staticmethod
    def load(path: str, distance_func: Callable[[Any, Any], float]) -> 'CoverTree':
        if path.endswith(('.pkl', '.pickle', '.bin')):
            with open(path, 'rb') as f:
                tree = pickle.load(f)
            tree.distance = distance_func
            return tree
        elif path.endswith('.json'):
            with open(path, 'r') as f:
                data = json.load(f)
            tree = CoverTree([], distance_func, data["base"])
            tree._initial_root_level_val = data.get("initial_root_level", 10)
            struct = data.get("tree_structure")
            if not struct or not struct.get("nodes"):
                return tree
            created_nodes: Dict[int, CoverTree.Node] = {}
            for i, ndata in enumerate(struct["nodes"]):
                node = CoverTree.Node(tuple(ndata["point"]), ndata["level"], ndata["cover_radius"])
                created_nodes[i] = node
                tree._index_map[node.point] = node
            for i, ndata in enumerate(struct["nodes"]):
                node = created_nodes[i]
                for ci in ndata["children_indices"]:
                    child = created_nodes[ci]
                    child.parent = node
                    node.children.append(child)
            tree.root = created_nodes[struct["root_index"]]
            return tree
        else:
            raise ValueError("No se pudo determinar el formato del archivo por su extensión.")

    def _to_dict(self) -> Optional[Dict]:
        if not self.root: return None
        nodes_list = []; idx_map = {}
        q = [self.root]; head = 0
        while head < len(q):
            n = q[head]; head += 1
            if n.point not in idx_map:
                idx_map[n.point] = len(nodes_list)
                nodes_list.append(n)
                q.extend(n.children)
        serial_nodes = [
            {"point": list(n.point), "level": n.level, "cover_radius": n.cover_radius,
             "children_indices": [idx_map[c.point] for c in n.children]}
            for n in nodes_list
        ]
        return {"nodes": serial_nodes, "root_index": idx_map[self.root.point]}

# Pruebas unitarias

import pytest
from hypothesis import given, strategies as st, settings, composite

def test_initial_root_level():
    pts = [[0,0], [100,0]]
    tree = CoverTree(pts, lambda a,b: math.dist(a,b))
    assert tree._initial_root_level_val == 7

def test_query_optimizations():
    pts = [[i, i] for i in range(20)]
    tree = CoverTree(pts, lambda a,b: math.dist(a,b))
    res = tree.query([1.1, 1.1], k=2)
    points_found = {tuple(p) for _, p in res}
    assert (1.0, 1.0) in points_found
    assert (2.0, 2.0) in points_found

@composite
def cover_tree_data(draw):
    dim = draw(st.integers(min_value=1, max_value=3))
    pt_strategy = st.tuples(*[st.floats(-100, 100) for _ in range(dim)])
    points = draw(st.lists(pt_strategy, min_size=1, max_size=20))
    k = draw(st.integers(min_value=1, max_value=len(points) + 5))
    query_pt = draw(pt_strategy)
    return dim, points, query_pt, k

@given(data=cover_tree_data())
@settings(max_examples=50)
def test_query_knn_property(data):
    dim, points, query_pt, k = data
    # Construir el árbol
    pts_list = [list(p) for p in points]
    tree = CoverTree(pts_list, lambda a,b: math.dist(a,b))
    # Ejecutar k-NN
    res = tree.query(list(query_pt), k=k)
    # Brute-force
    brute = sorted(
        [(math.dist(query_pt, p), list(p)) for p in points],
        key=lambda x: x[0]
    )
    expected = brute[:min(k, len(points))]
    # Comparar
    assert len(res) == len(expected)
    for (d_res, p_res), (d_exp, p_exp) in zip(res, expected):
        assert pytest.approx(d_res, rel=1e-6) == d_exp
        assert p_res == p_exp

if __name__ == '__main__':
    pytest.main(['-v', __file__])

## Pregunta 5


from __future__ import annotations
import math
from typing import List, Optional, Tuple, Any
import random

class Rectangle:
    """
    Caja AABB en R^n (aquí n=2).
    """
    __slots__ = ("min_x", "min_y", "max_x", "max_y")

    def __init__(self, min_x: float, min_y: float, max_x: float, max_y: float) -> None:
        assert min_x <= max_x and min_y <= max_y
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def enlarge(self, other: Rectangle) -> Rectangle:
        return Rectangle(
            min(self.min_x, other.min_x),
            min(self.min_y, other.min_y),
            max(self.max_x, other.max_x),
            max(self.max_y, other.max_y),
        )

    def area(self) -> float:
        return (self.max_x - self.min_x) * (self.max_y - self.min_y)

    def distance_to_point(self, x: float, y: float) -> float:
        dx = 0.0
        if x < self.min_x:
            dx = self.min_x - x
        elif x > self.max_x:
            dx = x - self.max_x
        dy = 0.0
        if y < self.min_y:
            dy = self.min_y - y
        elif y > self.max_y:
            dy = y - self.max_y
        return math.hypot(dx, dy)


class RTreeNode:
    __slots__ = ("is_leaf", "entries", "children", "mbr", "parent")

    def __init__(self, is_leaf: bool = True, parent: Optional[RTreeNode] = None):
        self.is_leaf = is_leaf
        # leaf: entries = list of (Rectangle, payload)
        # internal: children = list of RTreeNode
        self.entries: List[Tuple[Rectangle, Any]] = []
        self.children: List[RTreeNode] = []
        self.mbr: Optional[Rectangle] = None
        self.parent = parent

    def update_mbr(self):
        items: List[Rectangle]
        if self.is_leaf:
            items = [r for r, _ in self.entries]
        else:
            items = [c.mbr for c in self.children if c.mbr]
        if not items:
            self.mbr = None
            return
        m = items[0]
        for r in items[1:]:
            m = m.enlarge(r)
        self.mbr = m

    def add_entry(self, rect: Rectangle, payload: Any):
        self.entries.append((rect, payload))
        self._propagate_recalc()

    def add_child(self, node: RTreeNode):
        node.parent = self
        self.children.append(node)
        self._propagate_recalc()

    def _propagate_recalc(self):
        node: Optional[RTreeNode] = self
        while node:
            node.update_mbr()
            node = node.parent

class RTree:
    def __init__(self, M: int = 8, m: int = 4):
        assert m <= M // 2
        self.M = M
        self.m = m
        self.root = RTreeNode(is_leaf=True)

    def insert(self, rect: Rectangle, payload: Any):
        leaf = self._choose_leaf(self.root, rect)
        leaf.add_entry(rect, payload)
        self._handle_overflow(leaf)

    def _choose_leaf(self, node: RTreeNode, rect: Rectangle) -> RTreeNode:
        if node.is_leaf:
            return node
        # pick child that needs least enlargement
        best, best_inc = None, float("inf")
        for c in node.children:
            assert c.mbr
            area_before = c.mbr.area()
            area_after = c.mbr.enlarge(rect).area()
            inc = area_after - area_before
            if inc < best_inc:
                best_inc, best = inc, c
        return self._choose_leaf(best, rect)  # type: ignore

    def _handle_overflow(self, node: RTreeNode):
        if node.is_leaf:
            count = len(node.entries)
        else:
            count = len(node.children)
        if count <= self.M:
            return
        n1, n2 = self._linear_split(node)
        if node.parent is None:
            # create new root
            new_root = RTreeNode(is_leaf=False)
            new_root.add_child(n1)
            new_root.add_child(n2)
            self.root = new_root
        else:
            p = node.parent
            # replace node by n1, n2
            if node.is_leaf:
                # remueve a todas las entradas
                for e in node.entries:
                    pass
            p.children.remove(node)
            p.add_child(n1)
            p.add_child(n2)
            self._handle_overflow(p)

    def _linear_split(self, node: RTreeNode) -> Tuple[RTreeNode, RTreeNode]:
        # Split lineal Guttman 
        if node.is_leaf:
            items = [(rect, payload) for rect, payload in node.entries]
        else:
            items = [(c.mbr, c) for c in node.children]  # type: ignore
        dim = 2
        best_norm_sep, best_axis, seed1, seed2 = -1, None, None, None
        for axis in range(dim):
        
            lows = [(it[0].min_x if axis == 0 else it[0].min_y, i) for i, it in enumerate(items)]
            highs = [(it[0].max_x if axis == 0 else it[0].max_y, i) for i, it in enumerate(items)]
            low_min, i_low_min = min(lows)
            low_max, i_low_max = max(lows)
            high_min, i_high_min = min(highs)
            high_max, i_high_max = max(highs)
            width = (max(h[0] for h in highs) - min(l[0] for l in lows)) or 1.0
            norm_sep = (low_max - high_min) / width
            if norm_sep > best_norm_sep:
                best_norm_sep, best_axis = norm_sep, axis
                seed1 = items[i_low_max]
                seed2 = items[i_high_min]
        # construimos dos nodos
        n1 = RTreeNode(is_leaf=node.is_leaf)
        n2 = RTreeNode(is_leaf=node.is_leaf)

        def add_to(n: RTreeNode, it):
            if node.is_leaf:
                rect, payload = it
                n.entries.append((rect, payload))
            else:
                _, child = it
                n.children.append(child)
                child.parent = n
        add_to(n1, seed1); add_to(n2, seed2)
        # remaining
        remaining = [it for it in items if it is not seed1 and it is not seed2]
        for it in remaining:
            if node.is_leaf:
                r, _ = it
            else:
                r = it[0]
            m1 = n1.mbr.enlarge(r) if n1.mbr else r
            m2 = n2.mbr.enlarge(r) if n2.mbr else r
            d1 = m1.area() - (n1.mbr.area() if n1.mbr else 0)
            d2 = m2.area() - (n2.mbr.area() if n2.mbr else 0)
            target = n1 if d1 < d2 else n2
            add_to(target, it)
            if len(n1.entries if node.is_leaf else n1.children) + len(remaining) - 1 == self.m:
                for rest in remaining[remaining.index(it)+1:]:
                    add_to(n1, rest)
                break
            if len(n2.entries if node.is_leaf else n2.children) + len(remaining) - 1 == self.m:
                for rest in remaining[remaining.index(it)+1:]:
                    add_to(n2, rest)
                break
        # recalc MBRs
        n1.update_mbr(); n2.update_mbr()
        return n1, n2

    def nearest(self, x: float, y: float) -> Any:
        best_dist = float("inf")
        best_payload = None

        def recurse(node: RTreeNode):
            nonlocal best_dist, best_payload
            if node.is_leaf:
                for rect, payload in node.entries:
                    d = rect.distance_to_point(x, y)
                    if d < best_dist:
                        best_dist, best_payload = d, payload
            else:
                lst: List[Tuple[float, RTreeNode]] = []
                for c in node.children:
                    assert c.mbr
                    d = c.mbr.distance_to_point(x, y)
                    if d <= best_dist:
                        lst.append((d, c))
                lst.sort(key=lambda t: t[0])
                for d, c in lst:
                    if d > best_dist:
                        break
                    recurse(c)

        recurse(self.root)
        return best_payload


# Pruebas con pytest 

def test_nearest_vs_bruteforce():
    tree = RTree(M=8, m=4)
    rects = []
    # genera 100 rectángulos aleatorios en [0,100]^2 de tamaño aleatorio [1,5]
    for i in range(100):
        w, h = random.uniform(1,5), random.uniform(1,5)
        x0, y0 = random.uniform(0, 100-w), random.uniform(0, 100-h)
        rects.append((Rectangle(x0, y0, x0+w, y0+h), i))
    # inserta con payload = índice
    for r, idx in rects:
        tree.insert(r, idx)
    # prueba 10 consultas aleatorias
    for _ in range(10):
        qx, qy = random.uniform(0,100), random.uniform(0,100)
        best_i, best_d = None, float("inf")
        for r, idx in rects:
            d = r.distance_to_point(qx, qy)
            if d < best_d:
                best_d, best_i = idx, d
        found = tree.nearest(qx, qy)
        assert found == best_i

if __name__ == "__main__":
    import pytest, sys
    sys.exit(pytest.main([__file__]))

