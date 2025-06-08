from __future__ import annotations
from typing import List, Optional, Tuple, Iterator, TypeVar, Generic
from bisect import bisect_left
from collections import deque
import logging
import math

# Configurar logger para depuración detallada
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

K = TypeVar('K')
V = TypeVar('V')  # Tipo de valor en hojas

class BPlusTreeNode(Generic[K, V]):
    """
    Nodo de B+ Tree. Puede ser hoja o interno.

    Atributos:
        order: número máximo de claves por nodo.
        is_leaf: indica si es nodo hoja.
        keys: lista ordenada de claves.
        children: apuntadores a nodos hijos (solo internos).
        values: listas de valores por clave (solo hojas).
        next: enlace al siguiente nodo hoja.
    """
    __slots__ = ("order", "is_leaf", "keys", "children", "values", "next")

    def __init__(self, order: int, is_leaf: bool = False) -> None:
        self.order: int = order
        self.is_leaf: bool = is_leaf
        self.keys: List[K] = []
        self.children: List["BPlusTreeNode[K, V]"] = []
        self.values: List[List[V]] = []  # solo en hojas
        self.next: Optional[BPlusTreeNode[K, V]] = None  # enlace de hojas

    def __repr__(self) -> str:
        if self.is_leaf:
            return f"Hoja(claves={self.keys}, valores={self.values})"
        return f"Interno(claves={self.keys})"

    def find(self, key: K) -> Optional[List[V]]:
        """
        Busca todos los valores asociados a la clave.
        :param key: clave a buscar.
        :return: lista de valores o None si no existe.
        """
        if self.is_leaf:
            idx = bisect_left(self.keys, key)
            if idx < len(self.keys) and self.keys[idx] == key:
                logger.debug(f"Encontrada clave {key} en hoja con valores {self.values[idx]}")
                return self.values[idx]
            logger.debug(f"Clave {key} no encontrada en hoja")
            return None
        # si es interno, descender al hijo adecuado
        idx = bisect_left(self.keys, key)
        logger.debug(f"Descendiendo a child[{idx}] para buscar {key}")
        return self.children[idx].find(key)

    def insert_non_full(self, key: K, value: V) -> None:
        """
        Inserta la pareja (clave, valor) en un nodo que no está lleno.
        Si la pareja ya existe, no la duplica.
        """
        if self.is_leaf:
            idx = bisect_left(self.keys, key)
            if idx < len(self.keys) and self.keys[idx] == key:
                if value not in self.values[idx]:
                    self.values[idx].append(value)
                    logger.debug(f"Añadido valor {value} a clave existente {key}")
                else:
                    logger.debug(f"Pareja (clave={key}, valor={value}) ya existe; se ignora")
            else:
                self.keys.insert(idx, key)
                self.values.insert(idx, [value])
                logger.debug(f"Insertada clave {key} en hoja: {self.keys}")
        else:
            idx = bisect_left(self.keys, key)
            child = self.children[idx]
            if len(child.keys) == self.order:
                logger.debug(f"Hijo lleno en idx {idx}, realizando división")
                self.split_child(idx)
                if key > self.keys[idx]:
                    idx += 1
            self.children[idx].insert_non_full(key, value)

    def split_child(self, idx: int) -> None:
        """
        Divide el nodo hijo en idx cuando está lleno.
        Utiliza mid = (order+1)//2 para equilibrar.
        """
        child = self.children[idx]
        mid = (self.order + 1) // 2  # t = ceil(order/2)
        if child.is_leaf:
            nuevo = BPlusTreeNode[K, V](self.order, True)
            nuevo.keys = child.keys[mid:]
            nuevo.values = child.values[mid:]
            child.keys = child.keys[:mid]
            child.values = child.values[:mid]
            nuevo.next = child.next
            child.next = nuevo
            self.keys.insert(idx, nuevo.keys[0])
            self.children.insert(idx+1, nuevo)
            logger.debug(f"División de hoja en mid={mid}; promovida clave {nuevo.keys[0]}")
        else:
            nuevo = BPlusTreeNode[K, V](self.order, False)
            clave_mediana = child.keys[mid]
            nuevo.keys = child.keys[mid+1:]
            nuevo.children = child.children[mid+1:]
            child.keys = child.keys[:mid]
            child.children = child.children[:mid+1]
            self.keys.insert(idx, clave_mediana)
            self.children.insert(idx+1, nuevo)
            logger.debug(f"División de interno en mid={mid}; promovida clave {clave_mediana}")

    def delete(self, key: K) -> None:
        """
        Elimina la clave de este subárbol.
        No lanza error si la clave no existe.
        """
        if self.is_leaf:
            if key in self.keys:
                idx = self.keys.index(key)
                self.keys.pop(idx)
                self.values.pop(idx)
                logger.debug(f"Eliminada clave {key} de hoja; claves ahora {self.keys}")
            else:
                logger.debug(f"Clave {key} no encontrada en hoja para eliminar")
            return
        idx = bisect_left(self.keys, key)
        if idx < len(self.keys) and self.keys[idx] == key:
            idx += 1
            logger.debug(f"Delegando eliminación de {key} a child[{idx}]")
        hijo = self.children[idx]
        hijo.delete(key)
        t = math.ceil(self.order / 2)
        min_keys = t - 1
        if len(hijo.keys) < min_keys:
            logger.debug(f"Subdesbordamiento en child[{idx}]; rebalanceando")
            self._rebalance(idx)

    def _rebalance(self, idx: int) -> None:
        hijo = self.children[idx]
        t = math.ceil(self.order / 2)
        min_keys = t - 1
        # intentar préstamo de hermano izquierdo
        if idx and len(self.children[idx-1].keys) > min_keys:
            izq = self.children[idx-1]
            if hijo.is_leaf:
                hijo.keys.insert(0, izq.keys.pop())
                hijo.values.insert(0, izq.values.pop())
                self.keys[idx-1] = hijo.keys[0]
            else:
                hijo.keys.insert(0, self.keys[idx-1])
                self.keys[idx-1] = izq.keys.pop()
                hijo.children.insert(0, izq.children.pop())
            logger.debug(f"Préstamo de hermano previo en {idx-1}")
        # intentar préstamo de hermano derecho
        elif idx+1 < len(self.children) and len(self.children[idx+1].keys) > min_keys:
            der = self.children[idx+1]
            if hijo.is_leaf:
                hijo.keys.append(der.keys.pop(0))
                hijo.values.append(der.values.pop(0))
                self.keys[idx] = der.keys[0]
            else:
                hijo.keys.append(self.keys[idx])
                self.keys[idx] = der.keys.pop(0)
                hijo.children.append(der.children.pop(0))
            logger.debug(f"Préstamo de hermano siguiente en {idx+1}")
        else:
            objetivo = idx if idx+1 < len(self.children) else idx-1
            self._merge(objetivo)

    def _merge(self, idx: int) -> None:
        izq = self.children[idx]
        der = self.children[idx+1]
        if izq.is_leaf:
            izq.keys.extend(der.keys)
            izq.values.extend(der.values)
            izq.next = der.next
        else:
            izq.keys.append(self.keys[idx])
            izq.keys.extend(der.keys)
            izq.children.extend(der.children)
        self.keys.pop(idx)
        self.children.pop(idx+1)
        logger.debug(f"Merge de nodos en {idx} y {idx+1}")

class BPlusTree(Generic[K, V]):
    """
    B+ Tree de orden `order`.

    Ejemplo:
        tree = BPlusTree[int, str](4)
        tree.insert(2, 'a')
        tree.insert(2, 'b')  # añade valor a clave existente
        print(tree.find(2))  # ['a','b']
    """
    def __init__(self, order: int = 4) -> None:
        if order < 3:
            raise ValueError("El orden debe ser >= 3.")
        self.order = order
        self.root: BPlusTreeNode[K, V] = BPlusTreeNode(order, True)

    def __repr__(self) -> str:
        return f"BPlusTree(orden={self.order})"

    def find(self, key: K) -> Optional[List[V]]:
        return self.root.find(key)

    def insert(self, key: K, value: V) -> None:
        """
        Inserta la pareja (key, value). No duplica si ya existe.
        """
        raiz = self.root
        if len(raiz.keys) == self.order:
            nueva_raiz = BPlusTreeNode[K, V](self.order, False)
            nueva_raiz.children.append(raiz)
            nueva_raiz.split_child(0)
            self.root = nueva_raiz
            logger.debug("Raíz dividida; nueva raíz creada")
        self.root.insert_non_full(key, value)

    def delete(self, key: K) -> None:
        """
        Elimina la clave de todo el árbol.
        Si la clave no existe, no hace nada.
        """
        self.root.delete(key)
        if not self.root.keys and not self.root.is_leaf:
            self.root = self.root.children[0]
            logger.debug("Reducida altura del árbol tras eliminación")

    def traverse_leaves(self) -> Iterator[Tuple[K, List[V]]]:
        """
        Recorre todas las claves y valores en las hojas enlazadas.
        """
        nodo = self.root
        while not nodo.is_leaf:
            nodo = nodo.children[0]
        while nodo:
            for k, vs in zip(nodo.keys, nodo.values):
                yield k, vs
            nodo = nodo.next

    def validate(self) -> bool:
        """
        Verifica invariantes:
          - Nodos internos (no raíz): t-1 <= num_claves <= order
          - Hijos = num_claves+1
          - Todas hojas a la misma profundidad
        """
        profundidades: List[int] = []
        def dfs(n: BPlusTreeNode[K, V], prof: int) -> None:
            if n.is_leaf:
                profundidades.append(prof)
            else:
                t = math.ceil(self.order/2)
                min_claves = 1 if n is self.root else t-1
                assert min_claves <= len(n.keys) <= self.order, \
                    f"Nº de claves en interno fuera de rango: {n.keys}"
                assert len(n.children) == len(n.keys)+1, "Desajuste hijos/claves"
                for c in n.children:
                    dfs(c, prof+1)
        dfs(self.root, 1)
        assert profundidades and len(set(profundidades)) == 1, \
            f"Hojas a profundidades distintas: {profundidades}"
        logger.debug("Validación correcta: estructura válida")
        return True

# --- Pruebas con pytest ---
import pytest

def test_basic_insert_find():
    arbol = BPlusTree[int, str](4)
    arbol.insert(2, 'a')
    arbol.insert(2, 'b')  # verifica duplicados
    assert arbol.find(2) == ['a', 'b']
    assert arbol.find(99) is None
    assert arbol.validate()

@pytest.mark.parametrize("operaciones", [
    (['insert', 'delete', 'insert', 'delete'], [1,2,3,4]),
])
def test_mixed_operations_and_validate(operaciones):
    arbol = BPlusTree[int, int](3)
    seq = [5,2,8,1,3,7,9]
    for x in seq:
        arbol.insert(x, x)
    for x in [2,8,5]:
        arbol.delete(x)
        assert arbol.find(x) is None
        assert arbol.validate()
    for x in [5,8]:
        arbol.insert(x, x*2)
        assert arbol.find(x) == [x*2]
        assert arbol.validate()

def test_merge_chained_up_to_root():
    arbol = BPlusTree[int,int](3)
    for i in range(1, 20): arbol.insert(i, i)
    for i in range(1, 20):
        arbol.delete(i)
        assert arbol.validate()

def test_odd_even_order_behavior():
    for order in [3,4,5,6]:
        arbol = BPlusTree[int,int](order)
        for i in range(1, order*3): arbol.insert(i, i)
        assert arbol.validate()
        for i in range(1, order*3): arbol.delete(i)
        assert arbol.validate()

if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main(["-v", __file__]))
