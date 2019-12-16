#!/usr/bin/env python3



### IMPORTS ###

import aocd
import re
import parse
import typing
from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger

import numpy as np




### CONSTANTS ###

TEST_INPUT = [
    """
12345678
    """, """
80871224585914546619083218645595
    """, """

    """
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



def main():
    print('starting {}'.format(__file__.split('/')[-1]))

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    AocLogger.verbose = True
    # aoc_util.run_tests(solve_test_case, TEST_INPUT, TEST_OUTPUT)
    run_tests()

    # AocLogger.verbose = False

    solve_full_input(puzzle_input)




def run_tests():
    aoc_util.assert_equal(
        '01029498',
        solve_test_case(TEST_INPUT[0], 4)
    )
    aoc_util.assert_equal(
        '24176176',
        solve_test_case(TEST_INPUT[1], 100)
    )

def calc_pattern(idx, num_digits):
    pattern = [0, 1, 0, -1]
    p_idx = 0
    result = []
    is_done = False
    while not is_done:
        for x in range(idx + 1):
            result.append(pattern[p_idx])
            if len(result) > num_digits:
                is_done = True
                break
        p_idx = (p_idx + 1) % 4
    del result[0]
    return np.array(result)


# def f(i, digit, pattern):
#     product = digit * pattern[i]
#     return product % 10


def keepOnes(value):
    if value > 0:
        return value % 10
    else:
        return (-value) % 10


def solve_test_case(test_input, num_phases):
    test_input = test_input.strip()
    AocLogger.log('test input: {}'.format(test_input))

    digits = np.array([int(x) for x in test_input])
    num_digits = len(digits)

    patterns = []
    for i in range(num_digits):
        patterns.append(calc_pattern(i, num_digits))

    for phase in range(1, num_phases + 1):

        new_digits = []

        for out_digit in range(num_digits):

            sum_ = 0
            for in_digit in range(num_digits):
                pattern = patterns[out_digit]
                product = digits[in_digit] * pattern[in_digit]
                # product = keepOnes(product)
                sum_ += product
            new_digits.append(keepOnes(sum_))


        digits = new_digits
        AocLogger.log('phase {}: {}'.format(phase, digits))

    result = ''.join([str(x) for x in digits])

    z=0

    print(result)
    return result[:8]

def solve_full_input(puzzle_input):

    # puzzle_input *= 10000

    print(len(puzzle_input))

    return solve_test_case(puzzle_input, 100)







if __name__ == '__main__':
    main()




