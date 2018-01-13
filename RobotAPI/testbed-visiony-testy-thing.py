from sr.robot import *
import time

R = Robot()

v = 0
while True:
    markers = R.see()
    print "I can see", len(markers), "markers:"
    for m in markers:
        print " - Marker #{0} is {1} metres away".format(m.info.code, m.dist)
    g_multiplier = 0
    if len(markers) > 0:
        g_multiplier = 1
    r_multiplier = 1 - g_multiplier
    # R.motors[0].led.colour = (r_multiplier * 255, g_multiplier * 255, 0)
    R.motors[0].led.colour = (v * 255, (1-v) * 255, 0)
    if v == 0:
        v = 1
    else:
        v = 0
	time.sleep(1)


	
for i in range(100):
	markers = R.see()
	