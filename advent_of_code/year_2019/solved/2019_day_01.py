#!/usr/bin/env python3



### IMPORTS ###

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger



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

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        puzzle_input = aocd.data

        AocLogger.verbose = True
        self.test_cases()

        AocLogger.verbose = False
        aoc_util.assert_equal(
            3395944,
            self.solve_part_1(puzzle_input)
        )
        aoc_util.assert_equal(
            5091036,
            self.solve_part_2(puzzle_input)
        )

    def test_cases(self):
        self.verbose = True
        AocLogger.log()
        AocLogger.log('running test cases')

        for test_in, test_out in zip(TEST_INPUT, TEST_OUTPUT_2):
            test_in = test_in.strip()
            if not test_in:
                continue

            # do the test
            aoc_util.assert_equal(
                test_out,
                self.solve_part_2(test_in)
            )

        AocLogger.log('all test cases passed')
        AocLogger.log('\n' * 5)

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
        AocLogger.log('\n' * 5)
        lines = puzzle_input.strip().split()
        total_fuel_needed = 0
        for line in lines:
            fuel_needed_this_module = int(line) // 3 - 2
            prev_step_fuel_needed = fuel_needed_this_module

            while True:
                extra_fuel_needed = prev_step_fuel_needed // 3 - 2
                if extra_fuel_needed < 1:
                    break
                AocLogger.log(extra_fuel_needed)
                fuel_needed_this_module += extra_fuel_needed
                prev_step_fuel_needed = extra_fuel_needed

            total_fuel_needed += fuel_needed_this_module

        print('\npart 2 result: {}'.format(total_fuel_needed))
        return total_fuel_needed





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




