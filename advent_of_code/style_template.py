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

addToPath('../..')

### IMPORTS ###

import traceback
# import numpy as np

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger


### CONSTANTS ###
TEST_INPUT_1 = [
    """

    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    0,
    0,
    0,
]

TEST_INPUT_2 = [
    """

    """, """

    """, """

    """
]

TEST_OUTPUT_2 = [
    0,
    0,
    0,
]





class MyObject(object):

    def __init__(self, text):
        self.text = text
        self.id = 0

    def __str__(self):
        return 'MyObject {}: {}'.format(
            self.id, self.text)

    def __repr__(self):
        return str(self)





class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        try:
            puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            print(traceback.format_exc())
            puzzle_input = 'unable to get input'
        aoc_util.write_input(puzzle_input, __file__)

        self.run_tests()

        AocLogger.verbose = False

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_1(puzzle_input)
        # )

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_2(puzzle_input)
        # )

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT_1, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT_2, TEST_OUTPUT_2)

    def solve_test_case_1(self, test_input: str):
        test_input = test_input.strip()
        AocLogger.log('test input:\n{}\n'.format(test_input))
        return 0

    def solve_part_1(self, puzzle_input: str):
        part_1_result = self.solve_test_case_1(puzzle_input)

        print('part_1_result: {}'.format(part_1_result))
        return part_1_result

    def solve_test_case_2(self, test_input: str):
        test_input = test_input.strip()
        AocLogger.log('test input:\n{}\n'.format(test_input))
        return 0

    def solve_part_2(self, puzzle_input: str):
        part_2_result = self.solve_test_case_2(puzzle_input)

        print('part_2_result: {}'.format(part_2_result))
        return part_2_result





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




