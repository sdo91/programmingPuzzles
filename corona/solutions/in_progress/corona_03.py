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

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger
from advent_of_code.util.grid_2d import Grid2D

from corona.util import corona_util


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
        try:
            self.puzzle_input = corona_util.read_input(__file__)
        except:
            self.puzzle_input = traceback.format_exc()
            print(self.puzzle_input)

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))
        start_time = time.time()

        self.run_tests()

        self.run_real()

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def run_real(self):
        AocLogger.verbose = False

        aoc_util.assert_equal(
            0,
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

        self.lines = aoc_util.lines(self.text)

        # self.current

        self.N = self.lines[0]
        x, y = reversed(aoc_util.ints(self.lines[-1]))
        map = '\n'.join(self.lines[1:-1])

        self.grid = Grid2D(map)

        self.grid.overlay = {
            (x, y): '@'
        }

        self.block_infected()

        self.grid.show()

        AocLogger.log(str(self))

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def block_infected(self):
        infected_list = self.grid.find('I')
        for infected in infected_list:
            for adj in self.grid.get_adjacent_coords(infected):
                if self.grid.is_value(adj, '.'):
                    self.grid.set_tuple(adj, 'x')

        z=0

    def p1(self):
        """
        It’s Monday, the very first day of the week and you’re all hesitating to go out for a walk, a beer,
        or something to do as you’re free. But you’re not, we’re all confined. Today’s problem is about that.

        Mike is a nurse with only one mission, find the lost COVID-19 vaccine. Mike does not know where to start the
        search, so he asked a hacker (you), a good friend of his, to help him out.

        The hacker was able to get the site map of Mike’s location and extracted the following information:

        You are in a N x N field formed of cells, with different obstacles and people in it:
            Open cells, which you can walk through them (.)
            Obstacles, which block your way (X).
            People infected by the COVID-19, which you have maintain a distance of 1 cell from them (I).
            The COVID-19’s cure (C), i.e. the vaccine you are looking for.
        There may be more than one COVID-19 vaccines in the map, you need to find the closest one.

        You can only move up, down, right and left. No diagonal moves are allowed.

        Input
        You will receive an integer N, a char matrix N x N and an initial position x y.

        Output
        The minimum distance between original position and the cure. If there is no path to the cure, the output is -1.

        algo:
            add start at dist 0
            add adjacent
            do dijkstras

        """
        z=0
        return 1

    def p2(self):
        """

        """
        z=0
        return 2










if __name__ == '__main__':
    instance = DayManager()
    instance.run()




