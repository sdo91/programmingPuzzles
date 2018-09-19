#!/usr/bin/env python

from __future__ import division

import time
import primefac
from itertools import count


"""
Powerful digit sum
Problem 56 

A googol (10**100) is a massive number: one followed by one-hundred zeros; 
100**100 is almost unimaginably large: one followed by two-hundred zeros. 
Despite their size, the sum of the digits in each number is only 1.

Considering natural numbers of the form, a**b, where a, b < 100, 
what is the maximum digital sum?
"""
def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()

    assertEqual(sumDigits(10**100), 1)
    assertEqual(sumDigits(100**100), 1)
    assertEqual(sumDigits(12345), 15)
    
    runningMax = 0
    for a in range(80, 100):
        for b in range(80, 100):
            sumOfDigits = sumDigits(a**b)
            if sumOfDigits > runningMax:
                runningMax = sumOfDigits
                print 'new max: {}, {}**{} = {}'.format(
                    sumOfDigits, a, b, a**b)

    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

### HELPER FUNCTIONS ###

def sumDigits(x):
    # x = int(x)
    result = 0
    while x != 0:
        result += (x % 10)
        x //= 10
    return result

def assertEqual(a, b):
    if a != b:
        print 'a: {}'.format(a)
        print 'b: {}'.format(b)
    assert a == b


if __name__ == '__main__':
    main()
