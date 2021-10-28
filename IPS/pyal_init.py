from ipsframework import Component
import pyal
import numpy as np
import datetime
import shutil


class imas_init(Component):
    def init(self, timestamp=0.0, **keywords):
        self.cwd = self.services.get_working_dir()
        self.tokamak = self.services.get_config_param('TOKAMAK_ID')
        self.shot = int(self.services.get_config_param('SHOT_NUMBER'))
        self.run = int(self.services.get_config_param('RUN_ID'))
        self.imas_backend = int(self.services.get_config_param('IMAS_BACKEND'))

    def step(self, timestamp=0.0, **keywords):
        client = pyal.Client.create(self.shot, self.run, self.cwd, self.tokamak, '3', self.imas_backend)
        assert client.connected

        core_profiles = pyal.new_al_cpo("core_profiles")
        core_profiles.ids_properties.homogeneous_time = 1
        core_profiles.ids_properties.comment = 'This is a IPS test'
        core_profiles.ids_properties.creation_date = datetime.datetime.now().isoformat()

        core_profiles.time.resize(1)
        core_profiles.time[0] = 0.
        core_profiles.global_quantities.ip.resize(1)
        core_profiles.global_quantities.ip[0] = 0.

        core_profiles.profiles_1d.resize(1)

        core_profiles.profiles_1d[0].grid.rho_tor_norm = np.array([0, 1, 2])
        core_profiles.profiles_1d[0].time = 0.0

        client.put(core_profiles)

        client.close()

        self.archive_and_update_state()

    def archive_and_update_state(self):
        shutil.make_archive(f'{self.tokamak}_{self.shot}_{self.run}', 'zip', '.', self.tokamak)
        self.services.update_state()
