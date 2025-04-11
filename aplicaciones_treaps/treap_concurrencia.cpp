#include <bits/stdc++.h>
#include <shared_mutex>
#include <thread>
#include <chrono>
#include <cassert>
using namespace std;

/*
  Ejemplo de "Treap Concurrente" en C++.
  - Se usa un std::shared_mutex para permitir múltiples lecturas concurrentes
    (búsquedas) y bloqueos exclusivos para inserción y eliminación.
  - Se agregan pruebas unitarias y profiling.

*/

// Estructura del nodo 
// 
struct Node {
    int key;          // Clave almacenada
    int priority;     // Prioridad para el Treap (regla de heap)
    int subtreeSize;  // Tamaño del subárbol (para estadísticas u order statistics)

    Node* left;
    Node* right;

    Node(int k)
        : key(k), priority(rand()), subtreeSize(1), left(nullptr), right(nullptr) {}
};

// 
// Funciones auxiliares
// 
int getSize(Node* node) {
    return (node ? node->subtreeSize : 0);
}

void updateSize(Node* node) {
    if (!node) return;
    node->subtreeSize = 1 + getSize(node->left) + getSize(node->right);
}

Node* rotateRight(Node* Q) {
    Node* P = Q->left;
    Q->left = P->right;
    P->right = Q;
    updateSize(Q);
    updateSize(P);
    return P;
}

Node* rotateLeft(Node* P) {
    Node* Q = P->right;
    P->right = Q->left;
    Q->left = P;
    updateSize(P);
    updateSize(Q);
    return Q;
}

Node* treapInsert(Node* root, int key) {
    if (!root) {
        return new Node(key);
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

bool treapFind(Node* root, int key) {
    if (!root) return false;
    if (root->key == key) return true;
    if (key < root->key)
        return treapFind(root->left, key);
    else
        return treapFind(root->right, key);
}

Node* treapErase(Node* root, int key) {
    if (!root) return nullptr;
    if (key < root->key) {
        root->left = treapErase(root->left, key);
    } else if (key > root->key) {
        root->right = treapErase(root->right, key);
    } else {
        // Nodo encontrado, proceder a borrar
        if (!root->left) {
            Node* temp = root->right;
            delete root;
            return temp;
        } else if (!root->right) {
            Node* temp = root->left;
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

void inorder(Node* root) {
    if (!root) return;
    inorder(root->left);
    cout << root->key << " ";
    inorder(root->right);
}

// Clase que envuelve el treap con concurrencia  

class ConcurrentTreap {
private:
    Node* root;
    mutable std::shared_mutex treeMutex;

    // Funciones internas (sin protección de hilos; se asume que el llamador gestiona la sincronización)
    Node* insertInternal(Node* r, int key) {
        return treapInsert(r, key);
    }
    Node* eraseInternal(Node* r, int key) {
        return treapErase(r, key);
    }
    bool findInternal(Node* r, int key) const {
        return treapFind(r, key);
    }
    void inorderInternal(Node* r) const {
        if (!r) return;
        inorderInternal(r->left);
        cout << r->key << " ";
        inorderInternal(r->right);
    }
    // Función auxiliar para obtener los elementos en orden
    void inorderToVector(Node* r, vector<int>& vec) const {
        if (!r) return;
        inorderToVector(r->left, vec);
        vec.push_back(r->key);
        inorderToVector(r->right, vec);
    }

public:
    ConcurrentTreap() : root(nullptr) {
        srand((unsigned) time(nullptr));
    }

    // Inserta una clave (bloqueo exclusivo)
    void insert(int key) {
        unique_lock<shared_mutex> lock(treeMutex);
        root = insertInternal(root, key);
    }

    // Elimina una clave (bloqueo exclusivo)
    void erase(int key) {
        unique_lock<shared_mutex> lock(treeMutex);
        root = eraseInternal(root, key);
    }

    // Busca una clave (bloqueo compartido)
    bool find(int key) const {
        shared_lock<shared_mutex> lock(treeMutex);
        return findInternal(root, key);
    }

    // Imprime en in-order (bloqueo compartido)
    void printInorder() const {
        shared_lock<shared_mutex> lock(treeMutex);
        inorderInternal(root);
        cout << endl;
    }

    // Devuelve un vector con el recorrido in-order (útil para pruebas unitarias)
    vector<int> getInorder() const {
        vector<int> vec;
        shared_lock<shared_mutex> lock(treeMutex);
        inorderToVector(root, vec);
        return vec;
    }
};

// 
// Pruebas unitarias
// 
void runUnitTests() {
    cout << "Ejecutando pruebas unitarias" << endl;
    ConcurrentTreap ctreap;

    // Prueba 1: Inserción y orden in-order
    vector<int> keys = {20, 10, 30, 5, 15};
    for (int k : keys) {
        ctreap.insert(k);
    }
    vector<int> inord = ctreap.getInorder();
    vector<int> expected = {5, 10, 15, 20, 30};
    assert(inord == expected);
    cout << "- Test de inserción y recorrido in-order: OK" << endl;

    // Prueba 2: Búsqueda
    assert(ctreap.find(15) == true);
    assert(ctreap.find(100) == false);
    cout << "- Test de búsqueda: OK" << endl;

    // Prueba 3: Eliminación
    ctreap.erase(10); // Eliminar el valor 10
    inord = ctreap.getInorder();
    expected = {5, 15, 20, 30};
    assert(inord == expected);
    cout << "   - Test de eliminación: OK" << endl;

    cout << "Todas las pruebas unitarias pasaron correctamente." << endl;
}


// Profiling                        
void runProfiling() {
    cout << "Iniciando profiling del Treap concurrente" << endl;
    ConcurrentTreap ctreap;
    const int numThreads = 8;
    const int operationsPerThread = 10000;
    const int rangeKeys = 1000;

    auto start = chrono::steady_clock::now();
    vector<thread> threads;
    threads.reserve(numThreads);

    auto treapWorker = [&ctreap, operationsPerThread, rangeKeys](int threadId) {
        mt19937 rng(threadId * 12345 + (unsigned) time(nullptr));
        uniform_int_distribution<int> distOp(0, 2);       // 0 -> insert, 1 -> find, 2 -> erase
        uniform_int_distribution<int> distKey(1, rangeKeys);

        for (int i = 0; i < operationsPerThread; i++) {
            int op = distOp(rng);
            int key = distKey(rng);
            switch (op) {
                case 0:
                    ctreap.insert(key);
                    break;
                case 1:
                    ctreap.find(key);
                    break;
                case 2:
                    ctreap.erase(key);
                    break;
            }
            // Pequeño sleep artificial para simular carga
            this_thread::sleep_for(chrono::microseconds(5));
        }
    };

    // Lanzar hilos
    for (int i = 0; i < numThreads; i++) {
        threads.emplace_back(treapWorker, i);
    }
    for (auto& t : threads) {
        t.join();
    }
    auto end = chrono::steady_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);

    cout << " Tiempo total en profiling: " << duration.count() << " ms" << endl;
    cout << " Número de elementos finales: " << ctreap.getInorder().size() << endl;
}


// Demostración                 

void runDemo() {
    ConcurrentTreap ctreap;
    int numThreads = 4;
    int operationsPerThread = 200;   // Operaciones que realizará cada hilo
    int rangeKeys = 100;             // Rango de claves (1..100)

    cout << "Demostración de treap concurrente" << endl;
    cout << "Lanzando " << numThreads << " hilos." << endl;

    auto treapWorker = [&ctreap, operationsPerThread, rangeKeys](int threadId) {
        mt19937 rng(threadId * 12345 + (unsigned) time(nullptr));
        uniform_int_distribution<int> distOp(0, 2);       // 0: insert, 1: find, 2: erase
        uniform_int_distribution<int> distKey(1, rangeKeys);

        for (int i = 0; i < operationsPerThread; i++) {
            int op = distOp(rng);
            int key = distKey(rng);
            switch (op) {
                case 0:
                    ctreap.insert(key);
                    break;
                case 1:
                    ctreap.find(key);
                    break;
                case 2:
                    ctreap.erase(key);
                    break;
            }
            this_thread::sleep_for(chrono::microseconds(10));
        }
    };

    vector<thread> threads;
    threads.reserve(numThreads);
    for (int i = 0; i < numThreads; i++) {
        threads.emplace_back(treapWorker, i);
    }
    for (auto& t : threads) {
        t.join();
    }

    cout << "\nContenido final del Treap (in-order):" << endl;
    ctreap.printInorder();

    cout << "\nEjemplo de búsquedas secuenciales:" << endl;
    for (int keyTest : {10, 50, 75, 101}) {
        bool found = ctreap.find(keyTest);
        cout << "  Buscar " << keyTest << ": " << (found ? "Encontrado" : "No encontrado") << endl;
    }
    cout << "\nFin de la demostración concurrente." << endl;
}

// Función principal 

int main(int argc, char* argv[]) {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

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

    // Si no se pasan argumentos, se ejecuta la demostración por defecto.
    runDemo();
    return 0;
}

