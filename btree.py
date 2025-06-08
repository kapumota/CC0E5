from __future__ import annotations
from typing import List, Optional, Tuple, Iterator, TypeVar, Generic
from bisect import bisect_left
from collections import deque
import logging

# Configurar logger específico del módulo
logger = logging.getLogger(__name__)

# Excepciones propias para el Árbol B
class BTreeError(Exception):
    """Excepción base para errores en B-Tree."""
    pass

class BTreeKeyError(BTreeError, KeyError):
    """Se produce cuando no se encuentra una clave o la operación es inválida."""
    pass

# Tipo genérico que debe ser ordenable
K = TypeVar('K')

class BTreeNode(Generic[K]):
    """
    Nodo de un Árbol B que almacena claves y referencias a hijos.

    :param t: Grado mínimo del nodo.
    :param leaf: Indica si el nodo es hoja.
    """
    __slots__ = ("t", "leaf", "keys", "children")

    def __init__(self, t: int, leaf: bool = False) -> None:
        self.t: int = t
        self.leaf: bool = leaf
        self.keys: List[K] = []
        self.children: List[BTreeNode[K]] = []

    def __repr__(self) -> str:
        return f"{'Hoja' if self.leaf else 'Nodo'}(claves={self.keys})"

    def traverse(self) -> Iterator[K]:
        """
        Recorre el subárbol en orden ascendente de claves.
        :yield: Cada clave en orden.
        """
        for idx, key in enumerate(self.keys):
            if not self.leaf:
                yield from self.children[idx].traverse()
            yield key
        if not self.leaf:
            yield from self.children[len(self.keys)].traverse()

    def search(self, k: K) -> Optional[Tuple[BTreeNode[K], int]]:
        """
        Busca la clave k en el nodo o sus hijos.
        :param k: Clave a buscar.
        :return: Tupla (nodo, índice) si se encuentra, o None.
        """
        idx = bisect_left(self.keys, k)
        if idx < len(self.keys) and self.keys[idx] == k:
            return self, idx
        if self.leaf:
            return None
        return self.children[idx].search(k)

    def split_child(self, i: int) -> None:
        """
        Divide el hijo en la posición i cuando esté lleno.
        :param i: Índice del hijo a dividir.
        """
        y = self.children[i]
        t = y.t
        z = BTreeNode[K](t, y.leaf)

        # Transferir claves y subárboles al nuevo nodo z
        z.keys = y.keys[t:]
        if not y.leaf:
            z.children = y.children[t:]
        median = y.keys[t-1]
        y.keys = y.keys[:t-1]
        if not y.leaf:
            y.children = y.children[:t]

        # Insertar z y la clave mediana en el nodo actual
        self.children.insert(i + 1, z)
        self.keys.insert(i, median)
        logger.debug(f"índice hijo dividido={i}, mediana={median}")

    def insert_non_full(self, k: K) -> None:
        """
        Inserta la clave k en el subárbol cuando no está lleno.
        :param k: Clave a insertar.
        """
        if self.leaf:
            idx = bisect_left(self.keys, k)
            self.keys.insert(idx, k)
            logger.debug(f"Insertado {k} en hoja con claves ahora={self.keys}")
        else:
            idx = bisect_left(self.keys, k)
            child = self.children[idx]
            if len(child.keys) == 2 * self.t - 1:
                self.split_child(idx)
                if self.keys[idx] < k:
                    idx += 1
            self.children[idx].insert_non_full(k)

    def delete(self, k: K) -> None:
        """
        Elimina la clave k del subárbol, manteniendo el factor de llenado.
        :param k: Clave a eliminar.
        :raises BTreeKeyError: Si la clave no existe en este nodo.
        """
        idx = bisect_left(self.keys, k)
        # Caso: clave en este nodo
        if idx < len(self.keys) and self.keys[idx] == k:
            if self.leaf:
                self.keys.pop(idx)
                logger.debug(f"Borrada clave {k} de hoja")
            else:
                self._delete_internal(idx)
        else:
            # Si es hoja y no está, ignorar (no propagar excepción)
            if self.leaf:
                return
            if len(self.children[idx].keys) < self.t:
                self._fill(idx)
            # Ajustar índice si hubo combinación
            if idx > len(self.keys):
                self.children[idx-1].delete(k)
            else:
                self.children[idx].delete(k)

    # Métodos auxiliares de borrado
    def _delete_internal(self, idx: int) -> None:
        k = self.keys[idx]
        left, right = self.children[idx], self.children[idx+1]
        if len(left.keys) >= self.t:
            pred = left._get_predecessor()
            self.keys[idx] = pred
            left.delete(pred)
        elif len(right.keys) >= self.t:
            succ = right._get_successor()
            self.keys[idx] = succ
            right.delete(succ)
        else:
            self._merge(idx)
            left.delete(k)

    def _get_predecessor(self) -> K:
        node = self
        while not node.leaf:
            node = node.children[-1]
        return node.keys[-1]

    def _get_successor(self) -> K:
        node = self
        while not node.leaf:
            node = node.children[0]
        return node.keys[0]

    def _fill(self, idx: int) -> None:
        if idx and len(self.children[idx-1].keys) >= self.t:
            self._borrow_from_prev(idx)
        elif idx < len(self.keys) and len(self.children[idx+1].keys) >= self.t:
            self._borrow_from_next(idx)
        else:
            if idx < len(self.keys):
                self._merge(idx)
            else:
                self._merge(idx-1)

    def _borrow_from_prev(self, idx: int) -> None:
        child, sibling = self.children[idx], self.children[idx-1]
        child.keys.insert(0, self.keys[idx-1])
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        self.keys[idx-1] = sibling.keys.pop()

    def _borrow_from_next(self, idx: int) -> None:
        child, sibling = self.children[idx], self.children[idx+1]
        child.keys.append(self.keys[idx])
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        self.keys[idx] = sibling.keys.pop(0)

    def _merge(self, idx: int) -> None:
        child, sibling = self.children[idx], self.children[idx+1]
        child.keys.append(self.keys.pop(idx))
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.children.extend(sibling.children)
        self.children.pop(idx+1)

class BTree(Generic[K]):
    """
    Árbol B de grado mínimo t con operaciones de inserción, búsqueda y borrado.

    :param t: Grado mínimo del árbol.
    """
    def __init__(self, t: int) -> None:
        if t < 2:
            raise ValueError("El grado mínimo 't' debe ser al menos 2.")
        self.t: int = t
        self.root: Optional[BTreeNode[K]] = None

    def __repr__(self) -> str:
        return f"BTree(t={self.t}, root={self.root})"

    def __contains__(self, k: K) -> bool:
        """Permite usar 'k in tree' para buscar."""
        return bool(self.root and self.root.search(k))

    def __iter__(self) -> Iterator[K]:
        """Iterador en orden ascendente de claves."""
        if not self.root:
            return iter([])
        return self.root.traverse()

    def __len__(self) -> int:
        """Número total de claves en el árbol."""
        return sum(1 for _ in self)

    def traverse(self) -> List[K]:
        """Devuelve lista ordenada de todas las claves."""
        return list(self)

    def search(self, k: K) -> bool:
        """Busca si la clave k está en el árbol."""
        return k in self

    def insert(self, k: K) -> None:
        """
        Inserta una nueva clave.
        :param k: Clave a insertar.
        :raises BTreeError: Si la clave ya existe.
        """
        if k in self:
            raise BTreeError(f"Clave duplicada: {k}")
        if not self.root:
            self.root = BTreeNode[K](self.t, leaf=True)
            self.root.keys.append(k)
            logger.debug(f"Raíz creada con clave {k}")
            return
        if len(self.root.keys) == 2*self.t - 1:
            new_root = BTreeNode[K](self.t, leaf=False)
            new_root.children.append(self.root)
            new_root.split_child(0)
            idx = 1 if new_root.keys[0] < k else 0
            new_root.children[idx].insert_non_full(k)
            self.root = new_root
        else:
            self.root.insert_non_full(k)
        logger.debug(f"Insertado {k}, árbol ahora tiene {len(self)} claves")

    def delete(self, k: K) -> None:
        """
        Elimina la clave k.
        :param k: Clave a eliminar.
        :raises BTreeKeyError: Si el árbol está vacío.
        """
        if not self.root:
            return
        # Intentar borrado y silenciar si clave no existe
        self.root.delete(k)
        # Actualizar raíz si queda vacía
        if self.root and not self.root.keys:
            self.root = None if self.root.leaf else self.root.children[0]
        logger.debug(f"Borrada {k}, árbol ahora tiene {len(self)} claves")

    def validate(self) -> bool:
        """
        Verifica invariantes estructurales del árbol.
        :return: True si es válido.
        :raises AssertionError: Si alguna invariante falla.
        """
        if not self.root:
            return True
        # Validar raíz: entre 1 y 2t-1 claves
        assert 1 <= len(self.root.keys) <= 2*self.t - 1, "Raíz viola invariante"
        # Validar consistencia de hojas
        depths = self._get_leaf_depths()
        assert len(set(depths)) == 1, f"Hojas en niveles distintos: {depths}"
        # Validar nodos internos excepto la raíz
        self._validate_node(self.root, is_root=True)
        return True

    def _get_leaf_depths(self) -> List[int]:
        depths: List[int] = []
        queue = deque([(self.root, 1)])
        while queue:
            node, depth = queue.popleft()
            if node.leaf:
                depths.append(depth)
            else:
                for child in node.children:
                    queue.append((child, depth+1))
        return depths

    def _validate_node(self, node: BTreeNode[K], is_root: bool = False) -> None:
        # Nodos internos: verificar factor de llenado mínimo
        if not node.leaf:
            if not is_root:
                assert self.t-1 <= len(node.keys) <= 2*self.t-1, "Nodo interno viola invariante"
            # Hijos deben ser claves+1
            assert len(node.children) == len(node.keys)+1, "Hijos vs claves mismatch"
            for child in node.children:
                self._validate_node(child, is_root=False)

# --- Tests con pytest ---
def test_insert_traverse_search() -> None:
    tree = BTree[int](3)
    values = [10, 20, 5, 6, 12, 30, 7, 17]
    for v in values:
        tree.insert(v)
    assert tree.traverse() == sorted(values)
    assert tree.search(6)
    assert not tree.search(999)
    assert tree.validate()

def test_deletion_leaf() -> None:
    tree = BTree[int](3)
    for v in range(1, 10):
        tree.insert(v)
    tree.delete(3)
    assert 3 not in tree.traverse()
    tree.validate()
    tree.delete(8)
    assert 8 not in tree.traverse()
    assert tree.validate()

def test_deletion_internal() -> None:
    tree = BTree[int](3)
    values = [50, 20, 70, 10, 30, 60, 80, 5, 15, 25, 35]
    for v in values:
        tree.insert(v)
    tree.delete(20)
    assert 20 not in tree.traverse()
    tree.validate()
    tree.delete(50)
    assert 50 not in tree.traverse()
    assert tree.validate()

def test_delete_nonexistent() -> None:
    tree = BTree[int](3)
    values = [2, 4, 6, 8, 10]
    for v in values:
        tree.insert(v)
    tree.delete(100)
    assert tree.traverse() == values
    assert tree.validate()

def test_structural_invariants() -> None:
    tree = BTree[int](3)
    values = list(range(50))
    for v in values:
        tree.insert(v)
    assert tree.validate()
    for v in [10, 20, 30, 5, 45]:
        tree.delete(v)
    assert tree.validate()

def test_generic_types_string() -> None:
    tree = BTree[str](3)
    words = ["apple", "banana", "cherry", "date", "fig", "grape"]
    for word in words:
        tree.insert(word)
    assert tree.traverse() == sorted(words)
    assert tree.search("cherry")
    assert not tree.search("mango")
    tree.delete("banana")
    assert not tree.search("banana")
    assert tree.validate()

if __name__ == "__main__":
    import pytest, sys
    sys.exit(pytest.main(["-v", __file__]))
