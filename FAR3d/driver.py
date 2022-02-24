from ipsframework import Component


class driver(Component):
    def step(self, timestamp=0.0):
        imas_display_worker = self.services.get_port('IMAS')
        far3d_worker = self.services.get_port('FAR3D')

        self.services.call(imas_display_worker, 'step', 0)

        self.services.call(far3d_worker, 'step', 0)
