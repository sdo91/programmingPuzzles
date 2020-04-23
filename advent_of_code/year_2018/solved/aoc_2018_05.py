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
import typing
import traceback

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger


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
    4,
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

        aoc_util.assert_equal(
            4052,
            self.solve_part_2(puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

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

    def can_react(self, builder: typing.List[str], char: str):
        if not builder:
            return False
        a, b = builder[-1], char
        if a.lower() == b.lower():  # same type
            return a.islower() != b.islower()  # different polarity
        return False

    def p1(self, polymer=''):
        """
        dabAcCaCBAcCcaDA  The first 'cC' is removed.
        dabAaCBAcCcaDA    This creates 'Aa', which is removed.
        dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
        dabCBAcaDA        No further actions can be taken.
        """
        if not polymer:
            polymer = self.text
        builder = []
        for char in polymer:
            if self.can_react(builder, char):
                del builder[-1]  # pop
            else:
                builder.append(char)  # push

        # if AocLogger.verbose:
        #     AocLogger.log('p1 builder: {}'.format(''.join(builder)))
        return len(builder)

    def p2(self):
        """
        Time to improve the polymer.

        One of the unit types is causing problems; it's preventing the polymer from collapsing as much as it should.
        Your goal is to figure out which unit type is causing the most problems, remove all instances of it
        (regardless of polarity), fully react the remaining polymer, and measure its length.

        For example, again using the polymer dabAcCaCBAcCcaDA from above:

        Removing all A/a units produces dbcCCBcCcD      -> dbCBcD, which has length 6.
        Removing all B/b units produces daAcCaCAcCcaDA  -> daCAcaDA, which has length 8.
        Removing all C/c units produces dabAaBAaDA      -> daDA, which has length 4.
        Removing all D/d units produces abAcCaCBAcCcaA  -> abCBAc, which has length 6.
        In this example, removing all C/c units was best, producing the answer 4.

        What is the length of the shortest polymer you can produce by removing all units of exactly one type and
        fully reacting the result?
        """
        if 'z' in self.text:
            last_char = 'z'
        else:
            last_char = 'd'

        min_size = 9e9
        for x in range(ord('a'), ord(last_char) + 1):
            char = chr(x)
            polymer = self.text.replace(char, '')
            polymer = polymer.replace(char.upper(), '')
            size = self.p1(polymer)

            print('{}: {}'.format(char, size))
            if size < min_size:
                min_size = size

        return min_size










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




