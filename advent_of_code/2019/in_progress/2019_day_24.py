#!/usr/bin/env python3



### IMPORTS ###

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





class BugGrid(Grid2D):

    BUG = '#'
    EMPTY = '.'

    def __init__(self, text):
        super().__init__(text)

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

    def run_tests(self):
        AocLogger.verbose = True
        BugGrid.test_diversity()

        AocLogger.verbose = False
        aoc_util.assert_equal(
            2129920,
            self.solve_part_1(TEST_INPUT_1[0])
        )

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
        AocLogger.log('test input: {}'.format(test_input))
        return 0

    def solve_part_2(self, puzzle_input: str):
        puzzle_input = puzzle_input.strip()

        result = 0

        print('part 2 result: {}'.format(result))
        return result





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




