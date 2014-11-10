from src.os_logic import CPU
from src.simulation_unit import SimulationUnit
from src.task_generator import TaskGenerator


class OsSimulator(SimulationUnit):
    def __init__(self, env, stats, **params):
        super(OsSimulator, self).__init__(env, stats)
        self.delta = params['delta']
        self.buffer_size = params['buffer_size']
        self.buffer_latency = params['buffer_latency']
        self.gen_lambda = params['gen_lambda']
        self.time_distrib = params['time_distrib']

    def start(self):
        cpu = CPU(self.env, self.stats, self.delta, self.buffer_size, self.buffer_latency)
        task_gen = TaskGenerator(self.env, self.stats, cpu, self.gen_lambda, self.time_distrib)

        cpu.start()
        task_gen.start()