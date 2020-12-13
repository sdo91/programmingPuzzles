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

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger

### CONSTANTS ###
TEST_INPUT = [
    """
FBFBBFFRLR
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    357,
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

    def __init__(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        try:
            self.puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            error_msg = traceback.format_exc()
            print(error_msg)
            self.puzzle_input = 'unable to get input:\n\n{}'.format(error_msg)
        aoc_util.write_input(self.puzzle_input, __file__)

    def run(self):
        start_time = time.time()

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            842,
            self.solve_part_1(self.puzzle_input)
        )

        aoc_util.assert_equal(
            617,
            self.solve_part_2(self.puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def solve_part_1(self, text: str):
        lines = aoc_util.lines(text)
        high = 0

        for line in lines:
            solver = Solver(line)
            id = solver.p1()
            if id > high:
                high = id

        part_1_result = high
        print('part_1_result: {}\n'.format(part_1_result))
        return part_1_result

    def solve_part_2(self, text: str):
        lines = aoc_util.lines(text)
        all_ids = set()

        for line in lines:
            solver = Solver(line)
            id = solver.p1()
            assert id not in all_ids
            all_ids.add(id)

        all_ids = sorted(all_ids)
        part_2_result = None
        for x in aoc_util.range_len(all_ids):
            if all_ids[x] + 2 == all_ids[x + 1]:
                part_2_result = all_ids[x] + 1
                break

        print('part_2_result: {}\n'.format(part_2_result))
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

        """
        low = 0
        high = 127
        left = 0
        right = 7

        for c in self.text:
            mid_row = (low + high) // 2
            mid_col = (left + right) // 2

            if c == 'F':
                # lower
                high = mid_row
            elif c == 'B':
                # take upper
                low = mid_row + 1
            elif c == 'L':
                # take left
                right = mid_col
            elif c == 'R':
                # take right
                left = mid_col + 1

        mid_row = (low + high) // 2
        mid_col = (left + right) // 2

        return mid_row * 8 + mid_col

    def p2(self):
        """

        """
        z = 0
        return 2


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
