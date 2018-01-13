from sr.robot import *
import time

R = Robot()

R.servos[1] = 0

R.gpio.pin_mode(1,OUTPUT)

R.gpio.digital_write(1, True)


time.sleep(1)
print "waited complete"

while True:
	for i in range(0, 180):
		j = int(math.sin(math.radians(i*2))*100) # multiply sin result -1 to 1 up to
        R.servos[1] = -j                         # -100 to 100, then round towards 0
        R.servos[2] = j	
        time.sleep(0.02)
    # R.servos[1] = 0
    # R.servos[2] = 0
    # time.sleep(2)
    # R.servos[1] = 100
    # R.servos[2] = -100
    # time.sleep(2)
    # R.servos[1] = 0
    # R.servos[2] = 0
    # time.sleep(2)