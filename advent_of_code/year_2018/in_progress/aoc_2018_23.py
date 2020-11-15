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

import aocd
import math
import time
import traceback

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger

### CONSTANTS ###
TEST_INPUT = [
    """
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
    """, """
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
#pos=<50,50,50>, r=200
pos=<30,30,30>, r=60
pos=<10,10,10>, r=5
    """, """
pos=<10,10,0>, r=3
pos=<15,11,0>, r=5
    """
]

TEST_OUTPUT_1 = [
    7,
    6,
    None,
]

TEST_OUTPUT_2 = [
    None,
    36,
    21,
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
            399,
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
        self.test_poi_finders()
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def test_poi_finders(self):
        case_1 = 'pos=<10,10,0>, r=3 \n pos=<15,11,0>, r=5'
        solver = Solver(case_1)
        assert solver.test_poi_finders()

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


class Nanobot(object):

    def __init__(self, text):
        ints = aoc_util.ints(text)
        self.pos = tuple(ints[:3])
        self.radius = ints[-1]

    def __repr__(self):
        return 'pos={}, r={}'.format(self.pos, self.radius)

    def can_see(self, other_pos: tuple) -> bool:
        dist = aoc_util.manhatten_dist(self.pos, other_pos)
        return dist <= self.radius

    def get_corners(self):
        # todo: 2d -> 3d
        x, y, z = self.pos
        return [
            (x + 0, y - 1, z),
            (x + 1, y + 0, z),
            (x + 0, y + 1, z),
            (x - 1, y + 0, z),
        ]

    def calc_range(self, other, axis):
        min_index = min(self.pos[axis] - self.radius, other.pos[axis] - other.radius)
        max_index = max(self.pos[axis] + self.radius, other.pos[axis] + other.radius)
        return range(min_index, max_index + 1)


class Solver(object):

    def __init__(self, text: str):
        self.text = text.strip()
        self.lines = aoc_util.lines(self.text)
        AocLogger.log(str(self))

        self.nanobots = []
        for line in self.lines:
            if line.startswith('#'):
                continue
            bot = Nanobot(line)
            self.nanobots.append(bot)

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        """

        """

        max_rad = 0
        max_bot = None

        for bot in self.nanobots:
            if bot.radius > max_rad:
                max_rad = bot.radius
                max_bot = bot

        total_in_range = 0
        for bot in self.nanobots:
            if max_bot.can_see(bot.pos):
                total_in_range += 1

        return total_in_range

    def p2(self):
        """
        To increase the probability of success, you need to find the coordinate which puts you in range of the
        largest number of nanobots. If there are multiple, choose one closest to your position
        (0,0,0, measured by manhattan distance).

        algo:
            find all POI
                2d case
                get corners that are in range of both
                find all coords (4-6 that define the intersection)

            find best POI

        """

        points_of_interest = set()
        for i in aoc_util.range_len(self.nanobots):
            for j in range(i + 1, len(self.nanobots)):
                poi = self.find_points_of_interest_slow(self.nanobots[i], self.nanobots[j])
                points_of_interest |= poi

        # find best (not sure if this will be fast enough...)
        max_count = 0
        max_points = set()
        for point in points_of_interest:
            num_bots = 0
            for bot in self.nanobots:
                if bot.can_see(point):
                    num_bots += 1

            if num_bots > max_count:
                max_count = num_bots
                max_points.clear()
            if num_bots == max_count:
                max_points.add(point)

        # find closest of best
        shortest_dist = math.inf
        for point in max_points:
            dist = aoc_util.manhatten_dist(point, (0, 0, 0))
            if dist < shortest_dist:
                print('best so far: {}'.format(point))
                shortest_dist = dist

        return shortest_dist

    def find_points_of_interest_slow(self, first: Nanobot, second: Nanobot):
        """
        for now:
            2d only
            slow
        """
        print('comparing: {}'.format([first, second]))
        # corners = set()
        # for p in first.get_corners() + second.get_corners():
        #     corners.add(p)

        # first.calc_range(second.pos, 0)

        min_x = math.inf
        min_y = math.inf
        max_x = -math.inf
        max_y = -math.inf

        points_in_both = set()
        for z in first.calc_range(second, 2):
            for y in first.calc_range(second, 1):
                for x in first.calc_range(second, 0):
                    point = x, y, z
                    # if point == (12, 12, 12):
                    #     z = 0
                    if first.can_see(point) and second.can_see(point):
                        points_in_both.add(point)

                        if x < min_x:
                            min_x = x
                        if y < min_y:
                            min_y = y

                        if x > max_x:
                            max_x = x
                        if y > max_y:
                            max_y = y

        result = set()
        for point in points_in_both:
            x, y, z = point
            if x == min_x or x == max_x or y == min_y or y == max_y:
                result.add(point)

        return result

    def find_points_of_interest_fast(self, first: Nanobot, second: Nanobot):
        return set()

    def test_poi_finders(self):
        slow = self.find_points_of_interest_slow(self.nanobots[0], self.nanobots[1])
        fast = self.find_points_of_interest_fast(self.nanobots[0], self.nanobots[1])
        return slow == fast


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
