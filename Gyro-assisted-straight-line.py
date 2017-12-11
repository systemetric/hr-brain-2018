# encoding: utf-8
from __future__ import print_function                       #Import the future
from sr.robot import *
import time


#VARIBLES
last_speed = 0
m0_const = 0.905 #Previous value 0.88
m1_const = 1
gyro_pin = 1
gyro_const = 0.1

def motor_reset():                                          #allows the programer to rest the varibles
    global m0_const, m1_const
    m0_const = 0.905 #Previous value 0.88
    m1_const = 1 

def goto_power(robot, target):
    global last_speed, m0_const, m1_const, gyro_pin, gyro_const, gyro_zero #Uses these globals
    
    
    difference = target - last_speed                        #Gets the difference
    step = (1 if difference > 0 else -1)                    #Set the polarity of the step


    for i in range(last_speed, target, step):

        gyro_pos = robot.gpio.analogue_read(gyro_pin)       #Get current gyro position

        m0_const += ((gyro_zero - gyro_pos) * gyro_const)   #Adjust the calculated motor power according to the gyro
        m1_const -= ((gyro_zero - gyro_pos) * gyro_const)

        clamp(m0_const, -70, 70)                            #Prevent the value of calculated motor power exceding 70%.            
        clamp(m1_const, -70, 70)

        robot.motors[0].m0.power = m0_const * i             #Set power of motors
        robot.motors[0].m1.power = m1_const * i
        
        last_speed = i                                      #set the last speed to the current speed

        time.sleep(0.020)                                   #Slow the rate of acceleration

        

def stay_at_power(robot, ticks):
    global m0_const, m1_const, gyro_pin, gyro_const, gyro_zero#Uses these globals

    start_time = time.time()                                #Get UNIX-time
    
    while (time.time() - start_time) < ticks:               #Has more time passed than specified run time?
        gyro_pos = robot.gpio.analogue_read(gyro_pin)       #Get current gyro position
        
        m0_const += ((gyro_zero - gyro_pos) * gyro_const)   #Adjust the calculated motor power according to the gyro
        m1_const -= ((gyro_zero - gyro_pos) * gyro_const)

        clamp(m0_const, -70, 70)                            #Prevent the value of calculated motor power exceding 70%.            
        clamp(m1_const, -70, 70)
        
        robot.motors[0].m0.power = m0_const                 #Set the motors to the calculated power.
        robot.motors[0].m1.power = m1_const
        
        print("Gyro pos: ", gyro_pos, "  m0_const: ", m0_const, "  m1_const: ", m1_const) #DEBUGGING
        time.sleep(0.05)
        

R = Robot()

gyro_zero = robot.gpio.analogue_read(gyro_pin)          #Get the zero motion voltage of the gyro
print("Gyro_zeroed at: ", gyro_zero)

R.motors[0].led.colour = (255, 0, 0)
goto_power(R, 70)                       #Accelerate

R.motors[0].led.colour = (0, 255, 0)
stay_at_power(R, 5)                     #Moving constant speed waiting for 5 secs

R.motors[0].led.colour = (255, 0, 0)
goto_power(R, 0)                        #Decelerate


R.motors[0].led.colour = (255, 255, 255)
