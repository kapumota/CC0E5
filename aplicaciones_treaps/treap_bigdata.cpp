#include <bits/stdc++.h>
using namespace std;
using ll = long long;

/*
   
     Ejemplo de Treap aplicado a:
       - Procesamiento de Grandes Volúmenes de Datos (Big Data)
       - Estructuras Indexadas para Almacenamiento en Memoria

    Se define una estructura "Record" con algunos campos.
    Se implementa un "Treap" ordenado por "record.id", con:
       - Insert
       - Erase
       - Find
       - Range Query (por id)

    El main simula:
      1) Generar un gran volumen de datos (N registros).
      2) Insertarlos en el treap.
      3) Hacer algunas consultas:
          - Búsquedas concretas (find).
          - Consultas por rango (range query).
      4) Eliminar algunos registros.
      5) Mostrar resultados y tiempos de ejecución.

    Se incluyen además pruebas unitarias y profiling para evaluar funcionalidad y rendimiento.
   
*/

//  Definición de la estructura Record

struct Record {
    int id;         // Clave principal para indexar
    string name;    // Nombre (simula un campo de texto)
    int value;      // Algún valor numérico (ejemplo: puntuación, precio, etc.)

    Record() : id(0), name(""), value(0) {}
    Record(int _id, const string &_name, int _val)
        : id(_id), name(_name), value(_val) {}
};

//  Nodo del Treap

struct TreapNode {
    Record rec;
    int priority;         // Prioridad aleatoria
    TreapNode *left;
    TreapNode *right;
    int subtreeSize;      // Tamaño del subárbol, útil para estadísticas u order statistics

    // Constructor
    TreapNode(const Record &r)
        : rec(r), priority(rand()), left(nullptr), right(nullptr), subtreeSize(1) {}
};


// Funciones auxiliares del Treap

int getSize(TreapNode* node) {
    return (node == nullptr) ? 0 : node->subtreeSize;
}

void updateSize(TreapNode* node) {
    if (node) {
        node->subtreeSize = 1 + getSize(node->left) + getSize(node->right);
    }
}

TreapNode* rotateRight(TreapNode* Q) {
    // Rotación derecha
    TreapNode* P = Q->left;
    Q->left = P->right;
    P->right = Q;
    updateSize(Q);
    updateSize(P);
    return P;
}

TreapNode* rotateLeft(TreapNode* P) {
    // Rotación izquierda
    TreapNode* Q = P->right;
    P->right = Q->left;
    Q->left = P;
    updateSize(P);
    updateSize(Q);
    return Q;
}


// Insertar un Record en el Treap

TreapNode* treapInsert(TreapNode* root, const Record &r) {
    if (!root) {
        return new TreapNode(r);
    }
    if (r.id < root->rec.id) {
        // Insertamos en el subárbol izquierdo
        root->left = treapInsert(root->left, r);
        if (root->left->priority > root->priority) {
            root = rotateRight(root);
        }
    } else if (r.id > root->rec.id) {
        // Insertamos en el subárbol derecho
        root->right = treapInsert(root->right, r);
        if (root->right->priority > root->priority) {
            root = rotateLeft(root);
        }
    } else {
        // r.id == root->rec.id => actualizamos la info
        root->rec.name = r.name;
        root->rec.value = r.value;
    }
    updateSize(root);
    return root;
}

//  Encontrar un Record por su ID

TreapNode* treapFind(TreapNode* root, int id) {
    if (!root) return nullptr;
    if (root->rec.id == id) {
        return root;
    } else if (id < root->rec.id) {
        return treapFind(root->left, id);
    } else {
        return treapFind(root->right, id);
    }
}

//  Eliminar un Record por ID

TreapNode* treapErase(TreapNode* root, int id) {
    if (!root) return nullptr;
    if (id < root->rec.id) {
        root->left = treapErase(root->left, id);
    } else if (id > root->rec.id) {
        root->right = treapErase(root->right, id);
    } else {
        // Hallamos el nodo a borrar
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
                root->right = treapErase(root->right, id);
            } else {
                root = rotateLeft(root);
                root->left = treapErase(root->left, id);
            }
        }
    }
    updateSize(root);
    return root;
}

//  Range Query [L, R]: recoger todos los registros con L <= id <= R
void treapRangeQuery(TreapNode* root, int L, int R, vector<Record> &result) {
    if (!root) return;
    if (root->rec.id >= L) {
        treapRangeQuery(root->left, L, R, result);
    }
    if (root->rec.id >= L && root->rec.id <= R) {
        result.push_back(root->rec);
    }
    if (root->rec.id <= R) {
        treapRangeQuery(root->right, L, R, result);
    }
}

//  Recorrido in-order (para depuración con volúmenes pequeños)

void inorderPrint(TreapNode* root) {
    if (!root) return;
    inorderPrint(root->left);
    cout << "(" << root->rec.id << ", " << root->rec.name
         << ", value=" << root->rec.value << ") ";
    inorderPrint(root->right);
}


//  Clase Treap: envuelve las operaciones

class Treap {
private:
    TreapNode* root;
public:
    Treap() : root(nullptr) {
        srand((unsigned)time(nullptr));
    }
    void insert(const Record &r) {
        root = treapInsert(root, r);
    }
    void erase(int id) {
        root = treapErase(root, id);
    }
    TreapNode* find(int id) {
        return treapFind(root, id);
    }
    vector<Record> rangeQuery(int L, int R) {
        vector<Record> result;
        treapRangeQuery(root, L, R, result);
        return result;
    }
    void printInOrder() {
        inorderPrint(root);
        cout << "\n";
    }
};


//  Función para generar un nombre aleatorio

string randomName(mt19937 &rng, int length=5) {
    static const string alpha = "abcdefghijklmnopqrstuvwxyz";
    uniform_int_distribution<int> dist(0, (int)alpha.size()-1);
    string s;
    for (int i = 0; i < length; i++) {
        s.push_back(alpha[dist(rng)]);
    }
    return s;
}


// Pruebas unitarias

#include <cassert>
void runUnitTests() {
    cout << "Ejecutando pruebas unitarias\n";
    Treap testTreap;
    
    // Insertar registros conocidos
    vector<Record> testRecords = {
        Record(100, "alice", 500),
        Record(50, "bob", 300),
        Record(150, "carol", 700),
        Record(75, "dave", 400),
        Record(125, "eve", 600)
    };
    
    for (auto &r : testRecords) {
        testTreap.insert(r);
    }
    
    // Verificar que se puedan encontrar
    for (auto &r : testRecords) {
        TreapNode* node = testTreap.find(r.id);
        assert(node != nullptr);
        assert(node->rec.name == r.name);
        assert(node->rec.value == r.value);
    }
    
    // Probar range query para IDs entre 60 y 130
    vector<Record> rangeRes = testTreap.rangeQuery(60, 130);
    // Se esperarían registros con id 75, 100, 125
    vector<int> expected = {75, 100, 125};
    vector<int> obtained;
    for (auto &r : rangeRes)
        obtained.push_back(r.id);
    sort(obtained.begin(), obtained.end());
    assert(obtained == expected);
    
    // Probar eliminación: borrar el registro con id 75
    testTreap.erase(75);
    TreapNode* nodeAfterErase = testTreap.find(75);
    assert(nodeAfterErase == nullptr);
    
    cout << "Todas las pruebas unitarias pasaron\n\n";
}

//
//Profiling
//
#include <chrono>
void runProfiling() {
    cout << "Ejecutando profiling del Treap\n";
    const int NUM_RECORDS = 100000;
    Treap bigTreap;
    mt19937 rng(time(nullptr));
    uniform_int_distribution<int> distID(1, NUM_RECORDS * 10);
    uniform_int_distribution<int> distValue(0, 10000);
    
    auto startInsert = chrono::high_resolution_clock::now();
    for (int i = 0; i < NUM_RECORDS; i++) {
        int randomId = distID(rng);
        int val = distValue(rng);
        string nm = randomName(rng, 5);
        Record r(randomId, nm, val);
        bigTreap.insert(r);
    }
    auto endInsert = chrono::high_resolution_clock::now();
    double insertTime = chrono::duration<double, milli>(endInsert - startInsert).count();
    
    cout << "Inserción de " << NUM_RECORDS << " registros completada en " 
         << insertTime << " ms.\n";
    
    // Realizar un número de búsquedas aleatorias
    const int NUM_QUERIES = 10000;
    auto startFind = chrono::high_resolution_clock::now();
    int foundCount = 0;
    for (int i = 0; i < NUM_QUERIES; i++) {
        int q = distID(rng);
        if (bigTreap.find(q) != nullptr)
            foundCount++;
    }
    auto endFind = chrono::high_resolution_clock::now();
    double findTime = chrono::duration<double, milli>(endFind - startFind).count();
    cout << "Realizadas " << NUM_QUERIES << " búsquedas, encontrados: " 
         << foundCount << " registros en " << findTime << " ms.\n";
    
    // Realizar consultas por rango
    const int NUM_RANGE_QUERIES = 1000;
    auto startRange = chrono::high_resolution_clock::now();
    int totalResults = 0;
    for (int i = 0; i < NUM_RANGE_QUERIES; i++) {
        int L = distID(rng);
        int R = L + 50; // rango pequeño
        vector<Record> res = bigTreap.rangeQuery(L, R);
        totalResults += res.size();
    }
    auto endRange = chrono::high_resolution_clock::now();
    double rangeTime = chrono::duration<double, milli>(endRange - startRange).count();
    cout << "Realizadas " << NUM_RANGE_QUERIES << " consultas por rango en " 
         << rangeTime << " ms. (Total resultados: " << totalResults << ")\n";
    
    cout << "Profiling completado\n\n";
}

//  MAIN: Selección de modo (Test/Profiling /Demostracion)

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
    
    // Modo demo: ejecución interactiva de la demostración original.
    cout << "\n";
    cout << "Demostracion: Treap para Big Data/In-Memory Index\n";
    cout << " Insertando registros aleatorios...\n";
    cout << "\n\n";
    
    const int N = 10000;
    Treap indexTreap;
    mt19937 rng(time(nullptr));
    uniform_int_distribution<int> distID(1, N * 10);
    uniform_int_distribution<int> distValue(0, 10000);
    
    auto startInsert = chrono::high_resolution_clock::now();
    for (int i = 0; i < N; i++) {
        int randomId = distID(rng);
        int val = distValue(rng);
        string nm = randomName(rng, 5);
        Record r(randomId, nm, val);
        indexTreap.insert(r);
    }
    auto endInsert = chrono::high_resolution_clock::now();
    double insertTime = chrono::duration<double, milli>(endInsert - startInsert).count();
    cout << "Inserción finalizada en " << insertTime << " ms.\n\n";
    
    // Búsquedas concretas
    cout << "Ejecutando 5 búsquedas concretas:\n";
    for (int i = 0; i < 5; i++) {
        int testID = distID(rng);
        TreapNode* node = indexTreap.find(testID);
        if (node) {
            cout << "  ID=" << testID << " => Encontrado: ("
                 << node->rec.name << ", value=" << node->rec.value << ")\n";
        } else {
            cout << "  ID=" << testID << " => No encontrado\n";
        }
    }
    cout << "\n";
    
    // Consultas por rango
    cout << "Ejecutando consultas por rango:\n";
    vector<pair<int,int>> ranges = { {1, 50}, {100, 200}, {500,600}, {2000,2010} };
    for (auto &rg : ranges) {
        int L = rg.first, R = rg.second;
        vector<Record> res = indexTreap.rangeQuery(L, R);
        cout << "  Rango [" << L << ", " << R << "]: " << res.size() << " resultados.\n";
    }
    cout << "\n";
    
    // Eliminación de algunos registros
    cout << "Eliminando 5 IDs aleatorios:\n";
    for (int i = 0; i < 5; i++) {
        int randomId = distID(rng);
        cout << "  Borrando ID=" << randomId << "\n";
        indexTreap.erase(randomId);
    }
    
    cout << "\nDemo finalizada.\n";
    cout << "FIN.\n";
    return 0;
}

