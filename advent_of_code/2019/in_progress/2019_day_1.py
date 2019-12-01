#!/usr/bin/env python3



### IMPORTS ###

import aocd
import re
import parse
import typing
import aoc_util



### CONSTANTS ###
TEST_INPUT = [
    """
1969
    """, """
100756
    """, """

    """
]

TEST_OUTPUT_1 = [
    0,
    0,
    0,
]

TEST_OUTPUT_2 = [
    966,
    50346,
    0,
]





class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def __init__(self):
        self.verbose = True

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        self.verbose = True
        self.test_cases()

        self.verbose = False
        puzzle_input = aocd.data
        self.solve_part_1(puzzle_input)
        self.solve_part_2(puzzle_input)

    def log(self, msg=None, verbose=None):
        if verbose or (verbose is None and self.verbose):
            if msg is None:
                print()
            else:
                print(msg)

    def test_cases(self):
        self.verbose = True
        self.log()
        self.log('running test cases')

        for test_in, test_out in zip(TEST_INPUT, TEST_OUTPUT_2):
            test_in = test_in.strip()
            if not test_in:
                continue

            # do the test
            aoc_util.assert_equal(
                test_out,
                self.solve_part_2(test_in)
            )

        self.log('all test cases passed')
        self.log('\n' * 5)

    def solve_part_1(self, puzzle_input):
        """
        Args:
            puzzle_input (string): the input

        Returns: the answer
        """
        lines = puzzle_input.strip().split()
        result = 0
        for line in lines:
            result += (int(line) // 3) - 2

        print('\npart 1 result: {}'.format(result))
        return result

    def solve_part_2(self, puzzle_input):
        """
        Args:
            puzzle_input (string): the input

        Returns: the answer

        3395944 too low
        5093873 too high
        """
        self.log('\n' * 5)
        lines = puzzle_input.strip().split()
        total_fuel_needed = 0
        for line in lines:
            fuel_needed_this_module = int(line) // 3 - 2
            prev_step_fuel_needed = fuel_needed_this_module

            while True:
                extra_fuel_needed = prev_step_fuel_needed // 3 - 2
                if extra_fuel_needed < 1:
                    break
                self.log(extra_fuel_needed)
                fuel_needed_this_module += extra_fuel_needed
                prev_step_fuel_needed = extra_fuel_needed

            total_fuel_needed += fuel_needed_this_module

        print('\npart 2 result: {}'.format(total_fuel_needed))
        return total_fuel_needed





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




