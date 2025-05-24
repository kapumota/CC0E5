from __future__ import annotations
"""Motor híbrido de planificación y análisis de flujos
Estructuras de datos principales:
    * Heap máximo d-ario con actualizaciones dinámicas de prioridad (DHeap)
    * Índice probabilístico tipo skip-list para búsquedas con expectativa O(log N) (SkipListIndex)
    * Count–Min Sketch para estimación de frecuencias en flujos de datos (CountMinSketch)
    * Union–Find (DSU) con unión por tamaño y compresión de caminos (UnionFind)

Una clase liviana `HybridEngine` conecta estos componentes y ofrece
una fachada `process_event` para enrutar eventos heterogéneos provenientes
del planificador o del pipeline de análisis al módulo correspondiente.
Incluye una demo estilo CLI mínima bajo `__main__`.
"""

# Librerías estándar
from collections import defaultdict
from dataclasses import dataclass, field
import hashlib
import math
import os
import random
import time
from typing import Any, List, Optional, Sequence


# (a) Heap máximo d-ario con índice tipo skip-list                       #

class SkipListNode:
    """Nodo interno para la skip-list probabilística."""

    __slots__ = ("key", "value", "forward")

    def __init__(self, key: Any, value: Any, level: int):
        self.key = key
        self.value = value  # índice en el heap
        self.forward: List[Optional[SkipListNode]] = [None] * (level + 1)


class SkipListIndex:
    """Mapea *task_id* -> *índice en el heap* con operaciones esperadas en O(log N)."""

    P = 0.5  # distribución geométrica de niveles
    MAX_LEVEL = 32

    def __init__(self) -> None:
        self.level = 0
        self.head = SkipListNode(None, None, self.MAX_LEVEL)

    def _random_level(self) -> int:
        lvl = 0
        while random.random() < self.P and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def search(self, key: Any) -> Optional[int]:
        node = self.head
        for lvl in reversed(range(self.level + 1)):
            while node.forward[lvl] and node.forward[lvl].key < key:
                node = node.forward[lvl]
        node = node.forward[0]
        if node and node.key == key:
            return node.value
        return None

    def insert(self, key: Any, value: int) -> None:
        update = [None] * (self.MAX_LEVEL + 1)
        node = self.head
        for lvl in reversed(range(self.level + 1)):
            while node.forward[lvl] and node.forward[lvl].key < key:
                node = node.forward[lvl]
            update[lvl] = node
        node = node.forward[0]
        if node and node.key == key:  # actualizar si ya existe
            node.value = value
            return
        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.head
            self.level = lvl
        new_node = SkipListNode(key, value, lvl)
        for i in range(lvl + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def delete(self, key: Any) -> bool:
        update = [None] * (self.MAX_LEVEL + 1)
        node = self.head
        for lvl in reversed(range(self.level + 1)):
            while node.forward[lvl] and node.forward[lvl].key < key:
                node = node.forward[lvl]
            update[lvl] = node
        node = node.forward[0]
        if not node or node.key != key:
            return False
        for i in range(self.level + 1):
            if update[i].forward[i] is not node:
                break
            update[i].forward[i] = node.forward[i]
        while self.level > 0 and self.head.forward[self.level] is None:
            self.level -= 1
        return True


class DHeap:
    """Heap máximo genérico d-ario con operaciones O(log_d N) y actualización rápida.

    Un índice skip-list separado mapea *task_id* -> *índice en el array* para que
    `update_priority` ubique cualquier nodo en tiempo esperado O(log N)
    y luego haga `sift` en O(log_d N).
    """

    def __init__(self, d: int = 4):
        assert d >= 2, "El grado d debe ser ≥ 2"
        self.d = d
        self.heap: List[tuple[str, float]] = []  # (task_id, prioridad)
        self.index = SkipListIndex()  # task_id -> índice

    def _parent(self, idx: int) -> int:
        return (idx - 1) // self.d if idx else 0

    def _child_range(self, idx: int) -> range:
        start = idx * self.d + 1
        return range(start, min(start + self.d, len(self.heap)))

    def _sift_up(self, idx: int) -> None:
        while idx > 0:
            p = self._parent(idx)
            if self.heap[idx][1] <= self.heap[p][1]:
                break
            self._swap(idx, p)
            idx = p

    def _sift_down(self, idx: int) -> None:
        n = len(self.heap)
        while True:
            best = idx
            for c in self._child_range(idx):
                if self.heap[c][1] > self.heap[best][1]:
                    best = c
            if best == idx:
                break
            self._swap(idx, best)
            idx = best

    def _swap(self, i: int, j: int) -> None:
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.index.insert(self.heap[i][0], i)
        self.index.insert(self.heap[j][0], j)

    def insert(self, task_id: str, priority: float) -> None:
        idx = len(self.heap)
        self.heap.append((task_id, priority))
        self.index.insert(task_id, idx)
        self._sift_up(idx)

    def extract_max(self) -> Optional[tuple[str, float]]:
        if not self.heap:
            return None
        max_item = self.heap[0]
        last = self.heap.pop()
        self.index.delete(max_item[0])
        if self.heap:
            self.heap[0] = last
            self.index.insert(last[0], 0)
            self._sift_down(0)
        return max_item

    def update_priority(self, task_id: str, new_priority: float) -> bool:
        idx = self.index.search(task_id)
        if idx is None:
            return False
        old_task, old_priority = self.heap[idx]
        self.heap[idx] = (task_id, new_priority)
        # decidir dirección del sift
        if new_priority > old_priority:
            self._sift_up(idx)
        elif new_priority < old_priority:
            self._sift_down(idx)
        return True


# (b) Count–Min Sketch                                                      

class CountMinSketch:
    """Estimador probabilístico de frecuencias con garantías (ε, δ)."""

    def __init__(self, width: int, depth: int, seed: int | None = None):
        assert width > 0 and depth > 0, "Dimensiones inválidas para CMS"
        self.width = width
        self.depth = depth
        self.count: List[List[int]] = [[0] * width for _ in range(depth)]
        rng = random.Random(seed)
        self.seeds = [rng.randrange(1 << 31) for _ in range(depth)]
        self.total = 0

    def _hash(self, item: str | bytes, i: int) -> int:
        if isinstance(item, str):
            item = item.encode()
        h = hashlib.blake2b(item, digest_size=8, person=self.seeds[i].to_bytes(4, "little"))
        return int.from_bytes(h.digest(), "little") % self.width

    def update(self, item: str | bytes, count: int = 1) -> None:
        self.total += count
        for i in range(self.depth):
            j = self._hash(item, i)
            self.count[i][j] += count

    def estimate(self, item: str | bytes) -> int:
        return min(self.count[i][self._hash(item, i)] for i in range(self.depth))


# (c) Union–Find (Conjuntos Disjuntos)                                       #

class UnionFind:
    """Conectividad dinámica con unión por tamaño y compresión de caminos."""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x: int) -> int:
        # Compresión de caminos (recursiva)
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return False
        # Unión por tamaño (el menor se conecta al mayor)
        if self.size[xr] < self.size[yr]:
            xr, yr = yr, xr
        self.parent[yr] = xr
        self.size[xr] += self.size[yr]
        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


# (d) Orquestación de alto nivel                                             #

@dataclass
class HybridEngine:
    """Encaminador de eventos heterogéneos al subsistema apropiado."""

    heap_degree: int = 4
    cms_width: int = 2 ** 14
    cms_depth: int = 5
    uf_size: int = 10_000
    heap: DHeap = field(init=False)
    cms: CountMinSketch = field(init=False)
    uf: UnionFind = field(init=False)

    def __post_init__(self):
        self.heap = DHeap(self.heap_degree)
        self.cms = CountMinSketch(self.cms_width, self.cms_depth)
        self.uf = UnionFind(self.uf_size)

    def process_event(self, event: dict[str, Any]) -> Any:
        etype = event.get("type")
        match etype:
            case "task":
                action = event["action"]
                if action == "insert":
                    self.heap.insert(event["id"], event["priority"])
                elif action == "update":
                    self.heap.update_priority(event["id"], event["priority"])
                elif action == "extract":
                    return self.heap.extract_max()
            case "frequency":
                self.cms.update(event["item"], event.get("count", 1))
            case "query_freq":
                return self.cms.estimate(event["item"])
            case "union":
                self.uf.union(event["x"], event["y"])
            case "connected":
                return self.uf.connected(event["x"], event["y"])
            case _:
                raise ValueError(f"Tipo de evento desconocido: {etype}")


# Demostración rápida         

if __name__ == "__main__":
    engine = HybridEngine(heap_degree=4, uf_size=1000)
    # Carga de trabajo de ejemplo
    for i in range(100):
        engine.process_event({"type": "task", "action": "insert", "id": f"T{i}", "priority": random.random()})
    # Actualización de algunas prioridades
    for i in range(0, 100, 10):
        engine.process_event({"type": "task", "action": "update", "id": f"T{i}", "priority": random.random() + 1})
    # Extracción de los 5 con mayor prioridad
    print("Las cinco tareas con mayor prioridad:")
    for _ in range(5):
        print(engine.process_event({"type": "task", "action": "extract"}))
    # Frecuencia de flujo
    for word in ("red", "green", "blue", "red", "red", "green"):
        engine.process_event({"type": "frequency", "item": word})
    print("freq(red)=", engine.process_event({"type": "query_freq", "item": "red"}))
    # Demostración de Union–Find
    engine.process_event({"type": "union", "x": 1, "y": 2})
    engine.process_event({"type": "union", "x": 2, "y": 3})
    print("connected(1,3)=", engine.process_event({"type": "connected", "x": 1, "y": 3}))
