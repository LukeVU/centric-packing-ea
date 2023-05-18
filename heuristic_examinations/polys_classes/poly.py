import math, random
from typing import List, Tuple
from shapely.geometry import Polygon
from shapely import affinity


class Poly:
    """A class that represents a polygon. It is a wrapper for the shapely Polygon class."""

    def __init__(self, *args, **kwargs):
        self.polygon = Polygon(*args, **kwargs)
        self.rotation = 0.0
        self.furthest_point = self.get_furthest_point()
        # self.index = None

    def __getattr__(self, attr):
        return getattr(self.polygon, attr)
    
    def __str__(self):
        return f"Poly: {self.exterior.coords[:-1]}"
    
    def __getstate__(self):
        return self.__dict__
    
    def __setstate__(self, state):
        self.__dict__ = state
    
    def get_furthest_point(self) -> Tuple[float, float]:
        """
        Calculates the point in the polygon that is furthest away from the center (0,0).
        """
        # create a list of all points in the polygon
        all_points = []
        for point in self.exterior.coords:
            all_points.append(point)
        # for all points, calculate the distance to the center (0,0)
        distances = []
        for point in all_points:
            distances.append(math.sqrt(point[0]**2 + point[1]**2))
        # return the point with the maximum distance
        return all_points[distances.index(max(distances))]
    
    def translate(self, x_offset: float, y_offset: float):
        """
        Moves the polygon by the given x and y offsets. Maintains the rotation of the polygon.
        """
        self.polygon = affinity.translate(self.polygon, x_offset, y_offset)
        

    def rotate(self, angle: float):
        """
        Rotates the polygon by the given angle. Maintains the rotation of the polygon.
        """
        self.polygon = affinity.rotate(self.polygon, angle)
        self.rotation += angle
        if self.rotation > 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360
    
    def copy(self):
        """
        Returns a copy of the polygon.
        """
        rotation = self.rotation

        poly_copy = Poly(self.polygon)
        poly_copy.rotation = rotation

        if self.index is not None:
            index = self.index
            poly_copy.index = index

        return poly_copy
