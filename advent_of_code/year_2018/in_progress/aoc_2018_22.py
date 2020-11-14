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
depth: 510
target: 10,10
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    114,
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

    def __init__(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        try:
            self.puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            print(traceback.format_exc())
            self.puzzle_input = 'unable to get input'
        aoc_util.write_input(self.puzzle_input, __file__)

    def run(self):
        start_time = time.time()

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            0,
            self.solve_part_1(self.puzzle_input)
        )

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_2(self.puzzle_input)
        # )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

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

        ints = aoc_util.ints(self.text)
        self.depth = ints[0]
        self.target = tuple(ints[1:])

        self.erosion_levels = Grid2D()

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def calc_geologic_index(self, coord):
        """
        The geologic index can be determined using the first rule that applies from the list below:
            - The region at 0,0 (the mouth of the cave) has a geologic index of 0.
            - The region at the coordinates of the target has a geologic index of 0.
            - If the region's Y coordinate is 0, the geologic index is its X coordinate times 16807.
            - If the region's X coordinate is 0, the geologic index is its Y coordinate times 48271.
            - Otherwise, the region's geologic index is the result of multiplying the erosion levels
                of the regions at X-1,Y and X,Y-1.

        Returns:
            int
        """
        if coord == (0, 0) or coord == self.target:
            return 0
        if coord[1] == 0:
            return coord[0] * 16807
        if coord[0] == 0:
            return coord[1] * 48271
        west = self.erosion_levels.get_coord_west(coord)
        north = self.erosion_levels.get_coord_north(coord)
        return self.erosion_levels.get_tuple(west) * self.erosion_levels.get_tuple(north)

    def calc_erosion_level(self, geologic_index):
        """
        A region's erosion level is its geologic index plus the cave system's depth, all modulo 20183. Then:
            - If the erosion level modulo 3 is 0, the region's type is rocky.
            - If the erosion level modulo 3 is 1, the region's type is wet.
            - If the erosion level modulo 3 is 2, the region's type is narrow.

        Returns:
            int
        """
        return (geologic_index + self.depth) % 20183

    @staticmethod
    def to_type(erosion_level):
        risk = erosion_level % 3
        if risk == 0:
            return '.'  # rocky
        elif risk == 1:
            return '='  # wet
        else:
            return '|'  # narrow

    def p1(self):
        """

        """

        total_risk = 0
        for y in range(self.target[1] + 1):
            for x in range(self.target[0] + 1):
                coord = (x, y)

                geologic_index = self.calc_geologic_index(coord)
                erosion_level = self.calc_erosion_level(geologic_index)

                self.erosion_levels.set_tuple(coord, erosion_level)

                total_risk += (erosion_level % 3)

        if AocLogger.verbose:
            self.erosion_levels.show_converted(self.to_type)
        print('total_risk: {}'.format(total_risk))

        return total_risk

    def p2(self):
        """

        """
        z=0
        return 2










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




