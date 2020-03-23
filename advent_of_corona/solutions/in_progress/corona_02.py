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
from itertools import permutations

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger

from advent_of_corona.util import corona_util


### CONSTANTS ###

TEST_INPUT = [
    """

    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    0,
    0,
    0,
]

TEST_OUTPUT_2 = [
    0,
    0,
    0,
]










class DayManager(object):

    def __init__(self):
        self.puzzle_input = 'no input for day 2'

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))
        start_time = time.time()

        self.run_tests()

        self.run_real()

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        # aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

        for n in range(1, 4):
            assert Solver.find_num_paths_slow(n) == Solver.find_num_paths_fast(n)

    def run_real(self):
        AocLogger.verbose = False

        aoc_util.assert_equal(
            5550996791340,
            self.solve_part_1(self.puzzle_input)
        )

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_2(self.puzzle_input)
        # )

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

    def p1(self):
        """
        Ok, ok… We get it. It’s Sunday and all you want to do is chill and be lazy. Don’t worry, we won’t bother you
        much (today).

        Imagine that you are placed in a giant cube of size 10m x 10m x 10m, concretely in any corner of it. You are
        told to move to the opposite corner of that cube.

        How many paths you can take?
        """
        num_paths = self.find_num_paths_fast(10)
        return num_paths

    @classmethod
    def find_num_paths_slow(cls, x, y=None, z=None):
        if y is None and z is None:
            y = x
            z = x

        steps = []
        for i in range(x):
            steps.append('X')
        for i in range(y):
            steps.append('Y')
        for i in range(z):
            steps.append('Z')

        num_paths = len(set(permutations(steps)))
        print('{} x {} x {} -> {}'.format(x, y, z, num_paths))
        return num_paths

    @classmethod
    def find_num_paths_fast(cls, n):
        tri = cls.gen_tri(3 * n + 1)
        if AocLogger.verbose:
            cls.print_tri(tri)

        ans_2d = tri[n][n]
        mult_3d = tri[n][2 * n]
        ans_3d = ans_2d * mult_3d
        print('{} * {} = {}\n'.format(ans_2d, mult_3d, ans_3d))

        return ans_3d

    @classmethod
    def gen_tri(cls, n):
        tri = []
        for _ in range(n):
            # print('add a new diag')
            for y, row in enumerate(tri):
                # print('add to row {}'.format(y))
                x = len(row)
                if x < 1 or y < 1:
                    value = 1
                else:
                    value = tri[y - 1][x] + tri[y][x - 1]
                row.append(value)
            tri.append([1])
            z=0
        return tri

    @classmethod
    def print_tri(cls, tri):
        max_value_row = len(tri)//2
        max_value = tri[max_value_row][-1]
        width = len(str(max_value)) + 1
        print('tri: (max_value={})'.format(max_value))
        for row in tri:
            builder = []
            for x in row:
                builder.append('{:{}d}'.format(x, width))
            print(''.join(builder))

    def p2(self):
        """

        """
        z=0
        return 2










if __name__ == '__main__':
    instance = DayManager()
    instance.run()




