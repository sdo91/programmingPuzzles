

'''
Resilience
Problem 243
A positive fraction whose numerator is less than its denominator is called a proper fraction.
For any denominator, d, there will be d−1 proper fractions; for example, with d=12:
1/12 , 2/12 , 3/12 , 4/12 , 5/12 , 6/12 , 7/12 , 8/12 , 9/12 , 10/12 , 11/12 .

We shall call a fraction that cannot be cancelled down a resilient fraction.
Furthermore we shall define the resilience of a denominator, R(d), to be the ratio of its proper fractions that are resilient; for example, R(12) = 4/11 .
In fact, d=12 is the smallest denominator having a resilience R(d) < 4/10 .

Find the smallest denominator d, having a resilience R(d) < 15499/94744 .
'''

def p243():
    
    # greater than 112000...
    
    from fractions import gcd
    from itertools import count
    
    # fracToBeat = 4/10
    fracToBeat = 15499/94744
    
    for d in count(2,2): # d will be even (mult of 60?)
        
        cap = fracToBeat*(d-1)
        
        numRes = 0
        for num in range(1,d,2): # num will be odd
            # print(num, d)
            
            if gcd(d, num) == 1:
                numRes += 1
                if numRes > cap:
                    break
            
        if numRes/(d-1) < fracToBeat:
            print(d)
            break
        
        if d % 1000 == 0:
            print(d)