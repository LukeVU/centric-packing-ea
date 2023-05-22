import math, random
from typing import List, Tuple
from shapely.geometry import Polygon
from shapely import affinity



class Poly:
    """A class that represents a polygon. It is a wrapper for the shapely Polygon class."""

    def __init__(self, *args, **kwargs):
        self.polygon = Polygon(*args, **kwargs)
        self.rotation = 0.0
        # self.get_furthest_distance = self.get_furthest_distance()
        # self.index = None

    def __getattr__(self, attr):
        return getattr(self.polygon, attr)
    
    def __str__(self):
        return f"Poly: {self.exterior.coords[:-1]}"
    
    def __getstate__(self):
        return self.__dict__
    
    def __setstate__(self, state):
        self.__dict__ = state
    

    def get_furthest_distance(self) -> float:
        """
        Calculates the point in the polygon that is furthest away from the center (0,0).
        """
        # Calculate the distance of the point that is furthest away from the center (0,0)
        return max(math.sqrt(point[0]**2 + point[1]**2) for point in self.exterior.coords)

    
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
            poly_copy.index = self.index

        return poly_copy
