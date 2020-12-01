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
import pprint
import random
import time
import traceback

from collections import defaultdict

from advent_of_code.util import aoc_util
from advent_of_code.util import math_3d
from advent_of_code.util.aoc_util import AocLogger
from advent_of_code.util.math_3d import Polygon

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

        # make sure both algos are same
        test_cases = [

            'pos=<10,10,10>, r=10 \n pos=<12,14,16>, r=10',

            # 24 pts (max possible)
            'pos=<1,1,3>, r=12 \n pos=<7,5,9>, r=13',
            'pos=<8,8,9>, r=12 \n pos=<2,2,5>, r=11',

            # line on z plane
            'pos=<0,9,0>, r=15 \n pos=<8,0,0>, r=15',

            # 'pos=<9,10,0>, r=14 \n pos=<0,1,0>, r=13',
            # 'pos=<10,9,0>, r=14 \n pos=<1,0,0>, r=15',

            'pos=<2,9,7>, r=12 \n pos=<10,0,0>, r=15',

            'pos=<10,10,0>, r=3 \n pos=<15,11,2>, r=5',
            'pos=<10,10,0>, r=3 \n pos=<15,11,1>, r=5',
            'pos=<10,10,0>, r=3 \n pos=<15,11,0>, r=5',

            'pos=<10,1,0>, r=9 \n pos=<2,5,0>, r=15',
            'pos=<13,7,9>, r=13 \n pos=<14,11,0>, r=13',
            'pos=<10,10,0>, r=3 \n pos=<15,11,0>, r=5',

        ]
        for case in test_cases:
            solver = Solver(case)

            poi_slow = solver.find_points_of_interest_slow(*solver.get_first_pair())
            poi_slow = sorted(poi_slow)

            poi_fast = solver.find_points_of_interest_fast(*solver.get_first_pair())

            assert solver.test_poi_finders()

        # # randomize
        # counts = defaultdict(int)
        # cases = defaultdict(list)
        # bound_xy = 10
        # bound_r = 15
        # for x in range(10000):
        #     text = 'pos=<{},{},{}>, r={} \n pos=<{},{},{}>, r={}'.format(
        #         # random.randint(0, bound_xy), random.randint(0, bound_xy), 0,
        #         random.randint(0, bound_xy), random.randint(0, bound_xy), random.randint(0, bound_xy),
        #         random.randint(0, bound_r),
        #         # random.randint(0, bound_xy), random.randint(0, bound_xy), 0,
        #         random.randint(0, bound_xy), random.randint(0, bound_xy), random.randint(0, bound_xy),
        #         random.randint(0, bound_r),
        #     )
        #     solver = Solver(text)
        #     poi = solver.find_points_of_interest_slow(*solver.get_first_pair())
        #
        #     counts[len(poi)] += 1
        #
        #     if len(poi) >= 24:
        #         cases[len(poi)].append(text)
        #
        #     # if len(poi) == 32:
        #     #     print(text)
        #
        #     # poi = sorted(poi)
        #
        # # print(counts)
        #
        # # pp = pprint.PrettyPrinter(indent=4)
        # # pp.print(counts)
        #
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(counts)
        # pp.pprint(cases)
        #
        # z = 0
        # assert False

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
        x, y, z = self.pos
        return [
            (x - self.radius, y, z),
            (x + self.radius, y, z),
            (x, y - self.radius, z),
            (x, y + self.radius, z),
            (x, y, z - self.radius),
            (x, y, z + self.radius),
        ]

    def calc_range(self, other, axis):
        min_index = min(self.pos[axis] - self.radius, other.pos[axis] - other.radius)
        max_index = max(self.pos[axis] + self.radius, other.pos[axis] + other.radius)
        return range(min_index, max_index + 1)

    def get_faces(self):
        corners = self.get_corners()
        x_corners = corners[0:2]
        y_corners = corners[2:4]
        z_corners = corners[4:6]

        result = []
        for xc in x_corners:
            for yc in y_corners:
                for zc in z_corners:
                    poly = Polygon([xc, yc, zc])
                    result.append(poly)
        return result


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

    def get_first_pair(self):
        return self.nanobots[:2]

    def find_points_of_interest_slow(self, first: Nanobot, second: Nanobot):
        """
        for now:
            slow
        """
        print('comparing: {}'.format([first, second]))

        min_x = math.inf
        min_y = math.inf
        min_z = math.inf
        max_x = -math.inf
        max_y = -math.inf
        max_z = -math.inf

        all_shared = set()
        for z in first.calc_range(second, 2):
            for y in first.calc_range(second, 1):
                for x in first.calc_range(second, 0):
                    point = x, y, z
                    if first.can_see(point) and second.can_see(point):
                        all_shared.add(point)

                        # also keep track of bounds
                        if x < min_x:
                            min_x = x
                        if y < min_y:
                            min_y = y
                        if z < min_z:
                            min_z = z

                        if x > max_x:
                            max_x = x
                        if y > max_y:
                            max_y = y
                        if z > max_z:
                            max_z = z

        # find/min max sets from all 6 dirs
        x_min_set = set()
        x_max_set = set()
        y_min_set = set()
        y_max_set = set()
        z_min_set = set()
        z_max_set = set()

        for point in all_shared:
            x, y, z = point
            if x == min_x:
                x_min_set.add(point)
            if x == max_x:
                x_max_set.add(point)
            if y == min_y:
                y_min_set.add(point)
            if y == max_y:
                y_max_set.add(point)
            if z == min_z:
                z_min_set.add(point)
            if z == max_z:
                z_max_set.add(point)

        # find corners
        result = set()

        result |= self.find_line_corners(x_min_set, 0)
        result |= self.find_line_corners(x_max_set, 0)
        result |= self.find_line_corners(y_min_set, 1)
        result |= self.find_line_corners(y_max_set, 1)
        result |= self.find_line_corners(z_min_set, 2)
        result |= self.find_line_corners(z_max_set, 2)

        # done
        # result = sorted(result)
        return result

    def find_line_corners(self, points, dimension):
        min_x = math.inf
        min_y = math.inf
        min_z = math.inf
        max_x = -math.inf
        max_y = -math.inf
        max_z = -math.inf

        # find min/max
        for point in points:
            x, y, z = point

            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if z < min_z:
                min_z = z

            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            if z > max_z:
                max_z = z

        # filter
        result = set()
        for point in points:
            x, y, z = point

            if dimension != 0 and (x == min_x or x == max_x):
                result.add(point)
            if dimension != 1 and (y == min_y or y == max_y):
                result.add(point)
            if dimension != 2 and (z == min_z or z == max_z):
                result.add(point)

        return result

    def find_points_of_interest_fast(self, first: Nanobot, second: Nanobot):
        """
        see: https://stackoverflow.com/questions/6195413/intersection-between-3d-flat-polygons

        algo:
            for each pair of faces
                find intersection of the two triangles
                case1: coplanar
                    cases: point, line, poly, none
                case2: not
                    cases: point, line, none
        """
        shared_corners = set()
        for corner in first.get_corners():
            if second.can_see(corner):
                shared_corners.add(corner)
        for corner in second.get_corners():
            if first.can_see(corner):
                shared_corners.add(corner)

        # get all faces
        faces_1 = first.get_faces()
        faces_2 = second.get_faces()

        for f1 in faces_1:
            for f2 in faces_2:
                print('comparing: {}'.format([f1, f2]))

                math_3d.are_coplanar_triangles(f1, f2)

                z = 0

        return shared_corners

    def test_poi_finders(self):
        slow = self.find_points_of_interest_slow(*self.get_first_pair())
        fast = self.find_points_of_interest_fast(*self.get_first_pair())
        return slow == fast


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
