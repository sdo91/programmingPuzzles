
import heapq
import random


class MinHeap(object):
    """
    adapted from:
    https://leetcode.com/problems/network-delay-time/discuss/206419/python-dijkstras-sp-with-priority-queue
    """

    PRIORITY = 0
    ITEM = 1
    IS_ACTIVE = 2

    def __init__(self):
        self.h = []
        self.items = {}
        self.counter = 0

    def __repr__(self):
        return '{}: len={}, min={}'.format(
            self.classname(),
            len(self),
            self.peek(),
        )

    def __bool__(self):
        return not self.is_empty()

    def __len__(self):
        """
        Returns:
            int: the number of active items in the heap
        """
        return self.counter

    def classname(self):
        return type(self).__name__

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
        """
        effectively remove the given item from the heap by marking it as inactive
        """
        entry = self.items[item]
        entry[self.IS_ACTIVE] = False
        self.counter -= 1

    def pop(self):
        """
        remove and return the min item
        """
        while self.h:
            priority, item, is_active = heapq.heappop(self.h)
            if is_active:
                self.counter -= 1
                del self.items[item]
                return item
            # skip if not active
        raise RuntimeError('cannot pop from empty {}'.format(self.classname()))

    def peek(self):
        """
        return min item without removing
        """
        self._remove_inactive()
        if self.is_empty():
            return None
        else:
            return self.h[0][self.ITEM]

    def _remove_inactive(self):
        """
        remove any inactive entries from the top of the heap
        """
        while self.h:
            priority, item, is_active = self.h[0]
            if is_active:
                # top is active, we are done
                return
            else:
                # remove inactive entry
                heapq.heappop(self.h)

    def get_priority(self, item):
        """
        Returns:
            int: the current priority of the given item
        """
        return self.items[item][self.PRIORITY]

    def insert_if_better(self, item, priority):
        """
        update the priority of the item if it is better
        eg: for shortest path algorithms, update only if the new path is shorter

        Returns:
            bool: True if inserted
        """
        if item in self.items and priority >= self.get_priority(item):
            # not better
            return False
        else:
            self.insert(item, priority)
            return True










if __name__ == '__main__':
    # do some quick tests

    # create entries
    entries_ordered = [
        ('1U', (1, 0)),
        ('1L', (1, 1)),
        ('1R', (1, 2)),
        ('1D', (1, 3)),
        ('2U', (2, 0)),
        ('2L', (2, 1)),
        ('2R', (2, 2)),
        ('2D', (2, 3)),
    ]
    entries_shuffled = entries_ordered.copy()
    random.shuffle(entries_shuffled)

    # populate queue
    pq = MinHeap()
    for e in entries_shuffled:
        pq.insert(e[0], e[1])

    # check pop order
    for e in entries_ordered:
        assert e[0] == pq.pop()
    assert len(pq) == 0

    print('all tests passed: {}'.format(pq.classname()))


