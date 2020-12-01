from unittest import TestCase
from util import math_3d
from util.math_3d import Polygon


class Test(TestCase):

    def test_calc_plane_equation(self):
        plane = Polygon([
            (1, 0, 2),
            (-3, 5, 0),
            (6, -4, 2),
        ])
        result = math_3d.calc_plane_equation(plane)
        self.assertEqual((-8, -10, -9, 26), result)

        plane = Polygon([
            (1, 3, 2),
            (-1, 2, 4),
            (2, 1, 3),
        ])
        result = math_3d.calc_plane_equation(plane)
        self.assertEqual((3, 4, 5, -25), result)

    def test_are_coplanar_triangles(self):
        t1 = Polygon([
            (3, -3, 2),
            (1, 0, 1),
            (1, 1, 0),
        ])
        t2 = Polygon([
            (0, 1, 1),
            (-2, 3, 1),
            (4, 2, -4),
        ])
        self.assertTrue(math_3d.are_coplanar_triangles(t1, t2))

        t2 = Polygon([
            (0, 1, 1),
            (-2, 3, 1),
            (0, 0, 0),
        ])
        self.assertFalse(math_3d.are_coplanar_triangles(t1, t2))
