#!/usr/bin/env python3



### IMPORTS ###

import aocd
import re
import parse
import typing
import aoc_util
from aoc_util import AocLogger



### CONSTANTS ###
TEST_INPUT = [
    """
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    4,
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

        puzzle_input = aocd.data
        aoc_util.write_input(puzzle_input, __file__)

        AocLogger.verbose = True
        self.test_cases()

        AocLogger.verbose = False
        self.solve_part_1(puzzle_input)
        # self.solve_part_2(puzzle_input)

    def test_cases(self):
        self.verbose = True
        AocLogger.log()
        AocLogger.log('running test cases')

        for test_in, test_out in zip(TEST_INPUT, TEST_OUTPUT_1):
            test_in = test_in.strip()
            if not test_in:
                continue

            # do the test
            aoc_util.assert_equal(
                test_out,
                self.solve_part_1(test_in)
            )

        # for test_in, test_out in zip(TEST_INPUT, TEST_OUTPUT_2):
        #     test_in = test_in.strip()
        #     if not test_in:
        #         continue
        #
        #     # do the test
        #     aoc_util.assert_equal(
        #         test_out,
        #         self.solve_part_2(test_in)
        #     )

        AocLogger.log('all test cases passed')
        AocLogger.log('\n' * 5)

    def solve_part_1(self, puzzle_input):
        """
        Args:
            puzzle_input (string): the input

        Returns: the answer

        algo:
            for each claim
                mark squares
        """
        lines = puzzle_input.strip().split()
        result = 0
        for line in lines:
            line = line.strip()

            # todo: process line here
            AocLogger.log(line)

        print('\npart 1 result: {}'.format(result))
        return result

    def solve_part_2(self, puzzle_input):
        """
        Args:
            puzzle_input (string): the input

        Returns: the answer
        """
        lines = puzzle_input.strip().split('\n')
        result = 0
        for line in lines:
            line = line.strip()

            # todo: process line here
            AocLogger.log(line)

        print('\npart 2 result: {}'.format(result))
        return result





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




