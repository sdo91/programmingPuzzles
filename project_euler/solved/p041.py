#!/usr/bin/env python

def addToPath(relPath):
    from os import path
    import sys
    dirOfThisFile = path.dirname(path.realpath(__file__))
    dirToAdd = path.normpath(path.join(dirOfThisFile, relPath))
    if dirToAdd not in sys.path:
        print 'adding to path:', dirToAdd
        sys.path.insert(0, dirToAdd)
    else:
        print 'already in path:', dirToAdd

addToPath('../..')

import time

from prime_tools.prime_tools import PrimeTools



"""
We shall say that an n-digit number is pandigital 
if it makes use of all the digits 1 to n exactly once. 

For example, 2143 is a 4-digit pandigital and is also prime.

What is the largest n-digit pandigital prime that exists?
"""
def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()

    # print isPandigital(2142)
    # print isPandigital(2143)
    # print isPandigital(2144)

    pt = PrimeTools()

    for x in range(1, 2):
        tenMilPrimes_list = pt.getTenMilPrimesList(x)
        # print len(tenMilPrimes_list)

        for prime in tenMilPrimes_list:
            if prime > 7654321:
                break
            if isPandigital(prime):
                print prime

    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

''' helper functions '''

def isPandigital(candidate):
    ALL_DIGITS = '123456789'
    candidate_str = str(candidate)
    candidate_str = ''.join(sorted(candidate_str))
    numDigits = len(candidate_str)
    firstNDigits = ALL_DIGITS[:numDigits]
    return candidate_str == firstNDigits





if __name__ == '__main__':
    main()
