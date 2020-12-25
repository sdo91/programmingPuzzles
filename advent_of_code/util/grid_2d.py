import typing
from collections import defaultdict
from advent_of_code.util.aoc_util import AocLogger


class Grid2D(object):
    DIRECTIONS = {
        'N': (0, -1),
        'E': (+1, 0),
        'S': (0, +1),
        'W': (-1, 0),
    }

    EAST_WEST = {'E', 'W'}

    def __init__(self, text='', default=' ', overlay_chars=frozenset()):
        """
        NOTE: uses an inverted y-axis (increasing downwards)
        """
        self.default_value = default
        self.grid = defaultdict(lambda: default)

        self.value_width = 1

        self.min_x = 2 ** 32
        self.max_x = 0
        self.min_y = 2 ** 32
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

    def __hash__(self):
        return hash(str(self))

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

    def is_default(self, coord):
        return self.grid[coord] == self.default_value

    def is_value_in(self, coord, collection):
        return self.grid[coord] in collection

    def get_top(self, coord, conversion_method=None):
        if coord in self.overlay:
            return self.overlay[coord]
        elif conversion_method:
            return conversion_method(self.grid[coord])
        else:
            return self.grid[coord]

    def get_tuple(self, coord):
        return self.grid[coord]

    def get(self, x, y):
        return self.grid[(x, y)]

    def count(self, char):
        return sum([1 for v in self.grid.values() if v == char])

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

    def replace(self, old, new):
        for coord, value in self.grid.items():
            if value == old:
                self.set_tuple(coord, new)

    def top_left(self):
        return self.min_x, self.min_y

    def bottom_right(self):
        return self.max_x, self.max_y

    def to_string(self, top_left, bottom_right, conversion_method=None):
        row_range = range(top_left[1], bottom_right[1] + 1)
        col_range = range(top_left[0], bottom_right[0] + 1)
        lines = []
        for y in row_range:
            builder = []
            for x in col_range:
                coord = (x, y)
                value = self.get_top(coord, conversion_method)
                formatted = '{:{}}'.format(value, self.value_width)
                builder.append(formatted)
            if self.show_line_numbers:
                builder.append(' (line {})'.format(y))
            lines.append(''.join(builder))
        return '\n'.join(lines)

    def __repr__(self):
        top_left = self.top_left()
        bottom_right = self.bottom_right()
        return self.to_string(top_left, bottom_right)

    def show_from(self, top_left, bottom_right, conversion_method=None):
        print('\n{}: {} to {}\n{}\n'.format(
            type(self).__name__,
            top_left,
            bottom_right,
            self.to_string(top_left, bottom_right, conversion_method)
        ))

    def show(self, overlay_coord=None, overlay_char='*'):
        if overlay_coord:
            self.overlay = {overlay_coord: overlay_char}
        top_left = self.top_left()
        bottom_right = self.bottom_right()
        self.show_from(top_left, bottom_right)
        if overlay_coord:
            self.overlay = {}

    def show_converted(self, conversion_method):
        top_left = self.top_left()
        bottom_right = self.bottom_right()
        self.show_from(top_left, bottom_right, conversion_method)

    def rows(self):
        return range(self.min_y, self.max_y + 1)

    def cols(self):
        return range(self.min_x, self.max_x + 1)

    def coords(self):
        for y in self.rows():
            for x in self.cols():
                yield x, y

    def count_adjacent(self, coord, value, include_diagonal=False):
        coords = self.get_adjacent_coords(coord)
        if include_diagonal:
            coords += self.get_diagonal_coords(coord)
        return sum([1 for c in coords if self.is_value(c, value)])

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

    def set_coords_default(self, coords_list, value):
        """
        set each coord in 'coords_list' to 'value' if is was previously the default value
        """
        for coord in coords_list:
            if self.is_default(coord):
                self.set_tuple(coord, value)

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

    @classmethod
    def get_coord_direction(cls, coord: typing.Tuple[int], direction: str):
        dx, dy = cls.DIRECTIONS[direction]
        return cls.adjust_coord(coord, dx, dy)

    def rot90(self, n=1):
        """
        Returns:
            Grid2D: new grid rotated 90 degrees CCW
        """
        prev_grid = self.grid
        result = None
        for i in range(n):
            result = Grid2D()
            for coord, value in prev_grid.items():
                x = coord[1]
                y = -coord[0]
                result.set_tuple((x, y), value)
            prev_grid = result.grid
        return result

    def flip(self, axis: str):
        """
        Args:
            axis (str): 'X' or 'Y'

        Returns:
            Grid2D: new grid flipped over the specified axis
        """
        axis = axis.upper()[0]
        result = Grid2D()
        for coord, value in self.grid.items():
            if axis == 'X':
                new_coord = coord[0], -coord[1]
            else:
                new_coord = -coord[0], coord[1]
            result.set_tuple(new_coord, value)
        return result
