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
[1002,4,3,3,33], [3,0,4,0,99], ''
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
    # aoc_util.run_tests(solve_test_case, TEST_INPUT, TEST_OUTPUT)

    # solve_test_case(TEST_INPUT[0])

    AocLogger.verbose = False

    solve_full_input(puzzle_input)






def solve_test_case(test_input):
    AocLogger.log('test input: {}'.format(test_input))

    aoc_util.run_intcode(test_input)


    pass

def solve_full_input(puzzle_input):

    codes = aoc_util.ints(puzzle_input)


    # aoc_util.run_intcode(codes, 1)
    aoc_util.run_intcode(codes, 5)

    # aoc_util.run_intcode(
    #     [3,9,8,9,10,9,4,9,99,-1,8],
    #     8
    # )



    pass





if __name__ == '__main__':
    main()




