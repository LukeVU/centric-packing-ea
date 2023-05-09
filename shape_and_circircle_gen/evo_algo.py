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

from calculate_cir_circle import calc_cir_circle_radius
from move_overlapping import move_and_rotate, step_calculator, rotate_calculator


class EA(object):
    def __init__(self, pop_size, field_diameter, std = 0.01, num_parents = 20):
        self.pop_size = pop_size
        self.field_diameter = field_diameter
        self.std = std #the standard deviation, used as the proportion that a value can mutate with
        self.num_parents = num_parents #number of parents selected from the population

    def parent_selection(self, generation):
        # iterate over each set of polygons, calculate the minimum circle diameter, and add it to the list of radii. 
        radii = []
        for set_of_polys in generation:
            radii.append(calc_cir_circle_radius(set_of_polys))
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
        
    def mutation(self, children, step_size):
        # iterate over each child and mutate it
        for child in children:
            # randomly offset the polygon by a uniform amount
            x_offset, y_offset = step_calculator(step_size, triangular)
            old_polygon = child
            child = affinity.translate(child, x_offset, y_offset)
            # randomly rotate the polygon by a uniform amount
            angle = rotate_calculator(rotate_size, rotate_type)
            child = affinity.rotate(child, angle)
        return children
        
        
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