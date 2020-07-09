
import os
from os import path


def read_input(solution_path):
    INPUTS_DIR = 'inputs'

    solution_dir = path.dirname(path.realpath(solution_path))
    basename = path.basename(solution_path)
    digits = ''.join([x for x in basename if x.isdigit()])

    current_dir = solution_dir
    while True:
        # check for INPUTS_DIR
        if INPUTS_DIR in os.listdir(current_dir):

            # found INPUTS_DIR
            inputs_dir = path.join(current_dir, INPUTS_DIR)
            for filename in os.listdir(inputs_dir):
                if digits in filename:

                    # found matching input file
                    input_path = path.join(inputs_dir, filename)
                    with open(input_path) as infile:
                        result = infile.read()
                        return result

            # digits not found
            raise RuntimeError('digits not found: {}'.format(digits))

        # go up one dir
        current_dir = path.normpath(path.join(current_dir, '..'))
        if current_dir == '/':
            raise RuntimeError('dir not found: {}'.format(INPUTS_DIR))





