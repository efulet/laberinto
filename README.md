Primer Taller de Sistemas Inteligentes
======================================

Introduccion
------------

Este proyecto implementa 4 soluciones para el problema de llegar a la salida en 
un laberinto. Se utilizan los siguientes algoritmos para resolver el problema:

  * Breadth-First Search (BFS).
  * Depth-First Search (DFS).
  * Uniform Cost Search (UCS).
  * A* Search.

Como ejecutar el programa
-------------------------

Este programa puede ejecutarse de la siguiente manera:

  $> ./bin/laberinto.sh

  O

  $> python main.py

Las busquedas pueden elegirse con las siguientes opciones, por defecto se 
ejecuta Busqueda en Anchura:
  
  * BusquedaEnAnchura:
    $> ./bin/laberinto.sh -bea

  * BusquedaEnProfundidad:
    $> ./bin/laberinto.sh -bep

  * BusquedaCostoUniforme:
    $> ./bin/laberinto.sh -bcu

  * BusquedaA*:
    $> ./bin/laberinto.sh -bae