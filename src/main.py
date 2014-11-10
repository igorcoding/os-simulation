import simpy

from src.os_simulator import OsSimulator
from src.stats import GlobalStats


def experiment(stats, simulation_time, **params):
    env = simpy.Environment()
    simulator = OsSimulator(env, stats, **params)
    simulator.start()

    env.run(until=simulation_time)


def main():
    gen_lambda = 10
    sim_time = 1000
    time_distrib = dict(mu=40, sigma=10)
    delta = 9
    n = 5
    d = 1

    stats = GlobalStats()
    data1 = dict(delta=delta, buffer_size=n - 1, buffer_latency=d, gen_lambda=gen_lambda,
                 time_distrib=time_distrib, stats=stats.get_new_stats(), simulation_time=sim_time)
    experiment(**data1)
    pass

    # try:
    # while True:
    #         env.step()
    # except EmptySchedule:
    #     pass


if __name__ == "__main__":
    main()