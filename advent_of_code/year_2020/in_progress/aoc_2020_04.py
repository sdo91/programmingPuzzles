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

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger

### CONSTANTS ###
TEST_INPUT = [
    """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
    """, """
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
    """, """
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
    """
]

TEST_OUTPUT_1 = [
    2,
    None,
    None,
]

TEST_OUTPUT_2 = [
    2,
    0,
    4,
]


class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def __init__(self):
        print('starting {}'.format(__file__.split('/')[-1]))

        try:
            self.puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            error_msg = traceback.format_exc()
            print(error_msg)
            self.puzzle_input = 'unable to get input:\n\n{}'.format(error_msg)
        aoc_util.write_input(self.puzzle_input, __file__)

    def run(self):
        start_time = time.time()

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            208,
            self.solve_part_1(self.puzzle_input)
        )

        aoc_util.assert_equal(
            167,
            self.solve_part_2(self.puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        Solver.run_tests()
        aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def solve_part_1(self, text: str):
        solver = Solver(text)

        part_1_result = solver.p1()

        print('part_1_result: {}\n'.format(part_1_result))
        return part_1_result

    def solve_part_2(self, text: str):
        solver = Solver(text)

        part_2_result = solver.p2()

        print('part_2_result: {}\n'.format(part_2_result))
        return part_2_result


class Solver(object):

    def __init__(self, text: str):
        self.text = text.strip()
        AocLogger.log(str(self))

        self.passports = self.text.split('\n\n')

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        """

        """

        required = {
            'byr',
            'iyr',
            'eyr',
            'hgt',
            'hcl',
            'ecl',
            'pid',
            # 'cid',
        }

        result = 0
        for pp in self.passports:

            tokens = aoc_util.tokenize(pp)

            valid_tokens = set()

            for token in tokens:
                key = token.split(':')[0]
                if key in required:
                    valid_tokens.add(key)

            if valid_tokens == required:
                result += 1

        return result

    def p2(self):
        """
        168 wrong
        """
        required = {
            'byr',
            'iyr',
            'eyr',
            'hgt',
            'hcl',
            'ecl',
            'pid',
            # 'cid',
        }

        result = 0
        for pp in self.passports:

            tokens = aoc_util.tokenize(pp)

            valid_tokens = set()

            for token in tokens:
                key = token.split(':')[0]
                if key in required:
                    valid_tokens.add(key)

            if valid_tokens == required:
                is_valid = True
                for token in tokens:
                    if not self.is_valid(token):
                        print('invalid: (failed: {})\n{}\n'.format(token, pp))
                        is_valid = False
                        break
                if is_valid:
                    # print('valid: {}\n'.format(pp))
                    result += 1

        return result

    @classmethod
    def is_valid(cls, text: str):

        key, value = text.split(':')

        if key == 'byr':
            value = int(value)
            return 1920 <= value <= 2002
        elif key == 'iyr':
            value = int(value)
            return 2010 <= value <= 2020
        elif key == 'eyr':
            value = int(value)
            return 2020 <= value <= 2030
        elif key == 'hgt':
            if 'in' in value:
                value = int(value.replace('in', ''))
                return 59 <= value <= 76
            if 'cm' in value:
                value = int(value.replace('cm', ''))
                return 150 <= value <= 193
            return False
        elif key == 'hcl':
            if len(value) != 7:
                return False
            return len(aoc_util.re_find_all_matches('#[0-9a-f]{6}', value)) == 1
        elif key == 'ecl':
            return value in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
        elif key == 'pid':
            if len(value) != 9:
                return False
            return len(aoc_util.re_find_all_matches('[0-9]{9}', value)) == 1
        elif key == 'cid':
            return True
        else:
            raise RuntimeError(key)

        # otherwise
        return False

    @classmethod
    def run_tests(cls):
        assert cls.is_valid('byr:2002')
        assert not cls.is_valid('byr:2003')
        assert cls.is_valid('hgt:60in')
        assert cls.is_valid('hgt:190cm')
        assert not cls.is_valid('hgt:190in')
        assert not cls.is_valid('hgt:190')
        assert cls.is_valid('hcl:#123abc')
        assert not cls.is_valid('hcl:#123abz')
        assert not cls.is_valid('hcl:123abc')
        assert cls.is_valid('ecl:brn')
        assert not cls.is_valid('ecl:wat')
        assert cls.is_valid('pid:000000001')
        assert not cls.is_valid('pid:0123456789')


if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
