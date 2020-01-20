#!/usr/bin/env python3



### IMPORTS ###

import importlib

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.grid_2d import Grid2D

# day15 = importlib.import_module('2019.solved.2019_day_15')
from aoc_util.aoc_2019_day_15 import RecursivePathfinderDroid





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





class DonutDroid(RecursivePathfinderDroid):
    """
    given:
        the donut map
        the dict of portals
        a starting portal

    find:
        reachable portals
        their distances

    """

    def __init__(self, maze):
        super().__init__()

        self.maze = maze

    def find_reachable(self, start_portal):
        """
        given:
            AA


        """
        start_coord = self.maze.portals_dict[start_portal]

        self.x, self.y = start_coord
        self.desired_x, self.desired_y = start_coord

        pass

    def move(self, direction):
        if self.maze.get(self.desired_x, self.desired_y) != '.':
            return self.STATUS_HIT_WALL

        # do the move
        self.x = self.desired_x
        self.y = self.desired_y
        self.maze.overlay = {
            (self.x, self.y): 'D'
        }
        self.maze.show()

        if self.maze.get(self.x, self.y) == 'G':
            return self.STATUS_HIT_GOAL
        else:
            return self.STATUS_MOVED


class DonutMaze(Grid2D):
    """
    algo:
        find all portals

        for each portal:
            find all reachable portals and their distances

        ex: start at AA:
            find BC_in, ZZ, FG_in
    """

    def __init__(self, text):
        # read into grid
        super().__init__(text)

        self.show()

        # find all portals
        self.portals_dict = {}
        for y in range(self.max_y):
            for x in range(self.max_x):
                if self.is_value((x, y), '.'):
                    # check if there is an adj letter
                    adj_portal = self.get_portal(x, y)
                    if adj_portal:
                        print('{}: {}'.format((x, y), adj_portal))
                        self.portals_dict[adj_portal] = (x, y)

        print('portals_dict: {}'.format(self.portals_dict))
        z = 0

        # find portals reachable from AA
        portal = 'AA'

        dd = DonutDroid(self)

        dd.find_reachable(portal)



    def calc_num_steps(self):
        return 0

    def is_outside(self, x, y):
        THRESHOLD = 5
        if x < THRESHOLD or x > self.max_x - THRESHOLD:
            return True
        if y < THRESHOLD or y > self.max_y - THRESHOLD:
            return True
        return False

    def get_portal(self, x, y):
        result = ''
        adj_coords = self.get_adjacent_coords((x, y))
        for c in adj_coords:
            if self.get(*c).isalpha():
                # 1st char found, get 2nd

                n = self.get_coord_north(c)
                if self.get(*n).isalpha():
                    result = self.get(*n) + self.get(*c)
                    break

                w = self.get_coord_west(c)
                if self.get(*w).isalpha():
                    result = self.get(*w) + self.get(*c)
                    break

                s = self.get_coord_south(c)
                if self.get(*s).isalpha():
                    result = self.get(*c) + self.get(*s)
                    break

                e = self.get_coord_east(c)
                if self.get(*e).isalpha():
                    result = self.get(*c) + self.get(*e)
                    break

        if result not in {'', 'AA', 'ZZ'}:
            if self.is_outside(x, y):
                result += '_outside'
            else:
                result += '_inside'
        return result





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
    result = dm.calc_num_steps()

    print('result: {}'.format(result))
    return result


def solve_full_input(puzzle_input):
    return solve_test_case(puzzle_input)





if __name__ == '__main__':
    main()




