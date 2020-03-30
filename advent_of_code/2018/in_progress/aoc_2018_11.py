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
18
    """, """
42
    """, """

    """
]

TEST_OUTPUT_1 = [
    (33, 45),
    (21, 61),
    0,
]

TEST_OUTPUT_2 = [
    (90, 269, 16),
    (232, 251, 12),
    0,
]










class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))
        start_time = time.time()

        try:
            puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            print(traceback.format_exc())
            puzzle_input = 'unable to get input'
        aoc_util.write_input(puzzle_input, __file__)

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            (44, 37),
            self.solve_part_1(puzzle_input)
        )

        aoc_util.assert_equal(
            (235, 87, 13),
            self.solve_part_2(puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True

        aoc_util.assert_equal( 4, Solver.calc_power_level((  3,   5),  8))
        aoc_util.assert_equal(-5, Solver.calc_power_level((122,  79), 57))
        aoc_util.assert_equal( 0, Solver.calc_power_level((217, 196), 39))
        aoc_util.assert_equal( 4, Solver.calc_power_level((101, 153), 71))

        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)

        # aoc_util.assert_equal(
        #     TEST_OUTPUT_2[0],
        #     self.solve_part_2(TEST_INPUT[0])
        # )

        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def solve_part_1(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_1_result = solver.p1()

        print('part_1_result: {}'.format(part_1_result))
        return part_1_result

    def solve_part_2(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_2_result = solver.p2()

        print('part_2_result: {}'.format(part_2_result))
        return part_2_result










class Solver(object):

    ORDER = 300

    def __init__(self, text: str):
        self.text = text.strip()
        self.serial_number = int(self.text)

        # populate grid
        self.grid = Grid2D()
        self.grid.set_value_width(4)
        for y in range(1, self.ORDER + 1):
            for x in range(1, self.ORDER + 1):
                coord = x, y
                power_level = self.calc_power_level(coord, self.serial_number)
                self.grid.set_tuple(coord, power_level)

        AocLogger.log(str(self))

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        # find best square
        max_coord, max_sq_power = self.check_all_squares_of_size(3)

        self.show_square(max_coord)
        print('max_sq_power: {}'.format(max_sq_power))
        return max_coord

    def p2(self):
        max_coord = None
        max_sq_power = -99

        # todo: make faster
        for size in range(13, 14):
            print('on size: {}'.format(size))

            coord, power = self.check_all_squares_of_size(size)

            if power > max_sq_power:
                max_sq_power = power
                max_coord = (coord[0], coord[1], size)

            print('best so far: {}'.format(max_coord))

        print('max_sq_power: {}'.format(max_sq_power))
        return max_coord

    def check_all_squares_of_size(self, size):
        RANGE_MAX = self.ORDER - size + 1

        max_coord = None
        max_sq_power = -99

        for y in range(1, RANGE_MAX):

            for x in range(1, RANGE_MAX):
                # check square power
                top_left = x, y
                sq_power = self.calc_square_power(top_left, size)
                if sq_power > max_sq_power:
                    max_sq_power = sq_power
                    max_coord = top_left

        return max_coord, max_sq_power

    def calc_square_power(self, top_left, size):
        result = 0
        for y_offset in range(size):
            for x_offset in range(size):
                coord = (top_left[0] + x_offset, top_left[1] + y_offset)
                result += self.grid.get(*coord)
        return result

    def show_square(self, top_left):
        adj_top_left = (
            top_left[0] - 1,
            top_left[1] - 1
        )
        bottom_right = (
            top_left[0] + 3,
            top_left[1] + 3
        )
        self.grid.show_from(adj_top_left, bottom_right)

    @classmethod
    def calc_power_level(cls, coord, serial_number):
        rack_id = coord[0] + 10
        power_level = rack_id * coord[1] + serial_number
        power_level *= rack_id
        power_level = power_level % 1000 // 100  # get hundreds digit
        power_level -= 5
        return power_level










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




