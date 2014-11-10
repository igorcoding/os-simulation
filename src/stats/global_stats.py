import numpy
from src.stats.bulk_stats import BulkStats


class GlobalStats:
    def __init__(self):
        self.bulks = []

    def get_new_bulk_stats(self, **info):
        self.bulks.append(BulkStats(**info))
        return self.bulks[-1]

    def get_avg_total_time_vs_lambda(self):
        return self.get_avg_time_vs_lambda(BulkStats.get_avg_total_time.__name__)

    def get_avg_inner_time_vs_lambda(self):
        return self.get_avg_time_vs_lambda(BulkStats.get_avg_inner_time.__name__)

    def get_avg_time_vs_lambda(self, avg_time_func_name):
        points = []
        for bulk in self.bulks:

            if 'gen_lambda' in bulk.info:
                avg_time = getattr(bulk, avg_time_func_name)()
                gen_lambda = bulk.info['gen_lambda']
                points.append((gen_lambda, avg_time))

            else:
                raise Exception('No lambda to operate with')

        return points


