#!/usr/bin/env python3
"""
Implementación de RandomizedTreap. Un RandomizedTreap es un árbol de búsqueda cuya estructura depende de
la asignación aleatoria de prioridades (de tipo float) a los elementos,
lo que garantiza que, en promedio, el árbol esté balanceado.
Se utiliza la implementación de Treap definida en treap.py.
"""

import random
from typing import Optional, Generic, TypeVar
from treap import Treap

T = TypeVar('T')

class RandomizedTreap(Generic[T]):
    def __init__(self):
        self.treap: Treap[T, float] = Treap()
        self.rnd = random.Random()

    def add(self, element: T) -> bool:
        entry = Treap.Entry(element, self.rnd.random())
        return self.treap.add(entry)

    def remove(self, element: T) -> bool:
        return self.treap.removeKey(element)

    def clear(self) -> None:
        self.treap.clear()

    def min(self) -> Optional[T]:
        return self.treap.min()

    def max(self) -> Optional[T]:
        return self.treap.max()

    def search(self, element: T) -> Optional[T]:
        return self.treap.search(element)

    def isEmpty(self) -> bool:
        return self.treap.isEmpty()

    def size(self) -> int:
        return self.treap.size()

    def height(self) -> int:
        return self.treap.height()

    def _checkTreapInvariants(self) -> bool:
        return self.treap.checkTreapInvariants()

    def _checkBSTInvariants(self) -> bool:
        return self.treap.checkBSTInvariants()


if __name__ == "__main__":
    rt = RandomizedTreap[int]()
    rt.add(50)
    rt.add(30)
    rt.add(70)
    rt.add(20)
    rt.add(40)

    print("Tamaño:", rt.size())
    print("Altura:", rt.height())
    print("Mínimo:", rt.min())
    print("Máximo:", rt.max())
    print("Buscar 30:", rt.search(30))
    print("Invariantes treap válidas:", rt._checkTreapInvariants())
    print("Invariantes BST válidas:", rt._checkBSTInvariants())

