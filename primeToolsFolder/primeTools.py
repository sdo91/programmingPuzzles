import pdb
import time
import os

''' global vars '''
primeSet = []
maxPrime = -1

def isPrime(i):
    global primeSet
    global maxPrime
    
    assert type(i) is int
    
    if len(primeSet) == 0:
        primeSet = loadPrimes('1m')
        maxPrime = sorted(primeSet)[-1]
        
    assert i <= maxPrime
    
    return i in primeSet
    

def primeTests():
    
    print(len(loadPrimes('1m')))
    print(len(loadPrimes('50k')))
    print(len(loadPrimes()))
    
    prime = 10663993
    primeSet = loadPrimes('1m')
    
    pdb.set_trace()
    
    print(prime in primeSet)
    print(prime+1 in primeSet)
    
    time1 = time.time()
    for x in range(1000000):
        x in primeSet
    print(time.time()-time1)


def loadPrimes(size='50k'):
    
    startTime = time.time()
    
    # set up path
    path = 'primes{}.txt'.format(size)
    if os.path.isdir('./primeToolsFolder'):
        # print('use subfolder')
        path = 'primeToolsFolder/' + path
    print('loading primes from: ', path)
    
    # read file
    primeSet = set()
    with open(path) as inFile:
        
        for line in inFile:
            tokens = line.split()
            
            for token in tokens:
                primeSet.add(int(token))
                
    endTime = time.time()
    print('loaded primes in {}s'.format(endTime-startTime))
    
    return primeSet 
    
def testWrite():
    
    ''' figuring out how to work with folders in python... '''
    
    print('writing test file')
    
    path = 'testWrite.txt'
    if os.path.isdir('./primeToolsFolder'):
        # print('writing to subfolder')
        path = 'primeToolsFolder/' + path
    
    with open(path, 'w') as outFile:
        outFile.write('hi')
        
    
    
if __name__ == '__main__':
    print('import this module!')
    