# encoding: utf-8
from __future__ import print_function  # Import the future
import time
from sr.robot import *

#VARIBLES
last_speed = 0
m0_const = 0 #0.905 #Previous value 0.88
m1_const = 0 #1
gyro_const = 0.02
gyro_pin = 1
gyro_samples = 16

def clamp(n, smallest, largest): 
    if n > largest:
        return largest
    elif n < smallest:
        return smallest
    else:
        return n

def goto_power(robot, target):
    global last_speed, m0_const, m1_const, gyro_pin, gyro_const, gyro_zero #Uses these globals

    difference = target - last_speed                        #Gets the difference
    step = (1 if difference > 0 else -1)                    #Set the polarity of the step
    
    for i in range(last_speed, target, step):

        gyro_pos = robot.gpio.analog_read(gyro_pin)         #Get current gyro position

        m0_const += ((gyro_zero - gyro_pos) * gyro_const)   #Adjust the calculated motor power according to the gyro
        m1_const -= ((gyro_zero - gyro_pos) * gyro_const)

        m0_const = clamp(m0_const, -70, 70)                            #Prevent the value of calculated motor power exceding 70%.
        m1_const = clamp(m1_const, -70, 70)

        robot.motors[0].m0.power = m0_const * i             #Set power of motors
        robot.motors[0].m1.power = -(m1_const * i)

        last_speed = i                                      #set the last speed to the current speed

        time.sleep(0.020)                                   #Slow the rate of acceleration


def stay_at_power(robot, ticks):
    global m0_const, m1_const, gyro_pin, gyro_const, gyro_zero  #Uses these globals

    start_time = time.time()                                #Get UNIX-time

    while (time.time() - start_time) < ticks:               #Has more time passed than specified run time?
        gyro_pos = robot.gpio.analog_read(gyro_pin)       #Get current gyro position

        m0_const -= ((gyro_zero - gyro_pos) * gyro_const)   #Adjust the calculated motor power according to the gyro
        m1_const += ((gyro_zero - gyro_pos) * gyro_const)

        m0_const = clamp(m0_const, -70, 70)                            #Prevent the value of calculated motor power exceding 70%.
        m1_const = clamp(m1_const, -70, 70)

        robot.motors[0].m0.power = m0_const                 #Set the motors to the calculated power.
        robot.motors[0].m1.power = -(m1_const)

        print("Gyro offset: ", gyro_pos - gyro_zero, "  m0_const: ", m0_const, "  m1_const: ", m1_const) #DEBUGGING
        time.sleep(0.06)

#-----------------------------------------------

R = Robot()
R.gpio.pin_mode(gyro_pin, INPUT_ANALOG)

R.motors[0].led.colour = (0, 0, 255)
reading = 0

for i in range(gyro_samples):                                 #Collect some samples about the gyro's zero position
    reading += R.gpio.analog_read(gyro_pin)
    time.sleep(0.06)                                #The ADC on the PIC is slow. We need to take alot of samples but we are only going to get duplicate values

gyro_zero = reading/gyro_samples
print("Gyro_zeroed at: ", gyro_zero)

R.motors[0].led.colour = (255, 0, 0)
goto_power(R, 35)                       #Accelerate

m0_const = 28.40
m1_const = 31.59  #Numbers taken from 50% power * 0.905 offset

R.motors[0].m0.power = m0_const            #Set power of motors
R.motors[0].m1.power = -m1_const

R.motors[0].led.colour = (0, 255, 0)
stay_at_power(R, 1)                     #Moving constant speed waiting for 10 secs

m0_const = 40 * 0.95
m1_const = 40 * 1.05  #Numbers taken from 50% power * 0.905 offset

R.motors[0].m0.power = m0_const            #Set power of motors
R.motors[0].m1.power = -m1_const

R.motors[0].led.colour = (0, 255, 0)
stay_at_power(R, 1)                     #Moving constant speed waiting for 10 secs

m0_const = 70 * 0.95
m1_const = 70 * 1.05 #Numbers taken from 50% power * 0.905 offset

R.motors[0].m0.power = m0_const            #Set power of motors
R.motors[0].m1.power = -m1_const

R.motors[0].led.colour = (0, 255, 0)
stay_at_power(R, 10)                     #Moving constant speed waiting for 10 secs

R.motors[0].m0.power = 0            #Set power of motors
R.motors[0].m1.power = 0

R.motors[0].led.colour = (255, 255, 255)

