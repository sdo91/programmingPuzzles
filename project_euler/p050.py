#!/usr/bin/env python

import time
import primefac
import math
import itertools




"""
Consecutive prime sum
Problem 50 
The prime 41, can be written as the sum of six consecutive primes:

41 = 2 + 3 + 5 + 7 + 11 + 13
This is the longest sum of consecutive primes that adds to a prime below one-hundred.

The longest sum of consecutive primes below one-thousand that adds to a prime, contains 21 terms, 
and is equal to 953.

Which prime, below one-million, can be written as the sum of the most consecutive primes?
"""

"""
NOTES:
do under 100 1st
maximize numTerms

"""

def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()


    # CIELING = 100
    # CIELING = 1000
    # CIELING = 1e6
    CIELING = 1e7

    # primes_list = primefac.primes(CIELING)
    primes_list = list(itertools.islice(primefac.primegen(), int(math.sqrt(CIELING))))

    print 'numPrimes: {}'.format(len(primes_list))
    print primes_list[:20]
    print primes_list[-10:]
    print

    # get numTerms of 0 to N, sum less than CIELING
    numTermsGuess = 0
    runningSum = 0
    for prime in primes_list:
        numTermsGuess += 1
        runningSum += prime
        if runningSum > CIELING:
            runningSum -= prime
            break
    print 'numTermsGuess = {}, runningSum = {}'.format(numTermsGuess, runningSum)



    done = False
    result = {}

    # maxNumTerms = len(primes_list)  # improve?
    numTerms = 1
    while not done:
        numTerms += 1

        maxStartIndex = len(primes_list) - numTerms
        for startIndex in xrange(0, maxStartIndex):
            endIndex = startIndex + numTerms  # actually one past end

            sumOfTerms = sum(primes_list[startIndex:endIndex])

            if sumOfTerms > CIELING:
                if numTerms % 25 == 0:
                    print 'hit CIELING: numTerms = {}, startIndex = {}'.format(numTerms, startIndex)
                if startIndex == 0:
                    done = True
                break  # go to next numTerms

            if primefac.isprime(sumOfTerms):
                # print 'RESULT: numTerms = {}, sumOfTerms = {}'.format(numTerms, sumOfTerms)
                result = {
                    'numTerms': numTerms,
                    'sumOfTerms': sumOfTerms,
                    'startIndex': startIndex,
                }

                # todo: pretty print
    # end outer loop

    print
    print result
    for i in range(result['startIndex'], result['startIndex'] + result['numTerms']):
        print primes_list[i],
        if i + 1 < result['startIndex'] + result['numTerms']:
            print '+',
        else:
            print '=',
    print result['sumOfTerms']
    print








    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

''' helper functions '''




if __name__ == '__main__':
    main()
