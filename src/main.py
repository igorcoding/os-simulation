import simpy
import pylab

from src.os_simulator import OsSimulator
from src.stats.global_stats import GlobalStats


def experiment(stats, simulation_time, **params):
    env = simpy.Environment()
    simulator = OsSimulator(env, stats, **params)
    simulator.start()

    env.run(until=simulation_time)


def main():
    # gen_lambda = 10
    sim_time = 1000
    time_distrib = dict(mu=40, sigma=10)
    delta = 9
    n = 5
    # d = 1

    experiments_count = 10

    for d in xrange(1, 22, 5):
        print d
        results = GlobalStats()

        for l in xrange(1, 101):
            bulk_stats = results.get_new_bulk_stats(gen_lambda=l)

            for _ in xrange(experiments_count):
                stats = bulk_stats.get_new_stats()
                data = dict(delta=delta, buffer_size=n - 1, buffer_latency=d, gen_lambda=l,
                            time_distrib=time_distrib, stats=stats, simulation_time=sim_time)
                experiment(**data)

        plot_total = results.get_avg_total_time_vs_lambda()
        plot_inner = results.get_avg_inner_time_vs_lambda()

        pylab.figure(1)
        pylab.plot(*zip(*plot_total), label='d = %d' % d)

        pylab.figure(2)
        pylab.plot(*zip(*plot_inner), label='d = %d' % d)

    for i in [1, 2]:
        pylab.figure(i)
        pylab.legend()
        pylab.xlabel('lambda')
        pylab.ylabel('average time')
        pylab.grid(True)

    pylab.figure(1)
    pylab.title('Average total time vs lambda')
    pylab.savefig("avg_total.png")

    pylab.figure(2)
    pylab.title('Average inner time vs lambda')
    pylab.savefig("avg_inner.png")
        # pylab.show()

    pass

    # try:
    # while True:
    #         env.step()
    # except EmptySchedule:
    #     pass


if __name__ == "__main__":
    main()