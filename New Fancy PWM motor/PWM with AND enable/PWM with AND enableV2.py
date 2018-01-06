from sr.robot import *
import time

R = Robot()


R.gpio.pin_mode(1,OUTPUT)

R.gpio.digital_write(1, True)

R.servos[1] = 0


while True:
    R.servos[1] = -100
    time.sleep(5)
    R.servos[1] = 0
    time.sleep(5)
    R.servos[1] = 100
    time.sleep(5)
    R.servos[1] = 0
    time.sleep(5)