
import matplotlib.pyplot as plt

from create_shapes import easy_poly_gen
from move_overlapping import move_and_rotate
from calculate_cir_circle import calc_cir_circle_radius


FIELD_DIAMETER = 20
NUMBER_OF_POLYS = 10
SIZE = 2
IRREGULARITY = 0.5
SPIKINESS = 0.5
NUM_VERTICES = 4
STEP_SIZE = 2
ROTATE_SIZE = 3
STEP_TYPE = "triangular"
ROTATE_TYPE = "triangular"


polys = easy_poly_gen(NUMBER_OF_POLYS, FIELD_DIAMETER, SIZE, IRREGULARITY, SPIKINESS, NUM_VERTICES)

polys_copy = polys.copy()

non_overlapping_polygons = move_and_rotate(polys, FIELD_DIAMETER, STEP_SIZE, ROTATE_SIZE, STEP_TYPE, ROTATE_TYPE)

minimum_circle_diameter = calc_cir_circle_radius(non_overlapping_polygons)

# plot two plots side by side, one with the original polygons and one with the non-overlapping polygons
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
for poly in polys_copy:
    x,y = poly.exterior.xy
    ax1.plot(x, y, color='#6699cc', alpha=0.7,
    linewidth=3, solid_capstyle='round', zorder=2)
    ax1.set_title('Polygon')
ax1.set_title('Original Polygons')
ax1.set_xlim(-FIELD_DIAMETER, FIELD_DIAMETER)
ax1.set_ylim(-FIELD_DIAMETER, FIELD_DIAMETER)
ax1.set_aspect('equal')

for poly in non_overlapping_polygons:
    x,y = poly.exterior.xy
    ax2.plot(x, y, color='#6699cc', alpha=0.7,
    linewidth=3, solid_capstyle='round', zorder=2)

# plot the minimum circle that can contain all polygons, using the diameter calculated above, with the center of the circle at (0,0)
circle = plt.Circle((0, 0), minimum_circle_diameter, color='r', fill=False) # type: ignore
# add the value of the diameter under the plot
ax2.text(0, -FIELD_DIAMETER-5, f"Minimum circle diameter: {minimum_circle_diameter:.2f}", horizontalalignment='center', verticalalignment='center')

ax2.add_artist(circle)
ax2.set_title('Polygon')
ax2.set_title('Non-overlapping Polygons')
ax2.set_xlim(-FIELD_DIAMETER, FIELD_DIAMETER)
ax2.set_ylim(-FIELD_DIAMETER, FIELD_DIAMETER)
ax2.set_aspect('equal')


plt.show()

