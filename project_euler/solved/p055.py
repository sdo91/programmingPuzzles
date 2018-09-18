#!/usr/bin/env python

from __future__ import division

import time
import primefac
from itertools import count
from numbers import Number


"""
Lychrel numbers
Problem 55 
If we take 47, reverse and add, 47 + 74 = 121, which is palindromic.

Not all numbers produce palindromes so quickly. For example,

349 + 943 = 1292,
1292 + 2921 = 4213
4213 + 3124 = 7337

That is, 349 took three iterations to arrive at a palindrome.

Although no one has proved it yet, it is thought that some numbers, 
like 196, never produce a palindrome. 
A number that never forms a palindrome through the reverse and add process 
is called a Lychrel number. 
Due to the theoretical nature of these numbers, and for the purpose of this problem, 
we shall assume that a number is Lychrel until proven otherwise. 
In addition you are given that for every number below ten-thousand, it will either 
    (i) become a palindrome in less than fifty iterations, or, 
    (ii) no one, with all the computing power that exists, 
    has managed so far to map it to a palindrome. 
In fact, 10677 is the first number to be shown to require over fifty iterations 
before producing a palindrome: 4668731596684224866951378664 (53 iterations, 28-digits).

Surprisingly, there are palindromic numbers that are themselves Lychrel numbers; 
the first example is 4994.

How many Lychrel numbers are there below ten-thousand?

NOTE: Wording was modified slightly on 24 April 2007 to emphasise 
the theoretical nature of Lychrel numbers.
"""
def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()

    assertEqual(isPalindrome('47'), False)
    assertEqual(isPalindrome('74'), False)
    assertEqual(isPalindrome('121'), True)
    assertEqual(isPalindrome(47), False)
    assertEqual(isPalindrome(74), False)
    assertEqual(isPalindrome(121), True)

    assertEqual(addReverse(47), 121)
    assertEqual(addReverse(74), 121)

    assertEqual(isLychrel(1, verbose=True), False)
    assertEqual(isLychrel(47, verbose=True), False)
    assertEqual(isLychrel(349, verbose=True), False)
    assertEqual(isLychrel(196, verbose=True), True)
    assertEqual(isLychrel(4994, verbose=True), True)
    assertEqual(isLychrel(10677, verbose=True, maxIter=52), True)
    assertEqual(isLychrel(10677, verbose=True, maxIter=53), False)

    numLychrel = 0
    lychrel_list = []
    for x in xrange(1, int(10e3)):
        if isLychrel(x):
            numLychrel += 1
            lychrel_list.append(x)
    print 'numLychrel:', numLychrel
    print 'lychrel_list:', lychrel_list[:20]
    print 'lychrel_list:', lychrel_list[-15:]


    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

### HELPER FUNCTIONS ###

def isLychrel(candidate, verbose=False, maxIter=50):
    """
    349 + 943 = 1292,
    1292 + 2921 = 4213
    4213 + 3124 = 7337
    """
    x = candidate
    for i in xrange(1, maxIter + 1):
        x = addReverse(x)
        if isPalindrome(x):
            if verbose:
                print 'candidate: {}, numIter: {}, palindrome: {}'.format(
                    candidate, i, x)
            return False
    if verbose:
        print 'candidate: {}, numIter: {}, palindrome: {}'.format(
            candidate, i, None)
    return True

def addReverse(x):
    """ 47 + 74 = 121 """
    return x + int(str(x)[::-1])


def isPalindrome(candidate):
    # if isinstance(candidate, Number):
    candidate = str(candidate)
    middle = int(len(candidate) / 2)
    for i in range(middle):
        if candidate[i] != candidate[-(i + 1)]:
            return False
    return True



def assertEqual(a, b):
    if a != b:
        print 'a: {}'.format(a)
        print 'b: {}'.format(b)
    assert a == b


if __name__ == '__main__':
    main()
