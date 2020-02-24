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
from aoc_util.grid_2d import Grid2D
from aoc_util.recursive_pathfinder_droid import RecursivePathfinderDroid





### CONSTANTS ###

TEST_INPUT = [
    """
         A
         A
  #######.#########
  #######.........#
  #######.#######.#
  #######.#######.#
  #######.#######.#
  #####  B    ###.#
BC...##  C    ###.#
  ##.##       ###.#
  ##...DE  F  ###.#
  #####    G  ###.#
  #########.#####.#
DE..#######...###.#
  #.#########.###.#
FG..#########.....#
  ###########.#####
             Z
             Z
    """, """
                   A
                   A
  #################.#############
  #.#...#...................#.#.#
  #.#.#.###.###.###.#########.#.#
  #.#.#.......#...#.....#.#.#...#
  #.#########.###.#####.#.#.###.#
  #.............#.#.....#.......#
  ###.###########.###.#####.#.#.#
  #.....#        A   C    #.#.#.#
  #######        S   P    #####.#
  #.#...#                 #......VT
  #.#.#.#                 #.#####
  #...#.#               YN....#.#
  #.###.#                 #####.#
DI....#.#                 #.....#
  #####.#                 #.###.#
ZZ......#               QG....#..AS
  ###.###                 #######
JO..#.#.#                 #.....#
  #.#.#.#                 ###.#.#
  #...#..DI             BU....#..LF
  #####.#                 #.#####
YN......#               VT..#....QG
  #.###.#                 #.###.#
  #.#...#                 #.....#
  ###.###    J L     J    #.#.###
  #.....#    O F     P    #.#...#
  #.###.#####.#.#####.#####.###.#
  #...#.#.#...#.....#.....#.#...#
  #.#####.###.###.#.#.#########.#
  #...#.#.....#...#.#.#.#.....#.#
  #.###.#####.###.###.#.#.#######
  #.#.........#...#.............#
  #########.###.###.#############
           B   J   C
           U   P   P
    """, """
         A
         A
  #######.#########
  #######........##
  #######.#######.#
  #######.#######.#
  #######.#######.#
  #####  B    ###.#
BC...##  C  HI....#
  ##.##       ###.#
  ##...DE  F  ###.#
  #####    G  ###.#
  #########.#####.#
DE..#######..####.#
  #.#######.#.###.#
FG..#######.#.....#
  #########.#.#####
           H Z
           I Z
    """, """
             Z L X W       C
             Z P Q B       K
  ###########.#.#.#.#######.###############
  #...#.......#.#.......#.#.......#.#.#...#
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###
  #.#...#.#.#...#.#.#...#...#...#.#.......#
  #.###.#######.###.###.#.###.###.#.#######
  #...#.......#.#...#...#.............#...#
  #.#########.#######.#.#######.#######.###
  #...#.#    F       R I       Z    #.#.#.#
  #.###.#    D       E C       H    #.#.#.#
  #.#...#                           #...#.#
  #.###.#                           #.###.#
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#
CJ......#                           #.....#
  #######                           #######
  #.#....CK                         #......IC
  #.###.#                           #.###.#
  #.....#                           #...#.#
  ###.###                           #.#.#.#
XF....#.#                         RF..#.#.#
  #####.#                           #######
  #......CJ                       NM..#...#
  ###.#.#                           #.###.#
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#
  #.....#        F   Q       P      #.#.#.#
  ###.###########.###.#######.#########.###
  #.....#...#.....#.......#...#.....#.#...#
  #####.#.###.#######.#######.###.###.#.#.#
  #.......#.......#.#.#.#.#...#...#...#.#.#
  #####.###.#####.#.#.#.#.###.###.#.###.###
  #.......#.....#.#...#...............#...#
  #############.#.#.###.###################
               A O F   N
               A A D   M
    """
]

AA = 'AA'
ZZ = 'ZZ'
INF = 9e9











class Portal(object):
    def __init__(self):
        self.id = ''
        self.coord = (0, 0)

    def __str__(self):
        return '{} @ {}'.format(self.id, self.coord)

    def __repr__(self):
        return str(self)


class Node(object):
    def __init__(self, id):
        """
        Args:
            id (str):
        """
        self.id = id
        self.dist = INF
        self.path = []
        self.level = 0

    def __repr__(self):
        return 'id={}, dist={}, path={}'.format(self.id, self.dist, self.path)







class DonutDroid(RecursivePathfinderDroid):
    """
    given:
        the donut map
        the dict of portals
        a starting portal

    find:
        reachable portals
        their distances

    """

    def __init__(self, maze):
        super().__init__()

        self.maze = maze

        self.reachable_by_start = {}
        self.current_start = None


    def find_all_reachable(self):
        for id in self.maze.portals_by_id:
            self.find_reachable(id)
        return self.reachable_by_start


    def find_reachable(self, start_portal):
        """
        find the shortest distance to all portals reachable from the start portal

        example:
            given:
                AA

            find:
                BC: 4
                ZZ: 26
                FG: 30
        """
        self.current_start = start_portal
        self.reachable_by_start[self.current_start] = {}

        start_coord = self.maze.portals_by_id[start_portal].coord

        self.x, self.y = start_coord
        self.desired_x, self.desired_y = start_coord

        path_so_far = [start_coord]
        self._try_all_directions(path_so_far)

        # add other side of portal
        if start_portal.endswith('in') or start_portal.endswith('out'):
            linked_portal = self.flip_side(start_portal)
            self.reachable_by_start[self.current_start][linked_portal] = 1


    def flip_side(self, name):
        """
        Args:
            name (str):

        Returns:
            str
        """
        if name.endswith('in'):
            return name.replace('in', 'out')
        else:
            return name.replace('out', 'in')


    def move(self, direction):
        if self.maze.get(self.desired_x, self.desired_y) != '.':
            return self.STATUS_HIT_WALL

        # do the move
        self.x = self.desired_x
        self.y = self.desired_y
        self.maze.overlay = {
            (self.x, self.y): '@'
        }

        return self.STATUS_MOVED


    def process_new_path(self, new_path):
        if self.get_current() in self.maze.portals_by_coord:
            AocLogger.log('hit a portal: (path={})'.format(new_path))
            if AocLogger.verbose:
                self.maze.show()

            portal = self.maze.portals_by_coord[self.get_current()]
            reachable_dict = self.reachable_by_start[self.current_start]
            if portal.id in reachable_dict:
                raise RuntimeError

            reachable_dict[portal.id] = len(new_path) - 1











class DonutMaze(Grid2D):
    """
    algo:
        find all portals

        for each portal:
            find all reachable portals and their distances

        ex: start at AA:
            find BC_in, ZZ, FG_in
    """

    def __init__(self, text, is_part_2=False):
        # read into grid
        super().__init__(text)

        self.is_part_2 = is_part_2

        print('\n' * 5)
        print('loaded maze:')
        self.show()

        # find all portals
        self.portals_by_id = {}
        self.portals_by_coord = {}
        for y in range(self.max_y):
            for x in range(self.max_x):
                if self.is_value((x, y), '.'):
                    # check if there is an adj letter
                    adj_portal = self.get_portal(x, y)
                    if adj_portal:
                        AocLogger.log('portal found: {}'.format(adj_portal))
                        self.portals_by_id[adj_portal.id] = adj_portal
                        self.portals_by_coord[adj_portal.coord] = adj_portal

        print()
        AocLogger.log_dict(self.portals_by_id, 'portals_by_id')
        AocLogger.log_dict(self.portals_by_coord, 'portals_by_coord')

        # find reachable portals
        dd = DonutDroid(self)
        self.reachable_dict = dd.find_all_reachable()
        AocLogger.log_dict(self.reachable_dict, 'reachable_dict')
        self.test_get_reachable()

        print('DonutMaze ready')
        print()


    def find_shortest_path(self):
        """
        find shortest path from AA to ZZ using dijkstra's algo

        Returns:
            int: dist in steps

        algo:
            while there are unvisited nodes:
                select the node N at the shortest dist
                update dist to all nodes reachable from N

        part 2 algo:
            setup:
                all nodes dict should contain all level 0 portals
                make a get reachable function
        """
        ### do setup ###
        all_nodes_dict = {}

        for key in self.reachable_dict:
            if self.is_part_2:
                if 'out' in key:
                    continue
                key = '0_' + key

            all_nodes_dict[key] = Node(key)
            if AA in key:
                all_nodes_dict[key].dist = 0
                all_nodes_dict[key].path.append(key)

        AocLogger.log_dict(all_nodes_dict, 'all_nodes_dict')
        unvisited_nodes = set(all_nodes_dict.keys())

        ### do main algo loop ###
        while unvisited_nodes:
            # select node at shortest distance
            min_dist = INF
            selected_node = ''
            for node_name in unvisited_nodes:
                if all_nodes_dict[node_name].dist < min_dist:
                    min_dist = all_nodes_dict[node_name].dist
                    selected_node = node_name

            AocLogger.log('selected: {}'.format(all_nodes_dict[selected_node]))

            # check if done
            if ZZ in selected_node:
                print('shortest path found: {}'.format(all_nodes_dict[selected_node]))
                return all_nodes_dict[selected_node].dist

            # mark as visited
            unvisited_nodes.remove(selected_node)

            # update dist to all nodes reachable
            dist_to_selected = all_nodes_dict[selected_node].dist
            for reachable_node in self.get_reachable(selected_node):
                dist_selected_to_reachable = self.get_dist_to_reachable(selected_node, reachable_node)
                dist_via_selected = dist_to_selected + dist_selected_to_reachable

                if reachable_node not in all_nodes_dict:
                    all_nodes_dict[reachable_node] = Node(reachable_node)
                    unvisited_nodes.add(reachable_node)

                if dist_via_selected < all_nodes_dict[reachable_node].dist:
                    # update shortest path to node
                    all_nodes_dict[reachable_node].dist = dist_via_selected
                    all_nodes_dict[reachable_node].path = all_nodes_dict[selected_node].path.copy()
                    all_nodes_dict[reachable_node].path.append(reachable_node)

        raise RuntimeError('unreachable')


    def get_dist_to_reachable(self, selected, reachable):
        if self.is_part_2:
            return self.reachable_dict[self.get_portal_id(selected)][self.get_portal_id(reachable)]
        else:
            return self.reachable_dict[selected][reachable]


    def get_portal_id(self, id_with_level):
        i = id_with_level.index('_')
        return id_with_level[i + 1:]


    def get_reachable(self, start_portal):
        """
        Args:
            start_portal (str):

        Returns:
            dict:

        algo:
            get reachable no levels

            for each key:
                if same level:
                    if level 0:
                        filter outside portals
                    else:
                        filter AA, ZZ
                else: (paired portal)
                    keep, but mod level

        """
        if self.is_part_2:
            i = start_portal.index('_')

            portal_id = start_portal[i + 1:]
            portal_letters = portal_id.replace('_in', '').replace('_out', '')
            level = int(start_portal[:i])

            reachable_no_levels = self.reachable_dict[portal_id]
            result = {}

            for key in reachable_no_levels:
                if portal_letters in key:
                    # this is the paired portal
                    if start_portal.endswith('_out'):
                        new_level = level - 1
                    else:
                        new_level = level + 1

                    new_key = '{}_{}'.format(new_level, key)
                    result[new_key] = reachable_no_levels[key]
                else:
                    # portal is on the same level
                    if level == 0:
                        # skip outside portals
                        if key.endswith('_out'):
                            continue
                    else:
                        # skip AA/ZZ
                        if key in {AA, ZZ}:
                            continue

                    # otherwise, keep the portal
                    new_key = '{}_{}'.format(level, key)
                    result[new_key] = reachable_no_levels[key]

            # AocLogger.log('reachable from {}: {}'.format(start_portal, result))
            return result
        else:
            return self.reachable_dict[start_portal]


    def test_get_reachable(self):
        if self.is_part_2 and AocLogger.verbose:
            self.get_reachable('0_AA')
            self.get_reachable('0_BC_in')
            # self.get_reachable('0_BC_out')
            self.get_reachable('0_DE_in')
            # self.get_reachable('0_DE_out')
            self.get_reachable('1_BC_in')
            self.get_reachable('1_BC_out')
            self.get_reachable('1_DE_in')
            self.get_reachable('1_DE_out')


    def is_outside(self, x, y):
        THRESHOLD = 4
        if x < THRESHOLD or x > self.max_x - THRESHOLD:
            return True
        if y < THRESHOLD or y > self.max_y - THRESHOLD:
            return True
        return False


    def get_portal(self, x, y):
        result_str = ''
        adj_coords = self.get_adjacent_coords((x, y))
        for c in adj_coords:
            if self.get(*c).isalpha():
                # 1st char found, get 2nd

                n = self.get_coord_north(c)
                if self.get(*n).isalpha():
                    result_str = self.get(*n) + self.get(*c)
                    break

                w = self.get_coord_west(c)
                if self.get(*w).isalpha():
                    result_str = self.get(*w) + self.get(*c)
                    break

                s = self.get_coord_south(c)
                if self.get(*s).isalpha():
                    result_str = self.get(*c) + self.get(*s)
                    break

                e = self.get_coord_east(c)
                if self.get(*e).isalpha():
                    result_str = self.get(*c) + self.get(*e)
                    break

        if result_str not in {'', AA, ZZ}:
            if self.is_outside(x, y):
                result_str += '_out'
            else:
                result_str += '_in'

        if result_str:
            result_portal = Portal()
            result_portal.id = result_str
            result_portal.coord = (x, y)
            return result_portal
        else:
            return None














def main():
    print('starting {}'.format(__file__.split('/')[-1]))

    try:
        puzzle_input = aocd.data
    except aocd.exceptions.AocdError:
        puzzle_input = 'unable to get input'
    aoc_util.write_input(puzzle_input, __file__)

    AocLogger.verbose = True
    run_tests()

    AocLogger.verbose = False

    aoc_util.assert_equal(
        644,
        solve_part_1(puzzle_input)
    )

    aoc_util.assert_equal(
        7798,
        solve_part_2(puzzle_input)
    )


def run_tests():
    ### part 1 ###
    AocLogger.verbose = True
    aoc_util.assert_equal(
        23,
        solve_part_1(TEST_INPUT[0])
    )
    AocLogger.verbose = False
    aoc_util.assert_equal(
        58,
        solve_part_1(TEST_INPUT[1])
    )
    aoc_util.assert_equal(
        37,
        solve_part_1(TEST_INPUT[2])
    )
    aoc_util.assert_equal(
        77,
        solve_part_1(TEST_INPUT[3])
    )

    # ### part 2 ###
    AocLogger.verbose = True
    aoc_util.assert_equal(
        37,
        solve_part_2(TEST_INPUT[2])
    )


def solve_part_1(text):
    AocLogger.log('input text:\n{}'.format(text))

    dm = DonutMaze(text)
    part_1_result = dm.find_shortest_path()

    print('part_1_result: {}'.format(part_1_result))
    return part_1_result


def solve_part_2(text):
    AocLogger.log('input text:\n{}'.format(text))

    dm = DonutMaze(text, is_part_2=True)
    part_2_result = dm.find_shortest_path()

    print('part_2_result: {}'.format(part_2_result))
    return part_2_result





if __name__ == '__main__':
    main()



