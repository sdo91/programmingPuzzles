#!/usr/bin/env python3



### IMPORTS ###

import aocd
import parse

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger



### CONSTANTS ###
TEST_INPUT = [
    """
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    4,
    0,
    0,
]

TEST_OUTPUT_2 = [
    3,
    0,
    0,
]


















class Claim(object):

    def __init__(self, text):
        self.text = text
        AocLogger.log(self.text)

        parse_result = parse.parse('#{} @ {},{}: {}x{}', text)

        self.id = int(parse_result[0])
        self.from_left = int(parse_result[1])
        self.from_top = int(parse_result[2])
        self.width = int(parse_result[3])
        self.height = int(parse_result[4])

        self.x_end = self.from_left + self.width
        self.y_end = self.from_top + self.height

        self.has_conflict = False
















class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        puzzle_input = aocd.data
        aoc_util.write_input(puzzle_input, __file__)

        AocLogger.verbose = True
        self.test_cases()

        AocLogger.verbose = False
        aoc_util.assert_equal(116489, self.solve_part_1(puzzle_input))
        aoc_util.assert_equal(1260, self.solve_part_2(puzzle_input))

    def test_cases(self):
        self.verbose = True
        AocLogger.log()
        AocLogger.log('running test cases')

        for test_in, test_out in zip(TEST_INPUT, TEST_OUTPUT_1):
            test_in = test_in.strip()
            if not test_in:
                continue

            # do the test
            aoc_util.assert_equal(
                test_out,
                self.solve_part_1(test_in)
            )

        for test_in, test_out in zip(TEST_INPUT, TEST_OUTPUT_2):
            test_in = test_in.strip()
            if not test_in:
                continue

            # do the test
            aoc_util.assert_equal(
                test_out,
                self.solve_part_2(test_in)
            )

        AocLogger.log('all test cases passed')
        AocLogger.log('\n' * 5)

    def solve_part_1(self, puzzle_input):
        """
        Args:
            puzzle_input (string): the input

        Returns: the answer

        algo:
            for each claim
                mark squares
        """
        lines = puzzle_input.strip().split('\n')
        result = 0

        square_counts = {}
        for line in lines:
            line = line.strip()

            claim = Claim(line)

            for x in range(claim.from_left, claim.x_end):
                for y in range(claim.from_top, claim.y_end):
                    coords = '{}x{}'.format(x, y)
                    if coords not in square_counts:
                        square_counts[coords] = 0
                    square_counts[coords] += 1

        for count in square_counts.values():
            if count > 1:
                result += 1

        print('\npart 1 result: {}'.format(result))
        return result

    def solve_part_2(self, puzzle_input):
        """
        Args:
            puzzle_input (string): the input

        Returns: the answer

        instead of counts, keep a list of claim ids
        """
        lines = puzzle_input.strip().split('\n')
        result = 0

        square_claims = {}
        all_claims = []
        for line in lines:
            line = line.strip()

            claim = Claim(line)
            all_claims.append(claim)

            for x in range(claim.from_left, claim.x_end):
                for y in range(claim.from_top, claim.y_end):
                    coords = '{}x{}'.format(x, y)
                    if coords not in square_claims:
                        square_claims[coords] = []
                    square_claims[coords].append(claim)
                    if len(square_claims[coords]) > 1:
                        for claim in square_claims[coords]:
                            claim.has_conflict = True

        for claim in all_claims:
            if not claim.has_conflict:
                result = claim.id
                break

        print('\npart 2 result: {}'.format(result))
        return result





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




