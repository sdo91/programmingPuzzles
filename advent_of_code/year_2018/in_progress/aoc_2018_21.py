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

    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    0,
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
        #     12980435,
        #     self.solve_part_1(self.puzzle_input)
        # )

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

    def p1(self):
        """
        notes:
            goal: halt fast
                find lowest r0 to halt fast
            r0 only used by line 28
        """
        opcode_device = OpcodeDevice(num_registers=6)
        opcode_device.verbose = True
        opcode_device.show_hex = True

        # print out the instructions
        for i, instruction in enumerate(self.instructions):
            opcode_device.execute_opcode_name(*instruction)
            print('{}  # (line {})'.format(opcode_device.get_english(self.ip_register), i))
            opcode_device.clear_registers()
        print()

        # decompile
        assert self.code_decompiled(12980435) == 1

        # print verbose output
        opcode_device.registers[0] = 12980435
        AocLogger.verbose = True
        opcode_device.show_hex = False
        opcode_device.verbose = AocLogger.verbose

        ip = 0
        x = 0  # just a counter
        state = ''
        while True:
            # check ip range
            if ip >= len(self.instructions):
                break

            # stop after a while
            if x > 1e6:
                break

            # ip -> register
            opcode_device.registers[self.ip_register] = ip

            # print registers
            instruction = self.instructions[ip]
            if AocLogger.verbose:
                state = '{:}: ip={:2} {:45} {:35}'.format(x, ip, str(opcode_device.registers), str(instruction))

            # do instruction
            opcode_device.execute_opcode_name(*instruction)
            if AocLogger.verbose:
                state += ' {:20} {}'.format(opcode_device.get_english(self.ip_register), opcode_device.registers)
                print(state)

            # register -> ip
            ip = opcode_device.registers[self.ip_register]

            # increment
            ip += 1
            x += 1

        return opcode_device.registers[0]

    @staticmethod
    def code_decompiled(input_value):
        """
        r0: input value
        r1:
        r2: exit value
        r3:
        r4: ip
        r5:

        hex:
        65536 -> 0x10000
        255 -> 0xff
        """
        # ip = 0
        r0 = input_value
        num_checks = 0

        # lines 0-5 just test bitwise AND
        while True:
            r2 = 123  # (line 0)
            r2 = r2 & 456  # (line 1)
            if r2 == 72:
                break

        r2 = 0  # (line 5)

        while True:
            r5 = r2 | 65536  # (line 6)
            r2 = 16123384  # (line 7)

            while True:
                r3 = r5 & 255  # (line 8)
                r2 = r2 + r3  # (line 9)
                r2 = r2 & 16777215  # (line 10)
                r2 = r2 * 65899  # (line 11)
                r2 = r2 & 16777215  # (line 12)

                '''
                r3 = (256 > r5)  # (line 13)
                ip = r3 + ip  # (line 14)
                ip = ip + 1  # (line 15)
                ip = 27  # (line 16)
                '''
                if 256 > r5:
                    # r3=1 -> skip 15 -> goto 16 -> 28
                    break

                r3 = 0  # (line 17)

                while True:
                    r1 = r3 + 1  # (line 18)
                    r1 = r1 * 256  # (line 19)

                    '''
                    r1 = (r1 > r5)  # (line 20)
                    ip = r1 + ip  # (line 21)
                    ip = ip + 1  # (line 22)
                    ip = 25  # (line 23) -> goto 26
                    '''
                    if r1 > r5:
                        break

                    r3 = r3 + 1  # (line 24)

                    # ip = 17  # (line 25) -> loop back to 18

                r5 = r3  # (line 26)

                # ip = 7  # (line 27) -> loop back to 8

            '''
            r3 = (r2 == r0)  # (line 28)
            ip = r3 + ip  # (line 29)
            '''
            num_checks += 1
            if r2 == r0:
                return num_checks

            # ip = 5  # (line 30) -> loop back to 6

    def p2(self):
        """
        notes:
            goal: halt fast
                find lowest r0 to halt fast
            r0 only used by line 28
        """
        opcode_device = OpcodeDevice(num_registers=6)
        opcode_device.verbose = True
        opcode_device.show_hex = True

        # print out the instructions
        for i, instruction in enumerate(self.instructions):
            opcode_device.execute_opcode_name(*instruction)
            print('{}  # (line {})'.format(opcode_device.get_english(self.ip_register), i))
            opcode_device.clear_registers()
        print()

        # decompile
        assert self.code_decompiled(12980435) == 1

        # print verbose output
        opcode_device.registers[0] = 12980435
        AocLogger.verbose = True
        opcode_device.show_hex = False
        opcode_device.verbose = AocLogger.verbose

        ip = 0
        x = 0  # just a counter
        state = ''
        while True:
            # check ip range
            if ip >= len(self.instructions):
                break

            # stop after a while
            if x > 1e6:
                break

            # ip -> register
            opcode_device.registers[self.ip_register] = ip

            # print registers
            instruction = self.instructions[ip]
            if AocLogger.verbose:
                state = '{:}: ip={:2} {:45} {:35}'.format(x, ip, str(opcode_device.registers), str(instruction))

            # do instruction
            opcode_device.execute_opcode_name(*instruction)
            if AocLogger.verbose:
                state += ' {:20} {}'.format(opcode_device.get_english(self.ip_register), opcode_device.registers)
                print(state)

            # register -> ip
            ip = opcode_device.registers[self.ip_register]

            # increment
            ip += 1
            x += 1

        return opcode_device.registers[0]










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




