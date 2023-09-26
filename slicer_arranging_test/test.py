from nest2D import Point, Box, Item, nest, SVGWriter

polygons = [
    [(0, 0), (2, 0), (2, 2), (0, 2)],  # Square
    [(0, 0), (3, 0), (3, 1), (2, 1), (2, 2), (0, 2)],  # L-shape
    # Add more polygons as needed
]

items = []
for polygon in polygons:
    item = Item([Point(x, y) for x, y in polygon])
    items.append(item)

print(items)

print(items[0].points)

# center = Point(0, 0)
# box = Box(10, 10)

layout = nest(items, box)

# print(layout)

# for item in layout:
#     position = item.position
#     orientation = item.orientation
#     print(item)
#     print(position, orientation)

# svg_writer = SVGWriter()
# svg_writer.write_packgroup(layout)
# svg_writer.save()