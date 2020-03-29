
import typing
from collections import defaultdict
from advent_of_code.util.aoc_util import AocLogger


class Grid2D(object):

    def __init__(self, text='', default=' '):
        """
        NOTE: uses an inverted y-axis (increasing downwards)
        """
        self.grid = defaultdict(lambda: default)

        self.value_width = 1

        self.min_x = 2**32
        self.max_x = 0
        self.min_y = 2**32
        self.max_y = 0

        self.overlay = {}

        if text:
            # text = text.strip()
            lines = text.split('\n')
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    self.set(c, r, col)

    def set_value_width(self, width):
        self.value_width = width

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

    def find_by_function(self, func):
        result = []
        for coord, value in self.grid.items():
            if func(value):
                result.append(coord)
        return result

    def to_string(self, top_left, bottom_right):
        row_range = range(top_left[1], bottom_right[1] + 1)
        col_range = range(top_left[0], bottom_right[0] + 1)
        lines = []
        for y in row_range:
            builder = []
            for x in col_range:
                coord = (x, y)
                if coord in self.overlay:
                    value = self.overlay[coord]
                else:
                    value = self.grid[coord]
                formatted = '{:{}}'.format(value, self.value_width)
                builder.append(formatted)
            lines.append(''.join(builder))
        return '\n'.join(lines)

    def __repr__(self):
        top_left = (self.min_x, self.min_y)
        bottom_right = (self.max_x, self.max_y)
        return self.to_string(top_left, bottom_right)

    def show_from(self, top_left, bottom_right):
        print('\n{}: {} to {}\n{}\n'.format(
            type(self).__name__,
            top_left,
            bottom_right,
            self.to_string(top_left, bottom_right)
        ))

    def show(self):
        top_left = (self.min_x, self.min_y)
        bottom_right = (self.max_x, self.max_y)
        self.show_from(top_left, bottom_right)

    def rows(self):
        return range(self.min_y, self.max_y + 1)

    def cols(self):
        return range(self.min_x, self.max_x + 1)

    def count_adjacent(self, x, y, value):
        adj_coords = [
            (x-1, y),
            (x+1, y),
            (x, y-1),
            (x, y+1),
        ]
        return sum([1 for c in adj_coords if self.is_value(c, value)])

    def is_on_edge(self, x, y):
        return x == self.min_x or x == self.max_x or y == self.min_y or y == self.max_y

    @classmethod
    def get_adjacent_coords(cls, coord):
        return [
            cls.get_coord_north(coord),
            cls.get_coord_east(coord),
            cls.get_coord_south(coord),
            cls.get_coord_west(coord),
        ]

    @classmethod
    def get_diagonal_coords(cls, coord):
        # in order by quadrant
        return [
            (coord[0] + 1, coord[1] - 1),
            (coord[0] - 1, coord[1] - 1),
            (coord[0] - 1, coord[1] + 1),
            (coord[0] + 1, coord[1] + 1),
        ]

    @staticmethod
    def get_coord_north(coord: typing.Tuple[int]):
        return coord[0], coord[1] - 1

    @staticmethod
    def get_coord_east(coord: typing.Tuple[int]):
        return coord[0] + 1, coord[1]

    @staticmethod
    def get_coord_south(coord: typing.Tuple[int]):
        return coord[0], coord[1] + 1

    @staticmethod
    def get_coord_west(coord: typing.Tuple[int]):
        return coord[0] - 1, coord[1]





