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

from collections import defaultdict
import llist

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger


### CONSTANTS ###
TEST_INPUT = [
    """
9 players; last marble is worth 25 points
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    32,
    0,
    0,
]

TEST_OUTPUT_2 = [
    22563,
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
            374690,
            self.solve_part_1(puzzle_input)
        )

        aoc_util.assert_equal(
            3009951158,
            self.solve_part_2(puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        AocLogger.verbose = False
        aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def solve_part_1(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_1_result = solver.p1()

        print('part_1_result: {}'.format(part_1_result))
        return part_1_result

    def solve_part_2(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_2_result = solver.p2()

        print('part_2_result: {}'.format(part_2_result))
        return part_2_result










class Solver(object):

    current = ...  # type: llist.dllistnode

    def __init__(self, text: str):
        self.text = text.strip()

        self.circle = llist.dllist()
        self.circle.append(0)
        self.current = self.circle.first

        AocLogger.log(str(self))

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        num_players, last_marble = aoc_util.ints(self.text)
        return self.play_game(num_players, last_marble)

    def p2(self):
        num_players, last_marble = aoc_util.ints(self.text)
        last_marble *= 100
        return self.play_game(num_players, last_marble)

    def play_game(self, num_players, last_marble):
        """
        Then, each Elf takes a turn placing the lowest-numbered remaining marble into the circle between the marbles
        that are 1 and 2 marbles clockwise of the current marble. (When the circle is large enough, this means that
        there is one marble between the marble that was just placed and the current marble.) The marble that was just
        placed then becomes the current marble.

        However, if the marble that is about to be placed has a number which is a multiple of 23, something entirely
        different happens. First, the current player keeps the marble they would have placed, adding it to their
        score. In addition, the marble 7 marbles counter-clockwise from the current marble is removed from the circle
        and also added to the current player's score. The marble located immediately clockwise of the marble that was
        removed becomes the new current marble.

        [1]  0  8  4  9  2(10) 5  1  6  3  7
        [7]  0 16  8 17  4 18 19  2 24 20(25)10 21  5 22 11  1 12  6 13  3 14  7 15
        """

        scores = defaultdict(int)
        winning_score = 0

        player_0_idx = 0
        for x in range(1, last_marble + 1):
            player_1_idx = player_0_idx + 1

            if x % 23 == 0:
                # move current
                self.move_ccw(6)
                to_remove = self.ccw()

                # add to score
                scores[player_1_idx] += x
                scores[player_1_idx] += self.circle.remove(to_remove)
                winning_score = max(winning_score, scores[player_1_idx])
            else:
                self.move_cw(2)
                self.current = self.circle.insert(x, self.current)

                if self.current == self.circle.first:
                    # keep 0 at beginning
                    self.circle.rotate(-1)

            if AocLogger.verbose:
                AocLogger.log('[{}]: {}, {}'.format(player_1_idx, self.current.value, self.circle))

            player_0_idx += 1
            player_0_idx %= num_players

        return winning_score

    def move_cw(self, i):
        for x in range(i):
            self.current = self.current.next
            if self.current is None:
                self.current = self.circle.first

    def move_ccw(self, i):
        for x in range(i):
            self.current = self.ccw()

    def ccw(self):
        result = self.current.prev
        if result is None:
            result = self.circle.last
        return result










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




