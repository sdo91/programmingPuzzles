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

import itertools
import math
import time
import traceback

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger

### CONSTANTS ###
TEST_INPUT = [
    """
939
7,13,x,x,59,x,31,19
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    295,
    0,
    0,
]

TEST_OUTPUT_2 = [
    1068781,
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
            2045,
            self.solve_part_1(self.puzzle_input)
        )

        aoc_util.assert_equal(
            402251700208309,
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
        self.lines = aoc_util.lines(text)

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        desired_depart = int(self.lines[0])
        bus_ids = aoc_util.ints(self.lines[1])

        best_time = 9e9
        best_id = -1

        for bus_id in bus_ids:
            temp = desired_depart / bus_id
            temp = math.ceil(temp)
            next_depart = temp * bus_id
            if next_depart < best_time:
                best_time = next_depart
                best_id = bus_id

        wait_time = best_time - desired_depart
        return wait_time * best_id

    def p2(self):
        """
        t = 1068781

        A * 7 = t
        B * 13 = t + 1

        for now:
            find times where just 7 and 13 line up
        """

        # prev_t = -1
        # for t in range(0, 1068789, 7):
        #     if t % 13 == 0:
        #         print(t, t - prev_t)
        #         prev_t = t

        bus_ids = aoc_util.tokenize(self.lines[-1], ',')

        best_t = 0
        delta_t = 1

        for i, bus_id in enumerate(bus_ids):
            if bus_id == 'x':
                continue

            for t in itertools.count(best_t, delta_t):
                # check if it works
                if (t + i) % bus_id == 0:
                    # found it
                    best_t = t
                    break

            # check that all still work
            self.sanity_check(i, bus_ids, best_t)

            delta_t *= bus_id

        return best_t

    def sanity_check(self, end_index, bus_ids, best_t):
        for i in range(0, end_index + 1):
            bus_id = bus_ids[i]
            if bus_id == 'x':
                continue
            else:
                mod_value = (best_t + i) % bus_id
                assert mod_value == 0


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
