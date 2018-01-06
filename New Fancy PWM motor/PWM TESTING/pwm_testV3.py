from sr.robot import *
import time

R = Robot()


while True:
    R.servos[0][1] = -100
    time.sleep(5)
    R.servos[0][1] = 100
    time.sleep(5)