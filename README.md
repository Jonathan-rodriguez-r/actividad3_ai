# Pathfinder
Video demo: https://youtu.be/MiYJMIFpbcw

<img src="img/example.png" height="200">

Este es un algoritmo de búsqueda de rutas escrito en Python y que se muestra en el motor Pygame. Utiliza el algoritmo de búsqueda A* y su objetivo es encontrar la distancia más corta entre dos puntos, evitando cualquier obstáculo. En el diagrama anterior, los dos puntos finales están en azul oscuro, los nodos de la pared están en negro y el camino más corto se muestra en azul claro con una distancia de aproximadamente 38,63. Este algoritmo está garantizado para encontrar el camino más corto.

## Tabla de Contentenidos
* [ Instalación de Componentes ](#installation)
* [ Algoritmo de Busqueda A*  ](#a-star)
  * [ Explicación](#explanation)
  * [ Como usarlo ](#how-it-is-used-here)

<a name="installation"></a>
## Instalación

Primero, instala pygame leyendo las instrucciones [here](https://www.pygame.org/wiki/GettingStarted).


Una vez que esté instalado, ingrese a la carpeta del buscador de rutas y ejecute pathfinding.py usando Python 3. Los métodos pueden variar, pero aquí hay un ejemplo de un comando:
> python3 pathfinder.py


<a name="a-star"></a>
## Algoritmo de Busqueda A*
Credit to [Wikipedia](*https://en.wikipedia.org/wiki/A*_search_algorithm) for providing the information for the algorithm.

A* es un algoritmo de búsqueda que se utiliza para encontrar la ruta óptima entre dos ubicaciones. Se ejecuta más rápido que el algoritmo de Dijkstra y tiene en cuenta dos propiedades para determinar la prioridad de búsqueda de los nodos: 

* La distancia ya recorrida para llegar al nodo actual
* La distancia estimada entre el nodo actual y el nodo objetivo


<a name="explanation"></a>
### Explicación
El algoritmo A* utiliza dos conjuntos para realizar un seguimiento de los nodos. El conjunto cerrado se usa para rastrear cada nodo que ya se ha buscado, ya que no tiene sentido buscar un nodo dos veces. El conjunto abierto es la cola de prioridad del algoritmo, que se utiliza para determinar qué nodos se van a buscar.

El algoritmo tiene un orden muy específico en el que se deben buscar los nodos, y esto es lo que separa a A* de muchos de los otros algoritmos de búsqueda. A cada nodo se le asigna una *puntuación f*, que se encuentra usando la suma *g(n) + h(n)*. La función *g(n)* es la distancia recorrida desde el nodo de inicio, y *h(n)* es una función heurística, que estima la distancia entre el nodo de inicio y el de destino. El algoritmo busca el nodo con la puntuación f más baja que se encuentra en el conjunto abierto.

Cuando se busca un nodo, se agrega inmediatamente al conjunto cerrado y se analiza cada uno de sus vecinos. Cuando encuentra un vecino que ya se ha buscado, si la ruta actual es una distancia más corta, entonces se reescribe la ruta al vecino. Vea el ejemplo a continuación:

<img src="img/a_star_diagram.png" height=250>

En este diagrama, cada nodo está numerado del 1 al 5 para distinguirlos, siendo el nodo 1 el nodo de inicio y el nodo 5 el nodo de destino. Cada nodo tiene un número escrito adentro para indicar la distancia al nodo objetivo, que representa *h(n)*, y cada segmento de línea tiene una longitud. A primera vista, es fácil decir que el camino desde los nodos 1 -> 2 -> 4 -> 5 es el mejor camino, y recorremos un total de (1 + 2 + 2) = 5 unidades.

Inicialmente, el algoritmo comienza agregando el nodo 1 (el nodo inicial) al conjunto abierto, y dado que el nodo 1 es el único nodo en el conjunto abierto, se busca. Una vez que se busca el nodo 1, se agrega inmediatamente al conjunto cerrado. Se analizan sus vecinos, los nodos 2, 3 y 4. Las puntuaciones se dan en la siguiente tabla:

| Node | g(n) | h(n) | f(n) = g(n) + h(n) |
|------|------|------|--------------------|
| 2    | 1    | 4    | 5                  | 
| 3    | 2    | 5    | 7                  | 
| 4    | 4    | 2    | 6                  | 

Dado que el nodo 2 tiene la puntuación f más baja (5), se busca a continuación. Los vecinos del nodo 2 son los nodos 1 y 4, sin embargo, dado que el nodo 1 está en el conjunto cerrado, solo se analiza el nodo 4. Ahora nos damos cuenta de que al nodo 4 se le otorga una puntuación de 6 si comenzamos desde el nodo 1, sin embargo, a través del nodo 4, nos damos cuenta de que la puntuación f es *(1 + 2) + 2 = 5*, ¡que es un mejor camino! Esto significa que la ruta original 1 -> 4 se reemplaza con la ruta 1 -> 2 -> 4. Luego se agrega el nodo 2 al conjunto cerrado.

Ahora el nodo 4 tiene la puntuación f más baja de 5, por lo que se busca. Luego, se analiza el nodo objetivo, por lo que el programa finaliza. La ruta óptima de este algoritmo es, por lo tanto, del nodo 1 al nodo 2 al nodo 4 al nodo 5.

### Como se usa?
En el programa, cada nodo que no está en los bordes o esquinas tiene ocho vecinos. Para cualquier paso vertical u horizontal, el algoritmo lo registra como una distancia de 1. Para cualquier paso diagonal, la distancia se registra como la raíz cuadrada de 2.

Por el bien de este programa, la función heurística *h(n)* calcula la distancia más corta posible entre el nodo actual y el nodo objetivo, a través de pasos horizontales, verticales y diagonales. Si *d(n)* es la distancia real más corta entre el nodo actual y el nodo objetivo, entonces la desigualdad *h(n) ≤ d(n)* siempre se cumple.

Aquí hay una prueba de que este algoritmo siempre produce el camino más corto. Considere el paso final del algoritmo, donde se busca el nodo objetivo. Entonces esto debe significar que el nodo objetivo tiene la puntuación f más baja, sin embargo, dado que la distancia entre el nodo objetivo y él mismo es cero, *h(n) = 0* y *f(n) = g(n)*. Esto significa que la puntuación f es precisamente la distancia entre el nodo de inicio y el nodo de destino que toman ese camino. Sea esta distancia *d*.

Ahora considere cada nodo en el conjunto abierto. Sabemos que sus puntajes f deben ser mayores que *d*. Una vez más, sea *d(n)* la distancia real más corta entre el nodo actual y el nodo objetivo. Entonces tenemos la desigualdad,

*d ≤ f(n) = g(n) + h(n) ≤ g(n) + d(n)*.

Por lo tanto, *d ≤ g(n) + d(n)*, y tomar ese camino producirá una distancia mayor que *d*. Por lo tanto, el camino con distancia *d* es el más corto.
