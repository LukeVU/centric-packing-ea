from shapely import affinity
import random
from typing import List, Tuple
from shapely.geometry import Polygon

from .poly import Poly


## TODO: add a function that gives each poly a random rotation before moving them



def move_and_rotate(polys: List[Poly], field_diameter: int, step_size: float, rotate_size: float, 
                    step_type: str  = "triangular", rotate_type: str  = "triangular") -> List[Poly]:
    """Moves and rotates a list of polygons so that they don't overlap with each other.

    Args:
        polys (List[Poly]): The list of polygons to move and rotate
        field_diameter (int): The diameter of the field. This is used to determine how far the polygons can be moved
        step_size (float): The maximum distance that a polygon can be moved in either the x or y direction
        rotate_size (float): The maximum angle that a polygon can be rotated by
        step_type (str, optional): The type of step to take. Can be "triangular" or "uniform". Defaults to "triangular".
        rotate_type (str, optional): The type of rotation to take. Can be "triangular" or "uniform". Defaults to "triangular".

    Returns:
        List[Poly]: The list of polygons after they have been moved and rotated
    """

    # Parameter check
    if field_diameter < 0:
        raise ValueError("Field diameter must be positive.")
    
    if step_type not in ["triangular", "uniform"]:
        raise ValueError("Step type must be either 'triangular' or 'uniform'.")
    
    if step_size < 0:
        raise ValueError("Step size must be positive.")
    


    # Move and rotate the polygons
    non_overlapping_polygons = []

    # iterate over each polygon in the input list
    while len(polys) > 0:
        polygon = polys[0]
        polys.remove(polygon)
        # check if it overlaps with any other polygons or polygons that have already been moved
        while overlaps_with_others(polygon, polys) or overlaps_with_others(polygon, non_overlapping_polygons) or outside_field(polygon, field_diameter):
            # if outside the field, move to the center
            if outside_field(polygon, field_diameter):
                print("OUTSIDE")
                # calculate the distance to the center
                x_offset = -polygon.polygon.centroid.x
                y_offset = -polygon.polygon.centroid.y
                # move the polygon to the center
                polygon = Poly(affinity.translate(polygon.polygon, x_offset, y_offset))
                print("Moved polygon to center: {}".format(polygon))
            # randomly offset the polygon by a uniform amount
            x_offset, y_offset = step_calculator(step_size, step_type)
            old_polygon = polygon
            polygon = Poly(affinity.translate(polygon.polygon, x_offset, y_offset))
            # randomly rotate the polygon by a uniform amount
            angle = rotate_calculator(rotate_size, rotate_type)
            polygon = Poly(affinity.rotate(polygon.polygon, angle))
            polygon.rotation += angle

            # print("Moved polygon from {} to {}".format(old_polygon, polygon))
        # if the polygon doesn't overlap with any others, add it to the list of non-overlapping polygons
        non_overlapping_polygons.append(polygon)
        print("Added polygon {}".format(polygon))

    return non_overlapping_polygons

def overlaps_with_others(polygon, polygons):
    for other in polygons:
        if other.polygon.intersects(polygon.polygon):
            print("OVERPAP")
            return True
    return False

def outside_field(polygon, field_diameter):
    # for each vertacy in the polygon, check if it is outside the field
    for vertex in polygon.exterior.coords:
        if vertex[0] < -field_diameter or vertex[0] > field_diameter or vertex[1] < -field_diameter or vertex[1] > field_diameter:
            return True
    return False


def step_calculator(step_size: float, step_type: str = "triangular") -> Tuple[float, float]:
    """Calculates a random x and y offset to move a polygon by.

    Args:
        step_size (float): The maximum distance that a polygon can be moved in either the x or y direction
        step_type (str, optional): The type of step to take. Can be "triangular" or "uniform". Defaults to "triangular".

    Returns:
        Tuple[float, float]: The x and y offsets
    """

    # Parameter check
    if step_type not in ["triangular", "uniform"]:
        raise ValueError("Step type must be either 'triangular' or 'uniform'.")
    
    if step_size < 0:
        raise ValueError("Step size must be positive.")
    
    # Calculate the x and y offsets
    if step_type == "triangular":
        x_offset = random.triangular(-step_size, step_size, 0)
        y_offset = random.triangular(-step_size, step_size, 0)
    elif step_type == "uniform":
        x_offset = random.uniform(-step_size, step_size)
        y_offset = random.uniform(-step_size, step_size)
    else:
        raise ValueError("Step type must be either 'triangular' or 'uniform'.")
    
    return x_offset, y_offset

def rotate_calculator(rotate_size: float, rotate_type: str = "triangular") -> float:
    """Calculates a random angle to rotate a polygon by.

    Args:
        rotate_size (float): The maximum angle that a polygon can be rotated by
        rotate_type (str, optional): The type of rotation to take. Can be "triangular" or "uniform". Defaults to "triangular".

    Returns:
        float: The angle to rotate the polygon by
    """

    # Parameter check
    if rotate_type not in ["triangular", "uniform"]:
        raise ValueError("Rotate type must be either 'triangular' or 'uniform'.")
    
    if rotate_size < 0:
        raise ValueError("Rotate size must be positive.")
    
    # Calculate the angle to rotate by
    if rotate_type == "triangular":
        angle = random.triangular(-rotate_size, rotate_size, 0)
    elif rotate_type == "uniform":
        angle = random.uniform(-rotate_size, rotate_size)
    else:
        raise ValueError("Rotate type must be either 'triangular' or 'uniform'.")
    
    return angle

def randomize_shape_location_rotation(poly: Poly, field_diameter: int) -> Poly:
    """
    Randomizes the location and rotation of a polygon.

    Args:
        poly (Poly):
            the polygon to randomize.
        field_diameter (int):
            the diameter of the field.

    Returns:
        Poly: the randomized polygon.
    """
    # Generate a random center
    new_center = (random.triangular(-field_diameter, field_diameter, 0),
              random.triangular(-field_diameter, field_diameter, 0))

    # Generate a random rotation in degrees
    rotation = random.uniform(0, 360)

    # Move and rotate the polygon
    current_center = poly.centroid
    new_poly = Poly(affinity.translate(poly.polygon, new_center[0] - current_center.x, new_center[1] - current_center.y))
    new_poly = Poly(affinity.rotate(new_poly.polygon, rotation))

    return new_poly