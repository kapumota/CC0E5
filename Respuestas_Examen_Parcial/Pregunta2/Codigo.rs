//! src/main.rs
//! Rust 2021 — Suffix-tree + búsqueda de substring k-frecuente más largo
//! (compila limpio con `cargo run --release`).


//   1.  Suffix-array (ordenación O(n log² n)) + LCP (Kasai)

fn build_sa(text: &[u8]) -> Vec<usize> {
    let n = text.len();
    let mut sa: Vec<usize> = (0..n).collect();
    let mut rank = text.iter().map(|&c| c as i32).collect::<Vec<_>>();
    let mut tmp  = vec![0i32; n];
    let mut k = 1;

    while k < n {
        sa.sort_by(|&i, &j| {
            let a = (rank[i], rank.get(i + k).copied().unwrap_or(-1));
            let b = (rank[j], rank.get(j + k).copied().unwrap_or(-1));
            a.cmp(&b)
        });

        tmp[sa[0]] = 0;
        for idx in 1..n {
            let prev = sa[idx - 1];
            let cur  = sa[idx];
            tmp[cur] = tmp[prev]
                + (rank[prev], rank.get(prev + k).copied().unwrap_or(-1))
                    .cmp(&(rank[cur],  rank.get(cur  + k).copied().unwrap_or(-1))) as i32;
        }
        rank.clone_from_slice(&tmp);
        if rank[sa[n - 1]] == (n as i32 - 1) { break; }
        k <<= 1;
    }
    sa
}

fn build_lcp(text: &[u8], sa: &[usize]) -> Vec<usize> {
    let n = text.len();
    let mut rank = vec![0usize; n];
    for (i, &p) in sa.iter().enumerate() { rank[p] = i; }

    let mut h = 0usize;
    let mut lcp = vec![0usize; n - 1];
    for i in 0..n {
        if rank[i] == n - 1 { h = 0; continue; }
        let j = sa[rank[i] + 1];
        while i + h < n && j + h < n && text[i + h] == text[j + h] { h += 1; }
        lcp[rank[i]] = h;
        if h > 0 { h -= 1; }
    }
    lcp
}


//   2.  Árbol de sufijos compacto a partir de SA+LCP
#[derive(Clone)]
struct Edge { start: usize, end: usize, child: Box<Node> }

#[derive(Clone)]
struct Node {
    edges:  Vec<Edge>,
    leaves: Vec<usize>,   // posiciones de los sufijos bajo este nodo
}
impl Node { fn new() -> Self { Self { edges: vec![], leaves: vec![] } } }

fn sa_lcp_to_tree(text: &[u8], sa: &[usize], lcp: &[usize]) -> Box<Node> {
    let n = text.len();
    let mut root = Box::new(Node::new());
    let mut stack: Vec<(Box<Node>, usize)> = vec![(root, 0)]; // (nodo, profundidad)

    for (i, &suf_start) in sa.iter().enumerate() {
        let lcp_prev = if i == 0 { 0 } else { lcp[i - 1] };

        // 1) Desapila hasta que la profundidad ≤ lcp_prev
        while let Some(&(_, depth)) = stack.last() {
            if depth <= lcp_prev { break; }
            let (mut node, _) = stack.pop().unwrap();
            let label_len: usize =
                node.edges.iter().map(|e| e.end - e.start).sum::<usize>();
            if let Some((parent, pdepth)) = stack.last_mut() {
                parent.leaves.extend(&node.leaves);
                parent.edges.push(Edge {
                    start: suf_start + *pdepth,                 // ← *pdepth
                    end:   suf_start + *pdepth + label_len,     // ← *pdepth
                    child: node,
                });
            }
        }

        // 2) Crea hoja para sufijo actual
        let mut leaf = Box::new(Node::new());
        leaf.leaves.push(suf_start);
        if let Some((parent, depth)) = stack.last_mut() {
            parent.edges.push(Edge {
                start: suf_start + *depth,
                end:   n,
                child: leaf.clone(),
            });
        }
        stack.push((leaf, n - suf_start));
    }

    // 3) Vacía la pila restante
    while stack.len() > 1 {
        let (mut node, _) = stack.pop().unwrap();
        if let Some((parent, _)) = stack.last_mut() {
            parent.leaves.extend(&node.leaves);
            parent.edges.extend(node.edges.drain(..));
        }
    }
    stack.pop().unwrap().0
}


//   3.  Substring k-frecuente más largo
#[derive(Clone, Copy)]
struct Candidate { depth: usize, node: *const Node }

pub fn find_longest_k_frequent_substring(
    root: &Node,
    text: &[u8],
    k: usize,
) -> Option<(String, Vec<usize>)> {
    if k == 0 { return None; }

    // DFS para localizar el nodo más profundo con ≥ k hojas
    let mut best = Candidate { depth: 0, node: root as *const _ };
    let mut stack = vec![(root as *const Node, 0usize, 0usize)]; // (ptr, depth, edge_idx)

    while let Some((ptr, depth, idx)) = stack.pop() {
        let node = unsafe { &*ptr };
        if node.leaves.len() >= k && depth > best.depth {
            best = Candidate { depth, node: ptr };
        }
        if idx < node.edges.len() {
            // Devuelve el nodo con índice incrementado
            stack.push((ptr, depth, idx + 1));
            let e = &node.edges[idx];
            stack.push((&*e.child as *const _, depth + (e.end - e.start), 0));
        }
    }
    if best.depth == 0 { return None; }

    // Reconstruir la cadena: sigue un camino desde la raíz al nodo ganador
    let mut substr = Vec::with_capacity(best.depth);
    let mut cur = root as *const Node;
    while cur != best.node {
        let node = unsafe { &*cur };
        let (edge, child_ptr) = node.edges
            .iter()
            .find_map(|e| {
                let p = &*e.child as *const _;
                if subtree_contains(p, best.node) { Some((e, p)) } else { None }
            })
            .unwrap();
        substr.extend_from_slice(&text[edge.start..edge.end]);
        cur = child_ptr;
    }

    let positions = unsafe { &*best.node }.leaves.clone();
    Some((String::from_utf8(substr).unwrap(), positions))
}

// Utilidad recursiva: ¿subárbol de x contiene y?
fn subtree_contains(x: *const Node, y: *const Node) -> bool {
    if x == y { return true; }
    let node = unsafe { &*x };
    node.edges.iter().any(|e| subtree_contains(&*e.child as *const _, y))
}

//  4.  Demo
   
fn main() {
    let text = "banana_bandana$";     // '$' centinela único
    let k = 2;

    let bytes = text.as_bytes();
    let sa   = build_sa(bytes);
    let lcp  = build_lcp(bytes, &sa);
    let tree = sa_lcp_to_tree(bytes, &sa, &lcp);

    match find_longest_k_frequent_substring(&tree, bytes, k) {
        Some((s, pos)) => {
            println!("Substring más largo con frecuencia ≥ {k}: \"{s}\"");
            println!("Longitud: {}", s.len());
            println!("Posiciones: {pos:?}");
        }
        None => println!("No existe substring que aparezca {k} veces."),
    }
}
