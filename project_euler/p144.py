#!/usr/bin/env python

from __future__ import division

import time
import math
import primefac
from itertools import count


"""
Investigating multiple reflections of a laser beam
Problem 144 

In laser physics, a "white cell" is a mirror system that acts as a delay line for the laser beam. 
The beam enters the cell, bounces around on the mirrors, and eventually works its way back out.

The specific white cell we will be considering is an ellipse with the equation 4x**2 + y**2 = 100

The section corresponding to -0.01 <= x <= +0.01 at the top is missing, 
allowing the light to enter and exit through the hole.


The light beam in this problem starts at the point (0.0,10.1) just outside the white cell, 
and the beam first impacts the mirror at (1.4,-9.6).

Each time the laser beam hits the surface of the ellipse, 
it follows the usual law of reflection "angle of incidence equals angle of reflection." 
That is, both the incident and reflected beams make the same angle with the normal line 
at the point of incidence.

In the figure on the left, the red line shows the first two points of contact 
between the laser beam and the wall of the white cell; 
the blue line shows the line tangent to the ellipse at the point of incidence of the first bounce.

The slope m of the tangent line at any point (x,y) of the given ellipse is: m = -4x/y

The normal line is perpendicular to this tangent line at the point of incidence.

The animation on the right shows the first 10 reflections of the beam.

How many times does the beam hit the internal surface of the white cell before exiting?
"""
def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()

    # print calcFibonacci(13)

    # calc starting slope
    x1, y1 = 0, 10.1
    x2, y2 = 1.4, -9.6
    m = (y2 - y1) / (x2 - x1)
    print 'slope:', m

    x2, y2 = findNextIntersection(x1, y1, m)
    print x2, y2
    print calcTanLine(x2, y2, m)

    '''
    given a line, calc the next point of intersection
    calc the tangent line
    calc the next line
    repeat
    '''

    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

### HELPER FUNCTIONS ###

def calcTanLine(x, y, m_beam):
    """
    given a point, the slope of the incoming beam, the slope of the tan line,
    find the slope of the outgoing beam

    m = -4x/y
    """
    m_tan = -4 * x / y
    print m_tan
    m_normal = y / (-4 * x)
    print m_normal

def findNextIntersection(x1, y1, m):
    """
    4x**2 + y**2 = 100
    (0.0,10.1) (1.4,-9.6)
    y - y1 = m(x - x1)

    given point, slope, calc int
    y = m(x - x1) + y1
    y = mx - (m*x1+y1)
    b = (-m * x1) + y1
    y = mx + b
    4x**2 + (above)**2 = 100
    4x**2 + (mx + b)(mx + b) = 100
    4x**2 + m**2x**2 + 2bmx + b**2 = 100
    (4+m**2)x**2 + (2bm)x + (b**2-100) = 0
    """
    x1, y1 = 0, 10.1
    # x2, y2 = 1.4, -9.6
    # m = (y2 - y1) / (x2 - x1)
    # print 'slope:', m
    b = (-m * x1) + y1
    # print 'b:', b

    A = 4 + m**2
    B = 2 * b * m
    C = b**2 - 100

    x2 = solveQuadratic(A, B, C)
    y2 = m * x2 + b
    # print x2, y2
    return x2, y2





def solveQuadratic(A, B, C, doMinus=False):
    descriminant = (B ** 2) - (4 * A * C)
    # print descriminant
    if not doMinus:
        return (-B + math.sqrt(descriminant)) / (2 * A)
    else:
        return (-B - math.sqrt(descriminant)) / (2 * A)

def calcFibonacci(numTerms):
    result = [1, 1]
    for x in xrange(numTerms - 2):
        result.append(result[-1] + result[-2])
    return result

def assertEqual(a, b):
    if a != b:
        print 'a: {}'.format(a)
        print 'b: {}'.format(b)
    assert a == b


if __name__ == '__main__':
    main()
