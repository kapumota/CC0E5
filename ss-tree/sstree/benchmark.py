import time
import random
import argparse
from sstree.ss_tree import SsTree, Point
#python -m sstree.benchmark -n 20000 -d 5 -q 1000 -m 8

def generate_random_points(n: int, dim: int) -> list[Point]:
    """Genera n puntos aleatorios en dimensión dim con coordenadas en [0,1)."""
    return [Point([random.random() for _ in range(dim)]) for _ in range(n)]


def benchmark_construction(points: list[Point], max_points: int) -> float:
    """Mide el tiempo para construir un SsTree con los puntos dados."""
    start = time.perf_counter()
    _ = SsTree(points, max_points=max_points)
    return time.perf_counter() - start


def benchmark_insertion(points: list[Point], max_points: int) -> float:
    """Mide el tiempo de inserción secuencial en un árbol vacío."""
    tree = SsTree([], max_points=max_points)
    start = time.perf_counter()
    for p in points:
        tree.insert(p)
    return time.perf_counter() - start


def benchmark_queries(tree: SsTree, queries: list[Point]) -> float:
    """Mide el tiempo de consultas nearest_neighbour."""
    start = time.perf_counter()
    for q in queries:
        _ = tree.nearest_neighbour(q)
    return time.perf_counter() - start


def main():
    parser = argparse.ArgumentParser(description="Benchmark de SsTree")
    parser.add_argument("-n", type=int, default=10000, help="Número de puntos a generar")
    parser.add_argument("-d", type=int, default=10, help="Dimensionalidad de los puntos")
    parser.add_argument("-q", type=int, default=1000, help="Número de consultas NN")
    parser.add_argument("-m", type=int, default=10, help="max_points por nodo")
    args = parser.parse_args()

    print(f"Generando {args.n} puntos en R^{args.d}...")
    points = generate_random_points(args.n, args.d)
    print("Construyendo árbol...")
    t_build = benchmark_construction(points, args.m)
    print(f"Tiempo construcción: {t_build:.4f} s")

    print("Insertando secuencialmente en árbol vacío...")
    t_insert = benchmark_insertion(points, args.m)
    print(f"Tiempo inserción: {t_insert:.4f} s")

    tree = SsTree(points, max_points=args.m)
    queries = generate_random_points(args.q, args.d)
    print(f"Realizando {args.q} búsquedas nearest neighbour...")
    t_query = benchmark_queries(tree, queries)
    print(f"Tiempo consultas: {t_query:.4f} s")

if __name__ == "__main__":
    main()