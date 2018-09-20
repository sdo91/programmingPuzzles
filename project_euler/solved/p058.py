#!/usr/bin/env python

from __future__ import division

import time
import primefac
from itertools import count


"""
Spiral primes
Problem 58 
Starting with 1 and spiralling anticlockwise in the following way, 
a square spiral with side length 7 is formed.

    37 36 35 34 33 32 31
    38 17 16 15 14 13 30
    39 18  5  4  3 12 29
    40 19  6  1  2 11 28
    41 20  7  8  9 10 27
    42 21 22 23 24 25 26
    43 44 45 46 47 48 49

It is interesting to note that the odd squares lie along the bottom right diagonal, 
but what is more interesting is that 8 out of the 13 numbers lying along both diagonals are prime; 
that is, a ratio of 8/13 ~= 62%.

If one complete new layer is wrapped around the spiral above, 
a square spiral with side length 9 will be formed. 
If this process is continued, what is the side length of the square spiral 
for which the ratio of primes along both diagonals first falls below 10%?
"""
def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()

    numPrime = 0
    numCorners = 1

    for sideLength in count(3, 2):
        # if sideLength > 7:
        #     break
        oddSquare = sideLength**2
        corners = []
        for x in xrange(1, 4):
            corner = oddSquare - (x * (sideLength - 1))
            corners.append(corner)
            if primefac.isprime(corner):
                numPrime += 1
        numCorners += 4
        percent = numPrime/numCorners
        print '{} {} {}: {}/{} ~= {}'.format(
            sideLength, oddSquare, corners, numPrime, numCorners, percent)
        if percent < 0.1:
            break


    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

### HELPER FUNCTIONS ###


# def getOddSquares(4):


def assertEqual(a, b):
    if a != b:
        print 'a: {}'.format(a)
        print 'b: {}'.format(b)
    assert a == b


if __name__ == '__main__':
    main()
