from sr.robot import *
import time

R = Robot()

# for i in range(0, 100, 2):
# 	R.servos[1] = -i
# 	R.servos[2] = i
# 	time.sleep(0.05)

# time.sleep(5)
# R.servos[1] = 0
# R.servos[2] = 0

R.servos[1] = 100
time.sleep(15)
R.servos[2] = -100
time.sleep(15)
R.servos[1] = 0
R.servos[2] = 0