import math, random
from typing import List, Tuple
from shapely.geometry import Polygon


def easy_poly_gen(number_of_polys: int, field_diameter: int, size: float, 
                    irregularity: float, spikiness: float,
                    num_vertices: int) -> List[Polygon]:
    """
    Generates a list of polygons with the same size and shape.

    Args:
        number_of_polys (int):
            the number of polygons to generate.
        field_diameter (int):
            the diameter of the field.
        size (float):
            the size of each polygon.
        irregularity (float):
            variance of the spacing of the angles between consecutive vertices.
        spikiness (float):
            variance of the distance of each vertex to the center of
            the circumference.
        num_vertices (int):
            the number of vertices of the polygon.

    Returns:
        List[Polygon]: the list of polygons.
    """
    # Parameter check
    if irregularity < 0 or irregularity > 1:
        raise ValueError("Irregularity must be between 0 and 1.")
    if spikiness < 0 or spikiness > 1:
        raise ValueError("Spikiness must be between 0 and 1.")
    if size < 0 or size > field_diameter:
        raise ValueError("Size must be between 0 and the field diameter.")
    if size is None:
        size = field_diameter / 5

    polygons = []
    for i in range(number_of_polys):
        # Generate a random center
        center = (random.triangular(-field_diameter, field_diameter, 0),
                  random.triangular(-field_diameter, field_diameter, 0))

        # Create the polygon
        polygons.append(Polygon(generate_polygon(center, size,
                                                 irregularity, spikiness,
                                                 num_vertices)))

    return polygons



### START OF CODE FROM https://stackoverflow.com/questions/8997099/algorithm-to-generate-random-2d-polygon ###

def generate_polygon(center: Tuple[float, float], avg_radius: float,
                     irregularity: float, spikiness: float,
                     num_vertices: int) -> List[Tuple[float, float]]:
    """
    Start with the center of the polygon at center, then creates the
    polygon by sampling points on a circle around the center.
    Random noise is added by varying the angular spacing between
    sequential points, and by varying the radial distance of each
    point from the centre.

    Args:
        center (Tuple[float, float]):
            a pair representing the center of the circumference used
            to generate the polygon.
        avg_radius (float):
            the average radius (distance of each generated vertex to
            the center of the circumference) used to generate points
            with a normal distribution.
        irregularity (float):
            variance of the spacing of the angles between consecutive
            vertices.
        spikiness (float):
            variance of the distance of each vertex to the center of
            the circumference.
        num_vertices (int):
            the number of vertices of the polygon.
    Returns:
        List[Tuple[float, float]]: list of vertices, in CCW order.
    """
    # Parameter check
    if irregularity < 0 or irregularity > 1:
        raise ValueError("Irregularity must be between 0 and 1.")
    if spikiness < 0 or spikiness > 1:
        raise ValueError("Spikiness must be between 0 and 1.")

    irregularity *= 2 * math.pi / num_vertices
    spikiness *= avg_radius
    angle_steps = random_angle_steps(num_vertices, irregularity)

    # now generate the points
    points = []
    angle = random.uniform(0, 2 * math.pi)
    for i in range(num_vertices):
        radius = clip(random.gauss(avg_radius, spikiness), 0, 2 * avg_radius)
        point = (center[0] + radius * math.cos(angle),
                 center[1] + radius * math.sin(angle))
        points.append(point)
        angle += angle_steps[i]

    return points

def random_angle_steps(steps: int, irregularity: float) -> List[float]:
    """Generates the division of a circumference in random angles.

    Args:
        steps (int):
            the number of angles to generate.
        irregularity (float):
            variance of the spacing of the angles between consecutive vertices.
    Returns:
        List[float]: the list of the random angles.
    """
    # generate n angle steps
    angles = []
    lower = (2 * math.pi / steps) - irregularity
    upper = (2 * math.pi / steps) + irregularity
    cumsum = 0
    for i in range(steps):
        angle = random.uniform(lower, upper)
        angles.append(angle)
        cumsum += angle

    # normalize the steps so that point 0 and point n+1 are the same
    cumsum /= (2 * math.pi)
    for i in range(steps):
        angles[i] /= cumsum
    return angles

def clip(value, lower, upper):
    """
    Given an interval, values outside the interval are clipped to the interval
    edges.
    """
    return min(upper, max(value, lower))


### END OF CODE FROM https://stackoverflow.com/questions/8997099/algorithm-to-generate-random-2d-polygon ###