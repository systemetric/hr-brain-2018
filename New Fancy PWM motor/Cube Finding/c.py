from sr.robot import *
import time

SERVO_LEFT = 1
SERVO_RIGHT = 2
SERVO_ARM = 3
PIN_PUMP = 2

R = Robot()
R.gpio.pin_mode(PIN_PUMP, OUTPUT)

R.servos[SERVO_LEFT] = 0
R.servos[SERVO_RIGHT] = 0
R.servos[SERVO_ARM] = 0


def pickup():
    R.gpio.digital_write(PIN_PUMP, True)
    R.servos[SERVO_ARM] = -100
    time.sleep(3)


def drop():
    R.gpio.digital_write(PIN_PUMP, False)
    R.servos[SERVO_ARM] = -100


def forward(total_time):
    R.servos[SERVO_LEFT] = 50
    R.servos[SERVO_RIGHT] = -50

    time.sleep(total_time)

    R.servos[SERVO_LEFT] = 0
    R.servos[SERVO_RIGHT] = 0


def spin(total_time):
    R.servos[SERVO_LEFT] = 50
    R.servos[SERVO_RIGHT] = 50

    time.sleep(total_time)

    R.servos[SERVO_LEFT] = 0
    R.servos[SERVO_RIGHT] = 0


# Actual Code
seen_cubes = []

while True:
    print "Seeing"
    print seen_cubes
    markers = R.see(res=(640, 480), save=False)
    if len(markers) > 0:
        print "Seen", len(markers), "cubes"
        cubes = 0

        for marker in markers:
            print "Seen ", marker.info.code, marker.dist, "m away..."
            if marker.info.code in seen_cubes:
                print "Skipping", marker.info.code
                continue
            if marker.dist < 0.5:
                print "Picking up cube..."
                pickup()
                print "Dropping cube..."
                drop()
                print "Adding", marker.info.code, " to the list..."
                seen_cubes.append(marker.info.code)
                continue
            cubes += 1
            print "Moving towards", marker.info.code, "..."
            forward(1)
        if cubes == 0:
            spin(1)
    else:
        print "Looking for cubes..."
        spin(1)
    time.sleep(1)
