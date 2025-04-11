#include <bits/stdc++.h>
using namespace std;

/*
    Ejemplo de treaps aplicados en un escenario distribuido simplificado
    ----------------------------------------------------------------------------
    Se tendrá un sistema con varios "nodos" (shards) distribuidos, cada uno con:
      - Un treap local que almacena "Records" (clave, valor, versión).

    Se define un sencillo mecanismo de:
      1. Hashing para distribuir las claves en distintos nodos.
      2. Inserción y eliminación locales.
      3. Búsquedas globales (consultando el nodo que corresponde a la clave).
      4. Merge (tipo CRDT simple):
         - Cada nodo tiene su treap con (key, value, version).
         - Al fusionar dos treaps, gana la tupla con mayor version (timestamp).
    

    Estructuras principales:
      - Record: Contiene clave (int), valor (string) y version/timestamp (int).
      - Node: Estructura de nodo para el treap (almacena un 'Record').
      - Treap: Implementa las operaciones clásicas: insert, erase, find, etc.
      - DistributedTreapSystem: Conjunto de nodos (shards), cada uno con un Treap.
        - Insertar (se distribuye la clave por hash).
        - Buscar (se pregunta al shard correspondiente).
        - Merge shards (ej. para replicación o CRDT).
        - getAllRecords() que retorna todos los datos, útil para un "global range query".
    
    Se incluyen además funciones de pruebas unitarias y profiling para evaluar el
    correcto funcionamiento y el rendimiento del sistema.
*/


// Estructura "Record"

struct Record {
    int key;
    string value;
    int version;  // timestamp simple para resolver conflictos
    
    Record() : key(0), value(""), version(0) {}
    Record(int k, const string &v, int ver)
        : key(k), value(v), version(ver) {}
};

// Comparación de registros por clave (para el Treap)
bool operator<(const Record &a, const Record &b) {
    return a.key < b.key;
}
bool operator>(const Record &a, const Record &b) {
    return a.key > b.key;
}
bool operator==(const Record &a, const Record &b) {
    return a.key == b.key;
}


// Estructura de nodo para el treap    

struct Node {
    Record rec;
    int priority;    // prioridad para la propiedad de heap
    Node *left;
    Node *right;
    int subtreeSize; // para order statistics (si se requiere)

    Node(const Record &r)
      : rec(r), priority(rand()), left(nullptr), right(nullptr), subtreeSize(1) {}
};


// Funciones auxiliares treap
 
int getSize(Node* root) {
    return root ? root->subtreeSize : 0;
}

void updateSize(Node* root) {
    if (!root) return;
    root->subtreeSize = 1 + getSize(root->left) + getSize(root->right);
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


// Inserción, busqueda y eliminación 
// (incorporando "version" para conflictos)

Node* treapInsert(Node* root, const Record &rec) {
    if (!root) {
        return new Node(rec);
    }
    
    // Ubicar posición según key (BST)
    if (rec.key < root->rec.key) {
        root->left = treapInsert(root->left, rec);
        if (root->left->priority > root->priority) {
            root = rotateRight(root);
        }
    } else if (rec.key > root->rec.key) {
        root->right = treapInsert(root->right, rec);
        if (root->right->priority > root->priority) {
            root = rotateLeft(root);
        }
    } else {
        // Clave ya existe: resolver conflicto por versión.
        if (rec.version > root->rec.version) {
            root->rec.value = rec.value;
            root->rec.version = rec.version;
        }
    }
    updateSize(root);
    return root;
}

Node* treapErase(Node* root, int key) {
    if (!root) return nullptr;

    if (key < root->rec.key) {
        root->left = treapErase(root->left, key);
    } else if (key > root->rec.key) {
        root->right = treapErase(root->right, key);
    } else {
        // Nodo a eliminar encontrado.
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

Node* treapFind(Node* root, int key) {
    if (!root) return nullptr;
    if (root->rec.key == key) {
        return root;
    } else if (key < root->rec.key) {
        return treapFind(root->left, key);
    } else {
        return treapFind(root->right, key);
    }
}

// Recorrido in-order para recolectar registros
void inorderCollect(Node* root, vector<Record> &records) {
    if (!root) return;
    inorderCollect(root->left, records);
    records.push_back(root->rec);
    inorderCollect(root->right, records);
}

// Clase treap
 
class Treap {
private:
    Node* root;
public:
    Treap() : root(nullptr) {
        srand((unsigned) time(nullptr)); 
    }

    // Inserta un record (key, value, version)
    void insert(const Record &r) {
        root = treapInsert(root, r);
    }

    // Elimina por clave
    void erase(int key) {
        root = treapErase(root, key);
    }

    // Busca: retorna puntero al nodo o nullptr
    Node* find(int key) const {
        return treapFind(root, key);
    }

    // Obtiene todos los registros (in-order)
    vector<Record> getAll() const {
        vector<Record> result;
        inorderCollect(root, result);
        return result;
    }

    // Imprime en orden (para depuración)
    void printInOrder() const {
        vector<Record> all = getAll();
        for (auto &r : all) {
            cout << "(" << r.key << ", " << r.value << ", ver=" << r.version << ") ";
        }
        cout << "\n";
    }

    // Merge CRDT-like: incorpora registros de otro treap usando la resolución de versión.
    void mergeFrom(const Treap &other) {
        vector<Record> otherRecords = other.getAll();
        for (auto &rec : otherRecords) {
            this->insert(rec);
        }
    }
};


// Sistema distribuido de treaps
 
class DistributedTreapSystem {
private:
    vector<Treap> shards;  // cada shard posee su treap
    int numShards;
    // Hash sencillo para asignar la clave a un shard
    int getShardIndex(int key) const {
        return (key % numShards + numShards) % numShards; 
    }
public:
    DistributedTreapSystem(int n) : numShards(n) {
        shards.resize(n);
    }

    // Inserta un record en el shard correspondiente
    void insert(const Record &r) {
        int shardIdx = getShardIndex(r.key);
        shards[shardIdx].insert(r);
    }

    // Elimina un record por clave
    void erase(int key) {
        int shardIdx = getShardIndex(key);
        shards[shardIdx].erase(key);
    }

    // Busca un record en el shard de la clave
    Node* find(int key) const {
        int shardIdx = getShardIndex(key);
        return shards[shardIdx].find(key);
    }

    // Retorna todos los registros de todos los shards (no necesariamente ordenados globalmente)
    vector<Record> getAllGlobal() const {
        vector<Record> result;
        for (int i = 0; i < numShards; i++) {
            vector<Record> partial = shards[i].getAll();
            result.insert(result.end(), partial.begin(), partial.end());
        }
        return result;
    }

    // Merge entre dos shards: fusiona el contenido del shardB dentro del shardA.
    void mergeShards(int shardA, int shardB) {
        shards[shardA].mergeFrom(shards[shardB]);
    }

    // Imprime el estado del sistema distribuido (por shard)
    void printSystemState() const {
        cout << "\nDistributedTreapSystem State\n";
        for (int i = 0; i < numShards; i++) {
            cout << "Shard " << i << ": ";
            shards[i].printInOrder();
        }
        cout << "=====================================\n";
    }
};

// Pruebas unitarias
void runUnitTests() {
    cout << "Ejecutando pruebas unitarias\n";

    // Crear sistema con 4 shards
    DistributedTreapSystem system(4);

    // Inserciones básicas
    system.insert({10, "v10_1", 1});
    system.insert({14, "v14_1", 1});
    system.insert({2,  "v2_1", 1});
    system.insert({18, "v18_1", 1});
    // Actualización: versión mayor en la misma clave
    system.insert({2,  "v2_2", 2});
    system.insert({30, "v30_1", 1});
    system.insert({6,  "v6_1", 1});
    system.insert({22, "v22_1", 1});

    // Verificar el comportamiento de búsqueda
    {
        Node* n = system.find(2);
        assert(n != nullptr);
        assert(n->rec.value == "v2_2"); // se espera la versión actualizada
        n = system.find(14);
        assert(n != nullptr);
    }

    // Verificar eliminación
    system.erase(14);
    {
        Node* n = system.find(14);
        assert(n == nullptr);
    }

    // Verificar merge: simular fusionar shard 0 y 1
    // Antes del merge, recolectar registros de shard 1
    vector<Record> shard1Records = system.getAllGlobal();
    // Realizar merge entre shard 0 y shard 1
    system.mergeShards(0, 1);

    // Chequear que no se pierdan los registros ya presentes en shard 0
    vector<Record> globalRecords = system.getAllGlobal();
    // Ordenar los registros por clave para facilitar la comprobación
    sort(globalRecords.begin(), globalRecords.end(), [](const Record &a, const Record &b) {
        return a.key < b.key;
    });
    // Se espera que la clave 10, 2, 18, 30, 6 y 22 estén presentes, y que la clave 14 ya fue eliminada.
    vector<int> expectedKeys = {2,6,10,18,22,30};
    vector<int> obtainedKeys;
    for (auto &r : globalRecords) {
        obtainedKeys.push_back(r.key);
    }
    sort(obtainedKeys.begin(), obtainedKeys.end());
    assert(obtainedKeys == expectedKeys);

    cout << "Todas las pruebas unitarias pasaron correctamente\n\n";
}

//Profiling
 
#include <chrono>
void runProfiling() {
    cout << "=== Ejecutando Profiling del Sistema Distribuido ===\n";
    const int numShards = 8;
    const int numOps = 100000; // número total de operaciones
    DistributedTreapSystem system(numShards);
    srand((unsigned) time(nullptr));

    auto start = chrono::steady_clock::now();
    for (int i = 0; i < numOps; i++) {
        // Generar clave aleatoria y versión
        int key = rand() % 10000;    // clave entre 0 y 9999
        int ver = rand() % 100 + 1;    // versión entre 1 y 100
        string value = "val" + to_string(key);
        // Realizar inserción
        system.insert({key, value, ver});
        // Cada cierto número de operaciones se realiza una eliminación aleatoria
        if (i % 1000 == 0) {
            system.erase(rand() % 10000);
        }
    }
    auto end = chrono::steady_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
    cout << "Tiempo total para " << numOps << " operaciones: " << duration.count() << " ms\n";

    // Muestra la cantidad total de registros (globalmente)
    vector<Record> allRecords = system.getAllGlobal();
    cout << "Número total de registros acumulados: " << allRecords.size() << "\n\n";
}
 
// Funcion principal                    
// 
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

    // Modo demostración: ejecución del ejemplo original.
    cout << "  Demostración: Treaps en un Sistema Distribuido\n";

    DistributedTreapSystem distSystem(4);

    // Insertar registros de ejemplo (clave, value, versión)
    distSystem.insert({10, "valor10v1", 1});
    distSystem.insert({14, "valor14v1", 1});
    distSystem.insert({2,  "valor2v1", 1});
    distSystem.insert({18, "valor18v1", 1});
    distSystem.insert({2,  "valor2v2", 2}); // actualiza al tener versión mayor
    distSystem.insert({30, "valor30v1", 1});
    distSystem.insert({6,  "valor6v1", 1});
    distSystem.insert({22, "valor22v1", 1});

    cout << "Estado tras algunas inserciones:\n";
    distSystem.printSystemState();

    // Búsquedas de ejemplo
    vector<int> keysToFind = {2, 14, 5, 22};
    cout << "\nBuscando registros en el sistema:\n";
    for (auto key : keysToFind) {
        Node* found = distSystem.find(key);
        if (found) {
            cout << "  KEY=" << key << " => valor=" << found->rec.value
                 << ", version=" << found->rec.version << "\n";
        } else {
            cout << "  KEY=" << key << " => No encontrado\n";
        }
    }

    // Simulación de merge entre shards
    cout << "\nSimulando merge entre shard 0 y shard 1...\n";
    distSystem.mergeShards(0, 1);

    // Eliminación de un registro
    cout << "\nEliminando la clave 14...\n";
    distSystem.erase(14);

    cout << "\nEstado final:\n";
    distSystem.printSystemState();

    // Query global: obtener todos los registros y mostrarlos ordenados por clave
    cout << "Registros globales (desordenados):\n";
    vector<Record> globalData = distSystem.getAllGlobal();
    for (auto &r : globalData) {
        cout << "(k=" << r.key << ", val=" << r.value << ", ver=" << r.version << ") ";
    }
    cout << "\n";
    sort(globalData.begin(), globalData.end(), [](const Record &a, const Record &b) {
       return a.key < b.key;
    });
    cout << "Registros globales ordenados por key:\n";
    for (auto &r : globalData) {
        cout << "(k=" << r.key << ", val=" << r.value << ", ver=" << r.version << ") ";
    }
    cout << "\n\nFin de la demostración.\n";
    return 0;
}

