# Author: Abdul-Kudus Alhassan
# Date: 01/27/2023
# Description: Developing the pong game

from cs1lib import *

from random import uniform, randint

# -----------------
# MODEL
# ----------------
#these constants define the window width and Height
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

#these also define the size of the paddles
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 80
PADDLE_SPEED = 7 # this is the amount a paddle moves in a given direction each time any of the control key is pressed

# these contant variables store the keys that control the paddles, the game window and restarting of the game
LEFT_PADDLE_UP = "a"    # a to move left paddle up
LEFT_PADDLE_DOWN = "z"  # z to move left paddle down
RIGHT_PADDLE_UP = "k"   #k to move right paddle up
RIGHT_PADDLE_DOWN = "m" # m to move right paddle down
START_KEY = " "     #space bar to start a new Game
QUIT = "q"          #q to quit the game and close the window

# this sets the initial positions of the paddles
left_paddle_x = 0
left_paddle_y = 0
right_paddle_x = WINDOW_WIDTH - PADDLE_WIDTH
right_paddle_y = WINDOW_HEIGHT - PADDLE_HEIGHT

#  check if a control key has been pressed
a_pressed = False  # checks if a has been pressed
z_pressed = False  # checks if z has been pressed
k_pressed = False  # checks if k has been pressed
m_pressed = False  # checks if m has been pressed

# keep track of game start and stays true  if game is in progress and keeps updating the position of the ball
start = True
# this checks if the ball has gone out of the game window so it end the current play session
game_over = False

# These variables define the ball location and size
x = 200  # x coordinate of the ball
y = 200  # y coordinate of the ball
radius = 9  # radius of the ball

# this represents the r, g, b values of the ball's colour and it is initialized to white
r = 1
g = 1
b = 1

# this is the factor by which the x and y velocities increase whenever it hits a paddle in order to accelerate the ball
acceleration_factor = 0.5

# these boolean values keep track of all collisions
vertical_collision = False
left_paddle_collision = False
right_paddle_collision = False
bottom_collision = False
top_collision = False

# -----------------
# CONTROLLERS
# ----------------


# keeping track of pressed keys
def key_control(key):
    global LEFT_PADDLE_UP, LEFT_PADDLE_DOWN, RIGHT_PADDLE_DOWN, RIGHT_PADDLE_UP, a_pressed, z_pressed, k_pressed, m_pressed, start, game_over

    if key == START_KEY:
        game_over = False  # this is to show that the game is in progress
        start = not start  # this ensures that when the space bar is pressed, it starts a new game or ends the game if it was already in progress

    if key == LEFT_PADDLE_UP:  # this checks and registers if a has been pressed
        a_pressed = True

    if key == LEFT_PADDLE_DOWN:  # this checks and registers if z has been pressed
        z_pressed = True

    if key == RIGHT_PADDLE_UP:  # this checks and registers if k has been pressed
        k_pressed = True

    if key == RIGHT_PADDLE_DOWN:  # this checks and registers if m has been pressed
        m_pressed = True
    if key == QUIT:  # this checks and quits the game if q is pressed
        cs1_quit()


# keeping track of released keys
def key_control_release(key):
    global LEFT_PADDLE_UP, LEFT_PADDLE_DOWN, RIGHT_PADDLE_DOWN, RIGHT_PADDLE_UP, a_pressed, z_pressed, k_pressed, m_pressed

    if key == LEFT_PADDLE_UP:  # this checks and registers if a has been released
        a_pressed = False

    if key == LEFT_PADDLE_DOWN:  # this checks and registers if z has been released
        z_pressed = False

    if key == RIGHT_PADDLE_UP:  # this checks and registers if k has been released
        k_pressed = False

    if key == RIGHT_PADDLE_DOWN:  # this checks and registers if m has been released
        m_pressed = False


# -----------------
# VIEW
# ----------------
# This function randomly returns either -3 or 3 which is later used as the initial x component velocity of to make the initial ball direction random
def initial_x_direction():
    x_direction = randint(1, 2)

    if x_direction == 1:
        return -3
    else:
        return 3


# This function randomly returns either -3 or 3 which is later used as the initial y component velocity of to make the initial ball direction random
def initial_y_direction():
    y_direction = randint(1, 2)

    if y_direction == 1:
        return -3
    else:
        return 3


# These two variables initializes the x and y components of the ball
# and takes either positive or negative from the function calls
x_velocity = initial_x_direction()
y_velocity = initial_y_direction()


# this function checks and returns a boolean value depending on whether the ball has made contact with the left paddle
def left_paddle_contact():
    global x, y, radius, left_paddle_x, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT
    if (x + radius <= left_paddle_x + (PADDLE_WIDTH * 2)) and (left_paddle_y <= y <= left_paddle_y + PADDLE_HEIGHT):
        return True
    else:
        return False


# this function checks and returns a boolean value depending on whether the ball has made contact with the right paddle
def right_paddle_contact():
    global x, y, radius, right_paddle_x, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT
    if (x + radius >= right_paddle_x) and (right_paddle_y <= y <= right_paddle_y + PADDLE_HEIGHT):
        return True
    else:
        return False


# this function checks and returns a boolean value depending on whether the ball has made contact with the bottom wall of the game window
def bottom_horizontal_wall():
    global y, WINDOW_HEIGHT, bottom_collision, radius
    if y + radius >= WINDOW_HEIGHT:
        return True
    else:
        return False


# this function checks and returns a boolean value depending on whether the ball has made contact with the top wall of the game window
def top_horizontal_wall():
    global y, radius
    if (y + radius) <= PADDLE_WIDTH:
        return True
    else:
        return False


# this function checks and returns a boolean value depending on whether the ball has missed a paddle and made contact with the vertical side of the window
def vertical_wall_contact():
    global x, WINDOW_WIDTH, left_paddle_x
    if x > WINDOW_WIDTH or x < left_paddle_x:
        return True
    else:
        return False


# this function draws a paddle, and it takes two parameters to specify the location to drw the paddle
def paddle(x, y):
    global PADDLE_HEIGHT, PADDLE_WIDTH
    set_fill_color(1, 1, 1)  # sets the paddle colour to white
    draw_rectangle(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)


# this function draws an interface that is displayed when the game is over
def game_over_interface():
    enable_stroke()
    set_stroke_color(1, 1, 1)  # sets the color of the text
    set_font_size(45)  # font size of the text
    draw_text("Game Over", 100, 130)  # thext to be drawn
    set_font("Bodoni 72 Smallcaps")  # font type to be used
    set_font_size(15)  # font size of sub text
    set_font("Source Code Pro")  # font type
    draw_text("Press spacebar to restart", 120, 155)  # text to be drawn
    set_font_size(1)  # font size


# This function draws the ball
def draw_ball():
    global r, g, b, x, y, radius
    set_fill_color(r, g, b)  # ball colour depends on the values of the global variables, r, g, and b
    draw_circle(x, y, radius)


# this function updates the position of the paddles based on the keys that have been pressed
def paddle_movement():
    global left_paddle_y, right_paddle_y
    # this condition checks if a has been pressed and updates the position of the left paddle by moving it up
    if a_pressed:
        if left_paddle_y > 0:
            left_paddle_y -= PADDLE_SPEED
    # this condition checks if z has been pressed and updates the position of the left paddle by moving it down
    if z_pressed:
        if left_paddle_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
            left_paddle_y += PADDLE_SPEED

    # this condition checks if k has been pressed and updates the position of the right paddle by moving it up
    if k_pressed:
        if right_paddle_y > 0:
            right_paddle_y -= PADDLE_SPEED

    # this condition checks if m has been pressed and updates the position of the left paddle by moving it up
    if m_pressed:
        if right_paddle_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
            right_paddle_y += PADDLE_SPEED

#this function tracks all booleans and updates them upon collision
def collition_detect():
    global vertical_collision, left_paddle_collision, right_paddle_collision, bottom_collision, top_collision
    vertical_collision = vertical_wall_contact()
    left_paddle_collision = left_paddle_contact()
    right_paddle_collision = right_paddle_contact()
    bottom_collision = bottom_horizontal_wall()
    top_collision = top_horizontal_wall()

# this function checks for all collisions with walls and paddles
def collision():
    global vertical_collision, left_paddle_collision, right_paddle_collision, bottom_collision, top_collision, x_velocity, y_velocity, r, g, b, start, game_over

    collition_detect()

    # This handles the updates when the ball hits the right paddle
    if right_paddle_collision:
        if x_velocity > 0:
            x_velocity = - x_velocity - acceleration_factor  # it changes the direction of movement the ball and also accelerates it in the x direction
        # this accelerates the ball in the y direction
        if y_velocity > 0:
            y_velocity += acceleration_factor
        else:
            y_velocity -= acceleration_factor
        # this ensures that whenever the ball collides with this paddle, random values are generated for r, g, and b which sets a random colour for the ball
        r = uniform(0, 1)
        g = uniform(0, 1)
        b = uniform(0, 1)

    if left_paddle_collision:
        x_velocity = abs(x_velocity) + acceleration_factor # it changes the direction of movement the ball and also accelerates it in the x direction

        # this ensures that whenever the ball collides with this paddle, random values are generated for r, g, and b which sets a random colour for the ball
        r = uniform(0, 1)
        g = uniform(0, 1)
        b = uniform(0, 1)

    #  this checks if the ball has collided with the top or bottom walls of the window and changes the direction accordingly
    if top_collision or bottom_collision:
        y_velocity = -y_velocity

    # this checks if the ball has missed the paddles and and made contact with the vertical walls
    if vertical_collision:
        start = False  # this resets the game to the starting interface
        game_over = True  # this displays the game over interface

# this checks for when the game is over and displays the interface
def dispay_game_over():
    global game_over
    if game_over:
        game_over_interface()

# this initializes the interface and controls the updating position of the ball
def game_play():
    global start, x, y, left_paddle_y, left_paddle_x, right_paddle_y, right_paddle_x

    if start:     # this updates the position of the ball
        x += x_velocity
        y += y_velocity
    else:
        # if space bar is pressed whiles game is in progress, reset all ball and paddles to default positions
        x = 200
        y = 200
        left_paddle_x = 0
        left_paddle_y = 0
        right_paddle_x = WINDOW_WIDTH - PADDLE_WIDTH
        right_paddle_y = WINDOW_HEIGHT - PADDLE_HEIGHT

def draw_game_board():
    global left_paddle_x, left_paddle_y, right_paddle_x, right_paddle_y

    set_clear_color(0, 0, 0) #sets the background of the gamboard to balck
    clear()

    disable_stroke() #this removes the stroke

    #  this draws the left paddle
    paddle(left_paddle_x, left_paddle_y)

    # this draws the right paddle
    paddle(right_paddle_x, right_paddle_y)

    # this controls the paddle movements
    paddle_movement()

    # this draws the ball
    draw_ball()

    # this ensures that the position of the ball is updated if game is in progress and reinitialized when game is over
    game_play()

    # this checks for all ball coalitions and makes necessary updates
    collision()

    # this displays the interface when the game is over
    dispay_game_over()





start_graphics(draw_game_board, 2400, key_press=key_control, key_release=key_control_release)
