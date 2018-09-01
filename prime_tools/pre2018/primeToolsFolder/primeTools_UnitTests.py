import unittest
import primeTools

class PrimeTests(unittest.TestCase):
    
    def test1(self):
        self.assertTrue(True)
        self.assertFalse(False)
        
        
    def test2(self):
        
        self.assertTrue(len(primeTools.loadPrimes('1m')) == 1000000)
        self.assertTrue(len(primeTools.loadPrimes('50k')) == 50000)
        self.assertTrue(len(primeTools.loadPrimes()) == 50000)
        
        
        prime = 10663993
        primeSet = primeTools.loadPrimes('1m')
        self.assertTrue(prime in primeSet)
        self.assertFalse(prime+1 in primeSet)
        
    
    def test3(self):
        
        prime = 10663993
        self.assertTrue(primeTools.isPrime(prime))
        self.assertFalse(primeTools.isPrime(prime+1))
        
        
if __name__ == '__main__':
    
    unittest.main()