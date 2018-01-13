import time
from sr.robot import *

robot = Robot()



robot.motors[0].m0.power = 50
robot.motors[0].m1.power = -50
time.sleep(1)
robot.motors[0].m0.power = 20
robot.motors[0].m1.power = -20