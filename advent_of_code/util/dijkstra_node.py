
import math

from advent_of_code.util import aoc_util


class DijkstraNode(object):

    def __init__(self, coord):
        self.coord = coord
        self.dist = math.inf
        self.path = []

    def __repr__(self):
        return '{}: {}'.format(type(self).__name__, self.coord)

    def __eq__(self, other):
        return self.coord == other.coord

    def __hash__(self):
        return hash(self.coord)

    def __lt__(self, other):
        return aoc_util.is_reading_order(self.coord, other.coord)

    def is_better_than(self, other):
        return self.dist < other.dist
