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

addToPath('../../..')

### IMPORTS ###

import time
import traceback

import aocd

from advent_of_code.util import aoc_util
from advent_of_code.util.aoc_util import AocLogger


### CONSTANTS ###
TEST_INPUT = [
    """
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
    """, """

    """, """

    """
]

TEST_OUTPUT_1 = [
    138,
    0,
    0,
]

TEST_OUTPUT_2 = [
    66,
    0,
    0,
]










class AdventOfCode(object):
    """
    https://adventofcode.com
    """

    def run(self):
        print('starting {}'.format(__file__.split('/')[-1]))
        start_time = time.time()

        try:
            puzzle_input = aocd.data
        except aocd.exceptions.AocdError:
            print(traceback.format_exc())
            puzzle_input = 'unable to get input'
        aoc_util.write_input(puzzle_input, __file__)

        self.run_tests()

        AocLogger.verbose = False

        aoc_util.assert_equal(
            38722,
            self.solve_part_1(puzzle_input)
        )

        aoc_util.assert_equal(
            13935,
            self.solve_part_2(puzzle_input)
        )

        elapsed_time = time.time() - start_time
        print('elapsed_time: {:.3f} sec'.format(elapsed_time))

    def run_tests(self):
        AocLogger.verbose = True
        aoc_util.run_tests(self.solve_part_1, TEST_INPUT, TEST_OUTPUT_1)
        aoc_util.run_tests(self.solve_part_2, TEST_INPUT, TEST_OUTPUT_2)

    def solve_part_1(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_1_result = solver.p1()

        print('part_1_result: {}'.format(part_1_result))
        return part_1_result

    def solve_part_2(self, puzzle_input: str):
        solver = Solver(puzzle_input)

        part_2_result = solver.p2()

        print('part_2_result: {}'.format(part_2_result))
        return part_2_result










class Node(object):

    def __init__(self):
        self.next = 0  # points to next index after node

        self.num_children = 0
        self.children = []

        self.num_metadata = 0
        self.metadata = []

    def __repr__(self):
        return 'Node: {}'.format(self.metadata)

    def recursive_sum(self):
        result = sum(self.metadata)
        for x in self.children:  # type: Node
            result += x.recursive_sum()
        return result

    def calc_value(self):
        """
        The second check is slightly more complicated: you need to find the value of the root node
        (A in the example above).

        The value of a node depends on whether it has child nodes.

        If a node has no child nodes, its value is the sum of its metadata entries. So, the value of node B is
        10+11+12=33, and the value of node D is 99.

        However, if a node does have child nodes, the metadata entries become indexes which refer to those child
        nodes. A metadata entry of 1 refers to the first child node, 2 to the second, 3 to the third, and so on. The
        value of this node is the sum of the values of the child nodes referenced by the metadata entries. If a
        referenced child node does not exist, that reference is skipped. A child node can be referenced multiple time
        and counts each time it is referenced. A metadata entry of 0 does not refer to any child node.

        For example, again using the above nodes:

            Node C has one metadata entry, 2. Because node C has only one child node, 2 references a child node which
            does not exist, and so the value of node C is 0.

            Node A has three metadata entries: 1, 1, and 2. The 1 references node A's first child node, B, and the 2
            references node A's second child node, C. Because node B has a value of 33 and node C has a value of 0,
            the value of node A is 33+33+0=66. So, in this example, the value of the root node is 66.

        What is the value of the root node?
        """
        if not self.children:
            return sum(self.metadata)
        else:
            result = 0
            for x in self.metadata:
                node_index = x - 1
                try:
                    child = self.children[node_index]  # type: Node
                    result += child.calc_value()
                except IndexError:
                    pass
            return result










class Solver(object):

    def __init__(self, text: str):
        self.text = text.strip()

        numbers = aoc_util.ints(self.text)
        self.root_node = self.recursive_parse_node(numbers, 0)

        AocLogger.log(str(self))

    def __repr__(self):
        return '{}:\n{}\n'.format(
            type(self).__name__, self.text)

    def p1(self):
        """
        The sleigh is much easier to pull than you'd expect for something its weight. Unfortunately, neither you nor
        the Elves know which way the North Pole is from here.

        You check your wrist device for anything that might help. It seems to have some kind of navigation system!
        Activating the navigation system produces more bad news: "Failed to start navigation system. Could not read
        software license file."

        The navigation system's license file consists of a list of numbers (your puzzle input). The numbers define a
        data structure which, when processed, produces some kind of tree that can be used to calculate the license
        number.

        The tree is made up of nodes; a single, outermost node forms the tree's root, and it contains all other nodes
        in the tree (or contains nodes that contain nodes, and so on).

        Specifically, a node consists of:
            A header, which is always exactly two numbers:
                The quantity of child nodes.
                The quantity of metadata entries.
            Zero or more child nodes (as specified in the header).
            One or more metadata entries (as specified in the header).

        Each child node is itself a node that has its own header, child nodes, and metadata. For example:

        2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
        A----------------------------------
            B----------- C-----------
                             D-----

        In this example, each node of the tree is also marked with an underline starting with a letter for easier
        identification. In it, there are four nodes:
            A, which has 2 child nodes (B, C) and 3 metadata entries (1, 1, 2).
            B, which has 0 child nodes and 3 metadata entries (10, 11, 12).
            C, which has 1 child node (D) and 1 metadata entry (2).
            D, which has 0 child nodes and 1 metadata entry (99).

        The first check done on the license file is to simply add up all of the metadata entries. In this example,
        that sum is 1+1+2+10+11+12+2+99=138.

        What is the sum of all metadata entries?
        """
        result = self.root_node.recursive_sum()
        return result

    def recursive_parse_node(self, array, start_index):
        result = Node()
        result.num_children = array[start_index]
        result.num_metadata = array[start_index + 1]

        # parse children
        next_index = start_index + 2
        for x in range(result.num_children):
            child = self.recursive_parse_node(array, next_index)
            result.children.append(child)
            next_index = child.next

        # parse metadata
        for x in range(result.num_metadata):
            result.metadata.append(array[next_index])
            next_index += 1

        result.next = next_index
        return result

    def p2(self):
        result = self.root_node.calc_value()
        return result










if __name__ == '__main__':
    instance = AdventOfCode()
    instance.run()




