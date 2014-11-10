class GlobalStats:
    def __init__(self):
        self._stats = {}
        self.current_experiment = -1

    def get_new_stats(self):
        self.current_experiment += 1
        self._stats[self.current_experiment] = Stats()
        return self._stats[self.current_experiment]

    def get_stats_at(self, experiment_id):
        return self._stats[experiment_id]


class Stats:

    class TaskEventTypes:
        STARTED = 'started'
        PROCESSED = 'processed'
        FINISHED = 'finished'
        ENQUEUED = 'enqueued'
        BUFFERED = 'buffered'
        UNBUFFERED = 'unbuffered'

    class SystemEventTypes:
        STARTED = 'started'
        FINISHED = 'finished'

    def __init__(self):
        self.tasks_events = {}
        self.system_events = {}

    def _add_task_event(self, event_type, task, time):
        if task.id not in self.tasks_events:
            self.tasks_events[task.id] = []
        self.tasks_events[task.id].append({
            'event_type': event_type,
            'task': task,
            'time': time
        })

    def _add_system_event(self, event_type, time):
        if event_type not in self.tasks_events:
            self.tasks_events[event_type] = []
        self.tasks_events[event_type].append({
            'time': time
        })

    def started(self, time):
        self._add_system_event(self.SystemEventTypes.STARTED, time)

    def finished(self, time):
        self._add_system_event(self.SystemEventTypes.FINISHED, time)

    def started_task(self, task, time):
        self._add_task_event(self.TaskEventTypes.STARTED, task, time)
        print "Started task #%d. T = %d; time = %f" % (task.id, task.T, time)

    def processed_task(self, task, time):
        self._add_task_event(self.TaskEventTypes.PROCESSED, task, time)
        print "Processed task #%d. T = %d" % (task.id, task.T)

    def finished_task(self, task, time):
        self._add_task_event(self.TaskEventTypes.FINISHED, task, time)
        print "Finished task #%d. T = %d" % (task.id, task.T)

    def enqueue_task(self, task, time):
        self._add_task_event(self.TaskEventTypes.ENQUEUED, task, time)

    def buffered_task(self, task, time):
        self._add_task_event(self.TaskEventTypes.BUFFERED, task, time)
        print "task #%d in buffer. T = %d" % (task.id, task.T)

    def unbuffered_task(self, task, time):
        self._add_task_event(self.TaskEventTypes.UNBUFFERED, task, time)
        print "task #%d is out of buffer. T = %d" % (task.id, task.T)

