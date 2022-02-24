#!/bin/bash
#SBATCH -N 1
#SBATCH -n 96
#SBATCH --time=00:05:00
#SBATCH --job-name=ips-far3d
#SBATCH --output=ips-far3d.log
#SBATCH -p stellar-debug
#SBATCH -A pppl

module load anaconda3/2021.5
module load intel/2021.1.2
module load openmpi/intel-2021.1/4.1.0
module load fftw/intel-2021.1/openmpi-4.1.0/3.3.9
module load hdf5/intel-2021.1/openmpi-4.1.0/1.10.6
module load netcdf/intel-2021.1/hdf5-1.10.6/openmpi-4.1.0/4.7.4

export IMAS_PREFIX=/home/rw4086/IMAS_3.34
export LD_LIBRARY_PATH=$IMAS_PREFIX/lib:$LD_LIBRARY_PATH
export IMAS_VERSION=3.34.0
export PYTHONPATH=$IMAS_PREFIX/python/lib

export HDF5_DISABLE_VERSION_CHECK=1

ips.py --config=ips.far3d.config --platform=stellar.intel.conf
