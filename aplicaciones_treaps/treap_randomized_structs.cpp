#include <bits/stdc++.h>
using namespace std;
using ll = long long;

/*
 Ejemplo de árboles aleatorizados: treaps, skiplist y BST

Comparación con BST clásico (no balanceado) y un SkipList simplificado.

Este ejemplo muestra:

1) Implementación de un Treap (con prioridad aleatoria).
2) Implementación de un BST clásico (no balanceado).
3) Implementación simplificada de un SkipList.
4) Inserción de muchas claves aleatorias en cada estructura.
5) Búsquedas y medición de tiempo, además de la “altura” (o longitud base en el SkipList).

 Con ello se ilustra cómo la aleatoriedad en el Treap y en el SkipList
 contribuye a mantener tiempos esperados O(log n), a diferencia de un BST clásico
 que puede deteriorarse en el peor caso.

  

// Parte 1: BST clásico (no balance) 
*/
struct BSTNode {
    int key;
    BSTNode* left;
    BSTNode* right;
    BSTNode(int k) : key(k), left(nullptr), right(nullptr) {}
};

BSTNode* bstInsert(BSTNode* root, int key) {
    if (!root)
        return new BSTNode(key);
    if (key < root->key)
        root->left = bstInsert(root->left, key);
    else if (key > root->key)
        root->right = bstInsert(root->right, key);
    return root;
}

bool bstFind(BSTNode* root, int key) {
    if (!root) return false;
    if (root->key == key) return true;
    return (key < root->key) ? bstFind(root->left, key) : bstFind(root->right, key);
}

int bstHeight(BSTNode* root) {
    if (!root) return 0;
    return 1 + max(bstHeight(root->left), bstHeight(root->right));
}

// Parte 2: Treap (árbol aleatorizado)
 
struct TreapNode {
    int key;
    int priority; // aleatoria
    TreapNode* left;
    TreapNode* right;
    TreapNode(int k) : key(k), priority(rand()), left(nullptr), right(nullptr) {}
};

TreapNode* rotateRight(TreapNode* Q) {
    TreapNode* P = Q->left;
    Q->left = P->right;
    P->right = Q;
    return P;
}
TreapNode* rotateLeft(TreapNode* P) {
    TreapNode* Q = P->right;
    P->right = Q->left;
    Q->left = P;
    return Q;
}

TreapNode* treapInsert(TreapNode* root, int key) {
    if (!root) return new TreapNode(key);
    if (key < root->key) {
        root->left = treapInsert(root->left, key);
        if (root->left->priority > root->priority)
            root = rotateRight(root);
    } else if (key > root->key) {
        root->right = treapInsert(root->right, key);
        if (root->right->priority > root->priority)
            root = rotateLeft(root);
    }
    return root;
}

bool treapFind(TreapNode* root, int key) {
    if (!root) return false;
    if (root->key == key) return true;
    return (key < root->key) ? treapFind(root->left, key) : treapFind(root->right, key);
}

int treapHeight(TreapNode* root) {
    if (!root) return 0;
    return 1 + max(treapHeight(root->left), treapHeight(root->right));
}

// Parte 3: Skip List simplificado 
 
static const int MAX_LEVEL = 16;
static const double P = 0.5;

struct SkipListNode {
    int key;
    vector<SkipListNode*> forward;
    SkipListNode(int k, int level) : key(k), forward(level+1, nullptr) {}
};

struct SkipList {
    SkipListNode* header;
    int level; // nivel actual (0-based)
    SkipList() : level(0) {
        header = new SkipListNode(numeric_limits<int>::min(), MAX_LEVEL);
    }
};

int randomLevel() {
    int lvl = 0;
    while (((double)rand() / RAND_MAX) < P && lvl < MAX_LEVEL-1)
        lvl++;
    return lvl;
}

void skipListInsert(SkipList &sl, int key) {
    vector<SkipListNode*> update(MAX_LEVEL, nullptr);
    SkipListNode* current = sl.header;
    for (int i = sl.level; i >= 0; i--) {
        while (current->forward[i] && current->forward[i]->key < key)
            current = current->forward[i];
        update[i] = current;
    }
    current = current->forward[0];
    if (!current || current->key != key) {
        int newLevel = randomLevel();
        if (newLevel > sl.level) {
            for (int i = sl.level+1; i <= newLevel; i++)
                update[i] = sl.header;
            sl.level = newLevel;
        }
        SkipListNode* newNode = new SkipListNode(key, newLevel);
        for (int i = 0; i <= newLevel; i++) {
            newNode->forward[i] = update[i]->forward[i];
            update[i]->forward[i] = newNode;
        }
    }
}

bool skipListFind(const SkipList &sl, int key) {
    SkipListNode* current = sl.header;
    for (int i = sl.level; i >= 0; i--) {
        while (current->forward[i] && current->forward[i]->key < key)
            current = current->forward[i];
    }
    current = current->forward[0];
    return (current && current->key == key);
}

// Para el "skip list", tomamos la cantidad de nodos en el nivel base como medida
int skipListHeight(const SkipList &sl) {
    int count = 0;
    SkipListNode* cur = sl.header->forward[0];
    while (cur) {
        count++;
        cur = cur->forward[0];
    }
    return count;
}

// Funciones de prueba y profiling  

static const int NUM_OPER = 200000; // número de inserciones para pruebas

// Función de inserción masiva y medición de tiempos y "altura"
void testAllStructures() {
    cout << "Inserción masiva (" << NUM_OPER << " operaciones)\n";
    vector<int> keys;
    keys.reserve(NUM_OPER);
    for (int i = 0; i < NUM_OPER; i++) {
        keys.push_back(rand() % (NUM_OPER * 10));
    }

    // BST clásico
    BSTNode* bstRoot = nullptr;
    auto t1 = chrono::high_resolution_clock::now();
    for (int k : keys)
        bstRoot = bstInsert(bstRoot, k);
    auto t2 = chrono::high_resolution_clock::now();
    double timeBST = chrono::duration<double, milli>(t2 - t1).count();
    int heightBST = bstHeight(bstRoot);

    // Treap
    TreapNode* treapRoot = nullptr;
    t1 = chrono::high_resolution_clock::now();
    for (int k : keys)
        treapRoot = treapInsert(treapRoot, k);
    t2 = chrono::high_resolution_clock::now();
    double timeTreap = chrono::duration<double, milli>(t2 - t1).count();
    int heightTreap = treapHeight(treapRoot);

    // SkipList
    SkipList skip;
    t1 = chrono::high_resolution_clock::now();
    for (int k : keys)
        skipListInsert(skip, k);
    t2 = chrono::high_resolution_clock::now();
    double timeSkip = chrono::duration<double, milli>(t2 - t1).count();
    int skipCount = skipListHeight(skip);

    cout << "BST:\n  Tiempo inserción: " << timeBST << " ms\n  Altura: " << heightBST << "\n\n";
    cout << "Treap:\n  Tiempo inserción: " << timeTreap << " ms\n  Altura: " << heightTreap << "\n\n";
    cout << "SkipList:\n  Tiempo inserción: " << timeSkip << " ms\n  'Altura' (nodos nivel 0): " << skipCount << "\n\n";
}

// Función para medir tiempos de búsqueda en las 3 estructuras
void testSearchAllStructures() {
    cout << "Búsqueda aleatoria en BST, Treap y SkipList\n";
    vector<int> keys;
    keys.reserve(NUM_OPER);
    for (int i = 0; i < NUM_OPER; i++) {
        keys.push_back(rand() % (NUM_OPER * 10));
    }
    // Inserción en cada estructura
    BSTNode* bstRoot = nullptr;
    for (int k : keys)
        bstRoot = bstInsert(bstRoot, k);

    TreapNode* treapRoot = nullptr;
    for (int k : keys)
        treapRoot = treapInsert(treapRoot, k);

    SkipList skip;
    for (int k : keys)
        skipListInsert(skip, k);

    // Generar claves de búsqueda
    vector<int> searchKeys;
    searchKeys.reserve(NUM_OPER);
    for (int i = 0; i < NUM_OPER; i++) {
        searchKeys.push_back(rand() % (NUM_OPER * 10));
    }
    
    int foundBST = 0, foundTreap = 0, foundSkip = 0;
    auto t1 = chrono::high_resolution_clock::now();
    for (int k : searchKeys)
        if (bstFind(bstRoot, k)) foundBST++;
    auto t2 = chrono::high_resolution_clock::now();
    double timeBST = chrono::duration<double, milli>(t2 - t1).count();

    t1 = chrono::high_resolution_clock::now();
    for (int k : searchKeys)
        if (treapFind(treapRoot, k)) foundTreap++;
    t2 = chrono::high_resolution_clock::now();
    double timeTreap = chrono::duration<double, milli>(t2 - t1).count();

    t1 = chrono::high_resolution_clock::now();
    for (int k : searchKeys)
        if (skipListFind(skip, k)) foundSkip++;
    t2 = chrono::high_resolution_clock::now();
    double timeSkip = chrono::duration<double, milli>(t2 - t1).count();

    cout << "BST:\n  Tiempo búsqueda: " << timeBST << " ms\n  Claves encontradas: " << foundBST << "\n\n";
    cout << "Treap:\n  Tiempo búsqueda: " << timeTreap << " ms\n  Claves encontradas: " << foundTreap << "\n\n";
    cout << "SkipList:\n  Tiempo búsqueda: " << timeSkip << " ms\n  Claves encontradas: " << foundSkip << "\n\n";
}

// 
// Funcion principal
// 
int main(int argc, char* argv[]) {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Si se indica un argumento, se selecciona el modo:
    // "test" => Ejecuta pruebas unitarias (inserción y búsqueda)
    // "profile" => Ejecuta funciones de profiling (los mismos tests con tiempos)
    if (argc > 1) {
        string mode = argv[1];
        if (mode == "test") {
            testAllStructures();
            testSearchAllStructures();
            return 0;
        } else if (mode == "profile") {
            testAllStructures();
            testSearchAllStructures();
            return 0;
        }
    }

    // Si no se pasan parámetros, se ejecuta una demo interactiva
    cout << " Demostracion: Comparación de BST, Treap y SkipList\n";
    
    // En la demo se realizan ambas pruebas:
    testAllStructures();
    testSearchAllStructures();
    
    cout << "Fin de la demo.\n";
    return 0;
}

