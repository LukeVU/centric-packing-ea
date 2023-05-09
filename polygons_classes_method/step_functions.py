from shapely import affinity
import random
from typing import List, Tuple
from shapely.geometry import Polygon

from poly import Poly

# a function that sorts a list of polygons by their their furthest point from the center, in ascending order
def sort_by_furthest_point(polys: List[Poly]) -> List[Poly]:
    """Sorts a list of polygons by their furthest point from the center, in ascending order.

    Args:
        polys (List[Poly]): The list of polygons to sort

    Returns:
        List[Poly]: The sorted list of polygons
    """
    distances = []
    for poly in polys:
        distances.append(poly.furthest_point)
    # sort the polygons based on their distance from the center
    sorted_polys = [poly for _, poly in sorted(zip(distances, polys))]
    return sorted_polys
