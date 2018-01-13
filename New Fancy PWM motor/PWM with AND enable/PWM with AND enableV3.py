from sr.robot import *
import time

R = Robot()

R.servos[1] = 0

R.gpio.pin_mode(1,OUTPUT)

R.gpio.digital_write(1, True)


time.sleep(1)
print "waited complete"

while True:
    R.servos[1] = -100
    R.servos[2] = 100
    time.sleep(2)
    R.servos[1] = 0
    R.servos[2] = 0
    time.sleep(2)
    R.servos[1] = 100
    R.servos[2] = -100
    time.sleep(2)
    R.servos[1] = 0
    R.servos[2] = 0
    time.sleep(2)