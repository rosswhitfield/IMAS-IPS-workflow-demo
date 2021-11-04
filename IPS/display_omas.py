#!/usr/bin/env python
import omas
import sys

user = sys.argv[1]
tokamak = sys.argv[2]
shot = int(sys.argv[3])
run = int(sys.argv[4])

print("Python OMAS display program")
print(f'tokamak={tokamak} shot={shot} run={run}')

# hack to change IMAS backend to HDF5
omas.omas_imas.imas_open.__defaults__ = ({}, False, '3', 'HDF5', True)

ods = omas.load_omas_imas(user=user,
                          machine=tokamak,
                          pulse=shot,
                          run=run,
                          paths=['core_profiles'])

core_profiles = ods['core_profiles']

print(core_profiles['time'])
print(core_profiles['global_quantities.ip'])
for n in core_profiles['profiles_1d']:
    print(core_profiles['profiles_1d'][n]['time'], core_profiles['profiles_1d'][n]['grid']['rho_tor_norm'])

print("Program completed")
