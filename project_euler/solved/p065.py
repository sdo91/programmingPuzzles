#!/usr/bin/env python

from __future__ import division

import time
from fractions import Fraction

"""
Convergents of e
Problem 65 
The square root of 2 can be written as an infinite continued fraction.

The infinite continued fraction can be written, sqrt 2 = [1;(2)], (2) indicates that 2 repeats ad infinitum. 
In a similar way, sqrt 23 = [4;(1,3,1,8)].

It turns out that the sequence of partial values of continued fractions for square roots provide the best rational approximations. 
Let us consider the convergents for sqrt 2.
 
Hence the sequence of the first ten convergents for sqrt 2 are:

1, 3/2, 7/5, 17/12, 41/29, 99/70, 239/169, 577/408, 1393/985, 3363/2378, ...
What is most surprising is that the important mathematical constant,
e = [2; 1,2,1, 1,4,1, 1,6,1 , ... , 1,2k,1, ...].

The first ten terms in the sequence of convergents for e are:

2, 3, 8/3, 11/4, 19/7, 87/32, 106/39, 193/71, 1264/465, 1457/536, ...
The sum of digits in the numerator of the 10th convergent is 1+4+5+7=17.

Find the sum of digits in the numerator of the 100th convergent of the continued fraction for e.
"""


def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()

    assertEqual(getFracPart([2] * 0), 0)
    assertEqual(getFracPart([2] * 1), 1/2)
    assertEqual(getFracPart([2] * 2), 2/5)
    assertEqual(getFracPart([2] * 3), 5/12)

    assertEqual(converge(1, [2] * 0), 1)
    assertEqual(converge(1, [2] * 1), 3/2)
    assertEqual(converge(1, [2] * 2), 7/5)
    assertEqual(converge(1, [2] * 3), 17/12)

    assertEqual(converge_frac(1, [2] * 0), Fraction(1))
    assertEqual(converge_frac(1, [2] * 1), Fraction(3, 2))
    assertEqual(converge_frac(1, [2] * 2), Fraction(7, 5))
    assertEqual(converge_frac(1, [2] * 3), Fraction(17, 12))

    assertEqual(genValuesForE(0), [])
    assertEqual(genValuesForE(1), [1])
    assertEqual(genValuesForE(2), [1, 2])
    assertEqual(genValuesForE(3), [1, 2, 1])
    assertEqual(genValuesForE(4), [1, 2, 1, 1])
    assertEqual(genValuesForE(5), [1, 2, 1, 1, 4])
    assertEqual(genValuesForE(6), [1, 2, 1, 1, 4, 1])



    for N in range(1, 101):
        print 'N={}: {}'.format(N, getNthConvergentOfE(N))
        print 'sumOfDigits: {}'.format(sumOfDigits(N))
        print





    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)


# end main


''' helper functions '''

def sumOfDigits(N):
    nthConvergent = getNthConvergentOfE(N)
    # print 'nthConvergent:', nthConvergent

    digits = nthConvergent.numerator

    sumOfDigits = 0
    while digits != 0:
        sumOfDigits += (digits % 10)
        digits //= 10
    return sumOfDigits

def getNthConvergentOfE(N):
    return converge_frac(2, genValuesForE(N - 1))

def genValuesForE(numValues):
    kValue = 2
    result = [1] * numValues
    for x in xrange(1, numValues, 3):
        result[x] = kValue
        kValue += 2
    return result

def converge_frac(constant, values_list):
    return Fraction(constant) + getFracPart_frac(values_list)

def getFracPart_frac(values_list):
    if not values_list:
        return Fraction(0)
    return Fraction(1, Fraction(values_list[0]) + getFracPart_frac(values_list[1:]))

def converge(constant, values_list):
    return constant + getFracPart(values_list)

def getFracPart(values_list):
    if not values_list:
        return 0
    return 1 / (values_list[0] + getFracPart(values_list[1:]))



def assertEqual(a, b):
    if a != b:
        print 'a: {}'.format(a)
        print 'b: {}'.format(b)
    assert a == b

    

    
    



if __name__ == '__main__':
    main()
