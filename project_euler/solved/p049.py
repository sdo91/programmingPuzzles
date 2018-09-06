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
Prime permutations
Problem 49 
The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, 
is unusual in two ways: 
(i) each of the three terms are prime, and, 
(ii) each of the 4-digit numbers are permutations of one another.

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property, 
but there is one other 4-digit increasing sequence.

What 12-digit number do you form by concatenating the three terms in this sequence?
"""
def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()


    pt = PrimeTools()
    primes_list = pt.getTenMilPrimesList(1, 1e4)
    print 'max prime: {} \n'.format(primes_list[-1])

    permutationBuckets = {}

    for prime in primes_list:
        if prime < 1000:
            continue
        if prime > 9999:
            break
        # print prime

        # convert to sorted string

        sortedString = ''.join(sorted(str(prime)))
        # print sortedString

        if sortedString not in permutationBuckets:
            permutationBuckets[sortedString] = []
        permutationBuckets[sortedString].append(prime)

    # print len(permutationBuckets)
    # print permutationBuckets

    for bucket in permutationBuckets:
        primesInBucket = permutationBuckets[bucket]
        if len(primesInBucket) < 3:
            continue

        # if bucket == '1478':
        #     print primesInBucket

        differences = {}
        for i in range(len(primesInBucket) - 1):
            for j in range(i + 1, len(primesInBucket)):
                diff = primesInBucket[j] - primesInBucket[i]
                diff_str = '{} - {} = {}'.format(primesInBucket[j], primesInBucket[i], diff)
                diff_tuple = (primesInBucket[i], primesInBucket[j])
                # print diff_str

                # check for match
                if diff in differences:
                    resultA = differences[diff]
                    resultB = diff_tuple
                    if (resultA[0] == resultB[1]) or (resultA[1] == resultB[0]):
                        print 'RESULT FOUND: {}, {}, diff = {}'.format(resultA, resultB, diff)
                        print primesInBucket
                        print

                differences[diff] = diff_tuple
            # print


            # break




    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

''' helper functions '''




if __name__ == '__main__':
    main()
