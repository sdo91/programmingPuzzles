#!/usr/bin/env python3



### IMPORTS ###

import numpy as np

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.grid_2d import Grid2D





### CONSTANTS ###

TEST_INPUT = [
    """         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       """, """

    """, """

    """
]




class DonutMaze(Grid2D):

    def __init__(self, text):
        # read into grid
        super().__init__(text)

        self.show()

        # find all portals

        for y in range(self.max_y):
            for x in range(self.max_x):
                if self.is_value((x, y), '.'):
                    # check if there is an adj letter
                    adj_portal = self.get_portal(x, y)
                    if adj_portal:
                        print('{}: {}'.format((x, y), adj_portal))

        z = 0

        # find AA and ZZ

    def get_portal(self, x, y):
        adj_coords = self.get_adjacent_coords((x, y))
        for c in adj_coords:
            if self.get(*c).isalpha():
                # 1st char found, get 2nd

                n = self.get_coord_north(c)
                if self.get(*n).isalpha():
                    return self.get(*n) + self.get(*c)

                w = self.get_coord_west(c)
                if self.get(*w).isalpha():
                    return self.get(*w) + self.get(*c)

                s = self.get_coord_south(c)
                if self.get(*s).isalpha():
                    return self.get(*c) + self.get(*s)

                e = self.get_coord_east(c)
                if self.get(*e).isalpha():
                    return self.get(*c) + self.get(*e)

        return ''





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
        23,
        solve_test_case(TEST_INPUT[0])
    )


def solve_test_case(test_input):
    AocLogger.log('test input:\n{}'.format(test_input))

    dm = DonutMaze(test_input)

    result = 0

    print('result: {}'.format(result))
    return result


def solve_full_input(puzzle_input):
    return 0





if __name__ == '__main__':
    main()




