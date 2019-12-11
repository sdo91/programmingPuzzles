#!/usr/bin/env python3



### IMPORTS ###

import numpy as np
from fractions import Fraction

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
# from aoc_util.intcode_computer import IntcodeComputer


### CONSTANTS ###
TEST_INPUT_1 = [
    """
.#..#
.....
#####
....#
...##
    """,
    """

    """, """

    """
]

TEST_OUTPUT_1 = [
    ((3,4),8),
    0,
    0,
]

TEST_INPUT_2 = [
    """
.#..#
.....
#####
....#
...##
    """, """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
    """, """

    """
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

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        try:
            puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            puzzle_input = 'unable to get input'
        aoc_util.write_input(puzzle_input, __file__)

        AocLogger.verbose = True
        # aoc_util.run_tests(self.solve_test_case_1, TEST_INPUT_1, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_test_case_2, TEST_INPUT_2, TEST_OUTPUT_2)

        # self.solve_test_case_2(TEST_INPUT_2[0], 8)

        AocLogger.verbose = False

        # self.solve_test_case_2(TEST_INPUT_2[1], 200)

        self.solve_test_case_2(puzzle_input, 200)

        # self.solve_test_case_1(puzzle_input)

        # self.solve_part_2(puzzle_input)

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_1(puzzle_input)
        # )

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_2(puzzle_input)
        # )

    def solve_test_case_1(self, test_input: str):
        test_input = test_input.strip()
        AocLogger.log('test input: {}'.format(test_input))
        lines = test_input.split('\n')

        num_rows = len(lines)
        num_cols = len(lines[0])

        self.all_asteroids = set()
        # row = 0
        # for line in lines:
        #     col = 0
        #     for c in line:
        #         if c != '.':
        #             all_asteroids.add((row, col))
        #         col += 1
        #     row += 1


        for row in range(num_rows):
            for col in range(num_cols):
                if lines[row][col] != '.':
                    self.all_asteroids.add((col, row))


        assert not self.is_visible(
            (1,0),
            (3,4)
        )

        assert not self.is_visible(
            (4,0),
            (4,4)
        )

        # self.all_asteroids = list(self.all_asteroids)

        site_dict = {}
        max_vis = 0
        best_coords = None
        for potential_site in self.all_asteroids:
            AocLogger.log('\nchecking site: {}'.format(potential_site))
            visible_asteroids = 0
            # check which are visible
            for a in self.all_asteroids:
                if self.is_visible(a, potential_site):
                    visible_asteroids += 1
            site_dict[potential_site] = visible_asteroids
            AocLogger.log('site result: {}'.format(visible_asteroids))

            if visible_asteroids > max_vis:
                max_vis = visible_asteroids
                best_coords = potential_site

        result = best_coords, max_vis
        print('result: {}'.format(result))
        return result

    def is_visible(self, a, potential_site):
        if a == potential_site:
            # can't see self
            return False

        rel_x = a[0] - potential_site[0]
        rel_y = a[1] - potential_site[1]

        if rel_x == 0:
            # handle inf slope case

            # since both x are equal, check all y points

            min_y = min(a[1], potential_site[1])
            max_y = max(a[1], potential_site[1])

            for y in range(min_y + 1, max_y):
                potential_blocker = (a[0], y)
                if potential_blocker in self.all_asteroids:
                    AocLogger.log('{} blocks {}'.format(potential_blocker, a))
                    return False
        else:
            slope = Fraction(rel_y, rel_x)
            # slope = rel_y / rel_x

            min_x = min(a[0], potential_site[0])
            max_x = max(a[0], potential_site[0])

            for x in range(min_x + 1, max_x):
                y = self.get_y(slope, x, a)

                if y.denominator == 1:
                    # valid point
                    y_int = int(y)

                    potential_blocker = (x, y_int)

                    if potential_blocker in self.all_asteroids:
                        AocLogger.log('{} blocks {}'.format(potential_blocker, a))
                        return False

                    # print([x, y_int])

        # get x mids



        AocLogger.log('no blockers found for {}'.format(a))
        return True

    def get_y(self, m, x, point):
        """
        y = m(x - x_1) + y_1
        """
        return m * (x - point[0]) + point[1]

    def solve_part_1(self, puzzle_input: str):
        puzzle_input = puzzle_input.strip()

        result = 0

        print('part 1 result: {}'.format(result))
        return result

    def solve_test_case_2(self, test_input, n):
        test_input = test_input.strip()
        AocLogger.log('test input: {}'.format(test_input))
        lines = test_input.split('\n')

        num_rows = len(lines)
        num_cols = len(lines[0])

        self.all_asteroids = set()

        for row in range(num_rows):
            for col in range(num_cols):
                if lines[row][col] != '.':
                    self.all_asteroids.add((col, row))



        site_dict = {}
        max_vis = 0
        best_coords = None
        for potential_site in self.all_asteroids:
            AocLogger.log('\nchecking site: {}'.format(potential_site))
            visible_asteroids = []
            # check which are visible
            for a in self.all_asteroids:
                if self.is_visible(a, potential_site):
                    visible_asteroids.append(a)
            site_dict[potential_site] = visible_asteroids
            AocLogger.log('site result: {}'.format(visible_asteroids))

            if len(visible_asteroids) > max_vis:
                max_vis = len(visible_asteroids)
                best_coords = potential_site

        result = best_coords, max_vis, site_dict[best_coords]
        print('result: {}'.format(result))


        best_x = best_coords[0]
        best_y = best_coords[1]

        right_side_count = 0
        slope_dict = {}
        for visible_asteroid in site_dict[best_coords]:
            vis_x = visible_asteroid[0]
            vis_y = visible_asteroid[1]
            if vis_x >= best_x:
                right_side_count += 1
            else:
                # strictly left side
                rel_x = vis_x - best_x
                rel_y = vis_y - best_y

                slope = Fraction(rel_y, rel_x)

                slope_dict[slope] = visible_asteroid

        print('right_side_count: {}'.format(right_side_count))
        print('left_side_count: {}'.format(len(slope_dict)))

        sorted_left_side_keys = list(sorted(slope_dict.keys()))
        # for key in sorted_left_side_keys:
        #     print('{}: {}'.format(key, slope_dict[key]))

        left_side_index = n - right_side_count - 1
        final_idx = sorted_left_side_keys[left_side_index]

        final_coord = slope_dict[final_idx]
        print('{}th: {}, {}'.format(n, final_coord, final_coord[0] * 100 + final_coord[1]))

        return result

    def solve_part_2(self, puzzle_input: str):
        puzzle_input = puzzle_input.strip()

        result = 0

        print('part 2 result: {}'.format(result))
        return result





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




