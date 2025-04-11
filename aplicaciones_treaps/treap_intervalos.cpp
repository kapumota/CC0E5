#include <bits/stdc++.h>
#include <cassert>
#include <chrono>
#include <functional>
using namespace std;

/*
 * Ejemplo de implementación de Treap que soporta:
 *  1) Inserción de claves.
 *  2) Eliminación de claves.
 *  3) Búsqueda de claves.
 *  4) Obtención del k-ésimo elemento (Order Statistics).
 * Adicionalmente, se muestra una estructura estilo "Treap de Intervalos"
 * que nos permite almacenar intervalos [l, r] y hacer consultas de intersección.
 *
 * Se incluyen pruebas unitarias y funciones de profiling.
 */


// Treap de enteros 

struct TreapNode {
    int key;          // Clave (o valor) que almacena
    int priority;     // Prioridad aleatoria para mantener la propiedad de heap
    int sizeSubtree;  // Tamaño del subárbol (para order statistics)
    
    TreapNode* left;
    TreapNode* right;

    // Constructor
    TreapNode(int _key) {
        key = _key;
        priority = rand(); // Se puede utilizar mt19937 para mayor calidad en la aleatoriedad
        sizeSubtree = 1;
        left = right = nullptr;
    }
};

int getSize(TreapNode* node) {
    return (node == nullptr) ? 0 : node->sizeSubtree;
}

void updateSize(TreapNode* node) {
    if (node) {
        node->sizeSubtree = 1 + getSize(node->left) + getSize(node->right);
    }
}

TreapNode* rotateRight(TreapNode* Q) {
    TreapNode* P = Q->left;
    Q->left = P->right;
    P->right = Q;
    updateSize(Q);
    updateSize(P);
    return P;
}

TreapNode* rotateLeft(TreapNode* P) {
    TreapNode* Q = P->right;
    P->right = Q->left;
    Q->left = P;
    updateSize(P);
    updateSize(Q);
    return Q;
}

TreapNode* treapInsert(TreapNode* root, int key) {
    if (!root) {
        return new TreapNode(key);
    }
    if (key < root->key) {
        root->left = treapInsert(root->left, key);
        if (root->left->priority > root->priority) {
            root = rotateRight(root);
        }
    } else {
        // Para simplificar, si key == root->key se inserta a la derecha.
        root->right = treapInsert(root->right, key);
        if (root->right->priority > root->priority) {
            root = rotateLeft(root);
        }
    }
    updateSize(root);
    return root;
}

bool treapFind(TreapNode* root, int key) {
    if (!root) return false;
    if (root->key == key) return true;
    if (key < root->key) return treapFind(root->left, key);
    else return treapFind(root->right, key);
}

TreapNode* treapErase(TreapNode* root, int key) {
    if (!root) return nullptr;
    if (key < root->key) {
        root->left = treapErase(root->left, key);
    } else if (key > root->key) {
        root->right = treapErase(root->right, key);
    } else {
        // Nodo encontrado, se procede a bajarlo y eliminarlo
        if (!root->left) {
            TreapNode* temp = root->right;
            delete root;
            return temp;
        } else if (!root->right) {
            TreapNode* temp = root->left;
            delete root;
            return temp;
        } else {
            if (root->left->priority > root->right->priority) {
                root = rotateRight(root);
                root->right = treapErase(root->right, key);
            } else {
                root = rotateLeft(root);
                root->left = treapErase(root->left, key);
            }
        }
    }
    updateSize(root);
    return root;
}

int treapGetKth(TreapNode* root, int k) {
    // Se asume que k es válido: 1 <= k <= tamaño del subárbol
    if (!root) return -1;
    int sizeLeft = getSize(root->left);
    if (k == sizeLeft + 1) {
        return root->key;
    } else if (k <= sizeLeft) {
        return treapGetKth(root->left, k);
    } else {
        return treapGetKth(root->right, k - sizeLeft - 1);
    }
}

void inorder(TreapNode* root) {
    if (!root) return;
    inorder(root->left);
    cout << root->key << " ";
    inorder(root->right);
}


// Treap de intervalos
 

struct Interval {
    int start;
    int end;
    Interval(int s, int e) : start(s), end(e) {}
};

struct IntervalTreapNode {
    Interval interval;
    int priority;
    int maxEnd; // Máximo valor 'end' en el subárbol
    IntervalTreapNode* left;
    IntervalTreapNode* right;

    IntervalTreapNode(Interval i)
        : interval(i), priority(rand()), maxEnd(i.end), left(nullptr), right(nullptr) {}
};

void updateMaxEnd(IntervalTreapNode* node) {
    if (!node) return;
    node->maxEnd = node->interval.end;
    if (node->left) {
        node->maxEnd = max(node->maxEnd, node->left->maxEnd);
    }
    if (node->right) {
        node->maxEnd = max(node->maxEnd, node->right->maxEnd);
    }
}

IntervalTreapNode* rotateRight(IntervalTreapNode* Q) {
    IntervalTreapNode* P = Q->left;
    Q->left = P->right;
    P->right = Q;
    updateMaxEnd(Q);
    updateMaxEnd(P);
    return P;
}

IntervalTreapNode* rotateLeft(IntervalTreapNode* P) {
    IntervalTreapNode* Q = P->right;
    P->right = Q->left;
    Q->left = P;
    updateMaxEnd(P);
    updateMaxEnd(Q);
    return Q;
}

IntervalTreapNode* intervalTreapInsert(IntervalTreapNode* root, Interval i) {
    if (!root) {
        return new IntervalTreapNode(i);
    }
    // Ordenamos por el inicio del intervalo
    if (i.start < root->interval.start) {
        root->left = intervalTreapInsert(root->left, i);
        if (root->left->priority > root->priority) {
            root = rotateRight(root);
        }
    } else {
        root->right = intervalTreapInsert(root->right, i);
        if (root->right->priority > root->priority) {
            root = rotateLeft(root);
        }
    }
    updateMaxEnd(root);
    return root;
}

bool doOverlap(const Interval& i1, const Interval& i2) {
    return !(i1.end < i2.start || i2.end < i1.start);
}

void intersectingIntervals(IntervalTreapNode* root, Interval i, vector<Interval>& result) {
    if (!root) return;
    if (doOverlap(root->interval, i)) {
        result.push_back(root->interval);
    }
    if (root->left && root->left->maxEnd >= i.start) {
        intersectingIntervals(root->left, i, result);
    }
    if (root->interval.start <= i.end) {
        intersectingIntervals(root->right, i, result);
    }
}

void inorderIntervals(IntervalTreapNode* root) {
    if (!root) return;
    inorderIntervals(root->left);
    cout << "[" << root->interval.start << ", " << root->interval.end << "] "
         << "(maxEnd: " << root->maxEnd << ")  ";
    inorderIntervals(root->right);
}

// Pruebas Unitarias

void runUnitTests() {
    cout << "Ejecutando pruebas unitarias para el Treap de enteros..." << endl;
    
    //  Test del treap de enteros
    TreapNode* testRoot = nullptr;
    vector<int> testValues = {40, 20, 60, 10, 30, 50, 70};
    for (int v : testValues) {
        testRoot = treapInsert(testRoot, v);
    }
    
    // Verificamos el in-order (debe ser ordenado)
    vector<int> inorderResult;
    function<void(TreapNode*)> collectInorder = [&](TreapNode* node) {
        if (!node) return;
        collectInorder(node->left);
        inorderResult.push_back(node->key);
        collectInorder(node->right);
    };
    collectInorder(testRoot);
    vector<int> expected = {10, 20, 30, 40, 50, 60, 70};
    assert(inorderResult == expected);
    cout << "   - Test de recorrido in-order: OK" << endl;
    
    // Test de búsqueda
    assert(treapFind(testRoot, 30) == true);
    assert(treapFind(testRoot, 100) == false);
    cout << "   - Test de búsqueda: OK" << endl;
    
    // Test del k-ésimo elemento (1-indexado)
    int kth = treapGetKth(testRoot, 3); // Debe ser 30
    assert(kth == 30);
    cout << "   - Test de k-ésimo elemento: OK" << endl;
    
    // Test de eliminación: borramos 20 y verificamos
    testRoot = treapErase(testRoot, 20);
    inorderResult.clear();
    collectInorder(testRoot);
    expected = {10, 30, 40, 50, 60, 70};
    assert(inorderResult == expected);
    cout << "   - Test de eliminación: OK" << endl;
    
    // Test del treap de intervalos 
    cout << "Ejecutando pruebas unitarias para el Treap de intervalos..." << endl;
    IntervalTreapNode* intervalRoot = nullptr;
    vector<Interval> testIntervals = {
        Interval(15, 20),
        Interval(10, 30),
        Interval(17, 19),
        Interval(5, 20),
        Interval(12, 15),
        Interval(30, 40)
    };
    for (auto& itv : testIntervals) {
        intervalRoot = intervalTreapInsert(intervalRoot, itv);
    }
    
    // Consulta de intersección con [14, 16]
    Interval queryInterval(14, 16);
    vector<Interval> overlaps;
    intersectingIntervals(intervalRoot, queryInterval, overlaps);
    // Esperamos que se solapen los intervalos: [15,20], [10,30], [5,20] y [12,15]
    int expectedOverlapsCount = 4;
    assert(overlaps.size() == (size_t)expectedOverlapsCount);
    cout << "   - Test de intersección de intervalos: OK" << endl;
    
    cout << "Todas las pruebas unitarias pasaron correctamente." << endl;
}


// Profiling
 

void runProfiling() {
    cout << "Iniciando profiling para el Treap de enteros..." << endl;
    const int n = 100000;  // Número de elementos para el test de performance
    TreapNode* root = nullptr;
    
    // Profiling de inserción
    cout << "Insertando " << n << " elementos..." << endl;
    auto start = chrono::steady_clock::now();
    for (int i = 0; i < n; i++) {
        root = treapInsert(root, rand());
    }
    auto end = chrono::steady_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
    cout << "  Tiempo de inserción: " << duration.count() << " ms" << endl;
    
    // Profiling de búsqueda
    start = chrono::steady_clock::now();
    int foundCount = 0;
    for (int i = 0; i < n; i++) {
        if (treapFind(root, i))
            foundCount++;
    }
    end = chrono::steady_clock::now();
    duration = chrono::duration_cast<chrono::milliseconds>(end - start);
    cout << " Tiempo de búsqueda: " << duration.count() << " ms (encontrados " << foundCount << " elementos)" << endl;
    
    // Profiling de consultas al k-ésimo elemento (se hacen 100 consultas distribuidas)
    start = chrono::steady_clock::now();
    for (int k = 1; k <= n; k += n/100) {
        volatile int kth = treapGetKth(root, k);
        (void) kth;  // Evita optimizaciones que eliminen la consulta
    }
    end = chrono::steady_clock::now();
    duration = chrono::duration_cast<chrono::milliseconds>(end - start);
    cout << "  Tiempo de consultas k-ésimas: " << duration.count() << " ms" << endl;
}

 
// Función Principal (main)
 

int main(int argc, char* argv[]) {
    // Inicializamos la semilla para la generación de números aleatorios
    srand((unsigned)time(nullptr));

    // Si se pasa un argumento, se elige el modo de ejecución
    if (argc > 1) {
        string mode = argv[1];
        if (mode == "test") {
            runUnitTests();
            return 0;
        } else if (mode == "profile") {
            runProfiling();
            return 0;
        }
    }
    
    //Demostraciones 
    cout << "Demostración" << endl;
    TreapNode* rootInt = nullptr;
    
    vector<int> valores = {50, 30, 20, 40, 70, 60, 80};
    for (int v : valores) {
        rootInt = treapInsert(rootInt, v);
    }
    
    cout << "Treap (in-order): ";
    inorder(rootInt);
    cout << endl;
    
    cout << "Buscando 40 en el treap: " << (treapFind(rootInt, 40) ? "Encontrado" : "No encontrado") << endl;
    
    cout << "Eliminamos el valor 30" << endl;
    rootInt = treapErase(rootInt, 30);
    cout << "Treap (in-order): ";
    inorder(rootInt);
    cout << endl;
    
    cout << "El 3er elemento del treap es: " << treapGetKth(rootInt, 3) << endl;
    
    cout << "\nDemostración de intervalos" << endl;
    IntervalTreapNode* rootInterval = nullptr;
    vector<Interval> intervalos = {
        Interval(15, 20),
        Interval(10, 30),
        Interval(17, 19),
        Interval(5, 20),
        Interval(12, 15),
        Interval(30, 40)
    };
    for (auto& itv : intervalos) {
        rootInterval = intervalTreapInsert(rootInterval, itv);
    }
    
    cout << "Treap de intervalos (in-order):" << endl;
    inorderIntervals(rootInterval);
    cout << endl;
    
    Interval queryInterval(14, 16);
    cout << "Buscando intervalos que se intersecten con [" 
         << queryInterval.start << ", " << queryInterval.end << "]" << endl;
    vector<Interval> intersectados;
    intersectingIntervals(rootInterval, queryInterval, intersectados);
    
    cout << "Intervalos intersectados:" << endl;
    for (auto& iv : intersectados) {
        cout << "[" << iv.start << ", " << iv.end << "]" << endl;
    }
    
    cout << "\nFin de la demostración." << endl;
    return 0;
}

