#!/bin/bash

# Este script corre el programa laberinto
#
# Author: Exequiel Fuentes <efulet@gmail.com>
# Author: Brian Keith <briankeithn@gmail.com>

# Version de python valida
PYTHON_VERSION=2.7

if which python >/dev/null
then
  if ! (test "$(echo `python -c 'import sys;print(sys.version_info[:2])'`)" = "(2, 7)")
  then
    echo "Parece que python v${PYTHON_VERSION} no esta instalado en el sistema"
  fi
else
  echo "Parece que python v${PYTHON_VERSION} no esta instalado en el sistema"
fi

BINPATH=`dirname $0`
python "$BINPATH/../laberinto/main.py" $@
