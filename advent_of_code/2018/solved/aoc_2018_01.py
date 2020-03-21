#!/usr/bin/env python3


### IMPORTS ###

import aocd
from advent_of_code.util import aoc_util



class MyClass(object):
    """
    https://adventofcode.com/2018/day/1
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        puzzle_input = aocd.data

        aoc_util.assert_equal(
            (561, 563),
            self.solve(puzzle_input)
        )



    def solve(self, puzzle_input):
        tokens = puzzle_input.strip().split()

        part_1_result = 0
        for token in tokens:
            part_1_result += int(token)

        print('part_1_result: {}'.format(part_1_result))


        already_seen = set()
        sum_so_far = 0
        while True:
            for token in tokens:
                sum_so_far += int(token)
                if sum_so_far in already_seen:
                    print('seen 2x: {}'.format(sum_so_far))
                    return part_1_result, sum_so_far
                else:
                    already_seen.add(sum_so_far)




# end MyClass





### HELPER FUNCTIONS ###





if __name__ == '__main__':
    instance = MyClass()
    instance.run()




