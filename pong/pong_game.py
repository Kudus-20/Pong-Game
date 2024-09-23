# Author: Abdul-Kudus Alhassan
# Date: 01/27/2023
# Description: Developing the pong game

from cs1lib import *

from random import uniform, randint

# -----------------
# MODEL
# ----------------
# these constants define the window width and Height
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# these also define the size of the paddles
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 80
PADDLE_SPEED = 7  # this is the amount a paddle moves in a given direction each time any of the control key is pressed

# these contant variables store the keys that control the paddles, the game window and restarting of the game
LEFT_PADDLE_UP = "a"  # a to move left paddle up
LEFT_PADDLE_DOWN = "z"  # z to move left paddle down
RIGHT_PADDLE_UP = "k"  # k to move right paddle up
RIGHT_PADDLE_DOWN = "m"  # m to move right paddle down
START_KEY = " "  # space bar to start a new Game
QUIT = "q"  # q to quit the game and close the window

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

# These variables define the ball location and size
x = 200  # x coordinate of the ball
y = 200  # y coordinate of the ball
radius = 9  # radius of the ball

# these boolean values keep track of all collisions
vertical_collision = False
left_paddle_collision = False
right_paddle_collision = False
bottom_collision = False
top_collision = False

# These two variables initializes the x and y components of the ball
x_velocity = 3
y_velocity = 3


# -----------------
# CONTROLLERS
# ----------------


# keeping track of pressed keys
def key_control(key):
    global LEFT_PADDLE_UP, LEFT_PADDLE_DOWN, RIGHT_PADDLE_DOWN, RIGHT_PADDLE_UP, a_pressed, z_pressed, k_pressed, m_pressed, start

    if key == START_KEY:
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


# This function draws the ball
def draw_ball():
    global radius
    set_fill_color(1, 1, 1)  # ball colour depends on the values of the global variables, r, g, and b
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


# this function tracks all booleans and updates them upon collision
def collition_detect():
    global vertical_collision, left_paddle_collision, right_paddle_collision, bottom_collision, top_collision
    vertical_collision = vertical_wall_contact()
    left_paddle_collision = left_paddle_contact()
    right_paddle_collision = right_paddle_contact()
    bottom_collision = bottom_horizontal_wall()
    top_collision = top_horizontal_wall()


# this function checks for all collisions with walls and paddles
def collision():
    global vertical_collision, left_paddle_collision, right_paddle_collision, bottom_collision, top_collision, x_velocity, y_velocity, start

    collition_detect()

    # This handles the updates when the ball hits the right paddle
    if right_paddle_collision:
        if x_velocity > 0:
            x_velocity = - x_velocity  # it changes the direction of movement the ball

    if left_paddle_collision:
        x_velocity = abs(x_velocity)  # it changes the direction of movement the ball

    #  this checks if the ball has collided with the top or bottom walls of the window and changes the direction accordingly
    if top_collision or bottom_collision:
        y_velocity = -y_velocity

    # this checks if the ball has missed the paddles and made contact with the vertical walls
    if vertical_collision:
        start = False  # this resets the game to the starting interface


# this initializes the interface and controls the updating position of the ball
def game_play():
    global start, x, y, left_paddle_y, left_paddle_x, right_paddle_y, right_paddle_x

    if start:  # this updates the position of the ball
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

    set_clear_color(0, 0, 0)  # sets the background of the game board to back
    clear()

    disable_stroke()  # this removes the stroke

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


start_graphics(draw_game_board, 2400, key_press=key_control, key_release=key_control_release)
