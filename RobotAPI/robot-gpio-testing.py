import time

from sr.robot import *

R = Robot()

R.gpio.pin_mode(1, INPUT_ANALOG)

while True:
    pot_value_1 = R.gpio.analog_read(1)

    print "1:", pot_value_1

    # R.gpio.digital_write(LED_PIN, pot_value > 100)

    time.sleep(0.1)
