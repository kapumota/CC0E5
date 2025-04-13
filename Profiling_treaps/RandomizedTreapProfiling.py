#!/usr/bin/env python3
"""
RandomizedTreapProfiling.py

- BST iterativo (sin recursión profunda) para evitar RecursionError en secuencias ordenadas.
- bound >= max(size) para no superar el rango en random.sample().
- Insertar sin duplicados usando random.sample() + while new_val in keys.
"""

import random
import csv
import os
from typing import Optional, List, Generic, TypeVar
from RandomizedTreap import RandomizedTreap  # Usa tu Treap con rotaciones en el padre

T = TypeVar('T')

class BST(Generic[T]):
    """
    BST iterativo para evitar recursion depth excesiva con secuencias grandes y ordenadas.
    """
    def __init__(self):
        self.root: Optional["BST.BSTNode"] = None

    def add(self, element: T) -> bool:
        """
        Inserción iterativa: el BST se degenerará si insertas en orden,
        pero no habrá llamadas recursivas profundas.
        """
        if self.root is None:
            self.root = BST.BSTNode(element)
            return True

        current = self.root
        while True:
            if element <= current.key:
                if current.left is None:
                    current.left = BST.BSTNode(element)
                    break
                else:
                    current = current.left
            else:
                if current.right is None:
                    current.right = BST.BSTNode(element)
                    break
                else:
                    current = current.right
        return True

    def remove(self, element: T) -> bool:
        """
        Borrado iterativo. Retorna True si elimina, False si no encuentra la clave.
        """
        parent = None
        current = self.root

        # 1. Buscar el nodo 'element'
        while current is not None and current.key != element:
            parent = current
            if element <= current.key:
                current = current.left
            else:
                current = current.right

        # Si no se encontró
        if current is None:
            return False

        # 2. Eliminar el nodo 'current'
        self._removeNode(current, parent)
        return True

    def _removeNode(self, node: "BST.BSTNode", parent: Optional["BST.BSTNode"]) -> None:
        """
        Elimina 'node' conociendo también a 'parent'.
        """
        # Caso 1: nodo hoja
        if node.left is None and node.right is None:
            self._replaceChild(parent, node, None)
        # Caso 2: un solo hijo
        elif node.left is None:
            self._replaceChild(parent, node, node.right)
        elif node.right is None:
            self._replaceChild(parent, node, node.left)
        else:
            # Caso 3: dos hijos
            # Elige predecesor o sucesor aleatoriamente
            use_predecessor = (node.left is not None and
                               (node.right is None or random.random() < 0.5))
            if use_predecessor:
                predecessor, pred_parent = self._findMaxNode(node.left, node)
                node.key = predecessor.key
                self._removeNode(predecessor, pred_parent)
            else:
                successor, succ_parent = self._findMinNode(node.right, node)
                node.key = successor.key
                self._removeNode(successor, succ_parent)

    def _replaceChild(self, parent: Optional["BST.BSTNode"], oldNode: "BST.BSTNode",
                      newNode: Optional["BST.BSTNode"]) -> None:
        """
        Reemplaza 'oldNode' por 'newNode' en el padre 'parent'.
        Si parent es None, oldNode era la raíz.
        """
        if parent is None:
            self.root = newNode
        else:
            if parent.left == oldNode:
                parent.left = newNode
            else:
                parent.right = newNode

    def _findMaxNode(self, start: "BST.BSTNode", parent: "BST.BSTNode") -> ("BST.BSTNode", "BST.BSTNode"):
        """
        Encuentra el nodo con mayor clave en el subárbol 'start', retornando (nodo, padre).
        """
        current = start
        par = parent
        while current.right is not None:
            par = current
            current = current.right
        return current, par

    def _findMinNode(self, start: "BST.BSTNode", parent: "BST.BSTNode") -> ("BST.BSTNode", "BST.BSTNode"):
        """
        Encuentra el nodo con menor clave en el subárbol 'start', retornando (nodo, padre).
        """
        current = start
        par = parent
        while current.left is not None:
            par = current
            current = current.left
        return current, par

    def clear(self) -> None:
        self.root = None

    def min(self) -> Optional[T]:
        if not self.root:
            return None
        current = self.root
        while current.left:
            current = current.left
        return current.key

    def max(self) -> Optional[T]:
        if not self.root:
            return None
        current = self.root
        while current.right:
            current = current.right
        return current.key

    def search(self, element: T) -> Optional[T]:
        current = self.root
        while current is not None:
            if current.key == element:
                return current.key
            elif element <= current.key:
                current = current.left
            else:
                current = current.right
        return None

    def isEmpty(self) -> bool:
        return self.root is None

    def size(self) -> int:
        """Cuenta nodos de forma iterativa (no recursiva)."""
        if not self.root:
            return 0
        count = 0
        stack = [self.root]
        while stack:
            node = stack.pop()
            count += 1
            if node.left: stack.append(node.left)
            if node.right: stack.append(node.right)
        return count

    def height(self) -> int:
        """
        Calcula altura (número de niveles) con BFS iterativo.
        """
        if not self.root:
            return 0
        from collections import deque
        queue = deque([self.root])
        height = 0
        while queue:
            level_size = len(queue)
            for _ in range(level_size):
                node = queue.popleft()
                if node.left: queue.append(node.left)
                if node.right: queue.append(node.right)
            height += 1
        return height

    def checkBSTInvariants(self) -> bool:
        """
        Verifica la propiedad BST con un in-order iterativo.
        """
        stack = []
        current = self.root
        prev_key = None
        while stack or current:
            if current:
                stack.append(current)
                current = current.left
            else:
                current = stack.pop()
                if prev_key is not None and current.key < prev_key:
                    return False
                prev_key = current.key
                current = current.right
        return True

    class BSTNode:
        def __init__(self, key: T):
            self.key = key
            self.left: Optional["BST.BSTNode"] = None
            self.right: Optional["BST.BSTNode"] = None


# CSV y profiling

HEADERS = ["n", "height_bst", "height_rt"]
PROFILE_RANDOM_FILENAME = "bst_vs_rt_random_"
PROFILE_SKEWED_FILENAME = "bst_vs_rt_worst-case.csv"
DATA_DIRECTORY = "resultados"  # carpeta destino para los CSV

def write_to_csv_file(file_name: str, headers: List[str],
                      ns: List[int], hBSTs: List[int], hRSTs: List[int]) -> None:
    # Asegurarse de que exista la carpeta "resultados"
    os.makedirs(DATA_DIRECTORY, exist_ok=True)
    file_path = os.path.join(DATA_DIRECTORY, file_name)
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for i in range(len(ns)):
            writer.writerow([ns[i], hBSTs[i], hRSTs[i]])

def profile_height() -> None:
    """
    Inserciones y borrados aleatorios SIN duplicados, con un BST iterativo y un Treap,
    y con bound > size para no causar ValueError en random.sample().
    """
    runs_per_size = 5
    n_list: List[int] = []
    h_bst_list: List[int] = []
    h_rt_list: List[int] = []

    bound = 50000  # Aseguramos que bound >= cualquier size
    size = 1000
    while size <= 40000:
        for run in range(runs_per_size):
            rt = RandomizedTreap[int]()
            bst = BST[int]()

            # Genera 'size' valores únicos sin exceder bound
            unique_vals = random.sample(range(bound), size)  # no error, size <= bound
            keys: List[int] = []

            # Insertarlos en BST y Treap
            for val in unique_vals:
                bst.add(val)
                rt.add(val)
                keys.append(val)

            # Mezclar borrados e inserciones
            for _ in range(size):
                if keys and random.choice([True, False]):
                    idx = random.randrange(len(keys))
                    to_remove = keys.pop(idx)
                    bst.remove(to_remove)
                    rt.remove(to_remove)
                else:
                    new_val = random.randrange(bound)
                    # Evita duplicar
                    while new_val in keys:
                        new_val = random.randrange(bound)
                    bst.add(new_val)
                    rt.add(new_val)
                    keys.append(new_val)

            # Comprobación
            if bst.size() != rt.size() or bst.size() != len(keys):
                raise Exception("Error: desajuste en BST, RT, y keys")

            # Recolectar datos
            n_list.append(bst.size())
            h_bst_list.append(bst.height())
            h_rt_list.append(rt.height())

        # Volcar CSV
        file_name = PROFILE_RANDOM_FILENAME + str(bound) + ".csv"
        write_to_csv_file(file_name, HEADERS, n_list, h_bst_list, h_rt_list)

        size = int(size * 1.5)


def profile_height_ordered_sequence() -> None:
    """
    Inserta [0..n) en orden (BST iterativo + RandomizedTreap).
    - BST degenerado pero no recursivo, sin RecursionError.
    - bound no afecta aquí, no usamos random.sample en la fase principal.
    """
    runs_per_size = 3
    n_list: List[int] = []
    h_bst_list: List[int] = []
    h_rt_list: List[int] = []

    size = 100
    while size < 3000:
        for run in range(runs_per_size):
            rt = RandomizedTreap[int]()
            bst = BST[int]()
            for i in range(size):
                bst.add(i)
                rt.add(i)

            if bst.size() != rt.size():
                raise Exception("Error: desajuste BST/RT en la secuencia ordenada")
            # Comparar alturas
            if rt.height() > bst.height():
                raise Exception("Error: la altura de RT es mayor que la del BST (inusual)")

            n_list.append(bst.size())
            h_bst_list.append(bst.height())
            h_rt_list.append(rt.height())

        # Volcar en CSV (mismo worst-case)
        write_to_csv_file(PROFILE_SKEWED_FILENAME, HEADERS, n_list, h_bst_list, h_rt_list)
        size = int(size * 1.5)


def profile_cpu() -> None:
    """
    Inserciones y eliminaciones aleatorias con BST iterativo,
    y bound > size para random.sample.
    """
    runs_per_size = 3
    bound = 15000
    size = 4000

    for run in range(runs_per_size):
        bst = BST[int]()
        rt = RandomizedTreap[int]()
        keys: List[int] = []

        # Inserción inicial
        init_vals = random.sample(range(bound), size)  # no problem, size <= bound
        for val in init_vals:
            bst.add(val)
            rt.add(val)
            keys.append(val)

        # Mezclar
        for _ in range(size):
            if keys and random.choice([True, False]):
                idx = random.randrange(len(keys))
                to_remove = keys.pop(idx)
                bst.remove(to_remove)
                rt.remove(to_remove)
            else:
                new_val = random.randrange(bound)
                while new_val in keys:
                    new_val = random.randrange(bound)
                bst.add(new_val)
                rt.add(new_val)
                keys.append(new_val)

        if bst.size() != rt.size() or bst.size() != len(keys):
            raise Exception("Error: desajuste en profile_cpu")


def profile_cpu_ordered_sequence() -> None:
    """
    Inserción creciente para medir CPU, BST iterativo no recursivo.
    """
    runs_per_size = 3
    size = 3000
    for run in range(runs_per_size):
        bst = BST[int]()
        rt = RandomizedTreap[int]()
        for i in range(size):
            bst.add(i)
            rt.add(i)


def profile_memory() -> None:
    """
    Inserción de cadenas con BST iterativo y Treap. 
    No superamos size=3000, y no chocamos con random.sample en este caso.
    """
    runs_per_size = 3
    size = 3000
    start = "1000"
    for run in range(runs_per_size):
        bst = BST[str]()
        rt = RandomizedTreap[str]()
        for i in range(size):
            key = start + str(i)  # i no se repite => no hay duplicados
            bst.add(key)
            rt.add(key)


if __name__ == "__main__":
    print("Iniciando perfilado: Altura (operaciones aleatorias)...")
    profile_height()
    print("Perfilado: Altura con secuencia ordenada...")
    profile_height_ordered_sequence()
    print("Perfilado: CPU con operaciones aleatorias...")
    profile_cpu()
    print("Perfilado: CPU con secuencia ordenada...")
    profile_cpu_ordered_sequence()
    print("Perfilado: Uso de memoria...")
    profile_memory()
    print("Perfilado completado.")
