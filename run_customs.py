from heuristic_examinations.shape_creation import generate_population, create_saved_population_group, read_population_group, create_saved_custom_population, read_custom_population_group
import matplotlib.pyplot as plt
from heuristic_examinations.polys_classes import PolyGroup, Poly
from heuristic_examinations.ea import EAVariable
from heuristic_examinations.plotter import plot_generation, plot_first_and_last, plot_fitness_over_time, plot_fitness_over_time_multiple_runs, plot_saver
from tqdm import tqdm
import datetime
import pickle
import os
import json
from multiprocessing import Pool, freeze_support
from functools import partial
from typing import List

with open('heuristic_examinations/config_files/complete_config.json') as f:
    config_file = json.load(f)

list_of_configs = []
# list_of_configs.append("config1")
# list_of_configs.append("config2")
# list_of_configs.append("config3")
# list_of_configs.append("config4")
# list_of_configs.append("config5")
# list_of_configs.append("config6")
# list_of_configs.append("config7")
# list_of_configs.append("config8")
# list_of_configs.append("config9")
list_of_configs.append("config10")
# list_of_configs.append("config11")
# list_of_configs.append("config12")
# list_of_configs.append("config13")
# list_of_configs.append("config14")
# list_of_configs.append("config15")
# list_of_configs.append("config16")

# important configs:
# config1: everything is false
# config2: only variable step size is true
# config3: only mutate order is true
# config5: only mutate direction is true
# config9: only recombination is true
# config16: everything is true

# Define the 8 unique CONVEX polygons
# poly1 = Poly([[0,0], [0,2], [2,2], [2,0], [0,0]])
# poly2 = Poly([[0,0], [0,3], [3,3], [2,0], [0,0]])
# poly3 = Poly([[0,0], [0,4], [2,3], [2,1], [0,0]])
# poly4 = Poly([[0,0], [0,3], [4,2], [3,1], [0,0]])
# poly5 = Poly([[0,0], [2,3], [4,4], [3,2], [0,0]])
# poly6 = Poly([[0,0], [0,5], [4,3], [4,1], [0,0]])
# poly7 = Poly([[0,0], [1,4], [5,1], [2,0], [0,0]])
# poly8 = Poly([[0,0], [1,1], [3,1], [2,0], [0,0]])


# Define the 8 unique CONCAVE polygons
poly1 = Poly([[0,0], [0,5], [5,0], [1,2], [0,0]])
poly2 = Poly([[0,0], [5,5], [8,0], [4,2], [0,0]])
poly3 = Poly([[0,0], [3,2], [5,5], [4,0], [0,0]])
poly4 = Poly([[0,0], [2,5], [5,1], [3,2], [0,0]])
poly5 = Poly([[0,0], [4,5], [7,0], [3,1], [0,0]])
poly6 = Poly([[0,0], [0,3], [5,5], [2,3], [0,0]])
poly7 = Poly([[0,0], [1,5], [7,3], [1,2], [0,0]])
poly8 = Poly([[0,0], [0,4], [3,1], [1,1], [0,0]])


# Add the polygons to a list
polys: List[Poly] = [poly1, poly2, poly3, poly4, poly5, poly6, poly7, poly8]

NUM_POLY_GROUPS = 4
NUM_SURVIVORS = 10
NUM_CHILDREN = 40
FIELD_DIAMETER = 20

NUM_GENERATIONS = 100
NUM_RUNS = 1

# BELOW IS FOR GENERATING A NEW POPULATION
create_saved_custom_population(number_of_poly_groups = NUM_POLY_GROUPS, polys = polys, field_diameter= FIELD_DIAMETER)


def run(config, list_of_configs, config_file):
    global NUM_SURVIVORS
    global NUM_CHILDREN
    global FIELD_DIAMETER
    global NUM_GENERATIONS
    global NUM_RUNS
    # BELOW IS FOR READING A PREVIOUSLY GENERATED POPULATION. When kept empty, it will read the most recently generated population
    populations = read_custom_population_group()

    complete_ea_runs = []

    complete_runs = []

    # check which index the config is in the list of configs
    position = list_of_configs.index(config)
    with tqdm(total=len(populations) * NUM_GENERATIONS,position=position, leave=False,  desc=f"{config}", bar_format="{desc:<30}| {percentage:3.0f}% |{bar:40}| {elapsed}/{remaining} | {n_fmt}/{total_fmt}") as pbar_inner:
        for i in range(len(populations)):
            complete_run = []
            populations[i].sort(key=lambda x: x.fitness(), reverse=True)
            complete_run.append(populations[i])
            ea = EAVariable(config=config, config_file=config_file, num_survivors=NUM_SURVIVORS, field_diameter=FIELD_DIAMETER, num_children=NUM_CHILDREN)

            for generation in range(NUM_GENERATIONS):
                populations[i] = ea.step(populations[i], generation)
                single_gen = populations[i]
                complete_run.append(single_gen)
                
                pbar_inner.update(1)
            complete_runs.append(complete_run)
        complete_ea_runs.append(complete_runs)
            

        # plot_saver(complete_runs, NUM_RUNS, NUM_GENERATIONS, len(polys), config)

    # save complete ea runs as a pickle file
    now = datetime.datetime.now()
    file_path = f"heuristic_examinations\\results\\customs\\eas_{config}_{NUM_GENERATIONS}_generations_{NUM_RUNS}_runs_{len(polys)}_polys_{NUM_SURVIVORS}_survivors_{NUM_CHILDREN}_children___{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}.pkl"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        pickle.dump(complete_ea_runs, f)
    

if __name__ == '__main__':
    freeze_support()
    with Pool(len(list_of_configs)) as p:
        partial_run = partial(run, config_file=config_file, list_of_configs=list_of_configs)
        p.map(partial_run, list_of_configs)