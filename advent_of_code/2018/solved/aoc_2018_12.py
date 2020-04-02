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

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger


### CONSTANTS ###
TEST_INPUT = [
    """
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    325,
    0,
    0,
]

TEST_OUTPUT_2 = [
    0,
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
            3230,
            self.solve_part_1(puzzle_input)
        )

        aoc_util.assert_equal(
            4400000000304,
            self.solve_part_2(puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
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










class Generation(object):

    PRINT_LEFT = -5

    min = 0
    max = 0

    def __init__(self, gen=0):
        self.gen = gen
        self.pots = {}

    def __repr__(self):
        return '{:3}: {} (sum={})'.format(
            self.gen,
            self.to_string(self.PRINT_LEFT, self.max + 3),
            self.sum()
        )

    def to_string(self, left, right):
        rng = range(left, right + 1)
        return ''.join([self.get_pot(x) for x in rng])

    def set(self, i):
        self.pots[i] = '#'
        self.min = min(self.min, i)
        self.max = max(self.max, i)

    def get_pot(self, i):
        try:
            return self.pots[i]
        except KeyError:
            return '.'

    def get_combo(self, i):
        left = i - 2
        right = i + 2
        return self.to_string(left, right)

    def sum(self):
        return sum(self.pots.keys())

    def populate(self, prev_gen, plant_combos):
        """
        Args:
            prev_gen (Generation):
            plant_combos (set):
        """
        for pot in range(prev_gen.min - 2, prev_gen.max + 3):
            combo = prev_gen.get_combo(pot)
            if combo in plant_combos:
                self.set(pot)









class Solver(object):

    def __init__(self, text: str):
        self.text = text.strip()
        lines = aoc_util.lines(self.text)

        # parse initial state
        initial_state = lines[0].split()[-1]
        self.initial_gen = Generation()
        for i, char in enumerate(initial_state):
            if char == '#':
                self.initial_gen.set(i)
        print(self.initial_gen)

        # parse rules
        self.plant_combos = set()
        for line in lines:
            if '=> #' not in line:
                # skip
                continue
            tokens = aoc_util.split_and_strip_each(line, '=>')
            self.plant_combos.add(tokens[0])
        assert '.....' not in self.plant_combos

        AocLogger.log(str(self))

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        """
                         1         2         3
               0         0         0         0
         0: ...#..#.#..##......###...###...........
         1: ...#...#....#.....#..#..#..#...........
         2: ...##..##...##....#..#..#..##..........
         3: ..#.#...#..#.#....#..#..#...#..........
         4: ...#.#..#...#.#...#..#..##..##.........
         5: ....#...##...#.#..#..#...#...#.........
         6: ....##.#.#....#...#..##..##..##........
         7: ...#..###.#...##..#...#...#...#........
         8: ...#....##.#.#.#..##..##..##..##.......
         9: ...##..#..#####....#...#...#...#.......
        10: ..#.#..#...#.##....##..##..##..##......
        11: ...#...##...#.#...#.#...#...#...#......
        12: ...##.#.#....#.#...#.#..##..##..##.....
        13: ..#..###.#....#.#...#....#...#...#.....
        14: ..#....##.#....#.#..##...##..##..##....
        15: ..##..#..#.#....#....#..#.#...#...#....
        16: .#.#..#...#.#...##...#...#.#..##..##...
        17: ..#...##...#.#.#.#...##...#....#...#...
        18: ..##.#.#....#####.#.#.#...##...##..##..
        19: .#..###.#..#.#.#######.#.#.#..#.#...#..
        20: .#....##....#####...#######....#.#..##.
        """
        current_gen = self.initial_gen

        # loop
        for gen in range(1, 21):
            prev_gen = current_gen
            current_gen = Generation(gen)
            current_gen.populate(prev_gen, self.plant_combos)

            print(current_gen)

        return current_gen.sum()

    def p2(self):
        """
        after 200: 17904
        """
        current_gen = self.initial_gen
        num_repeats = 0
        diff = 0
        gen = 0

        # loop
        for gen in range(1, 201):
            prev_gen = current_gen
            prev_diff = diff

            current_gen = Generation(gen)
            current_gen.populate(prev_gen, self.plant_combos)

            # calc diff
            diff = current_gen.sum() - prev_gen.sum()
            print('diff={:5}, current_gen={}'.format(diff, current_gen))

            if diff == prev_diff:
                num_repeats += 1
                if num_repeats >= 5:
                    break
            else:
                num_repeats = 0

        num_gens_left = int(50e9) - gen
        result = current_gen.sum() + (num_gens_left * diff)
        return result










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




