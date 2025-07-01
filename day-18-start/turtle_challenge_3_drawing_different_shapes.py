import turtle as t

tim = t.Turtle()

# Turtle Challenge 3 - Drawing Different Shapes
def draw_shape(num_sides):
    angle = 360 / num_sides
    for _ in range(num_sides):
        tim.forward(100)
        tim.right(angle)

for shape_in_n in range(3, 11):
    draw_shape(shape_in_n)