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

import math
import time
import traceback

import aocd
import numpy as np

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger

### CONSTANTS ###
TEST_INPUT = [
    """
F10
N3
F7
R90
F11
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    25,
    0,
    0,
]

TEST_OUTPUT_2 = [
    286,
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
            1631,
            self.solve_part_1(self.puzzle_input)
        )

        aoc_util.assert_equal(
            58606,
            self.solve_part_2(self.puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        Solver.test_rotation()
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
    DELTAS = {
        0: np.array([0, 1]),
        90: np.array([1, 0]),
        180: np.array([0, -1]),
        270: np.array([-1, 0]),
    }

    DIRECTIONS = {
        'N': 0,
        'E': 90,
        'S': 180,
        'W': 270,
    }

    def __init__(self, text: str):
        self.text = text.strip()
        AocLogger.log(str(self))
        self.lines = aoc_util.lines(text)

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        heading = 90
        coord = np.array([0, 0])

        for line in self.lines:
            cmd = line[0]
            arg = int(line[1:])

            if cmd == 'L':
                heading -= arg
                heading %= 360
            elif cmd == 'R':
                heading += arg
                heading %= 360
            else:
                # move
                if cmd == 'F':
                    direction = heading
                else:
                    direction = self.DIRECTIONS[cmd]

                delta = self.DELTAS[direction]
                coord += arg * delta

        return aoc_util.manhatten_dist(coord)

    def p2(self):
        """
        high: 58856
        """
        ship = np.array([0, 0])
        waypoint = np.array([10, 1])

        for line in self.lines:
            cmd = line[0]
            arg = int(line[1:])

            if cmd == 'F':
                ship += arg * waypoint
            elif cmd == 'L':
                waypoint = self.rotate_point(waypoint, arg)
            elif cmd == 'R':
                waypoint = self.rotate_point(waypoint, -arg)
            else:
                # move waypoint
                direction = self.DIRECTIONS[cmd]
                delta = self.DELTAS[direction]
                waypoint += arg * delta

        return aoc_util.manhatten_dist(ship)

    @classmethod
    def rotate_point(cls, point, degrees):
        """
        rotate the point about the origin
        NOTE: positive rotation is CCW
        see: https://academo.org/demos/rotation-about-point/
        """
        radians = degrees * math.pi / 180
        sine = math.sin(radians)
        cosine = math.cos(radians)

        new_east = point[0] * cosine - point[1] * sine
        new_north = point[0] * sine + point[1] * cosine

        new_east = round(new_east)
        new_north = round(new_north)

        return np.array([new_east, new_north])

    @classmethod
    def test_rotation(cls):
        start_point = np.array([10, 4])
        assert list(cls.rotate_point(start_point, 0)) == [10, 4]
        assert list(cls.rotate_point(start_point, -90)) == [4, -10]
        assert list(cls.rotate_point(start_point, -180)) == [-10, -4]
        assert list(cls.rotate_point(start_point, -270)) == [-4, 10]


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
