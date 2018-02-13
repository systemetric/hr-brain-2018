import time

from sr.robot import *

R = Robot()

SERVO_ARM = 0
SERVO_LEFT = 2
SERVO_RIGHT = 1

GPIO_GATE = 1
GPIO_PUMP = 2

MULTIPLIER_LEFT = -1
MULTIPLIER_RIGHT = 0.95  # 0.91

SPEED_50 = 1.25 / 3
SPEED_100 = 1.7 * SPEED_50 * 1.25
SPEED_ANGULAR_30 = 360 / 4.25

markers = []

R.gpio.pin_mode(GPIO_GATE, OUTPUT)
R.gpio.pin_mode(GPIO_PUMP, OUTPUT)
R.gpio.digital_write(GPIO_GATE, True)
R.servos[SERVO_RIGHT] = 0
R.servos[SERVO_LEFT] = 0


def move(distance):
    R.servos[SERVO_LEFT] = MULTIPLIER_LEFT * 50
    R.servos[SERVO_RIGHT] = MULTIPLIER_RIGHT * 50

    time.sleep(distance / SPEED_50)

    R.servos[SERVO_RIGHT] = 0
    R.servos[SERVO_LEFT] = 0


def turn(angle):
    multiplier = 1
    if angle < 0:
        multiplier = -1
    R.servos[SERVO_LEFT] = MULTIPLIER_LEFT * -30 * multiplier
    R.servos[SERVO_RIGHT] = MULTIPLIER_RIGHT * 30 * multiplier

    time.sleep(abs(angle) / SPEED_ANGULAR_30)

    R.servos[SERVO_RIGHT] = 0
    R.servos[SERVO_LEFT] = 0


def succ():
    R.servos[SERVO_ARM] = -100
    time.sleep(1)
    R.gpio.digital_write(GPIO_PUMP, True)
    time.sleep(1)
    R.servos[SERVO_ARM] = 100
    time.sleep(0.5)


def pump_on():
    R.gpio.digital_write(GPIO_PUMP, True)


def drop():
    R.gpio.digital_write(GPIO_PUMP, False)


def find_cube():
    global markers
    at_cube = False
    while not at_cube:
        markers = R.see(res=(640, 480), save=True)
        for marker in markers:
            if marker.info.marker_type == MARKER_TOKEN:
                print('Cube ' + str(marker.info.code) + 'located')
        if len(markers) == 0:
            print('No cube found, rotating...')
            turn(30)
            time.sleep(0.3)
        else:
            print('Heading to cube ' + str(markers[0].info.code) + ' at angle ' + str(markers[0].rot_y))
            turn(markers[0].rot_y)
            move(markers[0].dist)
            at_cube = True


def find_bucket():
    global markers
    at_cube = False
    while not at_cube:
        markers = R.see(res=(640, 480), save=True)
        for marker in markers:
            if marker.info.marker_type == MARKER_BUCKET_SIDE:
                print('Cube ' + str(marker.info.code) + 'located')
        if len(markers) == 0:
            print('No cube found, rotating...')
            turn(30)
            time.sleep(0.3)
        else:
            print('Heading to cube ' + str(markers[0].info.code) + ' at angle ' + str(markers[0].rot_y))
            turn(markers[0].rot_y)
            move(markers[0].dist)
            at_cube = True