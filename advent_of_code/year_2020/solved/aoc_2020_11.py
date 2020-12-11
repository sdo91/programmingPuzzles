#!/usr/bin/env python3

def addToPath(relPath):
    from os import path
    import sys
    dirOfThisFile = path.dirname(path.realpath(__file__))
    dirToAdd = path.normpath(path.join(dirOfThisFile, relPath))
    if dirToAdd not in sys.path:
        print('adding to path: {}'.format(dirToAdd))
        sys.path.insert(0, dirToAdd)
    else:
        print('already in path: {}'.format(dirToAdd))


addToPath('../../..')

### IMPORTS ###

import time
import traceback

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger
from advent_of_code.util.grid_2d import Grid2D

### CONSTANTS ###
TEST_INPUT = [
    """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    37,
    0,
    0,
]

TEST_OUTPUT_2 = [
    26,
    0,
    0,
]


class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def __init__(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        try:
            self.puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            error_msg = traceback.format_exc()
            print(error_msg)
            self.puzzle_input = 'unable to get input:\n\n{}'.format(error_msg)
        aoc_util.write_input(self.puzzle_input, __file__)

    def run(self):
        start_time = time.time()

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            2211,
            self.solve_part_1(self.puzzle_input)
        )

        aoc_util.assert_equal(
            1995,
            self.solve_part_2(self.puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def solve_part_1(self, text: str):
        solver = Solver(text)

        part_1_result = solver.p1()

        print('part_1_result: {}\n'.format(part_1_result))
        return part_1_result

    def solve_part_2(self, text: str):
        solver = Solver(text)

        part_2_result = solver.p2()

        print('part_2_result: {}\n'.format(part_2_result))
        return part_2_result


class Solver(object):

    def __init__(self, text: str):
        self.text = text.strip()
        AocLogger.log(str(self))

        self.grid = Grid2D(self.text)

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        i = 0
        while True:
            i += 1
            new_grid = Grid2D()
            is_same = True

            for y in self.grid.rows():
                for x in self.grid.cols():
                    coord = x, y
                    value = self.grid.get_tuple(coord)

                    if value == 'L' and self.grid.count_adjacent(coord, '#', include_diagonal=True) == 0:
                        new_grid.set_tuple(coord, '#')
                        is_same = False
                    elif value == '#' and self.grid.count_adjacent(coord, '#', include_diagonal=True) >= 4:
                        new_grid.set_tuple(coord, 'L')
                        is_same = False
                    else:
                        new_grid.set_tuple(coord, value)

            if AocLogger.verbose:
                new_grid.show()
            if is_same:
                break
            self.grid = new_grid

        return self.grid.count('#')

    def p2(self):
        i = 0
        while True:
            i += 1
            new_grid = Grid2D()
            is_same = True

            for y in self.grid.rows():
                for x in self.grid.cols():
                    coord = x, y
                    value = self.grid.get_tuple(coord)

                    num_occupied = self.count_visible_occupied(coord)

                    if value == 'L' and num_occupied == 0:
                        new_grid.set_tuple(coord, '#')
                        is_same = False
                    elif value == '#' and num_occupied >= 5:
                        new_grid.set_tuple(coord, 'L')
                        is_same = False
                    else:
                        new_grid.set_tuple(coord, value)

            if AocLogger.verbose:
                new_grid.show()
            if is_same:
                break
            self.grid = new_grid

        return self.grid.count('#')

    def count_visible_occupied(self, coord):
        DIRECTIONS = {
            (-1, -1), (0, -1), (+1, -1),
            (-1, 00000000000), (+1, 00),
            (-1, +1), (0, +1), (+1, +1),
        }
        return sum(1 for d in DIRECTIONS if self.is_occupied(coord, d))

    def is_occupied(self, coord, direction):
        """
        return True if next seat in that direction is occupied
        """
        while True:
            # move in direction
            coord = self.grid.adjust_coord(coord, *direction)
            if self.grid.is_out_of_bounds(coord):
                return False

            value = self.grid.get_tuple(coord)
            if value == '#':
                return True
            if value == 'L':
                return False
            # otherwise, loop


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
