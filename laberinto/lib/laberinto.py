"""
@created_at 2014-06-09
@author Exequiel Fuentes <efulet@gmail.com>
@author Brian Keith <briankeithn@gmail.com>

Basado en el trabajo de Juan Bekios-Calfa <juan.bekios@ucn.cl>
"""

# Se recomienda seguir los siguientes estandares:
#   1. Para codificacion: PEP 8 - Style Guide for Python Code (http://legacy.python.org/dev/peps/pep-0008/)
#   2. Para documentacion: PEP 257 - Docstring Conventions (http://legacy.python.org/dev/peps/pep-0257/)

import os

from laberinto_excepcion import LaberintoExcepcion

class Laberinto:
    """Esta clase representa al laberinto. Tiene como entrada un mapa en formato 
    texto el cual es procesado por esta clase y guardado en un objeto para su 
    posterior uso.
    """
    
    def __init__(self, optiones):
        """Crea una instancia de la clase Laberinto
        
        :param optiones: Valores opcionales para inicializar las variables de clase
        """
        self._optiones = optiones
        
        # Si no hay un mapa como entrada se usa el mapa de ejemplo
        # TODO: cambiar nombre de la opcion "input"?? algo como mapa?
        if self._optiones.input:
            self._mapa_path = self._optiones.input
        else:
            self._mapa_path = self._input_path()
        
        self._mapa = self._leer_mapa()
        self._filas = len(self._mapa)
        self._columnas = len(self._mapa[0])
        
        # 3 representa a la meta
        self._posicion_meta = self._obtener_posicion(3)
        
        # 2 representa al jugador
        self._posicion_inicial_jugador = self._obtener_posicion(2)
    
    def _input_path(self):
        """Retorna el path del archivo laberinto usado como ejemplo"""
        pathfile = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(pathfile, "..", "input", "laberinto.txt")
    
    def _leer_mapa(self):
        """Lee el mapa de entrada el cual esta en formato texto. Retorna una 
        representacion del mapa en una lista."""
        # primero verifica si el archivo existe, sino existe crea una excepcion
        if os.path.isfile(self._mapa_path) == False:
            error_msg = "Archivo de entrada no existe: " + self._mapa_path
            raise LaberintoExcepcion(error_msg)
        
        # lee el archivo de entrada y a la vez remueve el salto de linea al final
        lineas = [linea.strip() for linea in open(self._mapa_path)]
        
        # transforma un caracter en una representacion numerica
        mapa = []
        for i in xrange(len(lineas)):
            lista = []
            cadena = lineas[i]
            
            for j in xrange(len(cadena)):
                if cadena[j] == ".":
                    lista.append(1)
                if cadena[j] == "#":
                    lista.append(0)
                if cadena[j] == "T":
                    lista.append(2)
                if cadena[j] == "S":
                    lista.append(3)
            
            mapa.append(lista)
        
        return mapa
    
    def _obtener_posicion(self, objeto):
        """Retorna las coordenadas de un objecto especifico"""
        for f in xrange(self._filas):
            for c in xrange(self._columnas):
                if self._mapa[f][c] == objeto:
                    return [f, c]
    
    def obtener_filas(self):
        """Retorna las filas"""
        return self._filas
    
    def obtener_columnas(self):
        """Retorna las columnas"""
        return self._columnas
    
    def obtener_matriz_laberinto(self):
        """Returna la representacion del mapa"""
        return self._mapa
    
    def obtener_posicion_meta(self):
        """Retorna la posicion de la meta"""
        return self._posicion_meta
              
    def obtener_posicion_inicial_jugador(self):
        """Retorna la posicion inicial del jugador"""
        return self._posicion_inicial_jugador
    
    def obtener_posiciones_libres(self, posicion_objeto):
        libres = []
        
        if self._mapa[posicion_objeto[0]-1][posicion_objeto[1]] == 1:
            libres.append([posicion_objeto[0]-1, posicion_objeto[1]])
        if self._mapa[posicion_objeto[0]+1][posicion_objeto[1]] == 1:
            libres.append([posicion_objeto[0]+1, posicion_objeto[1]])
        if self._mapa[posicion_objeto[0]][posicion_objeto[1]-1] == 1:
            libres.append([posicion_objeto[0], posicion_objeto[1]-1])
        if self._mapa[posicion_objeto[0]][posicion_objeto[1]+1] == 1:
            libres.append([posicion_objeto[0], posicion_objeto[1]+1])
        
        return libres
    
    def to_str(self):
        """Retorna el mapa en formato texto"""
        mapa_str = ""
        
        for f in xrange(self._filas):
            for c in xrange(self._columnas):
                if self._mapa[f][c] == 0:
                    mapa_str += "# "
                if self._mapa[f][c] == 1:
                    mapa_str += "  "
                if self._mapa[f][c] == 4:
                    mapa_str += ". "
                if self._mapa[f][c] == 2:
                    mapa_str += "T "
                if self._mapa[f][c] == 3:
                    mapa_str += "S "
                if self._mapa[f][c] == 5:
                    mapa_str += "  "
            mapa_str += '\n'
        
        return mapa_str
