from unittest import TestCase
from util.grid_2d import Grid2D


class Test(TestCase):

    def test_rot90(self):
        text0 = 'ABC\nDEF'
        text90 = 'CF\nBE\nAD'
        text180 = 'FED\nCBA'
        text270 = 'DA\nEB\nFC'

        expected0 = Grid2D(text0)
        expected90 = Grid2D(text90)
        expected180 = Grid2D(text180)
        expected270 = Grid2D(text270)
        grid = expected0

        grid = grid.rot90()
        self.assertEqual(repr(expected90), repr(grid))

        grid = grid.rot90()
        self.assertEqual(repr(expected180), repr(grid))

        grid = grid.rot90()
        self.assertEqual(repr(expected270), repr(grid))

        grid = grid.rot90()
        self.assertEqual(repr(expected0), repr(grid))

    def test_flip(self):
        text_og = 'ABC\nDEF'
        text_flipped_x = 'DEF\nABC'
        text_flipped_y = 'CBA\nFED'

        grid_og = Grid2D(text_og)
        grid_flipped_x = Grid2D(text_flipped_x)
        grid_flipped_y = Grid2D(text_flipped_y)
        grid = grid_og

        grid = grid.flip('X')
        self.assertEqual(repr(grid_flipped_x), repr(grid))

        grid = grid.flip('X')
        self.assertEqual(repr(grid_og), repr(grid))

        grid = grid.flip('Y')
        self.assertEqual(repr(grid_flipped_y), repr(grid))

        grid = grid.flip('Y')
        self.assertEqual(repr(grid_og), repr(grid))
