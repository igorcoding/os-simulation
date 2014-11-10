class Stats(object):
    class TaskEvents:
        STARTED = 'started'
        PROCESSED = 'processed'
        FINISHED = 'finished'
        ENQUEUED = 'enqueued'
        ENTERED_INNER = 'inner'
        BUFFERED = 'buffered'
        UNBUFFERED = 'unbuffered'

    class SystemEvents:
        STARTED = 'started'
        FINISHED = 'finished'

    def __init__(self, **info):
        super(Stats, self).__init__()
        self.tasks_events = {}
        self.system_events = {}
        self.info = info

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

    def get_task_events(self, task_id, event_type):
        if task_id in self.tasks_events:
            events = [e for e in self.tasks_events[task_id] if e['event_type'] == event_type]
            if len(events) == 0:
                return None
            return events


    def started(self, time):
        self._add_system_event(self.SystemEvents.STARTED, time)

    def finished(self, time):
        self._add_system_event(self.SystemEvents.FINISHED, time)

    def started_task(self, task, time):
        self._add_task_event(self.TaskEvents.STARTED, task, time)
        # print "Started task #%d. T = %d; time = %f" % (task.id, task.T, time)

    def processed_task(self, task, time):
        self._add_task_event(self.TaskEvents.PROCESSED, task, time)
        # print "Processed task #%d. T = %d" % (task.id, task.T)

    def finished_task(self, task, time):
        self._add_task_event(self.TaskEvents.FINISHED, task, time)
        # print "Finished task #%d. T = %d" % (task.id, task.T)

    def enqueue_task(self, task, time):
        self._add_task_event(self.TaskEvents.ENQUEUED, task, time)

    def entered_inner_task(self, task, time):
        self._add_task_event(self.TaskEvents.ENTERED_INNER, task, time)

    def buffered_task(self, task, time):
        self._add_task_event(self.TaskEvents.BUFFERED, task, time)
        # print "task #%d in buffer. T = %d" % (task.id, task.T)

    def unbuffered_task(self, task, time):
        self._add_task_event(self.TaskEvents.UNBUFFERED, task, time)
        # print "task #%d is out of buffer. T = %d" % (task.id, task.T)

