import math, random
from typing import List, Tuple
from shapely.geometry import Polygon

from ..polys_classes import PolyGroup
from .create_shapes import easy_poly_gen
from ..polys_classes import Poly
from .create_same_shape_list import generate_population

import dill as pickle

import datetime
import sys
import os
from tqdm import tqdm

def create_saved_population_group(num_populations: int, number_of_poly_groups : int, number_of_polys: int, field_diameter: int, 
                        step_size = .2, step_type = "triangular", rotate_size: float = 0.1, 
                        rotate_type: str = "uniform", size: float = 3, 
                        irregularity: float = 0.5, spikiness: float = 0.5,
                        num_vertices: int = 4) -> None:
    population_group = []
    # progress bar for creating the population group
    for i in tqdm(range(num_populations), desc=f"Creating population group", leave=False, bar_format="{desc:<30}| {percentage:3.0f}% |{bar:40}| {elapsed}/{remaining} | {n_fmt}/{total_fmt}"):
        population_group.append(generate_population(number_of_poly_groups, number_of_polys, field_diameter, step_size, step_type, rotate_size, rotate_type, size, irregularity, spikiness, num_vertices))

    # create the file name for the population group
    now = datetime.datetime.now()
    file_name = f"population_{num_populations}populations_{number_of_poly_groups}groups_{number_of_polys}polys_{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}.pickle"

    # set file path for where to save the population group. place the file inside the saved_populations folder, which is one level above this file
    file_path = os.path.join(os.path.dirname(__file__), "..", "saved_populations", file_name)

    # save the population group as a pickle file to the file path with the file name
    with open(file_path, "wb") as f:
        pickle.dump(population_group, f)


def read_population_group(file_name: str = None) -> List[List[PolyGroup]]:
    
    if file_name is None:
        # if no file name is given, look for the most recent file in the saved_populations folder
        # get the list of files in the saved_populations folder
        file_list = os.listdir(os.path.join(os.path.dirname(__file__), "..", "saved_populations"))
        # sort the list of files by date modified
        file_list.sort(key=lambda x: os.path.getmtime(os.path.join(os.path.dirname(__file__), "..", "saved_populations", x)), reverse=True)
        # get the most recent file name
        file_path = os.path.join(os.path.dirname(__file__), "..", "saved_populations", file_list[0])

    else:
        # look for the file name in the saved_populations folder
        file_path = os.path.join(os.path.dirname(__file__), "..", "saved_populations", file_name)

    # read the population group from the pickle file
    with open(file_path, "rb") as f:
        population_group = pickle.load(f)

    return population_group
