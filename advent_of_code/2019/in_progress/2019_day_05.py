#!/usr/bin/env python3



### IMPORTS ###

import aocd
import re
import parse
import typing
from aoc_util import aoc_util
from aoc_util.intcode_computer import IntcodeComputer
from aoc_util.aoc_util import AocLogger




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

    aoc_util.assert_equal(
        14155342,
        solve_part_1(puzzle_input)
    )

    aoc_util.assert_equal(
        8684145,
        solve_part_2(puzzle_input)
    )






def solve_test_case(test_input):
    AocLogger.log('test input: {}'.format(test_input))

    # intcode_computer.run_intcode(test_input)


    pass

def solve_part_1(puzzle_input):
    codes = aoc_util.ints(puzzle_input)
    computer = IntcodeComputer(codes)
    return computer.run(1)

def solve_part_2(puzzle_input):
    codes = aoc_util.ints(puzzle_input)

    # intcode_computer.run_intcode(
    #     [3,9,8,9,10,9,4,9,99,-1,8],
    #     8
    # )

    computer = IntcodeComputer(codes)
    return computer.run(5)










if __name__ == '__main__':
    main()




