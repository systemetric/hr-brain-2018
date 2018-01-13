from sr.robot import *
import time
import math

R = Robot()

i = 0
while True:
    v = math.sin(math.radians(i))

    if math.floor(i) % 10 == 0:
        # print i
        redMultiplier = 1
        blueMultiplier = 1

        if v < 0:
            blueMultiplier = 0
        if v > 0:
            redMultiplier = 0

        colourValue = abs(v * 255.0)

        R.motors[0].led.colour = (colourValue * redMultiplier, 0, colourValue * blueMultiplier)

    time.sleep(0.001)
    i += 0.05
