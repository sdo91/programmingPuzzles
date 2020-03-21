#!/usr/bin/env python3


### IMPORTS ###

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger
from advent_of_code.util.intcode_computer import IntcodeComputer










class Robot(object):

    BLACK = 0
    WHITE = 1

    LEFT = 0
    RIGHT = 1

    def __init__(self, text, starting_panel_color):
        self.text = text

        self.panels = {
            (0, 0): starting_panel_color
        }

        self.x = 0
        self.y = 0
        self.direction = 0  # up

        self.min_x = 9e9
        self.min_y = 9e9
        self.max_x = -9e9
        self.max_y = -9e9

        self.ic = IntcodeComputer(aoc_util.ints(text))

    def do_next(self):
        current = (self.x, self.y)

        color = self.BLACK
        if current in self.panels:
            color = self.panels[current]

        self.ic.queue_input(color)

        self.ic.run()
        color = self.ic.get_latest_output()
        self.panels[current] = color

        self.ic.run()
        turn_dir = self.ic.get_latest_output()

        # turn
        if turn_dir == self.RIGHT:
            self.direction += 1
        else:
            self.direction -= 1
        self.direction %= 4
        assert self.direction > -1
        assert self.direction < 4

        # move
        dx = {
            0: 0,
            1: 1,
            2: 0,
            3: -1,
        }
        dy = {
            0: -1,
            1: 0,
            2: 1,
            3: 0,
        }

        self.x += dx[self.direction]
        self.y += dy[self.direction]

        self.min_x = min(self.min_x, self.x)
        self.min_y = min(self.min_y, self.y)
        self.max_x = max(self.max_x, self.x)
        self.max_y = max(self.max_y, self.y)

        # turn and move

        z=0


    def __str__(self):
        return 'Robot {}: {}'.format(
            self.id, self.text)

    def __repr__(self):
        return str(self)


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

        AocLogger.verbose = False

        aoc_util.assert_equal(
            2021,
            self.solve_part_1(puzzle_input)
        )

        self.solve_part_2(puzzle_input)

    def run_robot(self, puzzle_input: str, starting_panel_color):
        """

        IRIHFKIH
        IR1HFKIH

        """
        puzzle_input = puzzle_input.strip()

        robot = Robot(puzzle_input, starting_panel_color)

        while not robot.ic.is_halted():
            robot.do_next()

        result = len(robot.panels)

        # robot.panels

        nr = robot.max_y
        nc = robot.max_x
        for r in range(nr+1):
            line = ''
            for c in range(nc+1):
                coord = (c, r)
                color = '  '
                if coord in robot.panels:
                    color = robot.panels[coord]
                    if color == Robot.WHITE:
                        color = '##'
                    else:
                        color = '  '
                line += color
            print(line)

        return result

    def solve_part_1(self, puzzle_input: str):
        p1_result = self.run_robot(puzzle_input, Robot.BLACK)
        print('p1_result: {}\n\n\n'.format(p1_result))
        return p1_result

    def solve_part_2(self, puzzle_input: str):
        print('p2_result: LBJHEKLH')
        self.run_robot(puzzle_input, Robot.WHITE)


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




