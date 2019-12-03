#!/usr/bin/env python3



### IMPORTS ###

import aocd
import re
import parse
import typing
import aoc_util
from aoc_util import AocLogger



### CONSTANTS ###
TEST_INPUT = [
    """
R8,U5,L5,D3
U7,R6,D4,L4
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    6,
    0,
    0,
]

TEST_OUTPUT_2 = [
    30,
    0,
    0,
]





class MyObject(object):

    def __init__(self, text):
        self.text = text
        self.id = 0

    def __str__(self):
        return 'MyObject {}: {}'.format(
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

        AocLogger.verbose = True
        self.run_tests()

        AocLogger.verbose = False

        self.solve_part_1(puzzle_input)

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_1(puzzle_input)
        # )

        self.solve_part_2(puzzle_input)

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_2(puzzle_input)
        # )

    def run_tests(self):
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def solve_part_1(self, puzzle_input):
        """
        Args:
            puzzle_input (string): the input

        Returns: the answer

        rank 842
        """
        lines = puzzle_input.strip().split('\n')
        # for line in lines:

        current_x = 0
        current_y = 0

        first_wire_spots = set()

        first_line = lines[0]
        tokens = first_line.strip().split(',')
        for token in tokens:
            dir = token[0].lower()
            num_steps = aoc_util.ints(token)[0]

            for i in range(num_steps):
                if dir == 'r':
                    current_x += 1
                if dir == 'l':
                    current_x -= 1
                if dir == 'u':
                    current_y += 1
                if dir == 'd':
                    current_y -= 1

                coord = (current_x, current_y)
                first_wire_spots.add(coord)
                print('first wire: {}'.format(coord))

        # done with first wire

        current_x = 0
        current_y = 0

        min_dist = 99999

        second_line = lines[1]
        tokens = second_line.strip().split(',')
        for token in tokens:
            dir = token[0].lower()
            num_steps = aoc_util.ints(token)[0]

            for i in range(num_steps):
                if dir == 'r':
                    current_x += 1
                if dir == 'l':
                    current_x -= 1
                if dir == 'u':
                    current_y += 1
                if dir == 'd':
                    current_y -= 1

                coord = (current_x, current_y)
                # print('2nd wire: {}'.format(coord))

                if coord in first_wire_spots:
                    print('match: {}'.format(coord))
                    md = aoc_util.manhatten_dist((0,0), coord)
                    print('dist: {}'.format(md))

                    min_dist = min(min_dist, md)


        print('\npart 1 result: {}'.format(min_dist))
        return min_dist

    def solve_part_2(self, puzzle_input):
        """
        Args:
            puzzle_input (string): the input

        Returns: the answer

        rank 716
        """
        lines = puzzle_input.strip().split('\n')
        # for line in lines:

        current_x = 0
        current_y = 0
        total_steps = 0

        first_wire_spots = {}

        first_line = lines[0]
        tokens = first_line.strip().split(',')
        for token in tokens:
            dir = token[0].lower()
            num_steps = aoc_util.ints(token)[0]

            for i in range(num_steps):
                if dir == 'r':
                    current_x += 1
                if dir == 'l':
                    current_x -= 1
                if dir == 'u':
                    current_y += 1
                if dir == 'd':
                    current_y -= 1

                coord = (current_x, current_y)
                total_steps += 1
                first_wire_spots[coord] = total_steps
                print('first wire: {}'.format([coord, total_steps]))

        # done with first wire

        current_x = 0
        current_y = 0
        total_steps = 0

        min_combined_dist = 99999

        second_line = lines[1]
        tokens = second_line.strip().split(',')
        for token in tokens:
            dir = token[0].lower()
            num_steps = aoc_util.ints(token)[0]

            for i in range(num_steps):
                if dir == 'r':
                    current_x += 1
                if dir == 'l':
                    current_x -= 1
                if dir == 'u':
                    current_y += 1
                if dir == 'd':
                    current_y -= 1

                coord = (current_x, current_y)
                total_steps += 1

                # print('2nd wire: {}'.format(coord))

                if coord in first_wire_spots:
                    print('match: {}'.format([coord, total_steps]))
                    dist = total_steps + first_wire_spots[coord]
                    print('dist: {}'.format(dist))

                    min_combined_dist = min(min_combined_dist, dist)
                    pass


        print('\npart 1 result: {}'.format(min_combined_dist))
        return min_combined_dist





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




