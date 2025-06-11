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
        
        # Heurística de raíz inicial: Si se proporcionan puntos, se establece un nivel
        # de raíz que refleje el diámetro del conjunto de datos para un mejor balance.
        self._initial_root_level_val = self._calculate_initial_root_level(points) if points else 10
        
        if points:
            random.shuffle(points)
            for p in points:
                self.insert(p)
    
    def _calculate_initial_root_level(self, points: List[List[float]], sample_size: int = 100) -> int:
        """
        Calcula un nivel de raíz inicial razonable estimando el diámetro del conjunto de datos.
        """
        if len(points) < 2:
            return 10
        
        # Toma una muestra de puntos para estimar el diámetro eficientemente.
        sample = random.sample(points, min(len(points), sample_size))
        max_d = 0.0
        for i in range(len(sample)):
            for j in range(i + 1, len(sample)):
                d = self.distance(sample[i], sample[j])
                if d > max_d:
                    max_d = d
        
        return math.ceil(math.log(max_d, self.base)) if max_d > 0 else 0

    def insert(self, point: List[float]) -> None:
        """
        Inserta un punto en el árbol. Incluye poda de candidatos para datos densos.
        """
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
                
                # Invariante de anidamiento: El nivel de un hijo debe ser exactamente
                # uno menos que el de su padre.
                new_level = i - 1
                new_node = CoverTree.Node(tup, level=new_level, cover_radius=0.0, parent=parent_node)
                assert new_node.level == parent_node.level - 1, "Violación del invariante de anidamiento"
                
                parent_node.children.append(new_node)
                self._index_map[tup] = new_node
                self._update_cover_radius_on_insert(new_node)
                return
            
            # Poda en la construcción: Al construir el siguiente conjunto de candidatos (Q_next),
            # solo se consideran los hijos que están "razonablemente" cerca del punto a insertar.
            # Esto previene que Q_i explote en tamaño en regiones muy densas.
            Q_next = []
            for node in Q_i:
                dist_to_node = d_p_Qi[node.point]
                for child in node.children:
                    # Si la bola de cobertura del nodo padre ya está muy lejos, es menos
                    # probable que sus hijos sean buenos candidatos.
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
        """Asciende por el árbol actualizando el radio de cobertura de los ancestros."""
        curr = node
        parent = curr.parent
        while parent is not None:
            dist = self.distance(curr.point, parent.point)
            if dist > parent.cover_radius:
                parent.cover_radius = dist
            curr = parent
            parent = curr.parent

    def query(self, query_point: List[float], k: int=1) -> List[Tuple[float, List[float]]]:
        """
        Búsqueda k-NN optimizada con un heap de candidatos y vectorización.
        """
        if self.root is None:
            return []

        q_tup = tuple(query_point)
        q_np = np.array(query_point)
        
        # Max-heap para los k-mejores resultados: (-distancia, punto)
        best_k = []
        # Min-heap para los candidatos a explorar: (cota_inferior_dist, nodo)
        candidates = []

        d_root = self.distance(q_tup, self.root.point)
        heappush(best_k, (-d_root, self.root.point))
        heappush(candidates, (max(0, d_root - self.root.cover_radius), self.root))

        while candidates:
            bound, node = heappop(candidates)
            
            # Poda principal: si la cota inferior del mejor candidato en el heap
            # es peor que el k-ésimo resultado ya encontrado, podemos parar.
            if len(best_k) == k and bound > -best_k[0][0]:
                break

            # Vectorización opcional: Si hay hijos, calcula sus distancias en bloque.
            if node.children:
                child_points = np.array([list(c.point) for c in node.children])
                # Usa NumPy para un cálculo de distancias eficiente.
                dists = np.linalg.norm(child_points - q_np, axis=1)

                for c, d in zip(node.children, dists):
                    # Actualiza los k-mejores si este hijo es un mejor candidato.
                    if len(best_k) < k:
                        heappush(best_k, (-d, c.point))
                    elif d < -best_k[0][0]:
                        heappop(best_k)
                        heappush(best_k, (-d, c.point))
                    
                    # Añade el hijo al heap de candidatos con su cota de distancia.
                    dist_k = -best_k[0][0]
                    child_bound = max(0, d - c.cover_radius)
                    # Poda secundaria: solo añade candidatos que podrían mejorar el resultado.
                    if len(best_k) < k or child_bound < dist_k:
                        heappush(candidates, (child_bound, c))

        result = sorted([(-neg_dist, list(p)) for neg_dist, p in best_k])
        return result[:k]

    def remove(self, point: List[float]) -> bool:
        """
        Elimina un punto. Los hijos del nodo eliminado se reinsertan en el árbol.
        """
        tup = tuple(point)
        if tup not in self._index_map:
            return False

        node_to_remove = self._index_map.pop(tup)
        parent = node_to_remove.parent

        # Recolecta todos los descendientes del nodo a eliminar.
        # Una futura optimización sería una reinserción en lote (batch).
        descendants = []
        q = list(node_to_remove.children)
        while q:
            n = q.pop(0)
            descendants.append(n)
            q.extend(n.children)
        
        # Separa los puntos de los nodos
        points_to_reinsert = [list(d.point) for d in descendants]
        for p in points_to_reinsert:
             # Es crucial eliminarlo del mapa de índices antes de reinsertar.
            if tuple(p) in self._index_map:
                del self._index_map[tuple(p)]

        if node_to_remove is self.root:
            self.root = None # Se reconstruirá con las reinserciones
        elif parent:
            parent.children.remove(node_to_remove)
            # Tras una eliminación, los radios de los ancestros podrían estar inflados.
            # Se recalcula hacia arriba para mantener la consistencia.
            self._recalculate_cover_radius_upwards(parent)
        
        # Reinserta todos los descendientes.
        # Nota de optimización: una rutina de inserción en lote que actualice
        # los radios una sola vez (bottom-up) sería más eficiente.
        for p in points_to_reinsert:
            self.insert(p)

        return True

    def _recalculate_cover_radius_upwards(self, start_node: 'CoverTree.Node'):
        """Recalcula el radio de cobertura desde un nodo hacia la raíz."""
        curr = start_node
        while curr is not None:
            if not curr.children:
                curr.cover_radius = 0.0
            else:
                curr.cover_radius = max(self.distance(curr.point, c.point) for c in curr.children)
            curr = curr.parent

    # Los métodos de persistencia (save/load) permanecen sin cambios
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
        if path.endswith('.pkl') or path.endswith('.pickle') or path.endswith('.bin'):
            with open(path, 'rb') as f:
                tree = pickle.load(f)
            tree.distance = distance_func
            return tree
        elif path.endswith('.json'):
            with open(path, 'r') as f:
                data = json.load(f)
            
            tree = CoverTree([], distance_func, data["base"])
            tree._initial_root_level_val = data.get("initial_root_level", 10)
            tree_structure = data.get("tree_structure")
            if not tree_structure or not tree_structure.get("nodes"):
                return tree

            nodes_data = tree_structure["nodes"]
            created_nodes: Dict[int, 'CoverTree.Node'] = {}
            for i, node_data in enumerate(nodes_data):
                point = tuple(node_data["point"])
                node = CoverTree.Node(point, node_data["level"], node_data["cover_radius"])
                created_nodes[i] = node
                tree._index_map[point] = node
            
            for i, node_data in enumerate(nodes_data):
                node = created_nodes[i]
                for child_idx in node_data["children_indices"]:
                    child_node = created_nodes[child_idx]
                    child_node.parent = node
                    node.children.append(child_node)
            
            tree.root = created_nodes[tree_structure["root_index"]]
            return tree
        else:
            raise ValueError("No se pudo determinar el formato del archivo por su extensión.")

    def _to_dict(self) -> Optional[Dict]:
        if not self.root: return None
        nodes_list = []; node_to_idx = {}
        q = [self.root]; head = 0
        while head < len(q):
            node = q[head]; head += 1
            if node.point not in node_to_idx:
                node_to_idx[node.point] = len(nodes_list)
                nodes_list.append(node)
                q.extend(node.children)
        serializable_nodes = [
            {"point": list(n.point), "level": n.level, "cover_radius": n.cover_radius,
             "children_indices": [node_to_idx[c.point] for c in n.children]} for n in nodes_list
        ]
        return {"nodes": serializable_nodes, "root_index": node_to_idx[self.root.point]}

# Pruebas unitarias

import pytest

def test_initial_root_level():
    pts = [[0,0], [100,0]]
    tree = CoverTree(pts, lambda a,b: math.dist(a,b))
    # El diámetro es 100. log2(100) es aprox 6.64. ceil(6.64) = 7.
    assert tree._initial_root_level_val == 7

def test_query_optimizations():
    pts = [[i, i] for i in range(20)]
    tree = CoverTree(pts, lambda a,b: math.dist(a,b))
    
    # Una consulta que debería beneficiarse de la poda
    res = tree.query([1.1, 1.1], k=2)
    points_found = {tuple(p) for _, p in res}
    
    # Los más cercanos a [1.1, 1.1] son [1,1] y [2,2]
    assert (1.0, 1.0) in points_found
    assert (2.0, 2.0) in points_found


if __name__ == '__main__':
    pytest.main(['-v', __file__])
