import math, random
from typing import List, Tuple
from shapely.geometry import Polygon
import dill as pickle
import datetime
import sys
import os
from tqdm import tqdm

from ..polys_classes import PolyGroup, Poly



def create_saved_custom_population(number_of_poly_groups : int, polys : List[Poly], field_diameter: int, 
                        step_size = .2, step_type = "triangular", rotate_size: float = 0.1, 
                        rotate_type: str = "uniform") -> None:
    population_group = []
    # progress bar for creating the population group
    for i in tqdm(range(number_of_poly_groups), desc=f"Creating population group", leave=False, bar_format="{desc:<30}| {percentage:3.0f}% |{bar:40}| {elapsed}/{remaining} | {n_fmt}/{total_fmt}"):
        population_group.append(generate_custom_population(number_of_poly_groups, polys, field_diameter, step_size, step_type, rotate_size, rotate_type))

    # create the file name for the population group
    now = datetime.datetime.now()
    file_name = f"CustomPopulation_{number_of_poly_groups}polyGroups_{len(polys)}polys_{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}.pickle"

    # set file path for where to save the population group. place the file inside the saved_populations folder, which is one level above this file
    file_path = os.path.join(os.path.dirname(__file__), "..", "saved_populations", "custom_populations", file_name)

    # save the population group as a pickle file to the file path with the file name
    with open(file_path, "wb") as f:
        pickle.dump(population_group, f)

def read_custom_population_group(file_name: str = None) -> List[List[PolyGroup]]:
    
    if file_name is None:
        # if no file name is given, look for the most recent file in the saved_populations folder
        # get the list of files in the saved_populations folder
        file_list = os.listdir(os.path.join(os.path.dirname(__file__), "..", "saved_populations", "custom_populations"))
        # sort the list of files by date modified
        file_list.sort(key=lambda x: os.path.getmtime(os.path.join(os.path.dirname(__file__), "..", "saved_populations", "custom_populations", x)), reverse=True)
        # get the most recent file name
        file_path = os.path.join(os.path.dirname(__file__), "..", "saved_populations", "custom_populations", file_list[0])

    else:
        # look for the file name in the saved_populations folder
        file_path = os.path.join(os.path.dirname(__file__), "..", "saved_populations", "custom_populations", file_name)

    # read the population group from the pickle file
    with open(file_path, "rb") as f:
        population_group = pickle.load(f)

    return population_group





# takes a list of Polys and returns a list of x PolyGroups, each with the same Polys

def generate_custom_population(number_of_poly_groups : int, polys : List[Poly], field_diameter: int, 
                        step_size = .2, step_type = "triangular", rotate_size: float = 0.1, 
                        rotate_type: str = "uniform") -> List[PolyGroup]:
    
    # create a list of PolyGroups with number_of_poly_groups instances of the original_instance
    population = [PolyGroup(polys) for _ in range(number_of_poly_groups)]

    # for each PolyGroup in the population, create a new Poly object for each polygon in the PolyGroup
    population_unique: List[PolyGroup] = []
    for poly_group in population:
        population_unique.append(poly_group.copy())


    # for each PolyGroup in the population, randomize the locations and rotations of the polygons, then move them so that they don't overlap
    for poly_group in population_unique:
        poly_group.randomize_poly_locations_and_rotations(field_diameter)
        poly_group.non_overlap(field_diameter, step_size, step_type, rotate_size, rotate_type)


    return population_unique