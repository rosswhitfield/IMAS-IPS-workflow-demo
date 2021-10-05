from ipsframework import Component


class driver(Component):
    def step(self, timestamp=0.0):
        ports = [self.services.get_port('IMAS'), self.services.get_port('IMAS_DISPLAY')]

        timeloop = self.services.get_time_loop()

        for port in ports:
            self.services.call(port, 'init', 0)

        # show starting IMAS, after INIT
        self.services.call(ports[1], 'step', 0)

        for t in timeloop:
            self.services.update_time_stamp(t)
            for port in ports:
                self.services.call(port, 'step', t)
                self.services.call(port, 'checkpoint', t)
