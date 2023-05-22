from typing import List, Tuple
import math, random


from ..polys_classes import PolyGroup
from ..polys_classes import Poly
# from ..shape_creation import copy_polygroup
from ..polys_classes import step_calculator, rotate_calculator, overlaps_with_others, outside_field



def randomly_move_polys_to_legal_locations(polys: PolyGroup, field_diameter: int, step_size: float, step_type: str, rotate_size: float, rotate_type: str, attempts: int) -> List[Poly]:
    """Moves and rotates the polygons in the PolyGroup until they no longer overlap with each other or go outside the field.
    """
    # iterate over each polygon in the input list. the polygon is randomly moved and rotated. if it overlaps with another polygon or goes outside the field, it is moved back to its original position and the process is repeated.
    moved_polys = []
    while len(polys._polys) > 0:
        attempts_countdown = attempts
        new_poly = polys._polys[0].copy()
        changing_poly = polys._polys[0].copy()
        polys._polys.remove(polys._polys[0])

        x_offset, y_offset = step_calculator(step_size, step_type)
        angle = rotate_calculator(rotate_size, rotate_type)
        changing_poly.translate(x_offset, y_offset)
        changing_poly.rotate(angle)
        while (overlaps_with_others(changing_poly, polys._polys) or overlaps_with_others(changing_poly, moved_polys) or outside_field(changing_poly, field_diameter)) and attempts_countdown > 0:
            changing_poly = new_poly.copy()
            changing_poly.translate(x_offset, y_offset)
            changing_poly.rotate(angle)
            x_offset, y_offset = step_calculator(step_size, step_type)
            angle = rotate_calculator(rotate_size, rotate_type)
            changing_poly.translate(x_offset, y_offset)
            changing_poly.rotate(angle)
            attempts_countdown -= 1
        if attempts_countdown == 0:
            moved_polys.append(new_poly)
        else:
            moved_polys.append(changing_poly)

    polys._polys = moved_polys
    return polys



def create_recombined_child(parents: List[PolyGroup], field_diameter, step_size, step_type, rotate_size, rotate_type) -> PolyGroup:
    """ For each polygon in the parent, calculate a location and rotation in between the locations and rotations of the two parents.
    """
    list_of_children = []
    for i in range(len(parents[0]._polys)):
        # find the polygon in the second parent with the same .index as the polygon in the first parent
        for j in range(len(parents[1]._polys)):
            if parents[0]._polys[i].index == parents[1]._polys[j].index:
                tri_value = random.triangular(-1, 1)
                y_delta = parents[0]._polys[i].polygon.centroid.y - parents[1]._polys[j].polygon.centroid.y
                x_delta = parents[0]._polys[i].polygon.centroid.x - parents[1]._polys[j].polygon.centroid.x

                rotation_delta = parents[0]._polys[i].rotation - parents[1]._polys[j].rotation
                if rotation_delta > 180:
                    rotation_delta = rotation_delta - 360

                total_rotation = rotation_delta/2 + tri_value*rotation_delta/2
                
                new_poly: Poly = parents[1]._polys[j].copy()
                new_poly.index = parents[1]._polys[j].index
                new_poly.rotation = parents[1]._polys[j].rotation 
                distance_moved = math.sqrt((x_delta/2 + tri_value*x_delta/2)**2 + (y_delta/2 + tri_value*y_delta/2)**2) 
                new_poly.translate(x_delta/2 + tri_value*x_delta/2, y_delta/2 + tri_value*y_delta/2)
                new_poly.rotate(total_rotation)
                new_poly.distance_moved = distance_moved
                list_of_children.append(new_poly)

    # make sure that none of the polygons are overlapping in the new child
    # sort the list of polygons by distance moved, in descending order
    list_of_children.sort(key = lambda x: x.distance_moved, reverse = True)
    poly_list = PolyGroup(list_of_children)
    poly_list.non_overlap(field_diameter, step_size, step_type, rotate_size, rotate_type)
    poly_list.shuffle()
    return poly_list



def randomly_move_polys_to_legal_locations_closer(polys: PolyGroup, field_diameter: int, step_size: float, step_type: str, rotate_size: float, rotate_type: str, attempts: int) -> List[Poly]:
    """Moves and rotates the polygons in the PolyGroup until they no longer overlap with each other or go outside the field and are closer to the center of the field.
    """
    # iterate over each polygon in the input list. the polygon is randomly moved and rotated. if it overlaps with another polygon or goes outside the field, it is moved back to its original position and the process is repeated.
    moved_polys = []
    while len(polys._polys) > 0:
        attempts_countdown = attempts
        new_poly = polys._polys[0].copy()
        changing_poly = polys._polys[0].copy()
        polys._polys.remove(polys._polys[0])

        initial_distance = changing_poly.get_furthest_distance()

        x_offset, y_offset = step_calculator(step_size, step_type)
        angle = rotate_calculator(rotate_size, rotate_type)
        changing_poly.translate(x_offset, y_offset)
        changing_poly.rotate(angle)

        new_distance = changing_poly.get_furthest_distance()
        while (overlaps_with_others(changing_poly, polys._polys) or overlaps_with_others(changing_poly, moved_polys) or outside_field(changing_poly, field_diameter) or (new_distance > initial_distance)) and attempts_countdown > 0:
            changing_poly = new_poly.copy()
            changing_poly.translate(x_offset, y_offset)
            changing_poly.rotate(angle)
            x_offset, y_offset = step_calculator(step_size, step_type)
            angle = rotate_calculator(rotate_size, rotate_type)
            changing_poly.translate(x_offset, y_offset)
            changing_poly.rotate(angle)
            new_distance = changing_poly.get_furthest_distance()
            attempts_countdown -= 1
        if attempts_countdown == 0:
            moved_polys.append(new_poly)
            # print("failed")
        else:
            moved_polys.append(changing_poly)

    polys._polys = moved_polys
    return polys