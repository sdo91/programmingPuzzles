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
import math
import traceback

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger

from advent_of_code.year_2018.solved.aoc_2018_16 import OpcodeDevice


### CONSTANTS ###
TEST_INPUT = [
    """
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    6,
    0,
    0,
]

TEST_OUTPUT_2 = [
    0,
    0,
    0,
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
            print(traceback.format_exc())
            self.puzzle_input = 'unable to get input'
        aoc_util.write_input(self.puzzle_input, __file__)

    def run(self):
        start_time = time.time()

        self.run_tests()

        AocLogger.verbose = False
        aoc_util.assert_equal(
            1056,
            self.solve_part_1(self.puzzle_input)
        )

        # AocLogger.verbose = True
        aoc_util.assert_equal(
            10915260,
            self.solve_part_2(self.puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)

        aoc_util.assert_equal(1056, Solver.code_decompiled(989))
        aoc_util.assert_equal(1056, sum(Solver.divisors(989)))

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

        self.instructions = []
        for line in aoc_util.lines(self.text):
            ints = aoc_util.ints(line)
            if line.startswith('#'):
                self.ip_register = ints[0]
            else:
                opcode_name = 'opcode_{}'.format(line.split()[0])
                self.instructions.append((opcode_name, tuple(ints)))

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self, start_val=0, max_num_steps=-1):
        opcode_device = OpcodeDevice(num_registers=6)
        opcode_device.registers[0] = start_val
        opcode_device.verbose = AocLogger.verbose

        ip = 0
        x = 0  # just a counter
        state = ''
        while True:
            # check ip range
            if ip >= len(self.instructions):
                break

            # ip -> register
            opcode_device.registers[self.ip_register] = ip

            # print registers
            instruction = self.instructions[ip]
            if AocLogger.verbose:
                state = '{}: ip={:2} {:35} {}'.format(x, ip, str(opcode_device.registers), instruction)

            # do instruction
            opcode_device.execute_opcode_name(*instruction)
            if AocLogger.verbose:
                state += ' {:18} {}'.format(opcode_device.get_english(self.ip_register), opcode_device.registers)
                print(state)

            # register -> ip
            ip = opcode_device.registers[self.ip_register]

            # inc ip
            ip += 1
            x += 1

        return opcode_device.registers[0]

    def p2(self):
        """
        10551389 too low
        """

        opcode_device = OpcodeDevice(num_registers=6)
        opcode_device.verbose = True

        # print out the instructions
        for i, inst in enumerate(self.instructions):
            if i == 17:
                print()
            opcode_device.execute_opcode_name(*inst)
            print('{}: {}'.format(i, opcode_device.get_english(self.ip_register)))
            opcode_device.clear_registers()
        # assert False

        # after reverse engineering the code, it comes out to this:
        result = sum(self.divisors(10551389))
        return result

    @staticmethod
    def divisors(n):
        results = set()
        i = 1
        root = math.sqrt(n)
        while i <= root:
            if n % i == 0:
                results.add(i)
                results.add(n//i)
            i += 1
        return results

    @staticmethod
    def code_decompiled(input_value):
        """
        r0: result
        r1: if chamber
        r2: inner counter
        r3: ip
        r4: input_value
        r5: outer counter

        calculates the sum of divisors of input_value
        NOTE: input_value for p1 is 989, p2 is 10551389
        """
        text = ''

        # start of program does setup
        r0 = 0
        r4 = input_value
        # returns to line 1

        # line 1-2
        r5 = 1  # (line 1)

        while True:
            r2 = 1  # (line 2)

            # lines 3-11
            while True:
                if (r5 * r2) == r4:  # (lines 3/4)
                    # if factors, add r5 to result
                    r0 += r5  # (line 7)
                    if AocLogger.verbose:
                        if text:
                            text += ' + '
                        text += str(r5)

                r2 += 1  # (line 8)
                if r2 > r4:  # (line 9)
                    break  # (line 10)
                # goto 3

            # lines 12-16
            r5 += 1  # (line 12)
            if r5 > r4:  # (line 13):
                if AocLogger.verbose:
                    text = '{} = {}'.format(text, r0)
                    print(text)
                return r0  # (line 16)
            # goto 2











if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
    print('done')




