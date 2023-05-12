from typing import List, Tuple
import math, random

from ..polys_classes import PolyGroup
from ..polys_classes import Poly
from ..shape_creation import copy_polygroup
from ..polys_classes import step_calculator, rotate_calculator, overlaps_with_others, outside_field


class EABarebones(List[PolyGroup]):
    def __init__(self, pop_size, field_diameter, std = 0.01, num_parents = 20, 
                rotate_size = 0.1, rotate_type = "triangular", step_type = "triangular", 
                step_size = 0.1, attempts = 100, num_generations = 100):
        self.pop_size = pop_size
        self.field_diameter = field_diameter
        self.std = std #the standard deviation, used as the proportion that a value can mutate with
        self.num_parents = num_parents #number of parents selected from the population
        self.rotate_size = rotate_size
        self.rotate_type = rotate_type
        self.step_type = step_type
        self.step_size = step_size
        self.attempts = attempts
        self.num_generations = num_generations

    def parent_selection(self, generation):

        parents = generation
        return parents
    
    def recombination(self, parents):
        # copy random parents from the population to create children until the population is full
        children = []

        while len(children) < self.pop_size - len(parents):
            child = random.choice(parents)
            children.append(child)

        # shuffle the children list
        random.shuffle(children)
        return children

    def mutation(self, children):
        # first shuffle the polygons in each child
        for child in children:
            child.shuffle()

        # then move and rotate the polygons in each child randomly, until they no longer overlap
        for child in children:
            randomly_move_polys_to_legal_locations(child, self.field_diameter, self.step_size, self.step_type, self.rotate_size, self.rotate_type, self.attempts)

        mutated_children = children

        return mutated_children
    
    def survivor_selection(self, parents, children):
        # combine the parents and children lists
        population = parents + children
        # sort the population by fitness
        population.sort(key = lambda x: x.fitness, reverse = True)
        # return the top pop_size number of polygons
        return population[:self.pop_size]









def randomly_move_polys_to_legal_locations(polys: PolyGroup, field_diameter: int, step_size: float, step_type: str = "triangular", rotate_size: float = 0.1, rotate_type: str = "uniform", attempts: int = 1000) -> List[Poly]:
    """Moves and rotates the polygons in the PolyGroup until they no longer overlap with each other or go outside the field.
    """
    # iterate over each polygon in the input list. the polygon is randomly moved and rotated. if it overlaps with another polygon or goes outside the field, it is moved back to its original position and the process is repeated.
    polys = polys._polys
    for poly in polys:
        old_poly = poly
        x_offset, y_offset = step_calculator(step_size, step_type)
        angle = rotate_calculator(rotate_size, rotate_type)
        poly.translate(x_offset, y_offset)
        poly.rotate(angle)
        while (overlaps_with_others(poly, polys) or outside_field(poly, field_diameter)) and attempts > 0:
            poly = old_poly
            x_offset, y_offset = step_calculator(step_size, step_type)
            angle = rotate_calculator(rotate_size, rotate_type)
            poly.translate(x_offset, y_offset)
            poly.rotate(angle)
            attempts -= 1
        if attempts == 0:
            print("Could not find a legal location for the poly.")
            poly = old_poly

    return polys
