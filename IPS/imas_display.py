from ipsframework import Component
import shutil


class imas_display(Component):
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
                                                                   self.IMAS_DISPLAY_EXE,
                                                                   self.cwd,
                                                                   self.tokamak,
                                                                   self.shot,
                                                                   self.run,
                                                                   self.imas_backend,
                                                                   timestamp))

        if retval != 0:
            raise RuntimeError(f"Error running {self.IMAS_DISPLAY_EXE}")

    def stage_and_unpack_state(self):
        self.services.stage_state()
        shutil.unpack_archive(f'{self.tokamak}_{self.shot}_{self.run}.zip')
