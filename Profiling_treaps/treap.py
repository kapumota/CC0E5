#!/usr/bin/env python3
"""
Implementación en Python de un Treap (árbol heap-binario de búsqueda)
"""

import threading
from typing import Optional, Generic, TypeVar

T = TypeVar('T')
S = TypeVar('S')

# Implementación simple de un Read/Write Lock similar a ReentrantReadWriteLock
class ReadWriteLock:
    def __init__(self):
        self._read_ready = threading.Condition(threading.RLock())
        self._readers = 0

    def acquire_read(self):
        self._read_ready.acquire()
        self._readers += 1
        self._read_ready.release()

    def release_read(self):
        self._read_ready.acquire()
        self._readers -= 1
        if self._readers == 0:
            self._read_ready.notify_all()
        self._read_ready.release()

    def acquire_write(self):
        self._read_ready.acquire()
        while self._readers > 0:
            self._read_ready.wait()

    def release_write(self):
        self._read_ready.release()


class Treap(Generic[T, S]):
    """
    Un Treap almacena pares (clave, prioridad) cumpliendo las propiedades
    de un árbol de búsqueda binario y de un heap.
    """
    class Entry(Generic[T, S]):
        def __init__(self, key: T, priority: S):
            self.key = key
            self.priority = priority

        def __lt__(self, other: 'Treap.Entry'):
            if other is None:
                return False
            return self.priority < other.priority

        def __eq__(self, other: 'Treap.Entry'):
            if other is None:
                return False
            return self.key == other.key and self.priority == other.priority

        def __repr__(self):
            return f"TreapEntry(key={self.key}, priority={self.priority})"

    def __init__(self):
        self.root: Optional['Treap.TreapNode'] = None
        self.lock = ReadWriteLock()

    def hasHigherPriority(self, first: S, second: S) -> bool:
        # Se considera que una prioridad es más alta si es menor (min-heap).
        return first < second

    def size(self) -> int:
        self.lock.acquire_read()
        try:
            return self.root.size() if self.root is not None else 0
        finally:
            self.lock.release_read()

    def height(self) -> int:
        self.lock.acquire_read()
        try:
            return self.root.height() if self.root is not None else 0
        finally:
            self.lock.release_read()

    def isEmpty(self) -> bool:
        self.lock.acquire_read()
        try:
            return self.root is None
        finally:
            self.lock.release_read()

    def min(self) -> Optional[T]:
        self.lock.acquire_read()
        try:
            return self.root.min() if self.root is not None else None
        finally:
            self.lock.release_read()

    def max(self) -> Optional[T]:
        self.lock.acquire_read()
        try:
            return self.root.max() if self.root is not None else None
        finally:
            self.lock.release_read()

    def search(self, key: T) -> Optional[T]:
        self.lock.acquire_read()
        try:
            node = self.root.search(key, None) if self.root is not None else None
            return node.key if node is not None else None
        finally:
            self.lock.release_read()

    def top(self) -> Optional['Treap.Entry']:
        """
        Extrae la raíz del Treap (el elemento con prioridad más alta),
        fusionando los subárboles resultantes.
        """
        self.lock.acquire_write()
        try:
            if self.root is None:
                return None
            result = Treap.Entry(self.root.key, self.root.priority)
            self.root = self._removeRoot(self.root)
            return result
        finally:
            self.lock.release_write()

    def peek(self) -> Optional['Treap.Entry']:
        """
        Retorna la raíz del Treap (el elemento con prioridad más alta)
        sin extraerlo.
        """
        self.lock.acquire_read()
        try:
            if self.root is None:
                return None
            return Treap.Entry(self.root.key, self.root.priority)
        finally:
            self.lock.release_read()

    def contains(self, entry: 'Treap.Entry') -> bool:
        self.lock.acquire_read()
        try:
            node = self.root.search(entry.key, entry.priority) if self.root is not None else None
            return node is not None
        finally:
            self.lock.release_read()

    def add(self, entry: 'Treap.Entry') -> bool:
        """
        Inserta un nodo con la clave y prioridad dadas.
        """
        self.lock.acquire_write()
        try:
            if self.root is not None:
                new_root = self.root.add(entry.key, entry.priority)
                # Ajustar la raíz subiendo hasta el verdadero padre
                while new_root.parent is not None:
                    new_root = new_root.parent
                self.root = new_root
            else:
                self.root = Treap.TreapNode(entry.key, entry.priority, self)
            return True
        finally:
            self.lock.release_write()

    def updatePriority(self, oldEntry: 'Treap.Entry', newEntry: 'Treap.Entry') -> bool:
        """
        Cambia la prioridad de una clave ya existente (vieja prioridad -> nueva prioridad).
        Sube o baja el nodo afectado para preservar la propiedad de heap.
        """
        if oldEntry.key != newEntry.key:
            raise ValueError("Las claves deben coincidir.")
        if oldEntry.priority == newEntry.priority:
            return False
        self.lock.acquire_write()
        try:
            target = self.root.search(oldEntry.key, oldEntry.priority) if self.root is not None else None
            if target is None:
                return False
            target.priority = newEntry.priority
            if self.hasHigherPriority(newEntry.priority, oldEntry.priority):
                target = target.bubbleUp()
            else:
                target = target.pushDown()
            # Ajustar raíz
            while target.parent is not None:
                target = target.parent
            self.root = target
            return True
        finally:
            self.lock.release_write()

    def remove(self, entry: 'Treap.Entry') -> bool:
        """
        Elimina un nodo que coincida con la (clave, prioridad) dada.
        """
        self.lock.acquire_write()
        try:
            removed = [False]
            if self.root is not None:
                self.root = self.root.remove(entry.key, entry.priority, removed)
            return removed[0]
        finally:
            self.lock.release_write()

    def removeKey(self, key: T) -> bool:
        """
        Elimina un nodo que tenga la clave dada (independientemente de su prioridad).
        """
        self.lock.acquire_write()
        try:
            node = self.root.search(key, None) if self.root is not None else None
            if node is None:
                return False
            return self.remove(Treap.Entry(node.key, node.priority))
        finally:
            self.lock.release_write()

    def clear(self) -> None:
        """
        Borra todos los nodos del Treap.
        """
        self.lock.acquire_write()
        try:
            old_root = self.root
            self.root = None
        finally:
            self.lock.release_write()
            if old_root is not None:
                old_root.cleanUp()

    def checkTreapInvariants(self) -> bool:
        """
        Comprueba que la propiedad del Treap (BST + min-heap en prioridad) se cumpla.
        """
        self.lock.acquire_read()
        try:
            return self.root.checkTreapInvariants() if self.root is not None else True
        finally:
            self.lock.release_read()

    def checkBSTInvariants(self) -> bool:
        """
        Comprueba únicamente la propiedad de BST.
        (Aquí se llama al mismo checkTreapInvariants por simplicidad, 
         pero podría implementarse uno que sólo valide BST).
        """
        self.lock.acquire_read()
        try:
            return self.root.checkTreapInvariants() if self.root is not None else True
        finally:
            self.lock.release_read()

    def _removeRoot(self, root: 'Treap.TreapNode') -> Optional['Treap.TreapNode']:
        """
        Fusión sencilla de subárboles al extraer la raíz:
        - Si uno de los dos hijos es None, la nueva raíz es el que NO es None.
        - Si ambos existen, se rota la raíz según quién tenga la prioridad más alta
          para bajar la raíz y seguir removiéndola.
        """
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left

        if self.hasHigherPriority(root.left.priority, root.right.priority):
            root = root.rotateRight()
            root.right = self._removeRoot(root.right)
            if root.right is not None:
                root.right.parent = root
            return root
        else:
            root = root.rotateLeft()
            root.left = self._removeRoot(root.left)
            if root.left is not None:
                root.left.parent = root
            return root

    class TreapNode:
        def __init__(self, key: T, priority: S, treap: 'Treap'):
            self.key = key
            self.priority = priority
            self.left: Optional['Treap.TreapNode'] = None
            self.right: Optional['Treap.TreapNode'] = None
            self.parent: Optional['Treap.TreapNode'] = None
            self.treap = treap

        def setLeft(self, node: Optional['Treap.TreapNode']):
            self.left = node
            if node is not None:
                node.parent = self

        def setRight(self, node: Optional['Treap.TreapNode']):
            self.right = node
            if node is not None:
                node.parent = self

        def isLeaf(self) -> bool:
            return self.left is None and self.right is None

        def isRoot(self) -> bool:
            return self.parent is None

        def isLeftChild(self) -> bool:
            return self.parent is not None and self.parent.left == self

        def isRightChild(self) -> bool:
            return self.parent is not None and self.parent.right == self

        def search(self, targetKey: T, targetPriority: Optional[S]) -> Optional['Treap.TreapNode']:
            """
            Busca un nodo con clave==targetKey y prioridad==targetPriority (si no es None).
            Si 'targetPriority' es None, solo compara la clave.
            """
            if (targetKey is None or self.key == targetKey) and \
               (targetPriority is None or self.priority == targetPriority):
                return self

            result = None
            if targetKey is None or targetKey <= self.key:
                if self.left is not None:
                    result = self.left.search(targetKey, targetPriority)
            if result is None and (targetKey is None or targetKey > self.key):
                if self.right is not None:
                    result = self.right.search(targetKey, targetPriority)
            return result

        def size(self) -> int:
            left_size = self.left.size() if self.left is not None else 0
            right_size = self.right.size() if self.right is not None else 0
            return 1 + left_size + right_size

        def height(self) -> int:
            left_height = self.left.height() if self.left is not None else 0
            right_height = self.right.height() if self.right is not None else 0
            return 1 + max(left_height, right_height)

        def min(self) -> T:
            return self.left.min() if self.left is not None else self.key

        def max(self) -> T:
            return self.right.max() if self.right is not None else self.key

        def add(self, key: T, priority: S) -> 'Treap.TreapNode':
            """
            Inserta (key, priority) en el subárbol con raíz en 'self',
            devolviendo la nueva raíz de ese subárbol tras las rotaciones.
            """
            if key <= self.key:
                if self.left is not None:
                    self.left = self.left.add(key, priority)
                    self.left.parent = self
                else:
                    self.left = Treap.TreapNode(key, priority, self.treap)
                    self.left.parent = self

                # Si la prioridad del hijo es "más alta" (numéricamente menor), el padre rota a la derecha
                if self.treap.hasHigherPriority(self.left.priority, self.priority):
                    return self.rotateRight()

            else:
                if self.right is not None:
                    self.right = self.right.add(key, priority)
                    self.right.parent = self
                else:
                    self.right = Treap.TreapNode(key, priority, self.treap)
                    self.right.parent = self

                # Si la prioridad del hijo es más alta, el padre rota a la izquierda
                if self.treap.hasHigherPriority(self.right.priority, self.priority):
                    return self.rotateLeft()

            return self

        def bubbleUp(self) -> 'Treap.TreapNode':
            """
            Sube este nodo mientras su prioridad sea más alta que la de su padre,
            rotando. Retorna la nueva raíz del subárbol.
            """
            node = self
            while node.parent is not None and not node.treap.hasHigherPriority(node.parent.priority, node.priority):
                if node.isLeftChild():
                    node = node.rotateRight()
                else:
                    node = node.rotateLeft()
            return node

        def pushDown(self) -> 'Treap.TreapNode':
            """
            Baja este nodo mientras alguno de sus hijos tenga prioridad más alta,
            rotando hacia la izquierda o derecha según corresponda.
            """
            node = self
            while True:
                candidate = None
                if node.left is not None and node.right is not None:
                    # Elige el hijo con prioridad más alta (menor valor)
                    if node.treap.hasHigherPriority(node.left.priority, node.right.priority):
                        candidate = node.left
                    else:
                        candidate = node.right
                elif node.left is not None:
                    candidate = node.left
                elif node.right is not None:
                    candidate = node.right
                else:
                    break

                if candidate is not None and node.treap.hasHigherPriority(candidate.priority, node.priority):
                    if candidate == node.left:
                        node = node.rotateRight()
                    else:
                        node = node.rotateLeft()
                else:
                    break
            return node

        def rotateRight(self) -> 'Treap.TreapNode':
            """
            Rotación a la derecha sobre self. 
            'self' baja a la derecha, 'leftChild' sube como padre.
            """
            leftChild = self.left
            if leftChild is None:
                raise Exception("rotateRight llamado sin hijo izquierdo")

            self.left = leftChild.right
            if leftChild.right is not None:
                leftChild.right.parent = self

            leftChild.right = self
            leftChild.parent = self.parent
            self.parent = leftChild

            if leftChild.parent is not None:
                if leftChild.parent.left == self:
                    leftChild.parent.left = leftChild
                else:
                    leftChild.parent.right = leftChild

            return leftChild

        def rotateLeft(self) -> 'Treap.TreapNode':
            """
            Rotación a la izquierda sobre self.
            'self' baja a la izquierda, 'rightChild' sube como padre.
            """
            rightChild = self.right
            if rightChild is None:
                raise Exception("rotateLeft llamado sin hijo derecho")

            self.right = rightChild.left
            if rightChild.left is not None:
                rightChild.left.parent = self

            rightChild.left = self
            rightChild.parent = self.parent
            self.parent = rightChild

            if rightChild.parent is not None:
                if rightChild.parent.left == self:
                    rightChild.parent.left = rightChild
                else:
                    rightChild.parent.right = rightChild

            return rightChild

        def remove(self, key: T, priority: S, removed: list) -> Optional['Treap.TreapNode']:
            """
            Eliminación de un nodo con (key, priority). Si lo encuentra, rota
            para bajarlo hasta que pueda removerlo como hoja o subárbol sin conflicto.
            """
            if self.key == key and self.priority == priority:
                removed[0] = True
                # Caso: 0 o 1 hijo
                if self.left is None:
                    temp = self.right
                    if temp is not None:
                        temp.parent = self.parent
                    return temp
                elif self.right is None:
                    temp = self.left
                    if temp is not None:
                        temp.parent = self.parent
                    return temp
                else:
                    # Nodo con dos hijos: rotar para "empujar" el nodo hacia abajo
                    if self.treap.hasHigherPriority(self.left.priority, self.right.priority):
                        newRoot = self.rotateRight()
                    else:
                        newRoot = self.rotateLeft()
                    # Continuar removiendo en el nuevo padre
                    return newRoot.remove(key, priority, removed)

            elif key <= self.key:
                if self.left is not None:
                    self.left = self.left.remove(key, priority, removed)
                    if self.left is not None:
                        self.left.parent = self
                return self
            else:
                if self.right is not None:
                    self.right = self.right.remove(key, priority, removed)
                    if self.right is not None:
                        self.right.parent = self
                return self

        def cleanUp(self):
            if self.left:
                self.left.cleanUp()
                self.left = None
            if self.right:
                self.right.cleanUp()
                self.right = None
            self.parent = None

        def checkTreapInvariants(self) -> bool:
            """
            Verifica recursivamente que se cumpla la propiedad de BST en claves
            y la propiedad de min-heap en prioridades.
            """
            # Chequeo subárbol izquierdo
            if self.left:
                # BST: clave del hijo izquierdo <= clave del padre
                if self.left.key > self.key:
                    return False
                # Heap: prioridad del hijo no debe ser más alta que la del padre
                if self.treap.hasHigherPriority(self.left.priority, self.priority):
                    return False
                if not self.left.checkTreapInvariants():
                    return False

            # Chequeo subárbol derecho
            if self.right:
                # BST: clave del hijo derecho > clave del padre
                if self.right.key <= self.key:
                    return False
                # Heap: prioridad del hijo no debe ser más alta que la del padre
                if self.treap.hasHigherPriority(self.right.priority, self.priority):
                    return False
                if not self.right.checkTreapInvariants():
                    return False

            return True

        def __repr__(self):
            return f"TreapNode(key={self.key}, priority={self.priority})"


if __name__ == "__main__":
    # Prueba básica
    treap = Treap[int, int]()
    treap.add(Treap.Entry(50, 30))
    treap.add(Treap.Entry(30, 20))
    treap.add(Treap.Entry(70, 40))
    treap.add(Treap.Entry(20, 10))
    treap.add(Treap.Entry(40, 25))
    
    print("Tamaño del treap:", treap.size())
    print("Altura del treap:", treap.height())
    print("Mínimo:", treap.min())
    print("Máximo:", treap.max())
    print("Buscar clave 30:", treap.search(30))
    print("Peek:", treap.peek())
    print("Top (extrae el máximo prioritario):", treap.top())
    print("Tamaño luego de top:", treap.size())

