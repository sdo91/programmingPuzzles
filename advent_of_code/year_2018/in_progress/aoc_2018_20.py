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
from advent_of_code.util.grid_2d import Grid2D


### CONSTANTS ###
TEST_INPUT = [
    """
^WNE$
    """, """
^ENWWW(NEEE|SSE(EE|N))$
    """, """
^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$
    """, """
^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$
    """, """
^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$
    """
]

TEST_OUTPUT_1 = [
    3,
    10,
    18,
    23,
    31,
]

TEST_OUTPUT_2 = [
    0,
    0,
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

        # aoc_util.assert_equal(
        #     4050,
        #     self.solve_part_1(self.puzzle_input)
        # )

        aoc_util.assert_equal(
            0,
            self.solve_part_2(self.puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2, cases={1})
        aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)
        # aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)

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

        # p2
        self.grid = Grid2D('X')
        self.surround((0, 0))
        self.grid.show()
        self.stamp = time.time()

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def process_p1(self, text):
        """
        algo:
            recursively process parens

            eg:
                while there are parens:
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
            text = text[:open_idx] + self.process_p1(inside) + text[close_idx + 1:]
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
        route = self.process_p1(self.text[1:-1])
        return len(route)

    def p2(self):
        """

        """
        text = self.text[1:-1]
        start_coord = (0, 0)
        self.draw_map(text, start_coord)
        self.grid.replace('?', '#')
        self.grid.show()
        z=0
        return 0

    def draw_map(self, text, start_coord):
        """
        algo:

            given a starting point

            if we hit a paren:
                find start/end
                call recursive (return coord)
                if there are more chars,
                    make sure coord is the same...
                    resume after end

            if we hit a pipe:
                reset back to start coord



        """
        i = 0
        current_coord = start_coord
        text_len = len(text)
        while i < text_len:

            char = text[i]

            if char in Grid2D.DIRECTIONS:
                current_coord = Grid2D.get_coord_direction(current_coord, char)
                door = '|' if char in Grid2D.EAST_WEST else '-'
                self.grid.set_tuple(current_coord, door)
                current_coord = Grid2D.get_coord_direction(current_coord, char)
                self.grid.set_tuple(current_coord, '.')
                self.surround(current_coord)

            elif char == '(':
                open_idx = i
                close_idx = self.find_close_paren(text, open_idx)
                inside = text[open_idx+1:close_idx]
                self.draw_map(inside, current_coord)
                i = close_idx

            elif char == '|':
                # reset current coord
                current_coord = start_coord

            else:
                assert False

            now = time.time()
            if now - self.stamp > 5:
                self.stamp = now
                self.grid.show(current_coord)
            i += 1

        return current_coord



    def surround(self, coord):
        self.grid.set_coords_default(Grid2D.get_adjacent_coords(coord), '?')
        self.grid.set_coords_default(Grid2D.get_diagonal_coords(coord), '#')
















if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




