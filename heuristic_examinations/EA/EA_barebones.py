from typing import List, Tuple
import math, random

from ..polys_classes import PolyGroup
from ..polys_classes import Poly
# from ..shape_creation import copy_polygroup
from ..polys_classes import step_calculator, rotate_calculator, overlaps_with_others, outside_field


class EABarebones(List[PolyGroup]):
    def __init__(self, num_survivors, field_diameter, num_children, std = 0.01,
                rotate_size = 0.1, rotate_type = "triangular", step_type = "triangular", 
                step_size = 0.1, attempts = 100):
        self.num_survivors = num_survivors
        self.field_diameter = field_diameter
        self.std = std #the standard deviation, used as the proportion that a value can mutate with
        self.num_children = num_children #number of children created from the parents
        self.rotate_size = rotate_size
        self.rotate_type = rotate_type
        self.step_type = step_type
        self.step_size = step_size
        self.attempts = attempts

    def parent_selection(self, generation):
        # starts with len(generation) parents, which should be the same as the population size
        parents = generation
        # when actually performing recombination, the number of parents would be pairs, and thus half the population size
        # however, since the parents are not actually recombined, the number of parents is the same as the population size
        return parents
    
    def recombination(self, parents):
        # with crossover, the number of parents would be pairs, and thus half the population size
        # however, since the parents are not actually recombined, the number of parents is the same as the population size
        children = []

        while len(children) < self.num_children:
            child = random.choice(parents)
            children.append(child)

        # shuffle the children list
        random.shuffle(children)

        # the number of children should be equal to the num_children parameter
        return children

    def mutation(self, children):
        # only mutating the children, not the parents, so the number of children should be equal to the num_children parameter
        # first shuffle the polygons in each child
        for child in children:
            child.shuffle()

        # then move and rotate the polygons in each child randomly, until they no longer overlap
        for child in children:
            randomly_move_polys_to_legal_locations(child, self.field_diameter, self.step_size, self.step_type, self.rotate_size, self.rotate_type, self.attempts)

        mutated_children = children

        # the number of mutated_children should be equal to the num_children parameter
        return mutated_children
    
    def survivor_selection(self, parents, children):
        # here the populations size exceeds the num_survivors parameter, as the parents and children are combined. the population size is num_survivors + num_children
        # combine the parents and children lists
        population = parents + children
        # sort the population by fitness
        population.sort(key = lambda x: x.fitness(), reverse = True)
        # return the top pop_size number of polygons
        survivors = population[:self.num_survivors]

        # the number of survivors should be equal to the num_survivors parameter
        return survivors
    
    def step(self, generation):
        # select parents
        parents = self.parent_selection(generation)
        # recombine parents to create children
        children = self.recombination(parents)
        # mutate children
        mutated_children = self.mutation(children)
        # select survivors
        survivors = self.survivor_selection(parents, mutated_children)
        # return the survivors
        return survivors









def randomly_move_polys_to_legal_locations(polys: PolyGroup, field_diameter: int, step_size: float, step_type: str = "triangular", rotate_size: float = 0.1, rotate_type: str = "uniform", attempts: int = 100) -> List[Poly]:
    """Moves and rotates the polygons in the PolyGroup until they no longer overlap with each other or go outside the field.
    """
    # iterate over each polygon in the input list. the polygon is randomly moved and rotated. if it overlaps with another polygon or goes outside the field, it is moved back to its original position and the process is repeated.
    number_of_legal_moves = 0
    number_of_illegal_moves = 0
    polys = polys._polys
    for poly in polys:
        old_poly = poly
        x_offset, y_offset = step_calculator(step_size, step_type)
        angle = rotate_calculator(rotate_size, rotate_type)
        poly.translate(x_offset, y_offset)
        poly.rotate(angle)
        poly_attempts = attempts
        while (overlaps_with_others(poly, polys) or outside_field(poly, field_diameter)) and poly_attempts > 0:
            print(f"overlaps_with_others: {overlaps_with_others(poly, polys)}")
            print(f"outside_field: {outside_field(poly, field_diameter)}")
            poly = old_poly
            x_offset, y_offset = step_calculator(step_size, step_type)
            angle = rotate_calculator(rotate_size, rotate_type)
            poly.translate(x_offset, y_offset)
            poly.rotate(angle)
            poly_attempts -= 1
        if poly_attempts == 0:
            poly = old_poly
            number_of_illegal_moves += 1
            
        else:
            number_of_legal_moves += 1
            
    print(f"Number of using old location: {number_of_illegal_moves}")
    print(f"Number of using new location: {number_of_legal_moves}")
    return polys
