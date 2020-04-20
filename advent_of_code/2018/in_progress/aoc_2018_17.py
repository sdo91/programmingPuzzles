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
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    57,
    0,
    0,
]

TEST_OUTPUT_2 = [
    0,
    0,
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
            0,
            self.solve_part_1(puzzle_input)
        )

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_2(puzzle_input)
        # )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def solve_part_1(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_1_result = solver.p1()

        print('part_1_result: {}\n'.format(part_1_result))
        return part_1_result

    def solve_part_2(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_2_result = solver.p2()

        print('part_2_result: {}\n'.format(part_2_result))
        return part_2_result










class Solver(object):

    OPEN = {'.', '|'}
    SOLID = {'#', '~'}
    WET = {'|', '~'}

    def __init__(self, text: str):
        self.text = text.strip()

        self.spring_coords = (500, 0)

        self.grid = Grid2D(default='.')
        self.grid.set_tuple(self.spring_coords, '+')

        lines = aoc_util.lines(self.text)
        for line in lines:
            line_values = aoc_util.ints(line)
            if line.startswith('x'):
                coord1 = (line_values[0], line_values[1])
                coord2 = (line_values[0], line_values[2])
            else:
                coord1 = (line_values[1], line_values[0])
                coord2 = (line_values[2], line_values[0])

            self.grid.set_range(coord1, coord2, '#')

        self.grid.show()
        # AocLogger.log(str(self))

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def recursive_drip(self, start_coord):
        """

        if we cant go down, scan left and right
            look for wall or drop off
            if 2 walls:
                settle (mark ~)
                go back to src
                    or just up 1?
            else:
                mark with |
                call recursive on each drop off point (1 or 2)

        """
        current_coord = start_coord

        while True:
            # check if done
            if self.grid.is_out_of_bounds(current_coord):
                # we have reached the bottom
                break

            if self.can_move_down(current_coord):
                if current_coord != self.spring_coords:
                    self.grid.set_tuple(current_coord, '|')
                current_coord = Grid2D.get_coord_south(current_coord)
            else:
                # next is solid

                # scan left and right
                left_coord, left_blocked = self.scan(current_coord, -1)
                right_coord, right_blocked = self.scan(current_coord, +1)

                if left_blocked and right_blocked:
                    # mark as settled
                    self.grid.set_range(left_coord, right_coord, '~')
                else:
                    self.grid.set_range(left_coord, right_coord, '|')
                    if not left_blocked:
                        self.recursive_drip(left_coord)
                    if not right_blocked:
                        self.recursive_drip(right_coord)
                    break

                current_coord = Grid2D.get_coord_north(current_coord)
        # end while

        self.grid.show()

    def scan(self, start_coord, dx):
        current = start_coord
        while True:
            # first check if can fall
            if self.can_move_down(current):
                return current, False

            # then check for wall
            next = Grid2D.adjust_coord(current, dx)
            if self.grid.is_value_in(next, self.SOLID):
                return current, True

            # advance coord
            current = next

    def can_move_down(self, coord):
        coord_below = Grid2D.get_coord_south(coord)
        return self.grid.is_value_in(coord_below, self.OPEN)

    def p1(self):
        self.recursive_drip(self.spring_coords)
        # self.grid.show()
        reachable = self.grid.find_by_function(lambda x: x in self.WET)
        return len(reachable)

    def p2(self):
        """

        """
        z=0
        return 2










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




