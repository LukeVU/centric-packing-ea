import math, random
from typing import List, Tuple
from shapely.geometry import Polygon


class Poly:
    """A class that represents a polygon. It is a wrapper for the shapely Polygon class."""

    def __init__(self, *args, **kwargs):
        self.polygon = Polygon(*args, **kwargs)
        self.rotation = 0.0
        self.furthest_point = self.get_furthest_point()

    def __getattr__(self, attr):
        return getattr(self.polygon, attr)
    
    def __str__(self):
        return f"Poly: {self.exterior.coords[:-1]}"
    
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