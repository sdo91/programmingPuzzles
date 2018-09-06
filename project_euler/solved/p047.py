#!/usr/bin/env python

import time
import primefac




"""
Distinct primes factors
Problem 47 
The first two consecutive numbers to have two distinct prime factors are:

14 = 2 * 7
15 = 3 * 5

The first three consecutive numbers to have three distinct prime factors are:

644 = 22 * 7 * 23
645 = 3 * 5 * 43
646 = 2 * 17 * 19.

Find the first four consecutive integers to have four distinct prime factors each. 
What is the first of these numbers?
"""
def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()

    # for i in range(1, 21):
    #     print i, set(primefac.primefac(i))

    GOAL = 4
    numInARow = 0
    i = 0
    while True:
        i += 1
        if i % 1e5 == 0:
            print i
        distinctFactors = set(primefac.primefac(i))
        if len(distinctFactors) == GOAL:
            numInARow += 1
            if numInARow >= GOAL:
                firstInStreak = i - numInARow + 1
                print 'RESULT: {} - {}'.format(firstInStreak, i)
                for j in range(firstInStreak, i + 1):
                    print j, set(primefac.primefac(j))
                break
        else:
            numInARow = 0


    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

''' helper functions '''




if __name__ == '__main__':
    main()
