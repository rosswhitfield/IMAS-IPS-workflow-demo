from ipsframework import Component
import shutil
import os


class far3d_worker(Component):
    def step(self, timestamp=0.0, **keywords):
        self.tokamak = self.services.get_config_param('TOKAMAK_ID')
        self.shot = int(self.services.get_config_param('SHOT_NUMBER'))
        self.run = int(self.services.get_config_param('RUN_ID'))

        self.stage_and_unpack_state()
        self.services.stage_input_files(self.INPUT_FILES)

        cwd = self.services.get_working_dir()
        os.environ['USER'] = cwd

        task_id = self.services.launch_task(self.NPROC, cwd, self.FAR3D_EXE)
        retcode = self.services.wait_task(task_id)

        if retcode != 0:
            msg = f'Error executing {self.FAR3D_EXE}'
            self.services.error(msg)
            raise Exception(msg)

        self.services.stage_output_files(timestamp, self.OUTPUT_FILES)

    def archive_and_update_state(self):
        shutil.make_archive(f'{self.tokamak}_{self.shot}_{self.run}', 'zip', '.', self.tokamak)
        self.services.update_state()

    def stage_and_unpack_state(self):
        self.services.stage_state()
        shutil.unpack_archive(f'{self.tokamak}_{self.shot}_{self.run}.zip')
