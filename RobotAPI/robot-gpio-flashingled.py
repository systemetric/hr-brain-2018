import time

from sr.robot import *

R = Robot()

LED_PIN = 4

R.gpio.pin_mode(LED_PIN, OUTPUT)

v = True
while True:
    R.gpio.digital_write(LED_PIN, v)

    v = not v

    time.sleep(1)
