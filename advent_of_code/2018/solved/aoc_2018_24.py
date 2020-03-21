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
import re

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger



IMMUNE_SYSTEM = 'Immune System'
INFECTION = 'Infection'

TEST_INPUT = '''
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4        
'''


class Group(object):

    def __init__(self, team, id, text, boost=0):
        self.team = team
        self.id = id
        self.text = text.lower()

        self.ints = aoc_util.ints(text)

        self.num_units = self.ints[0]
        self.hp_per_unit = self.ints[1]
        self.damage = self.ints[2]
        self.initiative = self.ints[3]

        if self.team == IMMUNE_SYSTEM:
            self.damage += boost

        self.weaknesses = []
        self.immunities = []
        parens_part = re.findall(r"\(.*\)", self.text)
        if parens_part:
            inside_parens = parens_part[0][1:-1]
            for x in inside_parens.split(';'):
                x = x.strip()
                if x.startswith('weak to'):
                    self.weaknesses = aoc_util.split_and_strip_each(x[7:], ',')
                if x.startswith('immune to'):
                    self.immunities = aoc_util.split_and_strip_each(x[9:], ',')

        results = re.findall(r" [a-z]+ damage", self.text)
        self.damage_type = results[0].strip().split()[0]

        # other stuff
        self.target_id = -1
        self.attacker_id = -1
        self.ep = -1
        self.tsp = -1

    def reset(self):
        self.target_id = -1
        self.attacker_id = -1
        self.ep = -1
        self.tsp = -1

    def calc_effective_power(self):
        self.ep = self.num_units * self.damage
        return self.ep

    def calc_target_selection_priority(self):
        self.tsp = -(self.calc_effective_power() * 100 + self.initiative)
        return self.tsp

    def choose_target(self, potential_targets):
        """
        input is a set of Group
        """
        narrowed_targets = []

        # 1st check potential damage
        max_dmg = 0
        for defense_group in potential_targets.values():
            if not defense_group.num_units:
                continue
            dmg = defense_group.check_damage(self.calc_effective_power(), self.damage_type)
            if not dmg:
                continue
            if dmg == max_dmg:
                narrowed_targets.append(defense_group)
            elif dmg > max_dmg:
                max_dmg = dmg
                narrowed_targets = [defense_group]
        if not narrowed_targets:
            # AocLogger.log('cant deal dmg: {}'.format(self))
            return  # cant deal damage
        if len(narrowed_targets) == 1:
            self.target_id = narrowed_targets[0].id
            narrowed_targets[0].attacker_id = self.id
            return

        # 2nd check defender's EP
        potential_targets = narrowed_targets
        narrowed_targets = []
        max_ep = -1
        for defense_group in potential_targets:
            ep = defense_group.calc_effective_power()
            if ep == max_ep:
                narrowed_targets.append(defense_group)
            elif ep > max_ep:
                max_ep = ep
                narrowed_targets = [defense_group]
        if not narrowed_targets:
            raise RuntimeError('this should be impossible?: choose_target')
        if len(narrowed_targets) == 1:
            self.target_id = narrowed_targets[0].id
            narrowed_targets[0].attacker_id = self.id
            return

        # 3rd check defender's initiative
        potential_targets = narrowed_targets
        result = None
        max_init = -1
        for defense_group in potential_targets:
            if defense_group.initiative > max_init:
                max_init = defense_group.initiative
                result = defense_group
        self.target_id = result.id
        result.attacker_id = self.id
        return result

    def log_selection(self):
        if self.target_id > -1:
            AocLogger.log('\t{} {} has selected {}'.format(self.team, self.id, self.target_id))

    def do_attack(self, defense_team):
        """
        Args:
            defense_team (dict of group):

        Returns (int): num enemy units killed
        """
        if self.target_id < 0:
            # cannot attack, this group did not select a target
            return 0

        target_group = defense_team[self.target_id]

        num_killed = target_group.deal_damage(self.calc_effective_power(), self.damage_type)
        AocLogger.log('{} {} ({} left) -> {} {} ({} left): killed {}'.format(
            self.team, self.id, self.num_units,
            self.get_other_team(), self.target_id, target_group.num_units,
            num_killed))
        self.target_id = -1

        return num_killed

    def deal_damage(self, ep, type):
        self.attacker_id = -1
        if type in self.immunities:
            raise RuntimeError('impossible case in deal_damage')
        if type in self.weaknesses:
            ep *= 2
        units_killed = min(ep // self.hp_per_unit, self.num_units)
        self.num_units -= units_killed
        return units_killed

    def check_damage(self, ep, type):
        if self.attacker_id >= 0:
            return 0  # can't have more than one attacker
        if type in self.immunities:
            return 0
        elif type in self.weaknesses:
            return ep * 2
        else:
            return ep

    def get_other_team(self):
        if self.team != INFECTION:
            return INFECTION
        else:
            return IMMUNE_SYSTEM

    def __str__(self):
        return '{} {}: {} left, damage={}'.format(
            self.team, self.id, self.num_units, self.damage)

    def __repr__(self):
        return str(self)



















class AdventOfCode(object):
    """
    https://adventofcode.com/2018
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        puzzle_input = aocd.data

        AocLogger.verbose = False
        self.test_cases(puzzle_input)

        AocLogger.verbose = False
        aoc_util.assert_equal(
            (INFECTION, 15392),
            self.solve_part_1(puzzle_input)
        )
        aoc_util.assert_equal(
            (46, 1092),
            self.solve_part_2(puzzle_input)
        )


    def test_cases(self, puzzle_input):
        # test part 1
        aoc_util.assert_equal(
            (INFECTION, 5216),
            self.solve_part_1(TEST_INPUT))

        # added boost to part 1 (for part 2)
        boost = 1570
        aoc_util.assert_equal(
            (IMMUNE_SYSTEM, 51),
            self.solve_part_1(TEST_INPUT, boost))

        # test stalemate edge case
        aoc_util.assert_equal(
            (INFECTION, -1),
            self.solve_part_1(puzzle_input, 45)
        )

        # test part 2
        aoc_util.assert_equal(
            (1570, 51),
            self.solve_part_2(TEST_INPUT)
        )

        print('all tests passed!{}'.format('\n' * 10))




    def solve_part_1(self, puzzle_input, boost=0):
        """
        14897 is too low...
        """
        AocLogger.log()

        # load all groups
        lines = puzzle_input.split('\n')
        current_team = IMMUNE_SYSTEM
        id_counter = 1
        teams = {}
        all_groups = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith(IMMUNE_SYSTEM):
                continue
            elif line.startswith(INFECTION):
                current_team = INFECTION
                id_counter = 1
                continue

            new_group = Group(current_team, id_counter, line, boost)
            if current_team not in teams:
                teams[current_team] = {}

            teams[current_team][id_counter] = new_group
            all_groups.append(new_group)
            id_counter += 1

        # start the fighting
        winning_army = ''
        while not winning_army:
            AocLogger.log('\n' * 5)

            # log summary
            AocLogger.log('unit summary:')
            for team_name in sorted(teams.keys()):
                AocLogger.log(team_name)
                num_groups_in_army = len(teams[team_name])
                for i in range(1, num_groups_in_army + 1):
                    group = teams[team_name][i]
                    if group.num_units:
                        AocLogger.log('\t{}'.format(group))
            AocLogger.log()

            # target selection phase
            all_groups.sort(key=lambda x: x.calc_target_selection_priority())

            for attacking_group in all_groups:
                defense_team = teams[attacking_group.get_other_team()]

                # choose the target
                attacking_group.choose_target(defense_team)

            # AocLogger.log('selection summary:')
            # for g in all_groups:
            #     g.log_selection()
            # AocLogger.log()

            # attack phase
            all_groups.sort(key=lambda x: -x.initiative)

            total_killed_this_round = 0
            for attacking_group in all_groups:
                # do the attack
                defense_team = teams[attacking_group.get_other_team()]
                num_killed = attacking_group.do_attack(defense_team)
                total_killed_this_round += num_killed

                # todo: count units, check if done
                defense_units_left = 0
                for d_group in defense_team.values():
                    defense_units_left += d_group.num_units
                if not defense_units_left:
                    winning_army = attacking_group.team
                    break

            if total_killed_this_round == 0:
                # handle the edge case where a stalemate is reached
                # return INFECTION as winning team, since we need IMMUNE_SYSTEM to win outright
                result = (INFECTION, -1)
                print('STALEMATE REACHED: {}'.format(result))
                return result

            for g in all_groups:
                g.reset()

        AocLogger.log('{}FINAL SUMMARY'.format('\n' * 5))
        units_left = 0
        for g in all_groups:
            AocLogger.log(g)
            units_left += g.num_units
        AocLogger.log('units_left: {}'.format(units_left))
        return winning_army, units_left


    def solve_part_2(self, puzzle_input):
        """
        Args:
            puzzle_input (string):
                the input

        Returns (tuple of int):
            (min boost, num units left)
        """

        # find lower/upper bound (such that opposite armies win)
        lower_bound_min_boost = 1
        upper_bound_min_boost = 2

        cached_results = {}
        def check_boost(boost):
            if boost not in cached_results:
                print('checking new boost: {}'.format(boost))
                cached_results[boost] = self.solve_part_1(puzzle_input, boost)
                print('new boost result: {}'.format([boost, cached_results[boost]]))
            return cached_results[boost]

        while True:
            war_result = check_boost(upper_bound_min_boost)
            if war_result[0] == IMMUNE_SYSTEM:
                # we have found the upper bound
                break
            else:
                # adjust the bounds
                lower_bound_min_boost = upper_bound_min_boost
                upper_bound_min_boost *= 2

        print('lower_bound_min_boost: {}'.format([lower_bound_min_boost, check_boost(lower_bound_min_boost)]))
        print('upper_bound_min_boost: {}'.format([upper_bound_min_boost, check_boost(upper_bound_min_boost)]))

        # lower loses, upper wins
        # do a binary search algo until lower and upper are next to each other
        while True:
            if upper_bound_min_boost - lower_bound_min_boost == 1:
                break

            mid_point_min_boost = (lower_bound_min_boost + upper_bound_min_boost) // 2
            war_result = check_boost(mid_point_min_boost)
            if war_result[0] == IMMUNE_SYSTEM:
                upper_bound_min_boost = mid_point_min_boost
            else:
                lower_bound_min_boost = mid_point_min_boost

        # now upper is the result
        result = (upper_bound_min_boost, check_boost(upper_bound_min_boost)[1])
        print('part 2 result: {}'.format(result))
        return result















if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




