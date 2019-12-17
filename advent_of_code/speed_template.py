#!/usr/bin/env python3



### IMPORTS ###

import numpy as np

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.intcode_computer import IntcodeComputer





### CONSTANTS ###

TEST_INPUT = [
    """

    """, """

    """, """

    """
]





def main():
    print('starting {}'.format(__file__.split('/')[-1]))

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    AocLogger.verbose = True
    run_tests()

    AocLogger.verbose = False
    solve_full_input(puzzle_input)


def run_tests():
    aoc_util.assert_equal(
        42,
        solve_test_case(TEST_INPUT[0])
    )


def solve_test_case(test_input):
    test_input = test_input.strip()
    AocLogger.log('test input:\n{}'.format(test_input))

    result = 0

    print('result: {}'.format(result))
    return result


def solve_full_input(puzzle_input):
    return 0





if __name__ == '__main__':
    main()




