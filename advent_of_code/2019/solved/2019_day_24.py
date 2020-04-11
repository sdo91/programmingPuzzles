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

from collections import defaultdict
from copy import deepcopy

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger
from advent_of_code.util.grid_2d import Grid2D


### CONSTANTS ###
TEST_INPUT_1 = [
    """
....#
#..#.
#..##
..#..
#....
    """, """
.....
.....
.....
#....
.#...
    """, """

    """
]










class RecursiveBugTower(object):
    """
    for order, use xyz when possible
    or col,row,level
    note y increases downwards
    """

    BUG = '#'
    EMPTY = '.'

    MIDDLE = 2

    TOP = 0
    BOTTOM = 4
    LEFT = 0
    RIGHT = 4

    SECOND_FROM_TOP = 1
    SECOND_FROM_BOTTOM = 3
    SECOND_FROM_LEFT = 1
    SECOND_FROM_RIGHT = 3

    def __init__(self, text):
        self.tower_dict = defaultdict(lambda: Grid2D())
        self.tower_dict[0] = Grid2D(text)
        self.generations = 0
        self.prev = None
        self.total_bugs = 0

    def __str__(self):
        """
        1 level -> 0
        3 levels -> -1
        5 -> -2
        """
        info = 'tower ({} generations, {} bugs):\n'.format(
            self.generations, self.total_bugs)
        result = ['\n\n\n\n\n', info]
        magnitude = len(self.tower_dict) // 2
        for level in range(-magnitude, magnitude+1):
            result.append('level {}:\n{}\n'.format(level, self.tower_dict[level]))
        result.append(info)
        return '\n'.join(result)

    def inc(self):
        """
        0,1 -> 1
        2,3 -> 2

        algo:
            make a copy (prev)
            for each level (-1 to 1):
                for each spot
                    count adjacent
        """
        self.prev = deepcopy(self.tower_dict)
        self.total_bugs = 0

        magnitude = 1 + (self.generations // 2)
        self.generations += 1

        for level in range(-magnitude, magnitude + 1):
            # print('debug: gen={}, level={}'.format(self.generations, level))
            for y in range(5):
                for x in range(5):
                    self.resolve_coord(x, y, level)

        AocLogger.log(self)


    def resolve_coord(self, x, y, level):
        """
        (2,2) -> ?

        algo:
            get adjacent spots
            count bugs

        get up:
            special cases:
                18: uvwxy
                ABCDE: 8
        """
        # middle is always ?
        if x == 2 and y == 2:
            self.tower_dict[level].set(x, y, '?')
            return

        # gat all adjacent
        adjacent_spots = []
        adjacent_spots += self.get_spots_up(x, y, level)
        adjacent_spots += self.get_spots_right(x, y, level)
        adjacent_spots += self.get_spots_down(x, y, level)
        adjacent_spots += self.get_spots_left(x, y, level)

        # count bugs
        adjacent_bugs = 0
        for coord in adjacent_spots:
            value = self.prev[coord[2]].get(coord[0], coord[1])
            if value == '#':
                adjacent_bugs += 1

        # apply rules
        new_value = self.EMPTY
        if self.prev[level].is_value((x, y), self.BUG):
            if adjacent_bugs == 1:
                new_value = self.BUG
        else:  # was empty
            if 1 <= adjacent_bugs <= 2:
                new_value = self.BUG

        if new_value == self.BUG:
            self.total_bugs += 1
        self.tower_dict[level].set(x, y, new_value)

    @classmethod
    def get_spots_up(cls, col, row, level):
        """
        the grid within 0 is level 1
        the grid that contains 0 is level -1

        special cases:
            18: uvwxy (level +1 bottom row)
            ABCDE (top row): 8 (of level -1)
        """
        result = []
        if col == cls.MIDDLE and row == cls.SECOND_FROM_BOTTOM:
            # 18 -> UVWXY
            result_row = cls.BOTTOM
            for result_col in range(5):
                result.append((result_col, result_row, level + 1))
        elif row == cls.TOP:
            # ABCDE -> 8
            result_row = cls.SECOND_FROM_TOP
            result_col = cls.MIDDLE
            result.append((result_col, result_row, level - 1))
        else:
            result.append((col, row - 1, level))
        return result

    @classmethod
    def get_spots_down(cls, col, row, level):
        result = []
        if col == cls.MIDDLE and row == cls.SECOND_FROM_TOP:
            # 8 -> ABCDE
            result_row = cls.TOP
            for result_col in range(5):
                result.append((result_col, result_row, level + 1))
        elif row == cls.BOTTOM:
            # UVWXY -> 18
            result_row = cls.SECOND_FROM_BOTTOM
            result_col = cls.MIDDLE
            result.append((result_col, result_row, level - 1))
        else:
            result.append((col, row + 1, level))
        return result

    @classmethod
    def get_spots_left(cls, col, row, level):
        result = []
        if row == cls.MIDDLE and col == cls.SECOND_FROM_RIGHT:
            # 14 -> E-Y
            result_col = cls.RIGHT
            for result_row in range(5):
                result.append((result_col, result_row, level + 1))
        elif col == cls.LEFT:
            # A-U -> 12
            result_col = cls.SECOND_FROM_LEFT
            result_row = cls.MIDDLE
            result.append((result_col, result_row, level - 1))
        else:
            result.append((col - 1, row, level))
        return result

    @classmethod
    def get_spots_right(cls, col, row, level):
        result = []
        if row == cls.MIDDLE and col == cls.SECOND_FROM_LEFT:
            # 12 -> A-U
            result_col = cls.LEFT
            for result_row in range(5):
                result.append((result_col, result_row, level + 1))
        elif col == cls.RIGHT:
            # E-Y -> 14
            result_col = cls.SECOND_FROM_RIGHT
            result_row = cls.MIDDLE
            result.append((result_col, result_row, level - 1))
        else:
            result.append((col + 1, row, level))
        return result




class BugGrid(Grid2D):

    BUG = '#'
    EMPTY = '.'

    def __init__(self, text, is_recursive=False):
        text = text.strip()
        super().__init__(text)
        self.is_recursive = is_recursive

    def update(self, prev):
        """
        Each minute, The bugs live and die based on the number of bugs in the four adjacent tiles:
            -A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
            -An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
        """
        for x in range(5):
            for y in range(5):
                coord = (x, y)
                adjacent_bugs = prev.count_adjacent(x, y, self.BUG)
                if prev.is_value(coord, self.BUG):
                    if adjacent_bugs == 1:
                        self.set_tuple(coord, self.BUG)
                    else:
                        self.set_tuple(coord, self.EMPTY)
                else:  # was empty
                    if 1 <= adjacent_bugs <= 2:
                        self.set_tuple(coord, self.BUG)
                    else:
                        self.set_tuple(coord, self.EMPTY)

    def calc_biodiversity(self):
        rating = 0
        points = 1
        for row in range(5):
            for col in range(5):
                if self.is_value((col, row), self.BUG):
                    rating += points
                points *= 2
        return rating

    @staticmethod
    def test_diversity():
        grid = BugGrid(TEST_INPUT_1[1])
        aoc_util.assert_equal(
            2129920,
            grid.calc_biodiversity()
        )






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

        aoc_util.assert_equal(
            13500447,
            self.solve_part_1(puzzle_input)
        )

        aoc_util.assert_equal(
            2120,
            self.solve_part_2(puzzle_input, 200)
        )

    def run_tests(self):
        AocLogger.verbose = True
        BugGrid.test_diversity()

        AocLogger.verbose = False
        aoc_util.assert_equal(
            2129920,
            self.solve_part_1(TEST_INPUT_1[0])
        )

        AocLogger.verbose = True

        for row in [0, 1, 3, 4]:
            coord = (RecursiveBugTower.MIDDLE, row, 0)
            print('{} -> {}'.format(
                coord, RecursiveBugTower.get_spots_up(*coord)))

        self.solve_part_2(TEST_INPUT_1[0], 10)

    def solve_part_1(self, test_input):
        test_input = test_input.strip()
        AocLogger.log('test input:\n{}'.format(test_input))

        prev_grid = BugGrid(test_input)
        grid = BugGrid(test_input)

        all_ratings = set()

        gen = 1
        while True:
            AocLogger.log('gen: {}'.format(gen))

            biodiversity = grid.calc_biodiversity()
            if biodiversity in all_ratings:
                grid.show()
                print('biodiversity: {}'.format(biodiversity))
                break
            else:
                all_ratings.add(biodiversity)

            # do next gen
            prev_grid, grid = grid, prev_grid
            grid.update(prev_grid)
            if AocLogger.verbose:
                grid.show()
            gen += 1

        return biodiversity

    def solve_part_2(self, test_input, num_gens):
        test_input = test_input.strip()
        AocLogger.log('solve_part_2 test input:\n{}'.format(test_input))

        tower = RecursiveBugTower(test_input)

        AocLogger.log(tower)

        for i in range(num_gens):
            if i > 0 and i % int(num_gens // 10) == 0:
                print('{}%'.format(int(i / num_gens * 100)))
            tower.inc()

        p2_result = tower.total_bugs
        print('p2_result: {}'.format(p2_result))
        return tower.total_bugs





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




