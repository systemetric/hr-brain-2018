from sr.robot import *
import time

# Utils
GYRO_CONST = 0.02  # 0.02
GYRO_PIN = 1
GYRO_SAMPLES = 16
GYRO_PROPORTIONAL = 11  # 50

R = Robot()
R.gpio.pin_mode(GYRO_PIN, INPUT_ANALOG)


def average_gyro():
    reading = 0
    for i in range(GYRO_SAMPLES):
        r = R.gpio.analog_read(GYRO_PIN)
        print i, ':', r
        reading += r
        time.sleep(0.06)
    return reading / GYRO_SAMPLES


GYRO_ZERO = average_gyro()
print "Gyro zeroed at:", GYRO_ZERO


def gyro():
    reading = R.gpio.analog_read(GYRO_PIN)
    #print 'G:', reading
    reading -= GYRO_ZERO
    reading /= 8192.0
    return clamp(reading, -1, 1)


last_speed_left = 0
last_speed_right = 0


def clamp(n, smallest, largest):
    if n > largest:
        return largest
    elif n < smallest:
        return smallest
    else:
        return n


def power(robot, p):
    global last_speed_left, last_speed_right

    gyro_pos = gyro()

    adj_left = last_speed_left * gyro_pos * GYRO_PROPORTIONAL
    m_left_speed = clamp(p - adj_left, -70, 70)

    adj_right = last_speed_right * gyro_pos * GYRO_PROPORTIONAL
    m_right_speed = clamp(-p + adj_right, -70, 70)

    robot.motors[0].m0.power = m_left_speed
    robot.motors[0].m1.power = m_right_speed

    #print 'L:', m_left_speed, 'R:', m_right_speed
    #print

    last_speed_left = m_left_speed
    last_speed_right = m_right_speed


def stay_at_power(robot, target, total_time):
    time_elapsed = 0
    while time_elapsed < total_time:
        power(robot, target)

        time.sleep(0.02)
        time_elapsed += 0.02


def spin(robot, total_time):
    global last_speed_left, last_speed_right

    last_speed_left = last_speed_right = 30
    robot.motors[0].m0.power = 30
    robot.motors[0].m1.power = 30

    time.sleep(total_time)

    last_speed_left = last_speed_right = 0
    robot.motors[0].m0.power = 0
    robot.motors[0].m1.power = 0


# Actual Code
seen_cubes = [34]

while True:
    print "Seeing"
    print seen_cubes
    markers = R.see(res=(640, 480), save=False)
    if len(markers) > 0:
        print "Seen", len(markers), "cubes"
        cubes = 0
        for marker in markers:
            if marker.info.code in seen_cubes:
                print "Skipping", marker.info.code
                continue
            elif marker.dist < 0.5:
                print "Added", marker.info.code, " to the list..."
                seen_cubes.append(marker.info.code)
                continue
            cubes += 1
            print "Moving towards", marker.info.code, "..."
            stay_at_power(R, 30, 1)
        if cubes == 0:
            spin(R, 1)
    else:
        print "Looking for cubes..."
        spin(R, 1)
    time.sleep(1)


# spin(R, 1)
#
# stay_at_power(R, 50, 5)
#
# stay_at_power(R, 0, 1)
