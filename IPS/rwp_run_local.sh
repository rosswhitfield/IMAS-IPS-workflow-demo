#!/bin/bash
export IMAS_PREFIX=/home/rwp/src/IMAS/access-layer
export IMAS_VERSION=3.33.0
export LD_LIBRARY_PATH=/home/rwp/src/IMAS/access-layer/lib

gfortran -I${IMAS_PREFIX}/fortraninterface/gfortran -o imas imas.f90 -L${IMAS_PREFIX}/fortraninterface -limas-gfortran

ips.py --config=ips.imas.config --platform=platform.conf
