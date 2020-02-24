#!/usr/bin/env python3



### IMPORTS ###

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.grid_2d import Grid2D
from aoc_util.recursive_pathfinder_droid import RecursivePathfinderDroid

import sys
sys.setrecursionlimit(2000)


### CONSTANTS ###

TEST_INPUT = [
    """      
#########
#b.A.@.a#
#########
    """, """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
    """, """

    """
]





class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        try:
            puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            puzzle_input = 'unable to get input'
        aoc_util.write_input(puzzle_input, __file__)

        self.run_tests()

        AocLogger.verbose = False

        # self.solve_part_1(puzzle_input)

        # self.solve_part_2(puzzle_input)

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_1(puzzle_input)
        # )

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_2(puzzle_input)
        # )

    def run_tests(self):
        AocLogger.verbose = True

        aoc_util.assert_equal(
            self.solve_part_1(TEST_INPUT[0]),
            0
        )

        aoc_util.assert_equal(
            self.solve_part_1(TEST_INPUT[1]),
            0
        )

    def solve_part_1(self, puzzle_input: str):
        puzzle_input = puzzle_input.strip()
        AocLogger.log('puzzle_input:\n{}\n'.format(puzzle_input))

        solver = MazeSolver(puzzle_input)
        part_1_result = solver.find_shortest_path()

        print('part 1 result: {}'.format(part_1_result))
        return part_1_result

    def solve_test_case_2(self, test_input):
        AocLogger.log('test input: {}'.format(test_input))
        return 0

    def solve_part_2(self, puzzle_input: str):
        puzzle_input = puzzle_input.strip()

        result = 0

        print('part 2 result: {}'.format(result))
        return result
















class MazeSolver(object):

    def __init__(self, text):
        self.text = text
        self.maze = Grid2D(text)
        self.finder_droid = KeyFinderDroid(self.maze)

        self.reachable_by_start_dict = {}
        # self.keys_by_point = {}

    def __str__(self):
        return '{}: {}'.format(
            type(self).__name__, [self.text])

    def __repr__(self):
        return str(self)

    def find_shortest_path(self):
        """
        algo:
            search map for all POIs {start, a, b}

            reachable from point:
                start: a=2{}, b=4{a}
                a: b=6{a}
                b: a=6{A}

            dijkstra's:
                start (): 0
                a (a): 2
                b (a,b): 8


        Args:
            test_input:

        Returns:

        """
        if AocLogger.verbose:
            self.maze.show()


        self.find_reachable()

        AocLogger.log_dict(self.reachable_by_start_dict, 'reachable_by_start_dict', force_verbose=True)

        z=0

        # todo: now do dijkstra's here

        return 0

    def find_reachable(self):
        """
        get points of interest
            (@, a, b)
        then get reachable for each
        """
        self.finder_droid.find_all_doors()

        start_coords = self.maze.find('@')[0]

        self.reachable_by_start_dict = {
            '@': self.finder_droid.find_reachable_from_start(start_coords)
        }

        key_coords = self.find_all_key_coords()

        for point in key_coords:
            letter = self.maze.get(*point)
            print('doing letter: {}'.format(letter))
            reachable = self.finder_droid.find_reachable_from_start(point)
            self.reachable_by_start_dict[letter] = reachable


    def find_all_key_coords(self):
        def is_maze_key(char: str):
            return char.islower()

        coords_list = self.maze.find_by_function(is_maze_key)
        return coords_list





class KeyFinderDroid(RecursivePathfinderDroid):

    def __init__(self, maze: Grid2D):
        super().__init__()

        self.maze = maze

        self.shortest_paths = {}

        self.doors_by_point = {}


    def find_all_doors(self):
        def is_maze_door(char: str):
            return char.isupper()

        coords_list = self.maze.find_by_function(is_maze_door)
        for point in coords_list:
            self.doors_by_point[point] = self.maze.get(*point)



    def find_reachable_from_start(self, start_point):
        """
        given a start point

        find num steps to each key, and keys needed
        """
        # reset
        self.shortest_paths = {}
        self.x, self.y = start_point

        path_so_far = [start_point]
        self._try_all_directions(path_so_far)

        result_dict = {}
        for key, path in self.shortest_paths.items():
            # path = self.shortest_paths[key]

            needed_keys = set()
            for point in path:
                if point in self.doors_by_point:
                    # door found in path

                    needed_keys.add(self.doors_by_point[point].lower())

            result_dict[key] = ReachableKey(key, len(path) - 1, needed_keys)

        z=0

        return result_dict

    def move(self, direction):
        desired_coords = self.desired_x, self.desired_y
        if self.maze.is_value(desired_coords, '#'):
            return self.STATUS_HIT_WALL

        # do the move
        self.x, self.y = desired_coords
        self.maze.overlay = {
            desired_coords: '$'
        }

        return self.STATUS_MOVED

    def process_new_path(self, new_path):
        if AocLogger.verbose:
            self.maze.show()

        value = self.maze.get(self.x, self.y)
        if value.islower():
            AocLogger.log('path to {}: {}'.format(value, new_path))

            if (value not in self.shortest_paths
                    or len(new_path) < len(self.shortest_paths[value])):
                # set shortest path
                self.shortest_paths[value] = new_path

        z=0


class ReachableKey(object):

    def __init__(self, letter, dist, needed):
        self.letter = letter
        self.dist = dist
        self.needed = needed

    def __str__(self):
        return '{}: {}'.format(
            type(self).__name__, [self.dist, self.needed])

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




