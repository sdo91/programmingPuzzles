
import typing
from collections import defaultdict
from advent_of_code.util.aoc_util import AocLogger


class Grid2D(object):

    def __init__(self, text='', default=' ', overlay_chars=frozenset()):
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
        self.show_line_numbers = False

        if text:
            lines = text.split('\n')
            for y, line in enumerate(lines):
                for x, char in enumerate(line):
                    coord = (x, y)
                    if char in overlay_chars:
                        # place the char in the overlay instead
                        self.overlay[coord] = char
                        # use the default in the main grid
                        self.set_tuple(coord, default)
                    else:
                        self.set_tuple(coord, char)

    def set_value_width(self, width):
        self.value_width = width

    def set_range(self, coord1, coord2, value):
        x_min = min(coord1[0], coord2[0])
        x_max = max(coord1[0], coord2[0])
        y_min = min(coord1[1], coord2[1])
        y_max = max(coord1[1], coord2[1])
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                coord = (x, y)
                self.set_tuple(coord, value)

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

    def is_value_in(self, coord, collection):
        return self.grid[coord] in collection

    def get_top(self, coord):
        if coord in self.overlay:
            return self.overlay[coord]
        else:
            return self.grid[coord]

    def get_tuple(self, coord):
        return self.grid[coord]

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
        """
        Args:
            func (function(str) -> bool):

        Returns:
             list[str]
        """
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
                value = self.get_top(coord)
                formatted = '{:{}}'.format(value, self.value_width)
                builder.append(formatted)
            if self.show_line_numbers:
                builder.append(' (line {})'.format(y))
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

    def count_adjacent(self, coord, value):
        adj_coords = self.get_adjacent_coords(coord)
        return sum([1 for c in adj_coords if self.is_value(c, value)])

    def is_on_edge(self, coord):
        x, y = coord
        return x == self.min_x or x == self.max_x or y == self.min_y or y == self.max_y

    def is_out_of_bounds(self, coord):
        x, y = coord
        return x < self.min_x or x > self.max_x or y < self.min_y or y > self.max_y

    @classmethod
    def get_adjacent_coords(cls, coord):
        # in reading order (important)
        return [
            cls.get_coord_north(coord),
            cls.get_coord_west(coord),
            cls.get_coord_east(coord),
            cls.get_coord_south(coord),
        ]

    @classmethod
    def get_diagonal_coords(cls, coord):
        # in order by quadrant (important)
        return [
            cls.adjust_coord(coord, +1, -1),
            cls.adjust_coord(coord, -1, -1),
            cls.adjust_coord(coord, -1, +1),
            cls.adjust_coord(coord, +1, +1),
        ]

    @classmethod
    def get_coord_north(cls, coord: typing.Tuple[int]):
        return cls.adjust_coord(coord, dy=-1)

    @classmethod
    def get_coord_east(cls, coord: typing.Tuple[int]):
        return cls.adjust_coord(coord, dx=+1)

    @classmethod
    def get_coord_south(cls, coord: typing.Tuple[int]):
        return cls.adjust_coord(coord, dy=+1)

    @classmethod
    def get_coord_west(cls, coord: typing.Tuple[int]):
        return cls.adjust_coord(coord, dx=-1)

    @classmethod
    def adjust_coord(cls, coord: typing.Tuple[int], dx=0, dy=0):
        return coord[0] + dx, coord[1] + dy





