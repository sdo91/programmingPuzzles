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
from advent_of_code.util.grid_2d import Grid2D

### CONSTANTS ###
TEST_INPUT = [
    """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    5,
    0,
    0,
]

TEST_OUTPUT_2 = [
    8,
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
            1548,
            self.solve_part_1(self.puzzle_input)
        )

        aoc_util.assert_equal(
            1375,
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


class GameConsole:

    def __init__(self, lines):
        self.accumulator = 0
        self.lines = lines

    def run(self):
        already_run = set()
        i = 0
        while True:
            if i in already_run:
                return False
            if i >= len(self.lines):
                return True
            already_run.add(i)

            intruction, arg = aoc_util.tokenize(self.lines[i])
            if intruction == 'acc':
                self.accumulator += arg
            elif intruction == 'jmp':
                i += (arg - 1)
            i += 1


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
        lines = aoc_util.lines(self.text)
        hgc = GameConsole(lines)
        hgc.run()
        return hgc.accumulator

    def p2(self):
        """

        """
        lines = aoc_util.lines(self.text)

        for i in range(len(lines)):
            # make the change
            og_line = lines[i]
            if 'jmp' in og_line:
                lines[i] = og_line.replace('jmp', 'nop')
            elif 'nop' in og_line:
                lines[i] = og_line.replace('nop', 'jmp')
            else:
                continue

            # see if it halts
            hgc = GameConsole(lines)
            halted = hgc.run()
            if halted:
                return hgc.accumulator

            # restore
            lines[i] = og_line


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
