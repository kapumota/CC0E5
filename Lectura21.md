## Evolución de la búsqueda de vecinos más cercanos: de 1-D a k-d trees

Hasta ahora hemos trabajado con contenedores que albergaban datos unidimensionales: las entradas que almacenábamos en colas, árboles y tablas hash siempre se asumían como números (o como traducibles a ellos): valores simples que podían compararse en el sentido matemático más intuitivo. 
En esta nota, veremos cómo esta simplificación no siempre se cumple en conjuntos de datos reales y examinaremos los problemas relacionados con el manejo de datos multidimensionales más complejos.

### El problema de búsqueda de vecinos más cercanos 

Comencemos el recorrido imaginando un mapa que muestra algunas ciudades y la ubicación de algunos almacenes (*warehouse*). 

<img src="https://github.com/kapumota/CC0E5/blob/main/data/Ciudades.png" alt="Descripción" width="650" height="400">


Imagina que estás viviendo en los años 90, en los albores de la era de internet, cuando el comercio electrónico estaba dando sus primeros pasos. 
Tienes una tienda en línea donde vendes productos de producción local colaborando con algunos minoristas. Ellos venden a tiendas físicas, y tú les proporcionas la infraestructura para vender también en línea, por una pequeña comisión.
Cada almacén se encarga de los envíos de sus pedidos, pero para atraer más minoristas a tu plataforma, ofreces un trato especial: por cada entrega a más de 10 km, reducirás tu comisión proporcionalmente a la distancia.

Volviendo al mapa imaginario. Eres el arquitecto principal de esta empresa y tu objetivo principal es encontrar, cuando un cliente hace un pedido, el almacén más cercano que tenga el producto en stock y, si es posible, que esté dentro de un radio de 10 km. En resumen, para que tu empresa se mantenga operativa (y para conservar tu trabajo), es vital que siempre redirijas a cada usuario al almacén más cercano. 

Imagina que alguien desde Ciudad Gótica intenta ordenar un queso francés. Miras tu lista de almacenes, calculas la distancia entre la dirección del cliente y cada uno de ellos, y eliges el más cercano, P-5. Inmediatamente después, alguien desde Metrópolis compra dos ruedas del mismo queso; lamentablemente, no puedes usar ninguna de las distancias calculadas antes, porque el punto de origen (la ubicación del cliente) es completamente diferente.
Así que simplemente vuelves a recorrer la lista de tiendas, calculas todas las distancias, y eliges el almacén B-2. Si el siguiente pedido viene, por ejemplo, desde Civic City.  Tienes que volver a calcular todas las N distancias para todos los N almacenes.

#### Soluciones

Ahora bien, sé que el  mapa imaginario indica solo cinco almacenes, así que parece una operación trivial y rápida revisar todos ellos para cada usuario. Incluso podrías gestionar los pedidos manualmente, eligiendo caso por caso basándote en tu intuición y experiencia.

Pero supón que, tras un año, como tu negocio va bien, más tiendas deciden vender en tu sitio web, y ya tienes cerca de cien en esa misma área. 
Eso se vuelve complicado, y tu equipo de atención al cliente no puede manejar mil pedidos al día: seleccionar manualmente el lugar más cercano para cada
pedido ya no funciona. Entonces escribes un pequeño fragmento de código que realiza automáticamente los pasos anteriores para cada pedido y verifica todas  las distancias.

```python
# Ejemplo conceptual de cálculo de distancias a todos los almacenes
def encontrar_almacen_mas_cercano_lineal(ubicacion_cliente, almacenes_stock):
    """
    Encuentra el almacén más cercano mediante escaneo lineal.

    Args:
        ubicacion_cliente (tuple): Coordenadas (x, y) del cliente.
        almacenes_stock (dict): Diccionario donde las claves son nombres de almacenes
                                 y los valores son diccionarios con 'ubicacion' (tuple)
                                 y 'stock' (int).

    Returns:
        str: Nombre del almacén más cercano con stock.
             None si no hay almacenes con stock.
    """
    almacen_mas_cercano = None
    distancia_minima = float('inf')

    for nombre_almacen, datos_almacen in almacenes_stock.items():
        if datos_almacen['stock'] > 0:
            # Asumimos una función calcular_distancia_2d simple
            # Para este ejemplo, usaremos distancia euclidiana al cuadrado para simplificar
            dist = ((ubicacion_cliente[0] - datos_almacen['ubicacion'][0])**2 +
                    (ubicacion_cliente[1] - datos_almacen['ubicacion'][1])**2)

            if dist < distancia_minima:
                distancia_minima = dist
                almacen_mas_cercano = nombre_almacen
    return almacen_mas_cercano

# Datos de ejemplo
cliente_gotham = (10, 20) # (x, y)
almacenes = {
    "P-5": {"ubicacion": (12, 22), "stock": 5},
    "B-2": {"ubicacion": (30, 40), "stock": 3},
    "W-1": {"ubicacion": (5, 5), "stock": 0}, # Sin stock
    "S-Mart": {"ubicacion": (15, 18), "stock": 10}
}

# print(f"Almacén más cercano para Gotham: {encontrar_almacen_mas_cercano_lineal(cliente_gotham, almacenes)}")
```

Pero luego de otro año, el negocio va tan bien que tu CEO decide que están listos para operar a nivel nacional tras cerrar un trato que hará que cientos o miles de tiendas medianas y grandes (distribuidas por todo el país) se unan a tu plataforma.

Calcular millones de distancias por usuario empieza a parecer abrumador e ineficiente además, dado que estamos en los años 90, los servidores no son tan rápidos, los centros de datos son una rareza y las granjas de servidores son cosas de grandes compañías como IBM.  Aún no existen como recurso para el comercio electrónico.


#### Primeros intentos 

Tu primera propuesta puede ser precalcular el almacén más cercano para cada usuario de una vez por todos los productos, pero eso no funciona realmente, porque los usuarios pueden mudarse, o a veces quieren que se les envíe el producto a su oficina o al correo, y no a su casa. 
Además, la disponibilidad de productos cambiará con el tiempo, por lo que la tienda más cercana no siempre será la mejor. Tendrías que mantener una lista de tiendas ordenadas por distancia para cada cliente (o al menos cada ciudad).

Razonando en 2D, podríamos intentar un enfoque distinto, inspirado en los mapas reales: dividir el mapa en secciones, usando una cuadrícula regular. 
De esta forma, podemos encontrar fácilmente en qué sección cae un punto a partir de sus coordenadas (simplemente dividiendo el valor de cada coordenada por el tamaño de la celda) y buscar los puntos más cercanos en esa celda o en las celdas vecinas. Esto ayuda a reducir el número de puntos que necesitamos comparar; sin embargo, hay una trampa. 

Este enfoque funciona si los datos están espaciados de forma regular, lo cual no suele ser el caso en conjuntos de datos reales.

```python
# Ejemplo conceptual de indexación con cuadrícula regular
def asignar_a_celda(punto, tamano_celda):
    """Asigna un punto a una celda de la cuadrícula."""
    # punto es una tupla (x, y)
    celda_x = int(punto[0] // tamano_celda)
    celda_y = int(punto[1] // tamano_celda)
    return (celda_x, celda_y)

# punto_cliente = (75, 125)
# tamano_celda_mapa = 50
# celda_cliente = asignar_a_celda(punto_cliente, tamano_celda_mapa)
# print(f"El cliente en {punto_cliente} cae en la celda: {celda_cliente}")

# # Supongamos que tenemos algunos almacenes y sus ubicaciones
# almacenes_ubicaciones = {
# "A1": (10, 20), "A2": (12, 25), "A3": (80, 130),
# "A4": (450, 460), "A5": (455, 465), "A6": (470, 480)
# }
# # Indexar almacenes en celdas
# celdas_almacenes = {}
# for nombre, ubicacion in almacenes_ubicaciones.items():
#     celda = asignar_a_celda(ubicacion, tamano_celda_mapa)
#     if celda not in celdas_almacenes:
#         celdas_almacenes[celda] = []
#     celdas_almacenes[celda].append(nombre)

# print("\nAlmacenes por celda:")
# for celda, nombres_almacenes in celdas_almacenes.items():
#     print(f"Celda {celda}: {nombres_almacenes}")
# # En este ejemplo, A1 y A2 estarían en la celda (0,0). A3 en (1,2).
# # A4, A5, A6 estarían en (9,9), mostrando cómo una celda puede tener alta densidad
# # y muchas otras estar vacías.
```
Los datos reales forman clústeres, conglomerados densos de puntos cercanos entre sí, alternados con áreas dispersas. 
Con una cuadrícula regular, el riesgo es tener muchas celdas vacías y unas pocas con cientos o miles de puntos, lo que anula el propósito del enfoque. 
Necesitamos algo diferente, algo más flexible.


#### Simplificar las cosas para obtener una pista 

La solución a este problema parece escurridiza. En estos casos, a veces ayuda resolver una versión simplificada del problema y luego idear una solución general que funcione para el problema original. 

Supongamos, por ejemplo, que pudiéramos restringir la búsqueda a un espacio unidimensional. 

Digamos que necesitamos atender solo a clientes en una única carretera que se extiende por kilómetros y todos los almacenes también están colocados a lo largo de esa misma carretera.

Para simplificar aún más, supongamos que la carretera es perfectamente recta, y que la distancia total cubierta es lo suficientemente corta como para no preocuparnos por la curvatura de la Tierra, latitud, longitud, etc.  Básicamente, asumimos que una aproximación con un segmento 1D es suficiente, y podemos usar la distancia euclidiana en 1D como una estimación de la distancia real entre ciudades.

Podemos representar las ubicaciones en esta línea como simples números.
```python
# Ciudades y almacenes en una línea 1-D (distancia desde un origen 0)
ubicaciones_1d = {
    "W-3 (Almacén)": 10,
    "Ciudad Gótica": 20,
    "B-2 (Almacén)": 32,
    "Civic City": 40,
    "P-5 (Almacén)": 62,
    "Metrópolis": 80,
    "Happy Harbor": 93
}
# Ordenados por posición para facilitar la visualización
puntos_ordenados_1d = sorted(ubicaciones_1d.items(), key=lambda item: item[1])
# print("Ubicaciones en 1-D (nombre, posición):")
# for nombre, pos in puntos_ordenados_1d:
# print(f"- {nombre}: {pos}")
```
Esta es una aproximación del escenario inicial, donde esos puntos pertenecen a un plano 2-D, que a su vez es una aproximación de la realidad, donde los mismos puntos están en una superficie curva tridimensional. Dependiendo del caso de uso, puede que nos baste con alguna de las aproximaciones, o que necesitemos un modelo más preciso que tenga en cuenta la curvatura terrestre.

Dado un punto aleatorio en el segmento, queremos saber cuál de los puntos de referencia está más cerca. Estando en un caso 1-D, esto se parece mucho a una búsqueda binaria.

```python
import bisect

def encontrar_vecino_mas_cercano_1d_bsearch(puntos_ordenados_valores, objetivo):
    """
    Encuentra el vecino más cercano en una lista ordenada de valores 1-D.

    Args:
        puntos_ordenados_valores (list): Lista de valores numéricos ordenados.
        objetivo (float): El valor para el cual buscar el vecino más cercano.

    Returns:
        float: El valor del vecino más cercano.
               None si la lista está vacía.
    """
    if not puntos_ordenados_valores:
        return None

    # Encontrar el punto de inserción
    # bisect_left devuelve un índice tal que todos e en a[:idx] tienen e < x,
    # y todos e en a[idx:] tienen e >= x.
    idx = bisect.bisect_left(puntos_ordenados_valores, objetivo)

    # Casos límite
    if idx == 0: # El objetivo es menor o igual al primer elemento
        return puntos_ordenados_valores[0]
    if idx == len(puntos_ordenados_valores): # El objetivo es mayor que el último elemento
        return puntos_ordenados_valores[-1]

    # Comparamos con el elemento en idx y el anterior (idx-1)
    vecino_izquierdo = puntos_ordenados_valores[idx - 1]
    vecino_derecho = puntos_ordenados_valores[idx]

    if abs(objetivo - vecino_izquierdo) <= abs(objetivo - vecino_derecho):
        return vecino_izquierdo
    else:
        return vecino_derecho

# Ejemplo de uso con los valores de los puntos ordenados
valores_1d = [pos for _, pos in puntos_ordenados_1d] # Extraer solo las posiciones
# objetivo_cliente = 75
# vecino_cercano = encontrar_vecino_mas_cercano_1d_bsearch(valores_1d, objetivo_cliente)

# Encontrar el nombre correspondiente al valor
# nombre_vecino = ""
# for nombre, pos in puntos_ordenados_1d:
# if pos == vecino_cercano:
# nombre_vecino = nombre
# break
# print(f"\nPara un cliente en la posición {objetivo_cliente}:")
# print(f"La búsqueda binaria indica que el vecino más cercano está en la posición: {vecino_cercano} ({nombre_vecino})")
# (El texto original menciona Happy Harbor (93) o Metrópolis (80).
# Con el objetivo 75, 80 está a 5 unidades, 62 está a 13 unidades. Así que 80 (Metrópolis) es más cercano)
# Corrigiendo el ejemplo del texto:
# Si el objetivo es 75:
# idx = bisect.bisect_left([10, 20, 32, 40, 62, 80, 93], 75) -> idx = 5 (valor 80)
# vecino_izquierdo = puntos_ordenados_valores[4] = 62
# vecino_derecho = puntos_ordenados_valores[5] = 80
# abs(75 - 62) = 13
# abs(75 - 80) = 5
# Entonces, 80 es el más cercano.
```

#### Elegir cuidadosamente una estructura de datos

La búsqueda binaria en un array es útil, pero los arrays no son conocidos por su flexibilidad. Si quisiéramos agregar un nuevo punto entre W-3 y B-2, tendríamos que mover todos los elementos desde B-2 hasta B-4, y posiblemente realocar el array si es estático.

Afortunadamente, conocemos una estructura de datos más flexible que los arrays y que nos permite realizar búsquedas binarias eficientemente. Como su nombre indica, un **árbol binario de búsqueda (BST)** es lo que buscamos. 

Para garantizar tiempos de ejecución logarítmicos en las operaciones más comunes, el árbol debe estar balanceado.

```python
# Definición conceptual de un nodo de BST y una función de inserción simple
class NodoBST:
    def __init__(self, clave, valor=None):
        self.clave = clave # La posición en 1D
        self.valor = valor # El nombre del lugar (opcional)
        self.izquierda = None
        self.derecha = None
        self.padre = None # Útil para encontrar el vecino más cercano

def insertar_bst(raiz, clave, valor=None):
    if raiz is None:
        return NodoBST(clave, valor)
    
    actual = raiz
    padre_actual = None
    while actual is not None:
        padre_actual = actual
        if clave < actual.clave:
            actual = actual.izquierda
        elif clave > actual.clave:
            actual = actual.derecha
        else: # Clave ya existe
            actual.valor = valor # Actualizar valor si es necesario
            return raiz 

    nuevo_nodo = NodoBST(clave, valor)
    nuevo_nodo.padre = padre_actual
    if clave < padre_actual.clave:
        padre_actual.izquierda = nuevo_nodo
    else:
        padre_actual.derecha = nuevo_nodo
    return raiz

# Construir un BST (no necesariamente balanceado aquí para simplificar)
# con los datos 1D:
# datos_1d_bst = {10: "W-3", 20: "Gótica", 32: "B-2", 40: "Civic", 62: "P-5", 80: "Metrópolis", 93: "Happy H."}
# raiz_bst = None
# for pos, nombre in datos_1d_bst.items():
#     raiz_bst = insertar_bst(raiz_bst, pos, nombre)

# (Nota: Un árbol balanceado requeriría algoritmos como AVL o Rojo-Negro
# que son más complejos de implementar brevemente aquí.
# Para el ejemplo, un BST simple ilustra la estructura.)
```
Para este ejemplo, mostramos un árbol que contiene tanto ciudades como almacenes. 

Puedes imaginar, para simplificar, que cada ciudad tiene un gran almacén o centro de distribución, así que las búsquedas simplemente devuelven la entrada más cercana (ya sea ciudad o almacén) a un cliente (que no está en una ciudad del árbol).

Y en efecto, las operaciones de inserción, eliminación y búsqueda están garantizadas como logarítmicas en el BST balanceado. 
Esto es mucho mejor que la búsqueda lineal inicial. Un tiempo logarítmico crece increíblemente lento; solo piensa que para un millón de puntos, 
pasaríamos de calcular un millón de distancias a solo unas 20.

El siguiente código muestra cómo ejecutaríamos una búsqueda en el BST para encontrar el vecino más cercano de un punto cuya coordenada x es 75.

```python
def buscar_en_bst(raiz, clave_objetivo):
    actual = raiz
    ultimo_visitado = None
    while actual is not None:
        ultimo_visitado = actual
        if clave_objetivo == actual.clave:
            return actual # Coincidencia exacta
        elif clave_objetivo < actual.clave:
            actual = actual.izquierda
        else:
            actual = actual.derecha
    return ultimo_visitado # No hay coincidencia exacta, devuelve el último nodo visitado

def vecino_mas_cercano_bst_1d(raiz, clave_objetivo):
    if raiz is None:
        return None

    nodo_final_busqueda = buscar_en_bst(raiz, clave_objetivo)

    if nodo_final_busqueda.clave == clave_objetivo:
        return nodo_final_busqueda # Coincidencia exacta

    # Si no hay coincidencia exacta, el vecino más cercano es el último nodo visitado
    # o su padre. Para ser más precisos, comparamos el nodo_final_busqueda
    # (que es el nodo hoja donde terminaría la búsqueda o el nodo igual al objetivo)
    # con su sucesor y predecesor en orden si el objetivo no está en el árbol.
    # De forma más simple, como se sugiere en el texto,
    # comparamos el último nodo visitado y su padre.

    candidatos = [nodo_final_busqueda]
    if nodo_final_busqueda.padre:
        candidatos.append(nodo_final_busqueda.padre)
    
    # También podríamos necesitar considerar los hijos del último visitado si este fuera interno
    # o su sucesor/predecesor en orden para ser más robusto.
    # El texto simplifica a "el último nodo visitado o su nodo padre".

    # Una forma más robusta es encontrar el predecesor y sucesor en orden del objetivo.
    # Si el nodo_final_busqueda.clave < clave_objetivo, su sucesor podría ser un candidato.
    # Si el nodo_final_busqueda.clave > clave_objetivo, su predecesor podría ser un candidato.
    
    # Simplificando según el texto:
    mejor_candidato = nodo_final_busqueda
    dist_min = abs(clave_objetivo - mejor_candidato.clave)

    if nodo_final_busqueda.padre:
        padre = nodo_final_busqueda.padre
        dist_padre = abs(clave_objetivo - padre.clave)
        if dist_padre < dist_min:
            mejor_candidato = padre
            dist_min = dist_padre
        # Considerar el otro hijo del padre si es relevante
        # (si el objetivo está entre el padre y el otro hijo)
        if clave_objetivo < padre.clave and padre.izquierda and padre.izquierda != nodo_final_busqueda:
            # Esto se vuelve complejo, el enfoque del texto es una simplificación.
            # El enfoque correcto involucra predecesor y sucesor en orden.
            pass
        elif clave_objetivo > padre.clave and padre.derecha and padre.derecha != nodo_final_busqueda:
            pass


    # Para una implementación más precisa de BST nearest neighbor:
    # 1. Realiza una búsqueda estándar.
    # 2. El nodo encontrado (si es exacto) es el vecino.
    # 3. Si no es exacto, el último nodo visitado (hoja o nodo interno donde terminó la búsqueda)
    #    y su ancestro desde el cual la búsqueda divergió son los principales candidatos.
    #    Más formalmente, son el predecesor y el sucesor en orden del valor objetivo.

    # Volviendo a la lógica del texto:
    # Si la búsqueda termina en 'nodo_final_busqueda':
    # Candidato 1: nodo_final_busqueda
    # Candidato 2: nodo_final_busqueda.padre (si existe)
    
    mejor_nodo = nodo_final_busqueda
    menor_distancia_abs = abs(clave_objetivo - nodo_final_busqueda.clave)

    # Considerar el padre
    padre_nodo = nodo_final_busqueda.padre
    if padre_nodo:
        dist_padre_abs = abs(clave_objetivo - padre_nodo.clave)
        if dist_padre_abs < menor_distancia_abs:
            menor_distancia_abs = dist_padre_abs
            mejor_nodo = padre_nodo
    
    return mejor_nodo


# Ejemplo de uso (asumiendo que `raiz_bst` fue construido previamente)
# objetivo_cliente_bst = 75
# nodo_cercano_bst = vecino_mas_cercano_bst_1d(raiz_bst, objetivo_cliente_bst)
# if nodo_cercano_bst:
# print(f"\nBúsqueda en BST para {objetivo_cliente_bst}:")
# print(f"Vecino más cercano: {nodo_cercano_bst.valor} en posición {nodo_cercano_bst.clave}")
# (El resultado dependerá de la estructura exacta del BST y la implementación precisa del vecino)
# Por ejemplo, si el BST es:
#       40
#      /  \
#    20    80
#   / \   / \
# 10  32 62  93
#
# Buscando 75:
# 1. Raíz (40). 75 > 40, ir a la derecha. Último visitado: 40. Padre: Ninguno.
# 2. Nodo (80). 75 < 80, ir a la izquierda. Último visitado: 80. Padre: 40.
# 3. Nodo (62). 75 > 62, ir a la derecha (supongamos que no hay hijo). Último visitado: 62. Padre: 80.
# Búsqueda termina en 62.
# Candidatos según texto simplificado:
# - Último nodo visitado: 62 (distancia a 75 es 13)
# - Padre del último visitado: 80 (distancia a 75 es 5)
# El más cercano es 80.
```

Entonces, ¿cuál es el algoritmo para encontrar el vecino más cercano de un punto 1-D, cuando el conjunto de datos está almacenado en un árbol binario de búsqueda? Podemos proponer:

1.  Ejecuta una búsqueda en el árbol binario.
2.  Si hay una coincidencia exacta, la entrada encontrada es el vecino más cercano (distancia 0).
3.  Si no hay coincidencia exacta, compara cuál de estas dos entradas está más cerca del objetivo: el último nodo visitado o su nodo padre.
   (Nota: una implementación más robusta consideraría el predecesor y sucesor en orden del valor objetivo).

Ahora que hemos resuelto brillantemente el problema en 1-D, surge la pregunta: ¿Podemos usar una estructura de datos similar para resolver el problema en 2-D?

#### Descripción y API 

Por supuesto, la respuesta es sí. Probablemente, el hecho de que hayamos planteado la pregunta ya te llevó a sospecharlo. Pero, aun así, pasar de 1-D a 2-D es un gran salto. No hay una forma sencilla de imaginar un árbol que funcione en dos dimensiones. 
Una vez que hayamos dado ese salto, será fácil pasar a 3-D y, en general, a hiperespacios con un número arbitrario de dimensiones.

Tampoco estaremos limitados a conjuntos de datos que se encuentren en el espacio geométrico 2-D o 3-D. Las dimensiones pueden ser cualquier cosa, siempre que podamos definir una medida de distancia sobre ellas, con la salvedad de que esta medida debe cumplir ciertos requisitos, concretamente, debe ser una distancia euclidiana. Por ejemplo, podemos tener entradas en 2-D donde la primera coordenada sea el precio y la segunda la calificación, y luego pedir la entrada más cercana a una tupla objetivo, como ($100, 4.5 estrellas). 

Más aún, también podremos pedir las N entradas más cercanas a esa tupla.

En este y en otras clases, vamos a describir tres estructuras de datos, tres contenedores, que permiten consultas eficientes de vecinos más cercanos.
Pero no solo eso: también proporcionarán algunas operaciones especiales:

* Obtener los N puntos más cercanos a un punto objetivo (que no necesariamente está en el contenedor).
* Obtener todos los puntos del contenedor dentro de una cierta distancia de un punto objetivo (interpretado geométricamente como todos los puntos dentro de una hiper-esfera).
* Obtener todos los puntos del contenedor dentro de un rango (todos los puntos que estén dentro de un hiper-rectángulo, o una semi-hiper-región).

Presentemos brevemente las tres estructuras que vamos a describir:

* **Árbol k-d:** Un árbol k-d es un árbol binario especial en el que cada nodo no hoja representa un hiperplano de división que divide el espacio k-dimensional en dos semi-espacios. Los puntos en un lado del hiperplano se almacenan en el subárbol izquierdo y los del otro lado, en el subárbol derecho.
* **Árbol R (R-tree):** La "R" viene de rectángulo. Un árbol R agrupa puntos cercanos y define el mínimo recuadro contenedor (hiper-rectángulo) que los abarca. Los puntos se particionan jerárquicamente en cajas mínimas contenedoras, una por cada nodo intermedio, con la raíz abarcando todos los puntos.
* **Árbol SS (Similarity Search Tree):** Similar a los árboles R, pero en lugar de usar hiper-rectángulos, los árboles SS usan hiper-esferas como regiones de agrupación. Las hojas contienen puntos, mientras que las esferas internas agrupan otras hiper-esferas.

Finalmente, definamos una interfaz genérica, común a todas las implementaciones concretas:

**Estructura de datos abstracta: NearestNeighborContainer**
**API**
```python
class NearestNeighborContainer:
    def size(self):
        # Devuelve el número de puntos en el contenedor
        raise NotImplementedError

    def isEmpty(self):
        # Devuelve True si el contenedor está vacío, False en caso contrario
        raise NotImplementedError

    def insert(self, point):
        # Inserta un punto en el contenedor
        raise NotImplementedError

    def remove(self, point):
        # Elimina un punto del contenedor
        raise NotImplementedError

    def search(self, point):
        # Verifica si un punto está en el contenedor
        raise NotImplementedError

    def nearestNeighbor(self, point, n=1):
        # Devuelve el punto más cercano (o los N puntos más cercanos)
        raise NotImplementedError

    def pointsInRegion(self, targetRegion):
        # Devuelve todos los puntos en una región determinada (hiper-esfera o hiper-rectángulo)
        raise NotImplementedError
```

**Contrato con el cliente**
El contenedor permite insertar y eliminar puntos, y realizar las siguientes consultas:
* **Existencia:** Verificar si un punto está en el contenedor.
* **Vecino más cercano:** Retornar el punto más cercano (o los N puntos más cercanos, para cualquier N) a un punto objetivo. El punto objetivo no necesita estar en el contenedor.
* **Rango:** Retornar todos los puntos en una región determinada, ya sea una hiper-esfera o un hiper-rectángulo.

#### Hacia espacios k-dimensionales 

Hemos mostrado que es posible resolver eficientemente el problema del vecino más cercano en 1-D usando un árbol binario de búsqueda. 
Sin embargo, al pasar de 1-D a 2-D, la situación se complica un poco, ya que en cada nodo no tenemos una bifurcación clara entre dos caminos, es decir, hijos izquierdo y derecho.

**Búsqueda binaria unidimensional**
Para resumir: es fácil realizar búsqueda binaria cuando las entradas están en un espacio unidimensional (ℝ). Cada punto en esa línea define implícitamente una izquierda y una derecha, lo cual se mapea naturalmente a los caminos izquierdo y derecho de un nodoen un BST.

**Pasando a dimensiones superiores**
Ahora, ¿qué pasa con ℝ² (puntos en un plano euclidiano bidimensional) o ℂ (números complejos)? La búsqueda binaria ya no es tan clara. 
Si consideras un punto P en el plano cartesiano, ¿cómo dividimos el plano en dos regiones, "izquierda" y "derecha" de P?

Una forma visualmente intuitiva podría ser dividir el plano con una línea vertical que pase por P.
```python
# Concepto de división vertical
# P = (px, py)
# Punto_Q = (qx, qy)
# if qx < px:
# # Q está a la "izquierda" de la línea vertical que pasa por P
# elif qx > px:
# # Q está a la "derecha"
# else:
# # Q está sobre la línea vertical
```
Esta solución puede parecer adecuada usando P como pivote, pero si tomamos otros puntos, surgen problemas. Si trazamos una línea vertical (paralela al eje Y) y usamos la coordenada X para dividir, puntos que están cerca en el espacio 2D pueden terminar 
en particiones diferentes si su coordenada Y es muy distinta. Ignoramos por completo la coordenada Y, perdiendo información valiosa.

**Modelar particiones 2D con estructuras de datos**
Usar siempre la misma dirección para todos los puntos no funciona bien, así que tal vez dividir el plano en cuatro cuadrantes sea mejor idea. 
Esto nos lleva a la idea de un árbol donde cada nodo tenga cuatro hijos (un **quadtree** conceptualmente).

```python
def obtener_cuadrante(punto_referencia, punto_a_clasificar):
    """
    Determina en qué cuadrante cae punto_a_clasificar con respecto a punto_referencia.
    Asume que punto_referencia es el origen del sistema de cuadrantes.
    """
    pr_x, pr_y = punto_referencia
    pac_x, pac_y = punto_a_clasificar

    if pac_x >= pr_x and pac_y >= pr_y:
        return "superior derecho (NE)"
    elif pac_x < pr_x and pac_y >= pr_y:
        return "superior izquierdo (NW)"
    elif pac_x < pr_x and pac_y < pr_y:
        return "inferior izquierdo (SW)"
    elif pac_x >= pr_x and pac_y < pr_y:
        return "inferior derecho (SE)"
    # Casos sobre los ejes se asignan a un cuadrante por convención.

# R = (50, 50) # Punto de referencia inicial
# P = (30, 70)
# U = (20, 60)

# print(f"P ({P}) con respecto a R ({R}): {obtener_cuadrante(R, P)}")
# # P está en el cuadrante superior izquierdo de R.
# # Ahora si P se vuelve el nuevo punto de referencia para U:
# print(f"U ({U}) con respecto a P ({P}): {obtener_cuadrante(P, U)}")
# # U está en el cuadrante inferior izquierdo de P.
```
Esto parece funcionar para ℝ², considerando ambas coordenadas. 

Ahora bien, ¿podemos extender esto a ℝ³? Para pasar a 3-D, necesitaríamos 8 octantes, y por tanto, 8 hijos por nodo.

En general, en un espacio k-dimensional, necesitaríamos $2^k$ hijos por nodo en el árbol. En conjuntos de datos reales, con el auge del big data, es común
que $k$ (el número de dimensiones o características) esté entre 10 y 30, o incluso 100.

* Si $k=10$, $2^{10} \approx 1000$ hijos.
* Si $k=100$, $2^{100} \approx 10^{30}$ hijos, un número imposible de manejar.

Necesitamos algo mucho mejor. Como veremos, los científicos computacionales han encontrado varias formas de abordar estos problemas. 

