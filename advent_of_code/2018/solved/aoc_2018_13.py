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
from bidict import bidict
from typing import List

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger
from advent_of_code.util.grid_2d import Grid2D


### CONSTANTS ###
TEST_INPUT = [
    r"""
/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/
    """, r"""
/---\
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+--/
  \----<-/
    """, r"""
/>-<\
|   |
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
    """
]

TEST_OUTPUT_1 = [
    (7, 3),
    0,
    0,
]

TEST_OUTPUT_2 = [
    0,
    0,
    (6, 4),
]










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
            print(traceback.format_exc())
            puzzle_input = 'unable to get input'
        aoc_util.write_input(puzzle_input, __file__)

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            (117, 62),
            self.solve_part_1(puzzle_input)
        )

        aoc_util.assert_equal(
            (69, 67),
            self.solve_part_2(puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True

        aoc_util.assert_equal(
            TEST_OUTPUT_1[0],
            self.solve_part_1(TEST_INPUT[0])
        )

        # self.solve_part_1(TEST_INPUT[1])

        aoc_util.assert_equal(
            TEST_OUTPUT_2[2],
            self.solve_part_2(TEST_INPUT[2])
        )

    def solve_part_1(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_1_result = solver.p1()

        print('part_1_result: {}\n'.format(aoc_util.format_coords(part_1_result)))
        return part_1_result

    def solve_part_2(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_2_result = solver.p2()

        print('part_2_result: {}\n'.format(aoc_util.format_coords(part_2_result)))
        return part_2_result










class Cart(object):

    DELTAS = {
        '<': (-1, 0),
        '>': (1, 0),
        '^': (0, -1),
        'v': (0, 1),
    }

    CHAR_TO_INT = bidict({
        '^': 0,
        '>': 1,
        'v': 2,
        '<': 3,
    })

    LR_CHARS = {'<', '>'}
    CORNERS = {'/', '\\'}
    INTERSECTION = '+'

    def __init__(self, char, coord, tracks: Grid2D):
        self.char = char
        self.coord = coord
        self.tracks = tracks
        self.next_turn = -1

    def __repr__(self):
        return '{} @ {}'.format(self.char, self.coord)

    def __lt__(self, other):
        """
        Args:
            other (Cart):

        carts on the top row move first (acting from left to right),
        then carts on the second row move (again from left to right),
        then carts on the third row, and so on.
        """
        if self.coord[1] == other.coord[1]:
            # if same row, choose left
            return self.coord[0] < other.coord[0]
        else:
            # choose top
            return self.coord[1] < other.coord[1]

    def get_track_under(self):
        if self.char in self.LR_CHARS:
            return '-'
        else:
            return '|'

    def move(self):
        r"""
        /->-\
        |   |  /----\
        | /-+--+-\  |
        | | |  | v  |
        \-+-/  \-+--/
          \------/

        new coord cases:
            straight: just move
            corner: move, decide, and turn
            intersection: move, decide, and turn

        """
        old = self.coord
        new = aoc_util.tuple_add(old, self.DELTAS[self.char])
        self.coord = new

        # check for collision
        if new in self.tracks.overlay:
            print('collison @ {}'.format(new))
            if AocLogger.verbose:
                self.tracks.show()
            return new

        # move
        del self.tracks.overlay[old]
        self.decide_direction(new)
        self.tracks.overlay[new] = self.char

        return None

    def decide_direction(self, new):
        """
        Each time a cart has the option to turn (by arriving at any intersection), it turns left the first time,
        goes straight the second time, turns right the third time, and then repeats those directions starting again
        with left the fourth time, straight the fifth time, and so on. This process is independent of the particular
        intersection at which the cart has arrived - that is, the cart has no per-intersection memory.
        """
        new_track = self.tracks.get_tuple(new)

        if new_track == self.INTERSECTION:
            self.apply_turn(self.next_turn)
            self.next_turn += 1
            if self.next_turn > 1:
                self.next_turn = -1

        elif new_track in self.CORNERS:
            turn_int = -1
            if new_track == '/':
                if self.char not in self.LR_CHARS:
                    # coming from top/bottom
                    turn_int = 1
            else:          # \
                if self.char in self.LR_CHARS:
                    # coming from left/right
                    turn_int = 1
            self.apply_turn(turn_int)

    def apply_turn(self, turn_int):
        current_int = self.CHAR_TO_INT[self.char]
        new_int = (current_int + turn_int) % 4
        self.char = self.CHAR_TO_INT.inverse[new_int]










class Solver(object):

    carts = ...  # type: List[Cart]

    def __init__(self, text: str):
        self.text = text.strip('\n')
        self.tracks = Grid2D(self.text)

        # find carts
        def is_cart(char):
            return char in Cart.DELTAS.keys()
        cart_coords = self.tracks.find_by_function(is_cart)

        # create carts, fix tracks
        self.carts = []
        for coord in cart_coords:
            char = self.tracks.get_tuple(coord)
            cart = Cart(char, coord, self.tracks)
            self.carts.append(cart)
            self.tracks.set_tuple(coord, cart.get_track_under())
        if AocLogger.verbose:
            self.tracks.show()

        # set overlay
        for cart in self.carts:
            self.tracks.overlay[cart.coord] = cart.char
        if AocLogger.verbose:
            self.tracks.show()

        # slow mode
        print('num_carts: {}'.format(len(self.carts)))
        self.delay = 0
        if len(self.carts) < 2:
            self.delay = 0.5

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        """
        Several carts are also on the tracks. Carts always face either up (^), down (v), left (<), or right (>). (On
        your initial map, the track under each cart is a straight path matching the direction the cart is facing.)

        Carts all move at the same speed; they take turns moving a single step at a time. They do this based on their
        current location: carts on the top row move first (acting from left to right), then carts on the second row
        move (again from left to right), then carts on the third row, and so on. Once each cart has moved one step,
        the process repeats; each of these loops is called a tick.

        not:
        132,47
        86,71
        """
        i = 0
        while True:
            i += 1
            # do one tick
            self.carts = list(sorted(self.carts))
            for cart in self.carts:  # type: Cart
                collision = cart.move()
                if collision:
                    return collision
            if AocLogger.verbose:
                self.tracks.show()
                print('i: {}'.format(i))
            if self.delay:
                time.sleep(self.delay)
            z=0

    def p2(self):
        """
        There isn't much you can do to prevent crashes in this ridiculous system. However, by predicting the crashes,
        the Elves know where to be in advance and instantly remove the two crashing carts the moment any crash occurs.

        They can proceed like this for a while, but eventually, they're going to run out of carts. It could be useful
        to figure out where the last cart that hasn't crashed will end up.

        After four very expensive crashes, a tick ends with only one cart remaining; its final location is 6,4.

        What is the location of the last cart at the end of the first tick where it is the only cart left?
        """
        i = 0
        while True:
            i += 1
            # do one tick
            self.carts = list(sorted(self.carts))
            tick_collisions = set()
            for cart in self.carts:  # type: Cart
                if cart.coord in tick_collisions:
                    # skip cart if already in a collison
                    print('skipping cart already in collision: {}'.format(cart))
                    continue
                collision = cart.move()
                if collision:
                    tick_collisions.add(collision)

            # remove collisions
            if tick_collisions:
                remaining = []
                self.tracks.overlay = {}
                for cart in self.carts:
                    if cart.coord not in tick_collisions:
                        remaining.append(cart)
                        self.tracks.overlay[cart.coord] = cart.char
                self.carts = remaining

            if AocLogger.verbose:
                self.tracks.show()
                print('i: {}'.format(i))

            if len(self.carts) == 1:
                if AocLogger.verbose:
                    self.tracks.show()
                return self.carts[0].coord

            if self.delay:
                time.sleep(self.delay)










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




