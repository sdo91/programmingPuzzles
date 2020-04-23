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

    def solve_part_1(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_1_result = solver.p1()

        print('part_1_result: {}'.format(aoc_util.format_coords(part_1_result)))
        return part_1_result

    def solve_part_2(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_2_result = solver.p2()

        print('part_2_result: {}'.format(aoc_util.format_coords(part_2_result)))
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
        max_coord, max_sq_power = self.check_squares_fast(3)

        self.show_square(max_coord)
        print('max_sq_power: {}'.format(max_sq_power))
        return max_coord

    def p2(self):
        max_coord = None
        max_sq_power = -99

        for size in range(3, 20):
            print('on size: {}'.format(size))

            coord, power = self.check_squares_fast(size)

            if power > max_sq_power:
                max_sq_power = power
                max_coord = (coord[0], coord[1], size)

            print('best so far: {}'.format(max_coord))

        print('max_sq_power: {}'.format(max_sq_power))
        return max_coord

    def check_squares_fast(self, size):
        max_coord = None
        max_sq_power = -99

        grid_rows = range(1, self.ORDER - size + 2)
        for grid_row in grid_rows:

            # calc subcolumn sums
            subcolumn_sums = []  # zero indexed
            for grid_col in range(1, self.ORDER + 1):
                # let col = 1
                subcol_sum = 0
                for y_offset in range(size):
                    coord = (grid_col, grid_row + y_offset)
                    subcol_sum += self.grid.get_tuple(coord)
                subcolumn_sums.append(subcol_sum)

            # find the best column given this row
            grid_col, sq_power = self.find_best_column(subcolumn_sums, size)
            if sq_power > max_sq_power:
                max_sq_power = sq_power
                max_coord = (grid_col, grid_row)

        return max_coord, max_sq_power

    def find_best_column(self, subcolumn_sums, size):
        max_col = None
        max_sq_power = -99
        sq_power = -1

        grid_columns = range(1, self.ORDER - size + 2)
        for grid_col in grid_columns:
            # calc square power
            if grid_col == 1:
                sq_power = sum(subcolumn_sums[0:size])
            else:
                old_col = grid_col - 2
                new_col = old_col + size
                sq_power += subcolumn_sums[new_col] - subcolumn_sums[old_col]

            # check square power
            if sq_power > max_sq_power:
                max_sq_power = sq_power
                max_col = grid_col

        return max_col, max_sq_power

    def show_square(self, top_left):
        adj_top_left = (
            top_left[0] - 1,
            top_left[1] - 1
        )
        adj_bottom_right = (
            top_left[0] + 3,
            top_left[1] + 3
        )
        self.grid.show_from(adj_top_left, adj_bottom_right)

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




