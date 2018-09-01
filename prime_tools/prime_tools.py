

import time


PRIMES_FOLDER = '/home/sdo91/Downloads/primes/'


class PrimeTools(object):

    def getTenMilPrimesList(self, whichPart):
        result = []
        primesFile = PRIMES_FOLDER + '2T_part{}.txt'.format(whichPart)
        NUM_LINES = 1e6
        with open(primesFile) as infile:
            i = 0
            for line in infile:
                i += 1
                if i % (NUM_LINES / 10) == 0:
                    print '{}%'.format(int(i * 100 / NUM_LINES)),
                tokens = line.split()
                for x in tokens:
                    result.append(int(x))
            print '\ndone loading part {}'.format(whichPart)
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

