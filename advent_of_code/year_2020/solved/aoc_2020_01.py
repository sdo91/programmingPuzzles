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

### CONSTANTS ###
TEST_INPUT = [
    """
1721
979
366
299
675
1456
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    514579,
    0,
    0,
]

TEST_OUTPUT_2 = [
    241861950,
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
            63616,
            self.solve_part_1(self.puzzle_input)
        )

        aoc_util.assert_equal(
            67877784,
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
        self.numbers = aoc_util.ints(self.text)

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        for first in self.numbers:
            for second in self.numbers:
                if first + second == 2020:
                    return first * second

    def p2(self):
        for first in self.numbers:
            for second in self.numbers:
                for third in self.numbers:
                    if first + second + third == 2020:
                        return first * second * third


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
