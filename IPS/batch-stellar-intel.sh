#!/bin/bash
#SBATCH -N 1
#SBATCH -n 96
#SBATCH --time=00:05:00
#SBATCH --job-name=ips-imas
#SBATCH --output=ips-imas.log
#SBATCH -p stellar-debug
#SBATCH -A pppl

module load matlab/R2021a
module load anaconda3/2021.5
module load intel-mkl/2020.1
module load intel/19.1.1.217

export IMAS_PREFIX=/home/apankin/software/AL.3_33
export IMAS_VERSION=3.33.0

export PYTHONPATH=/home/apankin/software/AL.3_33/python/lib
export LD_LIBRARY_PATH=/home/apankin/software/AL.3_33/lib:/home/apankin/software/postgresql/12/lib:/home/apankin/software/hdf5/lib:/home/apankin/software/mdsplus/lib:$LD_LIBRARY_PATH

ips.py --config=ips.imas.config --platform=stellar.intel.conf
