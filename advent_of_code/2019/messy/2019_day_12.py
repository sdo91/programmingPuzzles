#!/usr/bin/env python3



### IMPORTS ###

import numpy as np
import itertools
import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
# from aoc_util.intcode_computer import IntcodeComputer



### CONSTANTS ###
TEST_INPUT_1 = [
    """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
    """, """
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
    """, """

    """
]

TEST_OUTPUT_1 = [
    179,
    0,
    0,
]

TEST_INPUT_2 = [
    """

    """, """

    """, """

    """
]

TEST_OUTPUT_2 = [
    0,
    0,
    0,
]





class Moon(object):

    def __init__(self, text):
        self.text = text

        self.pos = aoc_util.ints(text)
        self.vel = [0,0,0]

        self.energy = 0

        self.px = {}
        self.py = {}
        self.pz = {}

        self.vx = {}
        self.vy = {}
        self.vz = {}

    # def check_for_dup(self, i):
    #     if

    def apply_grav(self, other):
        for axis in range(3):
            if self.pos[axis] < other.pos[axis]:
                self.vel[axis] += 1
                other.vel[axis] -= 1
            elif self.pos[axis] > other.pos[axis]:
                self.vel[axis] -= 1
                other.vel[axis] += 1

    def apply_vel(self):
        for axis in range(3):
            self.pos[axis] += self.vel[axis]

    def calc_energy(self):
        z = [0,0,0]
        self.energy = aoc_util.manhatten_dist(z, self.pos) * aoc_util.manhatten_dist(z, self.vel)
        return self.energy

    def __str__(self):
        return 'pos={}, vel={}, energy={}'.format(
            self.pos, self.vel, self.energy)

    def __repr__(self):
        return str(self)





class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        try:
            puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            puzzle_input = 'unable to get input'
        aoc_util.write_input(puzzle_input, __file__)

        self.run_tests()

        AocLogger.verbose = False

        self.solve_part_1(puzzle_input, 1000)

        # self.solve_part_2(puzzle_input)

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_1(puzzle_input)
        # )

        # aoc_util.assert_equal(
        #     0,
        #     self.solve_part_2(puzzle_input)
        # )

    def run_tests(self):
        AocLogger.verbose = True
        # aoc_util.run_tests(self.solve_part_1, TEST_INPUT_1, TEST_OUTPUT_1)

        self.solve_part_1(TEST_INPUT_1[0], 10)
        # self.solve_part_1(TEST_INPUT_1[1], 100)

        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT_2, TEST_OUTPUT_2)

    def solve_test_case_1(self, test_input):
        AocLogger.log('test input: {}'.format(test_input))
        return 0

    def calc_state(self, axis, moons):
        result = []
        for m in moons:
            result.append(m.pos[axis])
            result.append(m.vel[axis])
        return tuple(result)

    def solve_part_1(self, puzzle_input: str, num_steps):
        puzzle_input = puzzle_input.strip()

        lines = puzzle_input.split('\n')
        moons = []
        for line in lines:
            moons.append(Moon(line))

        pairs = list(itertools.combinations([0,1,2,3], 2))

        initial_state = []
        for axis in range(3):
            initial_state.append(self.calc_state(axis, moons))

        periods = [0,0,0]

        # all_states = set()

        # for i in range(1, num_steps+1):
        i = 0
        while True:
            i += 1

            if i % 1000000 == 0:
                print('i: {}'.format(i))

            # do vel
            for p in pairs:
                moons[p[0]].apply_grav(moons[p[1]])

            # do pos
            e_sum = 0
            # state = []
            for m in moons:
                m.apply_vel()
                e_sum += m.calc_energy()

                # m.check_for_dup()
                #
                # state += m.pos
                # state += m.vel

            # check state
            for axis in range(3):
                if periods[axis] == 0:
                    a_state = self.calc_state(axis, moons)
                    if a_state == initial_state[axis]:
                        print('axis match: {}, {}'.format(axis, i))
                        periods[axis] = i

            if all(periods):
                print(periods)

                print(np.lcm.reduce(periods))

                break



            # state = tuple(state)
            #
            # if state in all_states:
            #     print(i-1)
            #     break
            # all_states.add(state)

            # print('\nafter {}'.format(i))
            # for m in moons:
            #     print(m)
            # print(e_sum)


        result = 0

        print('part 1 result: {}'.format(result))
        return result

    # def ()

    def solve_test_case_2(self, test_input):
        AocLogger.log('test input: {}'.format(test_input))
        return 0

    def solve_part_2(self, puzzle_input: str):
        puzzle_input = puzzle_input.strip()

        result = 0

        print('part 2 result: {}'.format(result))
        return result





if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




