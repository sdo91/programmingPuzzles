
class Polygon(object):

    def __init__(self, points: list):
        self.points = points

    def __repr__(self):
        return '{} Poly: {}'.format(len(self.points), self.points)

def calc_poly_intersection(first: Polygon, second: Polygon):

    pass