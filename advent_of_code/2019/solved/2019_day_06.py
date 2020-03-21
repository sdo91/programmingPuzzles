#!/usr/bin/env python3



### IMPORTS ###

import aocd
import re
import parse
import typing
from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger




### CONSTANTS ###

TEST_INPUT = [
    """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
    """, """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
    """, """

    """
]





def main():
    print('starting {}'.format(__file__.split('/')[-1]))

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    AocLogger.verbose = True
    # aoc_util.run_tests(solve_test_case, TEST_INPUT, TEST_OUTPUT)
    aoc_util.assert_equal(
        [42],
        solve_puzzle(TEST_INPUT[0])
    )
    aoc_util.assert_equal(
        [54, 4],
        solve_puzzle(TEST_INPUT[1])
    )

    AocLogger.verbose = False

    aoc_util.assert_equal(
        [249308, 349],
        solve_puzzle(puzzle_input)
    )


def get_num_orbits(key, orbits_dict, base='COM'):
    if key == base:
        return 0
    else:
        return 1 + get_num_orbits(orbits_dict[key], orbits_dict, base)


def solve_puzzle(test_input: str):
    """
    38 min

    :param test_input:
    :return:
    """
    print()
    test_input = test_input.strip()
    AocLogger.log('test input:\n{}'.format(test_input))
    result = []

    orbits_dict = {}

    # matches = aoc_util.re_find_all_matches(r'COM\).+', test_input)

    lines = test_input.split('\n')
    for line in lines:
        tokens = line.split(')')
        orbits_dict[tokens[1]] = tokens[0]

    AocLogger.log('orbits_dict: {}'.format(orbits_dict))

    # solve part 1
    total_orbits = 0
    for key in orbits_dict:
        # count orbits
        num_orbits = get_num_orbits(key, orbits_dict)
        total_orbits += num_orbits
    result.append(total_orbits)
    if 'YOU' not in orbits_dict:
        # needed for part 2
        return result

    # solve part 2
    you_path = []
    current = 'YOU'
    while True:
        current = orbits_dict[current]
        you_path.append(current)

        if current == "COM":
            break

    san_path = []
    current = 'SAN'
    while True:
        current = orbits_dict[current]
        san_path.append(current)

        if current == "COM":
            break

    for star in you_path:
        if star in san_path:
            common = star
            break

    z = 0

    a = get_num_orbits(orbits_dict['YOU'], orbits_dict, common)
    b = get_num_orbits(orbits_dict['SAN'], orbits_dict, common)
    num_xfers = a + b
    result.append(num_xfers)
    print('result: {}'.format(result))
    return result





if __name__ == '__main__':
    main()




