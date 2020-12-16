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

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger
from advent_of_code.util.grid_2d import Grid2D

### CONSTANTS ###
TEST_INPUT = [
    """
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
    """, """
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
    """, """

    """
]

TEST_OUTPUT_1 = [
    71,
    0,  # not a typo
    0,
]

TEST_OUTPUT_2 = [
    None,
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
            error_msg = traceback.format_exc()
            print(error_msg)
            self.puzzle_input = 'unable to get input:\n\n{}'.format(error_msg)
        aoc_util.write_input(self.puzzle_input, __file__)

    def run(self):
        start_time = time.time()

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            21980,
            self.solve_part_1(self.puzzle_input)
        )

        aoc_util.assert_equal(
            0,
            self.solve_part_2(self.puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def solve_part_1(self, text: str):
        solver = Solver(text)

        part_1_result = solver.p1()

        print('part_1_result: {}\n'.format(part_1_result))
        return part_1_result

    def solve_part_2(self, text: str):
        solver = Solver(text)

        part_2_result = solver.p2()

        print('part_2_result: {}\n'.format(part_2_result))
        return part_2_result


class Solver(object):

    def __init__(self, text: str):
        self.text = text.strip()
        # self.lines = aoc_util.lines(text)
        AocLogger.log(str(self))

        rules_text, mine_text, nearby_text = text.split('\n\n')

        self.rules = {}
        for rule in aoc_util.lines(rules_text):
            name = rule.split(':')[0]
            ints = aoc_util.positive_ints(rule)
            valid_set = set(range(ints[0], ints[1] + 1)) | set(range(ints[2], ints[3] + 1))
            self.rules[name] = valid_set

        self.nearby_tickets = []
        for nt in aoc_util.lines(nearby_text):
            if 'nearby' in nt:
                continue
            self.nearby_tickets.append(aoc_util.ints(nt))

        self.my_ticket = aoc_util.ints(mine_text)

        self.all_rules = frozenset(self.rules.keys())

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        error_rate = 0

        for ticket in self.nearby_tickets:
            for value in ticket:
                # check if the value is valid
                if not self.is_valid_value(value):
                    error_rate += value

        return error_rate

    def p2(self):
        """

        get valid tickets

        for each field,
            check which rules fit

        from example:
            0: {'row'}
            1: {'class', 'row'}
            2: {'class', 'row', 'seat'}

        """
        valid_tickets = []
        for ticket in self.nearby_tickets:
            # ticket valid if all values are valid
            is_valid_ticket = all(self.is_valid_value(v) for v in ticket)
            if is_valid_ticket:
                valid_tickets.append(ticket)

        for field_id in range(len(self.my_ticket)):
            matches = self.get_matches(valid_tickets, field_id)
            print('{}: {}'.format(field_id, matches))
            z = 0

        # todo: simplify until all rules are assigned

        z = 0
        return 2

    def is_valid_value(self, value):
        return any(value in s for s in self.rules.values())

    def get_matches(self, valid_tickets, field_id):
        """
        get all rules
        for each field:
            eliminate any rules which dont fit
        assert 1 field left
        """
        potential_matches = set(self.all_rules)
        for ticket in valid_tickets:
            field_value = ticket[field_id]

            # check which rules match
            for rule_name in list(potential_matches):
                if field_value not in self.rules[rule_name]:
                    # not a match
                    potential_matches.remove(rule_name)

            z=0

        # assert len(potential_matches) == 1
        # return potential_matches.pop()
        return potential_matches


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
