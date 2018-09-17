#!/usr/bin/env python

from __future__ import division

import time
import primefac
from itertools import count

from fractions import gcd

"""
Permuted multiples
Problem 52 

It can be seen that the number, 125874, and its double, 251748, 
contain exactly the same digits, but in a different order.

Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, 
contain the same digits.
"""
def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()

    # goal = 2
    goal = 6


    for lastNum in count(goal, goal):

        # check if a set
        x = int(lastNum / goal)

        if x % 1e5 == 0:
            print x

        digits_1x = getSortedDigits(x)

        allDigitsMatch = True
        for N in xrange(2, goal + 1):
            digits_Nx = getSortedDigits(N * x)
            if digits_Nx != digits_1x:
                allDigitsMatch = False
                break
        if allDigitsMatch:
            print 'match found:'
            for N in xrange(1, goal + 1):
                print N * x,
            print
            break




    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

### HELPER FUNCTIONS ###

def getSortedDigits(x):
    result = ''.join(sorted(str(x)))
    firstNonZero = 0
    while result[firstNonZero] == '0':
        firstNonZero += 1
    return result[firstNonZero:]

def assertEqual(a, b):
    if a != b:
        print 'a: {}'.format(a)
        print 'b: {}'.format(b)
    assert a == b


if __name__ == '__main__':
    main()
