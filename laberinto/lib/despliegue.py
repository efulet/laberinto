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
from gasp import *
import sys

from despliegue_excepcion import DespliegueExcepcion


class Despliegue:
    def __init__(self, laberinto, busqueda, opciones):
        """Crea una instancia de la clase Despliegue
        
        :param laberinto: Es un objeto de la clase Laberinto
        :param busqueda: Es un objecto de la clase busqueda
        :param opciones: Valores opcionales para inicializar las variables de clase
        """
        self._laberinto = laberinto
        self._busqueda = busqueda
        self._opciones = opciones

        self._width = self._laberinto.obtener_columnas() * 32
        self._height = self._laberinto.obtener_filas() * 32

    @staticmethod
    def _img_path():
        """Retorna el path de las imagenes"""
        pathfile = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(pathfile, "..", "img")

    def _dibujar(self):
        """Dibuja el mapa"""
        w = 16
        h = (self._laberinto.obtener_filas() * 32 ) - 16
        mapa = self._laberinto.obtener_matriz_laberinto()

        img_path = self._img_path()
        grass_path = os.path.join(img_path, "grass.png")
        bloque_path = os.path.join(img_path, "bloque.png")
        ball_path = os.path.join(img_path, "ball.png")
        migas_path = os.path.join(img_path, "migas.png")

        for f in xrange(self._laberinto.obtener_filas()):
            for c in xrange(self._laberinto.obtener_columnas()):
                Image(grass_path, (w, h))
                if mapa[f][c] == 0:
                    Image(bloque_path, (w, h))
                if mapa[f][c] == 2:
                    Image(ball_path, (w, h))
                if mapa[f][c] == 4:
                    Image(migas_path, (w, h))
                w += 32
            w = 16
            h -= 32

    def comenzar(self):
        """Inicia el despliegue del laberinto"""
        begin_graphics(width=self._width, height=self._height, title="Buscador de Caminos")

        while self._busqueda.hay_solucion():
            if self._busqueda.es_meta():
                update_when('key_pressed')
                print self._busqueda.reconstruir_camino()
                sys.exit()

            # Si no es meta buscar otro candidato
            self._busqueda.proxima_posicion()

            time.sleep(0.15)
            clear_screen()
            update_when('next_tick')
            self._dibujar()

        end_graphics()
