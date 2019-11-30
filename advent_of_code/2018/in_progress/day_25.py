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

        input_dir = '/home/sdo91/code/subdirs/personal/programming_puzzles/advent_of_code/2018/input/'
        input_path = '{}/input_{}.txt'.format(input_dir, 25)

        with open(input_path) as infile:
            puzzle_input = infile.read()

            self.test_part_1()
            print('num groups: {}'.format(self.count_groups(puzzle_input)))

    @staticmethod
    def assert_equal(expected, actual):
        if expected != actual:
            print('expected: {}'.format(expected))
            print('actual: {}'.format(actual))
        assert expected == actual

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
        self.assert_equal(2, self.count_groups(test_input))

        test_input += '6,0,0,0'
        self.assert_equal(1, self.count_groups(test_input))



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

        return len(groups)

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




