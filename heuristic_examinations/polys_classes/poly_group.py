import math, random
from typing import List, Tuple
from shapely.geometry import Polygon

from .poly import Poly
from .move_overlapping import move_and_rotate, randomize_shape_location_rotation


class PolyGroup(object):
    """
    Class for a group of polygons with additional methods.
    """

    def __init__(self, polys: List[Poly], **kwargs):
        self._polys = polys
        self.count = len(polys)
        self.circle = self.get_minimal_circumscribed_circle_radius()

    def __str__(self):
        """Returns a string representation of the PolyGroup."""
        poly_str_list = []
        for i in range(len(self._polys)):
            coords = ", ".join(f"({x} {y})" for x, y in self._polys[i].exterior.coords[:-1])
            poly_str_list.append(f"Poly {i}: {coords}")

        return "\n".join(poly_str_list)
    
    def get_minimal_circumscribed_circle_radius(self) -> float:
        """
        Calculates the radius of the smallest circle that can contain all polygons in the list.
        """
        # create a list of all points in all polygons
        all_points = []
        for poly in self._polys:
            all_points.extend(poly.exterior.coords)
        # for all points, calculate the distance to the center (0,0)
        distances = []
        for point in all_points:
            distances.append(math.sqrt(point[0]**2 + point[1]**2))
        # return the maximum distance
        return max(distances)
    
    def non_overlap(self, field_diameter: int, step_size: float, step_type: str = "triangular", rotate_size: float = 0.1, rotate_type: str = "uniform") -> None:
        """Moves and rotates the polygons in the PolyGroup until they no longer overlap with each other or go outside the field.
        """
        self._polys = move_and_rotate(self._polys, field_diameter, step_size, rotate_size, step_type, rotate_type)

    def randomize_poly_locations_and_rotations(self, field_diameter: int) -> None:
        """Moves and rotates the polygons in the PolyGroup to random locations and rotations.
        """
        self._polys = [randomize_shape_location_rotation(poly, field_diameter) for poly in self._polys]
        # self._polys = randomize_shape_location_rotation(self._polys, field_diameter) 




