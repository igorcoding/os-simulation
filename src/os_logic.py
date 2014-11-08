import itertools
import numpy
import simpy
from simpy.resources.resource import PriorityRequest
from src.PriorityStore import PriorityStore


class Task(object):
    # noinspection PyPep8Naming
    def __init__(self, env, task_id, T, cpu):
        """

        :type env: simpy.Environment
        :type cpu: CPU
        """
        super(Task, self).__init__()
        self.env = env
        self.id = task_id
        self.T = T
        self.cpu = cpu

        self.action = None

    def start(self):
        self.action = self.env.process(self.run())
        print "Started task #%d. T = %d" % (self.id, self.T)

    def run(self):
        with PriorityRequest(self.cpu.cpu_obj, priority=1) as cpu_obj:
            yield cpu_obj
            print 'externally captured cpu_obj'

            yield self.env.process(self.process())

            if not self.processed():
                yield self.env.process(self.cpu.add_to_buffer(self))
                self.env.exit()
            else:
                print "Finished task #%d. T = %d" % (self.id, self.T)

    def process(self):
        yield self.env.timeout(self.cpu.delta)
        self.T -= self.cpu.delta
        print "Processed task #%d. T = %d" % (self.id, self.T)

    def processed(self):
        return self.T <= 0

    def __lt__(self, other):
        return self.T < other.T


class CPU(object):
    def __init__(self, env, delta, buffer_size, buffer_latency):

        """

        :param env:
         :type env: simpy.Environment
        """
        super(CPU, self).__init__()
        self.env = env
        self.cpu_obj = simpy.PriorityResource(env, capacity=1)

        self.delta = delta

        self.buffer = PriorityStore(env, buffer_size)  # internal queue
        self.buffer_filled = env.event()

        self.buffer_latency = buffer_latency

        self.action = env.process(self.run())

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

                yield self.env.process(task.process())

                if not task.processed():
                    yield self.env.process(self.add_to_buffer(task))
                else:
                    print "Finished task #%d. T = %d" % (task.id, task.T)

    def add_to_buffer(self, task):
        task.env = self.env
        with self.buffer.put(task) as req:
            yield req
            yield self.env.timeout(self.buffer_latency)
            print "task #%d in buffer. T = %d" % (task.id, task.T)

            if len(self.buffer.items) == self.buffer.capacity:
                self.buffer_filled.succeed()

    def get_from_buffer(self):
        task = yield self.buffer.get()
        print "task #%d is out of buffer. T = %d" % (task.id, task.T)
        yield self.env.timeout(self.buffer_latency)

        self.env.exit(task)


def task_generator(env, cpu, gen_lambda, t_prob_law, count=itertools.count()):
    """Generate new tasks"""
    for i in count:
        yield env.timeout(numpy.random.poisson(gen_lambda))
        t = int(numpy.random.normal(t_prob_law['mu'], t_prob_law['sigma']))
        t = Task(env, i, t, cpu)
        t.start()

