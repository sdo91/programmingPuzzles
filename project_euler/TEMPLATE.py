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

addToPath('./prime_tools')

import time
# import primefac
import prime_tools
from itertools import count
from fractions import Fraction


"""

"""
def main():
    print('starting {}'.format(__file__.split('/')[-1]))
    startTime = time.time()

    assertEqual(2 + 2, 4)

    elapsedTime = time.time() - startTime
    print('elapsedTime: {:.2f} s'.format(elapsedTime))
# end main

### HELPER FUNCTIONS ###




def assertEqual(a, b):
    if a != b:
        print('a: {}'.format(a))
        print('b: {}'.format(b))
    assert a == b


if __name__ == '__main__':
    main()
