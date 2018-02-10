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

for r in RESOLUTIONS:
    R.see(res=r, save=True)
    time.sleep(1)



