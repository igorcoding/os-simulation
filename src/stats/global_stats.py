import numpy
from src.stats.bulk_stats import BulkStats


class GlobalStats:
    def __init__(self):
        self.bulks = []

    def get_new_bulk_stats(self, **info):
        self.bulks.append(BulkStats(**info))
        return self.bulks[-1]

    def get_avg_total_time_vs_lambda(self, buffer_latency):
        return self.get_avg_time_vs_lambda(BulkStats.get_avg_total_time.__name__, buffer_latency)

    def get_avg_inner_time_vs_lambda(self, buffer_latency):
        return self.get_avg_time_vs_lambda(BulkStats.get_avg_inner_time.__name__, buffer_latency)

    def get_avg_time_vs_lambda(self, avg_time_func_name, buffer_latency):
        points = []
        for bulk in self.bulks:
            if 'buffer_latency' not in bulk.info or 'gen_lambda' not in bulk.info:
                raise Exception('No data to operate with')

            if bulk.info['buffer_latency'] == buffer_latency:
                avg_time = getattr(bulk, avg_time_func_name)()
                gen_lambda = bulk.info['gen_lambda']
                points.append((gen_lambda, avg_time))

        return points


