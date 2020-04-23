#!/usr/bin/env python3



### IMPORTS ###

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger




### CONSTANTS ###
TEST_INPUT = [
    111111,  # no double
    223450,  # decreases
    123789,  # no double
    112233,  # valid
    123444,  # no double
    111122,  # 1s dont create a double, but 2s do
]

TEST_OUTPUT = [
    False,
    False,
    False,
    True,
    False,
    True,
]








class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        try:
            puzzle_input = '165432-707912'
        except aocd.exceptions.AocdError:
            puzzle_input = 'unable to get input'
        aoc_util.write_input(puzzle_input, __file__)

        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_test_case, TEST_INPUT, TEST_OUTPUT)

        AocLogger.verbose = False



        # self.solve_full_input(puzzle_input)

        aoc_util.assert_equal(
            1716,
            self.solve_full_input(puzzle_input, part=1)
        )

        aoc_util.assert_equal(
            1163,
            self.solve_full_input(puzzle_input, part=2)
        )





    def solve_test_case(self, i, part=2):
        """
        i: 012345

        https://stackoverflow.com/questions/6306098/regexp-match-repeated-characters
        """
        digits = str(i)

        matches = aoc_util.re_find_all_matches(r'(.)\1+', digits)

        if part == 1:
            has_double = len(matches)
        else:
            has_double = any([len(x) == 2 for x in matches])

        is_inc = all([digits[i] <= digits[i+1] for i in range(len(digits)-1)])

        result = has_double and is_inc
        if result:
            AocLogger.log('good: {}'.format(i))
        else:
            AocLogger.log('bad: {}'.format(i))
        return result

    def solve_full_input(self, puzzle_input, part=2):

        rng = aoc_util.positive_ints(puzzle_input)

        results = set()

        for i in range(rng[0], rng[1] + 1):
            if self.solve_test_case(i, part):
                results.add(i)

        result = len(results)
        print('\nresult: {}'.format(result))
        return result





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




