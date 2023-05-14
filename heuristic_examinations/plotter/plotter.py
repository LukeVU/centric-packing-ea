import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize
import math

def plot_generation(generation, field_diameter, save=False, save_name=""):
    num_cols = math.ceil(len(generation) / 2)
    fig, axs = plt.subplots(2, num_cols, figsize=(15, 10))
    for i in range(len(generation)):
        row = i // num_cols
        col = i % num_cols
        axs[row, col].set_title("Poly Group " + str(i))

    for i in range(len(generation)):
        row = i // num_cols
        col = i % num_cols
        # plot the polygons in the poly group
        for poly in generation[i]._polys:
            axs[row, col].plot(*poly.polygon.exterior.xy)
        # add the rotation of each polygon at the centroid of each polygon
        for poly in generation[i]._polys:
            rotation_string = str(round(poly.rotation, 2))
            axs[row, col].text(poly.polygon.centroid.x-(len(rotation_string))/2.5, poly.polygon.centroid.y, rotation_string)
        # set the x and y limits of the plot to the field diameter
        axs[row, col].set_xlim(-field_diameter, field_diameter)
        axs[row, col].set_ylim(-field_diameter, field_diameter)
        # set the aspect ratio to 1 so that the polygons are not distorted
        axs[row, col].set_aspect(1)
        # give each polygon an exterior color based on its index. it has no fill color
        for poly in generation[i]._polys:
            x, y = poly.polygon.exterior.xy
            axs[row, col].fill(x, y, color=(poly.index/len(generation[i]._polys), 0, 0, 0), linewidth=1)

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
    max_index = max(max(poly.index for poly in first[0]._polys), max(poly.index for poly in last[0]._polys))
    
    # Create a Normalize instance to scale the index values
    norm = Normalize(vmin=0, vmax=max_index)

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