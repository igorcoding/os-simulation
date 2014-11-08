import simpy
from src.os_logic import CPU, task_generator

LAMBDA = 10
SIM_TIME = 1000
T_PROB_LAW = dict(mu=40, sigma=10)
DELTA = 9
N = 5
D = 1


def experiment(**params):
    env = simpy.Environment()
    cpu = CPU(env, params['DELTA'], params['N'], params['D'])
    env.process(task_generator(env, cpu, params['LAMBDA'], params['T_PROB_LAW']))

    env.run(until=SIM_TIME)


def main():
    data1 = dict(DELTA=DELTA, N=N-1, D=D, LAMBDA=LAMBDA, T_PROB_LAW=T_PROB_LAW)
    experiment(**data1)
    # try:
    #     while True:
    #         env.step()
    # except EmptySchedule:
    #     print len(cpu.buffer.items)


if __name__ == "__main__":
    main()