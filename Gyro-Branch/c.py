from sr.robot import *
import time

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
    print 'G:', reading
    reading -= GYRO_ZERO
    reading /= 8192.0
    # reading *= 100.0
    # reading = int(reading)
    # reading /= 100.0
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

    print 'L:', m_left_speed, 'R:', m_right_speed
    print

    last_speed_left = m_left_speed
    last_speed_right = m_right_speed


def goto_power(robot, target):
    difference = target - int(last_speed_left)
    step = (1 if difference > 0 else -1)

    for j in range(int(last_speed_left), target, step):
        power(robot, j)

        time.sleep(0.02)


def stay_at_power(robot, target, total_time):
    time_elapsed = 0
    while time_elapsed < total_time:
        power(robot, target)

        time.sleep(0.02)
        time_elapsed += 0.02


stay_at_power(R, 50, 5)

stay_at_power(R, 0, 1)
