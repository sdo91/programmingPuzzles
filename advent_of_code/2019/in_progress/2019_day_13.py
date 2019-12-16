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

addToPath('../..')

### IMPORTS ###

import numpy as np
import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.intcode_computer import IntcodeComputer


### CONSTANTS ###
TEST_INPUT_1 = [
    """

    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    0,
    0,
    0,
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





class Display(object):

    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

    tiles = {
        EMPTY: ' ',
        WALL: '|',
        BLOCK: 'X',
        PADDLE: '=',
        BALL: 'o',
    }

    def __init__(self):
        # self.text = text
        # self.id = 0

        self.score = 0
        self.grid = []

    def add(self, x, y, tile):
        if x == -1 and y == 0:
            self.score = tile
        else:
            # add until we have enough rows
            while len(self.grid) <= y:
                self.grid.append([])

            # add until we have enough cols
            cols = self.grid[y]
            while len(cols) <= x:
                cols.append(' ')

            self.grid[y][x] = self.tiles[tile]

    def show(self):
        print('score: {}'.format(self.score))
        for row in self.grid:
            for col in row:
                print(col, end='')
            print()



    # def __str__(self):
    #     return 'MyObject {}: {}'.format(
    #         self.id, self.text)
    #
    # def __repr__(self):
    #     return str(self)





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

        self.solve_part_1(puzzle_input)

        # self.solve_part_2(puzzle_input)

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_1(puzzle_input)
        # )

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_2(puzzle_input)
        # )

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT_1, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT_2, TEST_OUTPUT_2)

    def solve_part_1(self, puzzle_input: str):
        puzzle_input = puzzle_input.strip()

        mem = aoc_util.ints(puzzle_input)
        mem[0] = 2
        ic = IntcodeComputer(mem)



        EMPTY = 0
        WALL = 1
        BLOCK = 2
        PADDLE = 3
        BALL = 4

        num_blocks = 0
        score = 0

        d = Display()

        direction = -2

        directions_dict = {
            'a': -1,
            's': 0,
            'd': 1,
        }

        ball_pos = (19.14)
        prev_ball_pos = (19,14)
        paddle_pos = (0,0)

        while not ic.is_halted():

            out = -2
            # while ic.is_input_needed():
            #     d.show()
            #
            #     # direction = input('asd: ')
            #     direction = 0
            #
            #     ic.queue_input(direction)
            #
            #     # out = ic.run()
            #
            #     z=0
            #
            #     # assert False

            for _ in range(3):
                ic.run()

                while ic.state == ic.STATE_INPUT_NEEDED:
                    d.show()

                    # direction = input('asd: ')
                    direction = 0

                    z=0

                    if paddle_pos[0] > ball_pos[0]:
                        direction = -1
                    elif paddle_pos[0] < ball_pos[0]:
                        direction = 1
                    else:
                        direction = 0

                    ic.queue_input(direction)
                    ic.run()  # re run

            x, y, tile = ic.get_all_output()[-3:]

            if direction != -2:
                # d.show()
                z=0

            if x != -1 or y != 0:
                if tile == BLOCK:
                    num_blocks += 1
                elif tile == BALL:
                    prev_ball_pos = ball_pos
                    ball_pos = (x, y)
                elif tile == PADDLE:
                    paddle_pos = (x, y)



            d.add(x, y, tile)






        print('part 1 result: {}'.format(num_blocks))
        return num_blocks

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




