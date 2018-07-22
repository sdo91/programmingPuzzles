

import math

DEG2RAD = math.pi / 180
RAD2DEG = 180 / math.pi

def main():
    print 'hw'

    print calcY(5, 45 * DEG2RAD)

    x = 1e-3
    bestTheta = givenXFindTheta(x)
    print x, bestTheta * RAD2DEG, calcY(x, bestTheta)

    for x in range(1, 10):
        bestTheta = givenXFindTheta(x)
        print x, bestTheta * RAD2DEG, calcY(x, bestTheta)
    # print calcY(5, theta)

def calcY(x, theta):
    # theta *= DEG2RAD
    y = x*math.cos(theta)/math.sin(theta) - (9.81 * x**2)/(800 * math.sin(theta)**2)
    return y + 100

def givenXFindTheta(x):
    """
    d/dt x cos(t)/sin(t) - (9.81 * x^2)/(800 * sin(t)^2)
    y' = x (-1 + 0.024525 x cot(t)) csc^2(t)

    set y' = 0 and solve for theta:
    t1 = 2 (tan^(-1)((-40000 + sqrt(1600000000 + 962361 x^2))/(981 x)))
    t2 =

    :param x:
    :return:
    """

    if x == 0:
        return 0

    num1 = math.sqrt(962361 * x * x + 1.6e9) - 40000
    denom = 981 * x
    t1 = 2 * math.atan2(num1, denom)
    # print 'theta:', t1 * RAD2DEG
    return t1

    # num2 = math.sqrt(962361 * x * x + 1.6e9) + 40000
    # denom = 981 * x
    # t2 = -2 * math.atan2(num2, denom)
    # print t2 * RAD2DEG







if __name__ == '__main__':
    main()
