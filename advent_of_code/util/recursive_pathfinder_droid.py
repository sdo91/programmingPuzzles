




class RecursivePathfinderDroid(object):
    """
    used for AOC 2019 days 15, 18, 20
    """

    OPPOSITE_DIRECTIONS = {
        'n': 's',
        's': 'n',
        'w': 'e',
        'e': 'w',
    }

    DX = {
        'n': 0,
        's': 0,
        'w': -1,
        'e': 1,
    }

    DY = {
        'n': -1,
        's': 1,
        'w': 0,
        'e': 0,
    }

    STATUS_HIT_WALL = 0
    STATUS_MOVED = 1
    STATUS_HIT_GOAL = 2

    def __init__(self):
        self.x = 0
        self.y = 0
        self.desired_x = 0
        self.desired_y = 0

    def get_current(self):
        return self.x, self.y

    def _get_desired(self, direction):
        return self.x + self.DX[direction], self.y + self.DY[direction]

    def _update_desired(self, direction):
        self.desired_x, self.desired_y = self._get_desired(direction)

    def find_min_num_moves(self):
        path_so_far = [self.get_current()]
        result_path = self._try_all_directions(path_so_far)
        print('path found: {}'.format(result_path))

        result = len(result_path) - 1
        print('fewest moves: {}'.format(result))
        return result

    def _try_all_directions(self, path_so_far):
        candidate_paths = []
        candidate_paths.append(self._recursive_find_path('n', path_so_far))
        candidate_paths.append(self._recursive_find_path('s', path_so_far))
        candidate_paths.append(self._recursive_find_path('w', path_so_far))
        candidate_paths.append(self._recursive_find_path('e', path_so_far))

        # choose best path
        min_len = 9e9
        best_path = None  # default if no path can get to goal
        for cand in candidate_paths:
            if cand is None:
                continue
            if len(cand) < min_len:
                min_len = len(cand)
                best_path = cand

        return best_path

    def _recursive_find_path(self, direction, path_so_far):
        """
        base case:
            current + direction = goal
        """
        # assert last in path so far is current pos
        assert path_so_far[-1] == self.get_current()

        if self._get_desired(direction) in path_so_far:
            return None

        # first try to move from current
        self._update_desired(direction)
        status_code = self.move(direction)

        if status_code == self.STATUS_HIT_WALL:
            # this is not a valid path
            return None

        # add the point to the path
        new_path = path_so_far.copy()
        new_path.append(self.get_current())

        if status_code == self.STATUS_HIT_GOAL:
            result = new_path
        else:
            self.process_new_path(new_path)
            result = self._try_all_directions(new_path)

        # move back to prev point
        opposite_direction = self.OPPOSITE_DIRECTIONS[direction]
        self._update_desired(opposite_direction)
        self.move(opposite_direction)

        return result

    def move(self, direction):
        """
        move in the given direction
        (unless impossible, eg wall)

        return a status code
        """
        raise NotImplementedError

    def process_new_path(self, new_path):
        pass
