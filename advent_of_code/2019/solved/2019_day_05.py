#!/usr/bin/env python3



### IMPORTS ###

import aocd
from aoc_util import aoc_util
from aoc_util.intcode_computer import IntcodeComputer
from aoc_util.aoc_util import AocLogger




### CONSTANTS ###

TEST_INPUT_2 = [
    ([3,9,8,9,10,9,4,9,99,-1,8],7),
    ([3,9,8,9,10,9,4,9,99,-1,8],8),
    ([3,9,8,9,10,9,4,9,99,-1,8],9),

    ([3,9,7,9,10,9,4,9,99,-1,8],7),
    ([3,9,7,9,10,9,4,9,99,-1,8],8),

    ([3,3,1108,-1,8,3,4,3,99],7),
    ([3,3,1108,-1,8,3,4,3,99],8),
    ([3,3,1108,-1,8,3,4,3,99],9),

    ([3,3,1107,-1,8,3,4,3,99],7),
    ([3,3,1107,-1,8,3,4,3,99],8),

    ([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],0),
    ([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],42),

    ([3,3,1105,-1,9,1101,0,0,12,4,12,99,1],0),
    ([3,3,1105,-1,9,1101,0,0,12,4,12,99,1],42),

    ([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],7),
    ([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],8),
    ([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],9),
]

TEST_OUTPUT_2 = [
    0,
    1,
    0,

    1,
    0,

    0,
    1,
    0,

    1,
    0,

    0,
    1,

    0,
    1,

    999,
    1000,
    1001,
]









def main():
    print('starting {}'.format(__file__.split('/')[-1]))

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    AocLogger.verbose = True
    aoc_util.run_tests(solve_test_case_2, TEST_INPUT_2, TEST_OUTPUT_2)

    AocLogger.verbose = False

    aoc_util.assert_equal(
        14155342,
        solve_part_1(puzzle_input)
    )

    aoc_util.assert_equal(
        8684145,
        solve_part_2(puzzle_input)
    )


def solve_part_1(puzzle_input):
    codes = aoc_util.ints(puzzle_input)
    computer = IntcodeComputer(codes)
    return computer.run_to_halt(1)


def solve_test_case_2(test_input):
    AocLogger.log('test input: {}'.format(test_input))
    codes = test_input[0]
    input_value = test_input[1]

    computer = IntcodeComputer(codes)
    return computer.run_to_halt(input_value)


def solve_part_2(puzzle_input):
    codes = aoc_util.ints(puzzle_input)
    return solve_test_case_2((codes, 5))










if __name__ == '__main__':
    main()




