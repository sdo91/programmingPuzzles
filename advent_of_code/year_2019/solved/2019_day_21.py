#!/usr/bin/env python3



### IMPORTS ###

import time

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.intcode_computer import IntcodeComputer
from advent_of_code.util.aoc_util import AocLogger





def main():
    print('starting {}'.format(__file__.split('/')[-1]))
    start_time = time.time()

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    AocLogger.verbose = False

    aoc_util.assert_equal(
        19362259,
        solve_part_1(puzzle_input)
    )

    aoc_util.assert_equal(
        1141066762,
        solve_part_2(puzzle_input)
    )

    elapsed_time = time.time() - start_time
    print('elapsed_time: {:.2f} sec'.format(elapsed_time))


def solve_part_1(puzzle_input):
    # D and not (A and B and C)
    instructions = '''
        # store (A and B and C) in T
        OR A T
        AND B T
        AND C T

        # store D and not (A and B and C) in J
        NOT T J
        AND D J
        WALK
    '''
    p1_result = get_hull_damage(puzzle_input, instructions)
    print('p1_result: {}'.format(p1_result))
    return p1_result


def solve_part_2(puzzle_input):
    instructions = '''
        # same as part 1
        OR A T
        AND B T
        AND C T
        NOT T J
        AND D J

        # store (E or H) in T
        NOT H T
        NOT T T
        OR E T

        # store (part 1) and (E or H) in J
        AND T J
        RUN
    '''
    p2_result = get_hull_damage(puzzle_input, instructions)
    print('p2_result: {}'.format(p2_result))
    return p2_result


def get_hull_damage(puzzle_input, instructions):
    print('\n\n\n')
    ic = IntcodeComputer(puzzle_input)

    for instruction in aoc_util.stripped_lines(instructions):
        instruction = instruction.split('#')[0].strip()
        if not instruction:
            continue

        ic.run_to_input_needed()
        ic.print_output_string()
        ic.queue_input_string(instruction)
        print('instruction: {}'.format(instruction))

    print()
    ic.run_to_halt()

    try:
        # if output is ascii, droid didn't make it
        ic.print_output_string()
        raise RuntimeError('failed')
    except ValueError:
        result = ic.get_latest_output()
        print('damage: {}'.format(result))

    return result





if __name__ == '__main__':
    main()




