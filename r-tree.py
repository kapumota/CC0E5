from __future__ import annotations
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
from typing import List, Optional, Generator, Tuple, Union


class Rectangle:
    """
    Rectángulo mínimo contenedor (MBR).
    Atributos:
        min_x, min_y, max_x, max_y: coordenadas.
    """
    __slots__ = ("min_x", "min_y", "max_x", "max_y")

    def __init__(self, min_x: float, min_y: float, max_x: float, max_y: float) -> None:
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def area(self) -> float:
        """Calcula el área del rectángulo."""
        return (self.max_x - self.min_x) * (self.max_y - self.min_y)

    def intersection_area(self, other: Rectangle) -> float:
        """Calcula el área de intersección con otro rectángulo."""
        dx = min(self.max_x, other.max_x) - max(self.min_x, other.min_x)
        dy = min(self.max_y, other.max_y) - max(self.min_y, other.min_y)
        return dx * dy if dx > 0 and dy > 0 else 0.0

    def intersects(self, other: Rectangle) -> bool:
        """Determina si hay intersección con otro rectángulo."""
        return not (self.max_x < other.min_x or self.min_x > other.max_x
                    or self.max_y < other.min_y or self.min_y > other.max_y)

    def contains_rect(self, other: Rectangle) -> bool:
        """Comprueba si contiene completamente a otro rectángulo."""
        return (self.min_x <= other.min_x and self.max_x >= other.max_x
                and self.min_y <= other.min_y and self.max_y >= other.max_y)

    @staticmethod
    def union(rect1: Rectangle, rect2: Rectangle) -> Rectangle:
        """Devuelve el MBR que cubre ambos rectángulos."""
        return Rectangle(
            min(rect1.min_x, rect2.min_x),
            min(rect1.min_y, rect2.min_y),
            max(rect1.max_x, rect2.max_x),
            max(rect1.max_y, rect2.max_y)
        )


class RTreeNode:
    """
    Nodo de un R-Tree.

    Atributos:
        is_leaf: indica si es nodo hoja.
        parent: referencia al nodo padre.
        children: nodos hijos (si no es hoja).
        data_points: rectángulos en hojas.
        mbr: MBR que cubre hijos o data_points.
    """
    __slots__ = ("is_leaf", "parent", "children", "data_points", "mbr")

    def __init__(self, is_leaf: bool = True, parent: Optional[RTreeNode] = None) -> None:
        self.is_leaf = is_leaf
        self.parent = parent
        self.children: List[RTreeNode] = []
        self.data_points: List[Rectangle] = []
        self.mbr: Optional[Rectangle] = None

    def _recalculate_mbr(self) -> None:
        """
        Recalcula el MBR a partir de hijos o data_points y propaga al padre.
        """
        items = self.data_points if self.is_leaf else [c.mbr for c in self.children if c.mbr]
        self.mbr = None
        if items:
            m = items[0]
            for rect in items[1:]:
                m = Rectangle.union(m, rect)
            self.mbr = m
        if self.parent:
            self.parent._recalculate_mbr()

    def add_child(self, child: RTreeNode, recalc: bool = True) -> None:
        """
        Añade un nodo hijo e itera el recálculo del MBR ascendente.
        """
        child.parent = self
        self.children.append(child)
        if recalc:
            self._recalculate_mbr()

    def add_data_point(self, rect: Rectangle, recalc: bool = True) -> None:
        """
        Añade un rectángulo en hoja y recalcula mbr ascendente.
        """
        self.data_points.append(rect)
        if recalc:
            self._recalculate_mbr()


class RTree:
    """
    Estructura R-Tree con split cuadrático, reinserción diferida y delete.

    Parámetros:
        max_children: M, máximo de hijos/entries.
        min_fill: factor mínimo (por defecto 0.4).
        reinsert_count: número de entradas a reinsertar tras overflow.
    """
    def __init__(self, max_children: int = 4, min_fill: float = 0.4, reinsert_count: Optional[int] = None) -> None:
        if max_children < 2:
            raise ValueError("max_children debe ser >= 2")
        self.M = max_children
        self.m = max(2, int(math.ceil(self.M * min_fill)))
        self.reinsert_count = reinsert_count or max(1, int(self.M * 0.3))
        self.root = RTreeNode(is_leaf=True)

    def _choose_leaf(self, rect: Rectangle) -> RTreeNode:
        """
        Elige la hoja para insertar minimizando la ampliación de área.
        """
        node = self.root
        while not node.is_leaf:
            best, delta = None, float('inf')
            for c in node.children:
                assert c.mbr
                new_mbr = Rectangle.union(c.mbr, rect)
                enlargement = new_mbr.area() - c.mbr.area()
                if enlargement < delta:
                    best, delta = c, enlargement
            node = best  # type: ignore
        return node

    def insert(self, rect: Rectangle) -> None:
        """
        Inserta un nuevo rectángulo, con reinserción diferida y split.
        """
        leaf = self._choose_leaf(rect)
        leaf.add_data_point(rect)
        self._handle_overflow(leaf)

    def _pick_reinsert_entries(self, node: RTreeNode) -> List[Union[Rectangle, RTreeNode]]:
        """
        Selecciona las k entradas más alejadas del centro de MBR para reinserción.
        """
        center_x = (node.mbr.min_x + node.mbr.max_x) / 2  # type: ignore
        center_y = (node.mbr.min_y + node.mbr.max_y) / 2  # type: ignore
        def dist(entry):
            r = entry if isinstance(entry, Rectangle) else entry.mbr  # type: ignore
            cx = (r.min_x + r.max_x) / 2
            cy = (r.min_y + r.max_y) / 2
            return (cx - center_x)**2 + (cy - center_y)**2
        entries = node.data_points if node.is_leaf else node.children
        sorted_entries = sorted(entries, key=dist, reverse=True)
        return sorted_entries[:self.reinsert_count]

    def _handle_overflow(self, node: RTreeNode) -> None:
        """
        Si node excede capacidad, realiza reinserción diferida y split.
        """
        count = len(node.data_points) if node.is_leaf else len(node.children)
        if count <= self.M:
            return
        # Reinserción diferida: eliminar y guardar
        entries = self._pick_reinsert_entries(node)
        for e in entries:
            if node.is_leaf:
                node.data_points.remove(e)  # type: ignore
            else:
                node.children.remove(e)  # type: ignore
        node._recalculate_mbr()
        # Primero split del nodo reducido
        self._split_node(node)
        # Luego reinserción de todas las entradas
        for e in entries:
            if isinstance(e, Rectangle):
                self.insert(e)
            else:
                for r in (e.data_points if e.is_leaf else e.children):
                    self.insert(r)

    def _split_node(self, node: RTreeNode) -> None:
        """
        Divide node usando heurística cuadrática y garantiza min_fill.
        Eficiencia: recálculo único al final.
        """
        items = node.data_points if node.is_leaf else node.children  # type: ignore
        seed1, seed2 = self._pick_seeds_quadratic(items)
        g1 = RTreeNode(is_leaf=node.is_leaf)
        g2 = RTreeNode(is_leaf=node.is_leaf)
        g1.add_data_point(seed1, recalc=False) if node.is_leaf else g1.add_child(seed1, recalc=False)
        g2.add_data_point(seed2, recalc=False) if node.is_leaf else g2.add_child(seed2, recalc=False)
        remaining = [it for it in items if it not in (seed1, seed2)]
        while remaining:
            size1 = len(g1.data_points) if g1.is_leaf else len(g1.children)
            size2 = len(g2.data_points) if g2.is_leaf else len(g2.children)
            if size1 + len(remaining) == self.m:
                for it in remaining:
                    g1.add_data_point(it, recalc=False) if node.is_leaf else g1.add_child(it, recalc=False)
                break
            if size2 + len(remaining) == self.m:
                for it in remaining:
                    g2.add_data_point(it, recalc=False) if node.is_leaf else g2.add_child(it, recalc=False)
                break
            it = remaining.pop(0)
            rect = it if node.is_leaf else it.mbr  # type: ignore
            r1 = rect if g1.mbr is None else Rectangle.union(g1.mbr, rect)
            rect = it if node.is_leaf else it.mbr  # type: ignore
            r2 = rect if g2.mbr is None else Rectangle.union(g2.mbr, rect)
            d1 = r1.area() - (g1.mbr.area() if g1.mbr else 0)
            d2 = r2.area() - (g2.mbr.area() if g2.mbr else 0)
            target = g1 if d1 < d2 else g2
            if node.is_leaf:
                target.add_data_point(it, recalc=False)  # type: ignore
            else:
                target.add_child(it, recalc=False)  # type: ignore
        g1._recalculate_mbr()
        g2._recalculate_mbr()
        parent = node.parent
        if parent is None:
            new_root = RTreeNode(is_leaf=False)
            new_root.add_child(g1)
            new_root.add_child(g2)
            self.root = new_root
        else:
            parent.children.remove(node)
            parent.add_child(g1)
            parent.add_child(g2)
            self._handle_overflow(parent)

    def _pick_seeds_quadratic(self, items: List[Union[Rectangle, RTreeNode]]) -> Tuple:
        """
        Heurística cuadrática: elige par con mayor desperdicio si se agrupan.
        """
        max_waste = -1
        seeds = (items[0], items[1])
        for i in range(len(items)):
            for j in range(i+1, len(items)):
                a = items[i].mbr if isinstance(items[i], RTreeNode) else items[i]
                b = items[j].mbr if isinstance(items[j], RTreeNode) else items[j]
                waste = Rectangle.union(a, b).area() - a.area() - b.area()
                if waste > max_waste:
                    max_waste = waste
                    seeds = (items[i], items[j])
        return seeds

    def delete(self, rect: Rectangle) -> None:
        """
        Elimina un rectángulo y rebalancea nodos por debajo de min_fill (hojas e internos).
        """
        leaf = self._find_leaf(self.root, rect)
        if not leaf:
            return
        leaf.data_points.remove(rect)
        leaf._recalculate_mbr()
        Q: List[Union[Rectangle, RTreeNode]] = []
        n = leaf
        while n is not self.root:
            count = len(n.data_points) if n.is_leaf else	len(n.children)
            if count < self.m:
                parent = n.parent
                if parent:
                    parent.children.remove(n)
                if n.is_leaf:
                    Q.extend(n.data_points)
                else:
                    Q.extend(n.children)
                n = parent
            else:
                n =	n.parent  # type: ignore
        if self.root.children and not self.root.is_leaf	and len(self.root.children) == 1:
            self.root = self.root.children[0]
        for item in Q:
            if isinstance(item, Rectangle):
                self.insert(item)
            else:
                for r in (item.data_points if item.is_leaf else item.children):
                    self.insert(r)

    def _find_leaf(self, node: RTreeNode, rect: Rectangle) -> Optional[RTreeNode]:
        if node.is_leaf:
            return node if rect in node.data_points else None
        for c in node.children:
            if c.mbr and c.mbr.contains_rect(rect):
                res = self._find_leaf(c, rect)
                if res:
                    return	res
        return None

    def search(self, search_rect: Rectangle, max_results: Optional[int] = None) -> Generator[Rectangle, None, None]:
        """
        Generador de rectángulos que intersectan con search_rect.
        Valida que max_results sea None o >= 1.
        """
        if max_results is not None and max_results < 1:
            raise ValueError("max_results debe ser >= 1")
        count = 0
        def _rec(n: RTreeNode):
            nonlocal count
            if n.is_leaf:
                for r in n.data_points:
                    if search_rect.intersects(r):
                        yield r
                        count += 1
                        if max_results and	count >= max_results:
                            return
            else:
                for c in	n.children:
                    if c.mbr and search_rect.intersects(c.mbr):
                        yield from _rec(c)
                        if max_results and count >= max_results:
                            return
        yield from _rec(self.root)

    def visualize(self,
                  xlim: Tuple[float,	float] = (0, 100),
                  ylim: Tuple[float,	float] = (0, 100),
                  save_path: Optional[str] = None) -> None:
        """
        Muestra la estructura del R-Tree.

        Parámetros:
            xlim, ylim: límites del gráfico.
            save_path: ruta para guardar la figura (PNG, etc.).
        """
        fig, ax = plt.subplots()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        levels: List[List[RTreeNode]] = []
        queue: List[Tuple[RTreeNode, int]] = [(self.root, 0)]

        while queue:
            node, lvl = queue.pop(0)
            if len(levels) <= lvl:
                levels.append([])
            levels[lvl].append(node)
            if not node.is_leaf:
                for c in node.children:
                    queue.append((c, lvl + 1))

        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        labels = set()
        for lvl, nodes in	enumerate(levels):
            label = f"Nivel {lvl}"
            for n in nodes:
                if not n.mbr: continue
                rect = patches.Rectangle((n.mbr.min_x, n.mbr.min_y), n.mbr.max_x - n.mbr.min_x,	n.mbr.max_y - n.mbr.min_y,
                                         linewidth=2 if not n.is_leaf else 1,
                                         edgecolor=colors[lvl % len(colors)], facecolor='none', alpha=0.7)
                ax.add_patch(rect)
            labels.add((label, colors[lvl % len(colors)]))
        handles = [patches.Patch(edgecolor=color, facecolor='none', label=lbl) for lbl, color in labels]
        if handles:
            ax.legend(handles=handles, loc='upper right')

        if save_path:
            fig.savefig(save_path)
        ax.set_aspect('equal', 'box')
        plt.show()


# --- Pruebas unitarias con pytest ---
import pytest

def test_insert_and_search():
    tree = RTree(max_children=3, min_fill=0.4)
    rects = [Rectangle(0,0,1,1), Rectangle(2,2,3,3), Rectangle(1,1,2,2)]
    for r in rects:
        tree.insert(r)
    results = list(tree.search(Rectangle(1,1,1.5,1.5)))
    assert rects[2] in results

def test_split_and_overflow():
    tree = RTree(max_children=2, min_fill=0.4)
    for i in range(5):
        tree.insert(Rectangle(i,i,i+0.5,i+0.5))
    assert not tree.root.is_leaf

def test_delete_and_reinsert():
    tree = RTree(max_children=3)
    r = Rectangle(0,0,1,1)
    tree.insert(r)
    tree.delete(r)
    assert list(tree.search(r)) == []

def test_degenerate_rectangle():
    tree = RTree()
    r = Rectangle(0,0,0,0)
    tree.insert(r)
    assert list(tree.search(r)) == [r]

def test_empty_search():
    tree = RTree()
    assert list(tree.search(Rectangle(10,10,20,20))) == []

def test_exact_min_fill_split():
    M = 4
    tree = RTree(max_children=M, min_fill=0.5)
    coords = [(0,0), (1,1), (2,2), (3,3)]
    for x,y in coords:
        tree.insert(Rectangle(x,y,x+0.1,y+0.1))
    tree.insert(Rectangle(4,4,4.1,4.1))
    assert not tree.root.is_leaf

def test_root_collapse():
    tree = RTree(max_children=3)
    for i in range(3):
        tree.insert(Rectangle(i,i,i+0.5,i+0.5))
    for node in list(tree.search(Rectangle(0,0,10,10))):
        tree.delete(node)
    assert tree.root.is_leaf

def test_reinsertion_preserves_count():
    tree = RTree(max_children=3, reinsert_count=2)
    rects = [Rectangle(i, i, i+0.5, i+0.5) for i in range(6)]
    for r in rects:
        tree.insert(r)
    # tras overflow y reinserción, todos los rects deben estar presentes
    found = list(tree.search(Rectangle(0,0,10,10)))
    assert set(found) == set(rects)

if __name__ == '__main__':
    import pytest, sys
    sys.exit(pytest.main(["-v", __file__]))
