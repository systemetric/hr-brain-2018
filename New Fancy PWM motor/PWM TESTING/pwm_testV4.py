from sr.robot import *
import time

R = Robot()


while True:
    R.servos[1] = -100
    time.sleep(5)
    R.servos[1] = 100
    time.sleep(5)