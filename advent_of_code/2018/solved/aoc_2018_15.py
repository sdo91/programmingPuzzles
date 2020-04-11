#!/usr/bin/env python3

def addToPath(relPath):
    from os import path
    import sys
    dirOfThisFile = path.dirname(path.realpath(__file__))
    dirToAdd = path.normpath(path.join(dirOfThisFile, relPath))
    if dirToAdd not in sys.path:
        print('adding to path: {}'.format(dirToAdd))
        sys.path.insert(0, dirToAdd)
    else:
        print('already in path: {}'.format(dirToAdd))

addToPath('../../..')

### IMPORTS ###

import time
import traceback
import math
from collections import defaultdict

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger
from advent_of_code.util.dijkstra_grid import DijkstraGrid


### CONSTANTS ###
TEST_INPUT = [
    """
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
    """, """

    """, """
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########
    """
]

TEST_OUTPUT_1 = [
    27730,
    0,
    0,
]

TEST_OUTPUT_2 = [
    4988,
    0,
    0,
]










class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))
        start_time = time.time()

        try:
            puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            print(traceback.format_exc())
            puzzle_input = 'unable to get input'
        aoc_util.write_input(puzzle_input, __file__)

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            181522,
            self.solve_part_1(puzzle_input)
        )

        aoc_util.assert_equal(
            68324,
            self.solve_part_2(puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True

        aoc_util.assert_equal(
            TEST_OUTPUT_1[0],
            self.solve_part_1(TEST_INPUT[0])
        )

        aoc_util.assert_equal(
            TEST_OUTPUT_2[0],
            self.solve_part_2(TEST_INPUT[0])
        )

        # aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def solve_part_1(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_1_result = solver.p1()

        print('part_1_result: {}\n'.format(part_1_result))
        return part_1_result

    def solve_part_2(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_2_result = solver.p2()

        print('part_2_result: {}\n'.format(part_2_result))
        return part_2_result










class Unit(object):

    BASE_ATTACK_POWER = 3
    elf_attack_power = BASE_ATTACK_POWER

    def __init__(self, coord, grid: DijkstraGrid):
        self.coord = coord
        self.grid = grid
        self.char = self.grid.overlay[self.coord]
        self.target_char = self._get_target_char()
        self.attack_power = self.BASE_ATTACK_POWER
        if self.char == 'E':
            self.attack_power = self.elf_attack_power
        self.hp = 200

    def __repr__(self):
        return '{} @ {}: hp={}'.format(
            self.char, self.coord, self.hp)

    def __lt__(self, other):
        return aoc_util.is_reading_order(self.coord, other.coord)

    def _get_target_char(self):
        if self.char == 'G':
            return 'E'
        else:
            return 'G'

    def find_best_path(self):
        path = self.grid.find_shortest_path(self.coord, {'.'}, {self.target_char})
        return path

    def get_target(self, units_dict):
        best_target = None  # type: Unit
        best_hp = math.inf

        for adj_coord in self.grid.get_adjacent_coords(self.coord):
            if self.grid.get_top(adj_coord) == self.target_char:
                potential_target = units_dict[adj_coord]
                if potential_target.hp < best_hp:
                    best_hp = potential_target.hp
                    best_target = potential_target
        return best_target

    def is_dead(self):
        return self.hp <= 0










class Solver(object):

    UNIT_CHARS = {'G', 'E'}

    def __init__(self, text: str):
        self.text = text.strip()

        self.cached_results = {}

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def run(self, elf_power):
        """
        Args:
            elf_power (int): attack power of elves

        Returns:
            tuple[int]: (outcome, num_dead_elves)
        """

        # check if result is cached
        if elf_power in self.cached_results:
            return self.cached_results[elf_power]

        # load the map
        grid = DijkstraGrid(self.text, default='.', overlay_chars=self.UNIT_CHARS)
        grid.show()
        print('START!\n\n\n')

        # create units
        Unit.elf_attack_power = elf_power
        unit_coords = grid.overlay.keys()
        units_list = []
        units_dict = {}
        numbers = defaultdict(int)
        for coord in unit_coords:
            unit = Unit(coord, grid)
            units_list.append(unit)
            units_dict[coord] = unit
            numbers[unit.char] += 1
        num_start_elves = numbers['E']

        # run the rounds
        completed_rounds = 0
        while True:
            units_list.sort()

            dead_units = []
            for unit in units_list:
                if unit.is_dead():
                    print('skipping: {}'.format(unit))
                    continue

                # check if there are targets
                if numbers[unit.target_char] < 1:
                    remaining_hp = 0
                    for unit in units_list:
                        if not unit.is_dead():
                            remaining_hp += unit.hp
                    outcome = completed_rounds * remaining_hp
                    print('Outcome: {} * {} = {}'.format(completed_rounds, remaining_hp, outcome))
                    num_dead_elves = num_start_elves - numbers['E']
                    print('num_dead_elves: {}'.format(num_dead_elves))
                    result = (outcome, num_dead_elves)
                    self.cached_results[elf_power] = result
                    return result

                # move the unit (if possible)
                best_path = unit.find_best_path()
                if len(best_path) > 1:
                    # do the move
                    old = unit.coord
                    del grid.overlay[old]
                    del units_dict[old]

                    new = best_path[0]
                    unit.coord = new
                    grid.overlay[new] = unit.char
                    units_dict[new] = unit

                # attack (if possible)
                target = unit.get_target(units_dict)
                if target:
                    target.hp -= unit.attack_power

                    if target.hp < 1:
                        print('dead: {}'.format(target))
                        del grid.overlay[target.coord]
                        del units_dict[target.coord]
                        dead_units.append(target)
                        numbers[target.char] -= 1

            # done with units loop
            for unit in dead_units:
                units_list.remove(unit)

            completed_rounds += 1
            if AocLogger.verbose:
                print('\n'*2)
                print('After {} rounds:'.format(completed_rounds))
                grid.show()
                units_list.sort()
                for unit in units_list:
                    print(unit)
                print('\n'*2)
        # end while

    def p1(self):
        result = self.run(elf_power=3)
        return result[0]

    def p2(self):
        """
        algo:
            do binary search

            start min=3, max=4
            check 4, 8, 16 etc
        """

        def is_enough(elf_power):
            return self.run(elf_power)[-1] == 0

        min_elf_power = aoc_util.binary_search((3, 4), is_enough).min_true
        print('min_elf_power: {}'.format(min_elf_power))
        result = self.run(min_elf_power)
        print('cached_results: {}'.format(self.cached_results))
        return result[0]










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




