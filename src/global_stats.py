import numpy
from src.stats import Stats


class GlobalStats:
    def __init__(self):
        self.bulks = []

    def get_new_bulk_stats(self, **info):
        self.bulks.append(BulkStats(**info))
        return self.bulks[-1]

    def get_avg_total_time_vs_lambda(self):
        points = []
        for bulk in self.bulks:

            if 'gen_lambda' in bulk.info:
                avg_time = bulk.get_avg_total_time()
                gen_lambda = bulk.info['gen_lambda']
                points.append((gen_lambda, avg_time))

            else:
                raise Exception('No lambda to operate with')

        return points


class BulkStats:
    def __init__(self, **info):
        self._experiments = []
        self.info = info

    def get_new_stats(self):
        self._experiments.append(Stats())
        return self._experiments[-1]

    def get_stats_at(self, experiment_id):
        return self._experiments[experiment_id]

    def get_avg_total_time(self):
        total_avg_time = 0.0
        exp_count = 0
        for exp in self._experiments:
            exp_has_data = False

            avg_time = 0.0
            count = 0
            for task_id in exp.tasks_events:
                enqueue_events = exp.get_task_events(task_id, Stats.TaskEvents.ENQUEUED)
                finish_events = exp.get_task_events(task_id, Stats.TaskEvents.FINISHED)

                if enqueue_events is not None and finish_events is not None:
                    enqueue_time = enqueue_events[0]['time']
                    finish_time = finish_events[0]['time']
                    time_spent = finish_time - enqueue_time

                    avg_time += time_spent
                    count += 1
                    exp_has_data = True

            if exp_has_data:
                total_avg_time += avg_time
                exp_count += 1

        total_avg_time /= exp_count
        return total_avg_time