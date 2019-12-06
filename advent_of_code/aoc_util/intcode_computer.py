
import typing



class IntcodeComputer(object):

    def __init__(self, initial_memory: typing.List[int]):
        self.i_ptr = 0
        self.outputs = []
        self.memory = initial_memory

    def get_out_idx(self, opcode_index, offset):
        return self.memory[opcode_index + offset]

    def get_param(self, param_modes, opcode_index, offset):
        try:
            param_mode = param_modes[offset - 1]
        except:
            param_mode = 0
        if param_mode == 1:
            param_addr = opcode_index + offset
        else:
            param_addr = self.memory[opcode_index + offset]
        return self.memory[param_addr]

    def run(self, input_value):
        """
        from 2019 day 2
        may need to reuse...
        """
        i = 0

        while True:
            full_opcode = str(self.memory[i])

            opcode = int(full_opcode[-2:])
            param_modes = []

            for c in full_opcode[:-2]:
                param_modes.insert(0, int(c))


            if opcode == 99:
                break

            elif opcode == 1:
                # add
                a = self.get_param(param_modes, i, 1)
                b = self.get_param(param_modes, i, 2)
                out = self.get_out_idx(i, 3)
                self.memory[out] = a + b
                i += 4

            elif opcode == 2:
                # mult
                a = self.get_param(param_modes, i, 1)
                b = self.get_param(param_modes, i, 2)
                out = self.get_out_idx(i, 3)
                self.memory[out] = a * b
                i += 4

            elif opcode == 3:
                out = self.get_out_idx(i, 3)
                self.memory[out] = input_value
                i += 2

            elif opcode == 4:
                self.outputs.append(self.memory[self.memory[i+1]])
                print(self.outputs[-1])
                i += 2

            elif opcode == 5:
                # jump if true
                a = self.get_param(param_modes, i, 1)
                b = self.get_param(param_modes, i, 2)
                if a:
                    i = b
                else:
                    i += 3

            elif opcode == 6:
                # jump if false
                a = self.get_param(param_modes, i, 1)
                b = self.get_param(param_modes, i, 2)
                if not a:
                    i = b
                else:
                    i += 3

            elif opcode == 7:
                # less than
                a = self.get_param(param_modes, i, 1)
                b = self.get_param(param_modes, i, 2)
                out = self.get_out_idx(i, 3)
                self.memory[out] = int(a < b)
                i += 4

            elif opcode == 8:
                # eq
                a = self.get_param(param_modes, i, 1)
                b = self.get_param(param_modes, i, 2)
                out = self.get_out_idx(i, 3)
                self.memory[out] = int(a == b)
                i += 4

            else:
                raise RuntimeError('bad opcode')

        return self.memory

