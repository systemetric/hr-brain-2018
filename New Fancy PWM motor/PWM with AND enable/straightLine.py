from sr.robot import *
import time

R = Robot()

R.servos[1] = 0

R.gpio.pin_mode(1,OUTPUT)
R.gpio.digital_write(1, True)

print "go!!!!1!!!"

R.servos[1] = 50
R.servos[2] = -50
print('Powered up...')
time.sleep(4 )
print('Stopping...')
R.servos[1] = 0
R.servos[2] = 0
time.sleep(2)