import time

from sr.robot import *

R = Robot()

SERVO_ARM = 0
SERVO_LEFT = 2
SERVO_RIGHT = 1

GPIO_GATE = 1
GPIO_PUMP = 2

HELLO = True

MULTIPLIER_LEFT = -1
MULTIPLIER_RIGHT = 0.81

SPEED_50 = 1.25 / 3
SPEED_100 = 1.7 * SPEED_50 * 1.25
SPEED_ANGULAR_30 = 360 / 4.25

R.gpio.pin_mode(GPIO_GATE, OUTPUT)
R.gpio.digital_write(GPIO_GATE, True)
R.servos[SERVO_RIGHT] = 0
R.servos[SERVO_LEFT] = 0


def move(distance):
    R.servos[SERVO_LEFT] = MULTIPLIER_LEFT * 100
    R.servos[SERVO_RIGHT] = MULTIPLIER_RIGHT * 100

    time.sleep(distance / SPEED_100)

    R.servos[SERVO_RIGHT] = 0
    R.servos[SERVO_LEFT] = 0


def turn(angle):
    R.servos[SERVO_LEFT] = MULTIPLIER_LEFT * 30
    R.servos[SERVO_RIGHT] = MULTIPLIER_RIGHT * -30

    time.sleep(angle / SPEED_ANGULAR_30)

    R.servos[SERVO_RIGHT] = 0
    R.servos[SERVO_LEFT] = 0
