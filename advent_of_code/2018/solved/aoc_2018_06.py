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

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.grid_2d import Grid2D


### CONSTANTS ###
TEST_INPUT = [
    """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    17,
    0,
    0,
]

TEST_OUTPUT_2 = [
    16,
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
            3010,
            self.solve_part_1(puzzle_input)
        )

        aoc_util.assert_equal(
            48034,
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

        # populate grid, targets
        self.grid = Grid2D('', '.')
        self.targets = {}

        x = 0
        for line in aoc_util.lines(self.text):
            coords = tuple(aoc_util.ints(line))
            self.assign_char(coords, x)
            self.targets[coords] = 0
            x += 1
        # self.grid.show()

        # p1
        self.inf_targets = set()

        # p2
        self.p2_total = 0

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def assign_char(self, coords, x):
        if x < 26:
            i = ord('A') + x
        else:
            i = ord('a') + (x - 26)
        char = chr(i)
        print('assigning {} to target {}'.format(char, coords))
        self.grid.set_tuple(coords, char)

    def p1(self):
        """
        Using only the Manhattan distance, determine the area around each coordinate by counting the number of
        integer X,Y locations that are closest to that coordinate
        (and aren't tied in distance to any other coordinate).

        algo:
            for each coord in range
            assign to target

        3920 too high
        """
        for y in self.grid.rows():
            for x in self.grid.cols():
                coords = (x, y)
                self.find_closest_target(coords)

        # find biggest group
        max_area = 0
        max_char = ''
        for target, count in self.targets.items():
            char = self.grid.get(*target)
            self.grid.set_tuple(target, ' ')

            if target in self.inf_targets:
                continue

            if count > max_area:
                max_area = count
                max_char = char

        self.grid.show()
        print('max_char: {}'.format(max_char))
        return max_area

    def find_closest_target(self, coords):
        min_dist = 9e9
        min_targets = []
        for target in self.targets:
            d = aoc_util.manhatten_dist(target, coords)

            if d <= min_dist:
                if d < min_dist:
                    # reset
                    min_targets = []
                min_dist = d
                min_targets.append(target)

        if len(min_targets) == 1:
            selected = min_targets[0]
            char = self.grid.get(*selected)

            self.grid.set_tuple(coords, char)

            self.targets[selected] += 1

            if self.grid.is_on_edge(*coords):
                self.inf_targets.add(selected)

    def p2(self):
        for y in self.grid.rows():
            for x in self.grid.cols():
                coords = (x, y)
                self.check_dist(coords)

        self.grid.show()
        return self.p2_total

    def check_dist(self, coords):
        threshold = 32
        if len(self.targets) > 10:
            threshold = 10000

        total = sum([aoc_util.manhatten_dist(x, coords) for x in self.targets])

        if total < threshold:
            self.p2_total += 1
            if coords not in self.targets:
                self.grid.set_tuple(coords, '#')










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




