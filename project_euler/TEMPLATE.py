#!/usr/bin/env python

from __future__ import division

import time
import primefac
from itertools import count


"""

"""
def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()


    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

### HELPER FUNCTIONS ###




def assertEqual(a, b):
    if a != b:
        print 'a: {}'.format(a)
        print 'b: {}'.format(b)
    assert a == b


if __name__ == '__main__':
    main()
