
import typing
from aoc_util.aoc_util import AocLogger


class IntcodeComputer(object):

    STATE_READY = 'READY'
    STATE_HALTED = 'HALTED'
    STATE_OUTPUT = 'OUTPUT'

    POSITION_MODE = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE = 2

    def __init__(self, initial_memory: typing.List[int]):
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

    def get_latest_output(self) -> int:
        return self.output_list[-1]

    def get_all_output(self) -> typing.List[int]:
        return self.output_list

    def is_halted(self) -> bool:
        return self.state == self.STATE_HALTED

    def run_to_halt(self, input_value=None) -> int:
        if input_value is not None:
            self.queue_input(input_value)
        while not self.is_halted():
            self.run()
        return self.get_latest_output()

    def run(self) -> str:
        """
        from 2019 day 2, 5, 7
        may need to reuse...
        """

        while True:
            full_opcode = str(self.memory[self.instruction_ptr])

            if full_opcode == '203':
                z=0

            opcode = int(full_opcode[-2:])

            param_modes = []
            for c in full_opcode[:-2]:
                param_modes.insert(0, int(c))
            self.param_modes = param_modes

            z=0

            if opcode == 99:
                self.state = self.STATE_HALTED
                break

            elif opcode == 1:
                # add
                a = self._get_value(param_modes, 1)
                b = self._get_value(param_modes, 2)
                out = self._get_idx(3)
                self.memory[out] = a + b
                self.instruction_ptr += 4

            elif opcode == 2:
                # mult
                a = self._get_value(param_modes, 1)
                b = self._get_value(param_modes, 2)
                out = self._get_idx(3)
                self.memory[out] = a * b
                self.instruction_ptr += 4

            elif opcode == 3:
                # input
                out = self._get_idx(1)
                self.memory[out] = self.input_list[self.input_ptr]
                self.input_ptr += 1
                self.instruction_ptr += 2

            elif opcode == 4:
                # output
                a = self._get_value(param_modes, 1)
                self.output_list.append(a)
                print('intcode output: {}'.format(self.output_list[-1]))
                self.state = self.STATE_OUTPUT
                self.instruction_ptr += 2
                break

            elif opcode == 5:
                # jump if true
                a = self._get_value(param_modes, 1)
                b = self._get_value(param_modes, 2)
                if a:
                    self.instruction_ptr = b
                else:
                    self.instruction_ptr += 3

            elif opcode == 6:
                # jump if false
                a = self._get_value(param_modes, 1)
                b = self._get_value(param_modes, 2)
                if not a:
                    self.instruction_ptr = b
                else:
                    self.instruction_ptr += 3

            elif opcode == 7:
                # less than
                a = self._get_value(param_modes, 1)
                b = self._get_value(param_modes, 2)
                out = self._get_idx(3)
                self.memory[out] = int(a < b)
                self.instruction_ptr += 4

            elif opcode == 8:
                # eq
                a = self._get_value(param_modes, 1)
                b = self._get_value(param_modes, 2)
                out = self._get_idx(3)
                self.memory[out] = int(a == b)
                self.instruction_ptr += 4

            elif opcode == 9:
                # adjust rel off
                a = self._get_value(param_modes, 1)
                self.rel_offset += a
                self.instruction_ptr += 2

            else:
                raise RuntimeError('invalid opcode: {}'.format(opcode))

        return self.state

    def _expand_mem(self, index):
        while len(self.memory) <= index:
            self.memory.append(0)

    def _get_idx(self, offset: int) -> int:
        """
        write_index is the index we will be writing to
        """
        try:
            param_mode = self.param_modes[offset - 1]
        except IndexError:
            param_mode = 0

        if param_mode == self.POSITION_MODE:
            write_index = self.memory[self.instruction_ptr + offset]
        elif param_mode == self.RELATIVE_MODE:
            write_index = self.memory[self.instruction_ptr + offset] + self.rel_offset
        else:
            raise RuntimeError('invalid output param_mode: {}'.format(param_mode))

        self._expand_mem(write_index)
        return write_index

    def _get_value(self, param_modes: typing.List[int], offset: int) -> int:
        try:
            param_mode = param_modes[offset - 1]
        except IndexError:
            param_mode = 0

        if param_mode == self.POSITION_MODE:
            param_addr = self.memory[self.instruction_ptr + offset]
        elif param_mode == self.IMMEDIATE_MODE:
            param_addr = self.instruction_ptr + offset
        elif param_mode == self.RELATIVE_MODE:
            param_addr = self.memory[self.instruction_ptr + offset] + self.rel_offset
        else:
            raise RuntimeError('invalid param_mode: {}'.format(param_mode))

        self._expand_mem(param_addr)
        return self.memory[param_addr]




