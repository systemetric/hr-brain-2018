import math
import time

from sr.robot import *

R = Robot()

MAX_VALUE = 73  # Maximum Power such that OCP is not tripped

try:
    i = 0
    while True:
        v = math.sin(math.radians(i))
        # v = 1

        R.motors[0].m0.power = v * MAX_VALUE
        R.motors[0].m1.power = -v * MAX_VALUE

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

        # if i < 90:
        i += 0.05
except KeyboardInterrupt:
    print "\n"
    R.off()
