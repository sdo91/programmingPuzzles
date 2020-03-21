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
import traceback

from advent_of_code.aoc_util import aoc_util
from advent_of_code.aoc_util.aoc_util import AocLogger

from advent_of_corona.util import corona_util


### CONSTANTS ###

TEST_INPUT = [
    """
1 2 3 4 1 2 3
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    4,
    0,
    0,
]

TEST_OUTPUT_2 = [
    0,
    0,
    0,
]










class DayManager(object):

    def __init__(self):
        try:
            self.puzzle_input = corona_util.read_input(__file__)
        except:
            self.puzzle_input = traceback.format_exc()
            print(self.puzzle_input)

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))
        start_time = time.time()

        self.run_tests()

        self.run_real()

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def run_real(self):
        aoc_util.assert_equal(
            5,
            self.solve_part_1(self.puzzle_input)
        )

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_2(self.puzzle_input)
        # )

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

    def p1(self):
        """
        As today is the first day, we will begin a really simple problem. One of the most important things to do
        while you are under confinement is staying at home, so this will be a I'm not a robot test.

        You are given several natural numbers. Find the longest subsequence that fulfills the following rules:
            The resulting sequence must be increasing
            There cannot be two even numbers together nor two odd numbers together

        Write a program such that, prints the length of the longest sequence that can be produced according to the
        rules above using the numbers on that line.

        Input
        Input consists of a sequence of natural numbers.

        Output
        The length of the longest (an integer) sequence that can be made according to the rules given above.

        Example
        With an input 1 2 3 4 1 2 3 the program should generate the output 4.
        """

        sequence = aoc_util.ints(self.text)

        max_subsequence_len = 0
        current_subsequence_len = 0

        prev = None
        for x in sequence:
            # check that x obeys the rules
            if prev is None:
                # first number in seq always valid
                is_valid = True
            else:
                is_valid = self.is_increasing(prev, x) and self.is_even_odd(prev, x)

            if is_valid:
                current_subsequence_len += 1
                max_subsequence_len = max(max_subsequence_len, current_subsequence_len)
            else:
                # reset
                current_subsequence_len = 1

            prev = x

        return max_subsequence_len

    @classmethod
    def is_increasing(cls, a, b):
        return b > a

    @classmethod
    def is_even(cls, x):
        return x % 2 == 0

    @classmethod
    def is_even_odd(cls, a, b):
        return cls.is_even(a) != cls.is_even(b)

    def p2(self):
        """

        """
        z=0
        return 2










if __name__ == '__main__':
    instance = DayManager()
    instance.run()




