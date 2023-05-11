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
for i in range(2):
    for poly in population[i]._polys:
        x, y = poly.exterior.xy
        axs[i].plot(x, y, color="#6699cc", alpha=0.7, linewidth=3, solid_capstyle="round", zorder=2)
        axs[i].set_aspect("equal")
        axs[i].set_xlim(-20, 20)
        axs[i].set_ylim(-20, 20)
        axs[i].set_facecolor("#ffffff")
        axs[i].grid(True)

plt.tight_layout()
plt.show()

plt.show()