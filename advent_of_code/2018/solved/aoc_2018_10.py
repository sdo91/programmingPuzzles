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
import math

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger
from advent_of_code.util.grid_2d import Grid2D


### CONSTANTS ###

TEST_INPUT = [
    """
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
    """, """

    """, """

    """
]

TEST_OUTPUT_2 = [
    3,
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
            10345,
            self.solve_part_2(puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def solve_part_2(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_2_result = solver.p2()

        print('part_2_result: {}'.format(part_2_result))
        return part_2_result










class Point(object):

    def __init__(self, text):
        self.text = text
        numbers = aoc_util.ints(text)
        self.position = (numbers[0], numbers[1])
        self.velocity = (numbers[2], numbers[3])

    def __repr__(self):
        return 'p={}, v={}'.format(self.position, self.velocity)

    def update(self, num_secs=1):
        self.position = (
            self.position[0] + self.velocity[0] * num_secs,
            self.position[1] + self.velocity[1] * num_secs,
        )










class Solver(object):

    def __init__(self, text: str):
        self.text = text.strip()
        AocLogger.log(str(self))

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p2(self):

        all_points = []
        lines = aoc_util.lines(self.text)
        for line in lines:
            p = Point(line)
            all_points.append(p)

        prev_height = math.inf

        num_sec = 0
        while True:

            # dumb way to make it faster
            if prev_height != math.inf and prev_height > 10000:
                print('progress: num_sec={}, prev_height={}'.format(num_sec, prev_height))
                seconds_this_loop = 1000
            else:
                seconds_this_loop = 1

            # update
            grid = Grid2D(text='', default='.')
            for p in all_points:
                p.update(seconds_this_loop)
                grid.set_tuple(p.position, '#')
            height = grid.max_y - grid.min_y

            # check if done
            if height > prev_height:
                break
            num_sec += seconds_this_loop
            prev_height = height

            # show letters
            if height < 10:
                grid.show()
                print('after {} sec (height={})'.format(num_sec, height))

        return num_sec










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




