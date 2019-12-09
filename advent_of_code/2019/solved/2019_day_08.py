#!/usr/bin/env python3



### IMPORTS ###

import numpy as np

import aocd
from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger





class SpaceImage(object):

    def __init__(self, digits_str, width=25, height=6):
        self.digits_str = digits_str.strip()
        self.digits = [int(x) for x in digits_str]

        self.num_layers = len(self.digits) // (width * height)
        self.num_rows = height
        self.num_cols = width

        self.layers = np.reshape(
            self.digits,
            (self.num_layers, self.num_rows, self.num_cols)
        )
        AocLogger.log('\ntest layers:')
        AocLogger.log(self.layers)

    def solve_part_1(self):
        min_num_zeros = 9e9
        product = -1
        for layer in self.layers:
            counts = self.get_unique_digit_counts(layer)
            if counts[0] < min_num_zeros:
                min_num_zeros = counts[0]
                product = counts[1] * counts[2]

        print('\npart 1: {}'.format(product))
        return product

    def print_image(self):
        print()
        for r in range(self.num_rows):
            line = ''
            for c in range(self.num_cols):
                p = self.get_pixel(r, c)
                if p == 1:
                    line += '##'
                else:
                    line += '  '
            print(line)

    def get_pixel(self, row, col):
        for layer in self.layers:
            if layer[row][col] != 2:
                return layer[row][col]
        raise RuntimeError('pixel not found!')

    @staticmethod
    def get_unique_digit_counts(array):
        unique, counts = np.unique(array, return_counts=True)
        return dict(zip(unique, counts))



def main():
    print('starting {}'.format(__file__.split('/')[-1]))

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    AocLogger.verbose = True
    solve_test_case_part_1('123456789012', 3, 2)

    AocLogger.verbose = False

    aoc_util.assert_equal(
        1742,
        solve_part_1(puzzle_input)
    )

    solve_part_2(puzzle_input)


def solve_test_case_part_1(digits, width, height):
    image = SpaceImage(digits, width, height)
    z=0

def solve_part_1(puzzle_input):
    image = SpaceImage(puzzle_input)
    return image.solve_part_1()



def solve_part_2(puzzle_input):
    image = SpaceImage(puzzle_input)
    image.print_image()








if __name__ == '__main__':
    main()




