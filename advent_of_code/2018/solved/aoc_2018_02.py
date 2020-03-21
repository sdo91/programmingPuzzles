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

import aocd

from advent_of_code.util import aoc_util



class AdventOfCode(object):
    """
    https://adventofcode.com/2018/day/2
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        puzzle_input = aocd.data

        self.test_part_1()
        aoc_util.assert_equal(
            6000,
            self.solve_part_1(puzzle_input)
        )

        self.test_part_2()
        aoc_util.assert_equal(
            'pbykrmjmizwhxlqnasfgtycdv',
            self.solve_part_2(puzzle_input)
        )

    def test_part_2(self):
        test_input = 'abcde fghij klmno pqrst fguij axcye wvxyz'
        self.solve_part_2(test_input)

    def solve_part_2(self, puzzle_input):
        print()
        tokens = puzzle_input.strip().split()

        for first_index in range(len(tokens)):
            for second_index in range(first_index + 1, len(tokens)):
                id_1 = tokens[first_index]
                id_2 = tokens[second_index]
                # print('compare: {}, {}'.format(id_1, id_2))
                diff_index = -1
                for i in range(len(id_1)):
                    if id_1[i] != id_2[i]:
                        if diff_index != -1:
                            # its the 2nd diff
                            diff_index = -1
                            break
                        diff_index = i
                if diff_index != -1:
                    print('match: {}, {}'.format(id_1, id_2))
                    result = id_1[:diff_index] + id_1[diff_index+1:]
                    print('part 2 result: {}'.format(result))
                    return result

    def test_part_1(self):
        test_input = 'abcdef bababc abbcde abcccd aabcdd abcdee ababab'
        self.solve_part_1(test_input)

    def solve_part_1(self, puzzle_input):
        """
        count 2s and 3s
        """
        print()
        tokens = puzzle_input.strip().split()

        num_2 = 0
        num_3 = 0
        for box_id in tokens:
            counts = {}
            for letter in box_id:
                if letter not in counts:
                    counts[letter] = 0
                counts[letter] += 1

            has_2 = False
            has_3 = False
            for key in counts:
                if counts[key] == 2:
                    has_2 = True
                if counts[key] == 3:
                    has_3 = True
                if has_2 and has_3:
                    break
            if has_2:
                num_2 += 1
            if has_3:
                num_3 += 1
        result = num_2 * num_3
        print('part 1 result: {} * {} = {}'.format(num_2, num_3, result))
        return result








# end MyClass





### HELPER FUNCTIONS ###





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




