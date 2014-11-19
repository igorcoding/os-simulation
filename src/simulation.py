import simpy
import pylab

from src.sim.os_simulator import OsSimulator
from src.stats.global_stats import GlobalStats


def experiment(stats, simulation_time, **params):
    env = simpy.Environment()
    simulator = OsSimulator(env, stats, **params)
    simulator.start()

    env.run(until=simulation_time)


def generate_configs(data):
    configs = []
    for d in data['buffer_latency']:
        for l in data['gen_lambda']:
            config = dict(delta=data['delta'], buffer_size=data['buffer_size'] - 1, buffer_latency=d,
                          gen_lambda=l, time_distrib=data['time_distrib'])
            configs.append(config)

    return configs


def simulation(**data):
    results = GlobalStats()

    configs = generate_configs(data)
    for conf in configs:
        bulk_stats = results.get_new_bulk_stats(**conf)
        for _ in xrange(data['exp_per_conf']):
            stats = bulk_stats.get_new_stats()
            experiment(stats, data['sim_time'], **conf)

    for d in data['buffer_latency']:
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
    simulation(**data)


if __name__ == "__main__":
    main()