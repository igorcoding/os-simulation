import simpy
from simpy.resources.resource import PriorityRequest

from src.PriorityStore import PriorityStore
from src.simulation_unit import SimulationUnit


class Task(SimulationUnit):
    # noinspection PyPep8Naming
    def __init__(self, env, stats, task_id, T, cpu):
        """

        :type env: simpy.Environment
        :type cpu: CPU
        """
        super(Task, self).__init__(env, stats)
        self.id = task_id
        self.T = T
        self.cpu = cpu

    def start(self):
        super(Task, self).start()
        self.stats.started_task(self, self.env.now)

    def run(self):
        with PriorityRequest(self.cpu.cpu_obj, priority=1) as cpu_obj:
            yield cpu_obj
            print 'externally captured cpu_obj'

            yield self.env.process(self.execute())

    def execute(self):
        yield self.env.process(self.process())

        if not self.processed():
            yield self.env.process(self.cpu.add_to_buffer(self))
            self.env.exit()
        else:
            self.finish()

    def process(self):
        yield self.env.timeout(self.cpu.delta)
        self.T -= self.cpu.delta
        self.stats.processed_task(self, self.env.now)

    def finish(self):
        self.stats.finished_task(self, self.env.now)

    def processed(self):
        return self.T <= 0

    def __lt__(self, other):
        return self.T < other.T


class CPU(SimulationUnit):
    def __init__(self, env, stats, delta, buffer_size, buffer_latency):
        """
        :param env:
        :type env: simpy.Environment
        """
        super(CPU, self).__init__(env, stats)
        self.cpu_obj = simpy.PriorityResource(env, capacity=1)

        self.delta = delta

        self.buffer = PriorityStore(env, buffer_size)  # internal queue
        self.buffer_filled = env.event()

        self.buffer_latency = buffer_latency

    def run(self):
        while True:
            print 'Waiting buffer to fill'
            yield self.buffer_filled
            self.buffer_filled = self.env.event()
            print 'Buffer filled'

            with PriorityRequest(self.cpu_obj, priority=0) as req:
                yield req
                print 'captured cpu_obj'

                task = yield self.env.process(self.get_from_buffer())

                yield self.env.process(task.execute())

    def add_to_buffer(self, task):
        task.env = self.env
        with self.buffer.put(task) as req:
            yield req
            yield self.env.timeout(self.buffer_latency)
            self.stats.buffered_task(task, self.env.now)

            if len(self.buffer.items) == self.buffer.capacity:
                self.buffer_filled.succeed()

    def get_from_buffer(self):
        task = yield self.buffer.get()
        yield self.env.timeout(self.buffer_latency)

        self.stats.unbuffered_task(task, self.env.now)
        self.env.exit(task)







