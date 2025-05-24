# treap_augmented.py
from __future__ import annotations
from typing import Optional
import random

class TreapNode:
    """Nodo de Treap con máximo del subárbol aumentado."""
    __slots__ = ("key", "value", "priority", "left", "right", "subtree_max")

    def __init__(self, key: int, value: int, priority: float | None = None):
        self.key = key
        self.value = value
        self.priority = priority if priority is not None else random.random()
        self.left: Optional[TreapNode] = None
        self.right: Optional[TreapNode] = None
        self.subtree_max = value  # inicializa con su propio valor

    # ---------- funciones auxiliares ----------
    def _update(self) -> None:
        """Recalcula el máximo del subárbol después de un cambio estructural."""
        self.subtree_max = self.value
        if self.left:
            self.subtree_max = max(self.subtree_max, self.left.subtree_max)
        if self.right:
            self.subtree_max = max(self.subtree_max, self.right.subtree_max)

def rotate_left(p: TreapNode) -> TreapNode:
    """Retorna la nueva raíz después de una rotación a la izquierda."""
    r = p.right
    assert r is not None
    p.right = r.left
    r.left = p
    p._update()
    r._update()
    return r

def rotate_right(p: TreapNode) -> TreapNode:
    """Retorna la nueva raíz después de una rotación a la derecha."""
    l = p.left
    assert l is not None
    p.left = l.right
    l.right = p
    p._update()
    l._update()
    return l

# ---------- inserción ----------
def insert(root: Optional[TreapNode], key: int, value: int,
           priority: float | None = None) -> TreapNode:
    if root is None:
        return TreapNode(key, value, priority)

    if key < root.key:
        root.left = insert(root.left, key, value, priority)
        if root.left.priority < root.priority:          # propiedad de min-heap
            root = rotate_right(root)
    elif key > root.key:
        root.right = insert(root.right, key, value, priority)
        if root.right.priority < root.priority:
            root = rotate_left(root)
    else:  # sobrescribe el valor si la clave ya existe (claves únicas)
        root.value = value
    root._update()
    return root

# ---------- eliminación ----------
def delete(root: Optional[TreapNode], key: int) -> Optional[TreapNode]:
    if root is None:
        return None
    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:  # se encontró el nodo a eliminar
        if not (root.left or root.right):  # hoja
            return None
        # rota el hijo con menor prioridad hacia arriba
        if root.left and (not root.right or root.left.priority < root.right.priority):
            root = rotate_right(root)
            root.right = delete(root.right, key)
        else:
            root = rotate_left(root)
            root.left = delete(root.left, key)
    root._update()
    return root

# ---------- consulta de máximo en rango ----------
def find_max_value_in_range(root: Optional[TreapNode],
                            key_min: int, key_max: int) -> int | None:
    """Retorna el máximo valor para claves en el rango [key_min, key_max]."""
    if root is None or key_min > key_max:
        return None

    max_val = None
    node = root
    stack: list[TreapNode] = []
    while stack or node:
        while node:
            # Podar todo el subárbol si no puede contener claves en el rango
            if node.key < key_min:
                node = node.right
            elif node.key > key_max:
                node = node.left
            else:
                stack.append(node)
                node = node.left
        node = stack.pop()
        # node.key está garantizado dentro del rango
        if max_val is None or node.value > max_val:
            max_val = node.value
        # Si todo el subárbol derecho está dentro del rango, se puede usar el valor aumentado
        if node.right and node.right.key <= key_max:
            max_val = max(max_val, node.right.subtree_max)
            node = None  # terminado
        else:
            node = node.right
    return max_val
