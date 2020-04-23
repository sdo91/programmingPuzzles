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

        # self.run_tests()

        AocLogger.verbose = False

        # aoc_util.assert_equal(
        #     1056,
        #     self.solve_part_1(self.puzzle_input)
        # )

        AocLogger.verbose = True
        aoc_util.assert_equal(
            0,
            self.solve_part_2(self.puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

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

        self.instructions = []
        for line in aoc_util.lines(self.text):
            ints = aoc_util.ints(line)
            if line.startswith('#'):
                self.ip_register = ints[0]
            else:
                opcode_name = 'opcode_{}'.format(line.split()[0])
                self.instructions.append((opcode_name, tuple(ints)))


        AocLogger.log(str(self))

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self, start_val=0):
        """

        """

        opcode_device = OpcodeDevice(num_registers=6)
        opcode_device.verbose = True
        ip = 0
        state = ''

        opcode_device.registers[0] = start_val
        x=0

        while True:
            # check ip range
            if ip >= len(self.instructions) or x >= 1e5:
                break

            if x > 20 and ip >= 17:
                assert False

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
                # if instruction[-1][-1] == self.ip_register:
                #     state += ' ip jumped!'
                print(state)

            # register -> ip
            ip = opcode_device.registers[self.ip_register]

            # inc ip
            ip += 1
            x += 1
            z=0

        return opcode_device.registers[0]

    def p2(self):
        return self.p1(start_val=1)










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()
    print('done')




