
import re
import typing
from os import path
import time


class AocLogger(object):

    verbose = True

    @classmethod
    def log(cls, msg=None):
        if cls.verbose:
            if msg is None:
                print()
            else:
                print(msg)


def lmap(func, *iterables):
    return list(map(func, *iterables))


def ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"-?\d+", s))  # thanks mserrano!


def positive_ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"\d+", s))  # thanks mserrano!


def floats(s: str) -> typing.List[float]:
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))


def positive_floats(s: str) -> typing.List[float]:
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))


def words(s: str) -> typing.List[str]:
    return re.findall(r"[a-zA-Z]+", s)


def split_and_strip_each(s: str, c: str) -> typing.List[str]:
    """
    split the string on the char, and strip each item in the resulting list
    """
    return lmap(str.strip, s.split(c))


def assert_equal(expected, actual):
    if expected != actual:
        print('expected: {}'.format(expected))
        print('actual: {}'.format(actual))
    time.sleep(0.1)
    assert expected == actual


def write_input(text, file_path):
    out_dir = path.dirname(file_path)
    while not path.basename(out_dir).startswith('advent'):
        out_dir = path.realpath(path.join(out_dir, '..'))

    with open(out_dir + '/input.txt', 'w') as outfile:
        outfile.write(text)


def run_tests(function, test_inputs, test_outputs):
    AocLogger.log('\nrunning test cases')
    num_tests_passed = 0

    for i in range(len(test_inputs)):
        test_in = test_inputs[i]
        test_out = test_outputs[i]

        if type(test_in) == str:
            test_in = test_in.strip()
            if test_in == '':
                continue

        print('\nindex: {}'.format(i))

        # do the test
        assert_equal(
            test_out,
            function(test_in)
        )

        num_tests_passed += 1

    AocLogger.log('\npassed all test cases ({} tests)'.format(num_tests_passed))
    AocLogger.log('\n' * 5)


def manhatten_dist(a, b):
    result = 0
    for i in range(len(a)):
        result += abs(a[i] - b[i])
    return result


def re_find_all_matches(pattern, text):
    matcher = re.compile(pattern)
    return [match.group() for match in matcher.finditer(text)]










# todo: move intcode logic to a class

def get_out_idx(codes, opcode_index, offset):
    return codes[opcode_index + offset]

def get_param(codes, param_modes, opcode_index, offset):
    try:
        param_mode = param_modes[offset - 1]
    except:
        param_mode = 0
    if param_mode == 1:
        result = codes[opcode_index + offset]
    else:
        result = codes[codes[opcode_index + offset]]
    return result

def run_intcode(codes_list: typing.List[int], input_value):
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
            a = get_param(codes_list, param_modes, i, 1)
            b = get_param(codes_list, param_modes, i, 2)
            out = get_out_idx(codes_list, i, 3)
            codes_list[out] = a + b
            i += 4

        elif opcode == 2:
            # mult
            a = get_param(codes_list, param_modes, i, 1)
            b = get_param(codes_list, param_modes, i, 2)
            out = get_out_idx(codes_list, i, 3)
            codes_list[out] = a * b
            i += 4

        elif opcode == 3:
            out = get_out_idx(codes_list, i, 3)
            codes_list[out] = input_value
            i += 2

        elif opcode == 4:
            print(codes_list[codes_list[i+1]])
            i += 2

        elif opcode == 5:
            # jump if true
            a = get_param(codes_list, param_modes, i, 1)
            b = get_param(codes_list, param_modes, i, 2)
            if a:
                i = b
            else:
                i += 3

        elif opcode == 6:
            # jump if false
            a = get_param(codes_list, param_modes, i, 1)
            b = get_param(codes_list, param_modes, i, 2)
            if not a:
                i = b
            else:
                i += 3

        elif opcode == 7:
            # less than
            a = get_param(codes_list, param_modes, i, 1)
            b = get_param(codes_list, param_modes, i, 2)
            out = get_out_idx(codes_list, i, 3)
            codes_list[out] = int(a < b)
            i += 4

        elif opcode == 8:
            # eq
            a = get_param(codes_list, param_modes, i, 1)
            b = get_param(codes_list, param_modes, i, 2)
            out = get_out_idx(codes_list, i, 3)
            codes_list[out] = int(a == b)
            i += 4

        else:
            raise RuntimeError('bad opcode')

    return codes_list



