import pdb

'''
In England the currency is made up of pound, £, and pence, p, and there are eight coins in general circulation:

1p, 2p, 5p, 10p, 20p, 50p, £1 (100p) and £2 (200p).
It is possible to make £2 in the following way:

1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p
How many different ways can £2 be made using any number of coins?
'''

coins = [100,50,25,10,5,1]
# coins = [200,100,50,20,10,5,2,1]

def waysToMakeChange(amount, maxCoin, coins):
    
    if maxCoin == 1:
        return 1
    if amount == 0:
        return 1
    
    possibleNumMaxCoin = int(amount/maxCoin)
    
    # print(possibleNumMaxCoin)
    totalPossibilities = 0
    
    nextSmallerCoin = coins[coins.index(maxCoin)+1]
    
    for numMaxCoin in range(possibleNumMaxCoin+1):
        valueOfSmallerCoins = amount-numMaxCoin*maxCoin
        totalPossibilities += waysToMakeChange(valueOfSmallerCoins, nextSmallerCoin, coins)
        
    return totalPossibilities

print(waysToMakeChange(100,100,coins)) # 1 dollar
# print(waysToMakeChange(200,200,coins))
    
    