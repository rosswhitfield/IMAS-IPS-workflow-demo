#!/bin/bash
module load matlab/R2021a
module load anaconda3/2021.5
module load intel-mkl/2020.1
module load intel/19.1.1.217

export IMAS_PREFIX=/home/apankin/software/AL.3_33
export IMAS_VERSION=3.33.0

export PYTHONPATH=/home/apankin/software/AL.3_33/python/lib
export LD_LIBRARY_PATH=/home/apankin/software/AL.3_33/lib:/home/apankin/software/postgresql/12/lib:/home/apankin/software/hdf5/lib:/home/apankin/software/mdsplus/lib:$LD_LIBRARY_PATH

ifort -I${IMAS_PREFIX}/include/ifort -o imas imas.f90 -L${IMAS_PREFIX}/lib -limas-ifort
#gfortran -I${IMAS_PREFIX}/include/gfortran -o imas imas.f90 -L${IMAS_PREFIX}/lib -limas-gfortran
