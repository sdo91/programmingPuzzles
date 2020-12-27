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
    273,
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
            15670959891893,
            self.solve_part_1(self.puzzle_input)
        )

        aoc_util.assert_equal(
            0,
            self.solve_part_2(self.puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

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
        self.tiles_raw = text.split('\n\n')

        self.assembled_tile_ids = Grid2D()
        self.assembled_tile_ids.value_width = 5

        self.tiles_unassigned = {}
        self.tiles_in_progress = {}

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

        algo (top edge of OG tile):
            get string for top edge
            check each tile to find the one that contains the top edge
            orient the tile until it is correct
            place it in the picture
            add bottom to neighbors
            move list
        """
        self.assemble_tiles()

        result = 1
        result *= self.assembled_tile_ids.get_tuple(self.assembled_tile_ids.top_left())
        result *= self.assembled_tile_ids.get_tuple(self.assembled_tile_ids.top_right())
        result *= self.assembled_tile_ids.get_tuple(self.assembled_tile_ids.bottom_left())
        result *= self.assembled_tile_ids.get_tuple(self.assembled_tile_ids.bottom_right())
        return result

    def assemble_tiles(self):
        # make picture
        self.parse_tiles()
        while self.tiles_unassigned:
            self.assembled_tile_ids.show()
            self.process_tiles()
            time.sleep(0.1)
        self.assembled_tile_ids.show()

    def process_tiles(self):
        tiles_to_add = {}
        tiles_to_remove = set()

        for old_tile in self.tiles_in_progress.values():  # type: Tile
            if AocLogger.verbose:
                print('tile in progress: {}'.format(old_tile.id))
                old_tile.grid.show()

            for side, edge_str in old_tile.get_unmatched_edges().items():
                old_tile.sides_visited[side] = True  # do I need this?

                # get the coord on that side
                new_coord = old_tile.get_coord_to_side(side)

                if self.assembled_tile_ids.has_coord(new_coord):
                    AocLogger.log('coord already processed: {}'.format(new_coord))
                    continue

                new_tile = self.find_match(side, edge_str)
                if new_tile:
                    new_tile.coord = new_coord
                    self.assembled_tile_ids.set_tuple(new_tile.coord, new_tile.id)
                    if AocLogger.verbose:
                        AocLogger.log('new tile in picture:')
                        self.assembled_tile_ids.show()

                    # add new tile
                    tiles_to_add[new_tile.id] = new_tile

            # mark tile as done
            tiles_to_remove.add(old_tile.id)

        # update tiles in progress
        for tile_id in tiles_to_remove:
            del self.tiles_in_progress[tile_id]
        for tile_id, tile in tiles_to_add.items():
            del self.tiles_unassigned[tile_id]
            self.tiles_in_progress[tile_id] = tile

    def find_match(self, side: int, edge: str):
        """
        find match if it exists
        (ie, not on the edge)
        """
        AocLogger.log('finding match: {}'.format([side, edge]))

        for tile in self.tiles_unassigned.values():  # type: Tile
            if edge in tile.all_edges:
                AocLogger.log('match found')
                # match found, orient the tile

                opposite_side = (side + 2) % 4
                flipped_edge = Tile.reverse(edge)
                tile.orient(opposite_side, flipped_edge)
                tile.sides_visited[opposite_side] = True

                return tile

        # if we get to here, we are on an edge
        return None

    def parse_tiles(self):
        counts = defaultdict(int)
        max_count = 0

        # initialize all tiles
        is_first = True
        for text in self.tiles_raw:
            tile = Tile(text, is_first)
            # if AocLogger.verbose:
            #     tile.grid.show()

            for edge in tile.all_edges:
                counts[edge] += 1
                if counts[edge] > max_count:
                    max_count = counts[edge]

            if is_first:
                is_first = False
                tile.coord = (0, 0)
                self.assembled_tile_ids.set_tuple(tile.coord, tile.id)
                if AocLogger.verbose:
                    self.assembled_tile_ids.show()

                self.tiles_in_progress[tile.id] = tile
            else:
                self.tiles_unassigned[tile.id] = tile

    def p2(self):
        """

        """
        self.assemble_tiles()



        z = 0
        return 2


class Tile:
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

    def __init__(self, text, is_first):
        tokens = aoc_util.split_and_strip_each(text, ':')
        self.id = aoc_util.ints(tokens[0])[0]

        self.grid = Grid2D(tokens[1])  # type: Grid2D
        if is_first and AocLogger.verbose:
            self.grid = self.grid.flip('X')
            self.grid = Grid2D(repr(self.grid))
            print('flipped:')
            self.grid.show()

        self.cw_edges = self.get_cw_edges()
        self.all_edges = self.cw_edges | self.get_ccw_edges()

        # init
        self.coord = None
        self.sides_visited = [False] * 4  # True: visited (todo: is this needed?)

    def __repr__(self):
        return 'coord={}, id={}'.format(self.coord, self.id)

    def orient(self, side: int, edge: str):
        """
        orient the tile such that the edge is at the side
        """
        if edge not in self.cw_edges:
            AocLogger.log('flip')
            self.grid = self.grid.flip('y')

        self.rotate(side, edge)
        # rotation should be correct now

    def rotate(self, side: int, edge: str):
        """
        rotate until correct
        """
        for x in range(4):
            if self.get_edge_on_side(side) == edge:
                return
            AocLogger.log('rotate')
            self.grid = self.grid.rot90()
        assert False

    def get_edge_on_side(self, side: int):
        if side == self.TOP:
            return self.get_edge(self.grid.top_left(), (1, 0))
        elif side == self.RIGHT:
            return self.get_edge(self.grid.top_right(), (0, 1))
        elif side == self.BOTTOM:
            return self.get_edge(self.grid.bottom_right(), (-1, 0))
        elif side == self.LEFT:
            return self.get_edge(self.grid.bottom_left(), (0, -1))
        else:
            assert False

    def get_cw_edges(self):
        result = set()
        for side in range(4):
            result.add(self.get_edge_on_side(side))
        return result

    def get_ccw_edges(self):
        result = set()
        for edge in self.cw_edges:
            result.add(self.reverse(edge))
        return result

    @classmethod
    def reverse(cls, edge):
        return edge[::-1]

    def get_edge(self, start, delta):
        result = []
        coord = start
        for _ in range(10):
            result.append(self.grid.get_tuple(coord))
            coord = Grid2D.adjust_coord(coord, *delta)
        return ''.join(result)

    def get_unmatched_edges(self):
        """
        Returns:
            dict[int, str]: edges not yet matched
        """
        # self.show()
        result = {}
        for side in range(4):
            if not self.sides_visited[side]:
                # side has not been checked
                result[side] = self.get_edge_on_side(side)
        return result

    def get_coord_to_side(self, side: int):
        old_coord = self.coord
        if side == self.TOP:
            new_coord = Grid2D.get_coord_north(old_coord)
        elif side == self.RIGHT:
            new_coord = Grid2D.get_coord_east(old_coord)
        elif side == self.BOTTOM:
            new_coord = Grid2D.get_coord_south(old_coord)
        elif side == self.LEFT:
            new_coord = Grid2D.get_coord_west(old_coord)
        else:
            assert False
        return new_coord


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
