import itertools

import numpy

from src.sim.simulation_unit import SimulationUnit
from src.sim.os_logic import Task


class TaskGenerator(SimulationUnit):
    """Generate new tasks"""

    def __init__(self, env, stats, cpu, gen_lambda, time_distrib, tasks_ids=itertools.count()):
        super(TaskGenerator, self).__init__(env, stats)

        self.cpu = cpu
        self.gen_lambda = gen_lambda
        self.time_distrib = time_distrib
        self.tasks_ids = tasks_ids

    def run(self):
        for i in self.tasks_ids:
            yield self.env.timeout(numpy.random.poisson(self.gen_lambda))
            t = int(numpy.random.normal(self.time_distrib['mu'], self.time_distrib['sigma']))
            t = Task(self.env, self.stats, i, t, self.cpu)
            t.start()