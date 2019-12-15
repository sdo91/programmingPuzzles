#!/usr/bin/env python3



### IMPORTS ###

import aocd
from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.intcode_computer import IntcodeComputer

from collections import defaultdict
import math




### CONSTANTS ###

TEST_INPUT = [
    """      
##### 
##S##
#O.## 
#####  
    """, """

    """, """

    """
]

TEST_OUTPUT = [
    0,
    0,
    0,
]



class Grid2D(object):

    def __init__(self):
        self.grid = defaultdict(lambda: ' ')

        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

        self.overlay = {}

    def add(self, x, y, value):
        self.grid[(x, y)] = value

        self.min_x = min(self.min_x, x)
        self.max_x = max(self.max_x, x)
        self.min_y = min(self.min_y, y)
        self.max_y = max(self.max_y, y)

    def show(self):
        print()
        for y in range(self.max_y, self.min_y - 1, -1):
            line = ''
            for x in range(self.min_x, self.max_x + 1):
                coord = (x, y)
                if coord in self.overlay:
                    line += self.overlay[coord]
                else:
                    line += self.grid[coord]
            print(line)
        print()





class Droid(object):

    def __init__(self, puzzle_input):
        self.codes = aoc_util.ints(puzzle_input)
        self.ic = IntcodeComputer(self.codes)
        self.ic.verbose = False
        self.grid = Grid2D()

        self.directions_dict = {
            'w': 1,
            's': 2,
            'a': 3,
            'd': 4,
        }

        self.dx = {
            'w': 0,
            's': 0,
            'a': -1,
            'd': 1,
        }

        self.dy = {
            'w': 1,
            's': -1,
            'a': 0,
            'd': 0,
        }

        self.x = 0
        self.y = 0
        self.grid.add(0, 0, '.')

    def move(self, input_letter=''):
        while input_letter not in self.directions_dict:
            input_letter = input('direction? ')
        direction = self.directions_dict[input_letter]

        self.ic.queue_input(direction)

        desired_x = self.x + self.dx[input_letter]
        desired_y = self.y + self.dy[input_letter]

        self.ic.run()

        assert self.ic.state == IntcodeComputer.STATE_OUTPUT

        status = self.ic.get_latest_output()
        if status == 0:
            # wall, pos does not change
            self.grid.add(desired_x, desired_y, '#')
        elif status == 1:
            # empty, move
            self.grid.add(desired_x, desired_y, '.')
            self.x = desired_x
            self.y = desired_y
        else:
            self.grid.add(desired_x, desired_y, '2')
            print('found: {}'.format([desired_x, desired_y]))
            self.x = desired_x
            self.y = desired_y

        self.grid.overlay = {
            (self.x, self.y): 'D'
        }
        self.grid.show()
        z=0


    def get_path(self, direction, path_so_far):
        pass



    # def __str__(self):
    #     return 'Droid {}: {}'.format(
    #         self.id, self.text)
    #
    # def __repr__(self):
    #     return str(self)







def main():
    print('starting {}'.format(__file__.split('/')[-1]))

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    AocLogger.verbose = True
    # aoc_util.run_tests(solve_test_case, TEST_INPUT, TEST_OUTPUT)

    AocLogger.verbose = False

    solve_test_case(TEST_INPUT[0])
    solve_full_input(puzzle_input)






def solve_test_case(test_input):
    test_input = test_input.strip()
    AocLogger.log('test input:\n{}'.format(test_input))

    lines = test_input.split('\n')

    num_rows = len(lines)
    num_cols = len(lines[0])

    # find offset such that S + offset = (0,0)
    # offset = (0,0) - S
    for r, row in enumerate(lines):
        if 'S' in row:
            offset_y = -r
            offset_x = -row.find('S')






    z=0

def solve_full_input(puzzle_input):
    puzzle_input = puzzle_input.strip()


    droid = Droid(puzzle_input)



    # grid = Grid2D()
    #
    # grid.add(-3, -4, '5')
    # grid.add(6, 7, '8')
    #
    # grid.show()

    # z=0


    while True:


        droid.move()




    pass





if __name__ == '__main__':
    main()




