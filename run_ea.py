from heuristic_examinations.shape_creation import generate_population, create_saved_population_group, read_population_group
import matplotlib.pyplot as plt
from heuristic_examinations.polys_classes import PolyGroup, Poly
from heuristic_examinations.ea import EABarebones, EARecombination
from heuristic_examinations.plotter import plot_generation, plot_first_and_last, plot_fitness_over_time, plot_fitness_over_time_multiple_runs, plot_saver
from tqdm import tqdm

NUM_POLYS = 5
NUM_SURVIVORS = 10
NUM_CHILDREN = 40
FIELD_DIAMETER = 20

NUM_GENERATIONS = 500
NUM_RUNS = 30

class_mappings = {
    "EABarebones": EABarebones,
    "EARecombination": EARecombination
}

list_of_eas = ["EABarebones", "EARecombination"]
# BELOW IS FOR GENERATING A NEW POPULATION
create_saved_population_group(num_populations= NUM_RUNS, number_of_poly_groups= NUM_SURVIVORS, number_of_polys= NUM_POLYS, field_diameter= FIELD_DIAMETER)

# BELOW IS FOR READING A PREVIOUSLY GENERATED POPULATION. When kept empty, it will read the most recently generated population
populations = read_population_group()

complete_runs = []

total_value = len(list_of_eas) * len(populations) * NUM_GENERATIONS

with tqdm(total=total_value, leave=False, desc=f"Complete progress", smoothing=0.01) as pbar:
    for ea_index, ea_pick in enumerate(list_of_eas):
        with tqdm(total=len(populations) * NUM_GENERATIONS, leave=False, desc=f"EA {ea_index + 1} out of {len(list_of_eas)}: {ea_pick}") as pbar_inner:
            for i in range(len(populations)):
                ea = class_mappings[ea_pick](num_survivors=NUM_SURVIVORS, field_diameter=FIELD_DIAMETER, num_children=NUM_CHILDREN)

                complete_run = []
                populations[i].sort(key=lambda x: x.fitness(), reverse=True)
                complete_run.append(populations[i])

                for generation in tqdm(range(NUM_GENERATIONS), desc=f"Run {i+1} out of {NUM_RUNS}", leave=False):
                    populations[i] = ea.step(populations[i])
                    best_fitness = populations[i][0].fitness()
                    single_gen = populations[i]
                    complete_run.append(single_gen)
                    pbar.update(1)
                    pbar_inner.update(1)

                complete_runs.append(complete_run)

        plot_saver(plot_fitness_over_time_multiple_runs(complete_runs, NUM_SURVIVORS + NUM_CHILDREN, ea_pick), NUM_RUNS, NUM_GENERATIONS, NUM_POLYS, ea_pick)