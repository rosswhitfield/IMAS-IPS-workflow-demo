#!/usr/bin/env python
from omfit_classes.omfit_osborne import OMFITpFile
from omfit_classes.omfit_eqdsk import OMFITgeqdsk
import omas
import os

# hack to change IMAS backend to HDF5
omas.omas_imas.imas_open.__defaults__ = ({}, False, '3', 'HDF5', True)

pulse = 1
run = 1

eq = OMFITgeqdsk(f'g{pulse}.{run:05}')
pfile = OMFITpFile(f'p{pulse}.{run:05}')
ods = pfile.to_omas(gEQDSK=eq)

omas.save_omas_imas(ods, user=os.getcwd(), machine='d3d', pulse=pulse, run=run, new=True)
