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
  
  * Busqueda En Anchura:
    $> ./bin/laberinto.sh -bea

  * Busqueda En Profundidad:
    $> ./bin/laberinto.sh -bep

  * Busqueda Costo Uniforme:
    $> ./bin/laberinto.sh -bcu

  * Busqueda A*:
    $> ./bin/laberinto.sh -bae