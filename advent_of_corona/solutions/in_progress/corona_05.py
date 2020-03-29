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

addToPath('../../..')


### IMPORTS ###

import time
import traceback

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger

from advent_of_corona.util import corona_util


### CONSTANTS ###

TEST_INPUT = [
    """
10
2 4 2 6 1 7 8 9 2 1
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    0,
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

        # self.run_tests()

        self.run_real()

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def run_real(self):
        AocLogger.verbose = False

        aoc_util.assert_equal(
            0,
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
        The situation is getting worse, but nothing is lost yet. Someone anonymous has invented a vaccine for the
        coronavirus but as you might know, it is not easy to get it and the government needs to know how many
        vaccines there will be needed. Each citizen has an alpha number that goes between 0 and 100. This alpha
        reflects your contribution to society.

        When giving the vaccines we will follow the following rules:
            Each citizen should be given at least 1 vaccine.
            Between two contiguous citizens, the one that has the greater alpha gets more vaccines.
            The total number of vaccines should be minimal.

        Input
        You’ll get an N followed by N ordered integers in the next line, the citizens alphas.

        Output
        The minimum number of vaccines that follow the given rules.

        Example
        Being N = 10 and citizens = [2, 4, 2, 6, 1, 7, 8, 9, 2, 1].
        We will give                [1, 2, 1, 2, 1, 2, 3, 4, 2, 1] vaccines that has a total of 19.

        NOTE:
            adjacent citizens can have same value

            2 4 6 6 2
            1 2 3 2 1

        algo:
            find local min, assign 1
            in between, repeat recursive, x+1

            reduce until no reductions
        """
        lines = aoc_util.lines(self.text)
        citizens = aoc_util.ints(lines[-1])

        # self.assert_no_twins(citizens)

        # assert no equal


        # given start index, find next local min

        z=0
        return 1

    # def assert_no_twins(self, array):
    #     for x in range(len(array) - 1):
    #         assert array[x] != array[x + 1]

    def reduce(self, array, index):
        """
        set value to min value that is larger


        given A B

        if b is larger
        """

        return 0

    def p2(self):
        """

        """
        z=0
        return 2










if __name__ == '__main__':
    instance = DayManager()
    instance.run()




