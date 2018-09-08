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

addToPath('..')

import time

from prime_tools.prime_tools import PrimeTools



"""
It was proposed by Christian Goldbach that every odd composite number can be written as the sum of a prime and twice a square.

9 = 7 + 2*1^2
15 = 7 + 2*2^2
21 = 3 + 2*3^2
25 = 7 + 2*3^2
27 = 19 + 2*2^2
33 = 31 + 2*1^2

It turns out that the conjecture was false.

What is the smallest odd composite that cannot be written as the sum of a prime and twice a square?
"""
def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()


    pt = PrimeTools()
    primes_set = pt.getTenMilPrimesSet(1, 1e6)

    squares = {1}
    maxRootInSquares = 1
    maxSquareInSquares = 1

    done = False
    oddNum = 1
    while not done:
        oddNum += 2
        # if oddNum > 33:
        #     break
        if oddNum in primes_set:
            # not composite
            continue
        pairFound = False

        # print
        if (oddNum - 1) % 1e3 == 0:
            print oddNum
        while oddNum > maxSquareInSquares:
            maxRootInSquares += 1
            maxSquareInSquares = maxRootInSquares ** 2
            squares.add(maxSquareInSquares)
            print 'added {}^2 = {} to squares'.format(maxRootInSquares, maxSquareInSquares)

        # find prime and square
        for square in squares:
            possiblePrime = oddNum - (2 * square)
            if possiblePrime in primes_set:
                # print '{} = {} + 2 * {}'.format(oddNum, possiblePrime, square)
                pairFound = True
                break

        if not pairFound:
            print 'no solution for:', oddNum
            print squares
            done = True



    # 33 = 31 + 2 * 1^2


    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

''' helper functions '''




if __name__ == '__main__':
    main()
