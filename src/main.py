import itertools
import numpy
import simpy
from simpy.core import EmptySchedule
from simpy.resources.resource import PriorityResource, PriorityRequest

LAMBDA = 10
SIM_TIME = 1000
T_PROB_LAW = dict(mu=40, sigma=10)
DELTA = 9
N = 5
D = 1


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

            yield self.env.process(self.process())

            if not self.processed():
                yield self.env.process(self.cpu.add_to_buffer(self))
                self.env.exit()

    def process(self):
        yield self.env.timeout(DELTA)
        self.T -= DELTA
        print "Processed task #%d. T = %d" % (self.id, self.T)

    def processed(self):
        return self.T <= 0


class CPU(object):
    def __init__(self, env, buffer_size):

        """

        :param env:
         :type env: simpy.Environment
        """
        super(CPU, self).__init__()
        self.env = env
        self.cpu_obj = simpy.PriorityResource(env, capacity=1)

        self.queue = simpy.Store(env)  # external queue

        self.buffer = simpy.Store(env, buffer_size)  # internal queue # TODO: make it a priority queue
        self.buffer_filled = env.event()

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

                task = yield self.buffer.get()
                print "task #%d is out of buffer. T = %d" % (task.id, task.T)

                yield self.env.process(task.process())

                if not task.processed():
                    yield self.env.process(self.add_to_buffer(task))


    def add_to_buffer(self, task):
        task.env = self.env
        with self.buffer.put(task) as req:
            yield req
            print "task #%d in buffer. T = %d" % (task.id, task.T)

            if len(self.buffer.items) == self.buffer.capacity:
                self.buffer_filled.succeed()

    # def get_from_buffer(self):
    #
    #     yield task



def task_generator(env, cpu, count=itertools.count()):
    """Generate new tasks"""
    for i in count:
        yield env.timeout(numpy.random.poisson(LAMBDA))
        t = int(numpy.random.normal(T_PROB_LAW['mu'], T_PROB_LAW['sigma']))
        t = Task(env, i, t, cpu)
        t.start()


def main():
    env = simpy.Environment()
    cpu = CPU(env, N-1)
    # env.process(task_generator(env, cpu, range(1, 6)))
    env.process(task_generator(env, cpu))

    env.run(until=SIM_TIME)
    # try:
    #     while True:
    #         env.step()
    # except EmptySchedule:
    #     print len(cpu.buffer.items)


if __name__ == "__main__":
    main()