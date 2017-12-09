python
from sr.robot import *
import time

last_speed = 0


def goto_power(robot, target):
    global last_speed

    # current_power = int(robot.motors[0].m0.power)
    current_power = last_speed

    difference = target - current_power
    step = int(difference / abs(difference))

    for i in range(current_power, target, step):
        robot.motors[0].m0.power = 0.905 * i # 0.88
        robot.motors[0].m1.power = -i

        last_speed = i

        time.sleep(0.020)  #0.020


R = Robot()
R.motors[0].led.colour = (255, 0, 0)
goto_power(R, 35)
R.motors[0].led.colour = (0, 255, 0)
time.sleep(10)
R.motors[0].led.colour = (255, 0, 0)
goto_power(R, 0)
R.motors[0].led.colour = (255, 255, 255)
