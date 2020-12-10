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
16
10
15
5
1
11
7
19
6
12
4
    """, """
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
    """, """

    """
]

TEST_OUTPUT_1 = [
    7 * 5,
    22 * 10,
    0,
]

TEST_OUTPUT_2 = [
    8,
    19208,
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
            2400,
            self.solve_part_1(self.puzzle_input)
        )

        aoc_util.assert_equal(
            338510590509056,
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
        self.ints = sorted([0] + aoc_util.ints(self.text))
        self.ints.append(self.ints[-1] + 3)

        self.ways_map = {
            1: 1,
            2: 2,
            3: 4,
            4: 7,
        }

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        """

        """
        counts = defaultdict(int)

        for x in range(len(self.ints) - 1):
            diff = self.ints[x + 1] - self.ints[x]
            if AocLogger.verbose:
                print('{} - {} = {}'.format(self.ints[x + 1], self.ints[x], diff))
            counts[diff] += 1

        return counts[1] * counts[3]

    def p2(self):
        """
        all jumps are either 1 or 3
        both sides of 3 jumps are required

        so it just comes down to the strings of 1 jumps

        ex1:
            15,16 (both required)
            10,11,12 (11 op, so 2)
            4,5,6,7 (5 op, 6 op, so 4)
            2*4 = 8

            1,2,3,4,5 (2 * 2 * 2 - 1) = 7 (can't omit all 3)
        """
        counts = defaultdict(int)

        longest_streak = 0
        current_streak = 0

        num_ways = 1

        for x in range(len(self.ints) - 1):
            diff = self.ints[x + 1] - self.ints[x]
            if AocLogger.verbose:
                print('{} - {} = {}'.format(self.ints[x + 1], self.ints[x], diff))
            counts[diff] += 1

            if diff == 1:
                current_streak += 1
            else:
                # streak broken
                if current_streak > 0:
                    if current_streak > longest_streak:
                        longest_streak = current_streak

                    # update num ways
                    assert current_streak in self.ways_map
                    num_ways *= self.ways_map[current_streak]
                current_streak = 0

        return num_ways


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
