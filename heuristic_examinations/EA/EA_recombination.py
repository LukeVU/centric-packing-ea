from typing import List, Tuple
import math, random

from ..polys_classes import PolyGroup
from ..polys_classes import Poly
# from ..shape_creation import copy_polygroup
from ..polys_classes import step_calculator, rotate_calculator, overlaps_with_others, outside_field
from .ea__functions import randomly_move_polys_to_legal_locations, create_recombined_child

from ..plotter import plot_generation


class EARecombination(List[PolyGroup]):
    def __init__(self, num_survivors, field_diameter, num_children, std = 0.01,
                rotate_size = 10, rotate_type = "triangular", step_type = "triangular", 
                step_size = 10, attempts = 10):
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
        # NOTE: currently only works with even population sizes
        generation_copy = []
        for polygroup in generation:
            generation_copy.append(polygroup.copy())

        parents = []
        while len(generation_copy) > 0:
            # select 2 parents at random from the generation and add them to the parents list. then remove them from the generation
            parent1 = generation_copy.pop(random.randrange(len(generation_copy)))
            parent2 = generation_copy.pop(random.randrange(len(generation_copy)))
            parents.append([parent1, parent2])
        # the number of parents should be equal to the population size divided by 2
        return parents
    
    def recombination(self, parents):
        # the input parents list should be a list of pairs of parents
        children = []

        # randomly select a parent pair from the parents list
        while len(children) < self.num_children:
            parent_pair = random.choice(parents)
            # create a child from the parent pair
            child: PolyGroup = create_recombined_child(parent_pair, self.field_diameter, self.step_size, self.step_type, self.rotate_size, self.rotate_type)
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
        # single_parents = []
        # for parent_pair in parents:
        #     single_parents.append(parent_pair[0])
        #     single_parents.append(parent_pair[1])

        single_parents = [parent for parent_pair in parents for parent in parent_pair]

        population = single_parents + children
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
