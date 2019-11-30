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

from functools import total_ordering
import aocd
import re
import parse
import typing


import aoc_util



class Group(object):

    def __init__(self, team, id, text):
        self.team = team
        self.id = id
        self.text = text.lower()
        # print(self.text)

        self.target_id = -1
        self.attacker_id = -1

        self.ints = aoc_util.ints(text)

        self.num_units = self.ints[0]
        self.hit_points_per_unit = self.ints[1]
        self.damage = self.ints[2]
        self.initiative = self.ints[3]

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

        self.tsp = -1

    def calc_effective_power(self):
        self.ep = self.num_units * self.damage
        return self.ep

    def calc_target_selection_priority(self):
        self.tsp = -(self.calc_effective_power() * 100 + self.initiative)
        return self.tsp

    def attack(self, defense_team):
        print('{} {} -> {} {}'.format(
            self.team, self.id, self.get_other_team(), self.target_id))

    def choose_target(self, potential_targets):
        narrowed_targets = []

        # 1st check potential damage
        max_dmg = 0
        for defense_group in potential_targets:
            dmg = defense_group.check_damage(self.calc_effective_power(), self.damage_type)
            if dmg == max_dmg:
                narrowed_targets.append(defense_group)
            elif dmg > max_dmg:
                max_dmg = dmg
                narrowed_targets = [defense_group]
        if not narrowed_targets:
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
            print('this should be impossible?')
            assert False
            return
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
        if self.team != 'Infection':
            return 'Infection'
        else:
            return 'Immune'

    def __str__(self):
        return '{} {}: {}, {}'.format(
            self.team, self.id, self.ints, self.text)

    def __repr__(self):
        return str(self)


class AdventOfCode(object):
    """
    https://adventofcode.com/2018
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        puzzle_input = aocd.data

        self.test_part_1()
        # self.solve_part_1(puzzle_input)



    def test_part_1(self):
        test_input = '''
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4        
'''
        self.solve_part_1(test_input)


    def solve_part_1(self, puzzle_input):
        print()

        # load all groups
        lines = puzzle_input.split('\n')
        current_team = 'Immune'
        id_counter = 1
        teams = {}
        all_groups = []
        for line in lines:
            line = line.strip()
            if line in {'', 'Immune System:'}:
                continue
            elif line == 'Infection:':
                current_team = 'Infection'
                id_counter = 1
                continue

            new_group = Group(current_team, id_counter, line)
            id_counter += 1
            if current_team not in teams:
                teams[current_team] = []

            teams[current_team].append(new_group)
            all_groups.append(new_group)

        # start the fighting
        while True:

            # todo: reset all

            # for each army
            for key in teams:
                # target selection phase
                attack_team = teams[key]
                defense_team = teams[attack_team[0].get_other_team()]

                # choose order
                attack_team.sort(key=lambda x: x.calc_target_selection_priority())

                for attack_group in attack_team:
                    # choose the target
                    attack_group.choose_target(defense_team)

            # order for attack
            all_groups.sort(key=lambda x: -x.initiative)

            for group in all_groups:
                # do the attack
                defense_team = teams[group.get_other_team()]
                group.attack(defense_team)

            z = 5
            break














if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




