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
9
    """, """
51589
    """, """
15891
    """
]

TEST_OUTPUT_1 = [
    5158916779,
    0,
    0,
    0,
]

TEST_OUTPUT_2 = [
    0,
    9,
    10,
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
            3656126723,
            self.solve_part_1(puzzle_input)
        )

        aoc_util.assert_equal(
            20333868,
            self.solve_part_2(puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True

        aoc_util.assert_equal(
            TEST_OUTPUT_1[0],
            self.solve_part_1(TEST_INPUT[0])
        )

        aoc_util.assert_equal(
            TEST_OUTPUT_2[1],
            self.solve_part_2(TEST_INPUT[1])
        )

        aoc_util.assert_equal(
            TEST_OUTPUT_2[2],
            self.solve_part_2(TEST_INPUT[2])
        )

    def solve_part_1(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_1_result = solver.p1()

        print('part_1_result: {}\n'.format(part_1_result))
        return part_1_result

    def solve_part_2(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_2_result = solver.p2()

        print('part_2_result: {}\n'.format(part_2_result))
        return part_2_result










class Solver(object):

    def __init__(self, text: str):
        self.text = text.strip()

        self.scoreboard = [3, 7]
        self.elf_1_idx = 0
        self.elf_2_idx = 1

        AocLogger.log(str(self))

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def iterate(self):
        # create new recipes
        recipe_sum = self.scoreboard[self.elf_1_idx] + self.scoreboard[self.elf_2_idx]
        if recipe_sum < 10:
            self.scoreboard.append(recipe_sum)
        else:
            self.scoreboard += aoc_util.digits(recipe_sum)

        # move
        self.elf_1_idx += (1 + self.scoreboard[self.elf_1_idx])
        self.elf_1_idx %= len(self.scoreboard)
        self.elf_2_idx += (1 + self.scoreboard[self.elf_2_idx])
        self.elf_2_idx %= len(self.scoreboard)

    def p1(self):
        num_practice_recipes = int(self.text)
        NUM_RESULT_DIGITS = 10

        while len(self.scoreboard) < num_practice_recipes + NUM_RESULT_DIGITS:
            self.iterate()

        result = int(aoc_util.join_ints(self.scoreboard[-NUM_RESULT_DIGITS:]))
        return result

    def p2(self):
        goal_digits = aoc_util.digits(self.text)
        N = len(goal_digits)

        result = 0
        while not result:
            self.iterate()

            # check end
            almost_last_n = self.scoreboard[-(N+1):-1]
            last_n = self.scoreboard[-N:]

            if almost_last_n == goal_digits:
                result = len(self.scoreboard) - (N+1)
            elif last_n == goal_digits:
                result = len(self.scoreboard) - N

        return result










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




