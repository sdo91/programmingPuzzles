#!/usr/bin/env python3



### IMPORTS ###

import aocd
import re
import parse
import typing
from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.intcode_computer import IntcodeComputer

from itertools import permutations



### CONSTANTS ###

# TEST_INPUT = [
#     ([4,3,2,1,0],[3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]),
#
#     # ([0,1,2,3,4],[3,23,3,24,1002,24,10,24,1002,23,-1,23,
# # 101,5,23,23,1,24,23,23,4,23,99,0,0]),
# #
# #     ([1,0,4,3,2],[3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
# # 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0])
# ]
#
# TEST_OUTPUT = [
#     43210,
#     # 55555,
#     # 55555,
# ]

TEST_INPUT = [
    (
        [9,8,7,6,5],
        [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    ),

    # ([0,1,2,3,4],[3,23,3,24,1002,24,10,24,1002,23,-1,23,
# 101,5,23,23,1,24,23,23,4,23,99,0,0]),
#
#     ([1,0,4,3,2],[3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
# 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0])
]

TEST_OUTPUT = [
    139629729,
    # 55555,
    # 55555,
]









def main():
    print('starting {}'.format(__file__.split('/')[-1]))

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    AocLogger.verbose = True
    aoc_util.run_tests(solve_test_case_2, TEST_INPUT, TEST_OUTPUT)

    AocLogger.verbose = False

    # solve_full_input(puzzle_input)

    aoc_util.assert_equal(
        49810599,
        solve_full_input(puzzle_input)
    )






# def solve_test_case(test_input):
#     AocLogger.log('test input: {}'.format(test_input))
#
#     phase_settings = test_input[0]
#     init_mem = test_input[1]
#
#     # test_input = aoc_util.ints(test_input)
#
#     # ic_in = [4,3,2,1,0]
#     # ic_in = [3,0]
#
#     comp = IntcodeComputer(init_mem)
#
#     prev_out = 0
#     for i in range(5):
#         in_list = [phase_settings[i], prev_out]
#         AocLogger.log('in_list: {}'.format(in_list))
#         prev_out = comp.run(in_list)
#         AocLogger.log('prev_out: {}'.format(prev_out))
#
#
#     return prev_out

def solve_test_case_2(test_input):
    AocLogger.log('test input: {}'.format(test_input))

    phase_settings = test_input[0]
    init_mem = test_input[1]

    # test_input = aoc_util.ints(test_input)

    # ic_in = [4,3,2,1,0]
    # ic_in = [3,0]

    amps = []
    for i in range(5):
        amps.append(IntcodeComputer(init_mem))
        amps[-1].queue_input(phase_settings[i])

    prev_out = 0
    i = 0
    is_first_loop = True
    while True:
        # if is_first_loop:
        #     in_list = [phase_settings[i], prev_out]
        # else:
        #     in_list = [prev_out]

        # AocLogger.log('in_list: {}'.format(in_list))
        # ic_out = amps[i].run(in_list)

        amps[i].queue_input(prev_out)
        ic_out = amps[i].run()

        if ic_out == 'HALT':
            break
        prev_out = ic_out


        AocLogger.log('prev_out: {}'.format(prev_out))

        i += 1

        if i >= 5:
            i = 0
            is_first_loop = False


    return prev_out




def solve_full_input(puzzle_input):
    """
    87572

    1:25 minutes
    rank 872 (part 2)

    :param puzzle_input:
    :return:
    """
    puzzle_input = puzzle_input.strip()

    codes = aoc_util.ints(puzzle_input)


    # perms = list(permutations([0,1,2,3,4]))
    perms = list(permutations([5,6,7,8,9]))



    result = 0

    for perm in perms:

        test_in = (
            perm,
            codes.copy()
        )

        # perm_result = solve_test_case(test_in)
        perm_result = solve_test_case_2(test_in)

        result = max(result, perm_result)

    z=0
    pass

    print(result)

    return result





if __name__ == '__main__':
    main()




