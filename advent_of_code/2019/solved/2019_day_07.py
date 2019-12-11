#!/usr/bin/env python3



### IMPORTS ###

import aocd
from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.intcode_computer import IntcodeComputer

from itertools import permutations



### CONSTANTS ###

TEST_INPUT_1 = [
    ([4,3,2,1,0],[3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]),
    ([0,1,2,3,4],[3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]),
    ([1,0,4,3,2],[3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0])
]

TEST_OUTPUT_1 = [
    43210,
    54321,
    65210,
]

TEST_INPUT_2 = [
    (
        [9,8,7,6,5],
        [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    ),
    (
        [9,7,8,5,6],
        [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    ),
]

TEST_OUTPUT_2 = [
    139629729,
    18216,
]









def main():
    print('starting {}'.format(__file__.split('/')[-1]))

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    AocLogger.verbose = True
    aoc_util.run_tests(solve_test_case_1, TEST_INPUT_1, TEST_OUTPUT_1)
    aoc_util.run_tests(solve_test_case_2, TEST_INPUT_2, TEST_OUTPUT_2)

    AocLogger.verbose = False

    aoc_util.assert_equal(
        437860,
        solve_full_input_1(puzzle_input)
    )

    aoc_util.assert_equal(
        49810599,
        solve_full_input_2(puzzle_input)
    )


def solve_test_case_1(test_input):
    AocLogger.log('test input: {}'.format(test_input))

    phase_settings = test_input[0]
    init_mem = test_input[1]

    comp = IntcodeComputer(init_mem)

    prev_out = 0
    for i in range(5):
        AocLogger.log('\ni: {}'.format(i))
        AocLogger.log('inputs: {}'.format([phase_settings[i], prev_out]))
        AocLogger.log('prev_out: {}'.format(prev_out))

        comp.reset()
        comp.queue_input(phase_settings[i])
        comp.queue_input(prev_out)
        prev_out = comp.run_to_halt()

    AocLogger.log('result 1: {}'.format(prev_out))
    return prev_out


def solve_test_case_2(test_input):
    AocLogger.log('test input: {}'.format(test_input))

    phase_settings = test_input[0]
    init_mem = test_input[1]

    amps = []
    for i in range(5):
        amps.append(IntcodeComputer(init_mem))
        amps[-1].queue_input(phase_settings[i])

    prev_out = 0
    i = 0
    while True:
        AocLogger.log('prev_out: {}'.format(prev_out))
        amps[i].queue_input(prev_out)
        ic_state = amps[i].run()

        if ic_state == IntcodeComputer.STATE_HALTED:
            break
        prev_out = amps[i].get_latest_output()

        i += 1
        i %= 5

    AocLogger.log('result 2: {}'.format(prev_out))
    return prev_out


def solve_full_input_1(puzzle_input):
    puzzle_input = puzzle_input.strip()
    codes = aoc_util.ints(puzzle_input)
    perms = list(permutations([0,1,2,3,4]))

    result = 0
    for perm in perms:
        test_in = (
            perm,
            codes.copy()
        )

        perm_result = solve_test_case_1(test_in)
        result = max(result, perm_result)

    print(result)
    return result


def solve_full_input_2(puzzle_input):
    """
    incorrect:
    87572

    1:25 minutes
    rank 872 (part 2)

    :param puzzle_input:
    :return:
    """
    puzzle_input = puzzle_input.strip()
    codes = aoc_util.ints(puzzle_input)
    perms = list(permutations([5,6,7,8,9]))

    result = 0
    for perm in perms:
        test_in = (
            perm,
            codes.copy()
        )

        perm_result = solve_test_case_2(test_in)
        result = max(result, perm_result)

    print(result)
    return result





if __name__ == '__main__':
    main()




