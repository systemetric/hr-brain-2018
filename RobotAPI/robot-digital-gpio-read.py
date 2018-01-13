from sr.robot import *
import time

R = Robot()

R.gpio.pin_mode(4, INPUT_PULLUP)

while True:
    print R.gpio.digital_read(4)
    time.sleep(0.25)
