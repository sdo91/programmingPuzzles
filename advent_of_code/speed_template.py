#!/usr/bin/env python3



### IMPORTS ###

import aocd
import re
import parse
import typing
from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger




### CONSTANTS ###

TEST_INPUT = [
    """

    """, """

    """, """

    """
]

TEST_OUTPUT = [
    0,
    0,
    0,
]







def main():
    print('starting {}'.format(__file__.split('/')[-1]))

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    AocLogger.verbose = True
    aoc_util.run_tests(solve_test_case, TEST_INPUT, TEST_OUTPUT)

    AocLogger.verbose = False

    solve_full_input(puzzle_input)






def solve_test_case(test_input):
    AocLogger.log('test input: {}'.format(test_input))



    pass

def solve_full_input(puzzle_input):




    pass





if __name__ == '__main__':
    main()




