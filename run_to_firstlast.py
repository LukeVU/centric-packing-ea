import pickle
from heuristic_examinations.plotter import plot_first_and_last, plot_fitness_over_time, plot_fitness_over_time_multiple_runs, plot_saver

# import and read the pickle file from results folder
# file_location = "heuristic_examinations\\results\\eas_['config1', 'config2', 'config3', 'config4']_500_generations_15_runs_5_polys_10_survivors_40_children___2023_5_22_17_58.pkl"
# with open(file_location, "rb") as f:
#     complete_ea_runs = pickle.load(f)

# # plot the first and last generations of each run
# for complete_run in complete_ea_runs[1]:
#     plot_first_and_last(complete_run[0], complete_run[-1] , 20)


# iterate through all the files in a specified folder
import os

# folder_location = "heuristic_examinations\\results\\multi_full_step5"
# for file in os.listdir(folder_location):
#     config_name = file.split("_")[1]
#     with open(folder_location + "\\" + file, "rb") as f:
#         config = pickle.load(f)
#     config_run = config[0][4]
#     plot_first_and_last(config_run[0], config_run[-1], 20, config_name)

file = "heuristic_examinations\\results\\multi_full_step5\\eas_config1_500_generations_30_runs_5_polys_10_survivors_40_children___2023_5_23_21_48.pkl"
config_name = file.split("_")[4]
with open(file, "rb") as f:
    config = pickle.load(f)
config_run = config[0]

for run in config_run:
    plot_first_and_last(run[0], run[-1], 20, config_name)
