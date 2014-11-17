import simpy
import pylab

from src.os_simulator import OsSimulator
from src.stats.global_stats import GlobalStats


def experiment(stats, simulation_time, **params):
    env = simpy.Environment()
    simulator = OsSimulator(env, stats, **params)
    simulator.start()

    env.run(until=simulation_time)


def generate_configs(d_range, l_range):
    time_distrib = dict(mu=40, sigma=10)
    delta = 9
    n = 5

    configs = []
    for d in d_range:
        for l in l_range:
            config = dict(delta=delta, buffer_size=n - 1, buffer_latency=d, gen_lambda=l,
                          time_distrib=time_distrib)
            configs.append(config)

    return configs


def main():
    sim_time = 1000
    experiments_per_conf = 10
    d_range = xrange(1, 22, 5)
    l_range = xrange(1, 101)

    results = GlobalStats()

    configs = generate_configs(d_range, l_range)
    for conf in configs:
        bulk_stats = results.get_new_bulk_stats(**conf)
        for _ in xrange(experiments_per_conf):
            stats = bulk_stats.get_new_stats()
            experiment(stats, sim_time, **conf)

    for d in d_range:
        plot_total = results.get_avg_total_time_vs_lambda(d)
        plot_inner = results.get_avg_inner_time_vs_lambda(d)
        plots = [
            dict(title='Average total time vs lambda', file='avg_total.png', points=plot_total),
            dict(title='Average inner time vs lambda', file='avg_inner.png', points=plot_inner),
        ]

        for i, p in enumerate(plots):
            pylab.figure(i)
            pylab.plot(*zip(*p['points']), label='d = %d' % d)

            pylab.legend()
            pylab.xlabel('lambda')
            pylab.ylabel('average time')
            pylab.grid(True)

            pylab.title(p['title'])
            pylab.savefig(p['file'])


if __name__ == "__main__":
    main()