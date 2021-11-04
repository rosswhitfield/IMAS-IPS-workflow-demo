#!/bin/bash
#SBATCH -N 1
#SBATCH --time=00:05:00
#SBATCH --job-name=ips-imas
#SBATCH --output=ips-imas.log
#SBATCH -p debug
#SBATCH -C haswell

module load cray-hdf5/1.12.0.0
module load python
module load gcc

export IMAS_PREFIX=$HOME/IMAS
export IMAS_VERSION=3.34.0
export PYTHONPATH=$IMAS_PREFIX/python/lib
export LD_LIBRARY_PATH=$IMAS_PREFIX/lib:$LD_LIBRARY_PATH
export HDF5_USE_FILE_LOCKING=FALSE

ips.py --config=ips.imas.config --platform=cori.haswell.conf
