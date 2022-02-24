from ipsframework import Component
import shutil


class imas_worker(Component):
    def step(self, timestamp=0.0, **keywords):
        cwd = self.services.get_working_dir()
        self.tokamak = self.services.get_config_param('TOKAMAK_ID')
        self.shot = int(self.services.get_config_param('SHOT_NUMBER'))
        self.run = int(self.services.get_config_param('RUN_ID'))

        self.services.stage_input_files(self.INPUT_FILES)
        shutil.unpack_archive(f'{self.tokamak}_{self.shot}_{self.run}.zip')

        retval = self.services.wait_task(self.services.launch_task(1,
                                                                   cwd,
                                                                   self.IMAS_DISPLAY_EXE,
                                                                   cwd,
                                                                   self.tokamak,
                                                                   self.shot,
                                                                   self.run,
                                                                   timestamp))

        if retval != 0:
            raise RuntimeError(f"Error running {self.IMAS_DISPLAY_EXE}")

        self.archive_and_update_state()

    def stage_and_unpack_state(self):
        self.services.stage_state()
        shutil.unpack_archive(f'{self.tokamak}_{self.shot}_{self.run}.zip')

    def archive_and_update_state(self):
        shutil.make_archive(f'{self.tokamak}_{self.shot}_{self.run}', 'zip', '.', self.tokamak)
        self.services.update_state()

