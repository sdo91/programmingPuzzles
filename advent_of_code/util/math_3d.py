import numpy as np


class Polygon(object):

    def __init__(self, points: list):
        self.points = points

    def __repr__(self):
        return '{} Poly: {}'.format(len(self.points), self.points)


def calc_poly_intersection(first: Polygon, second: Polygon):
    pass


def calc_plane_equation(points: Polygon):
    """
    form: Ax + By + Cz + D = 0
    see: http://www.ambrsoft.com/TrigoCalc/Plan3D/Plane3D_.htm#planeGivenBy3PointsEx2
    """
    p1, p2, p3 = points.points

    v1 = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    v2 = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])

    cross_product = np.cross(v1, v2)
    A, B, C = cross_product

    # plug in one of the points to solve for D
    D = -(A * p1[0] + B * p1[1] + C * p1[2])

    result = A, B, C, D
    return result


def calc_dist_from_plane(point, plane_equation):
    """
    http://www.ambrsoft.com/TrigoCalc/Plan3D/PointsCoplanar.htm
    """
    A, B, C, D = plane_equation
    num = abs(A * point[0] + B * point[1] + C * point[2] + D)
    denom = np.linalg.norm([A, B, C])
    return num / denom


def is_on_plane(point, plane_equation):
    A, B, C, D = plane_equation
    abc_sum = A * point[0] + B * point[1] + C * point[2]
    return abc_sum == -D


def are_coplanar_triangles(first: Polygon, second: Polygon):
    """
    see: http://www.ambrsoft.com/TrigoCalc/Plan3D/PointsCoplanar.htm
    triangles are coplanar if all points are coplanar
    """
    plane_equation = calc_plane_equation(first)
    for point in second.points:
        if not is_on_plane(point, plane_equation):
            return False
    return True
