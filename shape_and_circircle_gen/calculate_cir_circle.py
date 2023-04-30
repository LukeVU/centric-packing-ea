from shapely.geometry import Polygon
import math
from typing import List

def calc_cir_circle_diameter(polys: List[Polygon]) -> float:
    """
    Calculates the diameter of the smallest circle that can contain all polygons in the list.
    """
    # create a list of all points in all polygons
    all_points = []
    for poly in polys:
        all_points.extend(poly.exterior.coords)
    # for all points, calculate the distance to the center (0,0)
    distances = []
    for point in all_points:
        distances.append(math.sqrt(point[0]**2 + point[1]**2))
    # return the maximum distance
    return max(distances)