#!/usr/bin/env python

import time

"""
Square digit chains
Problem 92 

A number chain is created by continuously adding the square of the digits in a number to form a new number until it has been seen before.

For example,

44 -> 32 -> 13 -> 10 -> 1 -> 1
85 -> 89 -> 145 -> 42 -> 20 -> 4 -> 16 -> 37 -> 58 -> 89

Therefore any chain that arrives at 1 or 89 will become stuck in an endless loop. What is most amazing is that EVERY starting number will eventually arrive at 1 or 89.

How many starting numbers below ten million will arrive at 89?
"""


def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()

    assert reduce(2, verbose=True) == 89
    assert reduce(44, verbose=True) == 1
    assert reduce(85, verbose=True) == 89
    assert reduce(145, verbose=True) == 89
    print

    print getSortedDigits(1020304)
    print

    assert reduceWithMap(2, verbose=True) == 89
    print mapping
    assert reduceWithMap(44, verbose=True) == 1
    print mapping
    assert reduceWithMap(85, verbose=True) == 89
    print mapping
    assert reduceWithMap(145, verbose=True) == 89
    print mapping
    print

    num89 = 0
    ceiling = 10e6
    for x in xrange(1, int(ceiling)):
        percentDone = x / ceiling * 100
        if percentDone % 10 == 0:
            print '{}% done'.format(percentDone)
        if reduceWithMap(x) == 89:
            num89 += 1
    print
    print 'num89:', num89
    print 'size of mapping:', len(mapping)
    print 'notFoundInMapping:', notFoundInMapping
    print

    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)


# end main

''' helper functions '''

def reduce(x, verbose=False):
    """
    continuously add the square of the digits
    example:
        44 -> 32 -> 13 -> 10 -> 1 -> 1
        85 -> 89 -> 145 -> 42 -> 20 -> 4 -> 16 -> 37 -> 58 -> 89
    return 1 or 89
    """
    if x in {1, 89}:
        if verbose:
            print x
        return x

    if verbose:
        print x, '->',

    sumOfSquares = 0
    while x != 0:
        sumOfSquares += (x % 10) ** 2
        x /= 10

    return reduce(sumOfSquares, verbose)

mapping = {
    '1': 1,
    '89': 89
}
notFoundInMapping = 0
def reduceWithMap(x, verbose=False):
    """
    continuously add the square of the digits
    example:
        44 -> 32 -> 13 -> 10 -> 1 -> 1
        85 -> 89 -> 145 -> 42 -> 20 -> 4 -> 16 -> 37 -> 58 -> 89
    return 1 or 89

    max 9^2 * 7 = 567
    """
    sortedDigits = getSortedDigits(x)

    if sortedDigits in mapping:
        if verbose:
            print mapping[sortedDigits]
        return mapping[sortedDigits]

    global notFoundInMapping
    notFoundInMapping += 1

    if verbose:
        print x, '->',

    sumOfSquares = 0
    while x != 0:
        sumOfSquares += (x % 10) ** 2
        x /= 10

    mapping[sortedDigits] = reduceWithMap(sumOfSquares, verbose)
    return mapping[sortedDigits]

def getSortedDigits(x):
    result = ''.join(sorted(str(x)))
    firstNonZero = 0
    while result[firstNonZero] == '0':
        firstNonZero += 1
    return result[firstNonZero:]






if __name__ == '__main__':
    main()
