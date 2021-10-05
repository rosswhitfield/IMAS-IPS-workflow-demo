# IPS-IMAS workflow demo

This IPS has 3 components:
 1. [Python IMAS init](IPS/imas_init.py) - creates an initial IMAS file
 1. [Fortran IMAS component](IPS/imas.f90) - does `get_slice`, modifies it and puts it back as a new slice `put_slice`.
      * [IPS wrapper script for component](IPS/imas_worker.py)
 1. [Python display script](IPS/display_imas.py) - load the IMAS file and display it's contents
      * [IPS wrapper script for component](IPS/imas_display.py)

It runs a time loop from 1 to 10.

## Running in Docker

This assumes you have cloned the repos already, since they will just be copied in

```
git clone ssh://git@git.iter.org/imas/access-layer.git
git clone ssh://git@git.iter.org/imas/data-dictionary.git
```

To build docker image

```
docker build . --tag imas
```

To run IPS-IMAS demo in container

```
docker run imas
```

## Running on stellar

First install IPS

```
module load anaconda3/2021.5
python -m pip install ipsframework
```

Build IMAS Fortran component, can use either gfortran or ifort

```
cd IPS
./build-stellar.sh
```

Submit batch script

```
sbatch batch-stellar-intel.sh
```
