### Problema de la mochila, NP-completitud y fuerza bruta, greedy, transformación del problema

Imagina que tienes la siguiente lectura: 

#### Empacando tu mochila

Has sido seleccionado para poblar la primera colonia en Marte. Las tiendas de comestibles marcianas aún presentan escasez de productos y encontrarlos es complicado, por lo que eventualmente tendrás que cultivar tus propios alimentos. Mientras tanto, durante los primeros meses, te enviarán productos para sostenerte.

#### Abstrayendo el problema

El problema es que tus cajas no pueden pesar más de 1000 kilogramos, y ese es un límite estricto. Además, solo puedes elegir de un conjunto limitado de productos, ya empacados en cajas, de la siguiente manera:

- **Papas:** 800 kg  
- **Arroz:** 300 kg  
- **Harina de trigo:** 400 kg  
- **Mantequilla de maní:** 20 kg  
- **Latas de tomate:** 300 kg  
- **Frijoles:** 300 kg  
- **Mermelada de fresa:** 50 kg  

Obtendrás agua gratis, así que no te preocupes por ello, pero solo puedes tomar una caja completa o dejarla. Claro que te gustaría tener variedad y no acabar con una tonelada de papas (al estilo de *The Martian*).

La principal preocupación de la expedición es mantenerte bien alimentado y lleno de energía, por lo que el factor clave para elegir qué llevar será el valor nutricional. Supondremos que el total de calorías es un buen indicador. La **Tabla 1** ofrece una perspectiva de los productos disponibles, con su peso y calorías totales:

| **Alimento**            | **Peso (kg)** | **Calorías totales** |
|-------------------------|---------------|----------------------|
| Papas                   | 800           | 1.501.600            |
| Harina de trigo         | 400           | 1.444.000            |
| Arroz                   | 300           | 1.122.000            |
| Frijoles (lata)         | 300           | 690.000              |
| Latas de tomate         | 300           | 237.000              |
| Mermelada de fresa      | 50            | 130.000              |
| Mantequilla de maní     | 20            | 117.800              |

Dado que el contenido de cada caja es irrelevante para la decisión —a pesar de tus comprensibles protestas, el control de la misión es muy estricto en ese punto—, lo único que importa es el peso y las calorías totales que aporta cada caja.  
Por lo tanto, el problema se puede abstraer de la siguiente forma:  
**"Elige cualquier número de elementos de un conjunto (sin permitir fracciones de ningún elemento) de modo que el peso total no supere los 1000 kg y se maximice la cantidad total de calorías."**

#### Buscando soluciones

Una vez planteado el problema, podrías sentir la tentación de empacar la caja comenzando por el producto con mayor cantidad total de calorías, es decir, la caja de papas (800 kg). Sin embargo, si lo haces, ni el arroz ni la harina de trigo cabrán en la caja, y su cantidad combinada de calorías supera con creces cualquier otra combinación posible con los 200 kg restantes. Con esta estrategia, el mejor resultado sería de 1.749.400 calorías (seleccionando papas, mermelada de fresa y mantequilla de maní).

Aunque parece natural emplear un algoritmo voraz —que en cada paso elige la mejor opción inmediata—, este enfoque no resulta óptimo para este problema y requiere un análisis más detenido.

Reúnes a tu equipo de logística para una lluvia de ideas y, pronto, alguien sugiere que, en lugar de considerar las calorías totales, se evalúen las **calorías por kg**. Actualizas la **Tabla 1** añadiendo una nueva columna y la ordenas de mayor a menor. El resultado (ahora denominado **Tabla 2**) es el siguiente:

| **Alimento**            | **Peso (kg)** | **Calorías totales** | **Calorías por kg** |
|-------------------------|---------------|----------------------|---------------------|
| Mantequilla de maní     | 20            | 117.800              | 5.890               |
| Arroz                   | 300           | 1.122.000            | 3.740               |
| Harina de trigo         | 400           | 1.444.000            | 3.610               |
| Mermelada de fresa      | 50            | 130.000              | 2.600               |
| Frijoles (lata)         | 300           | 690.000              | 2.300               |
| Papas                   | 800           | 1.501.600            | 1.877               |
| Latas de tomate         | 300           | 237.000              | 790                 |

Intentas empacar la caja seleccionando de arriba hacia abajo los productos con mayor relación calorías/kg, es decir, mantequilla de maní, arroz, harina de trigo y mermelada de fresa, para alcanzar un total de 2.813.800 calorías.  
Aunque este resultado es significativamente mejor, observarás que incluir la mantequilla de maní impide agregar los frijoles, que en conjunto podrían aumentar aún más el valor total. La buena noticia es que, al menos, ya no tendrás que seguir la "dieta de *The Martian*" esta vez, las papas no irán a Marte.

Tras algunas horas más de análisis, se llega a la conclusión de que la única forma de garantizar la mejor solución es evaluar, para cada elemento, si al incluirlo o excluirlo se obtiene un resultado superior. Es decir, es necesario enumerar todas las posibles combinaciones, filtrar aquellas que excedan el límite de peso y elegir la mejor opción. Este método se conoce como **algoritmo de fuerza bruta**, y, como bien sabrás, resulta muy costoso desde el punto de vista matemático.

Dado que para cada elemento se tiene la opción de incluirlo o no, en el caso inicial (7 elementos) existen 2⁷ = 128 soluciones posibles. Aunque la cantidad parece manejable, al añadir 25 nuevos alimentos —entre ellos azúcar, naranjas, soja y marmite (¡no preguntes!)— el número de combinaciones se dispara a aproximadamente 4 mil millones, lo que haría inviable el análisis exhaustivo.

#### Algoritmos al rescate

Ante la explosión combinatoria, decides desarrollar un programa de computadora que procese los números y tome la mejor decisión. Sin embargo, el tiempo de ejecución resulta ser de un par de horas, y para empeorar la situación, algunos colonos tienen alergias (una cuarta parte no puede consumir gluten y varios son alérgicos a la marmite). Esto implica ejecutar el algoritmo múltiples veces, considerando restricciones individuales. Además, el control de la misión contempla agregar 30 nuevos elementos para compensar las restricciones dietéticas, llevando el total a 62 elementos y haciendo que el programa deba analizar billones de combinaciones.

Cuando todo parece perdido, alguien recuerda que en el equipo hay un experto en algoritmos. Tras una breve consulta, identifica el problema: se trata de la **mochila 0-1**, un problema NP-completo, lo que significa que no existe un algoritmo rápido (en términos polinomiales respecto al número de elementos) que garantice la solución óptima.  
Sin embargo, hay una buena noticia: existe una solución **pseudo-polinomial** mediante programación dinámica, cuyo tiempo de ejecución es proporcional a la capacidad máxima de la mochila. Suponiendo que la unidad mínima de peso sea 1 kg, solo se requerirán 1000 × 62 pasos, lo cual es infinitamente mejor que evaluar 2⁶² combinaciones. Una vez reescrito el algoritmo, se halla la mejor solución en cuestión de segundos.

Para el ejemplo inicial, la mejor combinación resulta ser: **arroz, harina de trigo y frijoles**, alcanzando un total de 3.256.000 calorías. Aunque puede parecer fácil con solo siete elementos, imagina el reto con cientos de productos; la tarea manual se vuelve impracticable.

####  Pensando (literalmente) fuera de la caja

En este punto entra en escena el verdadero experto en algoritmos. Imagina que un distinguido académico visita las instalaciones mientras se prepara la misión y es invitado a ayudar a calcular la ruta óptima para ahorrar combustible. Durante el almuerzo, le cuentan con orgullo cómo resolviste el problema de empaquetar suministros. Entonces, el experto plantea una pregunta aparentemente ingenua:

> **"¿Por qué no pueden cambiar el tamaño de las cajas?"**

La respuesta suele ser: "Así es como siempre se ha hecho" o "los productos ya vienen empaquetados de fábrica, y cambiar esto implicaría costos y retrasos".  
El experto, sin embargo, explica que, si se elimina la restricción del tamaño fijo de la caja, el problema de la mochila 0-1 (NP-completo) se transforma en el problema de la mochila sin restricciones. Para este nuevo escenario existe una solución **voraz (greedy)** en tiempo lineal, que suele superar incluso a la mejor solución de la versión 0-1.

Traducido a un lenguaje más comprensible, el problema se redefine de la siguiente forma:

> **"Dado un conjunto de elementos, elige cualquier subconjunto o fracción de ellos, de manera que su peso total no supere los 1000 kg, maximizando la cantidad total de calorías."**

Y sí, vale la pena invertir tiempo en reorganizar el empaquetado, pues se obtiene una mejora significativa.  
En concreto, si se permite tomar cualquier fracción del peso original de cada producto, se pueden empacar los productos comenzando por el que tenga la mayor relación calorías/kg (en este caso, la mantequilla de maní). Cuando se encuentre un producto que no quepa en el espacio restante, se toma solo la fracción necesaria para completar la caja. De esta forma, ni siquiera es necesario reempaquetar todos los productos, ¡solo uno!

La mejor solución en este escenario es:  

**Mantequilla de maní, arroz, harina de trigo, mermelada de fresa y 230 kg de frijoles**, alcanzando un total de 3.342.800 calorías.

#### Final feliz

En nuestra historia, gracias a este proceso, los futuros colonos de Marte tendrán mayores posibilidades de sobrevivir y no se verán condenados a una dieta basada únicamente en papas con un poco de mantequilla de maní y mermelada de fresa.

Desde el punto de vista computacional, hemos pasado por las siguientes etapas:

- **Algoritmos incorrectos:** Enfoques voraces que eligen el mayor total o la mayor relación de calorías sin tener en cuenta el conjunto global.
- **Algoritmo correcto pero inviable:** La solución por fuerza bruta, que evalúa todas las combinaciones posibles.
- **Solución inteligente:** Un método que organiza la computación de manera más eficiente.

El siguiente paso, aún más importante, fue pensar fuera de la caja para simplificar el problema eliminando algunas restricciones, lo que nos permitió encontrar un algoritmo más sencillo y una solución superior. Esta es, de hecho, otra regla de oro:

> **"Siempre estudia tus requisitos en profundidad, cuestiona las restricciones y, cuando sea posible, elimínalas si ello te permite encontrar una solución igualmente valiosa o incluso ligeramente inferior, pero a un costo mucho menor."**

Por supuesto, en este proceso existen otras consideraciones (como leyes y seguridad) que deben respetarse, por lo que algunas restricciones no pueden ser eliminadas.  
En la descripción de algoritmos, tras este análisis, lo siguiente sería detallar la solución y ofrecer pautas de implementación. No lo haremos aquí, ya que el algoritmo de programación dinámica para la mochila 0-1 está ampliamente documentado en la literatura y nuestro objetivo era ilustrar:

- La importancia de evitar elecciones subóptimas en los algoritmos y estructuras de datos.
- El proceso que seguiremos en futuras clases para presentar problemas y sus posibles soluciones.

### Preguntas 

A partir del análisis anterior y teniendo en cuenta el siguiente fragmento:

> "Si eliminamos la restricción del tamaño fijo de la caja, el problema de la mochila 0-1, que es NP-completo, se convierte en el problema de la mochila sin restricciones, para el cual existe una solución voraz (greedy) en tiempo lineal que suele ser mejor que la mejor solución de la versión 0-1.  
> 
> Traducido a un lenguaje más comprensible, podemos convertir este problema en uno más fácil de resolver, lo que nos permitirá empacar las cajas con la mayor cantidad posible de calorías.  
> 
> La declaración del problema ahora se convierte en:  
> 
> Dado un conjunto de elementos, elige cualquier subconjunto o fracción de los mismos, de manera que su peso total no supere los 1000 kg, maximizando la cantidad total de calorías.  
> 
> Y sí, vale la pena invertir tiempo en reorganizar el empaquetado, porque obtenemos una mejora significativa.  
> 
> Específicamente, si podemos tomar cualquier fracción del peso original de cada producto, simplemente empacamos los productos comenzando por el que tiene la mayor relación calorías/kg (mantequilla de maní, en este caso), y cuando llegamos a una caja que no cabría en el espacio disponible restante, tomamos una fracción de ella para llenar el espacio y la reempaquetamos. Así que, al final, ni siquiera tendríamos que reempaquetar todos los productos, solo uno.  
> 
> La mejor solución sería entonces: mantequilla de maní, arroz, harina de trigo, mermelada de fresa y 230 kg de frijoles, con un total de 3.342.800 calorías."

se pueden plantear las siguientes preguntas:

1. **Sobre NP-completitud y fuerza bruta:**  
   - ¿Por qué se dice que el problema de la mochila 0-1 es NP-completo?  
   - ¿Qué implicaciones tiene la NP-completitud en la viabilidad de resolver este problema mediante un algoritmo de fuerza bruta?

2. **Acerca de soluciones pseudo-polinomiales:**  
   - ¿Qué es una solución pseudo-polinomial y en qué se diferencia de una solución estrictamente polinomial?
   - Explica el concepto utilizando el algoritmo de programación dinámica para la mochila 0-1 como ejemplo. Describe cómo la capacidad de la mochila influye en la complejidad y justifica por qué se denomina "pseudo-polinomial".
   - ¿Cómo influye la capacidad máxima (en este caso, 1000 kg) en el tiempo de ejecución de la solución basada en programación dinámica?

3. **Enfoque voraz (greedy):**  
   - ¿Por qué el algoritmo voraz es inadecuado para la versión 0-1 del problema, pero resulta eficaz al permitir fracciones de productos?  
   - ¿Qué ventajas y desventajas presenta el enfoque voraz en comparación con otros métodos (como la programación dinámica) en el contexto de problemas de optimización?
   - Diseña en pseudocódigo un algoritmo voraz para la mochila fraccional, basándote en la estrategia de seleccionar primero el producto con mayor relación calorías/kg. Asegúrate de incluir el manejo del caso en el que se debe tomar solo una fracción de un producto.

2. **Análisis de Complejidad:**
   - **Pregunta:** ¿Cuál es la complejidad temporal del algoritmo voraz diseñado para la mochila fraccional?
   - **Tarea:** Justifica tu respuesta analizando cada paso (por ejemplo, la ordenación de los elementos y el recorrido para llenar la mochila).

4. **Transformación del problema:**  
   - ¿Cómo y por qué simplifica el problema al permitir la selección de fracciones de productos en lugar de cajas completas?  
   - ¿Qué impacto tiene esta transformación en la complejidad computacional del problema?
   - Escoge uno de los algoritmos discutidos (por ejemplo, el algoritmo de programación dinámica para la mochila 0-1) y desarrolla una prueba formal de correctitud y terminación.  
   -¿Qué elementos o condiciones consideras críticos para asegurar la terminación y la correctitud en el diseño de un algoritmo?
5. **Programación dinámica para la mochila 0-1**

   - ¿Cómo se puede estructurar un algoritmo de programación dinámica para resolver la mochila 0-1?
   -  Escribe en pseudocódigo el algoritmo de programación dinámica para este problema. Define la matriz (o tabla) que almacena las soluciones parciales y explica cómo se construye.
   - ¿Cómo se garantiza que el algoritmo de programación dinámica termina y que la solución encontrada es correcta?
   - Realiza una breve prueba o argumentación formal sobre la correctitud (por inducción, por ejemplo) y explica por qué el algoritmo finaliza en un número finito de pasos.
   - ¿Cuál es la complejidad temporal y espacial del algoritmo de programación dinámica para la mochila 0-1 en función del número de elementos y la capacidad máxima?
   - Justifica cómo se obtiene la complejidad pseudo-polinomial y compara este resultado con el enfoque de fuerza bruta.


6. **Comparación de enfoques algorítmicos**
   - **Tarea:** Elabora una tabla comparativa en la que se destaquen las principales características (ventajas, desventajas, complejidad temporal y aplicabilidad) de los siguientes enfoques:
     - Fuerza bruta
     - Algoritmo greedy (voraz)
     - Programación dinámica

