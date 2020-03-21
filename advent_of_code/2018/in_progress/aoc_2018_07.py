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
from collections import defaultdict

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger


### CONSTANTS ###
TEST_INPUT = [
    """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    'CABDFE',
    '',
    '',
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
            'OUGLTKDJVBRMIXSACWYPEQNHZF',
            self.solve_part_1(puzzle_input)
        )

        aoc_util.assert_equal(
            0,
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
        self.lines = aoc_util.lines(self.text)

        # parse dependencies
        self.dependencies = defaultdict(set)
        self.all_steps = set()
        for line in self.lines:
            first, second = self.get_steps(line)
            self.dependencies[second].add(first)
            self.all_steps.add(first)
            self.all_steps.add(second)

        AocLogger.log(str(self))

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        """
        Step C must be finished before step A can begin.
        Step C must be finished before step F can begin.
        Step A must be finished before step B can begin.
        Step A must be finished before step D can begin.
        Step B must be finished before step E can begin.
        Step D must be finished before step E can begin.
        Step F must be finished before step E can begin.

        CABDFE
        """
        # pick order
        steps_done = set()
        steps_order = []
        ord_a = ord('A')
        while self.all_steps - steps_done:
            x = ord_a
            while True:
                char = chr(x)
                x += 1
                if char in steps_done:
                    continue
                if not (self.dependencies[char] - steps_done):
                    # all dependencies done, this is the next step
                    steps_order.append(char)
                    steps_done.add(char)
                    break

        return ''.join(steps_order)

    def get_steps(self, line):
        tokens = line.split()
        return tokens[1], tokens[-3]

    def p2(self):
        """
        Second   Worker 1   Worker 2   Done
           0        C          .
           1        C          .
           2        C          .
           3        A          F       C
           4        B          F       CA
           5        B          F       CA
           6        D          F       CAB
           7        D          F       CAB
           8        D          F       CAB
           9        D          .       CABF
          10        E          .       CABFD
          11        E          .       CABFD
          12        E          .       CABFD
          13        E          .       CABFD
          14        E          .       CABFD
          15        .          .       CABFDE
        """
        num_workers = 2
        base_step_time = 0

        z=0

        return 2










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




