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
    """
1,9,10,3,2,3,11,0,99,30,40,50
    """, """
1,0,0,0,99
    """, """
2,3,0,3,99
    """, """
2,4,4,5,99,0
    """, """
1,1,1,4,99,5,6,0,99
    """
]

TEST_OUTPUT_1 = [
    [3500, 9, 10, 70,
    2, 3, 11, 0,
    99,
    30, 40, 50],

    [2,0,0,0,99],

    [2,3,0,6,99],
    [2,4,4,5,99,9801],
    [30,1,1,4,2,5,6,0,99],
]





class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        puzzle_input = aocd.data
        aoc_util.write_input(puzzle_input, __file__)

        AocLogger.verbose = True
        self.run_tests()

        AocLogger.verbose = False
        aoc_util.assert_equal(
            3850704,
            self.solve_part_1(puzzle_input, 12, 2, verbose=True)[0]
        )
        aoc_util.assert_equal(
            6718,
            self.solve_part_2(puzzle_input)
        )

    def run_tests(self):
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)

    def solve_part_1(self, puzzle_input, first=None, second=None, verbose=False):
        """
        Args:
            puzzle_input (string): the input

        Returns: the answer
        """
        codes = aoc_util.ints(puzzle_input)

        if first is not None:
            codes[1] = first
            codes[2] = second

        i = 0
        while True:
            opcode = codes[i]

            if opcode == 99:
                break
            elif opcode == 1:
                # add
                a_index = codes[i+1]
                b_index = codes[i+2]
                dest_index = codes[i+3]
                codes[dest_index] = codes[a_index] + codes[b_index]
            elif opcode == 2:
                # mult
                a_index = codes[i+1]
                b_index = codes[i+2]
                dest_index = codes[i+3]
                codes[dest_index] = codes[a_index] * codes[b_index]
            else:
                raise RuntimeError('bad opcode')

            i += 4

        if verbose:
            print('\npart 1 result: {}'.format(codes[0]))
        return codes

    def solve_part_2(self, puzzle_input):
        """
        Args:
            puzzle_input (string): the input

        Returns: the answer
        """
        result = 0
        for i in range(99):
            for j in range(99):
                possible = self.solve_part_1(puzzle_input, i, j)
                if possible[0] == 19690720:
                    result = 100 * i + j
                    print('\npart 2 result: 100 * {} + {} = {}'.format(
                        i, j, result))
                    break

        return result







if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




