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

# addToPath('.')

### IMPORTS ###

import aocd
from aoc_util import aoc_util


class Star(object):

    def __init__(self, line):
        tokens = line.split(',')
        self.point = (
            int(tokens[0]),
            int(tokens[1]),
            int(tokens[2]),
            int(tokens[3]))

    def __str__(self):
        return str(self.point)

    def __repr__(self):
        return str(self)

    def dist(self, other):
        result = 0
        for i in range(len(self.point)):
            result += abs(self.point[i] - other.point[i])
        return result


















class AdventOfCode(object):
    """
    https://adventofcode.com/2018/day/2
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        puzzle_input = aocd.data

        self.test_part_1()
        aoc_util.assert_equal(
            390,
            self.count_groups(puzzle_input)
        )

    def test_part_1(self):
        test_input = '''
            0,0,0,0
            3,0,0,0
            0,3,0,0
            0,0,3,0
            0,0,0,3
            0,0,0,6
            9,0,0,0
            12,0,0,0
        '''
        aoc_util.assert_equal(2, self.count_groups(test_input))

        test_input += '6,0,0,0'
        aoc_util.assert_equal(1, self.count_groups(test_input))



    def count_groups(self, puzzle_input, verbose=False):
        """
        keep a set of groups

        for each new point check all previous points,
        note each group match

        if none:
            new group
        if one:
            add to group
        if 2+:
            merge groups, then add

        """
        input_lines = puzzle_input.strip().split('\n')
        groups = {}
        group_id_counter = 0

        for line in input_lines:
            line = line.strip()

            new_star = Star(line)
            matching_group_ids = []

            for group_id in groups:
                for existing_star in groups[group_id]:
                    if new_star.dist(existing_star) <= 3:
                        matching_group_ids.append(group_id)
                        break

            if len(matching_group_ids) == 0:
                # new group
                groups[group_id_counter] = {new_star}
                group_id_counter += 1
            else:
                # add to existing group
                groups[matching_group_ids[0]].add(new_star)

                while len(matching_group_ids) > 1:
                    # merge groups
                    first = groups[matching_group_ids[0]]
                    second = groups[matching_group_ids[-1]]
                    first.update(second)
                    del groups[matching_group_ids[-1]]
                    matching_group_ids.pop()

        if verbose:
            self.print_groups(groups)

        result = len(groups)
        print('result: {}'.format(result))
        return result

    def print_groups(self, groups):
        print()
        print('groups:')
        for key in groups:
            print(key)
            for value in groups[key]:
                print('\t{}'.format(value))









# end MyClass





### HELPER FUNCTIONS ###





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




