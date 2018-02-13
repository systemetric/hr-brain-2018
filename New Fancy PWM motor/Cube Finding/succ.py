import time

from sr.robot import *

SERVO_ARM = 0
SERVO_LEFT = 2
SERVO_RIGHT = 1

GPIO_GATE = 1
GPIO_PUMP = 2

MULTIPLIER_LEFT = -1
MULTIPLIER_RIGHT = 0.81

R = Robot()

R.gpio.pin_mode(GPIO_PUMP, OUTPUT)

R.gpio.pin_mode(GPIO_GATE, OUTPUT)
R.gpio.digital_write(GPIO_GATE, True)
R.servos[SERVO_RIGHT] = 0
R.servos[SERVO_LEFT] = 0
time.sleep(0.5)

while True:
    R.servos[SERVO_ARM] = -100
    time.sleep(1)

    R.gpio.digital_write(GPIO_PUMP, True)

    time.sleep(1)
    R.servos[SERVO_ARM] = 100

    R.servos[SERVO_LEFT] = MULTIPLIER_LEFT * 100
    R.servos[SERVO_RIGHT] = MULTIPLIER_RIGHT * -100

    # metres / SPEED_100

    time.sleep(5)
    # time.sleep(1)

    R.gpio.digital_write(GPIO_PUMP, False)

    time.sleep(0.5)

    R.servos[SERVO_LEFT] = 0
    R.servos[SERVO_RIGHT] = 0

    time.sleep(5)

# R.gpio.digital_write(GPIO_GATE, False)

