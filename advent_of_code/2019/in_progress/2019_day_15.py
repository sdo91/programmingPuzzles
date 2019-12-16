#!/usr/bin/env python3



### IMPORTS ###

import aocd
from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.intcode_computer import IntcodeComputer

from collections import defaultdict
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





class Grid2D(object):

    def __init__(self):
        """
        NOTE: uses an inverted y-axis by default (increasing downwards)
        """
        self.grid = defaultdict(lambda: ' ')

        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

        self.overlay = {}

    def setTuple(self, coord, value):
        self.set(coord[0], coord[1], value)

    def set(self, x, y, value):
        self.grid[(x, y)] = value

        self.min_x = min(self.min_x, x)
        self.max_x = max(self.max_x, x)
        self.min_y = min(self.min_y, y)
        self.max_y = max(self.max_y, y)

    def get(self, x, y):
        return self.grid[(x, y)]

    def show(self):
        print()
        # for y in range(self.max_y, self.min_y - 1, -1):
        for y in range(self.min_y, self.max_y + 1):
            line = ''
            for x in range(self.min_x, self.max_x + 1):
                coord = (x, y)
                if coord in self.overlay:
                    line += self.overlay[coord]
                else:
                    line += self.grid[coord]
            print(line)
        print()





class Droid(object):

    OPPOSITE_DIRECTIONS = {
        'n': 's',
        's': 'n',
        'w': 'e',
        'e': 'w',
    }

    DX = {
        'n': 0,
        's': 0,
        'w': -1,
        'e': 1,
    }

    DY = {
        'n': -1,
        's': 1,
        'w': 0,
        'e': 0,
    }

    STATUS_HIT_WALL = 0
    STATUS_MOVED = 1
    STATUS_HIT_GOAL = 2

    def __init__(self):
        self.x = 0
        self.y = 0
        self.desired_x = 0
        self.desired_y = 0

    def getCurrent(self):
        return self.x, self.y

    def getDesired(self, direction):
        return self.x + self.DX[direction], self.y + self.DY[direction]

    def updateDesired(self, direction):
        self.desired_x, self.desired_y = self.getDesired(direction)

    def find_min_num_moves(self):
        path_so_far = [self.getCurrent()]
        result_path = self.try_all_directions(path_so_far)
        print('path found: {}'.format(result_path))

        result = len(result_path) - 1
        print('fewest moves: {}'.format(result))
        return result

    def try_all_directions(self, path_so_far):
        candidate_paths = []
        candidate_paths.append(self.recursive_find_path('n', path_so_far))
        candidate_paths.append(self.recursive_find_path('s', path_so_far))
        candidate_paths.append(self.recursive_find_path('w', path_so_far))
        candidate_paths.append(self.recursive_find_path('e', path_so_far))

        # choose best path
        min_len = 9e9
        best_path = None  # default if no path can get to goal
        for cand in candidate_paths:
            if cand is None:
                continue
            if len(cand) < min_len:
                min_len = len(cand)
                best_path = cand

        return best_path

    def recursive_find_path(self, direction, path_so_far):
        """
        base case:
            current + direction = goal
        """
        # assert last in path so far is current pos
        assert path_so_far[-1] == self.getCurrent()

        if self.getDesired(direction) in path_so_far:
            return None

        # first try to move from current
        self.updateDesired(direction)
        status_code = self.move(direction)

        if status_code == self.STATUS_HIT_WALL:
            # this is not a valid path
            return None

        # add the point to the path
        new_path = path_so_far.copy()
        new_path.append(self.getCurrent())

        if status_code == self.STATUS_HIT_GOAL:
            result = new_path
        else:
            result = self.try_all_directions(new_path)

        # move back to prev point
        opposite_direction = self.OPPOSITE_DIRECTIONS[direction]
        self.updateDesired(opposite_direction)
        self.move(opposite_direction)

        return result

    def move(self, direction):
        raise NotImplementedError


class TestDroid(Droid):

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
                self.grid.setTuple(coord, col)

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


class IntcodeDroid(Droid):

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
            print('found: {}'.format(self.getCurrent()))
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

    solve_full_input(puzzle_input)


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
    puzzle_input = puzzle_input.strip()
    droid = IntcodeDroid(puzzle_input)

    min_moves = droid.find_min_num_moves()
    print('min_moves: {}'.format(min_moves))

    explored = droid.explored

    empty_space_values = {'.', 'S'}
    oxygen_spaces = set()
    empty_spaces = set()
    for coord, char in explored.grid.items():
        if char == 'G':
            explored.setTuple(coord, 'O')
            oxygen_spaces.add(coord)
        if char in empty_space_values:
            empty_spaces.add(coord)

    num_min = 0
    while True:
        spaces_this_loop = set()
        for ox_coord in oxygen_spaces:
            for em_coord in empty_spaces:
                if are_adjacent(ox_coord, em_coord):
                    spaces_this_loop.add(em_coord)

        for coord in spaces_this_loop:
            oxygen_spaces.add(coord)
            empty_spaces.remove(coord)
            explored.setTuple(coord, 'O')

        num_min += 1
        explored.show()

        if len(empty_spaces) == 0:
            break

    print('num_min: {}'.format(num_min))





if __name__ == '__main__':
    main()




