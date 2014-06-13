"""
@created_at 2014-06-09
@author Exequiel Fuentes <efulet@gmail.com>
@author Brian Keith <briankeithn@gmail.com>
"""

# Se recomienda seguir los siguientes estandares:
#   1. Para codificacion: PEP 8 - Style Guide for Python Code (http://legacy.python.org/dev/peps/pep-0008/)
#   2. Para documentacion: PEP 257 - Docstring Conventions (http://legacy.python.org/dev/peps/pep-0257/)

from argparse import ArgumentParser


class Opciones:
    """Esta clase ayuda a manejar los argumentos que pueden ser pasados por la 
    linea de comandos.
    
    Por ejemplo, escriba:
    $> ./bin/laberinto.sh --help
    """

    def __init__(self):
        self.parser = ArgumentParser(usage='/bin/laberinto.sh [--help]')
        self._init_parser()

    def _init_parser(self):
        # TODO: Agregar opciones para cada tipo de busqueda
        self.parser.add_argument('-a', '--auto',
                                 help='movimiento automatico o por tecla',
                                 action='store_true')
        self.parser.add_argument('-i', '--input',
                                 help='mapa en formato texto')

    def parse(self, args=None):
        return self.parser.parse_args(args)
