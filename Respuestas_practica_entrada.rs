// Problema 1

use std::io::{self, BufRead, Write};

/// Estructura para almacenar los requerimientos de cada persona.
#[derive(Debug)]
struct Persona {
    a: i32,
    b: i32,
    c: i32,
}

/// BIT2D (Fenwick Tree 2D) para actualización y consulta en dos dimensiones.
/// Se usa 1-indexación, por lo que se crea un vector de dimensiones (n+1) x (m+1).
struct BIT2D {
    n: usize, // tamaño para la dimensión B
    m: usize, // tamaño para la dimensión C
    data: Vec<Vec<i32>>,
}

impl BIT2D {
    fn new(n: usize, m: usize) -> BIT2D {
        BIT2D {
            n,
            m,
            data: vec![vec![0; m + 1]; n + 1],
        }
    }

    /// Actualiza la BIT en la posición (i, j) (1-indexado) sumando `delta`.
    fn update(&mut self, mut i: usize, j: usize, delta: i32) {
        while i <= self.n {
            let mut j_index = j;
            while j_index <= self.m {
                self.data[i][j_index] += delta;
                // j_index & -j_index se implementa usando wrapping_neg()
                j_index += j_index & j_index.wrapping_neg();
            }
            i += i & i.wrapping_neg();
        }
    }

    /// Consulta la suma acumulada en el rectángulo [1, i] x [1, j].
    fn query(&self, mut i: usize, j: usize) -> i32 {
        let mut res = 0;
        while i > 0 {
            let mut j_index = j;
            while j_index > 0 {
                res += self.data[i][j_index];
                j_index -= j_index & j_index.wrapping_neg();
            }
            i -= i & i.wrapping_neg();
        }
        res
    }
}

fn main() {
    let stdin = io::stdin();
    let mut iterator = stdin.lock().lines();

    // Lee el número de casos de prueba T.
    let t: i32 = iterator
        .next()
        .unwrap()
        .unwrap()
        .trim()
        .parse()
        .expect("Error al leer T");

    for tc in 1..=t {
        // Lee el número de personas N.
        let n: usize = iterator
            .next()
            .unwrap()
            .unwrap()
            .trim()
            .parse()
            .expect("Error al leer N");

        let mut personas = Vec::with_capacity(n);
        let mut global_a = 0;
        let mut global_b = 0;
        let mut global_c = 0;

        // Lee las preferencias de cada persona y calcula máximos globales.
        for _ in 0..n {
            let line = iterator.next().unwrap().unwrap();
            let parts: Vec<i32> = line
                .split_whitespace()
                .map(|s| s.parse().expect("Error al parsear un entero"))
                .collect();
            let a = parts[0];
            let b = parts[1];
            let c = parts[2];
            global_a = global_a.max(a);
            global_b = global_b.max(b);
            global_c = global_c.max(c);
            personas.push(Persona { a, b, c });
        }

        // Si se puede satisfacer a todas las personas con la mezcla (maximos globales)
        if global_a + global_b + global_c <= 10000 {
            println!("Caso #{}: {}", tc, n);
            continue;
        }

        // Recolecta los candidatos (valores únicos) para A, B y C, incluyendo 0 y 10000.
        let mut cand_a = vec![0, 10000];
        let mut cand_b = vec![0, 10000];
        let mut cand_c = vec![0, 10000];

        for p in &personas {
            cand_a.push(p.a);
            cand_b.push(p.b);
            cand_c.push(p.c);
        }

        // Ordena y elimina duplicados.
        cand_a.sort();
        cand_a.dedup();
        cand_b.sort();
        cand_b.dedup();
        cand_c.sort();
        cand_c.dedup();

        // Ordena las personas según su requerimiento en A.
        personas.sort_by_key(|p| p.a);

        // Funciones de compresión de coordenadas para B y C que generan índices 1-indexados.
        let get_index_b = |value: i32| -> usize {
            match cand_b.binary_search(&value) {
                Ok(idx) => idx + 1,
                Err(idx) => idx + 1,
            }
        };
        let get_index_c = |value: i32| -> usize {
            match cand_c.binary_search(&value) {
                Ok(idx) => idx + 1,
                Err(idx) => idx + 1,
            }
        };

        let size_b = cand_b.len();
        let size_c = cand_c.len();

        // Crea la BIT2D para las dimensiones B y C.
        let mut bit2d = BIT2D::new(size_b, size_c);
        let mut ans = 0;
        let mut pos = 0; // índice para recorrer las personas (ordenadas por A)

        // Se recorre cada candidato x (para A) en forma creciente.
        for &x in &cand_a {
            // Agrega a la BIT las personas cuyo A es <= x.
            while pos < personas.len() && personas[pos].a <= x {
                let idx_b = get_index_b(personas[pos].b);
                let idx_c = get_index_c(personas[pos].c);
                bit2d.update(idx_b, idx_c, 1);
                pos += 1;
            }

            // Para cada candidato y (para B) tal que la mezcla es válida (x+y <= 10000)
            for (j, &y) in cand_b.iter().enumerate() {
                if x + y > 10000 {
                    break;
                }
                let z = 10000 - x - y;

                // Usamos `partition_point` para obtener el "upper_bound" en cand_c para el valor z.
                let pos_c = cand_c.partition_point(|&v| v <= z);
                if pos_c == 0 {
                    continue;
                }

                // j es el índice 0-indexado en cand_b. Se usa j+1 para trabajar con BIT 1-indexado.
                let count = bit2d.query(j + 1, pos_c);
                ans = ans.max(count);
            }
        }

        println!("Caso #{}: {}", tc, ans);
    }
}

// Problema 2

use std::cmp;
use std::collections::HashMap;
use std::io::{self, BufRead, Write};

/// Para cada arista (u,v) con u < v, almacenamos la lista de "hijos" (vértices que se añadieron conectándose a u y v).
type ChildrenMap = HashMap<(usize, usize), Vec<usize>>;

/// El resultado de F(u,v): (valor, mejor_hijo, segundo_mejor_valor)
/// Si no hay ningún hijo, F(u,v) = (0, None, 0)
type FResult = (usize, Option<usize>, usize);

/// Función recursiva con memoización que calcula F(u,v).
/// Se supone que u < v.
fn f(u: usize, v: usize, children: &ChildrenMap, memo: &mut HashMap<(usize, usize), FResult>) -> FResult {
    if let Some(&res) = memo.get(&(u, v)) {
        return res;
    }
    let mut best = 0;
    let mut best_child = None;
    let mut second = 0;
    if let Some(child_list) = children.get(&(u, v)) {
        for &w in child_list.iter() {
            // Como w es agregado a una arista cuyos extremos son anteriores, se tiene: u < v < w.
            let (fu_w, _, _) = f(u, w, children, memo);
            let (fv_w, _, _) = f(v, w, children, memo);
            let candidate = 1 + fu_w + fv_w;
            if candidate > best {
                second = best;
                best = candidate;
                best_child = Some(w);
            } else if candidate > second {
                second = candidate;
            }
        }
    }
    let res = (best, best_child, second);
    memo.insert((u, v), res);
    res
}

/// Versión de f(u,v) que “excluye” el hijo 'forbid' (si se suministra)
fn f_forbid(u: usize, v: usize, forbid: Option<usize>, children: &ChildrenMap, memo: &mut HashMap<(usize, usize), FResult>) -> usize {
    let (best, best_child, second) = f(u, v, children, memo);
    if let Some(x) = forbid {
        if best_child == Some(x) {
            return second;
        }
    }
    best
}

/// Función que resuelve un caso de prueba.
fn solve_case<R: BufRead, W: Write>(reader: &mut R, writer: &mut W, case_number: usize) {
    let mut buf = String::new();
    reader.read_line(&mut buf).expect("Error leyendo N");
    let n: usize = buf.trim().parse().expect("No es un entero");
    
    // Inicializamos el mapa de hijos para las aristas.
    // Usamos solo claves con (u,v) con u < v.
    let mut children: ChildrenMap = HashMap::new();
    
    // El triángulo base: vértices 1,2,3. Aseguramos que las tres aristas existan (aunque sin hijos).
    children.entry((1, 2)).or_insert(Vec::new());
    children.entry((1, 3)).or_insert(Vec::new());
    children.entry((2, 3)).or_insert(Vec::new());
    
    // Para poder iterar luego en los triángulos "nuevos", guardamos (u,v,i) para cada vértice i añadido.
    let mut added_triangles: Vec<(usize, usize, usize)> = Vec::new();
    
    // Para cada vértice i de 4 a n, leemos la línea con dos enteros: A y B (sus dos conexiones).
    for i in 4..=n {
        buf.clear();
        reader.read_line(&mut buf).expect("Error leyendo línea");
        let parts: Vec<usize> = buf
            .trim()
            .split_whitespace()
            .map(|s| s.parse::<usize>().expect("No es un entero"))
            .collect();
        let a = parts[0];
        let b = parts[1];
        let (u, v) = if a < b { (a, b) } else { (b, a) };
        // Este vértice i se conecta a la arista (u,v). Se añade como hijo de dicha arista.
        children.entry((u, v)).or_insert(Vec::new()).push(i);
        // Guardamos el triángulo que se forma: (u, v, i)
        added_triangles.push((u, v, i));
        // Además se crean las nuevas aristas: (a, i) y (b, i).
        let key_ai = if a < i { (a, i) } else { (i, a) };
        let key_bi = if b < i { (b, i) } else { (i, b) };
        children.entry(key_ai).or_insert(Vec::new());
        children.entry(key_bi).or_insert(Vec::new());
    }
    
    // Usamos un mapa para memoizar los valores de F.
    let mut memo: HashMap<(usize, usize), FResult> = HashMap::new();
    
    let mut answer = 0;
    // Opción 1: usar el triángulo base (1,2,3)
    {
        let val = f_forbid(1, 2, None, &children, &mut memo)
            + f_forbid(1, 3, None, &children, &mut memo)
            + f_forbid(2, 3, None, &children, &mut memo)
            + 3;
        answer = cmp::max(answer, val);
    }
    
    // Opción 2: cada vértice añadido forma un triángulo único con sus dos conexiones.
    for &(u, v, w) in added_triangles.iter() {
        let val = f_forbid(u, v, Some(w), &children, &mut memo)
            + f_forbid(u, w, Some(v), &children, &mut memo)
            + f_forbid(v, w, Some(u), &children, &mut memo)
            + 3;
        answer = cmp::max(answer, val);
    }
    
    writeln!(writer, "Caso #{}: {}", case_number, answer).expect("Error al escribir");
}

fn main() {
    // Usamos lock de stdin y stdout.
    let stdin = io::stdin();
    let mut reader = stdin.lock();
    let stdout = io::stdout();
    let mut writer = io::BufWriter::new(stdout.lock());
    
    let mut buf = String::new();
    reader.read_line(&mut buf).expect("Error leyendo T");
    let t: usize = buf.trim().parse().expect("No es un entero T");
    
    for case in 1..=t {
        solve_case(&mut reader, &mut writer, case);
    }
}
