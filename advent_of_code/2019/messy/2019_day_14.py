#!/usr/bin/env python3



### IMPORTS ###

import numpy as np
import math
import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
# from aoc_util.intcode_computer import IntcodeComputer


### CONSTANTS ###
TEST_INPUT_1 = [
    """
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
    """, """
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
    """, """

    """
]

TEST_OUTPUT_1 = [
    13312,
    2210736,
    0,
]

TEST_OUTPUT_2 = [
    82892753,
    460664,
    0,
]





class Reaction(object):

    def __init__(self, text):
        self.text = text

        before, after = aoc_util.split_and_strip_each(self.text, '=>')

        self.num_out, self.out = after.split()
        self.num_out = int(self.num_out)

        self.inputs = {}

        for token in aoc_util.split_and_strip_each(before, ','):
            num, val = token.split()
            self.inputs[val] = int(num)

    def __str__(self):
        return 'Reaction {}'.format(self.text)

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

        # self.run_tests()

        AocLogger.verbose = False

        # self.solve_part_1(puzzle_input)

        self.solve_part_2(puzzle_input)

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
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT_1, TEST_OUTPUT_1)

        aoc_util.run_tests(self.solve_part_2, TEST_INPUT_1, TEST_OUTPUT_2)

    # def solve_test_case_1(self, test_input):
    #     AocLogger.log('test input: {}'.format(test_input))
    #     return 0


    def solve_part_2(self, puzzle_input: str):
        puzzle_input = puzzle_input.strip()

        # bounds of fuel created
        lower_bound = 1  #
        upper_bound = 2

        while True:

            num_ore_needed = self.solve_part_1(puzzle_input, upper_bound)

            if num_ore_needed > 1e12:
                print('bounds found: {}'.format([lower_bound, upper_bound]))
                break

            lower_bound = upper_bound
            upper_bound *= 2


        while True:
            # check if neighbors
            if upper_bound == lower_bound + 1:
                break

            midpoint = (upper_bound + lower_bound) // 2

            num_ore_needed = self.solve_part_1(puzzle_input, midpoint)

            if num_ore_needed > 1e12:
                upper_bound = midpoint
            else:
                lower_bound = midpoint



        result = lower_bound
        print('part 2 result: {}'.format(result))
        return result










    def solve_part_1(self, puzzle_input: str, num_fuel=1):
        puzzle_input = puzzle_input.strip()

        self.reaction_dict = {}
        for line in puzzle_input.split('\n'):
            r = Reaction(line)
            self.reaction_dict[r.out] = r

        self.collected = {}
        self.num_ore = 0

        # x = self.collect(7, 'A')
        # x = self.old_collect(100, 'FUEL')

        self.collect(num_fuel, 'FUEL')

        # result = self.num_ore
        # print('part 1 result: {}'.format(result))

        print('{} ore -> {} fuel'.format(self.num_ore, num_fuel))
        return self.num_ore

    def collect(self, desired_num, resource_name):
        """
        return num ore

        base case:
            name is ore, return number

        examples:
            1 fuel
                7a
                    10 ore, 3 a in extra

        goal for 7A: collect 10 ore, then convert to 10 A
        """
        if resource_name not in self.collected:
            self.collected[resource_name] = 0

        if resource_name == 'ORE':
            self.collected[resource_name] += desired_num
            self.num_ore += desired_num
            # print('created {} {}'.format(desired_num, resource_name))
        else:
            # non base case

            reaction = self.reaction_dict[resource_name]

            num_we_lack = desired_num - self.collected[resource_name]
            num_reactions_needed = int(math.ceil(num_we_lack/reaction.num_out))

            while self.collected[resource_name] < desired_num:
                # collect all ingredients
                for ingredient in reaction.inputs:
                    # print(ingredient)
                    num_ingredient_needed = reaction.inputs[ingredient] * num_reactions_needed
                    self.collect(num_ingredient_needed, ingredient)

                    # then consume the needed amount
                    self.collected[ingredient] -= num_ingredient_needed

                # we have now collected/consumed
                num_created = reaction.num_out * num_reactions_needed
                self.collected[resource_name] += num_created
                # print('created {} {}'.format(num_created, resource_name))

        z=0


    def old_collect(self, desired_num, resource_name):
        """
        return num ore

        base case:
            name is ore, return number

        examples:
            1 fuel
                7a
                    10 ore, 3 a in extra

        goal for 7A: collect 10 ore, then convert to 10 A
        """
        if resource_name not in self.collected:
            self.collected[resource_name] = 0

        if resource_name == 'ORE':
            self.collected[resource_name] += desired_num
            self.num_ore += desired_num
            print('created {} {}'.format(desired_num, resource_name))
        else:
            # non base case

            reaction = self.reaction_dict[resource_name]

            # num_we_lack = desired_num - self.collected[resource_name]
            # num_reactions_needed = int(math.ceil(num_we_lack/reaction.num_out))

            while self.collected[resource_name] < desired_num:
                # collect all ingredients
                for ingredient in reaction.inputs:
                    # print(ingredient)
                    num_ingredient_needed = reaction.inputs[ingredient]
                    self.collect(num_ingredient_needed, ingredient)

                    # then consume the needed amount
                    self.collected[ingredient] -= num_ingredient_needed

                # we have now collected/consumed
                self.collected[resource_name] += reaction.num_out
                print('created {} {}'.format(reaction.num_out, resource_name))











    def solve_test_case_2(self, test_input):
        AocLogger.log('test input: {}'.format(test_input))
        return 0







if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




