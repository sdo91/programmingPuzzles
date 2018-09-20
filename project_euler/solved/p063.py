#!/usr/bin/env python

from __future__ import division

import time
import primefac
from itertools import count


"""
Powerful digit counts
Problem 63 

The 5-digit number, 16807=7**5, is also a fifth power. 
Similarly, the 9-digit number, 134217728=8**9, is a ninth power.

How many n-digit positive integers exist which are also an nth power?
"""
def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()

    result = 0
    for x in xrange(100):
        result += getNumPowerful(x)
    print result

    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

### HELPER FUNCTIONS ###

def getNumPowerful(power):
    numPowerful = 0
    for base in count(1):
        candidate = base**power
        if getNumDigits(candidate) == power:
            print '{}**{} = {}'.format(base, power, candidate)
            numPowerful += 1
        elif getNumDigits(candidate) > power:
            break
    return numPowerful

def getNumDigits(x):
    return len(str(x))





def assertEqual(a, b):
    if a != b:
        print 'a: {}'.format(a)
        print 'b: {}'.format(b)
    assert a == b


if __name__ == '__main__':
    main()
