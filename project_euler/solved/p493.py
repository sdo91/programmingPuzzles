#!/usr/bin/env python

from __future__ import division

import time
import primefac
from itertools import count
import random
from fractions import Fraction

factorial_map = None

"""
Under The Rainbow
Problem 493 

70 colored balls are placed in an urn, 10 for each of the seven rainbow colors.

What is the expected number of distinct colors in 20 randomly picked balls?

Give your answer with nine digits after the decimal point (a.bcdefghij).
"""
def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()


    global factorial_map
    factorial_map = doFactorials(70)
    print n_choose_r(70, 20)


    print getProbOfAtLeastOneRed() * 7
    print float(getProbOfAtLeastOneRed_frac() * 7)

    # 9.166672 1e6, normal avg
    # 9.24717458445 1e6, running avg

    # resultSum = 0
    # numIterations = 0
    ALPHA = 0.1
    runningAvg = doSim()
    for x in xrange(int(1e3)):
        if x % 10000 == 0:
            print x
        runningAvg = doSim() * ALPHA + runningAvg * (1 - ALPHA)
    print 'avg: ', runningAvg

    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

def doSim():
    ballsPicked_list = random.sample(xrange(70), 20)
    colors_set = set()
    for ball in ballsPicked_list:
        colors_set.add(ball % 10)
    # print '{}: {}'.format(len(colors_set), colors_set)
    return len(colors_set)

def getProbOfAtLeastOneRed():
    """
    what is the prob of getting at least one red in 20 draws w/o replacment?
    what is prob of getting zero?
        60/70 * 59/69 * ... * 41/51
    """
    probOfZeroRed = 1
    for x in range(20):
        probOfZeroRed *= (60 - x) / (70 - x)
    return 1 - probOfZeroRed

def getProbOfAtLeastOneRed_frac():
    """
    what is the prob of getting at least one red in 20 draws w/o replacment?
    what is prob of getting zero?
        60/70 * 59/69 * ... * 41/51
    """
    probOfZeroRed = Fraction(1)
    for x in range(20):
        probOfZeroRed *= Fraction(60 - x, 70 - x)
    return Fraction(1) - probOfZeroRed


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
