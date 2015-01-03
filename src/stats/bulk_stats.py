from src.stats.stats import Stats


class BulkStats(object):
    TRACKING_EVENTS = [Stats.TaskEvents.ENQUEUED, Stats.TaskEvents.FINISHED,
                       Stats.TaskEvents.ENTERED_INNER, Stats.TaskEvents.FINISHED]

    def __init__(self, **info):
        super(BulkStats, self).__init__()
        self.experiments = []
        self.info = info

    def __del__(self):
        # print 'BulkStats.__del__'

        del self.experiments

    def get_new_stats(self):
        self.experiments.append(Stats(tracking_events=self.TRACKING_EVENTS))
        return self.experiments[-1]

    def get_stats_at(self, experiment_id):
        return self.experiments[experiment_id]

    def get_avg_total_time(self):
        return self.get_avg_time(Stats.TaskEvents.ENQUEUED, Stats.TaskEvents.FINISHED)

    def get_avg_inner_time(self):
        return self.get_avg_time(Stats.TaskEvents.ENTERED_INNER, Stats.TaskEvents.FINISHED)

    def get_avg_time(self, first_time_event, second_time_event):
        total_avg_time = 0.0
        exp_count = 0
        for exp in self.experiments:
            exp_has_data = False

            avg_time = 0.0
            count = 0
            for task_id in exp.tasks_events:
                enqueue_events = exp.get_task_events(task_id, first_time_event)
                finish_events = exp.get_task_events(task_id, second_time_event)

                if enqueue_events is not None and finish_events is not None:
                    enqueue_time = enqueue_events[0]['time']
                    finish_time = finish_events[0]['time']
                    time_spent = finish_time - enqueue_time

                    avg_time += time_spent
                    count += 1
                    exp_has_data = True

            if exp_has_data:
                avg_time /= count
                total_avg_time += avg_time
                exp_count += 1

        if exp_count != 0:
            total_avg_time /= exp_count
            return total_avg_time
        return 0