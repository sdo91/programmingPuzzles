#!/usr/bin/env python3

def addToPath(relPath):
    from os import path
    import sys
    dirOfThisFile = path.dirname(path.realpath(__file__))
    dirToAdd = path.normpath(path.join(dirOfThisFile, relPath))
    if dirToAdd not in sys.path:
        print('adding to path: {}'.format(dirToAdd))
        sys.path.insert(0, dirToAdd)
    else:
        print('already in path: {}'.format(dirToAdd))

addToPath('../..')

### IMPORTS ###

import time
import typing
import traceback
# import numpy as np

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger


### CONSTANTS ###
TEST_INPUT = [
    """
dabAcCaCBAcCcaDA
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    10,
    0,
    0,
]

TEST_OUTPUT_2 = [
    0,
    0,
    0,
]










class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))
        start_time = time.time()

        try:
            puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            print(traceback.format_exc())
            puzzle_input = 'unable to get input'
        aoc_util.write_input(puzzle_input, __file__)

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            9238,
            self.solve_part_1(puzzle_input)
        )

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_2(puzzle_input)
        # )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def solve_part_1(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_1_result = solver.p1()

        print('part_1_result: {}'.format(part_1_result))
        return part_1_result

    def solve_part_2(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_2_result = solver.p2()

        print('part_2_result: {}'.format(part_2_result))
        return part_2_result










class Solver(object):

    def __init__(self, text: str):
        self.text = text.strip()
        AocLogger.log(str(self))

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def can_react(self, chars: typing.List[str], x: int):
        if x+1 >= len(chars):
            return False
        a, b = chars[x], chars[x+1]
        if a.lower() == b.lower():  # same type
            return a.islower() != b.islower()  # different polarity
        return False

    def p1(self):
        """
        dabAcCaCBAcCcaDA  The first 'cC' is removed.
        dabAaCBAcCcaDA    This creates 'Aa', which is removed.
        dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
        dabCBAcaDA        No further actions can be taken.
        """
        prev = [x for x in self.text]
        is_changed = True
        while is_changed:
            builder = []
            is_changed = False
            x = 0
            while x < len(prev):
                if not self.can_react(prev, x):
                    # keep char
                    builder.append(prev[x])
                    x += 1
                else:
                    # destroy 2 chars
                    x += 2
                    is_changed = True
            prev = builder

        AocLogger.log('p1: {}'.format(prev))
        return len(prev)

    def p2(self):
        """

        """
        return 2










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




