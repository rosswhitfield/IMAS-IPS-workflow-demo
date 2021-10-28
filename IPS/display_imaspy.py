#!/usr/bin/env python
import imaspy
import sys
import os

user = sys.argv[1]
tokamak = sys.argv[2]
shot = int(sys.argv[3])
run = int(sys.argv[4])
imas_backend = int(sys.argv[5])

print("Python IMASPy display program")
print(f'tokamak={tokamak} shot={shot} run={run}')

imas_version = os.getenv("IMAS_VERSION")
xml_path = os.getenv("IMAS_PREFIX")+'/include/IDSDef.xml'

ids = imaspy.ids_root.IDSRoot(shot, run,
                              version=imas_version, xml_path=xml_path,
                              backend_version=imas_version, backend_xml_path=xml_path)
ids.open_env_backend(user, tokamak, imas_version, imas_backend, ual_version=imas_version)

assert ids.connected

core_profiles = ids.core_profiles
core_profiles.get()

print(core_profiles.time)
print(core_profiles.global_quantities.ip)
for profile_1d in core_profiles.profiles_1d:
    print(profile_1d.time.value, profile_1d.grid.rho_tor_norm)

ids.close()
print("Program completed")
