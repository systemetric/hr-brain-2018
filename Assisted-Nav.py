
# encoding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
import time
from sr.robot import *

#VARIBLES
last_speed = 0
m0_const = 0.905 #Previous value 0.88
m1_const = 1
gyro_const = 0.1
gyro_pin = 1

gyro_pin = 1
robot_mode_switch = 1    # When set to 0 , uses manual mode, when set to 1, uses vision



def motor_reset():                                          #allows the programer to rest the varibles
    global m0_const, m1_const
    m0_const = 0.905 #Previous value 0.88
    m1_const = 1

def goto_power(robot, target):
    global last_speed, m0_const, m1_const, gyro_pin, gyro_const, gyro_zero #Uses these globals


    step = (1 if difference > 0 else -1)                    #Set the polarity of the step
    difference = target - last_speed                        #Gets the difference
    
    for i in range(last_speed, target, step):

        gyro_pos = robot.gpio.analog_read(gyro_pin)         #Get current gyro position



        m0_const += ((gyro_zero - gyro_pos) * gyro_const)   #Adjust the calculated motor power according to the gyro
        m1_const -= ((gyro_zero - gyro_pos) * gyro_const)

        clamp(m0_const, -70, 70)                            #Prevent the value of calculated motor power exceding 70%.
        clamp(m1_const, -70, 70)

        R.motors[0].m0.power = m0_const * i             #Set power of motors
        R.motors[0].m1.power = m1_const * i

        last_speed = i                                      #set the last speed to the current speed

        time.sleep(0.020)                                   #Slow the rate of acceleration


def stay_at_power(robot, ticks):
    global m0_const, m1_const, gyro_pin, gyro_const, gyro_zero#Uses these globals

    start_time = time.time()                                #Get UNIX-time

    while (time.time() - start_time) < ticks:               #Has more time passed than specified run time?

        gyro_pos = robot.gpio.analog_read(gyro_pin)       #Get current gyro position


        m0_const += ((gyro_zero - gyro_pos) * gyro_const)   #Adjust the calculated motor power according to the gyro
        m1_const -= ((gyro_zero - gyro_pos) * gyro_const)

        clamp(m0_const, -70, 70)                            #Prevent the value of calculated motor power exceding 70%.
        clamp(m1_const, -70, 70)

        R.motors[0].m0.power = m0_const                 #Set the motors to the calculated power.
        R.motors[0].m1.power = m1_const

        print("Gyro pos: ", gyro_pos, "  m0_const: ", m0_const, "  m1_const: ", m1_const) #DEBUGGING
        time.sleep(0.05)



def turn_robot(robot,degrees):# Turn robot clockwise X degrees
    pass#ing this onot someone to do :)

#-----------------------------------------------
def goto_marker(robot):
    # Use vision to nagviage to marker
    # Calculates real time distance to marker and changes speed based on distance
    # If distance is more than 60cm , travels at a fast speed
    # If distance is less than 60cm but more 30cm, continue at a slower rate
    # If distance is less than 30 but more than 15, slow down considerably
    # If marker is less than 15cm away, stop

    while True:

        markers = R.see() # List of markers the robot can see per image

        if len(markers)>0:#If the robot has seen a marker
            current_marker_distance = (markers[0].dist*100) #Get distance in centimetres

            if current_marker_distance > 60: # If marker is more than 60cm away

                goto_power(R,55) #Robot travels at fast speed
                stay_at_power(R,1) #Stay at the power for 1 secs
                R.motors[0].led.colour = (0, 255, 0)# Green to indicate speed

            elif current_marker_distance <= 60 and current_marker_distance >= 30: #If marker is less than 60cm but more than 30cm

                goto_power(R,39)#Robot travels at a slower speed
                stay_at_power(R,1)#Stay at power for 1 secs
                R.motors[0].led.colour = (219, 199, 65)# Yellow to indicate slowing down


            elif current_marker_distance < 30 and current_marker_distance > 15:

                goto_power(R,30)# If marker is less than 30 and more than 15,travel EVEN slower
                stay_at_power(R,1)#Stay at power for 1second.
                R.motors[0].led.colour = (255, 6, 230)# Pink to indicate slow slow speed

            elif current_marker_distance <= 15:# If marker is less than 15cm away

                goto_power(R,0)# Stop
                stay_at_power(R,0)
                R.motors[0].led.colour = (255, 0, 0)# Red to indicate stopping
#----------------------------------------------


R = Robot()

gyro_zero = R.gpio.analog_read(gyro_pin)          #Get the zero motion voltage of the gyro
print("Gyro_zeroed at: ", gyro_zero)

robot_mode_switch = 1    # When set to 0 , uses manual mode, when set to 1, uses vision

if robot_mode_switch == 0:# Manual mode

    R.motors[0].led.colour = (189, 0, 255) # Purple to indicate manual mode
    time.sleep(1)

    R.motors[0].led.colour = (255, 0, 0)
    goto_power(R, 70)                       #Accelerate

    R.motors[0].led.colour = (0, 255, 0)
    stay_at_power(R, 3)                     #Moving constant speed waiting for 3 secs

    R.motors[0].led.colour = (255, 0, 0)
    goto_power(R, 0)                        #Decelerate

    R.motors[0].led.colour = (255, 255, 255)

if robot_mode_switch == 1:# Automated mode
    R.motors[0].led.colour = (5, 226, 247) # Turquoise to indicate Automated
    time.sleep(1)
    goto_marker(R)
