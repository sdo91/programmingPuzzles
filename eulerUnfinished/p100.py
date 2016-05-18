

'''
Arranged probability
Problem 100
If a box contains twenty-one coloured discs, composed of fifteen blue discs and six red discs, and two discs were taken at random, it can be seen that the probability of taking two blue discs, P(BB) = (15/21)×(14/20) = 1/2.

The next such arrangement, for which there is exactly 50% chance of taking two blue discs at random, is a box containing eighty-five blue discs and thirty-five red discs.

By finding the first arrangement to contain over 10^12 = 1,000,000,000,000 discs in total, determine the number of blue discs that the box would contain.
'''
    
def p100():
    
    # use diophantine eqs!!!
    
    from math import sqrt
    from itertools import count
    
    rootHalf = sqrt(.5)
    # print(rootHalf)
    
    
    for totalDiscs in count((10)+1):
    
        blueDiscs = 1+int(totalDiscs*rootHalf)
        # print(totalDiscs, blueDiscs)
        
        # probTwoBlue = (blueDiscs/totalDiscs)*((blueDiscs-1)/(totalDiscs-1))
        # print(probTwoBlue)
        
        numers = blueDiscs*(blueDiscs-1)*2
        denoms = totalDiscs*(totalDiscs-1)
        if numers == denoms:
            # print('y')
            print(totalDiscs, blueDiscs)
            # break
            
        if totalDiscs % 10000000 == 0:
            print('prog:',totalDiscs)
            break
            