from pygui import *
import socket
import io
from urllib2 import urlopen
import random
import threading
import json
import time
import gamepad

random.seed()

host = "127.0.0.1"  # robot.sr
port = 4096
s = socket.socket()

while True:
    try:
        s.connect((host, port))
        break
    except socket.error, msg:
        print "Socket Error: " + msg[1]
        host = raw_input("Enter IP of control server: ")

win = Window("Remote Control", 640, 480, 30, (255, 255, 255), False, True)

updating_image = False


def rand_colour():
    """Return random 6-bit hex code string.
    :rtype: str
    """
    colour = ''
    for i in range(0, 3):
        colour += ("%02X" % random.randint(0, 255))
    return colour


def update_image():
    """Get image from piCam (or placeholder) and update image global accordingly"""
    # TODO: Get feed as video stream instead of image sequence
    global updating_image
    global image

    image_str = urlopen("http://via.placeholder.com/640x480/" + rand_colour()).read()  # http://robot.sr/static/image.jpg
    image_file = io.BytesIO(image_str)
    image = pygame.image.load(image_file)

    updating_image = False


update_image()

ticks = 0


def update(event):
    send_gamepad_input()
    time.sleep(0.1)
    print event


def send_gamepad_input():
    input_vals = gamepad.get()
    # Using thumbsticks because the triggers on this gamepad have deadzones the size of Namibia
    s.send(json.dumps({
        "LThumbstick_Y": input_vals[gamepad.LTHUMBSTICK_Y],
        "RThumbstick_Y": input_vals[gamepad.RTHUMBSTICK_Y],
    }))


def render(display):
    global ticks
    global image
    global updating_image

    ticks += 1
    if ticks % 100 == 0 and not updating_image:
        updating_image = True
        thread = threading.Thread(target=update_image)
        thread.start()

    display.blit(image, (0, 0))


game = PyGame(update, render)

win.add(game)

win.main_loop()
