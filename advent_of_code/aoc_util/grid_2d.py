
import typing
from collections import defaultdict
from aoc_util.aoc_util import AocLogger


class Grid2D(object):

    def __init__(self, text: str = ''):
        """
        NOTE: uses an inverted y-axis by default (increasing downwards)
        """
        self.grid = defaultdict(lambda: ' ')

        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

        self.overlay = {}

        if text:
            text = text.strip()
            lines = text.split('\n')
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    self.set(c, r, col)

    def set_tuple(self, coord, value):
        self.set(coord[0], coord[1], value)

    def set(self, x, y, value):
        self.grid[(x, y)] = value

        self.min_x = min(self.min_x, x)
        self.max_x = max(self.max_x, x)
        self.min_y = min(self.min_y, y)
        self.max_y = max(self.max_y, y)

    def is_value(self, coord, value):
        return self.grid[coord] == value

    def get(self, x, y):
        return self.grid[(x, y)]

    def find(self, char):
        # todo: rename to find_all
        result = []
        for coord, value in self.grid.items():
            if value == char:
                result.append(coord)
        return result

    def show(self):
        print()
        # for y in range(self.max_y, self.min_y - 1, -1):
        for y in range(self.min_y, self.max_y + 1):
            line = ''
            for x in range(self.min_x, self.max_x + 1):
                coord = (x, y)
                if coord in self.overlay:
                    line += self.overlay[coord]
                else:
                    line += self.grid[coord]
            print(line)
        print()




