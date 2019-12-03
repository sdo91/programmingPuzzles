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

    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    0,
    0,
    0,
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
        self.run_tests()

        AocLogger.verbose = False

        # self.solve_part_1(puzzle_input)

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_1(puzzle_input)
        # )

        # self.solve_part_2(puzzle_input)

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_2(puzzle_input)
        # )

    def run_tests(self):
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def solve_part_1(self, puzzle_input):
        """
        Args:
            puzzle_input (string): the input

        Returns: the answer
        """
        lines = puzzle_input.strip().split('\n')
        result = 1
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
        result = 2
        for line in lines:
            line = line.strip()

            # todo: process line here
            AocLogger.log(line)

        print('\npart 2 result: {}'.format(result))
        return result





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




