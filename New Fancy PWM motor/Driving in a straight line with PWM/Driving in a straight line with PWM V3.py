from sr.robot import *
import time


R = Robot()

def pause():
    R.servos[1] = 0
    R.servos[2] = 0
    R.time.sleep(3)

pause()

while True:
    R.servos[1] = 100
    R.servos[2] = 100
    time.sleep(3)

    pause()

    R.servos[1] = -100
    R.servos[2] = -100
    time.sleep(3)

    pause()

    R.servos[1] = 100
    R.servos[2] = -100
    time.sleep(3)

    pause()

    R.servos[1] = -100
    R.servos[2] = 100
    time.sleep(3)

    pause()