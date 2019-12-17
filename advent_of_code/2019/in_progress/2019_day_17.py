#!/usr/bin/env python3



### IMPORTS ###

import numpy as np
import typing

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.intcode_computer import IntcodeComputer
from aoc_util.grid_2d import Grid2D





### CONSTANTS ###

TEST_INPUT = [
    """
..#..........
..#..........
##O####...###
#.#...#...#.#
##O###O###O##
..#...#...#..
..#####...^..
    """, """
#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......
    """, """

    """
]





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
        76,
        solve_test_case(TEST_INPUT[0])
    )

    aoc_util.assert_equal(
        'R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2',
        solve_test_case_2(TEST_INPUT[1])
    )


def is_intersection(grid: Grid2D, x, y):
    matches = {'#', 'O'}
    return grid.get(x, y) in matches \
        and grid.get(x + 1, y) in matches \
        and grid.get(x - 1, y) in matches \
        and grid.get(x, y + 1) in matches \
        and grid.get(x, y - 1) in matches


def solve_test_case(test_input):
    test_input = test_input.strip()
    AocLogger.log('test input:\n{}'.format(test_input))

    grid = Grid2D(test_input)

    grid.show()

    result = 0
    for y in range(grid.min_y+1, grid.max_y):
        for x in range(grid.min_x+1, grid.max_x):
            if is_intersection(grid, x, y):
                ap = x * y
                result += ap

    print('result: {}'.format(result))
    return result


def solve_test_case_2(test_input):
    test_input = test_input.strip()
    AocLogger.log('test input:\n{}'.format(test_input))

    grid = Grid2D(test_input)
    grid.show()

    start_coord = grid.find('^')[0]

    right_offset_dict = {
        0: (1, 0),
        1: (0, 1),
        2: (-1, 0),
        3: (0, -1),
    }
    left_offset_dict = {
        0: (-1, 0),
        1: (0, -1),
        2: (1, 0),
        3: (0, 1),
    }
    forward_offset_dict = {
        0: (0, -1),
        1: (1, 0),
        2: (0, 1),
        3: (-1, 0),
    }

    current_direction = 0  # up
    current_coord = start_coord
    # visited = {start_coord}
    path = []
    while True:
        # decide which way to turn
        coord_to_right = aoc_util.tuple_add(current_coord, right_offset_dict[current_direction])
        coord_to_left = aoc_util.tuple_add(current_coord, left_offset_dict[current_direction])

        if grid.is_value(coord_to_right, '#'):
            path.append('R')
            current_direction += 1
        elif grid.is_value(coord_to_left, '#'):
            path.append('L')
            current_direction -= 1
        else:
            break

        current_direction %= 4

        # go until not hash
        num_steps = 0
        while True:
            coord_forward = aoc_util.tuple_add(current_coord, forward_offset_dict[current_direction])
            if not grid.is_value(coord_forward, '#'):
                path.append(str(num_steps))
                break
            else:
                current_coord = coord_forward
                num_steps += 1

    result = ','.join(path)
    print('result: {}'.format(result))
    return result


def solve_full_input(puzzle_input):
    puzzle_input = puzzle_input.strip()
    AocLogger.log('puzzle_input input:\n{}'.format(puzzle_input))

    ic = IntcodeComputer(puzzle_input)
    ic.run_to_halt()

    output = ic.get_all_output()

    string = ''.join([chr(x) for x in output])
    print(string)

    result = solve_test_case(string)
    print('result 1: {}'.format(result))

    solve_test_case_2(string)
    """
    R,6,R,6,R,8,L,10,L,4,R,6,L,10,R,8,R,6,L,10,R,8,R,6,R,6,R,8,L,10,L,4,L,4,L,12,R,6,L,10,R,6,R,6,R,8,L,10,L,4,L,4,L,12,R,6,L,10,R,6,R,6,R,8,L,10,L,4,L,4,L,12,R,6,L,10,R,6,L,10,R,8

    R,6,R,6,R,8,L,10,L,4
    R,6,L,10,R,8
    L,4,L,12,R,6,L,10
    """
    A = 'R,6,R,6,R,8,L,10,L,4'
    B = 'R,6,L,10,R,8'
    C = 'L,4,L,12,R,6,L,10'





    return result





if __name__ == '__main__':
    main()




