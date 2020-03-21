#!/usr/bin/env python3



### IMPORTS ###

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger
from advent_of_code.util.intcode_computer import IntcodeComputer
from advent_of_code.util.grid_2d import Grid2D





### CONSTANTS ###

TEST_INPUT = [
    """
#.......................................
.#......................................
..##....................................
...###..................................
....###.................................
.....####...............................
......#####.............................
......######............................
.......#######..........................
........########........................
.........#########......................
..........#########.....................
...........##########...................
...........############.................
............############................
.............#############..............
..............##############............
...............###############..........
................###############.........
................#################.......
.................########OOOOOOOOOO.....
..................#######OOOOOOOOOO#....
...................######OOOOOOOOOO###..
....................#####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
......................###OOOOOOOOOO#####
.......................##OOOOOOOOOO#####
........................#OOOOOOOOOO#####
.........................OOOOOOOOOO#####
..........................##############
..........................##############
...........................#############
............................############
.............................###########
    """, """

    """, """

    """
]






class TestSolver(object):

    def __init__(self, test_input, side_length):
        test_input = test_input.strip()
        self.grid = Grid2D(test_input)
        self.grid.show()

        self.side_length = side_length

        self.slope_y = 34

        self.lo_x = 10  # cant go up 10 right 10
        self.hi_x = 27  # can
        self.result_coord = None

    def is_in_beam(self, x, y):
        return self.grid.get(x, y) != '.'

    def solve_2(self):
        # estimate slope
        y = self.slope_y
        x = 0
        while True:
            x += 1
            if self.is_in_beam(x, y):
                break
        slope = y/x
        print('given y={}, x={}, slope={}'.format(y, x, slope))

        # binary search
        while True:
            if self.hi_x == self.lo_x + 1:
                # hi_x is answer
                break

            lower_left_x = (self.lo_x + self.hi_x) // 2
            print('trying x={}'.format(lower_left_x))

            # given x estimate y
            lower_left_y = int(slope * lower_left_x) + 5
            z=0

            # find min y
            # while grid.get(lower_left_x, lower_left_y) == '.':
            while not self.is_in_beam(lower_left_x, lower_left_y):
                lower_left_y -= 1
            z=0

            assert self.is_in_beam(lower_left_x, lower_left_y)
            assert2 = self.is_in_beam(lower_left_x, lower_left_y + 1)
            if assert2:
                assert not assert2

            # check coord
            ur_coord = (
                lower_left_x + (self.side_length - 1),
                lower_left_y - (self.side_length - 1)
            )
            z=0


            if self.is_in_beam(*ur_coord):
                # a box fits between the 2 points
                self.hi_x = lower_left_x
                self.result_coord = (lower_left_x, lower_left_y - (self.side_length - 1))
            else:
                self.lo_x = lower_left_x

        result_math = (self.result_coord[0] * 10000) + self.result_coord[1]
        print('result: {}'.format([self.result_coord, result_math]))
        return result_math

class Solver(TestSolver):

    def __init__(self, puzzle_input, side_length):
        self.side_length = side_length

        self.ic = IntcodeComputer(puzzle_input)
        self.ic.verbose = False

        self.grid = Grid2D()

        self.slope_y = 1000

        # todo: these don't work...
        # self.lo_x = 10  # cant go up 10 right 10
        # self.hi_x = 9999  # can
        # but these do...
        self.lo_x = 1300  # cant go up 10 right 10
        self.hi_x = 1350  # can

        self.result_coord = None

    def is_in_beam(self, x, y):
        self.ic.reset()
        self.ic.queue_input(x)
        self.ic.queue_input(y)
        self.ic.run()
        value = self.ic.get_latest_output()
        if value == 1:
            self.grid.set(x, y, '#')
            return True
        else:
            self.grid.set(x, y, '.')
            return False

    def solve_1(self):
        count = 0
        for x in range(50):
            print(x)
            for y in range(50):

                if self.is_in_beam(x, y):
                    count += 1

        print(count)
        self.grid.show()
        return count






def main():
    print('starting {}'.format(__file__.split('/')[-1]))

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    AocLogger.verbose = True
    run_tests()

    AocLogger.verbose = False
    solve_full_input(puzzle_input)


def run_tests():
    aoc_util.assert_equal(
        250020,
        solve_test_case(TEST_INPUT[0])
    )


def solve_test_case(test_input):
    solver = TestSolver(test_input, 10)
    return solver.solve_2()


def solve_full_input(puzzle_input):
    """
    13121052 too high
    """
    solver = Solver(puzzle_input, 100)

    aoc_util.assert_equal(
        164,
        solver.solve_1()
    )

    aoc_util.assert_equal(
        13081049,
        solver.solve_2()
    )





if __name__ == '__main__':
    main()




