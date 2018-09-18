#!/usr/bin/env python

from __future__ import division

import time
import primefac
from itertools import count




factorial_map = None


"""
Combinatoric selections
Problem 53 
There are exactly ten ways of selecting three from five, 12345:

123, 124, 125, 134, 135, 145, 234, 235, 245, and 345

In combinatorics, we use the notation, 5C3 = 10.

In general,

nCr =	
n!
r!(n-r)!
,where r <= n, n! = n*(n-1)*...*3*2*1, and 0! = 1.
It is not until n = 23, that a value exceeds one-million: 23C10 = 1144066.

How many, not necessarily distinct, values of  nCr, for 1 <= n <= 100, are greater than one-million?
"""
def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()

    global factorial_map
    print doFactorials(10)
    factorial_map = doFactorials(100)

    assertEqual(n_choose_r(5, 3), 10)
    assertEqual(n_choose_r(23, 9), 817190)
    assertEqual(n_choose_r(23, 10), 1144066)
    assertEqual(n_choose_r(23, 11), 1352078)
    assertEqual(n_choose_r(23, 12), 1352078)
    assertEqual(n_choose_r(23, 13), 1144066)
    assertEqual(n_choose_r(23, 14), 817190)

    # for r in range(9, 15):
    #     value = n_choose_r(23, r)
    #     print '{}c{} = {}'.format(23, r, value)


    # maxN = 23
    maxN = 100
    numValuesOver1m = 0

    for N in range(1, maxN + 1):
        for R in range(1, N + 1):
            value = n_choose_r(N, R)
            if value > 1e6:
                numValuesOver1m += 1
                if maxN < 25:
                    print '{}c{} = {}'.format(N, R, value)
    print 'numValuesOver1m:', numValuesOver1m

    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

### HELPER FUNCTIONS ###

def doFactorials(upTo):
    result = {0: 1}
    for x in range(1, upTo + 1):
        result[x] = result[x-1] * x
    return result


def n_choose_r(n, r):
    """
    N choose R
    nCr = n! / r!(n-r)!
    where r <= n,
    n! = n*(n-1)*...*3*2*1, and 0! = 1.
    """
    return factorial_map[n] / (factorial_map[r] * factorial_map[n-r])




def assertEqual(a, b):
    if a != b:
        print 'a: {}'.format(a)
        print 'b: {}'.format(b)
    assert a == b


if __name__ == '__main__':
    main()
