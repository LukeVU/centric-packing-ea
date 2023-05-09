import pickle
import copy
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import random
from shapely import affinity
import random
from typing import List, Tuple
from shapely.geometry import Polygon

from move_overlapping import move_and_rotate, step_calculator, rotate_calculator, overlaps_with_others, outside_field
from step_functions import sort_by_furthest_point

## TODO: unfinished

class EA(object):
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
        # iterate over each set of polygons, calculate the minimum circle radius, and add it to the list of radii. 
        radii = []
        for set_of_polys in generation:
            radii.append(set_of_polys.circle)
        # normalize the radii
        radii = np.array(radii)
        radii = radii / np.max(radii)
        # calculate the fitness of each set of polygons
        fitness = 1 / radii
        # select the parents
        parents = np.random.choice(np.arange(len(generation)), size=self.num_parents, replace=False, p=fitness/np.sum(fitness))
        # return the parents
        print("Selected Parents fitness values: {}".format([fitness[i] for i in parents]))
        print("Non-selected Parents fitness values: {}".format([fitness[i] for i in range(len(generation)) if i not in parents]))
        return [generation[i] for i in parents], [fitness[i] for i in parents]

    def recombination(self, parents):
        # randomly make copies of the parents to create children (the number of children is equal to the population size)
        children = []
        for i in range(self.pop_size):
            children.append(copy.deepcopy(random.choice(parents)))
        return children
        
    def mutation(self, children, step_size, attempts = 100, step_type = "triangular", rotate_size = 0.1, rotate_type = "triangular"):
        # sort the children by their furthest point from the center, in ascending order
        children = sort_by_furthest_point(children)
        # iterate over each child and mutate it
        mutated_children = []
        for child in children:
            original_child = child
            best_mutation = child
            # remove the child from the list of children so that it doesn't overlap with itself
            children.remove(child)
            # while within the maximum number of attempts, try to mutate the child. if the mutation is successful, store it as the best mutation 
            # and continue trying to mutate the child until the maximum number of attempts has been reached
            for i in range(attempts):
                # randomly offset the polygon by a uniform amount
                x_offset, y_offset = step_calculator(step_size, step_type)
                child = affinity.translate(child, x_offset, y_offset)
                # randomly rotate the polygon by a uniform amount
                angle = rotate_calculator(rotate_size, rotate_type)
                child = affinity.rotate(child, angle)
                child.rotation += angle
                # if the child no longer overlaps with any other polygons or goes outside the field, store it as the best mutation
                if ((not overlaps_with_others(child, mutated_children)) and 
                    (not outside_field(child, self.field_diameter)) and 
                    (not overlaps_with_others(child, children)) and
                    child.circle < best_mutation.circle):
                    best_mutation = child

                child = best_mutation
            # if the best mutation is different from the original child, add it to the list of mutated children
            if best_mutation != original_child:
                mutated_children.append(best_mutation)
            else:
                mutated_children.append(original_child)
        return mutated_children
        
    def survivor_selection(self, x_old, x_children, f_old, f_children):

        x = np.concatenate([x_old, x_children]) #combining the old values with the new(children)
        f = np.concatenate([f_old, f_children])
        order = np.argsort(f) #sorting the total list based on performance
        x = x[order][:self.pop_size] #limiting the list based on the population size. due to the sorting only the best are selected
        f = f[order][:self.pop_size]
        return x, f

    # Evaluation step: DO NOT REMOVE!
    def evaluate(self, x):
        return self.repressilator.objective(x)
    
    def step(self, x_old, f_old):
        #-------
        # PLEASE FILL IN
        # NOTE: This function must return x, f
        # where x - population
        #       f - fitness values of the population
        #-------

        x_parents, f_parents = self.parent_selection(x_old, f_old)

        x_children = self.recombination(x_parents)

        x_children = self.mutation(x_children)

        f_children = self.evaluate(x_children)

        x, f = self.survivor_selection(x_old, x_children, f_old, f_children)
        
        return x, f