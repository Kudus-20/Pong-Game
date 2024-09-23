# Author: Abdul-Kudus Alhassan
# Date: 01/27/2023
# Description: Developing the pong game


from cs1lib import *

# -----------------
# MODEL
# ----------------

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 80
PADDLE_SPEED = 7
# control keys
LEFT_PADDLE_UP = "a"
LEFT_PADDLE_DOWN = "z"
RIGHT_PADDLE_UP = "k"
RIGHT_PADDLE_DOWN = "m"

# paddle positions
left_paddle_x = 0
left_paddle_y = 0
right_paddle_x = WINDOW_WIDTH - PADDLE_WIDTH
right_paddle_y = WINDOW_HEIGHT - PADDLE_HEIGHT


#  check for controls
a_pressed = False
z_pressed = False
k_pressed = False
m_pressed = False

# -----------------
# CONTROLLERS
# ----------------


# keeping track of pressed keys
def key_control(key):
    global LEFT_PADDLE_UP, LEFT_PADDLE_DOWN, RIGHT_PADDLE_DOWN, RIGHT_PADDLE_UP, a_pressed, z_pressed,  k_pressed, m_pressed

    if key == LEFT_PADDLE_UP:
        a_pressed = True

    if key == LEFT_PADDLE_DOWN:
        z_pressed = True

    if key == RIGHT_PADDLE_UP:
        k_pressed = True

    if key == RIGHT_PADDLE_DOWN:
        m_pressed = True


# keeping track of released keys
def key_control_release(key):
    global a_pressed, z_pressed,  k_pressed, m_pressed

    if key == LEFT_PADDLE_UP:
        a_pressed = False

    elif key == LEFT_PADDLE_DOWN:
        z_pressed = False

    if key == RIGHT_PADDLE_UP:
        k_pressed = False

    elif key == RIGHT_PADDLE_DOWN:
        m_pressed = False


# -----------------
# VIEW
# ----------------
def paddle(x, y):
    global PADDLE_HEIGHT, PADDLE_WIDTH
    set_fill_color(1, 1, 1)
    draw_rectangle(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)


def draw_game_board():
    global left_paddle_x, left_paddle_y, right_paddle_x, right_paddle_y

    set_clear_color(0, 0, 0,)
    clear()

#     draw left paddle
    paddle(left_paddle_x, left_paddle_y)

#     draw right paddle
    paddle(right_paddle_x, right_paddle_y)

# control paddles: updating position of paddles based on key press

    if a_pressed:
        if left_paddle_y > 0:
            left_paddle_y -= PADDLE_SPEED
    if z_pressed:
        if left_paddle_y < WINDOW_HEIGHT-PADDLE_HEIGHT:
            left_paddle_y += PADDLE_SPEED

    if k_pressed:
        if right_paddle_y > 0:
            right_paddle_y -= PADDLE_SPEED
    if m_pressed:
        if right_paddle_y < WINDOW_HEIGHT-PADDLE_HEIGHT:
            right_paddle_y += PADDLE_SPEED


start_graphics(draw_game_board, key_press=key_control, key_release=key_control_release)