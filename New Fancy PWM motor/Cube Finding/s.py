import time

from sr.robot import *

R = Robot()

SERVO_ARM = 0
SERVO_LEFT = 2
SERVO_RIGHT = 1

GPIO_GATE = 1
GPIO_PUMP = 2

MULTIPLIER_LEFT = -1
MULTIPLIER_RIGHT = 0.80

# 100%
# 3s 2.5m +
# 2s

# 50%
# 3s

R.gpio.pin_mode(GPIO_GATE, OUTPUT)
R.gpio.digital_write(GPIO_GATE, True)
R.servos[SERVO_RIGHT] = 0
R.servos[SERVO_LEFT] = 0
time.sleep(0.5)

R.servos[SERVO_LEFT] = MULTIPLIER_LEFT * 50
R.servos[SERVO_RIGHT] = MULTIPLIER_RIGHT * 50

time.sleep(3)

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
