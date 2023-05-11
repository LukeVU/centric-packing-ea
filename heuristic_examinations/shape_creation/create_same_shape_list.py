import math, random
from typing import List, Tuple
from shapely.geometry import Polygon

from ..polys_classes import PolyGroup
from .create_shapes import easy_poly_gen

def generate_population(number_of_poly_groups : int, number_of_polys: int, field_diameter: int, 
                        step_size = .2, step_type = "triangular", rotate_size: float = 0.1, 
                        rotate_type: str = "uniform", size: float = 3, 
                        irregularity: float = 0.5, spikiness: float = 0.5,
                        num_vertices: int = 4) -> List[PolyGroup]:
    
    population = []
    # create the initial shapes as a PolyGroup
    original_instance = easy_poly_gen(number_of_polys, field_diameter, size, irregularity, spikiness, num_vertices)

    # create a list of PolyGroups with number_of_poly_groups instances of the original_instance
    for i in range(number_of_poly_groups):
        population.append(original_instance)

    # for each PolyGroup in the population, randomize the locations and rotations of the polygons, then move them so that they don't overlap
    for poly_group in population:
        poly_group.randomize_poly_locations_and_rotations(field_diameter)
        poly_group.non_overlap(field_diameter, step_size, step_type, rotate_size, rotate_type)

    return population