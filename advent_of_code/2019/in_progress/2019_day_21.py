#!/usr/bin/env python3



### IMPORTS ###

import time

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.intcode_computer import IntcodeComputer





### CONSTANTS ###

TEST_INPUT = [
    """

    """, """

    """, """

    """
]




class SpringDroid(object):



    def __init__(self, puzzle_input):

        self.ic = IntcodeComputer(puzzle_input)
        # self.ic.verbose = False


    def get_hull_damage(self):
        """

        D and not (A and B and C)
        2nd arg must be writable (T or J)



        OR A T      # set T to A
        AND B T
        AND C T
        # T = (A and B and C)

        # T: (A and B and C)
        NOT T J
        # J: not (A and B and C)
        AND D J (D and J -> J)


        """



        # # D and not (A and B and C)
        # instructions = '''
        #     OR A T
        #     AND B T
        #     AND C T
        #     NOT T J
        #     AND D J
        #     WALK
        # '''

        instructions = '''
            OR A T
            AND B T
            AND C T
            NOT T J
            AND D J
            NOT H T
            NOT T T
            OR E T
            AND T J
            RUN
        '''


        # if 'WALK' not in instructions:
        #     instructions += 'WALK'

        instructions = aoc_util.stripped_lines(instructions)

        for instruction in instructions:
            self.ic.run_to_input_needed()
            self.ic.print_output_string()
            self.ic.queue_input_string(instruction)

        self.ic.run_to_halt()

        try:
            self.ic.print_output_string()
        except ValueError:
            result = self.ic.get_latest_output()

        z=0



        return -1




def main():
    print('starting {}'.format(__file__.split('/')[-1]))

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    AocLogger.verbose = True
    # run_tests()

    AocLogger.verbose = False


    aoc_util.assert_equal(
        0,
        solve_part_1(puzzle_input)
    )


# def run_tests():
#     aoc_util.assert_equal(
#         42,
#         solve_test_case(TEST_INPUT[0])
#     )
#
#
# def solve_test_case(test_input):
#     test_input = test_input.strip()
#     AocLogger.log('test input:\n{}'.format(test_input))
#
#     result = 0
#
#     print('result: {}'.format(result))
#     return result


def solve_part_1(puzzle_input):
    puzzle_input = puzzle_input.strip()

    sd = SpringDroid(puzzle_input)
    result = sd.get_hull_damage()

    print('result: {}'.format(result))
    return result





if __name__ == '__main__':
    main()




