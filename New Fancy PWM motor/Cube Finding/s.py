import time

from sr.robot import *

R = Robot()

SERVO_ARM = 0
SERVO_LEFT = 2
SERVO_RIGHT = 1

GPIO_GATE = 1
GPIO_PUMP = 2

MULTIPLIER_LEFT = -1
MULTIPLIER_RIGHT = 0.81

# 100%
# 3s 2.5m +
# 2s

# 50%
# 3s 1.25m
# (1.25 / 3) m/s

SPEED_50 = 1.25 / 3
SPEED_100 = 1.7 * SPEED_50 * 1.25


R.gpio.pin_mode(GPIO_GATE, OUTPUT)
R.gpio.digital_write(GPIO_GATE, True)
R.servos[SERVO_RIGHT] = 0
R.servos[SERVO_LEFT] = 0
time.sleep(0.5)

R.servos[SERVO_LEFT] = MULTIPLIER_LEFT * 33
R.servos[SERVO_RIGHT] = MULTIPLIER_RIGHT * -33

# metres / SPEED_100

time.sleep(1)

R.servos[SERVO_LEFT] = 0
R.servos[SERVO_RIGHT] = 0

time.sleep(0.5)
R.gpio.digital_write(GPIO_GATE, False)

# R.gpio.pin_mode(GPIO_PUMP, OUTPUT)
#
# while True:
#     R.servos[SERVO_ARM] = -100
#     time.sleep(1)
#     R.gpio.digital_write(GPIO_PUMP, True)
#     time.sleep(1)
#     R.servos[SERVO_ARM] = 100
#     time.sleep(5)
#     R.gpio.digital_write(GPIO_PUMP, False)
#     time.sleep(5)
