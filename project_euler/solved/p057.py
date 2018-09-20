#!/usr/bin/env python

from __future__ import division

import time
import primefac
from itertools import count
from fractions import Fraction


fracParts_dict = {}


"""
Square root convergents
Problem 57 
It is possible to show that the square root of two can be expressed as an infinite continued fraction.

sqrt 2 = 1 + 1/(2 + 1/(2 + 1/(2 + ... ))) = 1.414213...

By expanding this for the first four iterations, we get:

1 + 1/2 = 3/2 = 1.5
1 + 1/(2 + 1/2) = 7/5 = 1.4
1 + 1/(2 + 1/(2 + 1/2)) = 17/12 = 1.41666...
1 + 1/(2 + 1/(2 + 1/(2 + 1/2))) = 41/29 = 1.41379...

The next three expansions are 99/70, 239/169, and 577/408, but the eighth expansion, 1393/985, is the first example where the number of digits in the numerator exceeds the number of digits in the denominator.

In the first one-thousand expansions, how many fractions contain a numerator with more digits than denominator?
"""
def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()

    # print recursionTest(1)

    popFracParts(1000)
    # print fracParts_dict

    assertEqual(calcExpansion(1, verbose=True), Fraction(3, 2))
    assertEqual(calcExpansion(2, verbose=True), Fraction(7, 5))
    assertEqual(calcExpansion(3, verbose=True), Fraction(17, 12))
    assertEqual(calcExpansion(4, verbose=True), Fraction(41, 29))
    assertEqual(calcExpansion(8, verbose=True), Fraction(1393, 985))
    assert not isTopHeavy(calcExpansion(7))
    assert isTopHeavy(calcExpansion(8))
    assert not isTopHeavy(calcExpansion(9))

    numTopHeavy = 0
    for x in xrange(1, 1001):
        # if x % 10 == 0:
        #     print x
        expansion = calcExpansion(x)
        if isTopHeavy(expansion):
            # print 'top heavy: {}'.format(expansion)
            numTopHeavy += 1
    print 'numTopHeavy: {}'.format(numTopHeavy)

    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

### HELPER FUNCTIONS ###

def popFracParts(numParts):
    fracParts_dict[0] = 0
    for x in xrange(numParts):
        fracParts_dict[x + 1] = Fraction(1, 2 + fracParts_dict[x])

def isTopHeavy(frac):
    return len(str(frac.numerator)) > len(str(frac.denominator))

def calcExpansion(numIter, verbose=False):
    result = 1 + fracParts_dict[numIter]
    if verbose:
        print numIter, result, float(result)
    return result

def recursionTest(x):
    print x
    if x > 1000:
        return x
    return recursionTest(x + 1)

def assertEqual(a, b):
    if a != b:
        print 'a: {}'.format(a)
        print 'b: {}'.format(b)
    assert a == b


if __name__ == '__main__':
    main()
