from time import time
import primeTools



    
    
def primeSpeedTests():
    # speed comp
    
    startTime = time()
    sum1 = 0
    for x in range(1000000):
        if primeTools.isPrime(x):
            # print(x, end=', ')
            sum1 += 1
    print(time()-startTime)
    
    startTime = time()        
    sum2 = 0
    primes = primeTools.loadPrimes('1m')
    for x in range(1000000):
        if x in primes:
            sum2 += 1
    print(time()-startTime)
            
    assert sum1 == sum2
    
    
    
    
primeSpeedTests()