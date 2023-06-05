import os
import pickle
from scipy.stats import kruskal, wilcoxon
import itertools

num_generations = 500
evals_per_generation = 50
num_evaluations = num_generations * evals_per_generation

# This script is used to plot the collective results of multiple configs in a single plot
complete_fitness_lists = []
configs = []

# path to the folder in the results folder that contains the results to be plotted
folder_path = "heuristic_examinations\\results\\multi_full_step5"

# iterate through the files in the folder
for file_name in os.listdir(folder_path):
    config = file_name.split("_")[1]

    file_path = os.path.join(folder_path, file_name)
    # read the file
    with open(file_path, "rb") as f:
        loaded_file = pickle.load(f)

    # convert the loaded file to the average fitness over time
    fitness_lists = []
    for complete_run in loaded_file[0]:
        fitness_list = []
        for generation in complete_run:
            fitness_list.append(generation[0].fitness())
        fitness_lists.append(fitness_list)
    complete_fitness_lists.append([config, fitness_lists])

# sort the complete fitness lists by config
complete_fitness_lists.sort(key=lambda x: int(x[0][6:]))

# remove the configs from the complete fitness lists
for i in range(len(complete_fitness_lists)):
    complete_fitness_lists[i] = complete_fitness_lists[i][1]

final_fitness_lists = []
for fitness_list in complete_fitness_lists:
    final_fitnesses = []
    for run in fitness_list:
        final_fitnesses.append(run[-1])
    final_fitness_lists.append(final_fitnesses)


# num_runs = len(loaded_file[0])

# average_list = []
# for i in range(len(complete_fitness_lists)):
#     fitness_list = complete_fitness_lists[i]
#     averaged_fitness_list = []
#     for i in range(len(fitness_list[0])):
#         averaged_fitness_list.append(sum(fitness_list[j][i] for j in range(len(fitness_list))) / len(fitness_list))
#     average_list.append(averaged_fitness_list)

pairs = list(itertools.combinations(final_fitness_lists, 2))

p_limit = 0.05 

for pair in pairs:
    H, p_value = wilcoxon(pair[0], pair[1])
    formatted_p_value = format(p_value, ".20f")
    # formatted_h = format(H, ".100f")
    # give the index of the pair in the average_list
    if p_value < p_limit:
        note = "SIGNIFICANT"
    else:
        note = "NOT SIGNIFICANT"
    print(f"### {note} ### The pair config{final_fitness_lists.index(pair[0])+1} and config{final_fitness_lists.index(pair[1])+1} have a \n H statistic of {H} \n p-value of {formatted_p_value} \n")

for pair in pairs:
    H, p_value = wilcoxon(pair[0], pair[1])
    if p_value > p_limit:
        print(f"config{final_fitness_lists.index(pair[0])+1} and config{final_fitness_lists.index(pair[1])+1} are similar and have a p-value of {p_value}")



# H, p_value = kruskal(average_list[0], average_list[1], average_list[2], average_list[3], average_list[4], average_list[5], average_list[6], average_list[7], average_list[8], average_list[9], average_list[10], average_list[11], average_list[12], average_list[13], average_list[14], average_list[15])
# H, p_value = kruskal(average_list[0], average_list[2])


# print("H statistic:", H)
# formatted_p_value = format(p_value, ".100f")
# print("p-value:", formatted_p_value)