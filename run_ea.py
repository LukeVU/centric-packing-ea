from heuristic_examinations.shape_creation import generate_population, create_saved_population_group, read_population_group
import matplotlib.pyplot as plt
from heuristic_examinations.polys_classes import PolyGroup, Poly
from heuristic_examinations.ea import EABarebones
from heuristic_examinations.plotter import plot_generation, plot_first_and_last, plot_fitness_over_time, plot_fitness_over_time_multiple_runs
from tqdm import tqdm

NUM_POLYS = 5
NUM_SURVIVORS = 10
NUM_CHILDREN = 40
FIELD_DIAMETER = 20
NUM_GENERATIONS = 500
NUM_RUNS = 30

# BELOW IS FOR GENERATING A NEW POPULATION
# create_saved_population_group(num_populations= NUM_RUNS, number_of_poly_groups= NUM_SURVIVORS, number_of_polys= NUM_POLYS, field_diameter= FIELD_DIAMETER)

# BELOW IS FOR READING A PREVIOUSLY GENERATED POPULATION. When kept empty, it will read the most recently generated population
populations = read_population_group()

complete_runs = []

with tqdm(total = len(populations) * NUM_GENERATIONS) as pbar: 
    for i in tqdm(range(len(populations)), disable=True):
        # population = generate_population(number_of_poly_groups= NUM_SURVIVORS, number_of_polys= NUM_POLYS, field_diameter= FIELD_DIAMETER)
        ea = EABarebones(num_survivors= NUM_SURVIVORS, field_diameter= FIELD_DIAMETER, num_children= NUM_CHILDREN)

        complete_run = []
        populations[i].sort(key = lambda x: x.fitness(), reverse = True)
        complete_run.append(populations[i])


        for generation in tqdm(range(NUM_GENERATIONS), desc=f"Run {i+1} out of {NUM_RUNS}", leave=False):
            populations[i] = ea.step(populations[i])
            best_fitness = populations[i][0].fitness()
            # print(f"Generation {generation} has best fitness {best_fitness}")
            complete_run.append(populations[i])
            # plot_generation(population, FIELD_DIAMETER)
            pbar.update(1)

        # plot_first_and_last(complete_run[0], complete_run[-1], FIELD_DIAMETER)
        # plot_fitness_over_time(complete_run)

        complete_runs.append(complete_run)

plot_fitness_over_time_multiple_runs(complete_runs, NUM_SURVIVORS+NUM_CHILDREN)
