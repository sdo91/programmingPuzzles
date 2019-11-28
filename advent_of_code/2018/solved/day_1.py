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

import requests



class MyClass(object):
    """
    https://adventofcode.com/2018/day/1#part2
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        input_path = '/home/sdo91/code/subdirs/personal/programming_puzzles/advent_of_code/2018/input/input_1.txt'

        with open(input_path) as infile:
            puzzle_input = infile.read()

            self.solve(puzzle_input)

        # url = 'https://adventofcode.com/2018/day/1/input'
        # downloaded_input = requests.get(url)
        # self.solve(downloaded_input)


    def solve(self, puzzle_input):
        tokens = puzzle_input.strip().split()

        part_1_result = 0
        for token in tokens:
            part_1_result += int(token)

        print('part_1_result: {}'.format(part_1_result))


        already_seen = set()
        sum_so_far = 0
        isDone = False
        while not isDone:
            for token in tokens:
                sum_so_far += int(token)
                if sum_so_far in already_seen:
                    print('seen 2x: {}'.format(sum_so_far))
                    isDone = True
                    break
                else:
                    already_seen.add(sum_so_far)




# end MyClass





### HELPER FUNCTIONS ###





if __name__ == '__main__':
    instance = MyClass()
    instance.run()




