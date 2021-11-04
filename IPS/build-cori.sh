#!/bin/bash

export IMAS_PREFIX=$HOME/IMAS
export IMAS_VERSION=3.34.0
export PYTHONPATH=$IMAS_PREFIX/python/lib
export LD_LIBRARY_PATH=$IMAS_PREFIX/lib:$LD_LIBRARY_PATH

#ifort -I${IMAS_PREFIX}/include/ifort -o imas imas.f90 -L${IMAS_PREFIX}/lib -limas-ifort

module load gcc
gfortran -I${IMAS_PREFIX}/include/gfortran -o imas imas.f90 -L${IMAS_PREFIX}/lib -limas-gfortran
