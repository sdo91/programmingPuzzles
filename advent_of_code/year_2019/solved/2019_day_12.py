#!/usr/bin/env python3


### IMPORTS ###

import numpy as np
import itertools
import time

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger


### CONSTANTS ###

TEST_INPUT = [
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

TEST_OUTPUT = [
    (179, 2772),
    (1940, 4686774924),
    0,
]










class Moon(object):

    def __init__(self, text):
        self.text = text

        self.pos = aoc_util.ints(text)
        self.vel = [0, 0, 0]

        self.energy = 0

        self.px = {}
        self.py = {}
        self.pz = {}

        self.vx = {}
        self.vy = {}
        self.vz = {}

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
        z = [0, 0, 0]
        self.energy = aoc_util.manhatten_dist(z, self.pos) * aoc_util.manhatten_dist(z, self.vel)
        return self.energy

    def __repr__(self):
        return 'pos={}, vel={}, energy={}'.format(
            self.pos, self.vel, self.energy)










class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))
        start_time = time.time()

        try:
            puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            puzzle_input = 'unable to get input'
        aoc_util.write_input(puzzle_input, __file__)

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            (7722, 292653556339368),
            self.solve(puzzle_input, 1000)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True

        aoc_util.assert_equal(
            TEST_OUTPUT[0],
            self.solve(TEST_INPUT[0], 10)
        )

        aoc_util.assert_equal(
            TEST_OUTPUT[1],
            self.solve(TEST_INPUT[1], 100)
        )

    def calc_state(self, axis, moons):
        result = []
        for m in moons:
            result.append(m.pos[axis])
            result.append(m.vel[axis])
        return tuple(result)

    def solve(self, puzzle_input: str, num_steps_p1):
        print('\n\n\n')
        puzzle_input = puzzle_input.strip()
        p1_result = -1

        lines = puzzle_input.split('\n')
        moons = []
        for line in lines:
            moons.append(Moon(line))

        pairs = list(itertools.combinations([0, 1, 2, 3], 2))

        initial_state = []
        for axis in range(3):
            initial_state.append(self.calc_state(axis, moons))

        periods = [0, 0, 0]

        i = 0
        while True:
            i += 1

            # do vel
            for p in pairs:
                moons[p[0]].apply_grav(moons[p[1]])

            # do pos
            total_energy = 0
            for m in moons:
                m.apply_vel()
                total_energy += m.calc_energy()

            if i == num_steps_p1:
                p1_result = total_energy
                print('p1_result: {}'.format(p1_result))

            # check state
            for axis in range(3):
                if periods[axis] == 0:
                    a_state = self.calc_state(axis, moons)
                    if a_state == initial_state[axis]:
                        print('axis match: {}, {}'.format(axis, i))
                        periods[axis] = i

            if all(periods):
                AocLogger.log(periods)
                p2_result = np.lcm.reduce(periods)
                print('p2_result: {}'.format(p2_result))
                break
        # end while

        return p1_result, p2_result










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
