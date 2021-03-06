# coding=utf-8
import simpy
import pylab

from src.sim.os_simulator import OsSimulator
from src.stats.global_stats import GlobalStats


class Simulation(object):
    def __init__(self):
        super(Simulation, self).__init__()

    @staticmethod
    def _experiment(stats, simulation_time, **params):
        env = simpy.Environment()
        simulator = OsSimulator(env, stats, **params)
        simulator.start()

        env.run(until=simulation_time)
        del simulator

    @staticmethod
    def _generate_configs(data):
        configs = []
        for d in data['buffer_latency']:
            for l in data['gen_lambda']:
                config = dict(delta=data['delta'], buffer_size=data['buffer_size'] - 1, buffer_latency=d,
                              gen_lambda=l, time_distrib=data['time_distrib'])
                configs.append(config)

        return configs

    def simulation(self, **data):
        results = GlobalStats()

        configs = self._generate_configs(data)
        for i, conf in enumerate(configs):
            print "Running configuration %d/%d" % (i+1, len(configs))
            bulk_stats = results.get_new_bulk_stats(**conf)
            for j in xrange(data['exp_per_conf']):
                print "%d/%d" % (j+1, data['exp_per_conf']),
                stats = bulk_stats.get_new_stats()
                self._experiment(stats, data['sim_time'], **conf)
            print

        pylab.matplotlib.rc('font', family='Arial')
        pylab.clf()
        for d in data['buffer_latency']:
            plot_total = results.get_avg_total_time_vs_lambda(d)
            plot_inner = results.get_avg_inner_time_vs_lambda(d)
            plots = [
                dict(title=u'Среднее общее время пребывания задания (внешняя очередь + система)', file='avg_total.png', points=plot_total),
                dict(title=u'Среднее время пребывания задания в системе', file='avg_inner.png', points=plot_inner),
            ]

            for i, p in enumerate(plots):
                pylab.figure(i)
                pylab.plot(*zip(*p['points']), label='d = %d' % d)

                pylab.legend()
                pylab.xlabel(u'λ')
                pylab.ylabel(u'Время')
                pylab.grid(True)

                pylab.title(p['title'])
                pylab.savefig(p['file'])
        pylab.close()
        del results


def main():
    data = {
        'sim_time': 1000,
        'exp_per_conf': 1,
        'buffer_latency': xrange(1, 22, 5),
        'gen_lambda': xrange(1, 101),
        'buffer_size': 5,
        'delta': 9,
        'time_distrib': dict(mu=40, sigma=10)
    }
    s = Simulation()
    s.simulation(**data)


if __name__ == "__main__":
    main()