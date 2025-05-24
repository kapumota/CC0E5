#include <iostream>      // std::cout
#include <memory>        // std::unique_ptr, std::make_unique
#include <optional>      // std::optional, std::nullopt
#include <random>        // std::mt19937, std::uniform_real_distribution
#include <limits>        // std::numeric_limits
#include <algorithm>     // std::max
#include <utility>       // std::move

struct TreapNode {
    int key;
    int value;
    double priority;
    std::unique_ptr<TreapNode> left;
    std::unique_ptr<TreapNode> right;
    int subtree_max;

    TreapNode(int k, int v, std::optional<double> p = std::nullopt)
        : key{k}, value{v},
          priority{p.value_or(random_priority())},
          subtree_max{v} {}

private:
    static double random_priority() {
        static thread_local std::mt19937 rng(std::random_device{}());
        static std::uniform_real_distribution<double> dist(0.0, 1.0);
        return dist(rng);
    }
};

/* ---------- utilidades ---------- */
static void update(TreapNode* n) {
    if (!n) return;
    n->subtree_max = n->value;
    if (n->left)  n->subtree_max = std::max(n->subtree_max, n->left->subtree_max);
    if (n->right) n->subtree_max = std::max(n->subtree_max, n->right->subtree_max);
}

static std::unique_ptr<TreapNode> rotate_left(std::unique_ptr<TreapNode> p) {
    auto r = std::move(p->right);
    p->right = std::move(r->left);
    r->left = std::move(p);
    update(r->left.get());
    update(r.get());
    return r;
}

static std::unique_ptr<TreapNode> rotate_right(std::unique_ptr<TreapNode> p) {
    auto l = std::move(p->left);
    p->left = std::move(l->right);
    l->right = std::move(p);
    update(l->right.get());
    update(l.get());
    return l;
}

/* ---------- inserción ---------- */
std::unique_ptr<TreapNode> insert(std::unique_ptr<TreapNode> root,
                                  int key, int value,
                                  std::optional<double> pr = std::nullopt) {
    if (!root) return std::make_unique<TreapNode>(key, value, pr);

    if (key < root->key) {
        root->left = insert(std::move(root->left), key, value, pr);
        if (root->left->priority < root->priority)
            root = rotate_right(std::move(root));
    } else if (key > root->key) {
        root->right = insert(std::move(root->right), key, value, pr);
        if (root->right->priority < root->priority)
            root = rotate_left(std::move(root));
    } else {
        root->value = value;            // clave existente → actualiza valor
    }
    update(root.get());
    return root;
}

/* ---------- eliminación ---------- */
std::unique_ptr<TreapNode> delete_key(std::unique_ptr<TreapNode> root, int key) {
    if (!root) return nullptr;
    if (key < root->key) {
        root->left = delete_key(std::move(root->left), key);
    } else if (key > root->key) {
        root->right = delete_key(std::move(root->right), key);
    } else {
        if (!root->left && !root->right) return nullptr;
        if (root->left &&
            (!root->right || root->left->priority < root->right->priority)) {
            root = rotate_right(std::move(root));
            root->right = delete_key(std::move(root->right), key);
        } else {
            root = rotate_left(std::move(root));
            root->left = delete_key(std::move(root->left), key);
        }
    }
    update(root.get());
    return root;
}

/* ---------- consulta de rango ---------- */
std::optional<int> max_in_range(const TreapNode* root, int lo, int hi) {
    if (!root || lo > hi) return std::nullopt;
    const TreapNode* cur = root;
    int best = std::numeric_limits<int>::min();

    while (cur) {
        if (cur->key < lo) {
            cur = cur->right.get();
        } else if (cur->key > hi) {
            cur = cur->left.get();
        } else {
            best = std::max(best, cur->value);
            if (cur->left && cur->left->key >= lo)
                best = std::max(best, cur->left->subtree_max);
            cur = cur->right.get();
        }
    }
    return (best == std::numeric_limits<int>::min())
           ? std::nullopt
           : std::optional<int>(best);
}

/* ---------- demo mínima ---------- */
int main() {
    std::unique_ptr<TreapNode> root;
    root = insert(std::move(root), 10, 42);
    root = insert(std::move(root), 5, 99);
    root = insert(std::move(root), 15, 7);

    auto mx = max_in_range(root.get(), 1, 20);
    if (mx) std::cout << "Valor máximo en [1,20] = " << *mx << '\n';
    return 0;
}
