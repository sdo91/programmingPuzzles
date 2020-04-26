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
^WNE$
    """, """
^ENWWW(NEEE|SSE(EE|N))$
    """, """
^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$
    """
]

TEST_OUTPUT_1 = [
    3,
    10,
    18,
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
            print(traceback.format_exc())
            self.puzzle_input = 'unable to get input'
        aoc_util.write_input(self.puzzle_input, __file__)

    def run(self):
        start_time = time.time()

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            4050,
            self.solve_part_1(self.puzzle_input)
        )

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_2(self.puzzle_input)
        # )

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

        part_2_result = solver.p2()

        print('part_2_result: {}\n'.format(part_2_result))
        return part_2_result










class Solver(object):

    def __init__(self, text: str):
        self.text = text.strip()
        AocLogger.log(str(self))

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def process(self, text):
        """
        algo:
            recursively process parens

            eg:
                while there are perens:
                    find open, close
                    pass to func, replace with result

            then process pipes
        """
        # process parens
        while True:
            # '(' in text:
            open_idx = text.find('(')
            if open_idx == -1:
                # no more parens
                break

            # open found
            close_idx = self.find_close_paren(text, open_idx)
            inside = text[open_idx+1:close_idx]
            z=0
            text = text[:open_idx] + self.process(inside) + text[close_idx + 1:]
            z=0

        # process pipes
        routes = text.split('|')
        max_route_len = -1
        max_route = ''
        for route in routes:
            route_len = len(route)
            if route_len == 0:
                # special case: return ''
                return ''
            elif route_len > max_route_len:
                max_route_len = route_len
                max_route = route
        return max_route

    @staticmethod
    def find_close_paren(text, open_idx):
        scope = 1
        i = open_idx
        while True:
            i += 1
            if text[i] == '(':
                scope += 1
            elif text[i] == ')':
                scope -= 1
                assert scope >= 0
                if scope == 0:
                    return i

    def p1(self):
        assert (self.text[0], self.text[-1]) == ('^', '$')
        route = self.process(self.text[1:-1])
        return len(route)

    def p2(self):
        """

        """
        z=0
        return 2










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




