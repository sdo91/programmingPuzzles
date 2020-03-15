#!/usr/bin/env python3



### IMPORTS ###

import math
import time

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger





### CONSTANTS ###

TEST_INPUT = [
    """
deal with increment 7
deal into new stack
deal into new stack
Result: 0 3 6 9 2 5 8 1 4 7
    """, """
cut 6
deal with increment 7
deal into new stack
Result: 3 0 7 4 1 8 5 2 9 6
    """, """
deal with increment 7
deal with increment 9
cut -2
Result: 6 3 0 7 4 1 8 5 2 9
    ""","""
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
Result: 9 2 5 8 1 4 7 0 3 6
"""
]
















class Deck(object):

    def __init__(self, size):
        self.size = size
        self.cards = list(range(size))

    def __repr__(self):
        formatted_deck = ' '.join([str(x) for x in self.cards])
        # AocLogger.log('new_deck: {}'.format(formatted_deck))
        return formatted_deck

    def do(self, text):
        # techniques

        if 'stack' in text:
            self.do_stack()
        elif 'cut' in text:
            self.do_cut(aoc_util.ints(text)[0])
        elif 'increment' in text:
            self.do_increment(aoc_util.ints(text)[0])
        else:
            raise RuntimeError(text)

    def do_stack(self):
        self.cards = list(reversed(self.cards))

    def do_cut(self, n):
        if n < 0:
            n = self.size + n
        self.cards = self.cards[n:] + self.cards[:n]
        z=0

    def do_increment(self, n):
        new_cards = [0] * self.size
        new_index = 0
        for old_index in range(self.size):
            new_cards[new_index] = self.cards[old_index]
            new_index += n
            new_index %= self.size
        self.cards = new_cards

















class HugeDeck(object):

    P2_DECK_SIZE = 119315717514047
    P2_NUM_SHUFFLES = 101741582076661

    P2_RESULT_1_SHUFFLE = 12854400258724
    P2_RESULT_2_SHUFFLES = 50273104329503
    P2_RESULT_9_SHUFFLES = 14959559542067

    DEAL_STACK = 1
    CUT_N = 2
    DEAL_INC_N = 3

    def __init__(self, text, size, final_position):
        self.size = size
        self.position = final_position
        # self.technique_idx = 0

        # parse text
        self.shuffle_steps_reversed = []
        for line in reversed(aoc_util.lines(text)):
            if 'Result' in line:
                continue
            elif 'stack' in line:
                step = (line, self.DEAL_STACK)
            elif 'cut' in line:
                step = (line, self.CUT_N, aoc_util.ints(line)[0])
            elif 'increment' in line:
                step = (line, self.DEAL_INC_N, aoc_util.ints(line)[0])
            else:
                raise RuntimeError(line)
            # print('{} -> {}'.format(line, step))
            self.shuffle_steps_reversed.append(step)

    def deal_stack(self):
        """
        let size = 10

        0->9 = 9-0
        4->5 = 0-4
        5->4 = 9-5
        9->0 = 9-9
        """
        self.position = (self.size - 1) - self.position

    def cut_n(self, n):
        """
        let s=10, n=3

        0->3 = (p + n) % s
        6->9
        7->0
        9->2
        """
        self.position = (self.position + n) % self.size

    @staticmethod
    def mod_inverse(a, m):
        """
        NOTE: a and m must be coprime (GCD == 1)
        """
        if m < 100:
            for x in range(1, m):
                if (a * x) % m == 1:
                    return x
        if math.gcd(a, m) != 1:
            raise RuntimeError('can\'t mod divide: {}'.format([a, m]))
        return pow(a, m - 2, m)

    @classmethod
    def mod_divide(cls, num, denom, m):
        num %= m
        inv = cls.mod_inverse(denom, m)
        return (inv * num) % m

    def deal_inc_n(self, n):
        """
        let s=10, n=3
        forward:

        0->0
        1->3
        4->2: 0 + (4 * 3) = 2 (mod 10)
        5->5: (5 * 3) = 5
        6->8: (6 * 3) = 18

        modular division:

        reverse:
        if it ends at 8, where did it start? (6)
        8->6: 8 / 3 = 6 (mod 10)

        """
        self.position = self.mod_divide(self.position, n, self.size)

    def shuffle_n(self, n):
        """
        shuffle deck n times

        given:
            list of steps
            size of deck
            final position
            #num shuffles (start with 1)

        algo:
            go thru steps in reverse order
            calc a, b
            return ax + b
        """

        for x in range(n):
            # if x % 1000 == 0:
            #     print(x)

            # do one shuffle
            for step in self.shuffle_steps_reversed:
                # print()
                # print(step)
                # print(self.position)

                if step[1] == self.DEAL_STACK:
                    self.deal_stack()
                elif step[1] == self.CUT_N:
                    self.cut_n(step[2])
                elif step[1] == self.DEAL_INC_N:
                    self.deal_inc_n(step[2])
                else:
                    raise RuntimeError('invalid technique')

        return self.position
















def main():
    print('starting {}'.format(__file__.split('/')[-1]))

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    AocLogger.verbose = True
    run_tests(puzzle_input)

    AocLogger.verbose = False

    aoc_util.assert_equal(
        2519,
        solve_part_1(puzzle_input)
    )

    # time_test()


def time_test():
    start_time = time.time()
    x = HugeDeck.P2_NUM_SHUFFLES
    while x > 0:
        if x % 1000 == 9:
            print(x)
        x -= 1
    print(time.time() - start_time)


def assert_p1_test(text: str):
    input_text, expected_result = aoc_util.split_and_strip_each(text, 'Result:')

    shuffled_deck = solve_test_case_1(input_text)

    aoc_util.assert_equal(
        expected_result,
        str(shuffled_deck)
    )


def run_tests(puzzle_input):

    assert_p1_test(TEST_INPUT[0])
    assert_p1_test(TEST_INPUT[1])
    assert_p1_test(TEST_INPUT[2])
    assert_p1_test(TEST_INPUT[3])

    aoc_util.assert_equal(2, HugeDeck.mod_divide(8, 4, 5))
    aoc_util.assert_equal(1, HugeDeck.mod_divide(8, 3, 5))
    aoc_util.assert_equal(4, HugeDeck.mod_divide(11, 4, 5))

    aoc_util.assert_equal(7, HugeDeck.mod_inverse(3, 10))
    aoc_util.assert_equal(6, HugeDeck.mod_divide(8, 3, 10))

    aoc_util.assert_equal(
        5,
        solve_2(TEST_INPUT[3], size=10, final_position=2, num_times=1)
    )

    aoc_util.assert_equal(
        2019,
        solve_2(puzzle_input, size=10007, final_position=2519, num_times=1)
    )

    aoc_util.assert_equal(
        HugeDeck.P2_RESULT_1_SHUFFLE,
        solve_2(puzzle_input, size=HugeDeck.P2_DECK_SIZE, final_position=2020, num_times=1)
    )    
    
    aoc_util.assert_equal(
        HugeDeck.P2_RESULT_2_SHUFFLES,
        solve_2(puzzle_input, size=HugeDeck.P2_DECK_SIZE, final_position=2020, num_times=2)
    )

    aoc_util.assert_equal(
        HugeDeck.P2_RESULT_9_SHUFFLES,
        solve_2(puzzle_input, size=HugeDeck.P2_DECK_SIZE, final_position=2020, num_times=9)
    )


def solve_2(text, size, final_position, num_times):
    hd = HugeDeck(text, size, final_position)

    part_2_result = hd.shuffle_n(num_times)

    print('part_2_result: {}'.format(part_2_result))
    return part_2_result


def solve_test_case_1(test_input, size=10):
    test_input = test_input.strip()
    # AocLogger.log('test input:\n{}'.format(test_input))

    d = Deck(size)

    for line in aoc_util.lines(test_input):
        if 'Result' in line:
            continue
        d.do(line)

    return d


def solve_part_1(puzzle_input):
    """
    8611 high
    """
    shuffled_deck = solve_test_case_1(puzzle_input, 10007)
    return shuffled_deck.cards.index(2019)





if __name__ == '__main__':
    main()




