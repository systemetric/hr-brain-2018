import socket
import json
import threading
import time
# from sr.robot import Robot  # Comment out for local testing

ACCELERATION = 8
DECAY = 2

host = ""
port = 4096

s = socket.socket()
s.bind((host, port))

motor_power = [0, 0]

MAX_POWER = 40
MIN_POWER = -MAX_POWER

acceleration_left = 0
acceleration_right = 0

power_left = 0
power_right = 0

# R = Robot() # Comment out for local testing


def control_motor():
    global acceleration_left
    global acceleration_right
    global power_left
    global power_right

    while True:
        if power_left > 0:
            power_left -= DECAY
        if power_left < 0:
            power_left += DECAY
        if power_right > 0:
            power_right -= DECAY
        if power_right < 0:
            power_right += DECAY

        power_left += acceleration_left
        power_right += acceleration_right

        if power_left > MAX_POWER:
            power_left = MAX_POWER
        if power_right > MAX_POWER:
            power_right = MAX_POWER
        if power_left < MIN_POWER:
            power_left = MIN_POWER
        if power_right < MIN_POWER:
            power_right = MIN_POWER

        power_left = int(power_left)
        power_right = int(power_right)

        # if acceleration_left > 0:
        #     acceleration_left -= 1
        # if acceleration_left < 0:
        #     acceleration_left += 1
        # if acceleration_right > 0:
        #     acceleration_right -= 1
        # if acceleration_right < 0:
        #     acceleration_right += 1

        print "L:", power_left, "R:", power_right

        # R.motors[0].m0.power = 0.95 * power_left  # Comment out for local testing
        # R.motors[0].m1.power = -1.05 * power_right

        time.sleep(0.5)


motor_control_thread = threading.Thread(target=control_motor)
motor_control_thread.start()


# def see_repeat():  # Comment out for local testing
#     while True:
#         R.see(res=(640, 480), save=True)
#
#
# see_thread = threading.Thread(target=see_repeat)
# see_thread.start()

while True:
    print "Listening for connection..."
    s.listen(1)  # 1 connection at a time

    conn, addr = s.accept()

    print "Connection from " + addr[0] + ":" + str(addr[1]) + "."

    while True:
        try:
            data = conn.recv(1024)

            if not data:  # connection closed
                break

            json_data = str(data)

            data = json.loads(json_data)

            acceleration_left = 0
            acceleration_right = 0

            if data["up"]:
                acceleration_left += ACCELERATION
                acceleration_right += ACCELERATION
            if data["down"]:
                acceleration_left -= ACCELERATION
                acceleration_right -= ACCELERATION
            if data["left"]:
                acceleration_left -= ACCELERATION / 2
                acceleration_right += ACCELERATION / 2
            if data["right"]:
                acceleration_left += ACCELERATION / 2
                acceleration_right -= ACCELERATION / 2

            print data
        except socket.error, msg:
            print "Socket Error: " + msg[1]
            break

    # motor_power[0] = 0  # Comment out for local testing
    # motor_power[1] = 0

    conn.close()
