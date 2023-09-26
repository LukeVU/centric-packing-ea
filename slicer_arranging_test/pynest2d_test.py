from pynest2d import *


# 1000 x 1000 bounding volume centered around 
# 0 in which the items must be arranged.

volume = Box(10000,10000)


# long_thin_triangle = Item([
#     Point(  200  ,  200  ),
#     Point(  250 , 300 ),
#     Point( 300 , 300 ),
#     Point(  200  ,  200  )
# ])

#CLOCKWISE#
square = Item([
    Point(0,0),
    Point(100,0),
    Point(100,100),
    Point(0,100),
    Point(0,0)
])

square2 = Item([
    Point(200,0),
    Point(300,0),
    Point(300,100),
    Point(200,100),
    Point(200,0)
])
############

#COUNTER CLOCKWISE
# square = Item([
#     Point(0, 0),
#     Point(0, 100),
#     Point(100, 100),
#     Point(100, 0),
#     Point(0, 0)
# ])

# square2 = Item([
#     Point(200, 0),
#     Point(200, 100),
#     Point(300, 100),
#     Point(300, 0),
#     Point(200, 0)
# ])
############

config = NfpConfig()
config.accuracy = 10
config.alignment = NfpConfig.Alignment.CENTER

spacing = 5
# The actual arranging!
item_list = [square, square2]

print(square.area())

# for item in item_list:
#     assert item.is_valid, "Item is not a valid polygon"
#     assert item.area > 0, "Item has zero area"

num_bins = nest(item_list,volume,spacing,config)

print("test")

test = square.transformedShape()

print(test.toString())

# # How many bins are required to add all objects.
# num_bins  #  1

# # Doesn't modify the original item
# transformed_i1 = long_thin_triangle.transformedShape()

# print(transformed_i1.toString())

# # Contour {
# #    18 96
# #    117 46
# #    117 -4
# #    18 96
# # }

# transformed_i1.vertex(0).x()  #  18
# transformed_i1.vertex(0).y()  #  96
# long_thin_triangle.rotation()  #  4.71238898038469