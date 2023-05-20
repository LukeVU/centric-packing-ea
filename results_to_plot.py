from heuristic_examinations.shape_creation import generate_population, create_saved_population_group, read_population_group
import matplotlib.pyplot as plt
from heuristic_examinations.polys_classes import PolyGroup, Poly
from heuristic_examinations.ea import EABarebones, EARecombination
from heuristic_examinations.plotter import plot_generation, plot_first_and_last, plot_fitness_over_time, plot_fitness_over_time_multiple_runs, plot_saver
from tqdm import tqdm
import datetime
import pickle

# converts results from a pickle file to a plot

file_name = "heuristic_examinations\\results\\eas_['EABarebones', 'EARecombination']_10_generations_5_runs_5_polys_10_survivors_40_children___2023_5_20_14_17.pkl"

with open(file_name, "rb") as f:
    complete_ea_runs = pickle.load(f)

# convert the file name to the parameters used to generate the results
file_name = file_name.split("\\")[-1]
file_name = file_name.split(".")[0]

# save before the ___ as the file_name_params, and after the ___ as time_params
split_part = file_name.split("___")
file_name_params = split_part[0]
file_name_params = file_name_params.split("_")
list_of_eas = file_name_params[1][2:-2].split("', '")
NUM_GENERATIONS = int(file_name_params[2])
NUM_RUNS = int(file_name_params[4])
NUM_POLYS = int(file_name_params[6])
NUM_SURVIVORS = int(file_name_params[8])
NUM_CHILDREN = int(file_name_params[10])

time_params = split_part[1]


for i in range(len(complete_ea_runs)):
    plot_saver(complete_ea_runs[i], NUM_RUNS, NUM_GENERATIONS, NUM_POLYS, list_of_eas[i], time_params)
