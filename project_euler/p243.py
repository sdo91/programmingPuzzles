#!/usr/bin/env python

from __future__ import division

import time
import primefac

from fractions import gcd
from fractions import Fraction
from itertools import count


primes_list = None


"""
Resilience
Problem 243
A positive fraction whose numerator is less than its denominator is called a proper fraction.
For any denominator, d, there will be d-1 proper fractions; for example, with d=12:
1/12 , 2/12 , 3/12 , 4/12 , 5/12 , 6/12 , 7/12 , 8/12 , 9/12 , 10/12 , 11/12 .

We shall call a fraction that cannot be cancelled down a resilient fraction.
Furthermore we shall define the resilience of a denominator, R(d), 
to be the ratio of its proper fractions that are resilient; for example, R(12) = 4/11 .
In fact, d=12 is the smallest denominator having a resilience R(d) < 4/10 .

Find the smallest denominator d, having a resilience R(d) < 15499/94744 .
"""


def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()

    # 2*3*3*5
    # 235 -> 8
    # numRes = 8 * 3 = 24
    assertEqual(phiCoprime(90), 16)
    assertEqual(phiTherom(90), 24)


    # lookForPatterns()
    # return

    # denominator = 12
    # for numerator in xrange(1, denominator):
    #     if isResilient(numerator, denominator):
    #         print '{}/{}, isResilient'.format(numerator, denominator)

    # speedTest(9699690)

    # getResilience(30, verbose=True)
    # getResilience(210)
    # getResilience(2310)
    # getResilience(30030)
    # getNumResilient(30030)
    # getResilience(510510)  # 0.21 s
    # getResilience(9699690)  # 4 s
    # getResilience(223092870)

    # getResilience2(2310)
    # getNumResilient(2310)

    # getNumResilient(12)
    # getResilience2(30030)




    # fracToBeat = 4 / 10
    fracToBeat = 15499 / 94744
    print 'fracToBeat:', fracToBeat
    minSoFar = 1
    primeGtr = primefac.primegen()
    denominator = 1
    primeFactors = []
    while True:
        primeFactors.append(next(primeGtr))
        denominator *= primeFactors[-1]
        print denominator

        numResilient = phiCoprime(denominator)
        resilience = numResilient / (denominator - 1)
        # resilFrac = Fraction(numResilient, denominator - 1)
        # print resilFrac

        if resilience < minSoFar:
            minSoFar = resilience
            print 'new min: {}, {}'.format(denominator, resilience)
            print 'factors:', list(primefac.primefac(denominator))
            print
        if resilience < fracToBeat:
            break

    """
    our goal is 0.163588195559
    from above loop we see:
    d = 223092870
    new min: 0.163588196089 (very close to goal)
    factors: [2, 3, 5, 7, 11, 13, 17, 19, 23]
    productOfFactors = 223092870 = d
    we can test multiples of this til we get under the mark
    """
    minSoFar = 1  # reset
    for denominator in count(223092870, 223092870):
        print denominator
        numResilient = phiTherom(denominator)
        resilience = numResilient / (denominator - 1)

        if resilience < minSoFar:
            minSoFar = resilience
            print 'new min: {}, {}'.format(denominator, resilience)
            print 'factors:', list(primefac.primefac(denominator))
            print
        if resilience < fracToBeat:
            break



    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

### HELPER FUNCTIONS ###

def lookForPatterns():
    # fracToBeat = 4 / 10
    fracToBeat = 0.21
    # fracToBeat = 15499 / 94744
    print 'fracToBeat:', fracToBeat
    minSoFar = 1



    for denominator in count(6, 6):
        primeFactors = list(primefac.primefac(denominator))

        numResilient = getNumResilient(denominator)
        resilience = numResilient / (denominator - 1)

        if resilience < minSoFar:
            minSoFar = resilience
            print 'denominator: {}'.format(denominator, resilience)
            print 'new min: {}'.format(resilience)
            print 'factors:', primeFactors
            print 'numResilient:', numResilient

            uniqueFactors = set(primeFactors)
            productOfUniqueFactors = 1
            for f in uniqueFactors:
                productOfUniqueFactors *= f
            print 'uniqueFactors:', uniqueFactors
            print 'productOfUniqueFactors:', productOfUniqueFactors
            print 'phiCoprime:', phiCoprime(productOfUniqueFactors)
            print 'phiTherom:', phiTherom(denominator)
            assertEqual(numResilient, phiTherom(denominator))
            print
        if resilience < fracToBeat:
            break


def speedTest(x):
    for i in xrange(x):
        isEven = (i % 2 == 0)

def phiTherom(denominator, verbose=False):
    """
    NOTE: seems to return num resilient...
    """
    factors_list = list(primefac.primefac(denominator))
    result = 1
    lastValueSeen = -1
    for p in factors_list:
        if p == lastValueSeen:
            result *= p
        else:
            result *= p - 1
        lastValueSeen = p
    return result

def phiCoprime(denominator, verbose=False):
    """
    NOTE: only works for numbers with coprime factors
    """
    factors_list = list(primefac.primefac(denominator))
    if verbose:
        print '\n{}: {}'.format(denominator, factors_list)

    phi = 1
    for p in factors_list:
        phi *= p-1
    if verbose:
        print phi
    return phi


def getResilience2(denominator, verbose=False):
    factors_list = list(primefac.primefac(denominator))
    print '\n{}: {}'.format(denominator, factors_list)

    # primes_list = primefac.primes(denominator)
    knownResilient = {1}
    notYetKnownResilient = {}
    for p in primes_list:
        if p > denominator:
            break
        if p > factors_list[-1]:
            knownResilient.add(p)








    numResilient = 1  # 1/x always resilient
    for numerator in xrange(2, denominator):
        # if numerator % 1e6 == 0:
        #     pass
            # print numerator
        if isResilient(numerator, factors_list):
            if numerator not in knownResilient:
                notYetKnownResilient[numerator] = list(primefac.primefac(numerator))
            if verbose:
                print '{}/{}'.format(numerator, denominator),
            numResilient += 1
        else:
            # not resilient
            assert numerator not in knownResilient
    if verbose:
        print

    print len(knownResilient), sorted(knownResilient)
    print 'notYetKnownResilient', len(notYetKnownResilient), notYetKnownResilient
    for key in notYetKnownResilient:
        if len(notYetKnownResilient[key]) > 2:
            print key, notYetKnownResilient[key]
    print len(knownResilient) + len(notYetKnownResilient)
    print 'denominator: {}, numResilient: {}'.format(denominator, numResilient)

    result = []
    resultCount = 1 + getResilientNumerators_recursive(1, 5, denominator, result)
    print 'recursive', len(result), sorted(result)
    print 'resultCount', resultCount

    result = numResilient / (denominator - 1)
    return result

def getResilientNumerators_recursive(blob, i, denominator, result_list):
    if i >= len(primes_list):
        print 'WARNING: i={} out of range, last prime: {}'.format(i, primes_list[-1])
        return 0
    result = 0
    numeratorToCheck = blob * primes_list[i]
    if numeratorToCheck < denominator:
        result += 1
        result_list.append(numeratorToCheck)
        result += getResilientNumerators_recursive(numeratorToCheck, i, denominator, result_list)  # up
        result += getResilientNumerators_recursive(blob, i + 1, denominator, result_list)  # over
    return result


def getNumResilient(denominator, verbose=False):
    factors_list = list(primefac.primefac(denominator))
    if verbose:
        print '\n{}: {}'.format(denominator, factors_list)

    numResilient = 1  # 1/x always resilient
    for numerator in xrange(2, denominator):
        # if numerator % 1e6 == 0:
        #     pass
            # print numerator
        if isResilient(numerator, factors_list):
            if verbose:
                print '{}/{}'.format(numerator, denominator),
            numResilient += 1
    if verbose:
        print

    if verbose:
        print 'denominator: {}, numResilient: {}'.format(denominator, numResilient)

    return numResilient



def isResilient(num, denomFactors):
    for factor in denomFactors:
        if num % factor == 0:
            return False
    return True

def oldMethod():
    # greater than 112000...

    # fracToBeat = 4/10
    # fracToBeat = 2 / 10
    fracToBeat = 15499 / 94744



    # for denominator in count(2, 2):  # d will be even (mult of 60?)
    for denominator in count(60, 60):  # d will be even (mult of 60?)

        cap = fracToBeat * (denominator - 1)

        numRes = 0
        for num in range(1, denominator, 2):  # num will be odd
            # print(num, d)

            if gcd(denominator, num) == 1:
                numRes += 1
                if numRes > cap:
                    break

        if numRes / (denominator - 1) < fracToBeat:
            print(denominator)
            break

        if denominator % 1000 == 0:
            print(denominator)


def assertEqual(a, b):
    if a != b:
        print 'a: {}'.format(a)
        print 'b: {}'.format(b)
    assert a == b


if __name__ == '__main__':
    main()




