

import math
import matplotlib.pyplot as plt
import numpy as np


DEG2RAD = math.pi / 180
RAD2DEG = 180 / math.pi


"""
A firecracker explodes at h = 100 m AGL
all particles have v0 = 20 m/s
no air resistance
g = 9.81 m/s^2
find volume of region

steps:
find 2d area from center to end
    given x, theta find y
    given x find optimal theta
    integrate
"""


def main():
    print 'firework'

    # print calcY(5, 45 * DEG2RAD)

    # x = 1e-3
    # bestTheta = givenXFindTheta(x)
    # print x, bestTheta * RAD2DEG, calcY(x, bestTheta)

    # for x in range(1, 10):
    #     bestTheta = givenXFindTheta(x)
    #     print x, bestTheta * RAD2DEG, calcY(x, bestTheta)


    # approxSolution()
    varyDeltaX()




    # plotRangeOfFixedThetas()
    # plotOptimal()
    # showPlots()



def plotRangeOfFixedThetas():
    # for theta_deg in range(0, 180, 1):
    for theta_deg in range(0, 90, 5):
        plotWithFixedTheta(theta_deg)

def plotWithFixedTheta(theta_deg):

    # xValues = np.arange(1, 21, 1)

    xValues = np.arange(0, 100, 0.01)
    xValues = np.delete(xValues, 0)

    theta_rad = theta_deg * DEG2RAD
    yValues = calcYArray(xValues, theta_rad)


    # print len(xValues)
    # print xValues
    # print yValues

    plt.plot(xValues, yValues)







def plotOptimal():
    print
    print 'plotting...'

    # xValues = np.arange(0, 100, 0.5)
    xValues = np.arange(0, 100, 2)
    xValues = np.delete(xValues, 0)


    for x in xValues:
        # bestTheta = givenXFindTheta(x)
        # print x, bestTheta * RAD2DEG, calcY(x, bestTheta)
        plt.plot(x, givenXFindY(x), 'r.')





def calcY(x, theta):
    """
    takes theta in radians
    """
    y = x/math.tan(theta) - (9.81 * x**2)/(800 * math.sin(theta)**2)
    return y + 100

def calcYArray(xValues, theta=None):
    size = len(xValues)
    result = np.zeros(size)
    for i in range(size):
        # todo: calc best theta
        result[i] = calcY(xValues[i], theta)
    return result

def givenXFindY(x):
    """
    final function to integrate
    combine 'givenXFindTheta' and 'calcY'

    wolfram alpha version:
    y = 100+(x/tan(2*atan2(sqrt(962361*x**2+1.6e9)-40000,981*x)))-(9.81*x**2)/(800*sin(2*atan2(sqrt(962361*x**2+1.6e9)-40000,981*x))**2)

    x = 2000*sqrt(2362)/981
    """
    # theta_rad = 2 * math.atan2(math.sqrt(962361 * x**2 + 1.6e9) - 40000, 981 * x)
    return 100 + (x / math.tan(2 * math.atan2(math.sqrt(962361 * x ** 2 + 1.6e9) - 40000, 981 * x))) - (9.81 * x ** 2) / (800 * math.sin(2 * math.atan2(math.sqrt(962361 * x ** 2 + 1.6e9) - 40000, 981 * x)) ** 2)


def finalEquation():
    """
    shell integration

    V = 2 pi Integral(x * f(x)) dx from a to b
    f(x) = 100+(x/tan(2*atan2(sqrt(962361*x**2+1.6e9)-40000,981*x)))-(9.81*x**2)/(800*sin(2*atan2(sqrt(962361*x**2+1.6e9)-40000,981*x))**2)
    a = 0
    b = 2000*sqrt(2362)/981


    integrate 2 * pi * x * f(x) from 0 to (2000*sqrt(2362)/981)
    integrate 2 * pi * x * (100+(x/tan(2*atan2(sqrt(962361*x**2+1.6e9)-40000,981*x)))-(9.81*x**2)/(800*sin(2*atan2(sqrt(962361*x**2+1.6e9)-40000,981*x))**2)) from 0 to (2000*sqrt(2362)/981)

    ans = 1.85653e6
    """
    pass

def varyDeltaX():

    dxValues = []
    for x in range(5):
        dxValues.append(1 * 10 ** -x)

    print dxValues

    for dx in dxValues:
        print 'dx={}, vol={}'.format(dx, approxSolution(dx, False))


def approxSolution(dx=None, verbose=True):

    if not dx:
        dx = 1e-3

    lastXVal = 2000 * math.sqrt(2362) / 981
    if verbose:
        print 'lastXVal: {} (y={})'.format(lastXVal, givenXFindY(lastXVal))
    xValues = np.arange(0, lastXVal, dx)

    size = len(xValues)

    totalVolume = 0

    for i in xrange(size):
        a = xValues[i]
        b = a + dx
        x = (a+b)/2
        y = givenXFindY(x)

        shellVol = 2 * math.pi * x * y * dx

        if verbose:
            if i < 5 or size - i < 5:
                print 'shellVol at x={}, y={}: {}'.format(x, y, shellVol)

        totalVolume += shellVol

    if verbose:
        print 'totalVolume:', totalVolume
    return totalVolume



    # for x in xValues:
    #     # bestTheta = givenXFindTheta(x)
    #     # print x, bestTheta * RAD2DEG, calcY(x, bestTheta)
    #     plt.plot(x, givenXFindY(x), 'r.')


def givenXFindTheta(x):
    """
    take derivative:
    d/dt (x / tan(t)) - (9.81 * x^2)/(800 * sin(t)^2)
    y' = x (-1 + 0.024525 x cot(t)) csc^2(t)

    set y' = 0 and solve for theta:
    t1 = 2 (tan^(-1)((-40000 + sqrt(1600000000 + 962361 x^2))/(981 x)))
    t2 =

    :param x:
    :return:
    """

    if x == 0:
        return 0

    # t1 is correct
    return 2 * math.atan2(math.sqrt(962361 * x**2 + 1.6e9) - 40000, 981 * x)


    # num1 = math.sqrt(962361 * x**2 + 1.6e9) - 40000
    # denom = 981 * x
    # t1 = 2 * math.atan2(num1, denom)
    # # print 'theta:', t1 * RAD2DEG
    # return t1

    # num2 = math.sqrt(962361 * x * x + 1.6e9) + 40000
    # denom = 981 * x
    # t2 = -2 * math.atan2(num2, denom)
    # print t2 * RAD2DEG


def showPlots():

    xmin = 0
    xmax = 100
    ymin = 0
    ymax = 125
    plt.axis([xmin, xmax, ymin, ymax])

    plt.savefig("firework.png")

    plt.ion()
    plt.show()
    raw_input('Hit enter to continue')


def simplePlot():
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)
    plt.plot(t, s)

    plt.xlabel('time (s)')
    plt.ylabel('voltage (mV)')
    plt.title('About as simple as it gets, folks')
    plt.grid(True)

    # plt.ion()
    # plt.show()
    # raw_input('Hit enter to continue')




if __name__ == '__main__':
    main()
