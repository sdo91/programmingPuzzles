#!/usr/bin/env python3



### IMPORTS ###

import time
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
    start_time = time.time()

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    AocLogger.verbose = True
    run_tests()

    AocLogger.verbose = False
    aoc_util.assert_equal(
        0,
        solve_part_1(puzzle_input)
    )

    elapsed_time = time.time() - start_time
    print('elapsed_time: {:.2f} sec'.format(elapsed_time))


def run_tests():
    aoc_util.assert_equal(
        42,
        solve_test_case(TEST_INPUT[0])
    )


def solve_test_case(test_input):
    test_input = test_input.strip()
    AocLogger.log('test_input:\n{}'.format(test_input))

    result = 0

    print('solve_test_case: {}'.format(result))
    return result


def solve_part_1(puzzle_input):
    puzzle_input = puzzle_input.strip()
    AocLogger.log('puzzle_input:\n{}'.format(puzzle_input))

    result = 0

    print('solve_part_1: {}'.format(result))
    return result





if __name__ == '__main__':
    main()




