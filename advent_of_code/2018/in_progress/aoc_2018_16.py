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
from bidict import bidict

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger


### CONSTANTS ###
TEST_INPUT = [
    """
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    1,
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

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))
        start_time = time.time()

        try:
            puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            print(traceback.format_exc())
            puzzle_input = 'unable to get input'
        aoc_util.write_input(puzzle_input, __file__)

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            614,
            self.solve_part_1(puzzle_input)
        )

        aoc_util.assert_equal(
            656,
            self.solve_part_2(puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        # aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def solve_part_1(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_1_result = solver.p1()

        print('part_1_result: {}\n'.format(part_1_result))
        return part_1_result

    def solve_part_2(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_2_result = solver.p2()

        print('part_2_result: {}\n'.format(part_2_result))
        return part_2_result








class OpcodeDevice(object):

    def __init__(self):
        self.registers = [0] * 4
        self.opcodes_by_name = bidict()

    def get_opcode_method_names(self):
        return [x for x in dir(self) if x.startswith('opcode_') and callable(getattr(self, x))]

    def clear_registers(self):
        for x in range(len(self.registers)):
            self.registers[x] = 0

    def execute_instruction(self, text):
        tokens = aoc_util.ints(text)
        opcode = tokens[0]
        abc = tokens[1:]
        opcode_name = self.opcodes_by_name.inv[opcode]
        opcode_method = getattr(self, opcode_name)
        opcode_method(*abc)

    def opcode_addr(self, a, b, c):
        """
        addr (add register)
        stores into register C the result of adding register A and register B.
        """
        self.registers[c] = self.registers[a] + self.registers[b]

    def opcode_addi(self, a, b, c):
        """
        addi (add immediate)
        stores into register C the result of adding register A and value B.
        """
        self.registers[c] = self.registers[a] + b

    def opcode_mulr(self, a, b, c):
        """
        mulr (multiply register)
        stores into register C the result of multiplying register A and register B.
        """
        self.registers[c] = self.registers[a] * self.registers[b]

    def opcode_muli(self, a, b, c):
        """
        muli (multiply immediate)
        stores into register C the result of multiplying register A and value B.
        """
        self.registers[c] = self.registers[a] * b

    def opcode_banr(self, a, b, c):
        """
        banr (bitwise AND register)
        stores into register C the result of the bitwise AND of register A and register B.
        """
        self.registers[c] = self.registers[a] & self.registers[b]

    def opcode_bani(self, a, b, c):
        """
        bani (bitwise AND immediate)
        stores into register C the result of the bitwise AND of register A and value B.
        """
        self.registers[c] = self.registers[a] & b

    def opcode_borr(self, a, b, c):
        """
        borr (bitwise OR register)
        stores into register C the result of the bitwise OR of register A and register B.
        """
        self.registers[c] = self.registers[a] | self.registers[b]

    def opcode_bori(self, a, b, c):
        """
        bori (bitwise OR immediate)
        stores into register C the result of the bitwise OR of register A and value B.
        """
        self.registers[c] = self.registers[a] | b

    def opcode_setr(self, a, b, c):
        """
        setr (set register)
        copies the contents of register A into register C. (Input B is ignored.)
        """
        self.registers[c] = self.registers[a]

    def opcode_seti(self, a, b, c):
        """
        seti (set immediate)
        stores value A into register C. (Input B is ignored.)
        """
        self.registers[c] = a

    def opcode_gtir(self, a, b, c):
        """
        gtir (greater-than immediate/register)
        sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
        """
        self.registers[c] = int(a > self.registers[b])

    def opcode_gtri(self, a, b, c):
        """
        gtri (greater-than register/immediate)
        sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
        """
        self.registers[c] = int(self.registers[a] > b)

    def opcode_gtrr(self, a, b, c):
        """
        gtrr (greater-than register/register)
        sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
        """
        self.registers[c] = int(self.registers[a] > self.registers[b])

    def opcode_eqir(self, a, b, c):
        """
        eqir (equal immediate/register)
        sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
        """
        self.registers[c] = int(a == self.registers[b])

    def opcode_eqri(self, a, b, c):
        """
        eqri (equal register/immediate)
        sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
        """
        self.registers[c] = int(self.registers[a] == b)

    def opcode_eqrr(self, a, b, c):
        """
        eqrr (equal register/register)
        sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
        """
        self.registers[c] = int(self.registers[a] == self.registers[b])



class Sample(object):

    def __init__(self, lines):
        self.before = aoc_util.ints(lines[0])
        self.instruction = aoc_util.ints(lines[1])
        self.after = aoc_util.ints(lines[2])
        self.text = '\n'.join(lines)
        self.possible_opcode_names = set()

    def __repr__(self):
        return self.text

    def get_abc(self):
        return self.instruction[1:]







class Solver(object):

    def __init__(self, text: str):
        self.text = text.strip()
        self.text_parts = self.text.split('\n\n\n')

        self.samples_list = self.parse_samples(self.text_parts[0])

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def parse_samples(self, text):
        result = []
        lines_iter = iter(aoc_util.stripped_lines(text))
        num_blank_lines = 0

        try:
            while True:
                line = next(lines_iter)
                if not line:
                    # skip blank lines
                    num_blank_lines += 1
                    if num_blank_lines > 1:

                        print(result[0])
                        print(result[-1])

                        return result
                    continue
                else:
                    num_blank_lines = 0

                if 'Before' in line:
                    sample_lines = [line, next(lines_iter), next(lines_iter)]
                    result.append(Sample(sample_lines))
                else:
                    assert False

        except StopIteration:
            return result

    def p1(self):
        device = OpcodeDevice()
        opcode_method_names = [x for x in dir(OpcodeDevice) if x.startswith('opcode')]
        num_3_plus = 0

        for sample in self.samples_list:
            for name in opcode_method_names:
                device.registers = sample.before.copy()
                method = getattr(device, name)
                method(*sample.get_abc())
                if device.registers == sample.after:
                    sample.possible_opcode_names.add(name)
            if len(sample.possible_opcode_names) >= 3:
                num_3_plus += 1

        return num_3_plus

    def p2(self):
        device = OpcodeDevice()

        # figure out opcodes
        unassigned_opcode_names = device.get_opcode_method_names()
        for sample in self.samples_list:
            for name in unassigned_opcode_names:
                device.registers = sample.before.copy()
                method = getattr(device, name)
                method(*sample.get_abc())
                if device.registers == sample.after:
                    sample.possible_opcode_names.add(name)

            if len(sample.possible_opcode_names) == 1:
                # found a match
                opcode_name = sample.possible_opcode_names.pop()
                opcode = sample.instruction[0]

                device.opcodes_by_name[opcode_name] = opcode
                unassigned_opcode_names.remove(opcode_name)
                print('opcode {} is {}'.format(opcode, opcode_name))

        assert len(device.opcodes_by_name) == 16

        # run program
        program_lines = aoc_util.stripped_lines(self.text_parts[1].strip())
        print(program_lines[0])
        print(program_lines[-1])
        device.clear_registers()

        for line in program_lines:
            device.execute_instruction(line)

        return device.registers[0]










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




