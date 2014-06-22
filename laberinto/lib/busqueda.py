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

from busqueda_excepcion import BusquedaExcepcion


class Busqueda:
    """Esta clase abstracta define los metodos que deben ser implementados por las 
    busquedas especificas. El fin de esta clase es estandarizar la implementacion
    de sus clases hijas.
    """
    
    def nombre_busqueda(self):
        """Retorna el tipo de busqueda."""
        raise NotImplementedError
    
    def es_meta(self):
        """Comprueba si el jugador llego a la meta."""
        return self._posicion_jugador == self._meta

    def hay_solucion(self):
        """Comprueba si la busqueda encontro la solucion."""
        return len(self._abiertos) != 0

    def es_sucesor(self, candidato):
        """Comprueba si el candidato es un sucesor."""
        raise NotImplementedError
    
    def encontrar(self):
        """Encuentra el camino."""
        while self.hay_solucion():
            if self.es_meta():
                break
            # Si no es meta buscar otro candidato
            self.proxima_posicion()
    
    def proxima_posicion(self):
        """Encuentra los sucesores."""
        raise NotImplementedError

    def reconstruir_camino(self):
        """Reconstruye el camino solucion."""
        lista = list()
        elemento = None
        #Se busca primero la posicion final (que no necesariamente es la ultima del arreglo).
        for k in xrange(len(self._camino_final)):
            if self._camino_final[k][0] == self._meta:
                elemento = self._camino_final[k]
                break

        #Si es que no se encontro solucion no hay camino final.
        if elemento is None:
            return lista

        #Se busca los padres mientras no sea el inicio.
        while elemento[1] != self._posicion_inicial:
            for i in xrange(0, len(self._camino_final)):
                if self._camino_final[i][0] == elemento[1]:
                    elemento = self._camino_final[i]
                    lista.append(elemento[0])
                    break
        return lista


class BusquedaEnAnchura(Busqueda):
    """Esta clase implementa busqueda en anchura."""

    def __init__(self, laberinto, opciones):
        """Crea una instancia de la clase BusquedaEnAnchura.
        
        :param laberinto: Es un objeto de la clase Laberinto
        :param opciones: Valores opcionales para inicializar las variables de clase
        """

        self._laberinto = laberinto
        self._posicion_jugador = self._laberinto.obtener_posicion_inicial_jugador()
        self._posicion_inicial = self._posicion_jugador
        self._abiertos = deque([self._posicion_jugador])
        self._meta = self._laberinto.obtener_posicion_meta()
        self._opciones = opciones
        self._camino_final = [(self._posicion_inicial, None)]
    
    def nombre_busqueda(self):
        return "Busqueda En Anchura"
    
    def es_sucesor(self, candidato):
        lista = list(self._abiertos)
        for i in xrange(len(lista)):
            if lista[i] == candidato:
                return True
        return False

    def proxima_posicion(self):
        mapa = self._laberinto.obtener_matriz_laberinto()
        # Se libera la posicion actual. "4" significa "ya visitado"
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 4
        self._posicion_jugador = self._abiertos.popleft()
        # Nueva posicion del jugador. "2" significa "jugador"
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 2
        sucesores = self._laberinto.obtener_posiciones_libres(self._posicion_jugador)
        for sucesor in sucesores:
            if not self.es_sucesor(sucesor):
                self._abiertos.append(sucesor)
                self._camino_final.append((sucesor, self._posicion_jugador))


class BusquedaEnProfundidad(Busqueda):
    """Esta clase implementa busqueda en profundidad."""

    def __init__(self, laberinto, opciones):
        """Crea una instancia de la clase BusquedaEnProfundidad.
        
        :param laberinto: Es un objeto de la clase Laberinto
        :param opciones: Valores opcionales para inicializar las variables de clase
        """

        self._laberinto = laberinto
        self._posicion_jugador = self._laberinto.obtener_posicion_inicial_jugador()
        self._posicion_inicial = self._posicion_jugador
        self._abiertos = deque([self._posicion_jugador])
        self._meta = self._laberinto.obtener_posicion_meta()
        self._opciones = opciones
        self._camino_final = [(self._posicion_inicial, None)]
    
    def nombre_busqueda(self):
        return "Busqueda En Profundidad"
    
    def es_sucesor(self, candidato):
        lista = list(self._abiertos)
        for i in xrange(len(lista)):
            if lista[i] == candidato:
                return True
        return False

    def proxima_posicion(self):
        mapa = self._laberinto.obtener_matriz_laberinto()
        # Se libera la posicion actual. "4" significa "ya visitado"
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 4
        self._posicion_jugador = self._abiertos.pop()
        # Nueva posicion del jugador. "2" significa "jugador"
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 2
        sucesores = self._laberinto.obtener_posiciones_libres(self._posicion_jugador)
        for sucesor in sucesores:
            if not self.es_sucesor(sucesor):
                self._abiertos.append(sucesor)
                self._camino_final.append((sucesor, self._posicion_jugador))


class BusquedaCostoUniforme(Busqueda):
    """Esta clase implementa busqueda de costo uniforme."""

    def __init__(self, laberinto, opciones):
        """Crea una instancia de la clase BusquedaCostoAnchura.
        
        :param laberinto: Es un objeto de la clase Laberinto
        :param opciones: Valores opcionales para inicializar las variables de clase
        """

        self._laberinto = laberinto
        self._posicion_jugador = self._laberinto.obtener_posicion_inicial_jugador()
        self._posicion_inicial = self._posicion_jugador
        self._costo_actual = 0
        self._abiertos = [(self._costo_actual, self._posicion_jugador)]
        heapify(self._abiertos)
        self._meta = self._laberinto.obtener_posicion_meta()
        self._opciones = opciones
        self._camino_final = [(self._posicion_inicial, None)]
    
    def nombre_busqueda(self):
        return "Busqueda Costo Uniforme"
    
    def proxima_posicion(self):
        mapa = self._laberinto.obtener_matriz_laberinto()
        # Se libera la posicion actual. "4" significa "ya visitado"
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 4
        nodo_actual = heappop(self._abiertos)
        self._costo_actual = nodo_actual[0]
        self._posicion_jugador = nodo_actual[1]
        # Nueva posicion del jugador. "2" significa "jugador"
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 2
        sucesores = self._laberinto.obtener_posiciones_libres(self._posicion_jugador)
        lista = list(self._abiertos)
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
        self._abiertos = lista


class BusquedaAEstrella(Busqueda):
    """Esta clase implementa busqueda A* con una heuristica pasada por parametro."""

    def __init__(self, laberinto, opciones):
        """Crea una instancia de la clase BusquedaCostoAnchura.

        :param laberinto: Es un objeto de la clase Laberinto
        :param opciones: Valores opcionales para inicializar las variables de clase
        """

        self._laberinto = laberinto
        self._posicion_jugador = self._laberinto.obtener_posicion_inicial_jugador()
        self._posicion_inicial = self._posicion_jugador
        self._meta = self._laberinto.obtener_posicion_meta()
        self._costo_actual = self._funcion_heuristica(self._posicion_inicial)
        self._abiertos = [[self._costo_actual, self._posicion_jugador]]
        heapify(self._abiertos)
        self._opciones = opciones
        self._camino_final = [(self._posicion_inicial, None)]
    
    def nombre_busqueda(self):
        return "Busqueda A*"
    
    def _funcion_heuristica(self, sucesor):
        """Este metodo calcula el costo heuristico del sucesor dado.
        La heuristica utilizada es la distancia de Manhattan

        :param sucesor: Es una tupla (x,y) con las coordenadas de la posicion.
        """
        dx = abs(sucesor[0] - self._meta[0])
        dy = abs(sucesor[1] - self._meta[1])
        # Distancia de Manhattan!
        heuristica = dx + dy
        # Se agrega un factor rompe empates.
        p = 0.001
        return heuristica * (1 + p)

    def proxima_posicion(self):
        mapa = self._laberinto.obtener_matriz_laberinto()
        # Se libera la posicion actual. "4" significa "ya visitado"
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 4
        nodo_actual = heappop(self._abiertos)
        self._posicion_jugador = nodo_actual[1]
        self._costo_actual = nodo_actual[0] - self._funcion_heuristica(self._posicion_jugador)
        # Nueva posicion del jugador. "2" significa "jugador
        mapa[self._posicion_jugador[0]][self._posicion_jugador[1]] = 2
        sucesores = self._laberinto.obtener_posiciones_libres(self._posicion_jugador)
        lista = list(self._abiertos)
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
        self._abiertos = lista
