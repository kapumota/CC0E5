#include <bits/stdc++.h>
using namespace std;

/*
    
    Ejemplo de uso de treaps para:
      1. Planificación / Priorización de paquetes (cola de prioridad).
      2. Gestión de tablas de enrutamiento.

    Este ejemplo incluye:
      - TreapPriorityQueue:
          * Maneja "paquetes" con un campo 'priority' (cuanto mayor es, antes se procesa).
          * La clave del BST es -priority (para que el mayor priority quede "más arriba").
          * Operaciones: push, top, pop, empty, size.
      - TreapRoutingTable:
          * Cada entrada es (destino, nextHop, metric).
          * La clave del BST es 'destino'.
          * Operaciones: insert/actualiza, erase, find, printInOrder.
    
    Además se incorporan:
      - Pruebas unitarias para validar el correcto funcionamiento.
      - Profiling para medir el rendimiento en un gran número de operaciones.
    
*/

// Estructura de paquete para la cola de prioridad

struct Packet {
    int id;         // identificador del paquete
    int priority;   // prioridad del paquete (mayor => más urgente)
    string content; // datos o contenido

    Packet() : id(0), priority(0), content("") {}
    Packet(int i, int p, const string &c)
        : id(i), priority(p), content(c) {}
};

// Treap para Prioridad de Paquetes (TreapPriorityQueue) 

/*
    Para implementar la cola de prioridad con un treap:
    - Se utiliza como "BST key" el valor -priority (para que el mayor priority tenga la clave menor).
    - Se usa un valor aleatorio ("randVal") para mantener la propiedad de heap.
*/

struct PQNode {
    Packet packet;
    int key;       // key = -priority
    int randVal;   // para la propiedad de heap aleatoria
    PQNode* left;
    PQNode* right;
    int subtreeSize; // opcional para statistics

    PQNode(const Packet &pkt)
        : packet(pkt),
          key(-pkt.priority),
          randVal(rand()),
          left(nullptr),
          right(nullptr),
          subtreeSize(1) {}
};

static int getSize(PQNode* root) {
    return root ? root->subtreeSize : 0;
}
static void updateSize(PQNode* root) {
    if (root)
        root->subtreeSize = 1 + getSize(root->left) + getSize(root->right);
}
static PQNode* rotateRight(PQNode* Q) {
    PQNode* P = Q->left;
    Q->left = P->right;
    P->right = Q;
    updateSize(Q);
    updateSize(P);
    return P;
}
static PQNode* rotateLeft(PQNode* P) {
    PQNode* Q = P->right;
    P->right = Q->left;
    Q->left = P;
    updateSize(P);
    updateSize(Q);
    return Q;
}

static PQNode* pqInsert(PQNode* root, const Packet &pkt) {
    if (!root) {
        return new PQNode(pkt);
    }
    int newKey = -pkt.priority;
    if (newKey < root->key) {
        root->left = pqInsert(root->left, pkt);
        if (root->left->randVal > root->randVal)
            root = rotateRight(root);
    } else {
        root->right = pqInsert(root->right, pkt);
        if (root->right->randVal > root->randVal)
            root = rotateLeft(root);
    }
    updateSize(root);
    return root;
}

static Packet pqTop(PQNode* root) {
    return root->packet;
}

static PQNode* pqPopRoot(PQNode* root) {
    if (!root) return nullptr;
    if (!root->left && !root->right) {
        delete root;
        return nullptr;
    } else if (!root->left) {
        root = rotateLeft(root);
        root->left = pqPopRoot(root->left);
    } else if (!root->right) {
        root = rotateRight(root);
        root->right = pqPopRoot(root->right);
    } else {
        if (root->left->randVal > root->right->randVal) {
            root = rotateRight(root);
            root->right = pqPopRoot(root->right);
        } else {
            root = rotateLeft(root);
            root->left = pqPopRoot(root->left);
        }
    }
    updateSize(root);
    return root;
}

class TreapPriorityQueue {
private:
    PQNode* root;
    int countPackets;
public:
    TreapPriorityQueue() : root(nullptr), countPackets(0) {
        srand((unsigned) time(nullptr));
    }
    void push(const Packet &pkt) {
        root = pqInsert(root, pkt);
        countPackets++;
    }
    Packet top() {
        if (!root)
            return Packet(-1, -1, "EMPTY");
        return pqTop(root);
    }
    void pop() {
        if (!root) return;
        root = pqPopRoot(root);
        countPackets--;
    }
    bool empty() const {
        return (countPackets == 0);
    }
    int size() const {
        return countPackets;
    }
};


// Treap para gestión de tabla de enrutamiento
// 

struct RouteEntry {
    string destination;
    string nextHop;
    int metric; // costo o distancia

    RouteEntry() : destination(""), nextHop(""), metric(0) {}
    RouteEntry(const string &d, const string &n, int m)
        : destination(d), nextHop(n), metric(m) {}
};

static bool operator<(const RouteEntry &a, const RouteEntry &b) {
    return a.destination < b.destination;
}
static bool operator>(const RouteEntry &a, const RouteEntry &b) {
    return a.destination > b.destination;
}
static bool operator==(const RouteEntry &a, const RouteEntry &b) {
    return a.destination == b.destination;
}

struct RouteNode {
    RouteEntry entry;
    int randVal;     // para heap property
    RouteNode *left;
    RouteNode *right;
    int subtreeSize; // opcional

    RouteNode(const RouteEntry &e)
      : entry(e), randVal(rand()), left(nullptr), right(nullptr), subtreeSize(1) {}
};

static int getSize(RouteNode* root) {
    return root ? root->subtreeSize : 0;
}
static void updateSize(RouteNode* root) {
    if (root)
        root->subtreeSize = 1 + getSize(root->left) + getSize(root->right);
}
static RouteNode* rotateRight(RouteNode* Q) {
    RouteNode* P = Q->left;
    Q->left = P->right;
    P->right = Q;
    updateSize(Q);
    updateSize(P);
    return P;
}
static RouteNode* rotateLeft(RouteNode* P) {
    RouteNode* Q = P->right;
    P->right = Q->left;
    Q->left = P;
    updateSize(P);
    updateSize(Q);
    return Q;
}

static RouteNode* rtInsert(RouteNode* root, const RouteEntry &re) {
    if (!root)
        return new RouteNode(re);
    if (re < root->entry) {
        root->left = rtInsert(root->left, re);
        if (root->left->randVal > root->randVal)
            root = rotateRight(root);
    } else if (re > root->entry) {
        root->right = rtInsert(root->right, re);
        if (root->right->randVal > root->randVal)
            root = rotateLeft(root);
    } else {
        // Actualización si el destino ya existe
        root->entry.nextHop = re.nextHop;
        root->entry.metric = re.metric;
    }
    updateSize(root);
    return root;
}

static RouteNode* rtErase(RouteNode* root, const string &dest) {
    if (!root) return nullptr;
    if (dest < root->entry.destination) {
        root->left = rtErase(root->left, dest);
    } else if (dest > root->entry.destination) {
        root->right = rtErase(root->right, dest);
    } else {
        if (!root->left) {
            RouteNode* temp = root->right;
            delete root;
            return temp;
        } else if (!root->right) {
            RouteNode* temp = root->left;
            delete root;
            return temp;
        } else {
            if (root->left->randVal > root->right->randVal) {
                root = rotateRight(root);
                root->right = rtErase(root->right, dest);
            } else {
                root = rotateLeft(root);
                root->left = rtErase(root->left, dest);
            }
        }
    }
    updateSize(root);
    return root;
}

static RouteNode* rtFind(RouteNode* root, const string &dest) {
    if (!root) return nullptr;
    if (dest == root->entry.destination)
        return root;
    else if (dest < root->entry.destination)
        return rtFind(root->left, dest);
    else
        return rtFind(root->right, dest);
}

static void inorderPrint(RouteNode* root) {
    if (!root) return;
    inorderPrint(root->left);
    cout << "[" << root->entry.destination << " -> " << root->entry.nextHop 
         << ", metric=" << root->entry.metric << "] ";
    inorderPrint(root->right);
}

class TreapRoutingTable {
private:
    RouteNode* root;
public:
    TreapRoutingTable() : root(nullptr) {
        srand((unsigned) time(nullptr));
    }
    void insert(const RouteEntry &re) {
        root = rtInsert(root, re);
    }
    void erase(const string &dest) {
        root = rtErase(root, dest);
    }
    RouteNode* find(const string &dest) {
        return rtFind(root, dest);
    }
    void printInOrder() {
        inorderPrint(root);
        cout << "\n";
    }
};

//  Pruebas unitarias  
#include <cassert>
#include <chrono>

void runUnitTests() {
    cout << "Ejecutando pruebas unitarias\n";
    
    // Pruebas para TreapPriorityQueue
    {
        TreapPriorityQueue pq;
        pq.push(Packet(1, 10, "Test A"));
        pq.push(Packet(2, 30, "Test B"));
        pq.push(Packet(3, 20, "Test C"));
        Packet topPkt = pq.top();
        // Se espera que el paquete con mayor prioridad (30) sea el primero.
        assert(topPkt.id == 2 && topPkt.priority == 30);
        pq.pop();
        topPkt = pq.top();
        assert(topPkt.id == 3 && topPkt.priority == 20);
        while(!pq.empty())
            pq.pop();
        assert(pq.empty());
        cout << "Pruebas TreapPriorityQueue pasaron.\n";
    }
    
    // Pruebas para TreapRoutingTable
    {
        TreapRoutingTable rt;
        rt.insert(RouteEntry("192.168.1.1", "10.0.0.1", 1));
        rt.insert(RouteEntry("192.168.1.2", "10.0.0.2", 2));
        rt.insert(RouteEntry("192.168.1.3", "10.0.0.3", 3));
        // Actualizar la ruta para 192.168.1.1
        rt.insert(RouteEntry("192.168.1.1", "10.0.1.1", 1));
        RouteNode* found = rt.find("192.168.1.1");
        assert(found != nullptr && found->entry.nextHop == "10.0.1.1");
        rt.erase("192.168.1.2");
        RouteNode* found2 = rt.find("192.168.1.2");
        assert(found2 == nullptr);
        cout << "Pruebas TreapRoutingTable  pasaron.\n";
    }
    cout << "Todas las pruebas unitarias pasaron\n\n";
}

void runProfiling() {
    cout << "Ejecutando Profiling\n";
    // Profiling para TreapPriorityQueue
    const int NUM_PACKETS = 100000;
    TreapPriorityQueue pq;
    auto start = chrono::steady_clock::now();
    for (int i = 0; i < NUM_PACKETS; i++) {
        int prio = rand() % 1000 + 1;
        pq.push(Packet(i, prio, "Profiling Packet"));
    }
    auto mid = chrono::steady_clock::now();
    while (!pq.empty())
        pq.pop();
    auto end = chrono::steady_clock::now();
    auto durationInsert = chrono::duration_cast<chrono::milliseconds>(mid - start).count();
    auto durationPop = chrono::duration_cast<chrono::milliseconds>(end - mid).count();
    cout << "TreapPriorityQueue:\n"
         << "  Inserción de " << NUM_PACKETS << " paquetes: " << durationInsert << " ms\n"
         << "  Eliminación total: " << durationPop << " ms\n";
    
    // Profiling para TreapRoutingTable
    const int NUM_ROUTES = 100000;
    TreapRoutingTable rt;
    start = chrono::steady_clock::now();
    for (int i = 0; i < NUM_ROUTES; i++) {
        int a = rand() % 256, b = rand() % 256;
        string dest = "192.168." + to_string(a) + "." + to_string(b);
        string nextHop = "10.0.0." + to_string(rand() % 256);
        int metric = rand() % 10 + 1;
        rt.insert(RouteEntry(dest, nextHop, metric));
    }
    mid = chrono::steady_clock::now();
    for (int i = 0; i < NUM_ROUTES / 10; i++) {
        int a = rand() % 256, b = rand() % 256;
        string dest = "192.168." + to_string(a) + "." + to_string(b);
        rt.erase(dest);
    }
    end = chrono::steady_clock::now();
    durationInsert = chrono::duration_cast<chrono::milliseconds>(mid - start).count();
    auto durationErase = chrono::duration_cast<chrono::milliseconds>(end - mid).count();
    cout << "TreapRoutingTable:\n"
         << "  Inserción de " << NUM_ROUTES << " rutas: " << durationInsert << " ms\n"
         << "  Eliminación de " << NUM_ROUTES/10 << " rutas: " << durationErase << " ms\n\n";
}


// Funcion principal 

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
    
    // Modo demo (ejecución interactiva de la demostración original)
    cout << " Demostración de treap para redes y enrutamiento\n";
    
    // 1. Uso de TreapPriorityQueue
    TreapPriorityQueue packetQueue;
    packetQueue.push(Packet(1, 10, "Paquete A"));
    packetQueue.push(Packet(2, 30, "Paquete B"));
    packetQueue.push(Packet(3, 20, "Paquete C"));
    packetQueue.push(Packet(4, 50, "Paquete D"));
    packetQueue.push(Packet(5, 5,  "Paquete E"));
    
    cout << "Cola de prioridad de paquetes:\n";
    cout << "  Tamaño: " << packetQueue.size() << "\n";
    while (!packetQueue.empty()) {
        Packet topPkt = packetQueue.top();
        cout << "  Procesando Packet ID=" << topPkt.id
             << ", Priority=" << topPkt.priority
             << ", Content=\"" << topPkt.content << "\"\n";
        packetQueue.pop();
    }
    cout << "\n";
    
    // 2. Uso de TreapRoutingTable
    TreapRoutingTable routingTable;
    routingTable.insert(RouteEntry("192.168.0.1", "10.0.0.1", 1));
    routingTable.insert(RouteEntry("192.168.0.2", "10.0.0.2", 2));
    routingTable.insert(RouteEntry("10.10.10.1",  "10.0.0.3", 5));
    routingTable.insert(RouteEntry("8.8.8.8",     "10.0.0.9", 1));
    
    cout << "Tabla de enrutamiento (in-order):\n";
    routingTable.printInOrder();
    
    cout << "\nActualizando ruta para 192.168.0.1...\n";
    routingTable.insert(RouteEntry("192.168.0.1", "10.0.1.254", 1));
    RouteNode* found = routingTable.find("192.168.0.1");
    if (found)
        cout << "  Encontrada -> nextHop=" << found->entry.nextHop
             << ", metric=" << found->entry.metric << "\n";
    
    cout << "\nEliminando la ruta 8.8.8.8...\n";
    routingTable.erase("8.8.8.8");
    
    cout << "\nTabla de enrutamiento final (in-order):\n";
    routingTable.printInOrder();
    
    cout << "\nFin de la demostración.\n";
    return 0;
}

