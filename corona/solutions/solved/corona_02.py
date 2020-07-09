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
from itertools import permutations

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger










class DayManager(object):

    def __init__(self):
        self.puzzle_input = 'no input for day 2'

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))
        start_time = time.time()

        self.run_tests()

        self.run_real()

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True

        Solver.assert_fast_eq_slow(1)
        Solver.assert_fast_eq_slow(2)
        Solver.assert_fast_eq_slow(3)

        # Solver.print_tri(Solver.gen_pascals_tri(5))

        Solver.assert_fast_eq_slow(1, 4)
        Solver.assert_fast_eq_slow(1, 5)
        Solver.assert_fast_eq_slow(2, 4)
        Solver.assert_fast_eq_slow(2, 5)

    def run_real(self):
        AocLogger.verbose = False

        aoc_util.assert_equal(
            5550996791340,
            self.solve_part_1(self.puzzle_input)
        )

        aoc_util.assert_equal(
            623360743125120,
            self.solve_part_2(self.puzzle_input)
        )

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

    def __init__(self, text: str):
        self.text = text.strip()
        AocLogger.log(str(self))

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        """
        Ok, ok… We get it. It’s Sunday and all you want to do is chill and be lazy. Don’t worry, we won’t bother you
        much (today).

        Imagine that you are placed in a giant cube of size 10m x 10m x 10m, concretely in any corner of it. You are
        told to move to the opposite corner of that cube.

        How many paths you can take?

        Note: You must take the shortest possible path and can only walk on the edges of the 1m cubes forming the big
        one.

        #iwouldnotbruteforcethis
        """
        num_paths = self.find_num_paths_fast(10)
        return num_paths

    @classmethod
    def assert_fast_eq_slow(cls, n, d=3):
        assert cls.find_num_paths_slow(n, d) == cls.find_num_paths_fast(n, d)

    @classmethod
    def find_num_paths_slow(cls, n, dimensions=3):
        steps = []
        for i in range(n):
            for j in range(dimensions):
                char = chr(ord('A') + j)
                steps.append(char)

        num_paths = len(set(permutations(steps)))
        print('{} -> {}'.format(
            ' x '.join([str(n)] * dimensions),
            num_paths
        ))
        return num_paths

    @classmethod
    def find_num_paths_fast(cls, n, dimensions=3):
        triangle_size = n * dimensions
        tri = cls.gen_pascals_tri(triangle_size)
        if AocLogger.verbose or 1:
            cls.print_tri(tri)

        num_paths = 1  # 1d base case
        multipliers = []
        for x in range(2, dimensions + 1):
            mult = tri[n][n * (x - 1)]
            num_paths *= mult
            multipliers.append(str(mult))

        print('{} = {}\n'.format(
            ' * '.join(multipliers),
            num_paths
        ))
        return num_paths

    @classmethod
    def gen_pascals_tri(cls, n):
        tri = [[1]]
        for _ in range(n):
            # print('add a new diag')
            for y, row in enumerate(tri):
                # print('add to row {}'.format(y))
                x = len(row)
                if x < 1 or y < 1:
                    value = 1
                else:
                    value = tri[y - 1][x] + tri[y][x - 1]
                row.append(value)
            tri.append([1])
            # z=0
        return tri

    @classmethod
    def print_tri(cls, tri):
        max_value_row = len(tri)//2
        max_value = tri[max_value_row][-1]
        width = len(str(max_value)) + 1
        print('tri: (max_value={})'.format(max_value))
        for row in tri:
            builder = []
            for x in row:
                builder.append('{:{}d}'.format(x, width))
            print(''.join(builder))

    def p2(self):
        """
        Wow, you made it!

        I guess it was too easy, so… imagine that the cube is from another universe (also with a pandemic issue)
        where there are more than 3 dimensions. In that universe, the cube is converted to an hypercube of dimension 5.

        What would be the number of paths in that hypercube?

        Oh wait, I forgot something… The size of its sides was reduced by half during the multi-universe transition,
        so take that in mind.

        #idefinitelyshouldnotbruteforcethis
        """
        fast_5x5 = self.find_num_paths_fast(5, 5)
        return fast_5x5










if __name__ == '__main__':
    instance = DayManager()
    instance.run()




