#!/usr/bin/env python3



### IMPORTS ###

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.intcode_computer import IntcodeComputer



### CONSTANTS ###
TEST_INPUT_1 = [
    [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99],
    [1102,34915192,34915192,7,4,7,99,0],
    [104,1125899906842624,99],
]





class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        try:
            puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            puzzle_input = 'unable to get input'
        aoc_util.write_input(puzzle_input, __file__)

        AocLogger.verbose = True

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            3454977209,
            self.solve_puzzle(puzzle_input, 1)
        )

        aoc_util.assert_equal(
            50120,
            self.solve_puzzle(puzzle_input, 2)
        )

    def run_tests(self):
        # test 0
        ic = IntcodeComputer(TEST_INPUT_1[0])
        ic.run_to_halt()

        aoc_util.assert_equal(
            TEST_INPUT_1[0],
            ic.get_all_output()
        )

        # test 1
        ic = IntcodeComputer(TEST_INPUT_1[1])

        aoc_util.assert_equal(
            34915192**2,
            ic.run_to_halt()
        )

        # test 2
        ic = IntcodeComputer(TEST_INPUT_1[2])

        aoc_util.assert_equal(
            TEST_INPUT_1[2][1],
            ic.run_to_halt()
        )

    def solve_puzzle(self, puzzle_input, intcode_input):
        """
        0:45
        922/879
        """
        print('\nsolving...')
        codes = aoc_util.ints(puzzle_input.strip())
        ic = IntcodeComputer(codes)
        ic.queue_input(intcode_input)
        result = ic.run_to_halt()
        return result





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




