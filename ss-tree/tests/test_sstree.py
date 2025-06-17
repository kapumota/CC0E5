import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sstree.ss_tree import SsTree, Point

@pytest.fixture
def simple_tree():
    # Crea un árbol con puntos conocidos en R2
    pts = [Point([0, 0]), Point([1, 1]), Point([2, 2]), Point([3, 3])]
    tree = SsTree(pts, max_points=2)
    return tree

def test_insert_and_iter(simple_tree):
    # Iteración debe recorrer los 4 puntos iniciales
    result = list(simple_tree)
    coords = sorted(p.coordinates for p in result)
    expected = sorted([[0,0], [1,1], [2,2], [3,3]])
    assert coords == expected

def test_nearest_neighbour_exact(simple_tree):
    # El vecino más cercano de un punto existente debe ser el mismo
    target = Point([2, 2])
    nn = simple_tree.nearest_neighbour(target)
    assert nn is not None
    assert nn.coordinates == [2, 2]

def test_nearest_neighbour_between(simple_tree):
    # Para un punto intermedio, comprueba vecino correcto
    target = Point([1.1, 1.2])
    nn = simple_tree.nearest_neighbour(target)
    assert nn.coordinates in ([1,1], [2,2])
    # Verificar distancia mínima
    d = lambda a,b: ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5
    d_nn = d(nn.coordinates, target.coordinates)
    for c in [[1,1],[2,2]]:
        assert d_nn <= d(c, target.coordinates)

def test_to_from_dict_roundtrip(simple_tree):
    # Serializar y reconstruir, comparar contenido
    data = simple_tree.to_dict()
    new_tree = SsTree.from_dict(data)
    original = sorted([p.coordinates for p in simple_tree])
    recon = sorted([p.coordinates for p in new_tree])
    assert original == recon
    # Verificar que nearest_neighbour sigue funcionando
    target = Point([0.9,0.9])
    assert new_tree.nearest_neighbour(target).coordinates == [1,1]

def test_empty_tree():
    # Árbol vacío devuelve None
    tree = SsTree([], max_points=3)
    assert tree.is_empty()
    assert tree.nearest_neighbour(Point([0,0])) is None
    assert list(tree) == []

def test_invalid_dimension():
    # Insertar punto de dimensión distinta lanza error
    tree = SsTree([Point([0,0])], max_points=2)
    with pytest.raises(ValueError):
        tree.insert(Point([1,1,1]))
    with pytest.raises(ValueError):
        tree.nearest_neighbour(Point([1,2,3]))

@pytest.mark.parametrize("pts, target, expected", [
    ([[0]], [0], [0]),
    ([[0,0,0],[1,1,1]], [0.4,0.4,0.4], [0,0,0]),
])
def test_high_dimensional(pts, target, expected):
    # Funcionamiento en espacios de más dimensiones
    points = [Point(p) for p in pts]
    tree = SsTree(points, max_points=1)
    nn = tree.nearest_neighbour(Point(target))
    assert nn.coordinates == expected