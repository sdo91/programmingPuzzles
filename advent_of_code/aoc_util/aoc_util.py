
import re
import typing
from os import path
import time
import pprint
import json





class AocLogger(object):

    verbose = True

    @classmethod
    def log(cls, msg=None):
        if cls.verbose:
            if msg is None:
                print()
            else:
                print(msg)

    @classmethod
    def log_dict(cls, my_dict, name='', force_verbose=False):
        if cls.verbose or force_verbose:
            if name:
                print('{}:'.format(name))
            pprint.pprint(my_dict)
            # print(json.dumps(my_dict, indent=2))
            print()





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


def lines(s: str) -> typing.List[str]:
    return s.strip().split('\n')


def stripped_lines(s: str) -> typing.List[str]:
    return split_and_strip_each(s.strip(), '\n')


def split_and_strip_each(string: str, delim: str) -> typing.List[str]:
    """
    split the string on the char, and strip each item in the resulting list
    """
    return lmap(str.strip, string.split(delim))


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
    AocLogger.log('\nrunning test cases ({})'.format(str(function)))
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


def tuple_add(a, b):
    return tuple(i + j for i, j in zip(a, b))













