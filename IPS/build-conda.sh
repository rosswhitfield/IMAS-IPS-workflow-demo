#!/bin/bash
conda activate imas
gfortran -I${IMAS_PREFIX}/include/gfortran -o imas imas.f90 -L${IMAS_PREFIX}/lib -limas-gfortran
