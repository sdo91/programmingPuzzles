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
#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######
    """
]





class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        puzzle_input = aocd.data
        aoc_util.write_input(puzzle_input, __file__)

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            6098,
            self.solve_part_1(puzzle_input)
        )

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_2(puzzle_input)
        # )

    def run_tests(self):
        AocLogger.verbose = True

        # aoc_util.assert_equal(
        #     8,
        #     self.solve_part_1(TEST_INPUT[0])
        # )
        #
        # aoc_util.assert_equal(
        #     86,
        #     self.solve_part_1(TEST_INPUT[1])
        # )

        aoc_util.assert_equal(
            8,
            self.solve_part_2(TEST_INPUT[2])
        )

    def solve_part_1(self, puzzle_input: str):
        puzzle_input = puzzle_input.strip()
        AocLogger.log('puzzle_input:\n{}\n'.format(puzzle_input))

        solver = MazeSolver(puzzle_input)
        part_1_result = solver.find_shortest_path()

        print('part 1 result: {}'.format(part_1_result))
        return part_1_result

    def solve_part_2(self, puzzle_input: str):
        puzzle_input = puzzle_input.strip()
        AocLogger.log('puzzle_input:\n{}\n'.format(puzzle_input))

        solver = MazeSolver(puzzle_input, is_part_2=True)
        part_2_result = solver.find_shortest_path()

        z=0

        print('part 2 result: {}'.format(part_2_result))
        return part_2_result





class MazeSolver(object):

    def __init__(self, text, is_part_2=False):
        self.is_part_2 = is_part_2
        self.text = text

        self.maze = Grid2D(text)
        if is_part_2:
            self.replace_maze_center()
        self.maze.show()

        self.droids = []
        # self.reachable_by_start_dict = {}
        self.num_keys_in_maze = 0

    def __repr__(self):
        return '{}: {}'.format(type(self).__name__, self.text)

    def find_shortest_path(self):
        """
        p2 algo:
            create 4 droids
            each droid makes its own reachable_by_start_dict

        search map for all POIs {start, a, b}

        reachable from point:
            start: a=2{}, b=4{a}
            a: b=6{a}
            b: a=6{A}

        dijkstra's:
            start (): 0
            a (a): 2
            b (a,b): 8
        """
        # do setup
        self.init_all_droids()
        # self.find_reachable()
        # AocLogger.log_dict(self.reachable_by_start_dict, 'reachable_by_start_dict', force_verbose=True)

        start_node = Node('@', set())
        start_node.dist = 0
        all_nodes_dict = {start_node.uid: start_node}
        unvisited_nodes_set = {start_node}

        # do dijkstra's algo
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
            print('\nselected_node: {}'.format(selected_node))

            # check if done
            if len(selected_node.keys_set) == self.num_keys_in_maze:
                return selected_node.dist

            # update dist to all reachable nodes
            for key in self.reachable_by_start_dict[selected_node.char].values():
                if selected_node.does_not_have(key) and selected_node.can_reach(key):
                    AocLogger.log('checking: {}'.format(key))

                    # add node if not already there
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
                else:
                    AocLogger.log('skipping: {}'.format(key))

        raise RuntimeError('should never get here')

    def init_all_droids(self):
        for x in range(1, 5):
            droid = self.find_reachable(start_char=str(x))
            AocLogger.log_dict(droid.reachable_by_start_dict, 'reachable_by_start_dict', force_verbose=True)
            self.droids.append(droid)
        z=0

    def find_reachable(self, start_char='@'):
        """
        get points of interest
            (@, a, b)
        then get reachable for each
        """
        finder_droid = KeyFinderDroid(self.maze)

        # todo: just do once
        finder_droid.find_all_doors()

        start_coords = self.maze.find(start_char)[0]

        reachable_by_start_dict = {
            start_char: finder_droid.find_reachable_from_start(start_coords)
        }

        keys_in_quad = reachable_by_start_dict[start_char].keys()

        # todo: just do once
        all_key_coords = self.find_all_key_coords()
        if not self.num_keys_in_maze:
            self.num_keys_in_maze = len(all_key_coords)

        for point in all_key_coords:
            letter = self.maze.get(*point)
            if letter in keys_in_quad:
                # print('doing letter: {}'.format(letter))
                reachable = finder_droid.find_reachable_from_start(point)
                reachable_by_start_dict[letter] = reachable

        finder_droid.reachable_by_start_dict = reachable_by_start_dict
        return finder_droid

    def find_all_key_coords(self):
        def is_maze_key(char: str):
            return char.islower()

        coords_list = self.maze.find_by_function(is_maze_key)
        return coords_list

    def get_dist_between(self, selected_node, key):
        reachable = self.reachable_by_start_dict[selected_node.char][key.letter]  # type: ReachableKey
        return reachable.dist

    def replace_maze_center(self):
        center_point = self.maze.find('@')[0]

        self.maze.set_tuple(center_point, '#')

        for point in self.maze.get_adjacent_coords(center_point):
            self.maze.set_tuple(point, '#')

        quadrant = 1
        for point in self.maze.get_diagonal_coords(center_point):
            self.maze.set_tuple(point, str(quadrant))
            quadrant += 1





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
        # if AocLogger.verbose:
        #     self.maze.show()

        value = self.maze.get(self.x, self.y)
        if value.islower():
            # AocLogger.log('path to {}: {}'.format(value, new_path))

            if (value not in self.shortest_paths
                    or len(new_path) < len(self.shortest_paths[value])):
                # set shortest path
                self.shortest_paths[value] = new_path





class ReachableKey(object):

    def __init__(self, letter, dist, needed):
        self.letter = letter
        self.dist = dist
        self.needed = needed

    def __repr__(self):
        return '{}: {}'.format(
            type(self).__name__, [self.letter, self.dist, self.needed])





class Node(object):

    def __init__(self, char: str, keys_set: typing.Set[str]):
        self.char = char
        self.keys_set = keys_set
        self.uid = '{}({})'.format(char, ','.join(sorted(keys_set)))
        self.dist = INF
        self.path = []

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

    def does_not_have(self, key: ReachableKey):
        return key.letter not in self.keys_set

    def can_reach(self, key: ReachableKey):
        return self.keys_set.issuperset(key.needed)





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




