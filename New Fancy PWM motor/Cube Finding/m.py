from sr.robot import *

R = Robot()

for i in range(1, 5, 1):
    print i
    R.gpio.pin_mode(i, OUTPUT)
    R.gpio.digital_write(i, True)

for i in range(0, 4, 1):
    print i
    R.servos[i] = 100
