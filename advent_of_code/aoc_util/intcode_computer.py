
import typing



class IntcodeComputer(object):

    def __init__(self):
        self.i_ptr = 0
        self.output = []
        # self.memory = []

    def get_out_idx(self, codes, opcode_index, offset):
        return codes[opcode_index + offset]

    def get_param(self, codes, param_modes, opcode_index, offset):
        try:
            param_mode = param_modes[offset - 1]
        except:
            param_mode = 0
        if param_mode == 1:
            result = codes[opcode_index + offset]
        else:
            result = codes[codes[opcode_index + offset]]
        return result

    def run_intcode(self, codes_list: typing.List[int], input_value):
        """
        from 2019 day 2
        may need to reuse...
        """
        i = 0

        while True:
            full_opcode = str(codes_list[i])

            opcode = int(full_opcode[-2:])
            param_modes = []

            for c in full_opcode[:-2]:
                param_modes.insert(0, int(c))


            if opcode == 99:
                break

            elif opcode == 1:
                # add
                a = self.get_param(codes_list, param_modes, i, 1)
                b = self.get_param(codes_list, param_modes, i, 2)
                out = self.get_out_idx(codes_list, i, 3)
                codes_list[out] = a + b
                i += 4

            elif opcode == 2:
                # mult
                a = self.get_param(codes_list, param_modes, i, 1)
                b = self.get_param(codes_list, param_modes, i, 2)
                out = self.get_out_idx(codes_list, i, 3)
                codes_list[out] = a * b
                i += 4

            elif opcode == 3:
                out = self.get_out_idx(codes_list, i, 3)
                codes_list[out] = input_value
                i += 2

            elif opcode == 4:
                print(codes_list[codes_list[i+1]])
                i += 2

            elif opcode == 5:
                # jump if true
                a = self.get_param(codes_list, param_modes, i, 1)
                b = self.get_param(codes_list, param_modes, i, 2)
                if a:
                    i = b
                else:
                    i += 3

            elif opcode == 6:
                # jump if false
                a = self.get_param(codes_list, param_modes, i, 1)
                b = self.get_param(codes_list, param_modes, i, 2)
                if not a:
                    i = b
                else:
                    i += 3

            elif opcode == 7:
                # less than
                a = self.get_param(codes_list, param_modes, i, 1)
                b = self.get_param(codes_list, param_modes, i, 2)
                out = self.get_out_idx(codes_list, i, 3)
                codes_list[out] = int(a < b)
                i += 4

            elif opcode == 8:
                # eq
                a = self.get_param(codes_list, param_modes, i, 1)
                b = self.get_param(codes_list, param_modes, i, 2)
                out = self.get_out_idx(codes_list, i, 3)
                codes_list[out] = int(a == b)
                i += 4

            else:
                raise RuntimeError('bad opcode')

        return codes_list

