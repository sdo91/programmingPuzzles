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

import typing

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.grid_2d import Grid2D
from aoc_util.recursive_pathfinder_droid import RecursivePathfinderDroid
from aoc_util.min_heap import MinHeap

import sys
sys.setrecursionlimit(2000)


### CONSTANTS ###

INF = 9e9

TEST_INPUTS_P1 = [
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
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
    """, """
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
    """, """
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
    """
]

TEST_OUTPUTS_P1 = [
    8,
    86,
    132,
    136,
    81,
]

TEST_INPUTS_P2 = [
    """
#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######
    """, """
###############
#d.ABC.#.....a#
######@#@######
###############
######@#@######
#b.....#.....c#
###############
    """, """
#############
#DcBa.#.GhKl#
#.###@#@#I###
#e#d#####j#k#
###C#@#@###J#
#fEbA.#.FgHi#
#############
    """, """
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############
    """
]

TEST_OUTPUTS_P2 = [
    8,
    24,
    32,
    72,
]





class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        puzzle_input = aocd.data
        aoc_util.write_input(puzzle_input, __file__)

        # AocLogger.verbose = True
        AocLogger.verbose = False

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            6098,
            self.solve_part_1(puzzle_input)
        )

        aoc_util.assert_equal(
            1698,
            self.solve_part_2(puzzle_input)
        )

    def run_tests(self):
        aoc_util.run_tests(self.solve_part_1, TEST_INPUTS_P1, TEST_OUTPUTS_P1)
        aoc_util.run_tests(self.solve_part_2, TEST_INPUTS_P2, TEST_OUTPUTS_P2)

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

        print('part 2 result: {}'.format(part_2_result))
        return part_2_result





class MazeSolver(object):

    def __init__(self, text, is_part_2=False):
        self.is_part_2 = is_part_2
        self.text = text

        self.maze = Grid2D(text)
        self.replace_maze_center()
        self.maze.show()

        self.droids = []
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

        priority_queue = MinHeap()

        start_node = Node([x.start_char for x in self.droids], set())
        start_node.dist = 0
        priority_queue.insert(start_node, start_node.dist)

        # do dijkstra's algo
        while not priority_queue.is_empty():

            # select node at shortest distance
            selected_node = priority_queue.pop()  # type: Node

            print('\nselected_node: {}'.format(selected_node))
            print('num unvisited: {}'.format(priority_queue.get_num_active()))
            print('num keys: {}'.format(len(selected_node.keys_set)))

            # check if done
            if len(selected_node.keys_set) == self.num_keys_in_maze:
                return selected_node.dist

            # update dist to all reachable nodes
            for potential_node in self.get_nodes_reachable_from(selected_node):
                # 3 cases:
                #   DNE (use)
                #   better (use)
                #   worse (don't use)
                priority_queue.insert_if_better(potential_node, potential_node.dist)

        raise RuntimeError('should never get here')

    def get_nodes_reachable_from(self, selected_node):
        """
        for each droid:
            look thru reachable keys:
                keep:
                    dont have the key
                    path is unlocked

        Args:
            selected_node (Node):

        Returns:
            list[Node]:
        """
        results_list = []

        for i, droid in enumerate(self.droids):
            current_char = selected_node.locations[i]
            AocLogger.log('checking droid {} @ {}'.format(i, current_char))

            for key in droid.reachable_by_start_dict[current_char].values():
                if selected_node.does_not_have(key) and selected_node.is_path_unlocked(key):
                    AocLogger.log('path unlocked: {}'.format(key))

                    # calc dist via selected
                    dist_between = droid.get_dist_between(selected_node.locations[i], key)
                    dist_via_selected = selected_node.dist + dist_between

                    # add node to results_list
                    reachable_node = Node.create(selected_node, key, i)
                    reachable_node.dist = dist_via_selected
                    if AocLogger.verbose:
                        reachable_node.path = selected_node.path.copy()
                        reachable_node.path.append(key.letter)

                    results_list.append(reachable_node)
                else:
                    AocLogger.log('path locked: {}'.format(key))

        return results_list

    def init_all_droids(self):
        num_droids = 1
        if self.is_part_2:
            num_droids = 4
        for x in range(1, num_droids + 1):
            droid = self.find_reachable(start_char=str(x))
            AocLogger.log_dict(droid.reachable_by_start_dict, 'reachable_by_start_dict', force_verbose=True)
            self.droids.append(droid)

    def find_reachable(self, start_char: str):
        """
        get points of interest
            (@, a, b)
        then get reachable for each
        """
        finder_droid = KeyFinderDroid(self.maze, start_char)

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
                print('doing letter: {}'.format(letter))
                reachable = finder_droid.find_reachable_from_start(point)
                reachable_by_start_dict[letter] = reachable

        finder_droid.reachable_by_start_dict = reachable_by_start_dict
        return finder_droid

    def find_all_key_coords(self):
        def is_maze_key(char: str):
            return char.islower()

        coords_list = self.maze.find_by_function(is_maze_key)
        return coords_list

    def replace_maze_center(self):
        starting_points = self.maze.find('@')
        center_point = starting_points[0]

        if self.is_part_2:
            if len(starting_points) == 1:
                self.maze.set_tuple(center_point, '#')

                for point in self.maze.get_adjacent_coords(center_point):
                    self.maze.set_tuple(point, '#')

                starting_points = self.maze.get_diagonal_coords(center_point)

            quadrant = 1
            for point in starting_points:
                self.maze.set_tuple(point, str(quadrant))
                quadrant += 1
        else:
            self.maze.set_tuple(center_point, '1')





class KeyFinderDroid(RecursivePathfinderDroid):

    def __init__(self, maze: Grid2D, start_char: str):
        super().__init__()
        self.maze = maze
        self.shortest_paths = {}
        self.doors_by_point = {}

        self.start_char = start_char
        self.reachable_by_start_dict = {}

    def get_dist_between(self, start_char, key):
        """
        Args:
            start_char (str):
            key (ReachableKey):
        Returns:
            int:
        """
        reachable = self.reachable_by_start_dict[start_char][key.letter]  # type: ReachableKey
        return reachable.dist

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

    def __init__(self, locations: typing.List[str], keys_set: typing.Set[str]):
        self.locations = locations
        self.keys_set = keys_set
        self.uid = '[{}]({})'.format(
            ','.join(locations),
            ','.join(sorted(keys_set))
        )
        self.dist = INF
        self.path = []

    @staticmethod
    def create(selected, key, droid_index):
        """
        Args:
            selected (Node):
            key (ReachableKey):
            droid_index (int):

        Returns:
            Node:
        """
        combined_keys = selected.keys_set.copy()
        combined_keys.add(key.letter)
        locations = selected.locations.copy()
        locations[droid_index] = key.letter
        return Node(locations, combined_keys)

    def __repr__(self):
        return '{}: dist={}, uid={}, path={}'.format(
            type(self).__name__, self.dist, self.uid, self.path)

    def __eq__(self, other):
        return self.uid == other.uid

    def __hash__(self):
        return hash(self.uid)

    def __lt__(self, other):
        return self.uid < other.uid

    def does_not_have(self, key: ReachableKey):
        return key.letter not in self.keys_set

    def is_path_unlocked(self, key: ReachableKey):
        return self.keys_set.issuperset(key.needed)





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




