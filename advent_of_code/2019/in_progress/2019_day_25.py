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

addToPath('../..')

### IMPORTS ###

import aocd

from aoc_util import aoc_util
from aoc_util.aoc_util import AocLogger
from aoc_util.intcode_computer import IntcodeComputer






class Droid(IntcodeComputer):
    """
    --- Day 25: Cryostasis ---
    As you approach Santa's ship, your sensors report two important details:

    First, that you might be too late: the internal temperature is -40 degrees.

    Second, that one faint life signature is somewhere on the ship.

    The airlock door is locked with a code; your best option is to send in a small droid to investigate the
    situation. You attach your ship to Santa's, break a small hole in the hull, and let the droid run in before you
    seal it up again. Before your ship starts freezing, you detach your ship and set it to automatically stay within
    range of Santa's ship.

    This droid can follow basic instructions and report on its surroundings; you can communicate with it through an
    Intcode program (your puzzle input) running on an ASCII-capable computer.

    As the droid moves through its environment, it will describe what it encounters. When it says Command?,
    you can give it a single instruction terminated with a newline (ASCII code 10). Possible instructions are:

     - Movement via north, south, east, or west.
     - To take an item the droid sees in the environment, use the command take <name of item>. For example, if the droid reports seeing a red ball, you can pick it up with take red ball.
     - To drop an item the droid is carrying, use the command drop <name of item>. For example, if the droid is carrying a green ball, you can drop it with drop green ball.
     - To get a list of all of the items the droid is currently carrying, use the command inv (for "inventory").

    Extra spaces or other characters aren't allowed - instructions must be provided precisely.

    Santa's ship is a Reindeer-class starship; these ships use pressure-sensitive floors to determine the identity of
    droids and crew members. The standard configuration for these starships is for all droids to weigh exactly the
    same amount to make them easier to detect. If you need to get past such a sensor, you might be able to reach the
    correct weight by carrying items from the environment.

    Look around the ship and see if you can find the password for the main airlock.
    """

    directions = {
        'w': 'north',
        'd': 'east',
        's': 'south',
        'a': 'west',
    }

    dont_take = {
        'infinite loop',
        'photons',
        'escape pod',
        'giant electromagnet',
        'molten lava',
    }

    def __init__(self, initial_memory):
        super().__init__(initial_memory)

        self.do_auto_take = True

    def run_droid(self):

        while True:
            cmd = ''
            self.clear_output()

            self.run_to_input_needed()

            if self.do_auto_take:
                cmd = self.auto_take()

            if not cmd:
                cmd = input()

                if cmd in self.directions:
                    print('{} -> {}'.format(cmd, self.directions[cmd]))
                    cmd = self.directions[cmd]

                # if cmd == 't':
                #     self.take()

            self.queue_input_string(cmd)

            if cmd.startswith('take'):
                self.queue_input_string('inv')

    def try_combos(self):
        pass

    def auto_take(self):
        ITEMS_HERE = 'Items here:'
        CHECKPOINT = '== Security Checkpoint =='
        cmd = ''

        # get text
        text = self.get_output_string()
        if ITEMS_HERE not in text or CHECKPOINT in text:
            # can't do auto take
            return ''

        # get list of items
        text = text.split(ITEMS_HERE)[-1]
        items = [x[2:] for x in aoc_util.stripped_lines(text) if x.startswith('- ')]
        safe_items = [x for x in items if x not in self.dont_take]

        if len(safe_items) == 1:
            cmd = 'take {}'.format(items[0])

        # cmd = input('which item: {}?\n'.format(items))
        # for item in items:
        #     if item.lower().startswith(cmd):
        #         cmd = 'take {}'.format(item)
        #         break

        return cmd





def main():
    print('starting {}'.format(__file__.split('/')[-1]))

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    droid = Droid(puzzle_input)
    droid.run_droid()





if __name__ == '__main__':
    main()




