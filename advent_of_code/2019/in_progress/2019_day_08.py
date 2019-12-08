#!/usr/bin/env python3



### IMPORTS ###

import aocd
import re
import parse
import typing
from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger




### CONSTANTS ###

TEST_INPUT = [
    """
123456789012
    """, """

    """, """

    """
]

TEST_OUTPUT = [
    0,
    0,
    0,
]









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

    solve_full_input(puzzle_input)




def get_pixel(list_3d, row, col):
    for l in range(len(list_3d)):
        if list_3d[l][row][col] != 2:
            return list_3d[l][row][col]
    assert False

def solve_test_case(test_input):
    AocLogger.log('test input: {}'.format(test_input))
    test_input = test_input.strip()

    digits = [int(x) for x in test_input]

    width = 25
    height = 6

    # width = 3
    # height = 2
    num_layers = len(digits) // (width * height)

    pixels = []

    layer_digits = []

    i = 0
    for l in range(num_layers):
        layer = []
        layer_dict = {}
        for r in range(height):
            row = []
            for c in range(width):
                row.append(digits[i])
                if digits[i] not in layer_dict:
                    layer_dict[digits[i]] = 0
                layer_dict[digits[i]] += 1
                i += 1
            layer.append(row)
        pixels.append(layer)
        layer_digits.append(layer_dict)


    min_layer = -1
    min_zeros = 9e9
    for i, layer in enumerate(layer_digits):
        if layer[0] < min_zeros:
            min_zeros = layer[0]
            min_layer = i

    print(layer_digits[min_layer][1] * layer_digits[min_layer][2])


    for r in range(height):
        line = ''
        for c in range(width):
            p = get_pixel(pixels, r, c)
            if p == 1:
                line += '##'
            else:
                line += '  '
        print(line)


    z= 0


    pass

def solve_full_input(puzzle_input):


    solve_test_case(puzzle_input)




    pass





if __name__ == '__main__':
    main()




