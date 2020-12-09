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
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    127,
    0,
    0,
]

TEST_OUTPUT_2 = [
    62,
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
            41682220,
            self.solve_part_1(self.puzzle_input, n=25)
        )

        aoc_util.assert_equal(
            5388976,
            self.solve_part_2(self.puzzle_input, 41682220)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        aoc_util.assert_equal(
            TEST_OUTPUT_2[0],
            self.solve_part_2(TEST_INPUT[0], 127)
        )

    def solve_part_1(self, text: str, n=5):
        solver = Solver(text)

        part_1_result = solver.p1(n)

        print('part_1_result: {}\n'.format(part_1_result))
        return part_1_result

    def solve_part_2(self, text: str, p1_result):
        solver = Solver(text)

        part_2_result = solver.p2(p1_result)

        print('part_2_result: {}\n'.format(part_2_result))
        return part_2_result


class Solver(object):

    def __init__(self, text: str):
        self.text = text.strip()
        AocLogger.log(str(self))
        self.values = aoc_util.ints(self.text)

        # had to check if I needed to handle duplicates or not
        print('has duplicates: {}'.format(aoc_util.has_duplicates(self.values)))

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self, n=5):
        """
        pool is prev 25
        keep as a set
        keep track of line numbers:
            eg: 8: [6, 32]
            when I check to remove 8, it stays
        """
        pool = set()
        lines_by_value = defaultdict(set)

        # preamble
        for x in range(n):
            value = self.values[x]
            lines_by_value[value].add(x)
            pool.add(value)

        # start checking
        for x in range(n, len(self.values)):
            potential_value = self.values[x]
            lines_by_value[potential_value].add(x)

            is_valid = False
            for pool_value in pool:
                difference = potential_value - pool_value

                # check if valid
                if difference != pool_value and difference in pool:
                    # valid
                    is_valid = True
                    if AocLogger.verbose:
                        print('{} + {} = {}'.format(pool_value, difference, potential_value))
                    break

            if not is_valid:
                return potential_value

            # prep for next
            line_to_remove = x - n
            value_to_remove = self.values[line_to_remove]
            lines_by_value[value_to_remove].remove(line_to_remove)
            if lines_by_value[value_to_remove]:
                # will need to handle this edge case if it occurs
                assert False

            pool.remove(value_to_remove)
            pool.add(potential_value)
            assert len(pool) == n

        assert False

    def p2(self, p1_result):
        """
        inchworm
        """
        top_line = 0
        bottom_line = 1
        running_sum = self.values[top_line] + self.values[bottom_line]

        while True:
            if running_sum < p1_result:
                # move bottom down
                bottom_line += 1
                running_sum += self.values[bottom_line]
            elif running_sum > p1_result:
                # move top down
                running_sum -= self.values[top_line]
                top_line += 1
            else:
                # done
                smallest = min(self.values[top_line:bottom_line + 1])
                largest = max(self.values[top_line:bottom_line + 1])
                return smallest + largest


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
