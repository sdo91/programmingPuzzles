
import heapq


class MinHeap(object):
    """
    from: https://leetcode.com/problems/network-delay-time/discuss/206419/python-dijkstras-sp-with-priority-queue
    """

    def __init__(self):
        self.h = []
        self.items = {}
        self.counter = 0

    def is_empty(self):
        return not self.counter > 0

    def insert(self, item, priority):
        """
        NOTE: if the item is already in the heap, its priority will be updated
        """
        if item in self.items:
            self.remove(item)
        entry = [priority, item, True]
        self.counter += 1
        self.items[item] = entry
        heapq.heappush(self.h, entry)

    def remove(self, item):
        entry = self.items[item]
        entry[-1] = False
        self.counter -= 1

    def pop(self):
        while self.h:
            _, item, is_active = heapq.heappop(self.h)
            if is_active:
                self.counter -= 1
                del self.items[item]
                return item

    def get_num_active(self):
        return self.counter

    def get_priority(self, item):
        return self.items[item][0]

    def insert_if_better(self, item, priority):
        if item in self.items and priority >= self.get_priority(item):
            # not better
            return False
        else:
            self.insert(item, priority)
            return True
