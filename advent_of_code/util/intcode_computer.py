
import typing

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger


class IntcodeComputer(object):
    """
    from 2019 day 2, 5, 7, 9...
    """

    STATE_READY = 'READY'
    STATE_HALTED = 'HALTED'
    STATE_OUTPUT = 'OUTPUT'
    STATE_INPUT_NEEDED = 'INPUT_NEEDED'

    POSITION_MODE = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE = 2

    def __init__(self, initial_memory, ascii_output_mode=False):
        self.verbose = True
        self.ascii_output_mode = ascii_output_mode

        if isinstance(initial_memory, str):
            self.initial_memory = aoc_util.ints(initial_memory)
        else:
            self.initial_memory = initial_memory

        self.instruction_ptr = 0
        self.memory = []
        self.input_ptr = 0
        self.input_list = []
        self.output_list = []
        self.state = self.STATE_READY

        self.reset()

    def reset(self):
        self.instruction_ptr = 0
        self.memory = self.initial_memory.copy()

        self.input_ptr = 0
        self.input_list = []

        self.output_list = []
        self.state = self.STATE_READY

        self.rel_offset = 0

    def queue_input(self, value: int):
        self.input_list.append(value)
        if not self.is_input_needed():
            self.state = self.STATE_READY

    def queue_input_string(self, string: str):
        for c in string:
            self.queue_input(ord(c))
        self.queue_input(ord('\n'))

    def get_latest_output(self) -> int:
        return self.output_list[-1]

    def get_all_output(self) -> typing.List[int]:
        return self.output_list

    def get_output_size(self) -> int:
        return len(self.output_list)

    def get_output_string(self) -> str:
        return ''.join([chr(x) for x in self.output_list])

    def clear_output(self):
        self.output_list.clear()

    def print_output_string(self):
        output = self.get_output_string()
        if output:
            print(output)
            self.clear_output()

    def get_memory(self) -> typing.List[int]:
        return self.memory

    def is_state(self, desired_state: str) -> bool:
        return self.state == desired_state

    def is_halted(self) -> bool:
        return self.is_state(self.STATE_HALTED)

    def is_input_needed(self):
        return self.input_ptr >= len(self.input_list) and self.get_opcode() == 3

    def get_opcode(self):
        return self.memory[self.instruction_ptr] % 100

    def run_to_halt(self, input_value=None) -> int:
        if input_value is not None:
            self.queue_input(input_value)
        while not self.is_halted():
            self.run()
        return self.get_latest_output()

    def run_to_input_needed(self):
        while not self.is_input_needed():
            if self.is_halted():
                raise RuntimeError('halted')
            self.run()

    def run(self) -> str:
        while True:
            full_opcode = str(self.memory[self.instruction_ptr])

            opcode = self.get_opcode()

            self.param_modes = []
            for c in full_opcode[:-2]:
                self.param_modes.insert(0, int(c))

            z=0  # debug point

            if opcode == 99:
                self.state = self.STATE_HALTED
                break

            elif opcode == 1:
                # add
                a = self._get_value(1)
                b = self._get_value(2)
                out_idx = self._get_idx(3)
                self.memory[out_idx] = a + b
                self.instruction_ptr += 4

            elif opcode == 2:
                # mult
                a = self._get_value(1)
                b = self._get_value(2)
                out_idx = self._get_idx(3)
                self.memory[out_idx] = a * b
                self.instruction_ptr += 4

            elif opcode == 3:
                # input
                if self.input_ptr >= len(self.input_list):
                    self.state = self.STATE_INPUT_NEEDED
                    break

                out_idx = self._get_idx(1)
                self.memory[out_idx] = self.input_list[self.input_ptr]
                self.input_ptr += 1
                self.instruction_ptr += 2

            elif opcode == 4:
                # output
                a = self._get_value(1)
                self.output_list.append(a)
                if self.verbose:
                    if self.ascii_output_mode:
                        print(chr(a), end='')
                    else:
                        # AocLogger.log('intcode output: {}'.format(self.get_latest_output()))
                        pass
                self.state = self.STATE_OUTPUT
                self.instruction_ptr += 2
                break

            elif opcode == 5:
                # jump if true
                a = self._get_value(1)
                b = self._get_value(2)
                if a:
                    self.instruction_ptr = b
                else:
                    self.instruction_ptr += 3

            elif opcode == 6:
                # jump if false
                a = self._get_value(1)
                b = self._get_value(2)
                if not a:
                    self.instruction_ptr = b
                else:
                    self.instruction_ptr += 3

            elif opcode == 7:
                # less than
                a = self._get_value(1)
                b = self._get_value(2)
                out_idx = self._get_idx(3)
                self.memory[out_idx] = int(a < b)
                self.instruction_ptr += 4

            elif opcode == 8:
                # eq
                a = self._get_value(1)
                b = self._get_value(2)
                out_idx = self._get_idx(3)
                self.memory[out_idx] = int(a == b)
                self.instruction_ptr += 4

            elif opcode == 9:
                # adjust rel off
                a = self._get_value(1)
                self.rel_offset += a
                self.instruction_ptr += 2

            else:
                raise RuntimeError('invalid opcode: {}'.format(opcode))

        return self.state

    def _expand_mem(self, index):
        while len(self.memory) <= index:
            self.memory.append(0)

    def _get_idx(self, offset: int, immediate_valid=False) -> int:
        """
        get the index of the parameter in memory
        """
        try:
            param_mode = self.param_modes[offset - 1]
        except IndexError:
            param_mode = 0

        if param_mode == self.POSITION_MODE:
            result_idx = self.memory[self.instruction_ptr + offset]
        elif param_mode == self.IMMEDIATE_MODE and immediate_valid:
            result_idx = self.instruction_ptr + offset
        elif param_mode == self.RELATIVE_MODE:
            result_idx = self.memory[self.instruction_ptr + offset] + self.rel_offset
        else:
            raise RuntimeError('invalid param_mode: {}'.format(param_mode))

        self._expand_mem(result_idx)
        return result_idx

    def _get_value(self, offset: int) -> int:
        return self.memory[self._get_idx(offset, immediate_valid=True)]




