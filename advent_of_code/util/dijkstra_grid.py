
import math

from advent_of_code.util import aoc_util
from advent_of_code.util.grid_2d import Grid2D
from advent_of_code.util.min_heap import MinHeap


class Node(object):

    def __init__(self, coord):
        self.coord = coord
        self.dist = math.inf
        self.path = []

    def __repr__(self):
        return '{}: {}'.format(type(self).__name__, self.coord)

    def __eq__(self, other):
        return self.coord == other.coord

    def __hash__(self):
        return hash(self.coord)

    def __lt__(self, other):
        return aoc_util.is_reading_order(self.coord, other.coord)

    def is_better_than(self, other):
        return self.dist < other.dist


class DijkstraGrid(Grid2D):

    def find_shortest_path(self, start_coord, open_chars, goal_chars):
        """
        Args:
            start_coord (tuple):
            open_chars (set[str]):
            goal_chars (set[str]):

        Returns:
            list[tuple]:

        given:
            start coord
            open chars (can path through)
            goal chars (done when we hit)
            end?

        assume:
            cant move diag

        algo:
            keep a pq of nodes (just starts with one)

            while pq:
                select node at shortest dist (reading order)
                mark as visited
                check if done (goal reached)
                update dist to all reachable nodes
        """

        priority_queue = MinHeap()

        start_node = Node(start_coord)
        start_node.dist = 0
        # start_node.path.append(start_coord)

        all_nodes = {
            start_coord: Node(start_coord)
        }

        priority_queue.insert(start_node, 0)

        while priority_queue:

            # select node at shortest distance
            selected_node = priority_queue.pop()  # type: Node
            # print('\nselected_node: {}'.format(selected_node))

            # check if done
            char_at_coord = self.get_top(selected_node.coord)
            if char_at_coord in goal_chars:
                return selected_node.path

            # update dist to reachable nodes
            for adj_coord in self.get_adjacent_coords(selected_node.coord):

                char_at_coord = self.get_top(adj_coord)
                # print(char_at_coord)

                if char_at_coord in open_chars or char_at_coord in goal_chars:
                    # coord is valid

                    # create the potential new node
                    new_node = Node(adj_coord)
                    new_node.dist = selected_node.dist + 1
                    new_node.path = selected_node.path.copy()
                    new_node.path.append(adj_coord)

                    # check if we should skip
                    if adj_coord in all_nodes:
                        prev_node = all_nodes[adj_coord]
                        if not new_node.is_better_than(prev_node):
                            # skip since the new node is not better
                            continue
                        else:
                            print('dont know if this happens...')

                    # add node
                    all_nodes[adj_coord] = new_node
                    priority_queue.insert(new_node, new_node.dist)

        return []  # no path found




