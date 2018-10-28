#!/usr/bin/env python

from __future__ import division

import time
import primefac
from itertools import count
from fractions import Fraction


"""
Large non-Mersenne prime
Problem 97 

The first known prime found to exceed one million digits was discovered in 1999, 
and is a Mersenne prime of the form 2**6972593-1; it contains exactly 2,098,960 digits. 
Subsequently other Mersenne primes, of the form 2**p-1, have been found which contain more digits.

However, in 2004 there was found a massive non-Mersenne prime which contains 2,357,207 digits: 
(28433 * 2**7830457) + 1.

Find the last ten digits of this prime number.
"""
def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()

    # print 2**7830457
    # test()

    # findLastTenDigits(28433, 64)
    findLastTenDigits(28433, 7830457)

    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

### HELPER FUNCTIONS ###

def findLastTenDigits(A, B):
    """
    find last ten digits of A * 2**B + 1
    """

    # fullPower = 2**B
    # fullAnswer = A * fullPower + 1
    # print 'fullPower: {}'.format(fullPower)
    # print 'fullAnswer: {}'.format(fullAnswer)

    MOD_VALUE = 10000000000
    modPower = 1
    for x in xrange(B):
        modPower *= 2
        modPower %= MOD_VALUE
    modAnswer = (A * modPower + 1) % MOD_VALUE
    print 'modPower: {}'.format(modPower)
    print 'modAnswer: {}'.format(modAnswer)


    pass


def assertEqual(a, b):
    if a != b:
        print 'a: {}'.format(a)
        print 'b: {}'.format(b)
    assert a == b


if __name__ == '__main__':
    main()
