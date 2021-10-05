#!/usr/bin/env python
import imas
import sys

user = sys.argv[1]
tokamak = sys.argv[2]
shot = int(sys.argv[3])
run = int(sys.argv[4])
imas_baskend = int(sys.argv[5])

print("Python IMAS display program")
print(f'tokamak={tokamak} shot={shot} run={run}')

imas_obj = imas.ids(shot, run)
imas_obj.open_env_backend(user, tokamak, '3', imas_baskend)

if not imas_obj.isConnected():
    raise RuntimeError('open failed')

core_profiles = imas_obj.core_profiles
core_profiles.get()

print(core_profiles.time)
print(core_profiles.global_quantities.ip)
for i in range(len(core_profiles.profiles_1d)):
    print(core_profiles.profiles_1d[i].time, core_profiles.profiles_1d[i].grid.rho_tor_norm)

imas_obj.close()
print("Program completed")
