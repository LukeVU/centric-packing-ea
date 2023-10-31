import pickle
from heuristic_examinations.plotter import plot_first_and_last
import os
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize

RUN_NUMBER = 0

folder_path = "heuristic_examinations\\results\\multi_full_step5"

# configs = []

# # iterate through the files in the folder
# for file_name in os.listdir(folder_path):
#     config = file_name.split("_")[1]

#     file_path = os.path.join(folder_path, file_name)
#     # read the file
#     with open(file_path, "rb") as f:
#         loaded_file = pickle.load(f)
    
#     configs.append((config, loaded_file[0][RUN_NUMBER]))

# # save configs to a pickle file
# with open("heuristic_examinations\\results\\multi_full_step5\\configs.pkl", "wb") as f:
#     pickle.dump(configs, f)

# load configs from pickle file
with open("heuristic_examinations\\results\\multi_full_step5\\configs.pkl", "rb") as f:
    configs = pickle.load(f)


# a function to display the best poly group in each generation, for each config, in a single plot, in 1 4x4 grid, in order from best final fitness to worst final fitness
def plot_all_configs_each_gen(complete_ea_runs):

    # sort the complete_ea_runs from best final fitness to worst final fitness
    complete_ea_runs.sort(key=lambda x: x[1][-1][0].fitness(), reverse=True)

    # create a 4x4 grid of plots
    fig, axs = plt.subplots(4, 4, figsize=(12.8, 15.2))

    # set plot title
    fig.suptitle(f"Best Instance in Each Generation, For Each Config, Over 500 Generations", x=.48, fontsize=18)
    cmap = get_cmap('gist_rainbow')
    norm = Normalize(vmin=0, vmax=4)
    
    # repeat this for each generation
    for generation_number in range(len(complete_ea_runs[0][1])):
        # set the sub title of the plot to the generation number
        gen_text = fig.text(0.48, 0.92, f"Generation {str(generation_number).zfill(3)}", ha='center', fontsize=14)

        # repeat this for each config
        for config_index in range(len(complete_ea_runs)):
            # plot the poly group
            for poly in complete_ea_runs[config_index][1][generation_number][0]._polys:
                axs[config_index // 4][config_index % 4].plot(*poly.polygon.exterior.xy, color=cmap(norm(poly.index)))
            # set the title of the plot to the generation number
            axs[config_index // 4][config_index % 4].set_title(f"{complete_ea_runs[config_index][0]}")
            # set the x and y limits of each plot to the field diameter
            axs[config_index // 4][config_index % 4].set_xlim(-20, 20)
            axs[config_index // 4][config_index % 4].set_ylim(-20, 20)
            # set the aspect ratio to 1 so that the polygons are not distorted
            axs[config_index // 4][config_index % 4].set_aspect(1)

            # add the circle of the minimal circumscribed circle
            circle = plt.Circle((0, 0), complete_ea_runs[config_index][1][generation_number][0].get_minimal_circumscribed_circle_radius(), color='r', fill=False)
            axs[config_index // 4][config_index % 4].add_artist(circle)

            # hide the axis ticks
            axs[config_index // 4][config_index % 4].set_xticks([])
            axs[config_index // 4][config_index % 4].set_yticks([])

            # set the size of the plot
            plt.gcf().subplots_adjust(left=0.05, bottom=0.1, right=0.90, top=0.9, wspace=0.05, hspace=0.1)

            # add the fitness of each plot as a text box
            axs[config_index // 4][config_index % 4].text(-19, 16, f"Fitness: {complete_ea_runs[config_index][1][generation_number][0].fitness():.2f}", fontsize=12)


        # save the plot
        file_name = f"multi_full_step5_{str(generation_number).zfill(3)}.jpg"
        file_path = os.path.join(os.path.dirname(__file__), "heuristic_examinations", "plots", "animations", "test4", file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        plt.savefig(file_path, dpi=50, bbox_inches='tight')
        # clear all axes
        for ax in axs.flatten():
            ax.cla()
        # remove the generation text
        gen_text.remove()


plot_all_configs_each_gen(configs)

