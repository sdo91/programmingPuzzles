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
from advent_of_code.util.dijkstra_solver import DijkstraSolver


### CONSTANTS ###
TEST_INPUT = [
    """
depth: 510
target: 10,10
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    114,
    0,
    0,
]

TEST_OUTPUT_2 = [
    45,
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

        aoc_util.assert_equal(
            7915,
            self.solve_part_1(self.puzzle_input)
        )

        aoc_util.assert_equal(
            980,
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
        AocLogger.log(str(self))

        ints = aoc_util.ints(self.text)
        self.depth = ints[0]
        self.target = tuple(ints[1:])

        self.erosion_levels = Grid2D()

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def calc_geologic_index(self, coord):
        """
        The geologic index can be determined using the first rule that applies from the list below:
            - The region at 0,0 (the mouth of the cave) has a geologic index of 0.
            - The region at the coordinates of the target has a geologic index of 0.
            - If the region's Y coordinate is 0, the geologic index is its X coordinate times 16807.
            - If the region's X coordinate is 0, the geologic index is its Y coordinate times 48271.
            - Otherwise, the region's geologic index is the result of multiplying the erosion levels
                of the regions at X-1,Y and X,Y-1.

        Returns:
            int
        """
        if coord == (0, 0) or coord == self.target:
            return 0
        if coord[1] == 0:
            return coord[0] * 16807
        if coord[0] == 0:
            return coord[1] * 48271
        west = self.erosion_levels.get_coord_west(coord)
        north = self.erosion_levels.get_coord_north(coord)
        return self.erosion_levels.get_tuple(west) * self.erosion_levels.get_tuple(north)

    def calc_erosion_level(self, geologic_index):
        """
        A region's erosion level is its geologic index plus the cave system's depth, all modulo 20183. Then:
            - If the erosion level modulo 3 is 0, the region's type is rocky.
            - If the erosion level modulo 3 is 1, the region's type is wet.
            - If the erosion level modulo 3 is 2, the region's type is narrow.

        Returns:
            int
        """
        return (geologic_index + self.depth) % 20183

    @staticmethod
    def to_type(erosion_level):
        risk = erosion_level % 3
        if risk == 0:
            return '.'  # rocky
        elif risk == 1:
            return '='  # wet
        else:
            return '|'  # narrow

    def p1(self):
        """

        """

        total_risk = 0
        for y in range(self.target[1] + 1):
            for x in range(self.target[0] + 1):
                coord = (x, y)

                geologic_index = self.calc_geologic_index(coord)
                erosion_level = self.calc_erosion_level(geologic_index)

                self.erosion_levels.set_tuple(coord, erosion_level)

                total_risk += (erosion_level % 3)

        if AocLogger.verbose:
            self.erosion_levels.show_converted(self.to_type)
        print('total_risk: {}'.format(total_risk))

        return total_risk

    def p2(self):
        """

        """
        is_example = (self.target == (10, 10))

        if is_example:
            buffer = 6
        else:
            buffer = 20

        cave_grid = Grid2D(default=None)

        for y in range(self.target[1] + buffer):
            for x in range(self.target[0] + buffer):
                coord = (x, y)

                geologic_index = self.calc_geologic_index(coord)
                erosion_level = self.calc_erosion_level(geologic_index)

                self.erosion_levels.set_tuple(coord, erosion_level)
                cave_grid.set_tuple(coord, erosion_level % 3)

        if AocLogger.verbose:
            self.erosion_levels.show_converted(self.to_type)
            cave_grid.show()

        solver = CaveSolver(cave_grid, {0, 1, 2}, self.target)
        start_coord = (0, 0, CaveSolver.TOOL_TORCH)
        node = solver.find_shortest_path(start_coord)

        # trace path
        prev_tool = CaveSolver.TOOL_TORCH
        max_x_coord = 0
        num_switches = 0
        cave_grid.overlay[(0, 0)] = ' '
        for coord_3d in node.path:
            x, y, tool = coord_3d
            coord_2d = x, y
            max_x_coord = max(max_x_coord, x)

            if tool != prev_tool:
                # switch tool
                cave_grid.overlay[coord_2d] = 'S'
                prev_tool = tool
                num_switches += 1
            else:
                cave_grid.overlay[coord_2d] = ' '

        cave_grid.value_width = 1
        cave_grid.show_converted(self.to_type)
        print('max_x_coord: {}'.format(max_x_coord))
        print('num_switches: {}'.format(num_switches))

        return node.dist


class CaveSolver(DijkstraSolver):

    TOOL_NONE = 0   # not rocky
    TOOL_TORCH = 1  # not wet
    TOOL_GEAR = 2   # not narrow

    def __init__(self, grid, open_chars, target_2d):
        super().__init__(grid, open_chars, set())
        self.target_3d = (target_2d[0], target_2d[1], self.TOOL_TORCH)

    def is_done(self, coord):
        return coord == self.target_3d

    def get_adjacent(self, coord):
        x, y, tool = coord
        adj_coords = [
            (x + 0, y - 1, tool),
            (x - 1, y + 0, tool),
            (x + 1, y + 0, tool),
            (x + 0, y + 1, tool),
            (x, y, (tool - 1) % 3),
            (x, y, (tool + 1) % 3),
        ]
        return adj_coords

    def can_reach(self, coord):
        x, y, tool = coord
        if x < 0 or y < 0:
            return False
        region_type = self.grid.get(x, y)
        if region_type is None:
            # hack: coord is OOB
            return False
        if tool == region_type:
            return False
        return True

    def distance(self, first, second):
        if first[2] == second[2]:
            return 1
        else:
            return 7






if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




