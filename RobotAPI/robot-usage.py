from sr.robot import *

R = Robot()

# R.motors[0].m0.power = 0
# R.motors[0].m1.power = 100
#
# R.motors[0].led = (255, 255, 255)
#
# R.servos[0] = 100
# R.servos[1] = -100

R.gpio.pin_mode(1, INPUT)
R.gpio.digital_read(1)

R.gpio.pin_mode(2, OUTPUT)
R.gpio.digital_write(2, True)

R.gpio.pin_mode(3, INPUT_ANALOG)
R.gpio.analogue_read(3)
