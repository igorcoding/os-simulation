from unittest import TestCase

from src.sim.PriorityStore import Heap


class TestHeap(TestCase):
    def setUp(self):
        self.heap = Heap()

    def test_append_sequential(self):
        items = [1, 2, 3, 4, 5, 6]
        for i in items:
            self.heap.append(i)

        self.assertEqual(self.heap.pop(0), 1)

    def test_append_reverse(self):
        items = reversed([1, 2, 3, 4, 5, 6])
        for i in items:
            self.heap.append(i)

        self.assertEqual(self.heap.pop(0), 1)

    def test_append_rand(self):
        items = [6, 2, 3, 1, 12, 9]
        for i in items:
            self.heap.append(i)

        self.assertEqual(self.heap.pop(0), 1)

    def test_pop(self):
        items = [6, 2, 3, 1, 12, 9]
        for i in items:
            self.heap.append(i)

        self.assertEqual(self.heap.pop(0), 1)
        self.assertEqual(self.heap.pop(0), 2)
        self.assertEqual(self.heap.pop(0), 3)
        self.assertEqual(self.heap.pop(0), 6)
        self.assertEqual(self.heap.pop(0), 9)
        self.assertEqual(self.heap.pop(0), 12)