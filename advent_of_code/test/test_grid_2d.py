from unittest import TestCase
from util.grid_2d import Grid2D


class Test(TestCase):

    def test_rotate(self):
        text0 = 'ABC\nDEF'
        text90 = 'CF\nBE\nAD'
        text180 = 'FED\nCBA'
        text270 = 'DA\nEB\nFC'

        grid = Grid2D(text0)
        expected0 = Grid2D(text0)
        expected90 = Grid2D(text90)
        expected180 = Grid2D(text180)
        expected270 = Grid2D(text270)

        grid = grid.rot90()
        self.assertEqual(repr(expected90), repr(grid))

        grid = grid.rot90()
        self.assertEqual(repr(expected180), repr(grid))

        grid = grid.rot90()
        self.assertEqual(repr(expected270), repr(grid))

        grid = grid.rot90()
        self.assertEqual(repr(expected0), repr(grid))
