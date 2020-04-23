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
from advent_of_code.util.grid_2d import Grid2D


### CONSTANTS ###
TEST_INPUT = [
    """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    1147,
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

    def __init__(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        try:
            self.puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            print(traceback.format_exc())
            self.puzzle_input = 'unable to get input'
        aoc_util.write_input(self.puzzle_input, __file__)

    def run(self):
        start_time = time.time()

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            663502,
            self.solve_part_1(self.puzzle_input)
        )

        aoc_util.assert_equal(
            201341,
            self.solve_part_2(self.puzzle_input, 1000000000)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)

        # aoc_util.assert_equal(
        #     201341,
        #     self.solve_part_2(self.puzzle_input, 1000)
        # )

    def solve_part_1(self, text: str):
        solver = Solver(text)

        part_1_result = solver.p1()

        print('part_1_result: {}\n'.format(part_1_result))
        return part_1_result

    def solve_part_2(self, text: str, num_minutes: int):
        solver = Solver(text)

        part_2_result = solver.p2(num_minutes)

        print('part_2_result: {}\n'.format(part_2_result))
        return part_2_result










class Solver(object):

    OPEN = '.'
    TREES = '|'
    LUMBERYARD = '#'

    def __init__(self, text: str):
        self.text = text.strip()

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def process(self, current, prev):
        for coord in current.coords():
            prev_char = prev.get_tuple(coord)

            if prev_char == self.OPEN:
                """
                An open acre will become filled with trees if three or more adjacent acres contained trees. 
                Otherwise, nothing happens.
                """
                if prev.count_adjacent(coord, self.TREES, True) >= 3:
                    current.set_tuple(coord, self.TREES)
                else:
                    current.set_tuple(coord, prev_char)
            elif prev_char == self.TREES:
                """
                An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards.
                Otherwise, nothing happens.
                """
                if prev.count_adjacent(coord, self.LUMBERYARD, True) >= 3:
                    current.set_tuple(coord, self.LUMBERYARD)
                else:
                    current.set_tuple(coord, prev_char)
            elif prev_char == self.LUMBERYARD:
                """
                An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other
                lumberyard and at least one acre containing trees. Otherwise, it becomes open.
                """
                num_yards = prev.count_adjacent(coord, self.LUMBERYARD, True)
                num_trees = prev.count_adjacent(coord, self.TREES, True)
                if num_yards >= 1 and num_trees >= 1:
                    current.set_tuple(coord, self.LUMBERYARD)
                else:
                    current.set_tuple(coord, self.OPEN)
            else:
                assert False

    def p1(self, num_minutes=10):
        """
        The change to each acre is based entirely on the contents of that acre as well as the number of open, wooded,
        or lumberyard acres adjacent to it at the start of each minute. Here, "adjacent" means any of the eight acres
        surrounding that acre. (Acres on the edges of the lumber collection area might have fewer than eight adjacent
        acres; the missing acres aren't counted.)
        """

        current = Grid2D(self.text)
        prev = Grid2D(self.text)

        print('Initial state:')
        current.show()

        for m in range(1, num_minutes + 1):
            # populate current generation
            current, prev = prev, current
            self.process(current, prev)

            if AocLogger.verbose:
                print('After {} minutes:'.format(m))
                current.show()

        # finish up
        print('Final state:')
        current.show()

        num_trees = current.count(self.TREES)
        num_yards = current.count(self.LUMBERYARD)
        result = num_trees * num_yards
        print('{} * {} = {}'.format(num_trees, num_yards, result))
        return result

    def p2(self, num_minutes: int):
        """
        after 1000: 587 * 343 = 201341
        Args:
            num_minutes:

        Returns:

        """

        current = Grid2D(self.text)
        prev = Grid2D(self.text)

        assert hash(current) == hash(prev)

        current.show()
        print('(Initial state)')

        hash_list = []
        hash_set = set()

        final_hash = None

        i = 0
        while True:
            grid_hash = hash(current)

            if final_hash is None:
                # check for repeat
                if grid_hash in hash_set:
                    # we found the 1st repeat

                    first = hash_list.index(grid_hash)
                    second = i
                    cycle_len = second - first
                    minutes_left_mod = (num_minutes - second) % cycle_len
                    final_hash = hash_list[first + minutes_left_mod]

                    # print(first)
                    # print(second)
                    # print(cycle_len)
                    # print(final_hash)
                    # time.sleep(1)
                else:
                    # add the hash
                    hash_list.append(grid_hash)
                    hash_set.add(grid_hash)
            else:
                # check if done
                if grid_hash == final_hash:
                    break

            # populate current generation
            i += 1
            current, prev = prev, current
            self.process(current, prev)

            if AocLogger.verbose or i % 1 == 0:
                current.show()
                print('(After {} minutes)'.format(i))

        # finish up
        current.show()
        print('(Final state)')

        num_trees = current.count(self.TREES)
        num_yards = current.count(self.LUMBERYARD)
        result = num_trees * num_yards
        print('{} * {} = {}'.format(num_trees, num_yards, result))
        return result










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




