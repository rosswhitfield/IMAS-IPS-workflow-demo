from ipsframework import Component
import shutil


class imas_worker(Component):
    def init(self, timestamp=0.0, **keywords):
        self.cwd = self.services.get_working_dir()
        self.tokamak = self.services.get_config_param('TOKAMAK_ID')
        self.shot = int(self.services.get_config_param('SHOT_NUMBER'))
        self.run = int(self.services.get_config_param('RUN_ID'))
        self.imas_backend = int(self.services.get_config_param('IMAS_BACKEND'))

    def step(self, timestamp=0.0, **keywords):
        self.stage_and_unpack_state()

        retval = self.services.wait_task(self.services.launch_task(1,
                                                                   self.cwd,
                                                                   self.IMAS_EXE,
                                                                   self.cwd,
                                                                   self.tokamak,
                                                                   self.shot,
                                                                   self.run,
                                                                   self.imas_backend,
                                                                   timestamp))

        if retval != 0:
            raise RuntimeError(f"Error running {self.IMAS_EXE}")

        """
        imas_obj = imas.ids(self.shot, self.run)
        imas_obj.open_env_backend(self.cwd, self.tokamak, '3', self.imas_backend)

        if not imas_obj.isConnected():
            raise RuntimeError('open failed')

        core_profiles = imas_obj.core_profiles
        core_profiles.getSlice(timestamp, imas.imasdef.CLOSEST_INTERP)

        core_profiles.profiles_1d[0].grid.rho_tor_norm = core_profiles.profiles_1d[0].grid.rho_tor_norm + timestamp
        core_profiles.profiles_1d[0].time = timestamp

        core_profiles.global_quantities.ip[0] = core_profiles.global_quantities.ip[0] + timestamp
        core_profiles.time[0] = timestamp

        core_profiles.putSlice()
        imas_obj.close()
        """

        self.archive_and_update_state()

    def checkpoint(self, timestamp=0.0, **keywords):
        self.services.save_restart_files(timestamp, self.RESTART_FILES)

    def archive_and_update_state(self):
        shutil.make_archive(f'{self.tokamak}_{self.shot}_{self.run}', 'zip', '.', self.tokamak)
        self.services.update_state()

    def stage_and_unpack_state(self):
        self.services.stage_state()
        shutil.unpack_archive(f'{self.tokamak}_{self.shot}_{self.run}.zip')
