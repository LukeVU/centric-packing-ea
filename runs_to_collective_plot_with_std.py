import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
from itertools import chain



num_generations = 500
evals_per_generation = 50
num_evaluations = num_generations * evals_per_generation

# # This script is used to plot the collective results of multiple configs in a single plot
# complete_fitness_lists = []
# configs = []

# # path to the folder in the results folder that contains the results to be plotted
# folder_path = "heuristic_examinations\\results\\multi_full_step5"

# # iterate through the files in the folder
# for file_name in os.listdir(folder_path):
#     configs.append(file_name.split("_")[1])

#     file_path = os.path.join(folder_path, file_name)
#     # read the file
#     with open(file_path, "rb") as f:
#         loaded_file = pickle.load(f)

#     # convert the loaded file to the average fitness over time
#     fitness_lists = []
#     for complete_run in loaded_file[0]:
#         fitness_list = []
#         for generation in complete_run:
#             fitness_list.append(generation[0].fitness())
#         fitness_lists.append(fitness_list)
#     complete_fitness_lists.append(fitness_lists)

# num_runs = len(loaded_file[0])

# average_list = []
# for i in range(len(complete_fitness_lists)):
#     fitness_list = complete_fitness_lists[i]
#     averaged_fitness_list = []
#     for i in range(len(fitness_list[0])):
#         averaged_fitness_list.append(sum(fitness_list[j][i] for j in range(len(fitness_list))) / len(fitness_list))
#     average_list.append(averaged_fitness_list)

# # a total list is created which contains tuples of the form config, average_list
# total_list = []
# for i in range(len(configs)):
#     total_list.append((configs[i], complete_fitness_lists[i]))

# # save the total list to a file
# file_path = os.path.join(os.path.dirname(__file__), "heuristic_examinations", "plots", "fitness_plots", "30runs_500generations_5polys", "multi_step_size_5", "total_list.pkl")
# os.makedirs(os.path.dirname(file_path), exist_ok=True)
# with open(file_path, "wb") as f:
#     pickle.dump(total_list, f)

# load the total list from a file
file_path = os.path.join(os.path.dirname(__file__), "heuristic_examinations", "plots", "fitness_plots", "30runs_500generations_5polys", "multi_step_size_5", "total_list.pkl")
with open(file_path, "rb") as f:
    total_list = pickle.load(f)



# plot the averages, and save the plot, each average in a different color, and a legend


# plot the averages, each in a different color, and a legend
# set the colors to be distinctly different
colors = ["red", "blue", "green", "orange", "purple", "brown", "pink", "gray", "olive", "cyan", "magenta", "yellow", "black", "lime", "teal", "navy"] 

# plot the average fitness of each config over time, of each config over time
for config_index in range(len(total_list)):
    config_name, fitness_lists = total_list[config_index]
    averaged_fitness_list = []
    for gen_index in range(len(fitness_lists[0])):
        averaged_fitness_list.append(sum(fitness_lists[run_index][gen_index] for run_index in range(len(fitness_lists))) / len(fitness_lists))
    plt.plot(range(len(averaged_fitness_list)), averaged_fitness_list, color=colors[config_index], linewidth=2, alpha=0.6, label=config_name)

# plot the standard deviation of each config over time
for config_index in range(len(total_list)):
    config_name, fitness_lists = total_list[config_index]
    averaged_fitness_list = []
    for gen_index in range(len(fitness_lists[0])):
        averaged_fitness_list.append(sum(fitness_lists[run_index][gen_index] for run_index in range(len(fitness_lists))) / len(fitness_lists))
    standard_deviation_list = []
    for gen_index in range(len(fitness_lists[0])):
        standard_deviation_list.append(np.std([fitness_lists[run_index][gen_index] for run_index in range(len(fitness_lists))]))
    plt.fill_between(range(len(standard_deviation_list)), [averaged_fitness_list[i] - standard_deviation_list[i] for i in range(len(averaged_fitness_list))], [averaged_fitness_list[i] + standard_deviation_list[i] for i in range(len(averaged_fitness_list))], color=colors[config_index], alpha=0.1, edgecolor=None)

# Get current handles and labels
handles, labels = plt.gca().get_legend_handles_labels()

# Custom sort function to sort labels by the numeric part
def custom_sort(label):
    return int(label[6:])

# Sort the labels using the custom sort function
sorted_labels = sorted(labels, key=custom_sort)

# Reorder the handles based on the sorted labels
ordered_handles = [handles[labels.index(label)] for label in sorted_labels]

# Pass the reordered handles and labels to plt.legend()
plt.legend(ordered_handles, sorted_labels, loc="lower right", ncol=2)

# Set the x-axis tick locations and labels
tick_intervals = num_evaluations // 10
tick_locations = np.arange(0, len(total_list[0][1][0]), len(total_list[0][1][0]) // 10)
tick_labels = [i * tick_intervals for i in range(len(tick_locations))]
plt.xticks(ticks=tick_locations, labels=tick_labels, rotation=45)

# set the y axis tick locations and labels
tick_intervals = 0.1
tick_locations = np.arange(0, 0.9, 0.1)
tick_labels = [round(i * tick_intervals, 1) for i in range(len(tick_locations))]
plt.yticks(ticks=tick_locations, labels=tick_labels)


plt.title(f"Average Fitness Of Each Config Over {len(total_list[0][1])} Runs")
plt.xlabel("Evaluations")
plt.ylabel("Fitness")

# set image size
plt.gcf().set_size_inches(8, 6)

# set size of the plot
plt.gcf().subplots_adjust(left=0.1, bottom=0.15)

# save the plot
# file_name = f"multi_full_step1_{num_runs}runs_{num_generations}generations_{evals_per_generation}evals.jpg"
# file_path = os.path.join(os.path.dirname(__file__), "heuristic_examinations", "plots", "fitness_plots", "30runs_500generations_8polys", "multi_8poly", file_name)
# os.makedirs(os.path.dirname(file_path), exist_ok=True)

# plt.savefig(file_path, dpi=300)
plt.show()
