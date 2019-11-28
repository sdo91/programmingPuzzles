#!/usr/bin/env python

from __future__ import division

import time
import random
import operator

from collections import namedtuple


NUM_NETS = 100
NUM_SIMS = 1e5
NUM_REPLACEMENTS = 50


class Net(object):

    def __init__(self, percent):
        self.percent = percent
        self.uses = 0
        self.captures = 0
        self.resets = 0

    def reset(self):
        self.uses = 0
        self.captures = 0
        self.resets += 1

    def getSimSuccess(self):
        if self.uses == 0:
            return 0
        return self.captures / self.uses

    def __str__(self):
        return 'net: {:.2f}%, {}/{}, {:.2f}%, {}'.format(
            self.percent * 100,
            self.captures,
            self.uses,
            self.getSimSuccess() * 100,
            self.resets,
        )

    def __repr__(self):
        # return str(self)
        return '\n' + str(self)



"""
https://fivethirtyeight.com/features/who-will-capture-the-most-james-bonds/

"""
def main():
    print 'starting {}'.format(__file__.split('/')[-1])
    startTime = time.time()

    ### gen list of nets ###
    nets_list = []
    for x in range(1, int(NUM_NETS) + 1):
        # n = Net(x / NUM_NETS)
        n = Net(random.random())
        nets_list.append(n)
    #     print n
    # print nets_list

    ### sim ###
    for i in xrange(NUM_REPLACEMENTS):
        if i != 0:
            ### replace nets ###
            print 'replace: {}'.format(i)
            nets_list.sort(
                key=operator.methodcaller('getSimSuccess'),
                reverse=1)
            nets_list = nets_list[:int(NUM_NETS * 0.9)]
            for net in nets_list:
                net.reset()
            while len(nets_list) < NUM_NETS:
                nets_list.append(Net(random.random()))
            # print '{}: {}'.format(i, nets_list)


        doSim(nets_list)

        ### show results ###
        nets_list.sort(key=operator.methodcaller('getSimSuccess'), reverse=0)
        print '{}: {}'.format(i, nets_list[-10:])




    elapsedTime = time.time() - startTime
    print 'elapsedTime: {:.2f} s'.format(elapsedTime)
# end main

### HELPER FUNCTIONS ###

def doSim(nets_list):
    noCapture = 0
    for x in xrange(int(NUM_SIMS)):
        # if x % int(NUM_SIMS / 10) == 0:
        #     print x

        ### pick 3 random indexes ###
        indexes = set()
        while len(indexes) < 3:
            indexes.add(getRandIdx(nets_list))
        # print indexes

        ### order by percent ###
        orderedNets = []
        for i in indexes:
            nets_list[i].uses += 1
            orderedNets.append(nets_list[i])
        orderedNets.sort(key=operator.attrgetter('percent'))
        # print orderedNets

        ### run the sim, inc counters ###
        noCapture += 1
        for net in orderedNets:
            if net.percent > random.random():
                # net hit!
                net.captures += 1
                noCapture -= 1
                break
        # print orderedNets
    # print 'noCapture:', noCapture



def getRandIdx(x):
    return random.randint(0, len(x) - 1)


def assertEqual(a, b):
    if a != b:
        print 'a: {}'.format(a)
        print 'b: {}'.format(b)
    assert a == b


if __name__ == '__main__':
    main()
