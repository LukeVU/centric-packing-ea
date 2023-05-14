from heuristic_examinations.shape_creation import generate_population
import matplotlib.pyplot as plt
from heuristic_examinations.plotter import plot_generation

population = generate_population(2, 5, 20)

print(population[0])
# the population, each poly group in its own subplot
# the plots are square, so the polygons are not distorted


fig, axs = plt.subplots(1, len(population), figsize=(10, 5))
for i in range(len(population)):
    axs[i].set_title("Poly Group " + str(i))

for i in range(len(population)):
    # plot the polygons in the poly group
    for poly in population[i]._polys:
        axs[i].plot(*poly.polygon.exterior.xy)
    # add the rotation of each polygon at the centroid of each polygon
    for poly in population[i]._polys:
        rotation_string = str(round(poly.rotation, 2))
        axs[i].text(poly.polygon.centroid.x-(len(rotation_string))/2.5, poly.polygon.centroid.y, rotation_string)
    # set the x and y limits of the plot to the field diameter
    axs[i].set_xlim(-20, 20)
    axs[i].set_ylim(-20, 20)
    # set the aspect ratio to 1 so that the polygons are not distorted
    axs[i].set_aspect(1)

plt.tight_layout()
plt.show()