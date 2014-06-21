"""
@created_at 2014-06-09
@author Exequiel Fuentes <efulet@gmail.com>
@author Brian Keith <briankeithn@gmail.com>
"""

# Se recomienda seguir los siguientes estandares:
#   1. Para codificacion: PEP 8 - Style Guide for Python Code (http://legacy.python.org/dev/peps/pep-0008/)
#   2. Para documentacion: PEP 257 - Docstring Conventions (http://legacy.python.org/dev/peps/pep-0257/)

import traceback
import sys
import datetime

from lib import *


def check_version():
    """Python v2.7 es requerida por el curso, entonces verificamos la version"""
    if sys.version_info[:2] != (2, 7):
        raise Exception("Parece que python v2.7 no esta instalado en el sistema")


if __name__ == '__main__':
    try:
        # Verificar version de python
        check_version()
        
        opciones = Opciones()
        opts = opciones.parse(sys.argv[1:])
        
        laberinto = Laberinto(opts)
        
        # todo: Que tal agregar una medida de cuantos cuadritos tuvo que recorrer el algoritmo antes de terminar?
        # y ademas tener un contador de los cuadritos libres del laberinto, con eso se puede calcular
        # el % de cuadrados recorridos respecto al total de cuadrados recorribles, y junto con el tiempo
        # seria una metrica bastante interesante creo.

        busqueda = None
        if opts.bea:
            print "Ejecutando Busqueda en Anchura..."
            busqueda = BusquedaEnAnchura(laberinto, opts)
        elif opts.bep:
            print "Ejecutando Busqueda en Profundidad..."
            busqueda = BusquedaEnProfundidad(laberinto, opts)
        elif opts.bcu:
            print "Ejecutando Busqueda Costo Uniforme..."
            busqueda = BusquedaCostoUniforme(laberinto, opts)
        elif opts.bae:
            print "Ejecutando Busqueda A*..."
            busqueda = BusquedaAEstrella(laberinto, opts)
        else:
            print "Ejecutando Busqueda en Anchura..."
            busqueda = BusquedaEnAnchura(laberinto, opts)
        
        if not opts.tiempo:
            despliegue = Despliegue(laberinto, busqueda, opts)
            despliegue.comenzar()
        else:
            start = datetime.datetime.now()
            busqueda.encontrar()
            #print busqueda.reconstruir_camino()
            print "La ejecucion tomo:", str(datetime.datetime.now() - start)
    except Exception, err:
        print traceback.format_exc()
    finally:
        sys.exit()
