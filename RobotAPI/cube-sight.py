from sr.robot import *
import time

R = Robot()

RESOLUTIONS = [
    (640, 480),
    (1296, 736),
    (1296, 976),
    (1920, 1088),
    (1920, 1440)
]

r_index = 0
while True:
    markers = R.see(res=RESOLUTIONS[0], save=True)
    if len(markers) > 0:
        i = 0
        for m in markers:
            print RESOLUTIONS[r_index], ":", i, ":", m.dist
            i += 1
    r_index += 1
    if r_index == len(RESOLUTIONS):
        r_index = 0
        print



