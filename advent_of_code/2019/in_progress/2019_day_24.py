#!/usr/bin/env python3



### IMPORTS ###

from collections import defaultdict
from copy import deepcopy

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.grid_2d import Grid2D


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

TEST_INPUT_2 = [
    """

    """, """

    """, """

    """
]

TEST_OUTPUT_2 = [
    0,
    0,
    0,
]

class RecursiveBugTower(object):
    """
    for order, use xyz when possible
    or col,row,level
    note y increases downwards
    """

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

        z=0

    def __str__(self):
        """
        1 level -> 0
        3 levels -> -1
        5 -> -2
        Returns:

        """
        result = ['\ntower:']
        magnitude = len(self.tower_dict) // 2
        for level in range(-magnitude, magnitude+1):
            result.append('\nlevel {}:\n{}'.format(level, self.tower_dict[level]))
        return ''.join(result)

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
        print(self)

        self.prev = deepcopy(self.tower_dict)

        magnitude = 1 + (self.generations // 2)
        for level in range(-magnitude, magnitude + 1):
            print(level)
            for y in range(5):
                for x in range(5):
                    self.resolve_coord(x, y, level)

        self.generations += 1

        z=0

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
        if x == 2 and y == 2:
            self.tower_dict[level].set(x, y, '?')
            return

        z=0



class BugGrid(Grid2D):

    BUG = '#'
    EMPTY = '.'

    def __init__(self, text, is_recursive=False):
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

        # self.solve_part_2()

    def run_tests(self):
        AocLogger.verbose = True
        BugGrid.test_diversity()

        AocLogger.verbose = False
        aoc_util.assert_equal(
            2129920,
            self.solve_part_1(TEST_INPUT_1[0])
        )

        AocLogger.verbose = True

        # for row in [0, 1, 3, 4]:
        #     coord = (RecursiveBugTower.MIDDLE, row, 0)
        #     print('{} -> {}'.format(
        #         coord, RecursiveBugTower.get_spots_up(*coord)))

        self.solve_test_case_2(TEST_INPUT_1[0])

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

    def solve_test_case_2(self, test_input):
        test_input = test_input.strip()
        AocLogger.log('solve_test_case_2 test input:\n{}'.format(test_input))

        tower = RecursiveBugTower(test_input)

        tower.inc()

        return 0

    def solve_part_2(self, puzzle_input: str):
        puzzle_input = puzzle_input.strip()

        result = 0

        print('part 2 result: {}'.format(result))
        return result





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




