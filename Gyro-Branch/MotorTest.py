# s u c c 
# t h e 
# b  o  i

# encoding: utf-8
from __future__ import print_function  # Import the future
import time
from sr.robot import *

R = Robot()

print('Setting motor power')
R.motors[0].m0.power = 20       #Set power of motors
R.motors[0].m1.power = -20	
R.motors[0].led.colour = (120,239,4)
time.sleep(30)
print('Killing motors')
R.motors[0].m0.power = 0        #Set power of motors
R.motors[0].m1.power = 0
R.motors[0].led.colour = (255,255,255)
