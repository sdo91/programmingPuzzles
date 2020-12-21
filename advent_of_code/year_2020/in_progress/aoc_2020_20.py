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
from collections import defaultdict

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger
from advent_of_code.util.grid_2d import Grid2D

### CONSTANTS ###
TEST_INPUT = [
    """
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    20899048083289,
    0,
    0,
]

TEST_OUTPUT_2 = [
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
            error_msg = traceback.format_exc()
            print(error_msg)
            self.puzzle_input = 'unable to get input:\n\n{}'.format(error_msg)
        aoc_util.write_input(self.puzzle_input, __file__)

    def run(self):
        start_time = time.time()

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            0,
            self.solve_part_1(self.puzzle_input)
        )

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_2(self.puzzle_input)
        # )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

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
        # self.lines = aoc_util.lines(text)
        AocLogger.log(str(self))

        self.tiles_raw = text.split('\n\n')

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        """
        define 1st tile as origin
        loop thru unplaced tiles
        place each tile

        algo:
            for each partial tile:
                for each unmatched edge:
                    find the matching tile
                    place it
                    orient it:
                        check if normal or flipped
                        rotate until found
                        todo:
                            add flip/rotate methods to grid
                    add to partial list
                remove from partial list

        """

        counts = defaultdict(int)
        max_count = 0

        is_first = True

        unassigned_tiles = {}
        partial_tiles = {}
        # enclosed_tiles = {}  # just remove

        for text in self.tiles_raw:
            tile = Tile(text)
            if AocLogger.verbose:
                tile.show()

            for edge in tile.all_edges:
                counts[edge] += 1

                if counts[edge] > max_count:
                    max_count = counts[edge]

            if is_first:
                is_first = False
                tile.coord = (0, 0)
                tile.final_edges = tile.cw_edges
                partial_tiles[tile.id] = tile
            else:
                unassigned_tiles[tile.id] = tile

        # for partial_tile in partial_tiles.values():
        #     for unmatched_edge in partial_tile.get_unmatched_edges():
        #         pass

        z = 0
        return 1

    def p2(self):
        """

        """
        z = 0
        return 2


class Tile(Grid2D):
    """
    keep track of all edges

    keep track of CW edges, CCW edges

    potential.matches(edge)

    keep track of which edge is on each side


    given origin tile:
        check all tiles to find one that matches the top edge
        redraw that matching tile in the correct orientation
            or at least the edges
            algo:
                matching edge will be opposite origin edge (top -> bottom)
                if edge in normal edges:
                    # tile not flipped

                    rotate until correct edge is on top

                else:
                    # tile is flipped



    """

    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3

    def __init__(self, text):
        tokens = aoc_util.split_and_strip_each(text, ':')
        super().__init__(tokens[1])
        self.id = aoc_util.ints(tokens[0])[0]

        self.cw_edges = self.get_cw_edges()
        self.ccw_edges = self.get_ccw_edges()
        self.all_edges = set(self.cw_edges + self.ccw_edges)

        # init
        self.coord = None
        self.final_edges = None
        self.edge_matches = [False] * 4

        # self.is_flipped = None
        # self.rotation = None

    def __repr__(self):
        return 'coord={}, final={}'.format(self.coord, self.final_edges)

    def get_cw_edges(self):
        top = self.get_edge((0, 0), (1, 0))
        right = self.get_edge((9, 0), (0, 1))
        bottom = self.get_edge((9, 9), (-1, 0))
        left = self.get_edge((0, 9), (0, -1))

        return [
            top,
            right,
            bottom,
            left,
        ]

    def get_ccw_edges(self):
        return [
            self.reverse(self.cw_edges[self.TOP]),
            self.reverse(self.cw_edges[self.LEFT]),
            self.reverse(self.cw_edges[self.BOTTOM]),
            self.reverse(self.cw_edges[self.RIGHT]),
        ]

    def reverse(self, edge):
        return edge[::-1]

    # def get_all_edges(self):
    #     top = self.get_edge((0, 0), (1, 0))
    #     left = self.get_edge((0, 0), (0, 1))
    #     bottom = self.get_edge((9, 9), (-1, 0))
    #     right = self.get_edge((9, 9), (0, -1))
    #
    #     return [
    #         self.pick_edge(top),
    #         self.pick_edge(left),
    #         self.pick_edge(bottom),
    #         self.pick_edge(right),
    #     ]

    # def pick_edge(self, text: str):
    #     rev = text[::-1]
    #     return sorted([text, rev])[0]

    def get_edge(self, start, delta):
        result = []
        coord = start
        for _ in range(10):
            result.append(self.get_tuple(coord))
            coord = self.adjust_coord(coord, *delta)
        return ''.join(result)

    def get_unmatched_edges(self):
        pass


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
