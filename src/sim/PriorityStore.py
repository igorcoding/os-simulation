from simpy.resources.store import Store


class Heap(object):
    INITIAL_CAPACITY = 4
    INF = float('inf')

    def __init__(self):
        super(Heap, self).__init__()
        self.items = []

    def __len__(self):
        return self.items.__len__()

    def append(self, item):
        self.items.append(item)
        self._sift_up(len(self.items) - 1)

    def pop(self, i=-1):
        if i != 0:
            raise AttributeError('Only popping of the first element is allowed')

        self._swap(0, len(self.items) - 1)
        elem = self.items.pop(-1)
        self._sift_down(0)

        return elem

    def _swap(self, i, j):
        self.items[i], self.items[j] = self.items[j], self.items[i]

    def _sift_up(self, i):
        while i > 0:
            parent = int((i-1) / 2)
            if self.items[i] < self.items[parent]:
                self._swap(i, parent)
                i = parent
            else:
                break

    def _sift_down(self, i):
        size = len(self.items)
        while i < size:
            l = 2 * i + 1
            r = 2 * i + 2

            if l >= size and r >= size:
                break
            elif l < size <= r:
                min_ind = l
            elif r < size <= l:
                min_ind = r
            else:
                min_ind = l if self.items[l] < self.items[r] else r

            if self.items[i] > self.items[min_ind]:
                self._swap(i, min_ind)
                i = min_ind
            else:
                break


class PriorityStore(Store):
    def __init__(self, env, capacity=float('inf')):
        super(PriorityStore, self).__init__(env, capacity)
        self.items = Heap()
