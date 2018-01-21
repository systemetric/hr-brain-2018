import socket
import json
import threading
import time
# from sr.robot import Robot  # Comment out for local testing

MAX_ACCELERATION = 15

host = ""
port = 4096

s = socket.socket()
s.bind((host, port))

motor_power = [0, 0]

MAX_POWER = 40
MIN_POWER = -MAX_POWER

left_thumbstick_y = 0
right_thumbstick_y = 0

power_left = 0
power_right = 0

# R = Robot() # Comment out for local testing


def control_motor():
    global power_left
    global power_right
    global MAX_ACCELERATION

    while True:
        if (MAX_POWER * left_thumbstick_y) > power_left + MAX_ACCELERATION:  # Avoid overcurrenting the motors
            power_left += MAX_ACCELERATION
        elif (MAX_POWER * left_thumbstick_y) < power_left - MAX_ACCELERATION:
            power_left -= MAX_ACCELERATION
        else:
            power_left = int(MAX_POWER * left_thumbstick_y)

        if (MAX_POWER * right_thumbstick_y) > power_right + MAX_ACCELERATION:  # Avoid overcurrenting the motors
            power_right += MAX_ACCELERATION
        elif (MAX_POWER * right_thumbstick_y) < power_right - MAX_ACCELERATION:
            power_right -= MAX_ACCELERATION
        else:
            power_right = int(MAX_POWER * right_thumbstick_y)

        print "L:", power_left, "R:", power_right

        # R.motors[0].m0.power = 0.95 * power_left  # Comment out for local testing
        # R.motors[0].m1.power = -1.05 * power_right

        time.sleep(0.2)


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

            left_thumbstick_y = data["LThumbstick_Y"]
            right_thumbstick_y = data["RThumbstick_Y"]

            print data
        except socket.error, msg:
            print "Socket Error: " + msg[1]
            break

    # motor_power[0] = 0  # Comment out for local testing
    # motor_power[1] = 0

    conn.close()
