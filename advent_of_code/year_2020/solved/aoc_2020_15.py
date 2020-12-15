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
from collections import defaultdict

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger

### CONSTANTS ###
TEST_INPUT = [
    """
0,3,6
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    436,
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
            self.puzzle_input = '8,11,0,19,1,2'
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
            447,
            self.solve_part_1(self.puzzle_input)
        )

        aoc_util.assert_equal(
            11721679,
            self.solve_part_2(self.puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def solve_part_1(self, text: str):
        solver = Solver(text)

        part_1_result = solver.p1()

        print('part_1_result: {}\n'.format(part_1_result))
        return part_1_result

    def solve_part_2(self, text: str):
        solver = Solver(text)

        part_2_result = solver.p1(30000000)

        print('part_2_result: {}\n'.format(part_2_result))
        return part_2_result


class Solver(object):

    def __init__(self, text: str):
        self.text = text.strip()
        # self.lines = aoc_util.lines(text)
        AocLogger.log(str(self))

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self, end=2020):
        ints = aoc_util.ints(self.text)
        turns_by_number = defaultdict(list)

        for i, number in enumerate(ints):
            turn = i + 1
            turns_by_number[number].append(turn)

        prev_number = ints[-1]
        for turn_number in range(len(ints) + 1, end + 1):
            if turn_number % 1000000 == 0:
                print(turn_number)

            prev_turns = turns_by_number[prev_number]
            prev_count = len(prev_turns)

            next_number = 0
            if prev_count > 1:
                next_number = prev_turns[-1] - prev_turns[-2]

            turns_by_number[next_number].append(turn_number)
            while len(turns_by_number[next_number]) > 2:
                turns_by_number[next_number].pop(0)
            prev_number = next_number

        print('len turns_by_number: {}'.format(len(turns_by_number)))
        return prev_number


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
