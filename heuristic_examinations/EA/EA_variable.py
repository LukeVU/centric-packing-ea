from typing import List, Tuple
import math, random

from ..polys_classes import PolyGroup
from ..polys_classes import Poly
# from ..shape_creation import copy_polygroup
from ..polys_classes import step_calculator, rotate_calculator, overlaps_with_others, outside_field
from .ea__functions import randomly_move_polys_to_legal_locations, create_recombined_child, randomly_move_polys_to_legal_locations_closer


class EAVariable(List[PolyGroup]):
    def __init__(self, config, config_file, num_survivors, field_diameter, num_children,
                rotate_size = 10, rotate_type = "triangular", step_type = "triangular", 
                step_size = 5, attempts = 10):
        self.config = config
        self.config_file = config_file
        self.num_survivors = num_survivors
        self.field_diameter = field_diameter
        self.num_children = num_children #number of children created from the parents
        self.rotate_size = rotate_size
        self.rotate_type = rotate_type
        self.step_type = step_type
        self.step_size = step_size
        self.current_step_size = step_size
        self.attempts = attempts

    def parent_selection(self, generation):
        # IF RECOMBINATION IS TRUE
        if self.config_file[self.config]["recombination"] == True:
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

        # IF RECOMBINATION IS FALSE
        else:
            # starts with len(generation) parents, which should be the same as the population size
            parents = generation
            return parents
    
    def recombination(self, parents):
        # IF RECOMBINATION IS TRUE
        if self.config_file[self.config]["recombination"] == True:
            # the input parents list should be a list of pairs of parents
            children = []

            # randomly select a parent pair from the parents list
            while len(children) < self.num_children:
                parent_pair = random.choice(parents)
                # create a child from the parent pair
                child: PolyGroup = create_recombined_child(parent_pair, self.field_diameter, self.current_step_size, self.step_type, self.rotate_size, self.rotate_type)
                children.append(child)

        # IF RECOMBINATION IS FALSE
        else:

            # with crossover, the number of parents would be pairs, and thus half the population size
            # however, since the parents are not actually recombined, the number of parents is the same as the population size
            children = []

            while len(children) < self.num_children:
                child = random.choice(parents)
                children.append(child.copy())

        # the number of children should be equal to the num_children parameter
        return children

    def mutation(self, children):
        # shuffle the children list
        random.shuffle(children)

        # only mutating the children, not the parents, so the number of children should be equal to the num_children parameter

        # IF MUTATION ORDER IS TRUE
        if self.config_file[self.config]["mutation_order"] == True:
            # sort the polygons in each child by the furthest distance from the center, in increasing order
            for child in children:
                child._polys.sort(key = lambda x: x.get_furthest_distance(), reverse = True)

        # IF MUTATION ORDER IS FALSE
        else:
        # first shuffle the polygons in each child

            for child in children:
                random.shuffle(child._polys)


        # IF MUTATION CLOSER IS TRUE
        if self.config_file[self.config]["mutation_direction"] == True:
            for child in children:
                randomly_move_polys_to_legal_locations_closer(child, self.field_diameter, self.step_size, self.step_type, self.rotate_size, self.rotate_type, self.attempts)


        # IF MUTATION CLOSER IS FALSE
        else:
            # then move and rotate the polygons in each child randomly, until they no longer overlap
            for child in children:
                randomly_move_polys_to_legal_locations(child, self.field_diameter, self.current_step_size, self.step_type, self.rotate_size, self.rotate_type, self.attempts)

        mutated_children = children

        # the number of mutated_children should be equal to the num_children parameter
        return mutated_children
    
    def survivor_selection(self, parents, children):
        # here the populations size exceeds the num_survivors parameter, as the parents and children are combined. the population size is num_survivors + num_children
        
        # IF RECOMBINATION IS TRUE
        if self.config_file[self.config]["recombination"] == True:
            single_parents = [parent for parent_pair in parents for parent in parent_pair]

            population = single_parents + children
        
        # IF RECOMBINATION IS FALSE
        else:
            # combine the parents and children lists
            population = parents + children
        # sort the population by fitness
        population.sort(key = lambda x: x.fitness(), reverse = True)
        # return the top pop_size number of polygons
        survivors = population[:self.num_survivors]

        # the number of survivors should be equal to the num_survivors parameter
        return survivors
    
    def step(self, generation, generation_number):
        if self.config_file[self.config]["variable_step_size"] == True:
            self.current_step_size = self.step_size / math.sqrt(generation_number + 1)
            
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