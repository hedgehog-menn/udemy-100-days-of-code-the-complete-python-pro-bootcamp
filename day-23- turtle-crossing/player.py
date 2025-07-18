from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.setheading(90)
        self.penup()
        self.go_to_start()

    def go_up(self):
        # new_y = self.ycor() + MOVE_DISTANCE
        # self.goto(self.xcor(), new_y)
        self.forward(MOVE_DISTANCE)

    def go_down(self):
        # new_y = self.ycor() - MOVE_DISTANCE
        # self.goto(self.xcor(), new_y)
        self.backward(MOVE_DISTANCE)

    def go_left(self):
        new_x = self.xcor() - MOVE_DISTANCE
        self.goto(new_x, self.ycor())

    def go_right(self):
        new_x = self.xcor() + MOVE_DISTANCE
        self.goto(new_x, self.ycor())

    def go_to_start(self):
        self.goto(STARTING_POSITION)

    def is_at_finish_line(self):
        return self.ycor() > FINISH_LINE_Y
        # if self.ycor() > FINISH_LINE_Y:
        #     return True
        # else:
        #     return False