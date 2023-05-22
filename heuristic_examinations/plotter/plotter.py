import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize
import math
import numpy as np
import os
import datetime

def plot_generation(generation, field_diameter, save=False, save_name=""):
    num_cols = len(generation)
    fig, axs = plt.subplots(1, num_cols, figsize=(15, 5))
    for i in range(len(generation)):
        # plot the polygons in the poly group
        for poly in generation[i]._polys:
            axs[i].plot(*poly.polygon.exterior.xy)
        # add the rotation of each polygon at the centroid of each polygon
        for poly in generation[i]._polys:
            rotation_string = str(round(poly.rotation, 2))
            axs[i].text(poly.polygon.centroid.x-(len(rotation_string))/2.5, poly.polygon.centroid.y, rotation_string)
        # set the x and y limits of the plot to the field diameter
        axs[i].set_xlim(-field_diameter, field_diameter)
        axs[i].set_ylim(-field_diameter, field_diameter)
        # set the aspect ratio to 1 so that the polygons are not distorted
        axs[i].set_aspect(1)
        # give each polygon an exterior color based on its index. it has no fill color
        for poly in generation[i]._polys:
            x, y = poly.polygon.exterior.xy
            axs[i].fill(x, y, color=(poly.index/len(generation[i]._polys), 0, 0, 0), linewidth=1)

        for poly in generation[i]._polys:
            index_string = str(poly.index)
            axs[i].text(poly.polygon.centroid.x-(len(index_string))/2.5, poly.polygon.centroid.y - 2, index_string)

    plt.tight_layout()
    if save:
        plt.savefig(save_name)
    plt.show()

def plot_first_and_last(first, last, field_diameter):
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].set_title("First Generation")
    axs[1].set_title("Last Generation")
    
    cmap = get_cmap('gist_rainbow')
    
    # Find the maximum index value for normalization
    # max_index = max(max(poly.index for poly in first[0]._polys), max(poly.index for poly in last[0]._polys))
    
    # Create a Normalize instance to scale the index values
    norm = Normalize(vmin=0, vmax=4)

    # plot the polygons in the poly group
    for poly in first[0]._polys:
        axs[0].plot(*poly.polygon.exterior.xy, color=cmap(norm(poly.index)))
    for poly in last[0]._polys:
        axs[1].plot(*poly.polygon.exterior.xy, color=cmap(norm(poly.index)))

    # add the index of each polygon at the centroid of each polygon
    for poly in first[0]._polys:
        index_string = str(poly.index)
        axs[0].text(poly.polygon.centroid.x-(len(index_string))/2.5, poly.polygon.centroid.y, index_string)
    for poly in last[0]._polys:
        index_string = str(poly.index)
        axs[1].text(poly.polygon.centroid.x-(len(index_string))/2.5, poly.polygon.centroid.y, index_string)
    
    # set the x and y limits of the plot to the field diameter
    axs[0].set_xlim(-field_diameter, field_diameter)
    axs[0].set_ylim(-field_diameter, field_diameter)
    axs[1].set_xlim(-field_diameter, field_diameter)
    axs[1].set_ylim(-field_diameter, field_diameter)
    # set the aspect ratio to 1 so that the polygons are not distorted
    axs[0].set_aspect(1)
    axs[1].set_aspect(1)

    # add the circle of the minimal circumscribed circle to each plot
    circle_first = plt.Circle((0, 0), first[0].get_minimal_circumscribed_circle_radius(), color='r', fill=False)
    axs[0].add_artist(circle_first)
    circle_last = plt.Circle((0, 0), last[0].get_minimal_circumscribed_circle_radius(), color='r', fill=False)
    axs[1].add_artist(circle_last)

    plt.tight_layout()
    plt.show()


def plot_fitness_over_time(complete_run):
    # plot the fitness of the best poly group in each generation. the y axis is the fitness and the x axis is the number of evaluations.
    # the number of evaluations is the number of generations multiplied by the number of children + parents per generation
    num_evaluations = len(complete_run) * (len(complete_run[0]) + len(complete_run[0][0]._polys))
    fitness_list = []
    for generation in complete_run:
        fitness_list.append(generation[0].fitness())
    plt.plot(range(len(complete_run)), fitness_list)
    # make the x axis display num_evaluations over 10 intervals
    plt.xticks(range(0, len(complete_run), len(complete_run)//10), range(0, num_evaluations, num_evaluations//10))
    plt.title("Fitness Over Time")
    plt.xlabel("Evaluations")
    plt.ylabel("Fitness")
    plt.show()


def plot_fitness_over_time_multiple_runs(complete_runs, num_evaluations, ea: str):
    num_evaluations = num_evaluations * (len(complete_runs[0])-1)
    fitness_lists = []
    for complete_run in complete_runs:
        fitness_list = []
        for generation in complete_run:
            fitness_list.append(generation[0].fitness())
        fitness_lists.append(fitness_list)
    
    for fitness_list in fitness_lists:
        plt.plot(range(len(complete_runs[0])), fitness_list, color="gray", linewidth=0.3)
    
    averaged_fitness_list = []
    for i in range(len(fitness_lists[0])):
        averaged_fitness_list.append(sum(fitness_lists[j][i] for j in range(len(fitness_lists))) / len(fitness_lists))
    plt.plot(range(len(complete_runs[0])), averaged_fitness_list, color="black", linewidth=2)

    std_list = []
    for i in range(len(fitness_lists[0])):
        std = np.std([fitness_lists[j][i] for j in range(len(fitness_lists))])
        std_list.append((averaged_fitness_list[i] - std, averaged_fitness_list[i] + std))

    plt.fill_between(range(len(complete_runs[0])), [item[0] for item in std_list], [item[1] for item in std_list], alpha=0.2, color='black')
    
    final_average = averaged_fitness_list[-1]
    final_std_range = std*2

    # Set the x-axis tick locations and labels
    tick_intervals = num_evaluations // 10
    tick_locations = np.arange(0, len(complete_runs[0]), len(complete_runs[0]) // 10)
    tick_labels = [i * tick_intervals for i in range(len(tick_locations))]
    plt.xticks(ticks=tick_locations, labels=tick_labels, rotation=45)

    # set the y axis tick locations and labels
    tick_intervals = 0.1
    tick_locations = np.arange(0, 0.8, 0.1)
    tick_labels = [round(i * tick_intervals, 1) for i in range(len(tick_locations))]
    plt.yticks(ticks=tick_locations, labels=tick_labels)
    
    plt.title(f"Averaged Fitness Over {len(complete_runs)} Runs, {ea}")
    plt.xlabel("Evaluations")
    plt.ylabel("Fitness")

    plt.text(0.6, 0.1, f"Final Average: {final_average:.3f}\nFinal Std Range: {(final_std_range):.3f}", transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5, boxstyle='round'))

    # set image size
    plt.gcf().set_size_inches(8, 6)

    # set size of the plot
    plt.gcf().subplots_adjust(left=0.1, bottom=0.15)
    # plt.show()
    return plt

def plot_saver(complete_runs, num_runs: int, number_of_generations : int, number_of_polys: int, ea: str, time_params: str = None):
    plot = plot_fitness_over_time_multiple_runs(complete_runs, number_of_generations, ea)
    if time_params is None:
        now = datetime.datetime.now()
        file_name = f"{ea}_{num_runs}runs_{number_of_generations}generations_{number_of_polys}polys___{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}.png"
    else:
        file_name = f"{ea}_{num_runs}runs_{number_of_generations}generations_{number_of_polys}polys___{time_params}.png"
    folder_name = f"{num_runs}runs_{number_of_generations}generations_{number_of_polys}polys"
    file_path = os.path.join(os.path.dirname(__file__), "..", "plots", "fitness_plots", folder_name, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    plot.savefig(file_path)
    plot.close()