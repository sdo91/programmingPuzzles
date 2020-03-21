#!/usr/bin/env python3



### IMPORTS ###

from fractions import Fraction

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger


### CONSTANTS ###
TEST_INPUT = [
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
            [(20, 19), 284, (4, 4), 404],
            self.solve_puzzle(puzzle_input, 200)
        )

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.assert_equal(
            [(3, 4), 8, (2, 2), 202],
            self.solve_puzzle(TEST_INPUT[0], 8)
        )
        AocLogger.verbose = False
        aoc_util.assert_equal(
            [(11, 13), 210, (8, 2), 802],
            self.solve_puzzle(TEST_INPUT[1], 200)
        )

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

        AocLogger.log('no blockers found for {}'.format(a))
        return True

    def get_y(self, m, x, point):
        """
        y = m(x - x_1) + y_1
        """
        return m * (x - point[0]) + point[1]

    def solve_puzzle(self, test_input, n):
        print()
        test_input = test_input.strip()
        AocLogger.log('test input:\n{}'.format(test_input))
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

        print('best_coords, max_vis: {}'.format([best_coords, max_vis]))

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
        result_2 = final_coord[0] * 100 + final_coord[1]
        print('{}th: {}, {}'.format(n, final_coord, result_2))

        result = [best_coords, max_vis, final_coord, result_2]
        print('result: {}'.format(result))
        return result





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




