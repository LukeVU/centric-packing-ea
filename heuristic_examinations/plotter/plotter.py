from matplotlib import pyplot as plt
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

    plt.tight_layout()
    if save:
        plt.savefig(save_name)
    plt.show()

