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

import aocd
from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.intcode_computer import IntcodeComputer
from aoc_util.grid_2d import Grid2D
from aoc_util.recursive_pathfinder_droid import RecursivePathfinderDroid

import numpy as np

import sys
sys.setrecursionlimit(1500)



### CONSTANTS ###

TEST_INPUT = [
    """      
#######
#G...S#
#######
    """, """
#####
##S.#
#G.##
#####
    """, """

    """
]

TEST_OUTPUT = [
    0,
    0,
    0,
]



























class TestDroid(RecursivePathfinderDroid):

    def __init__(self, test_input):
        super().__init__()

        lines = test_input.split('\n')
        self.grid = Grid2D()

        # find offset such that: S + offset = origin (offset = (0,0) - S)
        offset = np.zeros(2)
        for r, row in enumerate(lines):
            if 'S' in row:
                offset_y = -r
                offset_x = -row.find('S')
                offset = np.array([offset_x, offset_y])
                break

        # populate grid
        for r, row in enumerate(lines):
            for c, col in enumerate(row):
                coord = np.array([c, r])
                coord += offset
                self.grid.set_tuple(coord, col)

        print('test grid:')
        self.grid.show()

    def move(self, direction):
        if self.grid.get(self.desired_x, self.desired_y) == '#':
            return self.STATUS_HIT_WALL

        # do the move
        self.x = self.desired_x
        self.y = self.desired_y
        self.grid.overlay = {
            (self.x, self.y): 'D'
        }
        self.grid.show()

        if self.grid.get(self.x, self.y) == 'G':
            return self.STATUS_HIT_GOAL
        else:
            return self.STATUS_MOVED












class IntcodeDroid(RecursivePathfinderDroid):

    DIRECTION_CODES = {
        'n': 1,
        's': 2,
        'w': 3,
        'e': 4,
    }

    def __init__(self, puzzle_input):
        super().__init__()

        self.codes = aoc_util.ints(puzzle_input)
        self.ic = IntcodeComputer(self.codes)
        self.ic.verbose = False

        self.explored = Grid2D()
        self.explored.set(0, 0, 'S')

    def move(self, direction):
        dir_code = self.DIRECTION_CODES[direction]

        self.ic.queue_input(dir_code)
        self.ic.run()
        assert self.ic.state == IntcodeComputer.STATE_OUTPUT

        status = self.ic.get_latest_output()
        if status == self.STATUS_HIT_WALL:
            # pos does not change, just add to explored
            self.explored.set(self.desired_x, self.desired_y, '#')
            return status

        # otherwise, the move was successful
        self.x = self.desired_x
        self.y = self.desired_y

        if status == self.STATUS_MOVED:
            # moved
            self.explored.set(self.x, self.y, '.')
        else:
            print('found: {}'.format(self.get_current()))
            self.explored.set(self.x, self.y, 'G')

        self.explored.overlay = {
            (self.x, self.y): 'D'
        }
        self.explored.show()
        return status













def main():
    print('starting {}'.format(__file__.split('/')[-1]))

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    AocLogger.verbose = True
    run_tests()

    AocLogger.verbose = False

    p1, p2 = solve_full_input(puzzle_input)
    print('part 1: {}'.format(p1))
    print('part 2: {}'.format(p2))
    aoc_util.assert_equal(238, p1)
    aoc_util.assert_equal(392, p2)


def run_tests():
    aoc_util.assert_equal(
        4,
        solve_test_case(TEST_INPUT[0])
    )

    aoc_util.assert_equal(
        2,
        solve_test_case(TEST_INPUT[1])
    )


def solve_test_case(test_input):
    test_input = test_input.strip()
    AocLogger.log('test input:\n{}'.format(test_input))

    td = TestDroid(test_input)
    result = td.find_min_num_moves()
    return result


def are_adjacent(ox_coord, empty_spaces):
    return aoc_util.manhatten_dist(ox_coord, empty_spaces) == 1


def solve_full_input(puzzle_input):
    ### part 1 ###
    puzzle_input = puzzle_input.strip()
    droid = IntcodeDroid(puzzle_input)

    min_moves = droid.find_min_num_moves()
    print('min_moves: {}'.format(min_moves))

    ### part 2 ###
    explored = droid.explored

    # setup initial state (one filled, all others empty)
    EMPTY_SPACE_VALUES = {'.', 'S'}
    spaces_filled_this_loop = set()
    empty_spaces = set()
    for coord, char in explored.grid.items():
        if char == 'G':
            explored.set_tuple(coord, 'O')
            spaces_filled_this_loop.add(coord)
        if char in EMPTY_SPACE_VALUES:
            empty_spaces.add(coord)
    print('num empty_spaces: {}'.format(len(empty_spaces)))

    # loop til all spaces filled
    num_min = 0
    while empty_spaces:
        # swap spaces
        spaces_filled_prev_loop = spaces_filled_this_loop
        spaces_filled_this_loop = set()

        # get spaces that will be filled this loop
        for ox_coord in spaces_filled_prev_loop:
            for em_coord in empty_spaces:
                if are_adjacent(ox_coord, em_coord):
                    spaces_filled_this_loop.add(em_coord)

        # fill the spaces
        for coord in spaces_filled_this_loop:
            empty_spaces.remove(coord)
            explored.set_tuple(coord, 'O')

        # finish up
        num_min += 1
        # explored.show()

    print('num_min: {}\n'.format(num_min))

    ### return answers ###
    return min_moves, num_min





if __name__ == '__main__':
    main()




