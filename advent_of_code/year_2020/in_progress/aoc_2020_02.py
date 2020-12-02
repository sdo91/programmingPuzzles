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
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    2,
    0,
    0,
]

TEST_OUTPUT_2 = [
    1,
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
            550,
            self.solve_part_1(self.puzzle_input)
        )

        aoc_util.assert_equal(
            0,
            self.solve_part_2(self.puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def solve_part_1(self, text: str):
        solver = Solver(text)

        part_1_result = solver.p1()

        print('part_1_result: {}\n'.format(part_1_result))
        return part_1_result

    def solve_part_2(self, text: str):
        solver = Solver(text)

        part_2_result = solver.p2()

        print('part_2_result: {}\n'.format(part_2_result))
        return part_2_result


class Solver(object):

    def __init__(self, text: str):
        self.text = text.strip()
        AocLogger.log(str(self))
        self.lines = aoc_util.lines(self.text)

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        """

        """

        total = 0
        for line in self.lines:
            line = line.replace(':', '')
            tokens = line.split(' ')

            min_count = int(tokens[0].split('-')[0])
            max_count = int(tokens[0].split('-')[1])

            count = tokens[-1].count(tokens[-2])

            if min_count <= count <= max_count: \
                    total += 1

            z = 0
        return total

    def p2(self):
        """
        682 wrong
        813
        """
        total = 0
        for line in self.lines:
            line = line.replace(':', '')
            tokens = line.split(' ')

            first = int(tokens[0].split('-')[0]) - 1
            second = int(tokens[0].split('-')[1]) - 1

            char = tokens[1]
            pwd = tokens[2]

            try:
                matches = 0
                if pwd[first] == char:
                    matches += 1
                if pwd[second] == char:
                    matches += 1
                if matches == 1:
                    total += 1
            except:
                pass

            z = 0
        return total


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
