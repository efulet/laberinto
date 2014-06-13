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

from lib import Optiones
from lib import Laberinto
from lib import BusquedaEnAnchura
from lib import BusquedaEnProfundidad
from lib import Despliegue

def check_version():
    """Python v2.7 es requerida por el curso, entonces verificamos la version"""
    if sys.version_info[:2] != (2, 7):
        raise Exception("Parece que python v2.7 no esta instalado en el sistema")

if __name__ == '__main__':
    try:
        # Verificar version de python
        check_version()
        
        optiones = Optiones()
        opts = optiones.parse(sys.argv[1:])
        
        # Ejemplo como medir tiempo de ejecucion, quizas podamos usar una 
        # libreria mas especializada para medir el uso de la memoria y cosas
        # asi.
        #print "Ejecutando Depth-First Search..."
        #start = datetime.datetime.now()
        #q1.depth_first_search()
        #print "La ejecucion tomo:", str(datetime.datetime.now() - start)
        
        laberinto = Laberinto(opts)
        
        #TODO: Si usamos opciones podemos elegir el tipo de busqueda
        busqueda = BusquedaEnAnchura(laberinto, opts)
        #busqueda = BusquedaEnProfundidad(laberinto, opts)

        despliegue = Despliegue(laberinto, busqueda, opts)
        despliegue.comenzar()
    except Exception, err:
        print traceback.format_exc()
