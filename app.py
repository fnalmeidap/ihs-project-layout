import os, sys
import turtle

from operator import truediv
from fcntl import ioctl
from scripts.board import DE2i

fd = os.open("/dev/mydev", os.O_RDWR)

################################## BOARD SETUP ##################################

displays = {"side":"right", "d1": 1, "d2":1, "d3":9, "d4": 9}
red_leds_dict = { 0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:1 }
green_leds_dict = { 0:1, 1:0, 2:1, 3:0, 4:0, 5:0, 6:0, 7:1, 8:1 }

############################# GAME SETUP ##########################################

screen_color = "black"
ball_color = "red"
left_paddle_color = "white"
right_paddle_color = "white"

left_paddle_shape = "square"
right_paddle_shape = "square"

switch_1 = True
switch_2 = True

# Create screen
sc = turtle.Screen()
sc.title("Pong game")
sc.bgcolor(screen_color)
sc.setup(width=1000, height=600)


# Left paddle
left_pad = turtle.Turtle()
left_pad.speed(0)
left_pad.shape(left_paddle_shape)
left_pad.color(left_paddle_color)
left_pad.shapesize(stretch_wid=6, stretch_len=1)
left_pad.penup()
left_pad.goto(-400, 0)


# Right paddle
right_pad = turtle.Turtle()
right_pad.speed(0)
right_pad.shape(right_paddle_shape)
right_pad.color(right_paddle_color)
right_pad.shapesize(stretch_wid=6, stretch_len=1)
right_pad.penup()
right_pad.goto(400, 0)


# Ball of circle shape
hit_ball = turtle.Turtle()
hit_ball.speed(40)
hit_ball.shape("circle")
hit_ball.color(ball_color)
hit_ball.penup()
hit_ball.goto(0, 0)
hit_ball.dx = 5
hit_ball.dy = -5


# Initialize the score
left_player = 0
right_player = 0


# Displays the score
sketch = turtle.Turtle()
sketch.speed(0)
sketch.color("blue")
sketch.penup()
sketch.hideturtle()
sketch.goto(0, 260)
sketch.write("Left_player : 0 Right_player: 0",
			align="center", font=("Courier", 24, "normal"))

# Functions to move paddle vertically
def paddleaup():
	y = left_pad.ycor()
	y += 20
	left_pad.sety(y)


def paddleadown():
	y = left_pad.ycor()
	y -= 20
	left_pad.sety(y)


def paddlebup():
	y = right_pad.ycor()
	y += 20
	right_pad.sety(y)


def paddlebdown():
	y = right_pad.ycor()
	y -= 20
	right_pad.sety(y)

# Keyboard bindings
sc.listen()
sc.onkey(paddleaup, "w")
sc.onkey(paddleadown, "s")
sc.onkey(paddlebup, "Up")
sc.onkey(paddlebdown, "Down")

################################## BOARD CONTROL ##################################

board = DE2i(fd)

board.set_display("right", d1 = displays["d1"], d2 = displays["d2"], d3 = displays["d3"], d4 = displays["d4"])

while True:
	sc.update()
	pbuttons=board.get_pbuttons()
	if pbuttons[0] == True:  #DESCE A
		paddleadown()
	if pbuttons[1] == True:  #SOBE A
		paddleaup()
	if pbuttons[2] == True:  #DESCE B
		paddlebdown()
	if pbuttons[3] == True:  #SOBE B
		paddleaup()

	hit_ball.setx(hit_ball.xcor()+hit_ball.dx)
	hit_ball.sety(hit_ball.ycor()+hit_ball.dy)
	
	if switch_1 and left_paddle_shape == "square":
		left_paddle_shape = "circle"
		left_pad.shape("circle")
	elif not switch_1 and left_paddle_shape == "circle":
		left_paddle_shape = "square"
		left_pad.shape("square")

	if switch_2 and right_paddle_shape == "square":
		right_paddle_shape = "circle"
		right_pad.shape("circle")
	elif not switch_2 and right_paddle_shape == "circle":
		right_paddle_shape = "square"
		right_pad.shape("square")
	
	# Checking borders
	if hit_ball.ycor() > 280:
		hit_ball.sety(280)
		hit_ball.dy *= -1

	if hit_ball.ycor() < -280:
		hit_ball.sety(-280)
		hit_ball.dy *= -1

	if hit_ball.xcor() > 500:
		hit_ball.goto(0, 0)
		hit_ball.dy *= -1
		left_player += 1
		sketch.clear()
		sketch.write("Left_player : {} Right_player: {}".format(
					left_player, right_player), align="center",
					font=("Courier", 24, "normal"))

	if hit_ball.xcor() < -500:
		hit_ball.goto(0, 0)
		hit_ball.dy *= -1
		right_player += 1
		sketch.clear()
		sketch.write("Left_player : {} Right_player: {}".format(
								left_player, right_player), align="center",
								font=("Courier", 24, "normal"))

	# Paddle ball collision
	if (hit_ball.xcor() > 360 and
						hit_ball.xcor() < 370) and (hit_ball.ycor() < right_pad.ycor()+80 and hit_ball.ycor() > right_pad.ycor()-80):
		hit_ball.setx(360)
		hit_ball.dx*=-1
		
	if (hit_ball.xcor()<-360 and hit_ball.xcor()>-370) and (hit_ball.ycor()<left_pad.ycor()+80 and hit_ball.ycor()>left_pad.ycor()-80):
		hit_ball.setx(-360)
		hit_ball.dx*=-1

os.close(fd)
