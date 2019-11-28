#!/usr/bin/env python3

def addToPath(relPath):
    from os import path
    import sys
    dirOfThisFile = path.dirname(path.realpath(__file__))
    dirToAdd = path.normpath(path.join(dirOfThisFile, relPath))
    if dirToAdd not in sys.path:
        print('adding to path: {}'.format(dirToAdd))
        sys.path.insert(0, dirToAdd)
    else:
        print('already in path: {}'.format(dirToAdd))

# addToPath('.')

### IMPORTS ###





class MyClass(object):

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))

# end MyClass





### HELPER FUNCTIONS ###





if __name__ == '__main__':
    instance = MyClass()
    instance.run()




