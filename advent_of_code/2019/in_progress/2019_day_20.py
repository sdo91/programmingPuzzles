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












class Portal(object):
    def __init__(self):
        self.id = ''
        self.coord = (0, 0)

    def __str__(self):
        return '{} @ {}'.format(self.id, self.coord)

    def __repr__(self):
        return str(self)










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

        self.reachable_by_start = {}
        self.current_start = None


    def find_reachable(self, start_portal):
        """
        find the shortest distance to all portals reachable from the start portal

        example:
            given:
                AA

            find:
                BC: 4
                ZZ: 26
                FG: 30
        """
        self.current_start = start_portal
        self.reachable_by_start[self.current_start] = {}

        start_coord = self.maze.portals_by_id[start_portal].coord

        self.x, self.y = start_coord
        self.desired_x, self.desired_y = start_coord

        path_so_far = [start_coord]
        self._try_all_directions(path_so_far)


    def move(self, direction):
        if self.maze.get(self.desired_x, self.desired_y) != '.':
            return self.STATUS_HIT_WALL

        # do the move
        self.x = self.desired_x
        self.y = self.desired_y
        self.maze.overlay = {
            (self.x, self.y): '@'
        }

        return self.STATUS_MOVED


    def process_new_path(self, new_path):
        if self.get_current() in self.maze.portals_by_coord:
            print('hit a portal: (path={})'.format(new_path))
            self.maze.show()

            portal = self.maze.portals_by_coord[self.get_current()]
            reachable_dict = self.reachable_by_start[self.current_start]
            if portal.id in reachable_dict:
                raise RuntimeError

            reachable_dict[portal.id] = len(new_path) - 1











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
        self.portals_by_id = {}
        self.portals_by_coord = {}
        for y in range(self.max_y):
            for x in range(self.max_x):
                if self.is_value((x, y), '.'):
                    # check if there is an adj letter
                    adj_portal = self.get_portal(x, y)
                    if adj_portal:
                        print('portal found: {}'.format(adj_portal))
                        self.portals_by_id[adj_portal.id] = adj_portal
                        self.portals_by_coord[adj_portal.coord] = adj_portal

        print('portals_by_id: {}'.format(self.portals_by_id))
        print('portals_by_coord: {}'.format(self.portals_by_coord))
        z = 0

        # find reachable portals
        dd = DonutDroid(self)
        for id in self.portals_by_id:
            dd.find_reachable(id)

        # todo: use dijkstra's algo to find shortest path
        z=0


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
        result_str = ''
        adj_coords = self.get_adjacent_coords((x, y))
        for c in adj_coords:
            if self.get(*c).isalpha():
                # 1st char found, get 2nd

                n = self.get_coord_north(c)
                if self.get(*n).isalpha():
                    result_str = self.get(*n) + self.get(*c)
                    break

                w = self.get_coord_west(c)
                if self.get(*w).isalpha():
                    result_str = self.get(*w) + self.get(*c)
                    break

                s = self.get_coord_south(c)
                if self.get(*s).isalpha():
                    result_str = self.get(*c) + self.get(*s)
                    break

                e = self.get_coord_east(c)
                if self.get(*e).isalpha():
                    result_str = self.get(*c) + self.get(*e)
                    break

        if result_str not in {'', 'AA', 'ZZ'}:
            if self.is_outside(x, y):
                result_str += '_outside'
            else:
                result_str += '_inside'

        if result_str:
            result_portal = Portal()
            result_portal.id = result_str
            result_portal.coord = (x, y)
            return result_portal
        else:
            return None














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




