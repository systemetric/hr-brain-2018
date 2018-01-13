from sr.robot import *
import time

R = Robot()

R.servos[1] = 100
R.servos[2] = 100
sleep(10)
R.servos[1] = 0
R.servos[2] = 0