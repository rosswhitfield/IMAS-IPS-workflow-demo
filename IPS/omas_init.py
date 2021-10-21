from ipsframework import Component
import omas
import datetime
import shutil


class omas_init(Component):
    def init(self, timestamp=0.0, **keywords):
        self.cwd = self.services.get_working_dir()
        self.tokamak = self.services.get_config_param('TOKAMAK_ID')
        self.shot = int(self.services.get_config_param('SHOT_NUMBER'))
        self.run = int(self.services.get_config_param('RUN_ID'))
        self.imas_backend = int(self.services.get_config_param('IMAS_BACKEND'))

    def step(self, timestamp=0.0, **keywords):
        ods = omas.ODS()

        ods['core_profiles.ids_properties.homogeneous_time'] = 1
        ods['core_profiles.ids_properties.comment'] = 'This is a IPS test'
        ods['core_profiles.ids_properties.creation_date'] = datetime.datetime.now().isoformat()

        ods['core_profiles.time'] = [0.]
        ods['core_profiles.global_quantities.ip'] = [0.]

        ods['core_profiles.profiles_1d[0].grid.rho_tor_norm'] = [0, 1, 2]
        ods['core_profiles.profiles_1d[0].time'] = 0.0

        # hack to change IMAS backend to HDF5
        omas.omas_imas.imas_open.__defaults__ = ({}, False, '3', 'HDF5', True)

        omas.save_omas_imas(ods,
                            user=self.cwd,
                            machine=self.tokamak,
                            pulse=self.shot,
                            run=self.run,
                            new=True)

        self.archive_and_update_state()

    def archive_and_update_state(self):
        shutil.make_archive(f'{self.tokamak}_{self.shot}_{self.run}', 'zip', '.', self.tokamak)
        self.services.update_state()
