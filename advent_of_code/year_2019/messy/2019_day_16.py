#!/usr/bin/env python3



### IMPORTS ###

import aocd
from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger

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

    aoc_util.assert_equal(
        '96136976',
        solve_part_1(puzzle_input)
    )

    aoc_util.assert_equal(
        '85600369',
        solve_part_2(puzzle_input)
    )


def run_tests():
    aoc_util.assert_equal(
        '01029498',
        test_part_1(TEST_INPUT[0], 4)
    )

    aoc_util.assert_equal(
        '24176176',
        test_part_1(TEST_INPUT[1], 100)
    )

    aoc_util.assert_equal(
        '84462026',
        solve_part_2('03036732577212944063491565474664')
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


def keep_ones(value):
    if value > 0:
        return value % 10
    else:
        return (-value) % 10


def test_part_1(test_input, num_phases):
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
                sum_ += product
            new_digits.append(keep_ones(sum_))

        digits = new_digits
        AocLogger.log('phase {}: {}'.format(phase, digits))

    result = ''.join([str(x) for x in digits])

    print(result)
    return result[:8]


def solve_part_1(puzzle_input):
    print(len(puzzle_input))
    return test_part_1(puzzle_input, 100)


def solve_part_2(puzzle_input):
    """
    --- Part Two ---
    Now that your FFT is working, you can decode the real signal.

    The real signal is your puzzle input repeated 10000 times. Treat this new signal as a single input list. Patterns
    are still calculated as before, and 100 phases of FFT are still applied.

    The first seven digits of your initial input signal also represent the message offset. The message offset is the
    location of the eight-digit message in the final output list. Specifically, the message offset indicates the
    number of digits to skip before reading the eight-digit message. For example, if the first seven digits of your
    initial input signal were 1234567, the eight-digit message would be the eight digits after skipping 1,234,
    567 digits of the final output list. Or, if the message offset were 7 and your final output list were
    98765432109876543210, the eight-digit message would be 21098765. (Of course, your real message offset will be a
    seven-digit number, not a one-digit number like 7.)

    Here is the eight-digit message in the final output list after 100 phases. The message offset given in each input
    has been highlighted. (Note that the inputs given below are repeated 10000 times to find the actual starting
    input lists.)

    03036732577212944063491565474664 becomes 84462026.
    02935109699940807407585447034323 becomes 78725270.
    03081770884921959731165446850517 becomes 53553731.

    After repeating your input signal 10000 times and running 100 phases of FFT, what is the eight-digit message
    embedded in the final output list?
    """
    puzzle_input = puzzle_input.strip()

    num_to_skip = int(puzzle_input[:7])

    puzzle_input *= 10000
    num_digits_large = len(puzzle_input)
    puzzle_input = puzzle_input[num_to_skip:]
    num_digits_small = len(puzzle_input)

    # do some checks
    assert num_to_skip > num_digits_large / 2
    assert num_to_skip + num_digits_small == num_digits_large

    digits = [int(x) for x in puzzle_input]
    prev_digits = digits.copy()

    for iteration in range(100):
        print(iteration)
        prev_digits, digits = digits, prev_digits
        running_sum = 0
        for i in range(num_digits_small - 1, -1, -1):
            running_sum += prev_digits[i]
            running_sum = keep_ones(running_sum)
            digits[i] = running_sum

    first_8 = ''.join([str(x) for x in digits[:8]])
    print(first_8)
    return first_8





if __name__ == '__main__':
    main()




