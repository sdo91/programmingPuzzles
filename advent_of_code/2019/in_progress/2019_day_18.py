#!/usr/bin/env python3



### IMPORTS ###

import typing

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.grid_2d import Grid2D
from aoc_util.recursive_pathfinder_droid import RecursivePathfinderDroid

import sys
sys.setrecursionlimit(2000)


### CONSTANTS ###

INF = 9e9

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

        self.solve_part_1(puzzle_input)

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
            8
        )

        aoc_util.assert_equal(
            self.solve_part_1(TEST_INPUT[1]),
            86
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
        self.num_keys = 0

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

        start_node = Node('@', set())
        start_node.dist = 0
        all_nodes_dict = {start_node.uid: start_node}
        unvisited_nodes_set = {start_node}

        while unvisited_nodes_set:
            # select node at shortest distance
            min_dist = INF
            selected_node = None  # type: Node
            for node in unvisited_nodes_set:
                if node.dist < min_dist:
                    min_dist = node.dist
                    selected_node = node

            # mark as visited
            unvisited_nodes_set.remove(selected_node)
            selected_node.visited = True
            print('\nselected_node: {}'.format(selected_node))

            # check if done
            if len(selected_node.keys_set) == self.num_keys:
                return selected_node.dist

            # update dist to all nodes reachable
            for key in self.reachable_by_start_dict[selected_node.char].values():
                if selected_node.does_not_have(key) and selected_node.can_reach(key):
                    AocLogger.log('checking: {}'.format(key))

                    # add node if DNE
                    new_node = Node.create(selected_node, key)
                    if new_node.uid in all_nodes_dict:
                        AocLogger.log('already exists: {}'.format(new_node))
                    else:
                        all_nodes_dict[new_node.uid] = new_node
                        unvisited_nodes_set.add(new_node)
                    reachable_node = all_nodes_dict[new_node.uid]

                    # calc dist via selected
                    dist_between = self.get_dist_between(selected_node, key)
                    dist_via_selected = selected_node.dist + dist_between

                    if dist_via_selected < reachable_node.dist:
                        # update shortest path to node
                        reachable_node.dist = dist_via_selected
                        reachable_node.path = selected_node.path.copy()
                        reachable_node.path.append(reachable_node.char)
                        AocLogger.log('updated path: {}'.format(reachable_node))

                    # add node if not already there (letter, keys)


                    z=0
                else:
                    AocLogger.log('skipping: {}'.format(key))

                # z=0
                # if can reach
                # and dont already have




            z=0

            # select smallest, mark as visited

            # check if done
            # add/update all reachable



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
        self.num_keys = len(key_coords)

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


    def get_dist_between(self, selected_node, key):
        reachable = self.reachable_by_start_dict[selected_node.char][key.letter]  # type: ReachableKey
        return reachable.dist





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
            type(self).__name__, [self.letter, self.dist, self.needed])

    def __repr__(self):
        return str(self)





class Node(object):

    def __init__(self, char: str, keys_set: typing.Set[str]):
        self.char = char
        self.keys_set = keys_set
        self.uid = '{}({})'.format(char, ','.join(sorted(keys_set)))
        self.dist = INF
        self.path = []
        self.visited = False

    @staticmethod
    def create(selected, key):
        """
        Args:
            selected (Node):
            key (ReachableKey):

        Returns:
            Node:
        """
        combined_keys = selected.keys_set.copy()
        combined_keys.add(key.letter)
        return Node(key.letter, combined_keys)

    def __repr__(self):
        return '{}: uid={}, dist={}, path={}'.format(
            type(self).__name__, self.uid, self.dist, self.path)

    def get_id(self):
        return

    def does_not_have(self, key: ReachableKey):
        return key.letter not in self.keys_set

    def can_reach(self, key: ReachableKey):
        return self.keys_set.issuperset(key.needed)



if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




