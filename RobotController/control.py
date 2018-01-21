from pygui import *
import socket
import io
from urllib2 import urlopen
import random
import threading
import json
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

keys = {}

arrow_up = pygame.image.load("arrow.png")
arrow_right = pygame.transform.rotate(arrow_up, 270)
arrow_down = pygame.transform.rotate(arrow_up, 180)
arrow_left = pygame.transform.rotate(arrow_up, 90)
arrow_selected_up = pygame.image.load("arrow_selected.png")
arrow_selected_right = pygame.transform.rotate(arrow_selected_up, 270)
arrow_selected_down = pygame.transform.rotate(arrow_selected_up, 180)
arrow_selected_left = pygame.transform.rotate(arrow_selected_up, 90)

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


def get_key_down(key):
    try:
        return keys[key]
    except KeyError:
        return False


def send_keys():
    global keys

    s.send(json.dumps({
        "up": get_key_down(pygame.K_UP),
        "down": get_key_down(pygame.K_DOWN),
        "left": get_key_down(pygame.K_LEFT),
        "right": get_key_down(pygame.K_RIGHT),
    }))


def update(event):
    global keys

    if event.type == pygame.KEYDOWN:
        keys[event.key] = True
        send_keys()
    elif event.type == pygame.KEYUP:
        keys[event.key] = False
        send_keys()


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

    up = arrow_up
    if get_key_down(pygame.K_UP):
        up = arrow_selected_up
    down = arrow_down
    if get_key_down(pygame.K_DOWN):
        down = arrow_selected_down
    left = arrow_left
    if get_key_down(pygame.K_LEFT):
        left = arrow_selected_left
    right = arrow_right
    if get_key_down(pygame.K_RIGHT):
        right = arrow_selected_right

    display.blit(up, (win.w / 2 - 32, 300))
    display.blit(down, (win.w / 2 - 32, 384))
    display.blit(left, (win.w / 2 - 32 - 84, 384))
    display.blit(right, (win.w / 2 + 32 + 20, 384))


game = PyGame(update, render)

win.add(game)

win.main_loop()
