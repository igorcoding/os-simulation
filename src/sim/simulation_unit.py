class SimulationUnit(object):
    def __init__(self, env, stats):
        super(SimulationUnit, self).__init__()
        self.env = env
        self.stats = stats

        self.action = None

    def start(self):
        self.action = self.env.process(self.run())

    def run(self):
        raise Exception("Bare simulation unit cannot be run")