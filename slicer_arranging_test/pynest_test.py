from nest2d import Polygon, arrange_polygons

# Define the coordinates of the vertices for the two polygons
polygon1_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
polygon2_vertices = [(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5)]

# Create Polygon objects for each polygon
polygon1 = Polygon(polygon1_vertices)
polygon2 = Polygon(polygon2_vertices)

# Arrange the polygons
arranged_polygons = arrange_polygons([polygon1, polygon2])

# Print the vertices of the first arranged polygon
print(arranged_polygons[0].vertices)
