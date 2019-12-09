
import typing
from aoc_util.aoc_util import AocLogger


class IntcodeComputer(object):

    STATE_READY = 'READY'
    STATE_HALTED = 'HALTED'
    STATE_OUTPUT = 'OUTPUT'

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

    def queue_input(self, value: int):
        self.input_list.append(value)

    def get_latest_output(self) -> int:
        return self.output_list[-1]

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

            opcode = int(full_opcode[-2:])

            param_modes = []
            for c in full_opcode[:-2]:
                param_modes.insert(0, int(c))

            if opcode == 99:
                self.state = self.STATE_HALTED
                break

            elif opcode == 1:
                # add
                a = self._get_param(param_modes, 1)
                b = self._get_param(param_modes, 2)
                out = self._get_out_idx(3)
                self.memory[out] = a + b
                self.instruction_ptr += 4

            elif opcode == 2:
                # mult
                a = self._get_param(param_modes, 1)
                b = self._get_param(param_modes, 2)
                out = self._get_out_idx(3)
                self.memory[out] = a * b
                self.instruction_ptr += 4

            elif opcode == 3:
                # input
                out = self._get_out_idx(1)
                self.memory[out] = self.input_list[self.input_ptr]
                self.input_ptr += 1
                self.instruction_ptr += 2

            elif opcode == 4:
                # output
                a = self._get_param(param_modes, 1)
                self.output_list.append(a)
                AocLogger.log('intcode output: {}'.format(self.output_list[-1]))
                self.state = self.STATE_OUTPUT
                self.instruction_ptr += 2
                break

            elif opcode == 5:
                # jump if true
                a = self._get_param(param_modes, 1)
                b = self._get_param(param_modes, 2)
                if a:
                    self.instruction_ptr = b
                else:
                    self.instruction_ptr += 3

            elif opcode == 6:
                # jump if false
                a = self._get_param(param_modes, 1)
                b = self._get_param(param_modes, 2)
                if not a:
                    self.instruction_ptr = b
                else:
                    self.instruction_ptr += 3

            elif opcode == 7:
                # less than
                a = self._get_param(param_modes, 1)
                b = self._get_param(param_modes, 2)
                out = self._get_out_idx(3)
                self.memory[out] = int(a < b)
                self.instruction_ptr += 4

            elif opcode == 8:
                # eq
                a = self._get_param(param_modes, 1)
                b = self._get_param(param_modes, 2)
                out = self._get_out_idx(3)
                self.memory[out] = int(a == b)
                self.instruction_ptr += 4

            else:
                raise RuntimeError('invalid opcode: {}'.format(opcode))

        return self.state

    def _get_out_idx(self, offset: int) -> int:
        return self.memory[self.instruction_ptr + offset]

    def _get_param(self, param_modes: typing.List[int], offset: int) -> int:
        POSITION_MODE = 0
        IMMEDIATE_MODE = 1

        try:
            param_mode = param_modes[offset - 1]
        except IndexError:
            param_mode = 0

        if param_mode == POSITION_MODE:
            param_addr = self.memory[self.instruction_ptr + offset]
        elif param_mode == IMMEDIATE_MODE:
            param_addr = self.instruction_ptr + offset
        else:
            raise RuntimeError('invalid param_mode: {}'.format(param_mode))

        return self.memory[param_addr]




