from heuristic_examinations.shape_creation import generate_population
import matplotlib.pyplot as plt

population = generate_population(2, 5, 20)
print("done")
print(population[0])
print(population[1])

# the population, each poly group in its own subplot
# the plots are square, so the polygons are not distorted
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
axs[0].set_title("Poly Group 1")
axs[1].set_title("Poly Group 2")
for i in range(len(population)):
    #make the first poly in the poly group red
    axs[i].plot(*population[i]._polys[0].exterior.xy, color="red")
    #make the other polys in the poly group blue
    for j in range(1, len(population[i]._polys)):
        axs[i].plot(*population[i]._polys[j].exterior.xy, color="blue")
    # set the x and y limits of the plot to the field diameter
    axs[i].set_xlim(-20, 20)
    axs[i].set_ylim(-20, 20)
    # set the aspect ratio to 1 so that the polygons are not distorted
    axs[i].set_aspect(1)

plt.tight_layout()
plt.show()