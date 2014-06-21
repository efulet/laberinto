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
from heapq import heappush, heappop, heapify
from math import sqrt

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

    def es_sucesor(self, candidato):
        """Comprueba si el candidato es un sucesor."""
        raise NotImplementedError

    def proxima_posicion(self):
        """Encuentra los sucesores."""
        raise NotImplementedError
    
    def reconstruir_camino(self):
        """Reconstruye el camino encontrado."""
        raise NotImplementedError


class BusquedaEnAnchura(Busqueda):
    """Esta clase implementa busqueda en anchura."""

    def __init__(self, laberinto, opciones):
        """Crea una instancia de la clase BusquedaEnAnchura.
        
        :param laberinto: Es un objeto de la clase Laberinto
        :param opciones: Valores opcionales para inicializar las variables de clase
        """

        self._laberinto = laberinto
        self._posicion_jugador = self._laberinto.obtener_posicion(2)
        self._cola = deque([self._posicion_jugador])
        self._meta = self._laberinto.obtener_posicion_meta()
        self._opciones = opciones
        self._camino_final = []

    def es_meta(self):
        return self._posicion_jugador == self._meta

    def hay_solucion(self):
        return len(self._cola) != 0

    def es_sucesor(self, candidato):
        lista = list(self._cola)
        for i in xrange(len(lista)):
            if lista[i] == candidato:
                return True
        return False

    def proxima_posicion(self):
        mapa = self._laberinto.obtener_matriz_laberinto()

        # Se libera la posicion actual. "4" significa "ya visitado"
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 4

        self._posicion_jugador = self._cola.popleft()

        # Nueva posicion del jugador. "2" significa "jugador"
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 2

        sucesores = self._laberinto.obtener_posiciones_libres(self._posicion_jugador)

        for sucesor in sucesores:
            if not self.es_sucesor(sucesor):
                self._cola.append(sucesor)
                self._camino_final.append((sucesor, self._posicion_jugador))

    def reconstruir_camino(self):
        lista = list()
        n = len(self._camino_final)
        elemento = self._camino_final[n - 1]
        #Mientras no sea el inicio.
        while elemento[1] != self._camino_final[0][0]:
            for i in xrange(0, len(self._camino_final)):
                if self._camino_final[i][0] == elemento[1]:
                    elemento = self._camino_final[i]
                    lista.append(elemento[0])
                    break
        return lista


class BusquedaEnProfundidad(Busqueda):
    """Esta clase implementa busqueda en profundidad."""

    def __init__(self, laberinto, opciones):
        """Crea una instancia de la clase BusquedaEnProfundidad.
        
        :param laberinto: Es un objeto de la clase Laberinto
        :param opciones: Valores opcionales para inicializar las variables de clase
        """

        self._laberinto = laberinto
        self._posicion_jugador = self._laberinto.obtener_posicion(2)
        self._cola = deque([self._posicion_jugador])
        self._meta = self._laberinto.obtener_posicion_meta()
        self._opciones = opciones
        self._camino_final = []

    def es_meta(self):
        return self._posicion_jugador == self._meta

    def hay_solucion(self):
        return len(self._cola) != 0

    def es_sucesor(self, candidato):
        lista = list(self._cola)
        for i in xrange(len(lista)):
            if lista[i] == candidato:
                return True
        return False

    def proxima_posicion(self):
        mapa = self._laberinto.obtener_matriz_laberinto()

        # Se libera la posicion actual. "4" significa "ya visitado"
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 4

        self._posicion_jugador = self._cola.pop()

        # Nueva posicion del jugador. "2" significa "jugador"
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 2

        sucesores = self._laberinto.obtener_posiciones_libres(self._posicion_jugador)

        for sucesor in sucesores:
            if not self.es_sucesor(sucesor):
                self._cola.append(sucesor)
                self._camino_final.append((sucesor, self._posicion_jugador))

    def reconstruir_camino(self):
        lista = list()
        n = len(self._camino_final)
        elemento = self._camino_final[n - 1]
        lista.append(elemento[0])
        #Mientras no sea el inicio.
        while elemento[1] != self._camino_final[0][0]:
            for i in xrange(0, len(self._camino_final)):
                if self._camino_final[i][0] == elemento[1]:
                    elemento = self._camino_final[i]
                    lista.append(elemento[0])
                    break
        return lista


class BusquedaCostoUniforme(Busqueda):
    """Esta clase implementa busqueda de costo uniforme."""

    def __init__(self, laberinto, opciones):
        """Crea una instancia de la clase BusquedaCostoAnchura.
        
        :param laberinto: Es un objeto de la clase Laberinto
        :param opciones: Valores opcionales para inicializar las variables de clase
        """

        self._laberinto = laberinto
        self._posicion_jugador = self._laberinto.obtener_posicion(2)
        self._costo_actual = 0
        self._heap = [(self._costo_actual, self._posicion_jugador)]
        heapify(self._heap)
        self._meta = self._laberinto.obtener_posicion_meta()
        self._opciones = opciones
        self._camino_final = []

    def es_meta(self):
        return self._posicion_jugador == self._meta

    def hay_solucion(self):
        return len(self._heap) != 0

    def es_sucesor(self, candidato):
        return False

    def proxima_posicion(self):
        mapa = self._laberinto.obtener_matriz_laberinto()

        # Se libera la posicion actual. "4" significa "ya visitado"
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 4

        nodo_actual = heappop(self._heap)

        self._costo_actual = nodo_actual[0]
        self._camino_final.append((nodo_actual[1], self._posicion_jugador))
        self._posicion_jugador = nodo_actual[1]

        # Nueva posicion del jugador. "2" significa "jugador"
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 2

        sucesores = self._laberinto.obtener_posiciones_libres(self._posicion_jugador)

        lista = list(self._heap)
        for sucesor in sucesores:
            costo = self._costo_actual + 1
            # Flag indica si es que existe o no ya en el heap el par (x,y).
            flag = False
            for i in xrange(len(lista)):
                if lista[i][1] == sucesor:
                    flag = True
                    if lista[i][0] >= costo:
                        # Debe cambiar el costo.
                        lista[i][0] = costo
                        # Debo heapifiar.
                        heapify(lista)
                        # Esto es para reconstruir el camino.
                        for j in xrange(0, len(self._camino_final)):
                            if self._camino_final[j][0] == sucesor:
                                self._camino_final[j] = (sucesor, self._posicion_jugador)
            # Finalmente, los que no existiesen se agregan.
            if not flag:
                heappush(lista, [costo, sucesor])
                # Esto es para reconstruir el camino.
                self._camino_final.append((sucesor, self._posicion_jugador))
        #Se actualiza el heap.
        self._heap = lista


    def reconstruir_camino(self):
        lista = list()
        n = len(self._camino_final)
        elemento = self._camino_final[n - 1]
        #Mientras no sea el inicio.
        while elemento[1] != self._camino_final[0][0]:
            for i in xrange(0, len(self._camino_final)):
                if self._camino_final[i][0] == elemento[1]:
                    elemento = self._camino_final[i]
                    lista.append(elemento[0])
                    break
        return lista


class BusquedaAEstrella(Busqueda):
    """Esta clase implementa busqueda A* con una heuristica pasada por parametro."""

    def __init__(self, laberinto, opciones):
        """Crea una instancia de la clase BusquedaCostoAnchura.

        :param laberinto: Es un objeto de la clase Laberinto
        :param opciones: Valores opcionales para inicializar las variables de clase
        """

        self._laberinto = laberinto
        self._posicion_jugador = self._laberinto.obtener_posicion(2)
        self._posicion_inicial = self._posicion_jugador
        self._meta = self._laberinto.obtener_posicion_meta()
        self._costo_actual = self._funcion_heuristica(self._posicion_inicial)
        self._heap = [[self._costo_actual, self._posicion_jugador]]
        heapify(self._heap)
        self._opciones = opciones
        self._camino_final = []

        #todo: que tal pasar la funcion heuristica y costo como parametros?
        #todo: que tal si ponemos en vez de [0] e [1], .x y .y para que sea mas lindo? En todos los lados que se hace uso de las coordenadas.

    def es_meta(self):
        return self._posicion_jugador == self._meta

    def hay_solucion(self):
        return len(self._heap) != 0

    def _funcion_heuristica(self, sucesor):
        dx = abs(sucesor[0] - self._meta[0])
        dy = abs(sucesor[1] - self._meta[1])
        dx2 = self._posicion_inicial[0] - self._meta[0]
        dy2 = self._posicion_inicial[1] - self._meta[1]
        cross = abs(dx * dy2 - dx2 * dy)
        # "Distancia" (sin raiz) euclideana!
        #return dx*dx +dy*dy
        # Distancia de Manhattan!
        return dx + dy + min(dx, dy)
        # Distancia de manhattan + cosa rara!
        #return dx + dy + min(dx, dy)

    def proxima_posicion(self):
        mapa = self._laberinto.obtener_matriz_laberinto()

        # Se libera la posicion actual. "4" significa "ya visitado"
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 4

        nodo_actual = heappop(self._heap)
        self._posicion_jugador = nodo_actual[1]
        self._camino_final.append((nodo_actual[1], self._posicion_jugador))
        self._costo_actual = nodo_actual[0] - self._funcion_heuristica(self._posicion_jugador)

        # Nueva posicion del jugador. "2" significa "jugador
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 2

        sucesores = self._laberinto.obtener_posiciones_libres(self._posicion_jugador)

        lista = list(self._heap)

        for sucesor in sucesores:
            heuristica = self._funcion_heuristica(sucesor)
            # Flag indica si es que existe o no ya en el heap el par (x,y).
            flag = False
            for i in xrange(len(lista)):
                if lista[i][1] == sucesor:
                    flag = True
                    if lista[i][0] >= self._costo_actual + 1 + heuristica:
                        # Debe cambiar el costo.
                        lista[i][0] = self._costo_actual + 1 + heuristica
                        # Debo heapifiar.
                        heapify(lista)
                        # Esto es para reconstruir el camino.
                        for j in xrange(0, len(self._camino_final)):
                            if self._camino_final[j][0] == sucesor:
                                self._camino_final[j] = (sucesor, self._posicion_jugador)
            # Finalmente, los que no existiesen se agregan.
            if not flag:
                heappush(lista, [self._costo_actual + 1 + heuristica, sucesor])
                # Esto es para reconstruir el camino.
                self._camino_final.append((sucesor, self._posicion_jugador))

        #Se actualiza el heap.
        self._heap = lista

    def reconstruir_camino(self):
        lista = list()
        n = len(self._camino_final)
        elemento = self._camino_final[n - 1]
        #Mientras no sea el inicio.
        while elemento[1] != self._camino_final[0][0]:
            for i in xrange(0, len(self._camino_final)):
                if self._camino_final[i][0] == elemento[1]:
                    elemento = self._camino_final[i]
                    lista.append(elemento[0])
                    break
        return lista

