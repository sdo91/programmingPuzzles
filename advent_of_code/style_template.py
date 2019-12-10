#!/usr/bin/env python3



### IMPORTS ###

import numpy as np
import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
# from aoc_util.intcode_computer import IntcodeComputer


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
            puzzle_input = 'unable to get input'
        aoc_util.write_input(puzzle_input, __file__)

        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT_1, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT_2, TEST_OUTPUT_2)

        AocLogger.verbose = False

        # self.solve_part_1(puzzle_input)

        # self.solve_part_2(puzzle_input)

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_1(puzzle_input)
        # )

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_2(puzzle_input)
        # )

    def solve_test_case_1(self, test_input):
        AocLogger.log('test input: {}'.format(test_input))
        return 0

    def solve_part_1(self, puzzle_input: str):
        puzzle_input = puzzle_input.strip()

        result = 0

        print('part 1 result: {}'.format(result))
        return result

    def solve_test_case_2(self, test_input):
        AocLogger.log('test input: {}'.format(test_input))
        return 0

    def solve_part_2(self, puzzle_input: str):
        puzzle_input = puzzle_input.strip()

        result = 0

        print('part 2 result: {}'.format(result))
        return result





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




