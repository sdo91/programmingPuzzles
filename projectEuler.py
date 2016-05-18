import pdb
import time
import math
from primeToolsFolder.primeTools import isPrime
# import numpy


''' global vars '''
startTime = -1

def main():
    
    print('Scott\'s project Euler solutions \n')
    global startTime
    startTime = time.time()
    
    p42()
    # p89()
    # testPrimeToolsModule()
    
    elapsedTime = time.time()-startTime
    print('\n'+'Done!')
    printElapsedTime()
    
    
def printElapsedTime():
    global startTime
    elapsedTime = time.time()-startTime
    print('Elapsed time: {}s'.format(elapsedTime))
    
    
    
    

''' problems ''' 
    

def p89():
    
    import romanMod
    
    charsSaved = 0
    with open('files/p089_roman.txt') as inFile:
        for romanNum in inFile:
            
            romanNum = romanNum.strip()
            
            value = romanMod.fromRoman(romanNum)
            romanNum2 = romanMod.toRoman(value)
            
            if romanNum != romanNum2:
                saved = len(romanNum) - len(romanNum2)
                charsSaved += saved
                
            
                
    print(charsSaved)
            
            
            
    
    
def p42():
    
    import csv
    from itertools import count
    
    # get word list
    wordList = []
    with open('files/p042_words.txt') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')
        wordList = next(csvReader)
    
    
    # get max word value
    maxValue = -1
    maxWord = None
    for word in wordList:
        # word = 'SKY'
        
        wordValue = 0
        for letter in word:
            wordValue += letterToNumber(letter)
            
        if wordValue > maxValue:
            maxValue = wordValue
            maxWord = word
        
    print(maxWord, maxValue)
    
    
    # populate triNumbers set
    triNumbers = set()
    for n in count(1):
        triNum = n*(n+1)/2
        triNum = int(triNum)
        # print(triNum)
        triNumbers.add(triNum)
        if triNum > maxValue:
            break
        
    print(triNumbers)
    
    
    # check all words
    sum1 = 0
    for word in wordList:
        
        wordValue = 0
        for letter in word:
            wordValue += letterToNumber(letter)
            
        if wordValue in triNumbers:
            sum1 += 1
            
    print('result:', sum1)
    
    
        
def letterToNumber(letter):
    letter = letter.lower()
    number = ord(letter) - 96 ## before a
    return number
    

def p39():
    
    maxWays = -1
    maxP = -1
    for p in range(1,1001):
        
        maxA = p/(2+math.sqrt(2))
       
        numWays = 0
        for a in range(1,int(maxA)+1):
            # print(a)
            
            d = p-a
            b = (d**2-a**2)/(2*d)
            
            if b.is_integer():
                # print(a, b)
                numWays += 1
              
        if numWays >= 5:
            print(p, numWays)
            
            if numWays > maxWays:
                maxWays = numWays
                maxP = p
            
    print()
    print(maxP, maxWays)
                
    

def p38():
    
    
    # real
    maxN = 5
    maxConProd = -1
    for i in range(10000):
        conProd = ''
        n = 1
        while len(conProd) < 9:
            conProd += str(i*n)
            n += 1
            
        if isPandigital2(conProd):
            conProd = int(conProd)
            print(i, conProd)
            maxConProd = max(maxConProd, conProd)
            
    
    print('result:', maxConProd)
        
    # pdb.set_trace()
    
    
    
    
def isPandigital2(digits):
   
    if len(digits) != 9:
        return False
        
    sortedDigits = ''.join(sorted(digits))
    if sortedDigits == '123456789':
        return True
    else:
        return False
    

def p37():
    
    assert isTruncatablePrime(3796) == False
    assert isTruncatablePrime(3797) == True
    assert isTruncatablePrime(3798) == False
    
    matches = []
    sum1 = 0
    
    x = 11
    while len(matches) < 11:
    # for x in range(10,5000):
        if isTruncatablePrime(x):
            # print(x)
            matches.append(x)
            sum1 += x
        x += 2
            
    print(matches)
    print(sum1)
    
    
    
def isTruncatablePrime(i):
    
    if not isPrime(i):
        return False
    
    # remove ->
    modValue = 10
    while modValue < i:
        # print(i % modValue)
        if not isPrime(i % modValue):
            return False
        modValue *= 10
    
    # remove <-
    while i >= 10:
        i /= 10
        i = int(i)
        # print(i)
        if not isPrime(i):
            return False
        
    # passed all tests
    return True
    
        
def testPrimeToolsModule():
    for x in range(10):
        print('{}, {}'.format(x, isPrime(x)))

def p40():
    
    
    digitsArray = ['x']
    i = 1
    
    while len(digitsArray) < 1000001:
        
        digitsArray += toDigitArray(i)
        
        i += 1
        
    print(i)
    print(len(digitsArray))
        
    # print(digitsArray)
    assert digitsArray[12] == 1
    
    product = 1
    
    index = 1
    for _ in range(7):
        
        # print(index)
        product *= digitsArray[index]
        
        index *= 10
        
    print(product)

def p33():
    
    #print(isCurious(49, 98))
    numeratorFinal = 1
    denominatorFinal = 1
    
    for numerator in range(10,100):
        if numerator % 10 == 0:
            continue
        for denominator in range(numerator+1,100):
            if denominator % 10 == 0:
                continue
            
            if isCurious(numerator, denominator):
                #print('{}/{}'.format(numerator, denominator))
                numeratorFinal *= numerator
                denominatorFinal *= denominator
                
    from fractions import Fraction
    print(Fraction(numeratorFinal, denominatorFinal))
            
def isCurious(numerator, denominator):
    
    numeratorDigits = toDigitArray(numerator)
    denominatorDigits = toDigitArray(denominator)
    
    # print(set(numeratorDigits) & set(denominatorDigits))
    
    decimal = numerator/denominator
    
    # for each item in set, find other numbers
    if numeratorDigits[0] == denominatorDigits[0]: # if digits cancel
        if numeratorDigits[1]/denominatorDigits[1] == decimal: # and it's =
            return True
    if numeratorDigits[0] == denominatorDigits[1]: # if digits cancel
        if numeratorDigits[1]/denominatorDigits[0] == decimal: # and it's =
            return True
    if numeratorDigits[1] == denominatorDigits[0]: # if digits cancel
        if numeratorDigits[0]/denominatorDigits[1] == decimal: # and it's =
            return True
    if numeratorDigits[1] == denominatorDigits[1]: # if digits cancel
        if numeratorDigits[0]/denominatorDigits[0] == decimal: # and it's =
            return True
            
    return False
        
    
    
def toDigitArray(i):
    digits = []
    for digit in str(i):
        digits.append(int(digit))
    return digits
    
    
    
    

def p32():
    
    # print(isPandigital(39,186))
    
    # twoDigitNum = 39
    
    # min3Digit = 100
    # max3Digit = int(9999/twoDigitNum)
    
    products = set()
    
    # pdb.set_trace()
    
    for twoDigitNum in range(10,100):
        
        # print(twoDigitNum)
        min3Digit = 100
        max3Digit = int(9999/twoDigitNum)+1
    
        for threeDigitNum in range(min3Digit,max3Digit):
            
            if isPandigital(twoDigitNum,threeDigitNum):
                products.add(twoDigitNum*threeDigitNum)
                print('{} * {} = {}'.format(twoDigitNum, threeDigitNum, twoDigitNum*threeDigitNum))
                    
    
        
    # products2 = set()
    for oneDigitNum in range(1,10):
        
        min4Digit = 1000
        max4Digit = int(9999/oneDigitNum)+1
        
        for fourDigitNum in range(min4Digit,max4Digit):
            
            if isPandigital(oneDigitNum,fourDigitNum):
                products.add(oneDigitNum*fourDigitNum)
                print('{} * {} = {}'.format(oneDigitNum, fourDigitNum, oneDigitNum*fourDigitNum))
        
    print(products)
        
    sum1 = 0        
    for p in products:
        sum1 += p
        
    print(sum1)
            
            
            
def isPandigital(a, b):
    product = a*b
    
    digits = str(a)+str(b)+str(product)
    
    if len(digits) != 9:
        return False
        
    sortedDigits = ''.join(sorted(digits))
    if sortedDigits == '123456789':
        return True
    else:
        return False
    

def p36():
    
    sum1 = 0
    for x in range(1,1000000,2):
        
        if isPalindromic(str(x)):
            
            binDigits = bin(x)[2:]
            if isPalindromic(binDigits):
                # print(x,':',binDigits)
                sum1 += x
                
    print(sum1)
    
def isPalindromic(digits):
    
    middle = int(len(digits)/2)
    for i in range(middle):
        if digits[i] != digits[-(i+1)]:
            return False
            
    return True
    
def p31():
    coins = [200,100,50,20,10,5,2,1]
    print(waysToMakeChange(200,200,coins))
    
def waysToMakeChange(amount, maxCoin, coins):
    
    if maxCoin == 1:
        return 1
    if amount == 0:
        return 1
    
    possibleNumMaxCoin = int(amount/maxCoin)
    
    # print(possibleNumMaxCoin)
    totalWays = 0
    
    nextSmallerCoin = coins[coins.index(maxCoin)+1]
    
    for numMaxCoin in range(possibleNumMaxCoin+1):
        valueOfSmallerCoins = amount-numMaxCoin*maxCoin
        totalWays += waysToMakeChange(valueOfSmallerCoins, nextSmallerCoin, coins)
        
    return totalWays

def p35():
    
    # getRotations(197)
    primes = loadPrimes('1m')
    circPrimes = []
    
    for n in range(1,1000000,2):
        rotations = getRotations(n)
        
        isCircPrime = True
        # n = 10 or n = 11
        
        for r in rotations: # check all rotations of a number
            if r not in primes: # a rotation failed
                # print('r:', r)
                isCircPrime = False
                break
            
        if isCircPrime:
            circPrimes.append(n)
        
    print(len(circPrimes))
        
    
def getRotations(i):
    
    asStr = str(i)
    rotations = []
        
    for startIdx in index(asStr):
        newRotation = asStr[startIdx:] + asStr[:startIdx]
        rotations.append(int(newRotation))
        
    return rotations
    

def p34():
    
    maxVal = math.factorial(9) * (len(str(math.factorial(9)))+1)
    # print(maxVal)
    
    sum2 = 0
    for x in range(10, maxVal):
        if isSumFact(x):
            sum2 += x
    
    print(sum2)
    
def isSumFact(i):
    
    stringRep = str(i)
    sum1 = 0
    
    for char in stringRep:
        # print(char)
        sum1 += math.factorial(int(char))
    
    return sum1 == i
    

def p44():
    
    numToGenerate = 500000
    numList = ['x']
    numSet = set()
    
    for n in range(1,numToGenerate):
        pentNum = n*(3*n-1)/2
        numList.append(pentNum)
        numSet.add(pentNum)
        
    d = 99999999999999
    print('done w/ part 1')
        
    for smallerNum in range(1,numToGenerate):
        
        if smallerNum%10000 == 0:
            print(smallerNum)
        
        for largerNum in range(smallerNum+1,min(numToGenerate,smallerNum+1000)):
            # print(smallerNum, largerNum)
            
            if numList[smallerNum] + numList[largerNum] in numSet:
                if numList[largerNum] - numList[smallerNum] in numSet:
                    print('some d found')
                    d = min(d, numList[largerNum] - numList[smallerNum])
    
    print('d: ', d)
        
    
def p82():
    
    matrixRows = []
    
    with open('files/p081_matrix.txt') as inFile:
        for line in inFile:
            
            line = line.strip().split(',')
            line = list(map(int, line))
            
            matrixRows.append(line)
            
            # pdb.set_trace()
            
    # print(matrixRows)
    
    matrixSize = len(matrixRows)
    
    for col in range(matrixSize-2,-1,-1):
        
        # col to the right is of min sum to the end
        
        
        newCol = [10000*matrixSize]*matrixSize
        
        # print(newCol)
        
        
        for row in range(matrixSize):
            
            # find the best sum to end of this row
            
            # row = 2 #test
            
            for possibleCorner in range(matrixSize):
                #go from matrix[row][col] to matrix[corner][col]
                
                sumToEnd = matrixRows[possibleCorner][col+1]
                
                if possibleCorner < row:
                    #pc = 0, row = 2
                    for x in range(row, possibleCorner-1, -1):
                        sumToEnd += matrixRows[x][col]
                    
                elif possibleCorner == row:
                    sumToEnd += matrixRows[row][col]
                    
                elif possibleCorner > row:
                    for x in range(row, possibleCorner+1):
                        sumToEnd += matrixRows[x][col]
                    
                else:
                    print('flagrant error')
                    
                newCol[row] = min(newCol[row], sumToEnd)
                
                
                
                # print(possibleCorner)
                
                # print(matrixRows[possibleCorner][col])
                
                
                #pdb.set_trace()
                
                
        # print(newCol)
        
        for i in index(newCol):
            # print(i, col)
            matrixRows[i][col] = newCol[i]
            
    
    
    # print(matrixRows)
    
    minVal = 10000*matrixSize
    for i in range(matrixSize):
        minVal = min(minVal, matrixRows[i][0])
        
    print(minVal)
    
    # pdb.set_trace()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
def index(x):
    return range(len(x))
    
    
def p62():
    
    x = 0
    permutationDict = {}
    done = False
    numPermutations = 5
    
    while not done:
        
        stringRep = str(x**3)
        
        # print(stringRep)
        
        arrayRep = []
        for c in stringRep:
            arrayRep.append(c)
        arrayRep = sorted(arrayRep)
        
        stringRep = ''
        for c in arrayRep:
            stringRep += c
        
        # print(arrayRep)
        # print(stringRep)
        
        # stringRep has sorted digits
        if stringRep not in permutationDict:
            permutationDict[stringRep] = [x]
        else:
            permutationDict[stringRep].append(x)
            if len(permutationDict[stringRep]) >= numPermutations:
                
                print(permutationDict[stringRep])
                
                for entry in permutationDict[stringRep]:
                    print('entry: {}, cube: {}'.format(entry, entry**3))
                
                done = True
        
        x += 1
    # end while
    
def p51():

    primeSet = loadPrimes('1m')
    
    # find 7 primes in 5 digits
    # right most digit will not be an *, also left
    
    
    
    
def p59():
    
    assert ord('A') == 65
    assert ord('*') == 42
    assert ord('k') == 107
    
    assert 65 ^ 42 == 107
    assert 107 ^ 42 == 65
    
    ''' import file '''
    ciphertext = []
    with open('files/p059_cipher.txt') as inFile:
        strings = inFile.read().split(',')
        for s in strings:
            ciphertext.append(int(s))
            
    # print(strings)
    # print(ciphertext)
    assert len(ciphertext) == 1201
    assert ciphertext[0] == 79
    assert ciphertext[-1] == 73
    
    ''' loop '''
    loopStart = ord('a')
    loopEnd = ord('z')+1
    
    for char0 in range(loopStart, loopEnd):
        for char1 in range(loopStart, loopEnd):
            for char2 in range(loopStart, loopEnd):
                chars = [char0, char1, char2]
                
                decrypted = ''
                for i in range(len(ciphertext)):
                    charIdx = i%3
                    
                    nextChar = chars[charIdx] ^ ciphertext[i]
                    nextChar = chr(nextChar)
                    
                    decrypted += nextChar
                    
                # print(decrypted)
                
                words = decrypted.split()
                
                if len(words) > 200:
                    
                    # match found
                    
                    print(len(words))
                    print(decrypted)
                    
                    print('key: ', end='')
                    for x in chars:
                        print(chr(x), end='')
                    print()
                    
                    sum = 0
                    for x in decrypted:
                        sum += ord(x)
                    
                    print(sum)
                    
                    
                    # pdb.set_trace()
                
                
        
        # print(chr(char1))
    
    

    
    
    
def p27():
    
    primes = loadPrimes()
    
    absMax = 1000
    
    # b must be prime
    sortedPrimes = sorted(primes)
    possBVals = []
    for x in range(168):
        # print(sortedPrimes[x])
        possBVals.append(sortedPrimes[x])
        
    assert len(possBVals) == 168
    
    
    
    
    highestN, bestA, bestB = -1, 0, 0
    
    for a in range(1-absMax,absMax):
        for b in possBVals:
            
            #a, b = 1, 41
            # a/b are chosen
            
            # start at n = 1, inc
            # we know n=0 works
            
            
            
            n = 0
            stillGoing = True
            while stillGoing:
                
                resultOfEq = n**2 + a*n + b
                
                assert resultOfEq < sortedPrimes[-1] # or my list doesnt work
                
                numberIsPrime = resultOfEq in primes
                
                if not numberIsPrime:
                    
                    biggestWorkingN = n-1
                    
                    if biggestWorkingN > highestN:
                        
                        highestN = biggestWorkingN
                        bestA = a
                        bestB = b
                    
                    stillGoing = False
                
                n += 1
            # end while
    
    # print(bestA)
    # print(bestB)
    # print(highestN)
    print(bestA*bestB)
    
    
    
def p29():
    
    aMax = 100
    bMax = aMax
    
    distinct = set()
    
    for a in range(2,aMax+1):
        for b in range(2,bMax+1):
            power = a**b
            distinct.add(power)
            
    
    # sortedSet = sorted(distinct)
    # print(type(sortedSet))
    # print(sortedSet)

    print(len(distinct))




def loadPrimes(size='50k'):
    ''' deprecated, use primeTools module '''
    assert False
    return None 


if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
