"""
Mostly taken from http://yameb.blogspot.co.uk/2013/01/gamepad-input-in-python.html
"""

import pygame

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
print 'Initialized Joystick : %s' % j.get_name()

# Input mapping for the cheap Xbox 360 knockoff controller used for testing
# Each const corresponds to the relevant index in the array returned by get()
LTHUMBSTICK_X = 0
LTHUMBSTICK_Y = 1
LTRIGGER = 2
RTHUMBSTICK_X = 3
RTHUMBSTICK_Y = 4
RTRIGGER = 5
BUTTON_A = 6
BUTTON_B = 7
BUTTON_X = 8
BUTTON_Y = 9
LBUMPER = 10
RBUMPER = 11
BUTTON_SELECT = 12
BUTTON_START = 13
BUTTON_HOME = 14
LTHUMBSTICK_PRESS = 15
RTHUMBSTICK_PRESS = 16


def get():
    out = [0, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    it = 0  # iterator
    pygame.event.pump()

    # Read input from the two joysticks
    for i in range(0, j.get_numaxes()):
        out[it] = j.get_axis(i)
        it += 1
    # Read input from buttons
    for i in range(0, j.get_numbuttons()):
        out[it] = j.get_button(i)
        it += 1
    return out


def test():
    while True:
        print get()


def test_tank():
    while True:
        input_raw = get()
        print input_raw[LTHUMBSTICK_Y]
        print input_raw[RTHUMBSTICK_Y]