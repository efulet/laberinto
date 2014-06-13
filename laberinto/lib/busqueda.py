"""
@created_at 2014-06-09
@author Exequiel Fuentes <efulet@gmail.com>
@author Brian Keith <briankeithn@gmail.com>

Basado en el trabajo de Juan Bekios-Calfa <juan.bekios@ucn.cl>
"""

# Se recomienda seguir los siguientes estandares:
#   1. Para codificacion: PEP 8 - Style Guide for Python Code (http://legacy.python.org/dev/peps/pep-0008/)
#   2. Para documentacion: PEP 257 - Docstring Conventions (http://legacy.python.org/dev/peps/pep-0257/)

from collections import deque

from busqueda_excepcion import BusquedaExcepcion

class Busqueda:
    """Esta clase define los metodos que deben ser implementados por las 
    busquedas especificas. El fin de esta clase es estandarizar la implentacion 
    de sus clases hijas.
    """
    def es_meta(self):
        """Comprueba si el jugador llego a la meta."""
        raise NotImplementedError
    
    def hay_solucion(self):
        """Comprueba si la busqueda encontro la solucion."""
        raise NotImplementedError
    
    def proxima_posicion(self):
        """Encuentra los sucesores."""
        raise NotImplementedError

class BusquedaEnAnchura(Busqueda):
    """Esta clase implementa busqueda en anchura."""
    
    # TODO: Esto es un ejemplo
    #def breadth_first_search(self):
        #"""Encuentra todas las posibles soluciones usando el algoritmo Breadth-First."""
        #initial_state = self.__create_board()
        #open_states = []
        #open_states = deque([])
        #open_states.append(initial_state)
        #valid_boards = []
        #
        #while open_states:
        #    current_board = open_states.popleft()
        #    if current_board.is_valid():
        #        valid_boards.append(current_board)
        #    else:
        #        # Genera proximos estados
        #        new_boards = self.__get_successors(current_board)
        #        for new_board in new_boards:
        #            open_states.append(new_board)
        #
        #return valid_boards
    
    def __init__(self, laberinto, optiones):
        """Crea una instancia de la clase BusquedaEnAnchura.
        
        :param laberinto: Es un objeto de la clase Laberinto
        :param optiones: Valores opcionales para inicializar las variables de clase
        """
        
        # BFS is based on queue data structure.
        # Aca se inicializan los estados
        
        self._laberinto = laberinto
        self._posicion_jugador = self._laberinto.obtener_posicion_inicial_jugador()
        self._cola = deque([self._posicion_jugador])
        self._meta = self._laberinto.obtener_posicion_meta()
        self._optiones = optiones
    
    def es_meta(self):
        return self._posicion_jugador == self._meta
    
    def hay_solucion(self):
        return len(self._cola) != 0
    
    #TODO queda pendiente calcular los siguientes sucesores y guardar los visitados
    def proxima_posicion(self):
        mapa = self._laberinto.obtener_matriz_laberinto()
        
        # Se libera la posicion actual. "4" significa "ya visitado"
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 4
        
        # Nueva posicion del jugador. "2" significa "jugador"
        self._posicion_jugador = self._cola.popleft()
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 2
        
        sucesores = self._laberinto.obtener_posiciones_libres(self._posicion_jugador)
        
        for sucesor in sucesores:
            self._cola.append(sucesor)

class BusquedaEnProfundidad(Busqueda):
    """Esta clase implementa busqueda en profundidad."""
    
    # TODO: Esto es un ejemplo
    #def depth_first_search(self):
        #"""Encuentra todas las posibles soluciones usando el algoritmo Depth-First."""
        #initial_state = self.__create_board()
        #open_states = []
        #open_states.append(initial_state)
        #valid_boards = []
        #
        #while open_states:
        #    current_board = open_states.pop()
        #    if current_board.is_valid():
        #        valid_boards.append(current_board)
        #    else:
        #        # Genera proximos estados
        #        new_boards = self.__get_successors(current_board)
        #        for new_board in new_boards:
        #            open_states.append(new_board)
        #
        #return valid_boards
    
    def __init__(self, laberinto, optiones):
        """Crea una instancia de la clase BusquedaEnProfundidad.
        
        :param laberinto: Es un objeto de la clase Laberinto
        :param optiones: Valores opcionales para inicializar las variables de clase
        """
        
        # DFS is based on stack data structure.
        
        self._laberinto = laberinto
        self._posicion_jugador = self._laberinto.obtener_posicion_inicial_jugador()
        self._cola = deque([self._posicion_jugador])
        self._meta = self._laberinto.obtener_posicion_meta()
        self._optiones = optiones
    
    def es_meta(self):
        return self._posicion_jugador == self._meta
    
    def hay_solucion(self):
        return len(self._cola) != 0

    #TODO queda pendiente calcular los siguientes sucesores y guardar los visitados
    def proxima_posicion(self):
        mapa = self._laberinto.obtener_matriz_laberinto()

        # Se libera la posicion actual. "4" significa "ya visitado"
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 4

        # Nueva posicion del jugador. "2" significa "jugador"
        self._posicion_jugador = self._cola.pop()
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 2

        sucesores = self._laberinto.obtener_posiciones_libres(self._posicion_jugador)

        for sucesor in sucesores:
            self._cola.append(sucesor)
