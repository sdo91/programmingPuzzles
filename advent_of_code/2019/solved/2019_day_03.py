#!/usr/bin/env python3



### IMPORTS ###

import aocd
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

TEST_OUTPUT = [
    (6, 30),
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
        self.run_tests()

        AocLogger.verbose = False

        # aoc_util.assert_equal(
        #     768,
        #     self.solve_part_1(puzzle_input)
        # )

        aoc_util.assert_equal(
            (768, 8684),
            self.solve_test_case(puzzle_input)
        )

    def run_tests(self):
        aoc_util.run_tests(self.solve_test_case, TEST_INPUT, TEST_OUTPUT)


    def solve_test_case(self, puzzle_input):
        """
        Args:
            puzzle_input (string): the input

        Returns: the answer

        part 1: rank 842
        part 2: rank 716
        """

        first_wire_spots = {}
        is_first_line = True

        min_man_dist = 9e9
        min_combined_steps = 9e9

        lines = puzzle_input.strip().split('\n')
        for line in lines:

            current_x = 0
            current_y = 0
            total_steps = 0

            tokens = line.strip().split(',')
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

                    if is_first_line:
                        first_wire_spots[coord] = total_steps
                        # print('first wire: {}'.format([coord, total_steps]))
                    else:
                        if coord in first_wire_spots:
                            # match found
                            print('match: {}'.format([coord, total_steps]))

                            # part 1
                            man_dist = aoc_util.manhatten_dist((0,0), coord)
                            print('man_dist: {}'.format(man_dist))
                            min_man_dist = min(min_man_dist, man_dist)

                            # part 2
                            combo_dist = total_steps + first_wire_spots[coord]
                            print('combo_dist: {}'.format(combo_dist))
                            min_combined_steps = min(min_combined_steps, combo_dist)

                            pass

            if is_first_line:
                print('done with first line')
                is_first_line = False
        # end for loop

        result = min_man_dist, min_combined_steps
        print('\nresult: {}'.format(result))
        return result





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




