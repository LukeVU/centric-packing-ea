import pickle
from heuristic_examinations.plotter import plot_first_and_last, plot_fitness_over_time, plot_fitness_over_time_multiple_runs, plot_saver

# import and read the pickle file from results folder
file_location = "heuristic_examinations\\results\\eas_['config1', 'config2', 'config3', 'config4']_500_generations_15_runs_5_polys_10_survivors_40_children___2023_5_22_17_58.pkl"
with open(file_location, "rb") as f:
    complete_ea_runs = pickle.load(f)

# plot the first and last generations of each run
for complete_run in complete_ea_runs[1]:
    plot_first_and_last(complete_run[0], complete_run[-1] , 20)