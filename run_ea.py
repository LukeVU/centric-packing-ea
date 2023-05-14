from heuristic_examinations.shape_creation import generate_population
import matplotlib.pyplot as plt
from heuristic_examinations.polys_classes import PolyGroup, Poly
from heuristic_examinations.ea import EABarebones
from heuristic_examinations.plotter import plot_generation, plot_first_and_last
from tqdm import tqdm

LENGTH = 20

NUM_SURVIVORS = 10
NUM_CHILDREN = 50
FIELD_DIAMETER = 20
NUM_GENERATIONS = 500


population = generate_population(number_of_poly_groups= NUM_SURVIVORS, number_of_polys= 5, field_diameter= FIELD_DIAMETER)
# plot_generation(population, FIELD_DIAMETER)

ea = EABarebones(num_survivors= NUM_SURVIVORS, field_diameter= FIELD_DIAMETER, num_children= NUM_CHILDREN)

complete_run = []
population.sort(key = lambda x: x.fitness(), reverse = True)
complete_run.append(population)

best_fitness_list = []
for generation in tqdm(range(NUM_GENERATIONS)):
    population = ea.step(population)
    best_fitness = population[0].fitness()
    # print(f"Generation {generation} has best fitness {best_fitness}")
    best_fitness_list.append(best_fitness)
    complete_run.append(population)
    # plot_generation(population, FIELD_DIAMETER)

plot_first_and_last(complete_run[0], complete_run[-1], FIELD_DIAMETER)

print(f"Best fitness list: {best_fitness_list}")
