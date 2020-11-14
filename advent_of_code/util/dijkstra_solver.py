
from advent_of_code.util.dijkstra_node import Node
from advent_of_code.util.grid_2d import Grid2D
from advent_of_code.util.min_heap import MinHeap


class DijkstraSolver(object):

    def __init__(self, grid, open_chars, goal_chars):
        self.grid = grid  # type: Grid2D
        self.open_chars = open_chars  # type: set
        self.goal_chars = goal_chars  # type: set

    def is_done(self, coord):
        char_at_coord = self.grid.get_top(coord)
        return char_at_coord in self.goal_chars

    def get_adjacent(self, coord):
        return self.grid.get_adjacent_coords(coord)

    def can_reach(self, coord):
        char_at_coord = self.grid.get_top(coord)
        return char_at_coord in self.open_chars or char_at_coord in self.goal_chars

    def find_shortest_path(self, start_coord):
        """
        Args:
            start_coord (tuple):

        Returns:
            list[tuple]: the coords that make up a shortest path (reading order)

        given:
            start coord
            open chars (can path through)
            goal chars (done when we hit)

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

        priority_queue = MinHeap()  # unvisited

        start_node = Node(start_coord)
        start_node.dist = 0
        # start_node.path.append(start_coord)

        all_nodes = {
            start_coord: Node(start_coord)
        }

        priority_queue.insert(start_node, 0)

        # while queue not empty
        while priority_queue:

            # select node at shortest distance
            selected_node = priority_queue.pop()  # type: Node
            # print('\nselected_node: {}'.format(selected_node))

            # check if done
            if self.is_done(selected_node.coord):
                return selected_node.path

            # update dist to reachable nodes
            for adj_coord in self.get_adjacent(selected_node.coord):

                if self.can_reach(adj_coord):
                    # coord is valid

                    # create the potential new node
                    new_node = Node(adj_coord)
                    new_node.dist = selected_node.dist + 1
                    new_node.path = selected_node.path.copy()
                    new_node.path.append(adj_coord)

                    # check if the new node is better
                    if adj_coord in all_nodes:
                        prev_node = all_nodes[adj_coord]
                        if not new_node.is_better_than(prev_node):
                            # skip since the new node is not better
                            continue

                    # add node (node is new, or better than old)
                    all_nodes[adj_coord] = new_node
                    priority_queue.insert(new_node, new_node.dist)

        return []  # no path found




