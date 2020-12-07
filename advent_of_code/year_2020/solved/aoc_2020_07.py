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

### CONSTANTS ###
TEST_INPUT = [
    """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
    """, """
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
    """, """

    """
]

TEST_OUTPUT_1 = [
    4,
    0,
    0,
]

TEST_OUTPUT_2 = [
    32,
    126,
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
            121,
            self.solve_part_1(self.puzzle_input)
        )

        aoc_util.assert_equal(
            3805,
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


class Relation(object):

    def __init__(self, text: str):
        text = text.replace('bags', '')
        text = text.replace('bag', '')
        text = text.replace('.', '')

        tokens = text.split('contain')
        self.container = tokens[0].strip()
        self.contained = {}

        for entry in tokens[-1].split(','):
            if 'no other' in entry:
                continue
            entry = entry.strip()
            i = entry.find(' ')
            num_bags = int(entry[:i])
            color = entry[i + 1:]
            self.contained[color] = num_bags

    def __repr__(self):
        return '{} contains {}'.format(self.container, self.contained)


class Solver(object):

    def __init__(self, text: str):
        self.text = text.strip()
        AocLogger.log(str(self))
        self.lines = aoc_util.lines(self.text)

        self.relations = {}
        for line in self.lines:
            rel = Relation(line)
            self.relations[rel.container] = rel

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        # find holders of each color of bag
        holders_of = defaultdict(set)
        for relation in self.relations.values():
            for color in relation.contained:
                holders_of[color].add(relation.container)

        # recursively get all holders
        result_set = set()
        self.recursive_get_holders('shiny gold', holders_of, result_set)
        return len(result_set)

    def recursive_get_holders(self, small_bag, holders_of, result_set):
        for large_bag in holders_of[small_bag]:
            result_set.add(large_bag)
            self.recursive_get_holders(large_bag, holders_of, result_set)

    def p2(self):
        num_bags = self.recursive_count_bags_contained('shiny gold')
        return num_bags

    def recursive_count_bags_contained(self, large):
        result = 0
        relation = self.relations[large]
        for small in relation.contained:
            num_small = relation.contained[small]
            result += num_small * (self.recursive_count_bags_contained(small) + 1)
        return result


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
