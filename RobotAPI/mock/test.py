import time

from sr.robot import *

R = Robot()

R.gpio.pin_mode(1, OUTPUT)
R.gpio.pin_mode(2, OUTPUT)

R.gpio.digital_write(1, True)
R.gpio.digital_write(2, True)

R.servos[1] = 100
R.servos[2] = 100

time.sleep(5)

R.servos[1] = 0
R.servos[2] = 0

R.gpio.digital_write(1, False)
R.gpio.digital_write(2, False)
