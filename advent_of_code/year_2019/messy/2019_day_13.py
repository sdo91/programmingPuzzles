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

import time

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger
from advent_of_code.util.intcode_computer import IntcodeComputer










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










class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))
        start_time = time.time()

        try:
            puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            puzzle_input = 'unable to get input'
        aoc_util.write_input(puzzle_input, __file__)

        AocLogger.verbose = False
        # AocLogger.verbose = True

        aoc_util.assert_equal(
            318,
            self.solve(puzzle_input)
        )

        aoc_util.assert_equal(
            16309,
            self.solve(puzzle_input, is_p2=True)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def solve(self, puzzle_input: str, is_p2=False):
        """
        todo: use Grid2D
        """
        puzzle_input = puzzle_input.strip()

        mem = aoc_util.ints(puzzle_input)
        if is_p2:
            mem[0] = 2
        ic = IntcodeComputer(mem)

        num_blocks = 0

        d = Display()

        ball_pos = (19, 14)
        paddle_pos = (0, 0)

        while not ic.is_halted():

            for _ in range(3):
                ic.run()

                while ic.state == ic.STATE_INPUT_NEEDED:
                    if AocLogger.verbose:
                        d.show()

                    if paddle_pos[0] > ball_pos[0]:
                        direction = -1
                    elif paddle_pos[0] < ball_pos[0]:
                        direction = 1
                    else:
                        direction = 0

                    ic.queue_input(direction)
                    ic.run()

            x, y, tile = ic.get_all_output()[-3:]

            if x != -1 or y != 0:
                if tile == Display.BLOCK:
                    num_blocks += 1
                elif tile == Display.BALL:
                    ball_pos = (x, y)
                elif tile == Display.PADDLE:
                    paddle_pos = (x, y)

            d.add(x, y, tile)

        if not is_p2:
            result = num_blocks
            print('p1 result: {}'.format(result))
        else:
            result = ic.get_latest_output()
            print('p2 result: {}'.format(result))
        return result










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




