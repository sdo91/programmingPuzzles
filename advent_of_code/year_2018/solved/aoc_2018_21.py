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

        aoc_util.assert_equal(
            12980435,
            self.solve_part_1(self.puzzle_input)
        )

        aoc_util.assert_equal(
            14431711,
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
        # AocLogger.log(str(self))

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
        result = -1
        opcode_device = OpcodeDevice(num_registers=6)
        opcode_device.verbose = True
        opcode_device.show_hex = True

        # print out the instructions
        for i, instruction in enumerate(self.instructions):
            opcode_device.execute_opcode_name(*instruction)
            print('{}  # (line {})'.format(opcode_device.get_english(self.ip_register), i))
            opcode_device.clear_registers()
        print()

        # print verbose output
        opcode_device.registers[0] = 42  # any value should work
        AocLogger.verbose = True
        opcode_device.show_hex = False
        opcode_device.verbose = AocLogger.verbose

        ip = 0
        x = 0  # just a counter
        state = ''
        while True:
            # check ip range
            if ip >= len(self.instructions):
                assert False

            # check if done
            if ip == 28:
                result = opcode_device.registers[2]
                break

            # # stop after a while
            # if x > 1e6:
            #     break

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

        # decompile
        assert self.code_decompiled('P1') == result
        assert self.code_decompiled('HALT', result) == 1

        return result


    @staticmethod
    def code_decompiled(mode, input_value=42):
        """
        modes:
            'HALT': return number of checks
            'P1': return input for fastest halt
            'P2': return input for slowest halt

        r0: input value
        r1:
        r2: exit value
        r3:
        r4: ip
        r5:
        """
        r0 = input_value
        r1 = 0
        num_checks = 0
        previous_r2 = 0
        seen_values = set()

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
                assert mode == 'HALT'
                return num_checks

            if mode == 'P1':
                return r2

            if num_checks % 1000 == 0 or r2 in seen_values:
                # time to print info
                print('num_checks: {}, previous_r2: {}, r1={:10}, r2={:10}, r3={:10}, r5={:10}'.format(
                    num_checks, previous_r2, r1, r2, r3, r5
                ))

                if r2 in seen_values:
                    # repeating pattern found
                    assert mode == 'P2'
                    return previous_r2

            # prep for next loop
            seen_values.add(r2)
            previous_r2 = r2

            # ip = 5  # (line 30) -> loop back to 6

    def p2(self):
        """
        notes: look for pattern
        """
        result = self.code_decompiled('P2')
        return result










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




