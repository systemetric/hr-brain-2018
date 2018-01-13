import time

from sr.robot import *

R = Robot()

LED_PIN = 4

R.gpio.pin_mode(LED_PIN, OUTPUT)

# Printed Slot => Mapped Slot
# 1 => 3
# 2 => 1
# 3 => 2
# 4 => 4


def flash_led(times):
    for t in range(times):
        print "Flashing..."
        R.gpio.digital_write(LED_PIN, True)
        time.sleep(0.5)
        R.gpio.digital_write(LED_PIN, False)
        time.sleep(1)


# R.servos[0] = 50
# time.sleep(1)
# R.servos[0] = 0
# time.sleep(1)
# R.servos[0] = 100
# time.sleep(1)
# R.servos[0] = -50
# time.sleep(1)
# R.servos[0] = -100

for i in range(4):
    print "Testing servo", i
    flash_led(i + 1)
    R.servos[i] = -100
    time.sleep(1)
    R.servos[i] = 0
    time.sleep(1)
    R.servos[i] = 100
    time.sleep(1)

R.gpio.digital_write(LED_PIN, False)
