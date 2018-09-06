

import time


PRIMES_FOLDER = '/home/sdo91/code/programming_puzzles/prime_tools/primes/'


class PrimeTools(object):

    def getTenMilPrimesList(self, whichPart, numPrimesToLoad=10e6):
        result = []
        primesFile = PRIMES_FOLDER + '2T_part{}.txt'.format(whichPart)
        print 'loading primes from {}'.format(primesFile)
        with open(primesFile) as infile:
            i = 0
            for line in infile:
                i += 1
                if i * 10 > numPrimesToLoad:
                    break
                if i % (numPrimesToLoad / 100) == 0:
                    print '{}%'.format(int(i * 1000 / numPrimesToLoad)),
                tokens = line.split()
                for x in tokens:
                    result.append(int(x))
            print '\nloaded {} primes'.format(len(result))
        return result

    def getTenMilPrimesSet(self, whichPart, numPrimesToLoad=10e6):
        l = self.getTenMilPrimesList(whichPart, numPrimesToLoad)
        result = set(l)
        print 'converted to set'
        return result



def main():

    ### load primes ###
    startTime = time.time()

    pt = PrimeTools()
    tenMilPrimes_list = pt.getTenMilPrimesList(1)
    print len(tenMilPrimes_list)

    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)

if __name__ == '__main__':
    main()

