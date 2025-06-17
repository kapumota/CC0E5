## **Práctica calificada 5 CC0E5**

Fecha de entrega:4 de julio.

### **Propuesta de proyecto 1: Simulación de enjambre de drones para búsqueda y rescate autónomo**

- **Área principal:** Robótica y sistemas autónomos (Swarm Robotics).
- **Áreas secundarias:** Simulación y optimización, geometría computacional, estructuras espaciales (Quadtrees).

#### **Descripción detallada**
Este proyecto consiste en desarrollar una simulación 2D o 3D de un enjambre de drones autónomos cuya misión es explorar un área designada después de un desastre para localizar objetivos (e.g., personas desaparecidas). El sistema se basará en el algoritmo **Boids** para el comportamiento de enjambre (cohesión, alineación, separación) y lo extenderá con una capa de **optimización de búsqueda** y **evasión de obstáculos**. Se utilizará una estructura de datos espacial como un **Quadtree** para gestionar de manera eficiente el entorno y las interacciones entre drones.

El objetivo es demostrar cómo un comportamiento emergente, descentralizado y cooperativo puede realizar una tarea compleja de manera más eficiente que un solo agente. La simulación debe ser visualmente atractiva para la presentación y el video, mostrando claramente el área de búsqueda, los drones, los obstáculos y los objetivos encontrados.

#### **Tecnologías clave**
* **Lenguaje:** Python.
* **Librerías principales:**
    * `Pygame` o `Godot (con GDScript/Python)` para la simulación y visualización 2D/3D.
    * `NumPy` para cálculos vectoriales eficientes.
    * `SciPy` para optimizaciones y métricas (opcional).
    * `Matplotlib` para generar gráficos de rendimiento (e.g., área cubierta vs. tiempo).

#### **Entregables clave**
* **Código fuente completo:** Organizado, comentado y versionado con Git. Debe superar las 800 líneas de código real (excluyendo comentarios y espacios en blanco).
* **Simulador funcional:** Un ejecutable o script que permita iniciar la simulación, configurar parámetros básicos (número de drones, tamaño del mapa) y observar el comportamiento del enjambre.
* **Documentación técnica:** Un `README.md` detallado que explique la arquitectura del sistema, el rol de cada componente (Boids, Quadtree, módulo de búsqueda) y las instrucciones para ejecutar el proyecto.

#### **Video de demostración:**
* **Enfoque:** Mostrar la eficiencia y la inteligencia emergente del enjambre.
* **Pasos a mostrar:**
    -  Presentar el escenario: un mapa con obstáculos y objetivos ocultos.
    -  Ejecutar la simulación con un solo dron, mostrando su lenta capacidad de búsqueda.
    -  Ejecutar la simulación con el enjambre de drones, destacando visualmente las reglas de Boids (cohesión, alineación, separación).
    -  Mostrar cómo el enjambre se dispersa para cubrir el área eficientemente y cómo los drones comunican (implícitamente) las áreas ya exploradas.
    -  Mostrar el momento en que varios drones convergen en un objetivo encontrado.
    -  resentar un gráfico final que compare el tiempo de búsqueda (o área cubierta por unidad de tiempo) del dron único vs. el enjambre, demostrando la ventaja del sistema multi-agente.

### **Propuesta de proyecto 2: Cryptoparty: Rompiendo cifrados simétricos con el algoritmo de Grover**

- **Área principal:** Computación cuántica y ciberseguridad.
- **Áreas secundarias:** Algoritmia, criptografía, simulación de sistemas físicos.

#### **Descripción detallada**
Este proyecto implementa un ataque teórico de "fuerza bruta cuántica" contra un cifrado simétrico simple (como una versión reducida de AES o un cifrado de juguete) utilizando el **Algoritmo de Grover**. 
A diferencia de un ataque clásico que prueba una clave a la vez, el algoritmo de Grover puede encontrar la clave correcta en aproximadamente $\sqrt{N}$ intentos, ofreciendo una ventaja cuadrática.

El equipo desarrollará dos componentes principales:
-  Un **script clásico en Python** que cifra un mensaje usando un cifrado simétrico simple con una clave secreta.
-  Un **circuito cuántico en Qiskit** que implementa el algoritmo de Grover para encontrar esa clave secreta. El corazón del proyecto es el diseño del **"oráculo" cuántico**, que es el componente del circuito que "marca" el estado cuántico correspondiente a la clave correcta.

Finalmente, se ejecutarán simulaciones para verificar la ventaja cuántica y se generará un gráfico comparativo de las complejidades $O(N)$ vs. $O(\sqrt{N})$.

#### **Tecnologías clave**
* **Lenguaje:** Python.
* **Librerías Principales:**
    * `Qiskit`: El framework de computación cuántica de IBM para construir, simular y (potencialmente) ejecutar circuitos cuánticos.
    * `NumPy`: Para manejo de datos y vectores.
    * `Cryptography` o similar: Para la implementación del cifrado clásico de referencia.
    * `Matplotlib`: Para visualizar los resultados (histogramas de probabilidad y curvas de complejidad).

#### **Entregables clave**
* **Código fuente completo:** Dos scripts principales (clásico y cuántico) y módulos auxiliares. Versionado con Git y superando las 800 líneas.
* **Scripts ejecutables:** Un script para cifrar y otro para ejecutar la búsqueda cuántica.
* **Documentación técnica:** Un `README.md` que explique los fundamentos del algoritmo de Grover, la estructura del circuito cuántico y, fundamentalmente, el diseño del oráculo. Se debe incluir una explicación conceptual del rol de cada compuerta.

#### **Video de demostración:**
* **Enfoque:** Debe ser una demostración clara y contundente.
* **Pasos a mostrar:**
    -  Ejecutar el script clásico para cifrar un mensaje: "Aquí está nuestro texto cifrado, la clave es secreta".
    -  Mostrar el código Qiskit que construye el circuito de Grover.
    -  Ejecutar la simulación cuántica.
    -  Mostrar el histograma de resultados del simulador: una barra alta y clara sobre el estado que representa la clave correcta.
    -  Mostrar el gráfico final que compara la curva $O(N)$ con la curva $O(\sqrt{N})$.


### **Propuesta de proyecto 3: Sistema de detección de colisiones 3D con árboles BVH**

- **Área principal:** Detección de colisiones complejas usando árboles BVH.
- **Áreas secundarias:** Geometría computacional, estructuras espaciales, simulación y optimización.

#### **Descripción detallada**
Este proyecto se centra en construir desde cero un sistema robusto y eficiente para detectar colisiones entre mallas 3D complejas.  La fuerza bruta (comparar cada triángulo de un objeto con cada triángulo del otro) es computacionalmente prohibitiva. 
La solución es implementar **árboles de volúmenes envolventes (bounding volume trees-BVH)**.

El sistema hará lo siguiente:
1.  **Pre-procesamiento:** Para una malla 3D dada, construirá un BVH. Esto implica agrupar jerárquicamente los triángulos de la malla dentro de volúmenes envolventes simples como **AABB (Axis-Aligned Bounding Boxes)**.
2.  **Fase amplia (broad phase):** Utilizará los AABB raíz de los BVH para descartar rápidamente pares de objetos que están demasiado lejos para colisionar.
3.  **Fase estrecha (narrow phase):** Para los objetos que podrían colisionar, el sistema recorrerá simultáneamente sus BVH para encontrar pares de triángulos que se solapen y confirmar la colisión exacta.

#### **Objetivos clave**
1.  **Primitivas geométricas:** Implementar las estructuras de datos y funciones matemáticas para vectores, rayos, AABB y triángulos, incluyendo pruebas de intersección.
2.  **Construcción de BVH:** Implementar el algoritmo para construir un BVH a partir de una lista de triángulos.
3.  **Recorrido del árbol (query):** Implementar la función de consulta que recorre dos BVH simultáneamente.
4.  **Visualización y pruebas:** Crear una escena 3D simple que permita cargar modelos, moverlos y visualizar colisiones en tiempo real.

#### **Tecnologías y librerías sugeridas**
* **Lenguaje:** C++.
* **Gráficos:** `OpenGL` con `GLFW` y `GLM`.
* **Carga de modelos:** `Assimp`.
* **Paralelismo (opcional avanzado):** `OpenMP`.

#### **Entregables y cómo enfocar la evaluación**
* **Presentación:** Explicar el problema de la detección de colisiones en $O(N*M)$ y cómo los BVH lo resuelven.
* **Video:** Mostrar la aplicación cargando dos modelos complejos (e.g., conejos de Stanford). Mover uno hasta que colisione, mostrando la eficiencia (FPS) y visualizando el árbol BVH.

### **Propuesta de proyecto 4: Creador de un renderizador 3D por software desde cero**

- **Área principal:** Renderizado 3D (Z-buffer, scanline).
- **Áreas secundarias:** Geometría computacional.

#### **Descripción detallada**
Este es un proyecto fundamental que consiste en construir un motor de renderizado 3D completo **sin usar ninguna API gráfica de hardware como OpenGL o DirectX**. Todo el pipeline (transformación, rasterización, Z-buffer, iluminación) se implementará en software (CPU) para entender desde los cimientos cómo una GPU transforma un modelo 3D en una imagen 2D.

#### **Objetivos clave**
1.  **Framework base:** Crear una ventana que pueda mostrar un buffer de píxeles.
2.  **Matemáticas 3D:** Implementar una librería de matrices y vectores.
3.  **Carga y transformación:** Cargar un modelo `.obj` y aplicar las matrices de transformación.
4.  **Rasterizador y Z-buffer:** Implementar la rasterización de triángulos y el test de profundidad.
5.  **Iluminación y shading:** Añadir sombreado de Gouraud o Phong.

#### **Tecnologías y librerías sugeridas**
* **Lenguaje:** C++ (por su rendimiento) o Python con NumPy.
* **Librerías:** Una librería simple para crear una ventana y dibujar píxeles como `SFML` (C++), `SDL2` (C++) o `Pygame` (Python). **No usar sus funciones de dibujo 3D.**

#### **Entregables y cómo enfocar la evaluación**
* **Presentación:** Explicar cada paso del pipeline de renderizado gráfico.
* **Video:** Mostrar el renderizador en acción. Cargar diferentes modelos. Activar y desactivar el Z-buffer y la iluminación para mostrar su efecto.

### **Propuesta de proyecto 5: IA para un juego de estrategia con árboles de comportamiento (behaviour trees)**

- **Área principal:** Behaviour trees.
- **Áreas secundarias:** Simulación y optimización.

#### **Descripción detallada**
Este proyecto se enfoca en diseñar la IA para las unidades de un mini-juego de estrategia usando **árboles de comportamiento (behaviour trees -BT)**. 
Se creará una simulación 2D con Recolectores (buscar recursos, huir de enemigos) y Soldados (patrullar, atacar, retirarse). 
El núcleo es la implementación del motor de BT (nodos de Secuencia, Selector, etc.) y el diseño de los árboles para cada unidad. 

#### **Objetivos clave**
1.  **Motor de simulación básico:** Crear un entorno 2D donde las unidades puedan moverse.
2.  **Framework de behaviour tree:** Implementar las clases base para el árbol (`Node`, `SequenceNode`, `SelectorNode`, etc.).
3.  **Tareas básicas:** Crear nodos de acción concretos: `MoveTo`, `FindResource`, `AttackEnemy`, `Flee`.
4.  **Diseño de árboles:** Construir los BT para el recolector y el soldado.
5.  **Visualización:** Mostrar el estado actual del BT de una unidad seleccionada en tiempo real.

#### **Tecnologías y librerías sugeridas**
* **Lenguaje:** C# con Unity o Godot, C++ con SFML, o Python con Pygame.
* **Conceptos:** Patrones de diseño de software para la implementación del BT.

#### **Entregables y cómo enfocar la evaluación**
* **Presentación:** Explicar qué son los árboles de comportamiento y por qué son superiores a las máquinas de estados finitos (FSM).
* **Video** Mostrar la simulación en acción. Seleccionar una unidad y mostrar su árbol de comportamiento actualizándose en vivo mientras toma decisiones.

### **Propuesta de proyecto 6: Predicción de movimiento en VR con filtros de Kalman**

- **Área principal:** Predicción de movimiento y seguimiento en entornos VR (Kalman / SLAM).
- **Áreas secundarias:** Simulación y Optimización.

#### **Descripción detallada**
Este proyecto busca mitigar la latencia en VR implementando un **filtro de Kalman** para predecir la posición y orientación futuras de los controladores. 
El sistema procesará datos de movimiento simulados y ruidosos para estimar el estado real del controlador y predecir su estado futuro, resultando en un movimiento más suave y 
con menor latencia percibida.

#### **Objetivos clave**
1.  **Entorno de simulación 3D:** Crear una escena para visualizar un objeto (el controlador).
2.  **Generador de datos ruidosos:** Crear un sistema que genere trayectorias y les añada ruido.
3.  **Implementación del filtro de Kalman:** Implementar el algoritmo de predicción y actualización.
4.  **Integración y visualización:** Procesar los datos ruidosos y mostrar en paralelo la trayectoria real, la ruidosa y la estimada/predicha por el filtro.
5.  **Extensión a rotación (opcional):** Adaptar el filtro para que también estime la orientación (filtro de Kalman extendido).

#### **Tecnologías y librerías sugeridas**
* **Lenguaje:** C# con Unity o C++ con una librería gráfica.
* **Librerías:** `Eigen` (C++) o `Math.NET Numerics` (C#) para operaciones matriciales.

#### **Entregables y cómo enfocar la evaluación**
* **Presentación:** Explicar de forma intuitiva qué es un Filtro de Kalman y su ciclo de predicción-actualización.
* **Video:** Mostrar las tres trayectorias (real, ruidosa, filtrada) lado a lado para que el efecto de suavizado y predicción sea evidente.

### **Propuesta de proyecto 7: Ray Tracer Offline con aceleración por KD-Tree**

- **Área principal:** Ray Tracing acelerado con estructuras KD-Tree.
- **Áreas secundarias:** Geometría Computacional, Renderizado 3D.

#### **Descripción detallada**
Este proyecto consiste en escribir un **Ray Tracer** desde cero para generar imágenes fotorrealistas. Para que sea factible renderizar escenas complejas, se implementará 
un **KD-Tree** para particionar espacialmente la escena, reduciendo drásticamente el número de pruebas de intersección rayo-objeto de $O(N)$ a $O(\log N)$. 
El ray tracer soportará primitivas básicas, sombras, reflexiones y múltiples luces.

#### **Objetivos clave**
1.  **Motor de Ray Tracing básico:** Implementar el lanzamiento de rayos y la intersección con esferas.
2.  **Modelo de iluminación:** Aplicar el modelo de Phong, incluyendo sombras.
3.  **Construcción de KD-Tree:** Implementar el algoritmo de construcción, preferiblemente con la heurística SAH (Surface Area Heuristic).
4.  **Recorrido del KD-Tree:** Implementar el algoritmo de recorrido del árbol para acelerar la búsqueda de intersecciones.
5.  **Ray Tracing recursivo:** Añadir recursividad para simular reflexiones.

#### **Tecnologías y librerías sugeridas**
* **Lenguaje:** C++.
* **Librerías:** `stb_image_write` para guardar imágenes, `Assimp` para cargar mallas, `OpenMP` para paralelización.

#### **Entregables y cómo enfocar la evaluación**
* **Presentación:** Explicar el algoritmo de Ray Tracing, por qué se necesita una estructura de aceleración y cómo funciona un KD-Tree con SAH.
* **Video:** Mostrar las imágenes renderizadas, desde escenas simples a complejas. Presentar una tabla comparando tiempos de renderizado con y sin el KD-Tree.

### **Propuesta de proyecto 8: Netcode de Rollback (GGPO) para un juego de lucha P2P**

- **Área principal:** Algoritmos de sincronización en red (Rollback).
- **Áreas secundarias:** Simulación y optimización.

#### **Descripción detallada**
Este proyecto aborda la latencia en juegos en línea implementando un juego de lucha 2D P2P con **netcode de rollback**. En lugar de esperar la entrada del oponente, el juego 
predice su acción, simula el frame y, si la predicción fue incorrecta, retrocede en el tiempo (rollback) y re-simula con la entrada correcta. 
Esto crea una experiencia de juego casi sin lag. 

#### **Objetivos clave**
1.  **Juego base (offline):** Crear un juego de lucha 2D simple y determinista.
2.  **Gestión de estado:** Implementar un sistema para guardar y cargar rápidamente el estado del juego.
3.  **Capa de red P2P:** Establecer una conexión P2P básica usando UDP.
4.  **Motor de rollback:** Implementar la lógica de predicción, rollback y re-simulación.
5.  **Visualización de depuración:** Mostrar en pantalla el ping, el estado y el número de rollbacks.

#### **Tecnologías y librerías sugeridas**
* **Lenguaje:** C++ con `SFML`/`SDL2`, Rust, o C# con `Monogame`.
* **Red:** Sockets UDP nativos o una librería como `enet`.
* **Determinismo:** Usar números de punto fijo o tener cuidado con los de punto flotante.

#### **Entregables y cómo enfocar la evaluación**
* **Presentación:** Explicar el problema del lag, comparar netcode de retraso vs. rollback y diagramar el flujo de predicción-corrección.
* **Video :** Mostrar dos instancias del juego corriendo lado a lado con latencia simulada para demostrar la fluidez.

### **Propuesta de proyecto 9: Motor de renderizado basado en vóxeles con generación procedural**

- **Área principal:** Renderizado 3D (Voxel-Grid).
- **Áreas secundarias:** Generación procedural (Perlin Noise), estructuras espaciales.

#### **Descripción detallada**
Inspirado en juegos como Minecraft, este proyecto consiste en desarrollar un motor 3D donde el mundo está hecho de **vóxeles**. 
Los desafíos son dos: la **generación procedural** del mundo en "chunks" usando ruido Perlin y el **renderizado eficiente** mediante "Greedy Meshing", un algoritmo que crea
una malla de polígonos optimizada solo para las superficies visibles. 

#### **Objetivos clave**
1.  **Estructura de datos de vóxeles:** Implementar el almacenamiento del mundo en chunks.
2.  **Generación procedural:** Usar ruido Perlin 3D para generar el terreno.
3.  **Algoritmo de "meshing":** Implementar Greedy Meshing para convertir vóxeles en una malla optimizada.
4.  **Motor de renderizado:** Renderizar las mallas y gestionar la carga/descarga de chunks.
5.  **Interacción:** Permitir al jugador añadir o eliminar vóxeles.

#### **Tecnologías y librerías sugeridas**
* **Lenguaje:** C++ con OpenGL, C# con Unity/Godot.
* **Librerías:** `OpenGL` / `GLFW` / `GLM` en C++. `FastNoiseLite` para el ruido.

#### **Entregables y cómo enfocar la evaluación**
* **Presentación :** Explicar qué son los vóxeles y cómo el Greedy Meshing soluciona el problema de rendimiento del renderizado ingenuo.
* **Video:** Mostrar una exploración fluida del mundo, la carga dinámica de chunks y la modificación del terreno en tiempo real.

### **Propuesta de proyecto 10: Sistema distribuido de búsqueda de similitud vectorial**

- **Área principal:** Distributed Similarity Search Systems usando M-tree y Hashing consistente.
- **Áreas secundarias:** Simulación y optimización.

#### **Descripción detallada**
Este proyecto consiste en construir un prototipo de un **sistema distribuido** para realizar búsquedas de similitud en un gran conjunto de vectores de alta dimensión (e.g., embeddings de IA). 
Se usará un **M-Tree** en cada nodo para una búsqueda local eficiente y **Hashing Consistente** para distribuir los datos de forma escalable entre los nodos. 

#### **Objetivos clave**
1.  **Implementación del M-Tree:** Implementar la estructura M-Tree desde cero (inserción y búsqueda k-NN/rango).
2.  **Implementación de consistent Hashing:** Implementar el anillo de hashing para mapear vectores a nodos.
3.  **Nodo de servicio:** Crear un servicio que contenga un M-Tree y responda a peticiones.
4.  **Orquestador/Gateway:** Crear un punto de entrada que distribuya las peticiones a los nodos y agregue los resultados.
5.  **Simulación distribuida:** Simular el sistema con varios nodos ejecutándose como procesos separados.

#### **Tecnologías y librerías sugeridas**
* **Lenguaje:** Python (con `Flask` o `FastAPI`) o Go/Java.
* **Librerías:** `NumPy` para cálculos vectoriales.

#### **Entregables y cómo enfocar la evaluación**
* **Presentación:** Explicar el problema de la búsqueda de similitud a gran escala y el rol del M-Tree y el Hashing consistente.
* **Video:** Mostrar la arquitectura en acción: iniciar varios nodos, insertar vectores, mostrar cómo se distribuyen y ejecutar una búsqueda.

### **Propuesta de proyecto 11: Detección de anomalías en flujos de datos con Apache Flink**

- **Área principal:** Streaming y redes en tiempo real.
- **Áreas secundarias:** Procesamiento de datos masivos, simulación y optimización.

#### **Descripción detallada**
Este proyecto consiste en construir un sistema de detección de anomalías en tiempo real para flujos de datos de alta frecuencia, como transacciones financieras o métricas de sensores IoT. Se utilizará **Apache Flink**, un motor de procesamiento de flujos de última generación, para implementar la lógica. El sistema procesará eventos de un stream, los agrupará en **ventanas de tiempo deslizantes** (e.g., "el número de transacciones en los últimos 5 segundos") y aplicará reglas para detectar comportamientos inusuales, como picos repentinos en la actividad o valores fuera de rango.

#### **Objetivos clave**
1.  **Entorno de streaming:** Configurar un entorno de desarrollo con Apache Flink y un generador de flujos de datos (e.g., Apache Kafka o un simulador simple).
2.  **Definición de eventos:** Modelar la estructura de los datos de entrada (e.g., `TransactionEvent` con ID de usuario, monto y timestamp).
3.  **Lógica de ventanas:** Implementar operaciones de ventana en Flink para agregar datos en tiempo real (e.g., contar eventos por usuario por minuto).
4.  **Detección de anomalías:** Escribir funciones que analicen los resultados agregados y emitan alertas cuando se superen ciertos umbrales.
5.  **Visualización:** Crear un panel simple (dashboard) o una salida de consola que muestre el flujo de datos y las alertas de anomalías a medida que se generan.

#### **Tecnologías y librerías sugeridas**
* **Lenguaje:** Java o Scala.
* **Motor de streaming:** `Apache Flink`.
* **Fuente de datos:** `Apache Kafka` (recomendado) o un generador de datos personalizado.
* **Contenerización:** `Docker` para simplificar la configuración del entorno.

#### **Entregables y cómo enfocar la evaluación**
* **Presentación:** Explicar los conceptos clave del procesamiento de flujos: ventanas, estado y tiempo de evento vs. tiempo de procesamiento.
* **Video:** Mostrar el sistema en acción. Iniciar el generador de datos y ver en el panel cómo Flink procesa los eventos y dispara alertas cuando se simula una actividad anómala (e.g., un ataque de fraude).

### **Propuesta de proyecto 12: Servidor de streaming de video adaptativo (HLS/DASH)**

- **Área principal:** Streaming y redes en tiempo real.
- **Áreas secundarias:** Procesamiento multimedia, redes de computadoras.

#### **Descripción detallada**
Este proyecto busca construir un servidor de video bajo demanda que implemente **streaming de tasa de bits adaptativa (adaptive bitrate streaming)**. El sistema tomará un archivo de video de alta calidad y, usando **FFmpeg**, lo transcodificará automáticamente en múltiples versiones con diferentes resoluciones y calidades. Luego, generará los archivos de manifiesto para los protocolos **HLS (HTTP Live Streaming)** de Apple o **DASH (Dynamic Adaptive Streaming over HTTP)** de MPEG. Finalmente, un reproductor de video web simple solicitará los segmentos de video y cambiará de calidad de forma inteligente según el ancho de banda disponible simulado.

#### **Objetivos clave**
1.  **Script de transcodificación:** Crear un script que automatice el uso de FFmpeg para generar las diferentes variantes de calidad del video y lo segmente.
2.  **Generación de manifiestos:** Asegurarse de que el script también genere los archivos de manifiesto (`.m3u8` para HLS o `.mpd` para DASH) que describen las variantes disponibles.
3.  **Servidor de contenidos:** Configurar un servidor web simple (e.g., Nginx, Apache) para alojar los segmentos de video y los manifiestos.
4.  **Reproductor adaptativo:** Construir una página web con un reproductor de video (usando librerías como `video.js` o `Shaka Player`) que sea capaz de leer el manifiesto y cambiar de calidad automáticamente.
5.  **Monitoreo (opcional):** Añadir lógica al reproductor para monitorizar métricas de Calidad de Experiencia (QoE), como el número de cambios de calidad o el tiempo de buffering.

#### **Tecnologías y librerías sugeridas**
* **Lenguaje:** Python o Bash para el scripting.
* **Procesamiento de video:** `FFmpeg`.
* **Servidor web:** `Nginx` o `Node.js` con Express.
* **Frontend:** HTML5, JavaScript, `video.js` o `Shaka Player`.

#### **Entregables y cómo enfocar la evaluación**
* **Presentación:** Explicar qué es el streaming adaptativo y por qué es el estándar de la industria (Netflix, YouTube). Describir la estructura de un manifiesto HLS/DASH.
* **Video:** Mostrar el flujo completo. Ejecutar el script de transcodificación sobre un video. Luego, abrir el reproductor web y, usando las herramientas de desarrollador del navegador para limitar el ancho de banda, mostrar cómo el video cambia de alta a baja calidad sin interrumpirse.

### **Propuesta de proyecto 13: Realidad aumentada con oclusión y colisiones realistas**

- **Área principal:** Realidad aumentada y realidad virtual.
- **Áreas secundarias:** Geometría computacional, renderizado 3D.

#### **Descripción detallada**
El objetivo es crear una aplicación de realidad aumentada (AR) que supere la sensación de "calcomanía flotante" de los objetos virtuales. Utilizando las capacidades avanzadas de los dispositivos móviles modernos (como los sensores de profundidad LiDAR o la estimación de profundidad por IA), la aplicación **generará una malla 3D del entorno real en tiempo real**. Esta malla se usará para dos propósitos:
1.  **Oclusión:** Permitir que los objetos virtuales se oculten de forma realista detrás de objetos reales (e.g., un personaje virtual que camina detrás de un sofá).
2.  **Colisiones:** Hacer que los objetos virtuales interactúen físicamente con el mundo real (e.g., una pelota virtual que rebota en el suelo y en las paredes reales).

#### **Objetivos clave **
1.  **Configuración del proyecto AR:** Establecer un proyecto en Unity o Unreal Engine con los plugins ARKit (iOS) o ARCore (Android).
2.  **Detección del entorno:** Habilitar la detección de planos y la generación de mallas del entorno (environment meshing).
3.  **Shader de oclusión:** Configurar los materiales de los objetos virtuales para que sean ocluidos por la malla del entorno.
4.  **Físicas AR:** Añadir componentes de física (e.g., `Rigidbody`, `Collider`) tanto a los objetos virtuales como a la malla del entorno para permitir colisiones realistas.
5.  **Interacción del usuario:** Permitir que el usuario coloque objetos en la escena y los lance para probar las colisiones y la oclusión.

#### **Tecnologías y librerías sugeridas**
* **Motor:** `Unity` o `Unreal Engine`.
* **Frameworks AR:** `ARKit` (Apple), `ARCore` (Google).
* **Lenguaje:** C# (Unity) o C++ (Unreal).

#### **Entregables y cómo enfocar la evaluación**
* **Presentación:** Explicar cómo funcionan la detección de profundidad y la generación de mallas en AR. Mostrar por qué la oclusión y las colisiones son cruciales para la inmersión.
* **Video:** La demostración es clave. Grabar la aplicación en un entorno con muebles. Colocar un personaje virtual y hacer que camine detrás de una silla. Lanzar una pelota virtual y mostrar cómo rebota de forma convincente en el suelo, una mesa y una pared.


### **Propuesta de proyecto 14: Búsqueda semántica distribuida con índices HNSW**

- **Área principal:** Búsqueda y recuperación de información.
- **Áreas secundarias:** Inteligencia artificial, arquitectura de microservicios.

#### **Descripción detallada**
Este proyecto busca construir un sistema de **búsqueda semántica** capaz de encontrar imágenes o textos similares basados en su significado, no solo en palabras clave. El sistema convertirá los datos (e.g., imágenes) en vectores de alta dimensión (embeddings) usando un modelo de IA pre-entrenado. La clave del proyecto es indexar estos vectores usando **HNSW (Hierarchical Navigable Small World)**, un algoritmo de última generación para la búsqueda de vecinos más cercanos aproximada (ANN) que es extremadamente rápido y eficiente. El sistema se implementará como un microservicio distribuido.

#### **Objetivos clave**
1.  **Vectorización de datos:** Integrar un modelo de IA pre-entrenado (e.g., CLIP para imágenes, S-BERT para texto) para convertir datos en bruto en embeddings vectoriales.
2.  **Índice HNSW:** Implementar o integrar una librería de HNSW (como `faiss` o `hnswlib`) para crear un índice con los vectores generados.
3.  **Microservicio de búsqueda:** Envolver el índice en un microservicio con una API REST simple. La API deberá tener al menos dos puntos finales: uno para añadir nuevos elementos al índice y otro para realizar una búsqueda.
4.  **Interfaz de usuario:** Crear una interfaz web muy simple que permita al usuario subir una imagen o escribir un texto de consulta y que muestre los resultados más similares devueltos por el servicio.
5.  **Distribución (opcional):** Diseñar cómo se podría distribuir el índice en varios nodos para escalar a miles de millones de vectores.

#### **Tecnologías y librerías sugeridas**
* **Lenguaje:** Python.
* **Frameworks de servicio:** `FastAPI` o `Flask`.
* **Librerías de IA:** `transformers`, `torch`, `Pillow`.
* **Índice ANN:** `hnswlib`, `faiss` (de Facebook AI), o una base de datos vectorial como `Weaviate` o `Milvus`.
* **Contenerización:** `Docker`.

#### **Entregables y cómo enfocar la evaluación**
* **Presentación:** Explicar qué es la búsqueda semántica y los embeddings. Describir por qué la búsqueda exacta es inviable en alta dimensión (la "maldición de la dimensionalidad") y cómo algoritmos como HNSW resuelven este problema.
* **Video:** Demostrar la potencia del sistema. Usar una consulta de imagen, como una foto de "un perro en la playa", y mostrar que el sistema devuelve otras imágenes de perros en playas, aunque la composición y los colores sean diferentes. Hacer lo mismo con texto.
