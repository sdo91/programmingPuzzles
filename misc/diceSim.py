import random
from time import time


def roll():
    return random.randint(1,6)
    

numRolls = 0
sum1 = 0
results = dict()
time1 = time()
numSeconds = 60

while time()-time1 < numSeconds:
    rolledNum = roll()
    
    sum1 += rolledNum
    numRolls += 1
    
    if rolledNum in results:
        results[rolledNum] += 1
    else:
        results[rolledNum] = 1
    
print(sum1/numRolls)
print(results)
print(numRolls/6)

print(time()-time1)